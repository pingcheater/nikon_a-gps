"""Hindcast: generate files as if it were an earlier date and compare them with the orbits and clocks measured later.

Usage:
  python -m agps.hindcast run --start 2026-09-07 --out hc [--data hc-data] [--label baseline] [--no-download]
  python -m agps.hindcast summary --inp results-folder --out hindcast/baseline [--label baseline]
"""
import argparse, csv, datetime, glob, os, sys, warnings
import numpy as np
from . import orbit, generate, download, nml28a as N

C = 299792458.0
warnings.filterwarnings("ignore", message="All-NaN slice")
DAY = 86400.0
FIELDS = ["label", "start", "prn", "day", "n", "pos_med", "pos_p95", "pos_max", "clk_med", "clk_rel_med", "eclipse_min"]


def load_truth_with_clock(folder):
    """prn -> (t, xyz ECEF [m], clock [s]) from all rapid SP3 files."""
    rows = {}
    for f in sorted(glob.glob(os.path.join(folder, "*OPSRAP*ORB.SP3"))):
        for prn, a in orbit.read_sp3(f).items():
            d = rows.setdefault(prn, {})
            for r in a:
                d.setdefault(r[0], (r[1], r[2], r[3], r[4]))
    out = {}
    for prn, d in rows.items():
        t = np.array(sorted(d)); v = np.array([d[k] for k in t])
        out[prn] = (t, v[:, :3], v[:, 3])
    return out


def shadow_minutes(t, xyz, sun_ecef):
    """1 where the satellite is in the Earth's shadow (cylinder model), per epoch."""
    sh = sun_ecef / np.linalg.norm(sun_ecef, axis=1, keepdims=True)
    along = (xyz * sh).sum(1)
    perp = np.linalg.norm(xyz - along[:, None] * sh, axis=1)
    return (along < 0) & (perp < orbit.RE)


