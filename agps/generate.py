"""Generates NML_28A.ee (Nikon A-GPS) from IGS data.

Usage:  python -m agps.generate --out out [--data DATA_FOLDER] [--no-download] [--now 2026-11-13T15:30]
"""
import argparse, datetime, glob, math, os, sys, time
from multiprocessing import Pool
import numpy as np
from scipy.optimize import least_squares
from . import orbit, brdc, download, nml28a as N

MU = N.MU; OE = N.OMEGA_E; TWO = 2 * math.pi
EXCLUDE = (1, 22, 30)   # missing in all original Nikon files 2015-2026
DAY = 86400.0
HERE = os.path.dirname(os.path.abspath(__file__))
GRAV = os.path.join(HERE, "..", "data", "JGM3.gfc")


# ------------------------------------------------------------ ephemeris fit
def model(x, toe, t):
    sqrtA, e, i0, Om, w, M0, dn, Omd, idot, cuc, cus, crc, crs, cic, cis = x
    A = sqrtA * sqrtA; n = math.sqrt(MU / A ** 3) + dn; tk = t - toe
    M = M0 + n * tk; E = M.copy()
    for _ in range(10): E = M + e * np.sin(E)
    v = np.arctan2(math.sqrt(1 - e * e) * np.sin(E), np.cos(E) - e)
    phi = v + w; s2 = np.sin(2 * phi); c2 = np.cos(2 * phi)
    u = phi + cus * s2 + cuc * c2; r = A * (1 - e * np.cos(E)) + crs * s2 + crc * c2; i = i0 + cis * s2 + cic * c2 + idot * tk
    om = Om + (Omd - OE) * tk
    xp = r * np.cos(u); yp = r * np.sin(u)
    return np.stack([xp * np.cos(om) - yp * np.cos(i) * np.sin(om), xp * np.sin(om) + yp * np.cos(i) * np.cos(om), yp * np.sin(i)], axis=1)


def osculating(r, v):
    h = np.cross(r, v); hn = np.linalg.norm(h); rn = np.linalg.norm(r)
    i = math.acos(h[2] / hn); Om = math.atan2(h[0], -h[1])
    ev = np.cross(v, h) / MU - r / rn; e = np.linalg.norm(ev)
    a = 1 / (2 / rn - v @ v / MU)
    nd = np.array([math.cos(Om), math.sin(Om), 0.0])
    u = math.atan2(r @ np.cross(h / hn, nd), r @ nd)
    w = math.atan2(ev @ np.cross(h / hn, nd), ev @ nd)
    nu = u - w; E = 2 * math.atan2(math.sqrt(1 - e) * math.sin(nu / 2), math.sqrt(1 + e) * math.cos(nu / 2))
    return [math.sqrt(a), e, i, Om, w, E - e * math.sin(E)]


SC = np.array([0.1, 1e-4, 1e-4, 1e-4, 1e-4, 1e-4, 1e-8, 1e-8, 1e-8, 1e-4, 1e-4, 1e3, 1e3, 1e-4, 1e-4])
KW = dict(xtol=1e-14, ftol=1e-14, gtol=1e-14, max_nfev=3000)


def _rms(fun):
    return math.sqrt((fun ** 2).reshape(-1, 3).sum(1).mean())


