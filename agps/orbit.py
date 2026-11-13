"""GPS orbit model: force model, numerical integration, orbit fit to SP3 positions."""
import math, glob, os
import numpy as np
import erfa
from scipy.integrate import solve_ivp

GM = 3.986004415e14
RE = 6378136.3
GM_SUN = 1.32712440018e20
GM_MOON = 4.9028e12
AU = 149597870700.0
CLIGHT = 299792458.0
LEAP = 18
R_SUN = 6.96e8
NMAX = 8


# ---------------------------------------------------------------- time / EOP
def mjd_utc(t):
    return 44244.0 + (np.asarray(t, float) - LEAP) / 86400.0


class EOP:
    def __init__(self, folder):
        rows = {}
        for f in sorted(glob.glob(os.path.join(folder, "*ERP.ERP"))):
            for line in open(f):
                p = line.split()
                if len(p) > 5 and p[0].replace(".", "").isdigit() and "." in p[0]:
                    rows[float(p[0])] = (float(p[1]) * 1e-6, float(p[2]) * 1e-6, float(p[3]) * 1e-7, float(p[4]) * 1e-7)
        m = np.array(sorted(rows))
        v = np.array([rows[k] for k in m])
        self.mjd, self.xp, self.yp, self.dut, self.lod = m, v[:, 0], v[:, 1], v[:, 2], v[:, 3]
        self.frozen_after = None  # for hindcast tests: EOP after this date are extrapolated only

    def get(self, t):
        m = np.atleast_1d(mjd_utc(t))
        mj, xp, yp, dut, lod = self.mjd, self.xp, self.yp, self.dut, self.lod
        if self.frozen_after is not None:
            k = mj <= self.frozen_after
            mj, xp, yp, dut, lod = mj[k], xp[k], yp[k], dut[k], lod[k]
        x = np.interp(m, mj, xp); y = np.interp(m, mj, yp); d = np.interp(m, mj, dut)
        late = m > mj[-1]
        if late.any():
            lod_mean = lod[-5:].mean()
            d[late] = dut[-1] - lod_mean * (m[late] - mj[-1])
        return x, y, d


def c2t(t, eop):
    """GCRS -> ITRS rotation matrices for GPS times t (array)."""
    t = np.atleast_1d(np.asarray(t, float))
    xp, yp, dut = eop.get(t)
    asec = math.pi / 180 / 3600
    tt = (t + 51.184) / 86400.0
    ut = (t - LEAP + dut) / 86400.0
    return erfa.c2t06a(2444244.5, tt, 2444244.5, ut, xp * asec, yp * asec)


def sun_moon(t):
    t = np.atleast_1d(np.asarray(t, float))
    tt = (t + 51.184) / 86400.0
    pvh, _ = erfa.epv00(2444244.5, tt)
    sun = -pvh["p"] * AU
    moon = erfa.moon98(2444244.5, tt)["p"] * AU
    return sun, moon


# ---------------------------------------------------------------- gravity field
def load_gravity(path, nmax=NMAX):
    C = np.zeros((nmax + 2, nmax + 2)); S = np.zeros((nmax + 2, nmax + 2))
    for line in open(path):
        p = line.split()
        if p and p[0] == "gfc":
            n, m = int(p[1]), int(p[2])
            if n <= nmax:
                k = math.sqrt((2 - (m == 0)) * (2 * n + 1) * math.factorial(n - m) / math.factorial(n + m))
                C[n, m] = float(p[3]) * k; S[n, m] = float(p[4]) * k
    return C, S