def evaluate(target, truth, now_gps, eop, label, start):
    B = N.read_file(target)
    T0 = B[0]["t"]
    E = {}
    for b in B:
        for s in b["slots"]:
            if s["status"] == 0:
                E.setdefault(s["prn"], []).extend(N.ephemerides(b, s))
    end = T0 + 28 * DAY
    grid = np.arange(np.ceil(now_gps / 900) * 900, end, 900.0)
    M = orbit.c2t(grid, eop)
    sun, _ = orbit.sun_moon(grid)
    sun_ecef = np.einsum("nij,nj->ni", M, sun)
    idx = {t: i for i, t in enumerate(grid)}
    clk_err = np.full((33, len(grid)), np.nan); pos_err = np.full((33, len(grid)), np.nan); ecl = np.zeros((33, len(grid)), bool)
    for prn, eps in E.items():
        if prn not in truth: continue
        t, x, c = truth[prn]
        for j in range(len(t)):
            i = idx.get(t[j])
            if i is None: continue
            k = int((t[j] - T0) // 21600)
            ep = eps[k]
            pos_err[prn, i] = np.linalg.norm(np.array(N.ecef(ep, t[j])) - x[j])
            if np.isfinite(c[j]):
                clk_err[prn, i] = (ep["af0"] + ep["af1"] * (t[j] - ep["toe"]) - c[j]) * C
        ok = np.isfinite(pos_err[prn])
        if ok.any():
            ii = np.where(ok)[0]
            xx = np.array([x[np.searchsorted(t, grid[i])] for i in ii])
            ecl[prn, ii] = shadow_minutes(grid[ii], xx, sun_ecef[ii])
    # the receiver clock absorbs an error common to all satellites: remove the per-epoch median
    common = np.nanmedian(clk_err[1:], axis=0)
    clk_rel = clk_err - common[None, :]
    rows = []
    day = ((grid - now_gps) // DAY).astype(int) + 1
    for prn in sorted(E):
        for d in range(1, day.max() + 1):
            m = (day == d) & np.isfinite(pos_err[prn])
            if not m.any(): continue
            pe = pos_err[prn, m]; ce = np.abs(clk_err[prn, m]); cr = np.abs(clk_rel[prn, m])
            rows.append(dict(label=label, start=start, prn=prn, day=d, n=int(m.sum()),
                             pos_med=round(float(np.median(pe)), 2), pos_p95=round(float(np.percentile(pe, 95)), 2),
                             pos_max=round(float(pe.max()), 2),
                             clk_med=round(float(np.nanmedian(ce)), 2) if np.isfinite(ce).any() else "",
                             clk_rel_med=round(float(np.nanmedian(cr)), 2) if np.isfinite(cr).any() else "",
                             eclipse_min=int(ecl[prn, m].sum() * 15)))
    return rows


def run(a):
    start = datetime.date.fromisoformat(a.start)
    now = datetime.datetime(start.year, start.month, start.day, 0, 0)
    if not a.no_download:
        print("Downloading IGS data for %s ..." % start, flush=True)
        missing = download.download_range(a.data, start - datetime.timedelta(days=6), start + datetime.timedelta(days=28),
                                          [start - datetime.timedelta(days=1), start])
        if missing: print("missing:", ", ".join(missing), flush=True)
    os.makedirs(a.out, exist_ok=True)
    try:
        r = generate.build(a.data, os.path.join(a.out, "file-" + a.start), now, freeze_eop=True, keep_on_fail=True)
    except RuntimeError as e:   # e.g. a gap in the IGS archive: record it and carry on with the other start dates
        print("SKIPPED:", e)
        with open(os.path.join(a.out, "notes-%s-%s.txt" % (a.label, a.start)), "w") as f:
            f.write("skipped: %s\n" % e)
        return
    eop = orbit.EOP(a.data); eop.frozen_after = float(orbit.mjd_utc(r["now_gps"]))
    truth = load_truth_with_clock(a.data)
    rows = evaluate(r["target"], truth, r["now_gps"], eop, a.label, a.start)
    path = os.path.join(a.out, "result-%s-%s.csv" % (a.label, a.start))
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, FIELDS); w.writeheader(); w.writerows(rows)
    with open(os.path.join(a.out, "notes-%s-%s.txt" % (a.label, a.start)), "w") as f:
        f.write("checks ok: %s\n" % r["ok"])
        f.write("\n".join("%s %s" % ("OK  " if c[1] else "FAIL", c[0]) for c in r["checks"]) + "\n")
        f.write("\n".join(r["notes"]) + "\n")
    print("written", path, len(rows), "rows")


def _q(v, p):
    v = [x for x in v if x == x]
    return float(np.percentile(v, p)) if v else float("nan")


def summary(a):
    rows = []
    for f in sorted(glob.glob(os.path.join(a.inp, "**", "result-*.csv"), recursive=True)):
        with open(f) as fh:
            for r in csv.DictReader(fh):
                if a.label and r["label"] != a.label: continue
                for k in ("prn", "day", "n", "eclipse_min"): r[k] = int(r[k])
                for k in ("pos_med", "pos_p95", "pos_max", "clk_med", "clk_rel_med"): r[k] = float(r[k]) if r[k] != "" else float("nan")
                rows.append(r)
    if not rows: sys.exit("no results found")
    os.makedirs(a.out, exist_ok=True)
    with open(os.path.join(a.out, "results.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, FIELDS); w.writeheader(); w.writerows(rows)
    starts = sorted(set(r["start"] for r in rows))
    L = ["# Hindcast %s" % (a.label or ""), "",
         "Start dates (%d): %s" % (len(starts), ", ".join(starts)), "",
         "Each start date: orbits fitted to the data up to 00:00 UTC, file generated, then compared with the IGS rapid",
         "orbits and clocks measured afterwards. Values per satellite and prediction day, then aggregated.",
         "Clock error converted to metres; \"relative\" removes the error common to all satellites, which the receiver",
         "clock absorbs.", "",
         "## By prediction day", "",
         "| Day | Position median | Position p95 | Position max | Clock rel. median | Clock rel. p95 | Clock raw median | Pos. median, eclipsing sats | Pos. median, others |",
         "|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for d in sorted(set(r["day"] for r in rows)):
        R = [r for r in rows if r["day"] == d]
        ec = [r["pos_med"] for r in R if r["eclipse_min"] > 0]; no = [r["pos_med"] for r in R if r["eclipse_min"] == 0]
        L.append("| %d | %.1f m | %.1f m | %.1f m | %.1f m | %.1f m | %.1f m | %s | %.1f m |" % (
            d, _q([r["pos_med"] for r in R], 50), _q([r["pos_p95"] for r in R], 95), max(r["pos_max"] for r in R),
            _q([r["clk_rel_med"] for r in R], 50), _q([r["clk_rel_med"] for r in R], 95), _q([r["clk_med"] for r in R], 50),
            ("%.1f m (%d)" % (_q(ec, 50), len(ec))) if ec else "-", _q(no, 50)))
    L += ["", "## Worst satellite-days (position)", "", "| Start | PRN | Day | Position median | Position max | Eclipse min |", "|---|---:|---:|---:|---:|---:|"]
    for r in sorted(rows, key=lambda r: -r["pos_max"])[:15]:
        L.append("| %s | %d | %d | %.0f m | %.0f m | %d |" % (r["start"], r["prn"], r["day"], r["pos_med"], r["pos_max"], r["eclipse_min"]))
    L += ["", "## Worst satellite-days (relative clock)", "", "| Start | PRN | Day | Clock rel. median |", "|---|---:|---:|---:|"]
    for r in sorted([r for r in rows if r["clk_rel_med"] == r["clk_rel_med"]], key=lambda r: -r["clk_rel_med"])[:15]:
        L.append("| %s | %d | %d | %.0f m |" % (r["start"], r["prn"], r["day"], r["clk_rel_med"]))
    notes = sorted(glob.glob(os.path.join(a.inp, "**", "notes-*.txt"), recursive=True))
    if notes:
        L += ["", "## Generator notes per start", ""]
        for f in notes:
            L += ["### " + os.path.basename(f)[6:-4], "", "```"] + open(f).read().strip().splitlines() + ["```", ""]
    open(os.path.join(a.out, "summary.md"), "w").write("\n".join(L) + "\n")
    print("\n".join(L[:50]))


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    r = sp.add_parser("run"); r.add_argument("--start", required=True); r.add_argument("--out", default="hc")
    r.add_argument("--data", default="hc-data"); r.add_argument("--label", default="baseline"); r.add_argument("--no-download", action="store_true")
    s = sp.add_parser("summary"); s.add_argument("--inp", required=True); s.add_argument("--out", required=True); s.add_argument("--label", default="")
    a = ap.parse_args()
    run(a) if a.cmd == "run" else summary(a)


if __name__ == "__main__":
    main()