def fit_sat(args):
    prn, t, xe, T0 = args
    out = []; rmsl = []
    for k in range(112):
        toe = T0 + 21600 * k + 10800
        sl = slice(24 * k, 24 * k + 25); tt = t[sl]; xx = xe[sl]; c = 24 * k + 12
        lo = max(0, min(c - 5, len(t) - 11)); st = orbit.initial_state(t[lo:lo + 11], xe[lo:lo + 11], toe)
        x0 = np.array(osculating(xe[c], st[3:] + np.cross([0, 0, OE], xe[c])) + [0] * 9)
        s = least_squares(lambda z: (model(x0 + z * SC, toe, tt) - xx).ravel(), np.zeros(15), method="lm", diff_step=1e-6, **KW)
        out.append(x0 + s.x * SC); rmsl.append(_rms(s.fun))

    def shift(x, steps):
        y = x.copy(); n = math.sqrt(MU / x[0] ** 6) + x[6]; dt = 21600 * steps
        y[5] += n * dt; y[3] += (x[7] - OE) * dt; y[2] += x[8] * dt
        return y
    med = np.median(rmsl); lim = max(4.0, 3 * med)
    for _ in range(3):   # retry poor windows with start values taken from their neighbours
        bad = [k for k in range(112) if rmsl[k] > lim]
        if not bad: break
        for k in bad:
            toe = T0 + 21600 * k + 10800; sl = slice(24 * k, 24 * k + 25); tt = t[sl]; xx = xe[sl]
            for nb in (k - 1, k + 1, k - 2, k + 2):
                if not (0 <= nb < 112) or rmsl[nb] > lim: continue
                x0 = shift(out[nb], k - nb)
                f = lambda z: (model(x0 + z * SC, toe, tt) - xx).ravel()
                for meth, kw in (("lm", dict(diff_step=1e-6)), ("trf", dict(x_scale="jac"))):
                    s = least_squares(f, np.zeros(15), method=meth, **kw, **KW)
                    if _rms(s.fun) < rmsl[k]: rmsl[k] = _rms(s.fun); out[k] = x0 + s.x * SC
    return prn, np.array(out), np.array(rmsl)


# ------------------------------------------------------------ encoding
def encode_robust(ints, width):
    k = np.arange(28.); y = np.array(ints, float); note = ""
    A = np.stack([np.ones(28), k, k * k, k ** 3 / 256], 1)
    c = np.linalg.lstsq(A, y, rcond=None)[0]
    L3 = (1 << 19) - 1; L2 = (1 << 23) - 1
    if abs(c[3]) > L3:
        c3 = math.copysign(L3, c[3]); c = np.append(np.linalg.lstsq(A[:, :3], y - c3 * A[:, 3], rcond=None)[0], c3); note = "h3"
    if abs(c[2]) > L2:
        c2 = math.copysign(L2, c[2]); cc = np.linalg.lstsq(A[:, :2], y - c2 * A[:, 2] - c[3] * A[:, 3], rcond=None)[0]
        c = np.array([cc[0], cc[1], c2, c[3]]); note += " h2"
    h = [int(round(v)) for v in c]
    lim = (1 << (width - 1)) - 1
    raw = [int(round(ints[j] - (h[0] + h[1] * j + h[2] * j * j + h[3] * j ** 3 / 256))) for j in range(28)]
    s = [max(-lim, min(lim, v)) for v in raw]
    if s != raw: note += " residual"
    return dict(h=h, z=0, s=s), note.strip()


ORDER = ["sqrtA", "e", "i0", "raan", "M0", "omega", "idot", "omegadot", "deltan", "crc", "crs", "cic", "cis", "cuc", "cus"]
COL = dict(sqrtA=0, e=1, i0=2, omega=4, M0=5, deltan=6, omegadot=7, idot=8, cuc=9, cus=10, crc=11, crs=12, cic=13, cis=14)