def accel_harmonic(r, C, S, nmax=NMAX):
    """Acceleration in the Earth-fixed frame (Cunningham recursion), r: (N,3)."""
    x, y, z = r[:, 0], r[:, 1], r[:, 2]
    r2 = x * x + y * y + z * z
    rho = RE * RE / r2
    x0, y0, z0 = RE * x / r2, RE * y / r2, RE * z / r2
    N = len(x)
    V = np.zeros((nmax + 2, nmax + 2, N)); W = np.zeros((nmax + 2, nmax + 2, N))
    V[0, 0] = RE / np.sqrt(r2)
    V[1, 0] = z0 * V[0, 0]
    for n in range(2, nmax + 2):
        V[n, 0] = ((2 * n - 1) * z0 * V[n - 1, 0] - (n - 1) * rho * V[n - 2, 0]) / n
    for m in range(1, nmax + 2):
        V[m, m] = (2 * m - 1) * (x0 * V[m - 1, m - 1] - y0 * W[m - 1, m - 1])
        W[m, m] = (2 * m - 1) * (x0 * W[m - 1, m - 1] + y0 * V[m - 1, m - 1])
        if m <= nmax:
            V[m + 1, m] = (2 * m + 1) * z0 * V[m, m]
            W[m + 1, m] = (2 * m + 1) * z0 * W[m, m]
        for n in range(m + 2, nmax + 2):
            V[n, m] = ((2 * n - 1) * z0 * V[n - 1, m] - (n + m - 1) * rho * V[n - 2, m]) / (n - m)
            W[n, m] = ((2 * n - 1) * z0 * W[n - 1, m] - (n + m - 1) * rho * W[n - 2, m]) / (n - m)
    ax = np.zeros(N); ay = np.zeros(N); az = np.zeros(N)
    for n in range(0, nmax + 1):
        for m in range(0, n + 1):
            c, s = C[n, m], S[n, m]
            if c == 0 and s == 0:
                continue
            if m == 0:
                ax -= c * V[n + 1, 1]; ay -= c * W[n + 1, 1]; az -= (n + 1) * c * V[n + 1, 0]
            else:
                fac = 0.5 * (n - m + 1) * (n - m + 2)
                ax += 0.5 * (-c * V[n + 1, m + 1] - s * W[n + 1, m + 1]) + fac * (c * V[n + 1, m - 1] + s * W[n + 1, m - 1])
                ay += 0.5 * (-c * W[n + 1, m + 1] + s * V[n + 1, m + 1]) + fac * (-c * W[n + 1, m - 1] + s * V[n + 1, m - 1])
                az += (n - m + 1) * (-c * V[n + 1, m] - s * W[n + 1, m])
    return (GM / (RE * RE)) * np.stack([ax, ay, az], axis=1)


