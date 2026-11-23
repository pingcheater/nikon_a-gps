"""Downloads the required IGS data from BKG (igs.bkg.bund.de)."""
import datetime, gzip, os, re, urllib.request

BASE = "https://igs.bkg.bund.de/root_ftp/IGS"
GPS_EPOCH = datetime.datetime(1980, 1, 6)


def _get(url, tries=3):
    last = None
    for _ in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "nikon-agps (github actions)"})
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except Exception as e:  # noqa
            last = e
    raise RuntimeError("download failed: %s (%s)" % (url, last))


def listing(url):
    try:
        html = _get(url).decode("utf-8", "replace")
    except RuntimeError:
        return []
    return re.findall(r'href="([^"?/][^"/]*)"', html)


def fetch(url, name, folder):
    target = os.path.join(folder, name[:-3] if name.endswith(".gz") else name)
    if os.path.exists(target):
        return target
    raw = _get(url + name)
    if name.endswith(".gz"):
        raw = gzip.decompress(raw)
    with open(target, "wb") as f:
        f.write(raw)
    print("  downloaded", name, flush=True)
    return target


def download_all(folder, now=None, days=8):
    """Rapid orbits of the last `days` days, the three newest ultra-rapid orbits, broadcast data of today and yesterday."""
    os.makedirs(folder, exist_ok=True)
    now = now or datetime.datetime.utcnow()
    week = (now - GPS_EPOCH).days // 7
    oldest = (now - datetime.timedelta(days=days)).strftime("%Y%j")
    ult = []
    for w in (week - 2, week - 1, week):
        url = "%s/products/%d/" % (BASE, w)
        names = listing(url)
        for n in names:
            m = re.match(r"^IGS0OPSRAP_(\d{7})\d{4}_01D_(15M_ORB\.SP3|01D_ERP\.ERP)\.gz$", n)
            if m and m.group(1) >= oldest:
                fetch(url, n, folder)
            if re.match(r"^IGS0OPSULT_\d{11}_02D_15M_ORB\.SP3\.gz$", n):
                ult.append((n, url))
    for n, url in sorted(ult)[-3:]:
        fetch(url, n, folder)
        try:
            fetch(url, n.replace("15M_ORB.SP3", "01D_ERP.ERP"), folder)
        except RuntimeError:
            pass
    got = 0
    for back in range(0, 3):
        d = now - datetime.timedelta(days=back)
        url = "%s/BRDC/%d/%03d/" % (BASE, d.year, d.timetuple().tm_yday)
        names = listing(url)
        pick = [n for n in names if re.match(r"^BRDC00IGS_R_.*_MN\.rnx\.gz$", n)] or \
               [n for n in names if re.match(r"^BRDC00WRD_R_.*_MN\.rnx\.gz$", n)]
        if pick:
            fetch(url, pick[0], folder); got += 1
        if got >= 2:
            break
    if not ult:
        raise RuntimeError("no ultra-rapid orbits found")
    if not got:
        raise RuntimeError("no broadcast data found")


def download_range(folder, first, last, brdc_days):
    """Rapid orbits and ERP for every day from `first` to `last` (dates), broadcast files for the dates in `brdc_days`."""
    os.makedirs(folder, exist_ok=True)
    d = first; missing = []
    while d <= last:
        week = (datetime.datetime(d.year, d.month, d.day) - GPS_EPOCH).days // 7
        url = "%s/products/%d/" % (BASE, week)
        stamp = "%d%03d0000" % (d.year, d.timetuple().tm_yday)
        for kind in ("01D_15M_ORB.SP3.gz", "01D_01D_ERP.ERP.gz"):
            try:
                fetch(url, "IGS0OPSRAP_%s_%s" % (stamp, kind), folder)
            except RuntimeError:
                missing.append("%s %s" % (d, kind))
        d += datetime.timedelta(days=1)
    for d in brdc_days:
        url = "%s/BRDC/%d/%03d/" % (BASE, d.year, d.timetuple().tm_yday)
        names = listing(url)
        pick = [n for n in names if re.match(r"^BRDC00IGS_R_.*_MN\.rnx\.gz$", n)] or \
               [n for n in names if re.match(r"^BRDC00WRD_R_.*_MN\.rnx\.gz$", n)]
        if pick: fetch(url, pick[0], folder)
        else: missing.append("%s broadcast" % d)
    return missing