def build_blocks(T0, eph, latest, log, clock_fn=None):
    blocks = []
    for b in range(4):
        Tb = int(T0 + 604800 * b); slots = []
        for prn in range(1, 33):
            empty = [dict(h=[0, 0, 0, 0], z=0, s=[0] * 28) for _ in N.PARAMS]
            br = latest.get(prn); af0 = af1 = 0
            if br and clock_fn and prn in clock_fn:
                # predicted clock: best straight line over this block's week
                tt = Tb + 3600.0 * np.arange(169); cc = clock_fn[prn](tt)
                c1, c0 = np.polyfit(tt - Tb, cc, 1)
                af1 = int(round(c1 / N.AF1_LSB)); af0 = int(round(c0 / N.AF0_LSB))
            elif br:
                af1 = int(round(br["af1"] / N.AF1_LSB)); af0 = int(round((br["af0"] + br["af1"] * (Tb - br["toc"])) / N.AF0_LSB))
                if not (-2 ** 31 <= af0 < 2 ** 31 and -2 ** 23 <= af1 < 2 ** 23): br = None; af0 = af1 = 0
            if prn == 1:
                slots.append(dict(prn=0, status=0xFF, af0=0, af1=0, reserved=0, sections=empty)); continue
            if not (prn in eph and br and br["health"] == 0 and prn not in EXCLUDE):
                slots.append(dict(prn=prn, status=0xFF, af0=af0, af1=af1, reserved=0, sections=empty)); continue
            X = eph[prn][28 * b:28 * b + 28].copy()
            toe = Tb + 21600 * np.arange(28) + 10800
            for k in range(1, 28):
                n = math.sqrt(MU / X[k - 1, 0] ** 6) + X[k - 1, 6]
                X[k, 5] += TWO * round((X[k - 1, 5] + n * 21600 - X[k, 5]) / TWO)
                X[k, 4] += TWO * round((X[k - 1, 4] - X[k, 4]) / TWO)
            raan = np.array([X[k, 3] + OE * (toe[k] % 604800) + N.gmst(toe[k] - toe[k] % 604800) for k in range(28)])
            for k in range(1, 28): raan[k] += TWO * round((raan[k - 1] - raan[k]) / TWO)
            raan -= TWO * math.floor(raan[0] / TWO); X[:, 5] -= TWO * math.floor(X[0, 5] / TWO); X[:, 4] -= TWO * math.floor(X[0, 4] / TWO)
            secs = []
            for name, (pname, width, lsb, _) in zip(ORDER, N.PARAMS):
                vals = raan if name == "raan" else X[:, COL[name]]
                sec, note = encode_robust([int(round(v / lsb)) for v in vals], width)
                if note: log.append("block %d PRN %d %s: %s clipped" % (b + 1, prn, name, note))
                secs.append(sec)
            slots.append(dict(prn=prn, status=0, af0=af0, af1=af1, reserved=0, sections=secs))
        blocks.append(dict(t=Tb, index=b, count=4, slots=slots))
    return blocks


# ------------------------------------------------------------ main flow
def read_leap(path):
    for line in open(path):
        if "LEAP SECONDS" in line: return int(line.split()[0])
        if "END OF HEADER" in line: break
    return None


DEFAULTS = dict(clock="broadcast", srp="ecom1", arc="5")


def parse_opts(text):
    """'clock=quad5,srp=ecom2,arc=7' -> dict, missing keys from DEFAULTS.
    clock: broadcast | linN | quadN (fit to the last N days of IGS clocks); srp: ecom1 | ecom2; arc: longest fit arc in days."""
    o = dict(DEFAULTS)
    for part in filter(None, (text or "").split(",")):
        k, v = part.split("=", 1); o[k.strip()] = v.strip()
    return o


def make_clock_fn(data, now_gps, latest, spec, notes):
    """Clock predictions from a polynomial fit to IGS clocks, shifted to the broadcast time scale."""
    import re
    m = re.match(r"^(lin|quad)(\d+(?:\.\d+)?)$", spec)
    if not m: raise ValueError("unknown clock model " + spec)
    deg = 1 if m.group(1) == "lin" else 2; days = float(m.group(2))
    clocks = orbit.load_clocks(data, now_gps)
    cfs = {p: orbit.clock_model(t, c, now_gps, days, deg) for p, (t, c) in clocks.items()}
    cfs = {p: cf for p, cf in cfs.items() if cf is not None and p in latest}
    if len(cfs) < 20:
        notes.append("clock model %s: only %d satellites, using broadcast clocks" % (spec, len(cfs))); return None
    # IGS clocks and broadcast clocks differ by an offset common to all satellites: take the median at `now`
    off = np.median([latest[p]["af0"] + latest[p]["af1"] * (now_gps - latest[p]["toc"]) - np.polyval(cf, 0.0) for p, cf in cfs.items()])
    return {p: (lambda tt, cf=cf: np.polyval(cf, (np.asarray(tt) - now_gps) / 86400.0) + off) for p, cf in cfs.items()}