# ---------------------------------------------------------------- forces
class Force:
    def __init__(self, eop, gravfile):
        self.eop = eop
        self.C, self.S = load_gravity(gravfile)

    def accel(self, t, r, v, p):
        """r, v: (N,3) in GCRS; p: (N,5) solar radiation pressure parameters D0,Y0,B0,Bc,Bs."""
        M = c2t(t, self.eop)[0]
        a = accel_harmonic(r @ M.T, self.C, self.S) @ M
        sun, moon = sun_moon(t); sun = sun[0]; moon = moon[0]
        rn = np.linalg.norm(r, axis=1, keepdims=True)
        rh = r / rn
        for body, gm in ((sun, GM_SUN), (moon, GM_MOON)):
            d = body - r
            dn = np.linalg.norm(d, axis=1, keepdims=True)
            sn = np.linalg.norm(body)
            a += gm * (d / dn ** 3 - body / sn ** 3)
            # solid Earth tides (k2)
            sh = body / sn
            cth = rh @ sh
            a += (0.3 / 2) * (gm / sn ** 3) * (RE ** 5 / rn ** 4) * ((3 - 15 * cth[:, None] ** 2) * rh + 6 * cth[:, None] * sh)
        # relativity (Schwarzschild)
        v2 = np.sum(v * v, axis=1, keepdims=True); rv = np.sum(r * v, axis=1, keepdims=True)
        a += GM / (CLIGHT ** 2 * rn ** 3) * ((4 * GM / rn - v2) * r + 4 * rv * v)
        # solar radiation pressure (ECOM) with Earth shadow
        d = sun - r
        dn = np.linalg.norm(d, axis=1, keepdims=True)
        eD = d / dn
        eY = np.cross(eD, rh); eY /= np.linalg.norm(eY, axis=1, keepdims=True)
        eB = np.cross(eD, eY)
        h = np.cross(r, v); h /= np.linalg.norm(h, axis=1, keepdims=True)
        node = np.stack([-h[:, 1], h[:, 0], np.zeros(len(h))], axis=1)
        node /= np.linalg.norm(node, axis=1, keepdims=True)
        u = np.arctan2(np.sum(r * np.cross(h, node), axis=1), np.sum(r * node, axis=1))
        # shadow: distance from the shadow axis, smooth transition across the penumbra
        sh = sun / np.linalg.norm(sun)
        s_along = r @ sh
        perp = np.linalg.norm(r - s_along[:, None] * sh, axis=1)
        pen = np.abs(s_along) * R_SUN / np.linalg.norm(sun)
        nu = np.where(s_along < 0, np.clip((perp - (RE - pen)) / (2 * pen), 0, 1), 1.0)
        scale = (AU / dn) ** 2 * nu[:, None]
        a += scale * (p[:, 0:1] * eD + p[:, 1:2] * eY + (p[:, 2:3] + p[:, 3:4] * np.cos(u)[:, None] + p[:, 4:5] * np.sin(u)[:, None]) * eB)
        return a

    def propagate(self, t0, y0, p, t_eval, rtol=1e-10):
        """y0: (N,6), p: (N,5). Returns (len(t_eval), N, 6)."""
        N = len(y0)

        def f(t, y):
            y = y.reshape(N, 6)
            return np.concatenate([y[:, 3:], self.accel(t0 + t, y[:, :3], y[:, 3:], p)], axis=1).ravel()

        te = np.asarray(t_eval, float) - t0
        fwd = te[te >= 0]; bwd = te[te < 0]
        out = np.zeros((len(te), N, 6))
        atol = np.tile([1e-4] * 3 + [1e-7] * 3, N)
        if len(fwd):
            s = solve_ivp(f, (0, fwd.max() if fwd.max() > 0 else 1), y0.ravel(), method="DOP853", t_eval=fwd, rtol=rtol, atol=atol, first_step=60)
            out[te >= 0] = s.y.T.reshape(-1, N, 6)
        if len(bwd):
            s = solve_ivp(f, (0, bwd.min()), y0.ravel(), method="DOP853", t_eval=bwd[::-1], rtol=rtol, atol=atol, first_step=60)
            out[te < 0] = s.y.T.reshape(-1, N, 6)[::-1]
        return out


# ---------------------------------------------------------------- SP3
GPS0 = __import__("datetime").datetime(1980, 1, 6)


def read_sp3(path):
    """-> dict prn -> (t[], xyz[] in m, clk[] in s)"""
    import datetime
    data = {}
    t = None
    for line in open(path):
        if line.startswith("*  "):
            y, mo, d, h, mi = (int(x) for x in line[3:19].split())
            s = float(line[19:31])
            t = (datetime.datetime(y, mo, d, h, mi) - GPS0).total_seconds() + s
        elif line.startswith("PG") and t is not None:
            prn = int(line[2:4])
            x, y_, z, c = (float(line[4 + 14 * i:18 + 14 * i]) for i in range(4))
            if abs(x) + abs(y_) + abs(z) < 1:
                continue
            pred = len(line) > 75 and line[75] == "P"
            data.setdefault(prn, []).append((t, x * 1e3, y_ * 1e3, z * 1e3, c * 1e-6 if c < 999999 else np.nan, pred))
    return {k: np.array(v) for k, v in data.items()}


