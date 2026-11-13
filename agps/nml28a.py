#!/usr/bin/env python3
"""
nml28a.py - Leser und Schreiber fuer Nikon A-GPS-Dateien "NML_28A.ee"
(D5300, COOLPIX P330/P510/P520).

Format (per Reverse Engineering ermittelt, Stand 13.11.2026):

Datei   = 4 Wochenbloecke zu je 32.680 Bytes (alles Big Endian)
Block   = Header (6 Bytes) + 32 Slots (je 1.021 Bytes) + CRC (2 Bytes)
Header  = Startzeit in GPS-Sekunden seit 06.01.1980 (uint32),
          Blocknummer 0..3 (uint8), Blockanzahl 4 (uint8)
CRC     = CRC-16/XMODEM (Polynom 0x1021, Startwert 0) ueber Header + Slots
Slot    = PRN (uint8), Status (uint8: 0x00 = Bahn vorhanden, 0xff = keine Bahn),
          af0 (int32, 2^-40 s, bezogen auf Blockstart),
          af1 (int24, 2^-50 s/s), 24 Null-Bits,
          danach 15 Sektionen (bitgepackt), je eine pro Ephemeridenparameter.
Sektion = h0 (34 Bit), h1 (34 Bit), h2 (24 Bit), h3 (20 Bit), z (8 Bit),
          28 Residuen s[k] (je 12, 16 oder 24 Bit, vorzeichenbehaftet)
          Wert(k) = h0 + h1*k + h2*k^2 + h3*k^3/256 + s[k],  k = 0..27

Jeder Block enthaelt damit pro Satellit 28 Ephemeridensaetze im Stil der
GPS-Broadcast-Ephemeriden, einen je 6 Stunden. Die Bezugszeit (toe) von Satz k
liegt in der Mitte seines Intervalls: toe = Blockstart + 6h*k + 3h.

Reihenfolge, Bitbreite der Residuen und Einheit (LSB) der 15 Parameter:
"""
import sys, math, struct, csv, datetime

BLOCK = 32680
SLOT = 1021
NSEC = 15
NSAMP = 28
STEP = 21600           # 6 Stunden
TOE_OFFSET = 10800     # toe in Intervallmitte
PI = 3.1415926535898   # Wert aus der GPS-Schnittstellenspezifikation
OMEGA_E = 7.2921151467e-5
MU = 3.986005e14
GPS_EPOCH = datetime.datetime(1980, 1, 6, tzinfo=datetime.timezone.utc)

# (Name, Residuenbreite in Bit, LSB, Einheit nach Skalierung)
PARAMS = [
    ("sqrtA", 16, 2.0 ** -19, "sqrt(m)"),
    ("e",     16, 2.0 ** -33, "-"),
    ("i0",    16, 2.0 ** -31 * PI, "rad"),
    ("raan",  16, 2.0 ** -31 * PI, "rad"),   # inertiale Rektaszension, siehe omega0()
    ("M0",    24, 2.0 ** -31 * PI, "rad"),
    ("omega", 24, 2.0 ** -31 * PI, "rad"),
    ("idot",  12, 2.0 ** -43 * PI, "rad/s"),
    ("omegadot", 16, 2.0 ** -43 * PI, "rad/s"),
    ("deltan", 12, 2.0 ** -43 * PI, "rad/s"),
    ("crc",   12, 2.0 ** -5, "m"),
    ("crs",   12, 2.0 ** -5, "m"),
    ("cic",   12, 2.0 ** -29, "rad"),
    ("cis",   12, 2.0 ** -29, "rad"),
    ("cuc",   12, 2.0 ** -29, "rad"),
    ("cus",   12, 2.0 ** -29, "rad"),
]
AF0_LSB = 2.0 ** -40
AF1_LSB = 2.0 ** -50


def crc16(data):
    crc = 0
    for b in data:
        crc ^= b << 8
        for _ in range(8):
            crc = ((crc << 1) ^ 0x1021) & 0xFFFF if crc & 0x8000 else (crc << 1) & 0xFFFF
    return crc


def gps_datetime(t):
    return GPS_EPOCH + datetime.timedelta(seconds=t)


def gmst(gps_seconds):
    """GMST (IAU 1982) in rad; die Datei setzt GPS-Zeit ohne Schaltsekunden als UT ein."""
    jd = 2444244.5 + gps_seconds / 86400.0
    T = (jd - 2451545.0) / 36525.0
    g = 67310.54841 + (876600 * 3600 + 8640184.812866) * T + 0.093104 * T * T - 6.2e-6 * T ** 3
    return (g % 86400) / 86400 * 2 * math.pi


