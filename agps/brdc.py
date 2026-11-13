import datetime
GPS0 = datetime.datetime(1980, 1, 6)
def read_rinex3_gps(path):
    L = open(path).read().splitlines()
    i = [n for n, l in enumerate(L) if "END OF HEADER" in l][0] + 1
    out = []
    def f(s):
        s = s.strip().replace("D", "E")
        return float(s) if s else 0.0
    while i < len(L):
        l = L[i]
        if l.startswith("G") and len(l) > 23 and l[3] == " ":
            try:
                prn = int(l[1:3]); y, mo, d, h, mi, s = (int(x) for x in l[4:23].split())
                v = [f(l[23 + 19 * j:42 + 19 * j]) for j in range(3)]
                for q in range(1, 8):
                    row = L[i + q]
                    v += [f(row[4 + 19 * j:23 + 19 * j]) for j in range(4)]
                toc = (datetime.datetime(y, mo, d, h, mi, s) - GPS0).total_seconds()
                out.append(dict(prn=prn, toc=toc, af0=v[0], af1=v[1], af2=v[2], crs=v[4], deltan=v[5], M0=v[6], cuc=v[7], e=v[8], cus=v[9],
                                sqrtA=v[10], toe=v[21] * 604800 + v[11], tow=v[11], cic=v[12], omega0=v[13], cis=v[14], i0=v[15], crc=v[16],
                                omega=v[17], omegadot=v[18], idot=v[19], health=v[24], fit=v[28]))
                i += 8; continue
            except Exception as e:
                pass
        i += 1
    return out