def build(data, out, now, freeze_eop=False, keep_on_fail=False, opts=None):
    """Generates out/NML_28A.ee and out/status.md from the IGS files in `data`, using only data up to `now`.
    freeze_eop: extrapolate Earth rotation parameters after `now` (for hindcasts). opts: see parse_opts.
    Returns a result dict."""
    opts = parse_opts(opts) if not isinstance(opts, dict) else opts
    npar = {"ecom1": 5, "ecom2": 9}[opts["srp"]]
    arc = float(opts["arc"])
    os.makedirs(out, exist_ok=True)
    # broadcast data: clocks, health, leap seconds
    bfiles = sorted(glob.glob(os.path.join(data, "BRDC*MN.rnx")), key=lambda p: os.path.basename(p).split("_")[2])
    leap = next((l for l in (read_leap(f) for f in reversed(bfiles)) if l), None)
    if leap: orbit.LEAP = leap
    now_gps = (now - datetime.datetime(1980, 1, 6)).total_seconds() + orbit.LEAP
    allb = [r for f in bfiles for r in brdc.read_rinex3_gps(f) if r["toc"] <= now_gps + 4 * 3600]
    latest = {}
    for r in allb:
        if r["prn"] not in latest or r["toc"] > latest[r["prn"]]["toc"]: latest[r["prn"]] = r
    if len(latest) < 24: raise RuntimeError("only %d satellites in the broadcast data" % len(latest))

    eop = orbit.EOP(data); truth = orbit.load_truth(data); force = orbit.Force(eop, GRAV)
    if freeze_eop: eop.frozen_after = float(orbit.mjd_utc(now_gps))
    truth = {p: (t[t <= now_gps], x[t <= now_gps]) for p, (t, x) in truth.items()}
    t_last = max(v[0][-1] for v in truth.values())
    print("orbit data until %s, %d satellites" % (N.gps_datetime(t_last).strftime("%Y-%m-%d %H:%M"), len(truth)), flush=True)

    # orbit fit with staggered arc lengths (manoeuvres shorten the arc)
    res = {}; todo = sorted(truth); notes = []
    for days, lim in ((arc, 3.0), (arc / 2, 10.0), (1.0, 30.0)):
        t_s = t_last - days * DAY
        ok = []
        for p in todo:
            ts = truth[p][0]; k = ts >= t_s - 1
            if k.sum() >= 0.75 * days * 96 and ts[k][0] - t_s < 1900 and t_last - ts[-1] < 1900: ok.append(p)
        if not ok: continue
        tic = time.time()
        t0, y0, p_, rms = orbit.fit_orbits(force, truth, eop, ok, t_s, t_last, verbose=False, iters=5, npar=npar)
        print("fit over %.1f days: %d satellites, %.0f s" % (days, len(ok), time.time() - tic), flush=True)
        for n, p in enumerate(ok):
            if rms[n] <= lim: res[p] = dict(t0=t0, y0=y0[n], p=p_[n], rms=float(rms[n]), arc=days)
            else: notes.append("PRN %d: %.1f m residual error over %.1f days" % (p, rms[n], days))
        todo = [p for p in todo if p not in res]
    if todo: notes.append("no orbit: PRN " + ", ".join(map(str, todo)))
    if len(res) < 24:
        raise RuntimeError("only %d satellites could be fitted (data gap in the orbit files?)" % len(res))

    # file start: last 14:00 GPS time before now (as in the original Nikon files)
    T0 = math.floor((now_gps - 14 * 3600) / DAY) * DAY + 14 * 3600
    grid = T0 + 900.0 * np.arange(112 * 24 + 1)
    ecef = {}
    tic = time.time()
    for t0 in sorted(set(r["t0"] for r in res.values())):
        ps = [p for p in sorted(res) if res[p]["t0"] == t0]
        traj = force.propagate(t0, np.array([res[p]["y0"] for p in ps]), np.array([res[p]["p"] for p in ps]), grid)
        for n, p in enumerate(ps): ecef[p] = orbit.gcrs_to_ecef(grid, traj[:, n, :3], eop)
    print("28-day prediction: %.0f s" % (time.time() - tic), flush=True)
    tic = time.time()
    with Pool() as pool: R = pool.map(fit_sat, [(p, grid, ecef[p], T0) for p in sorted(ecef)])
    eph = {}
    for p, x, r in R:
        if r.max() < 30: eph[p] = x
        else: notes.append("PRN %d: ephemeris fit %.0f m, skipped" % (p, r.max()))
    print("ephemeris fit: %.0f s" % (time.time() - tic), flush=True)

    clock_fn = None if opts["clock"] == "broadcast" else make_clock_fn(data, now_gps, latest, opts["clock"], notes)
    blocks = build_blocks(T0, eph, latest, notes, clock_fn)
    target = os.path.join(out, "NML_28A.ee")
    N.write_file(target, blocks)

    # ---------------- checks: decode the file and compare
    B = N.read_file(target)
    E = {}
    for b in B:
        for s in b["slots"]:
            if s["status"] == 0: E.setdefault(s["prn"], []).extend(N.ephemerides(b, s))
    own = [np.linalg.norm(np.array(N.ecef(eps[min(int((grid[j] - T0) // 21600), 111)], grid[j])) - ecef[prn][j])
           for prn, eps in E.items() for j in range(0, len(grid) - 1, 4)]
    bro = []
    for x in allb:
        if x["prn"] in E and x["health"] == 0 and x["toe"] >= T0 and x["toe"] < T0 + 28 * DAY:
            t = x["toe"]; bro.append(np.linalg.norm(np.array(N.ecef(E[x["prn"]][int((t - T0) // 21600)], t)) - np.array(N.ecef(x, t))))
    ult = []
    ufiles = sorted(glob.glob(os.path.join(data, "*OPSULT*ORB.SP3")))
    if ufiles:
        for prn, arr in orbit.read_sp3(ufiles[-1]).items():
            if prn in E:
                for row in arr[arr[:, 0] >= T0]:
                    ult.append(np.linalg.norm(np.array(N.ecef(E[prn][int((row[0] - T0) // 21600)], row[0])) - row[1:4]))
    nsat = len(E)
    med = lambda v: float(np.median(v)) if len(v) else float("nan")
    checks = [("CRC of all blocks", all(b["crc_ok"] for b in B)),
              ("at least 24 satellites (%d)" % nsat, nsat >= 24),
              ("file vs. own prediction (median %.1f m, max %.1f m)" % (med(own), max(own, default=float("nan"))), len(own) > 0 and max(own) < 50),
              ("file vs. IGS prediction (median %.1f m, %d comparisons)" % (med(ult), len(ult)), len(ult) == 0 or med(ult) < 25),
              ("file vs. broadcast ephemerides (median %.1f m, %d comparisons)" % (med(bro), len(bro)), len(bro) == 0 or med(bro) < 25)]
    ok = all(c[1] for c in checks)
    end = N.gps_datetime(T0 + 28 * DAY)
    lines = ["# A-GPS file status", "",
             "- Model: " + ", ".join("%s=%s" % kv for kv in sorted(opts.items())),
             "- Generated: %s UTC" % now.strftime("%Y-%m-%d %H:%M"),
             "- Valid: %s to %s (GPS time)" % (N.gps_datetime(T0).strftime("%Y-%m-%d %H:%M"), end.strftime("%Y-%m-%d %H:%M")),
             "- Orbit data until: %s" % N.gps_datetime(t_last).strftime("%Y-%m-%d %H:%M"),
             "- Satellites (%d): %s" % (nsat, " ".join(str(p) for p in sorted(E))), "", "## Checks", ""]
    lines += ["- %s %s" % ("OK   " if c[1] else "FAIL", c[0]) for c in checks]
    if notes: lines += ["", "## Notes", ""] + ["- " + n for n in notes]
    open(os.path.join(out, "status.md"), "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))
    if not ok and not keep_on_fail:
        os.remove(target)
    return dict(ok=ok, target=target, T0=T0, now_gps=now_gps, notes=notes, checks=checks)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="out"); ap.add_argument("--data", default="igs-data")
    ap.add_argument("--no-download", action="store_true"); ap.add_argument("--now", default=None)
    ap.add_argument("--opts", default="", help="model options, e.g. clock=quad5,srp=ecom2,arc=7")
    a = ap.parse_args()
    now = datetime.datetime.fromisoformat(a.now) if a.now else datetime.datetime.utcnow()
    if not a.no_download:
        print("Downloading IGS data ...", flush=True); download.download_all(a.data, now)
    r = build(a.data, a.out, now, opts=a.opts)
    if not r["ok"]:
        sys.exit("ERROR: checks failed, file discarded")


if __name__ == "__main__":
    main()