def load_truth(folder, include_ultra=True, ultra_observed_only=True):
    """Merge all SP3 files: prn -> (t, xyz ECEF)."""
    merged = {}
    files = sorted(glob.glob(os.path.join(folder, "*OPSRAP*ORB.SP3")))
    if include_ultra:
        files += sorted(glob.glob(os.path.join(folder, "*OPSULT*ORB.SP3")))
    for f in files:
        ult = "OPSULT" in f
        d = read_sp3(f)
        for prn, a in d.items():
            if ult and ultra_observed_only:
                a = a[a[:, 0] < a[0, 0] + 86400]  # first 24 h are observed, the rest is predicted
            m = merged.setdefault(prn, {})
            for row in a:
                m.setdefault(row[0], row[1:4])  # Rapid takes precedence (loaded first)
    out = {}
    for prn, m in merged.items():
        ts = np.array(sorted(m))
        out[prn] = (ts, np.array([m[k] for k in ts]))
    return out


def ecef_to_gcrs(t, xyz, eop):
    M = c2t(t, eop)
    return np.einsum("nji,nj->ni", M, xyz)


def gcrs_to_ecef(t, xyz, eop):
    M = c2t(t, eop)
    return np.einsum("nij,nj->ni", M, xyz)


def initial_state(ts, xi, t0):
    """Initial state from inertial positions: polynomial through 11 points around t0."""
    i = int(np.argmin(np.abs(ts - t0)))
    lo = max(0, min(i - 5, len(ts) - 11))
    tt = ts[lo:lo + 11]; xx = xi[lo:lo + 11]
    s = (tt - t0) / 3600.0
    V = np.vander(s, 11, increasing=True)
    coef = np.linalg.solve(V, xx)
    return np.concatenate([coef[0], coef[1] / 3600.0])


def fit_orbits(force, truth, eop, prns, t_start, t_end, iters=4, verbose=True, step=900):
    """Fits initial state + 5 radiation pressure parameters per satellite. Returns t0, y0 (N,6), p (N,5), rms (N)."""
    t0 = t_start
    grid = np.arange(t_start, t_end + 1, step)
    obs = []; y0 = []
    for prn in prns:
        ts, xe = truth[prn]
        k = (ts >= t_start - 1e-3) & (ts <= t_end + 1e-3)
        tk = ts[k]
        xi = ecef_to_gcrs(tk, xe[k], eop)
        full = np.full((len(grid), 3), np.nan)
        full[np.round((tk - t_start) / step).astype(int)] = xi
        obs.append(full)
        y0.append(initial_state(tk, xi, t0))
    obs = np.array(obs)            # (N, T, 3)
    y0 = np.array(y0); N = len(prns)
    p = np.tile([-1.0e-7, 0, 0, 0, 0], (N, 1))
    dpar = np.array([10.0] * 3 + [1e-3] * 3 + [2e-9] * 5)
    rms = None
    for it in range(iters):
        Y = np.repeat(y0, 12, axis=0); P = np.repeat(p, 12, axis=0)
        for j in range(11):
            idx = np.arange(N) * 12 + 1 + j
            if j < 6: Y[idx, j] += dpar[j]
            else: P[idx, j - 6] += dpar[j]
        traj = force.propagate(t0, Y, P, grid)[:, :, :3]   # (T, 12N, 3)
        traj = traj.transpose(1, 0, 2).reshape(N, 12, len(grid), 3)
        res = obs - traj[:, 0]                             # (N,T,3)
        rms = np.sqrt(np.nanmean((res ** 2).sum(axis=2), axis=1))
        res = np.nan_to_num(res)
        if verbose:
            print("  iteration %d: fit error median %.3f m, max %.3f m" % (it, np.median(rms), rms.max()), flush=True)
        if it == iters - 1:
            break
        for n in range(N):
            J = np.stack([(traj[n, 1 + j] - traj[n, 0]).ravel() / dpar[j] for j in range(11)], axis=1)
            dx = np.linalg.lstsq(J, res[n].ravel(), rcond=None)[0]
            y0[n] += dx[:6]; p[n] += dx[6:]
    return t0, y0, p, rms