class _Bits:
    def __init__(self, data):
        self.x = int.from_bytes(data, "big")
        self.n = len(data) * 8
        self.pos = 0

    def get(self, k, signed=True):
        v = (self.x >> (self.n - self.pos - k)) & ((1 << k) - 1)
        self.pos += k
        if signed and v >> (k - 1):
            v -= 1 << k
        return v


def parse_slot(slot):
    b = _Bits(slot)
    r = dict(prn=b.get(8, False), status=b.get(8, False), af0=b.get(32), af1=b.get(24),
             reserved=b.get(24, False), sections=[])
    for _, width, _, _ in PARAMS:
        h = [b.get(34), b.get(34), b.get(24), b.get(20)]
        z = b.get(8, False)
        s = [b.get(width) for _ in range(NSAMP)]
        r["sections"].append(dict(h=h, z=z, s=s))
    assert b.pos == b.n
    return r


def pack_slot(r):
    x = 0
    n = 0

    def put(v, k):
        nonlocal x, n
        lo, hi = -(1 << (k - 1)), (1 << k) - 1
        if not lo <= v <= hi:
            raise ValueError("Wert %d passt nicht in %d Bit" % (v, k))
        x = (x << k) | (v & ((1 << k) - 1))
        n += k

    put(r["prn"], 8); put(r["status"], 8); put(r["af0"], 32); put(r["af1"], 24); put(r["reserved"], 24)
    for sec, (_, width, _, _) in zip(r["sections"], PARAMS):
        for v, k in zip(sec["h"], (34, 34, 24, 20)):
            put(v, k)
        put(sec["z"], 8)
        for v in sec["s"]:
            put(v, width)
    assert n == SLOT * 8
    return x.to_bytes(SLOT, "big")


def read_file(path):
    data = open(path, "rb").read()
    if len(data) % BLOCK:
        raise ValueError("unerwartete Dateigroesse %d" % len(data))
    blocks = []
    for i in range(len(data) // BLOCK):
        blk = data[i * BLOCK:(i + 1) * BLOCK]
        t, idx, cnt = struct.unpack(">IBB", blk[:6])
        slots = [parse_slot(blk[6 + s * SLOT:6 + (s + 1) * SLOT]) for s in range(32)]
        blocks.append(dict(t=t, index=idx, count=cnt, slots=slots,
                           crc_ok=crc16(blk) == 0))
    return blocks


def write_file(path, blocks):
    out = b""
    for blk in blocks:
        body = struct.pack(">IBB", blk["t"], blk["index"], blk["count"])
        body += b"".join(pack_slot(s) for s in blk["slots"])
        out += body + struct.pack(">H", crc16(body))
    open(path, "wb").write(out)


def section_values(sec):
    """Ganzzahlige Rohwerte der 28 Stuetzstellen (in LSB)."""
    h0, h1, h2, h3 = sec["h"]
    return [h0 + h1 * k + h2 * k * k + h3 * k ** 3 / 256.0 + sec["s"][k] for k in range(NSAMP)]


def ephemerides(block, slot):
    """28 Ephemeridensaetze eines Satelliten in SI-Einheiten (GPS-ICD-Konvention)."""
    if slot["status"] != 0:
        return []
    cols = [section_values(sec) for sec in slot["sections"]]
    out = []
    for k in range(NSAMP):
        toe = block["t"] + STEP * k + TOE_OFFSET
        week_start = toe - toe % 604800
        ep = dict(prn=slot["prn"], toe=toe, week=toe // 604800, tow=toe % 604800)
        for (name, _, lsb, _), col in zip(PARAMS, cols):
            ep[name] = col[k] * lsb
        # Datei speichert die inertiale Rektaszension; Omega0 nach ICD = raan - GMST(Wochenbeginn)
        ep["omega0"] = (ep["raan"] - gmst(week_start) + math.pi) % (2 * math.pi) - math.pi
        ep["M0"] = (ep["M0"] + math.pi) % (2 * math.pi) - math.pi
        ep["omega"] = (ep["omega"] + math.pi) % (2 * math.pi) - math.pi
        ep["af0"] = slot["af0"] * AF0_LSB + slot["af1"] * AF1_LSB * (toe - block["t"])
        ep["af1"] = slot["af1"] * AF1_LSB
        out.append(ep)
    return out


def ecef(ep, t):
    """Satellitenposition (ECEF, m) zur GPS-Zeit t nach dem Standardalgorithmus der GPS-ICD."""
    A = ep["sqrtA"] ** 2
    n = math.sqrt(MU / A ** 3) + ep["deltan"]
    tk = t - ep["toe"]
    M = ep["M0"] + n * tk
    E = M
    for _ in range(15):
        E = M + ep["e"] * math.sin(E)
    v = math.atan2(math.sqrt(1 - ep["e"] ** 2) * math.sin(E), math.cos(E) - ep["e"])
    phi = v + ep["omega"]
    s2, c2 = math.sin(2 * phi), math.cos(2 * phi)
    u = phi + ep["cus"] * s2 + ep["cuc"] * c2
    r = A * (1 - ep["e"] * math.cos(E)) + ep["crs"] * s2 + ep["crc"] * c2
    i = ep["i0"] + ep["cis"] * s2 + ep["cic"] * c2 + ep["idot"] * tk
    om = ep["omega0"] + (ep["omegadot"] - OMEGA_E) * tk - OMEGA_E * ep["tow"]
    xp, yp = r * math.cos(u), r * math.sin(u)
    return (xp * math.cos(om) - yp * math.cos(i) * math.sin(om),
            xp * math.sin(om) + yp * math.cos(i) * math.cos(om),
            yp * math.sin(i))


def encode_section(values, width):
    """Ganzzahlige Rohwerte (28 Stueck, in LSB) -> Sektion mit kubischem Fit und Residuen."""
    import numpy as np
    k = np.arange(NSAMP, dtype=float)
    A = np.stack([np.ones(NSAMP), k, k * k, k ** 3 / 256.0], axis=1)
    coef = np.linalg.lstsq(A, np.asarray(values, float), rcond=None)[0]
    h = [int(round(c)) for c in coef]
    s = [int(round(values[j] - (h[0] + h[1] * j + h[2] * j * j + h[3] * j ** 3 / 256.0)))
         for j in range(NSAMP)]
    lim = 1 << (width - 1)
    if max(abs(x) for x in s) >= lim:
        raise ValueError("Residuum uebersteigt %d Bit" % width)
    return dict(h=h, z=0, s=s)


def info(path):
    blocks = read_file(path)
    for b in blocks:
        prns = [s["prn"] for s in b["slots"] if s["status"] == 0 and s["prn"]]
        print("Block %d/%d  Start %s (GPS-Zeit)  CRC %s  %d Satelliten: %s" % (
            b["index"] + 1, b["count"], gps_datetime(b["t"]).strftime("%d.%m.%Y %H:%M"),
            "ok" if b["crc_ok"] else "FEHLER", len(prns), " ".join(map(str, prns))))
    end = blocks[-1]["t"] + 604800
    print("Gueltig bis %s" % gps_datetime(end).strftime("%d.%m.%Y %H:%M"))


def export_csv(path, out):
    blocks = read_file(path)
    names = ["prn", "toe_gps", "week", "tow", "sqrtA", "e", "i0", "omega0", "omega", "M0",
             "deltan", "omegadot", "idot", "cuc", "cus", "crc", "crs", "cic", "cis", "af0", "af1"]
    with open(out, "w", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(names)
        for b in blocks:
            for s in b["slots"]:
                for ep in ephemerides(b, s):
                    ep["toe_gps"] = gps_datetime(ep["toe"]).strftime("%Y-%m-%d %H:%M:%S")
                    w.writerow([ep[n] if not isinstance(ep[n], float) else repr(ep[n]) for n in names])
    print("geschrieben:", out)


def selftest(path):
    """Datei lesen, neu schreiben und Byte fuer Byte vergleichen."""
    import tempfile, os
    blocks = read_file(path)
    tmp = tempfile.mktemp()
    write_file(tmp, blocks)
    same = open(tmp, "rb").read() == open(path, "rb").read()
    os.remove(tmp)
    print("Roundtrip byte-identisch:", same)
    return same


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "info":
        info(sys.argv[2])
    elif len(sys.argv) >= 4 and sys.argv[1] == "csv":
        export_csv(sys.argv[2], sys.argv[3])
    elif len(sys.argv) >= 3 and sys.argv[1] == "selftest":
        sys.exit(0 if selftest(sys.argv[2]) else 1)
    else:
        print("Aufruf: nml28a.py info DATEI | csv DATEI AUSGABE.csv | selftest DATEI")
