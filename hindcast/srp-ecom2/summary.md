# Hindcast srp-ecom2

Start dates (7): 2026-08-31, 2026-09-07, 2026-09-14, 2026-09-21, 2026-09-28, 2026-10-05, 2026-10-19

Each start date: orbits fitted to the data up to 00:00 UTC, file generated, then compared with the IGS rapid
orbits and clocks measured afterwards. Values per satellite and prediction day, then aggregated.
Clock error converted to metres; "relative" removes the error common to all satellites, which the receiver
clock absorbs.

## By prediction day

| Day | Position median | Position p95 | Position max | Clock rel. median | Clock rel. p95 | Clock raw median | Pos. median, eclipsing sats | Pos. median, others |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1.0 m | 6.1 m | 14.7 m | 0.3 m | 0.8 m | 0.5 m | 1.8 m (30) | 0.9 m |
| 2 | 1.4 m | 13.4 m | 2724.9 m | 0.9 m | 2.8 m | 1.1 m | 3.1 m (21) | 1.3 m |
| 3 | 2.2 m | 24.1 m | 100606.4 m | 1.9 m | 5.5 m | 2.0 m | 5.0 m (21) | 2.1 m |
| 4 | 3.4 m | 40.5 m | 338826.7 m | 3.1 m | 9.4 m | 3.3 m | 8.2 m (20) | 3.2 m |
| 5 | 5.1 m | 72.6 m | 411150.8 m | 4.3 m | 15.8 m | 4.5 m | 8.1 m (18) | 4.7 m |
| 6 | 6.8 m | 99.3 m | 483818.7 m | 5.8 m | 22.4 m | 6.2 m | 11.7 m (20) | 6.4 m |
| 7 | 8.9 m | 121.0 m | 556455.0 m | 7.9 m | 31.9 m | 8.6 m | 15.0 m (22) | 8.6 m |
| 8 | 10.8 m | 151.0 m | 628937.0 m | 9.5 m | 42.7 m | 10.3 m | 16.1 m (34) | 9.7 m |
| 9 | 13.4 m | 225.9 m | 701255.8 m | 11.2 m | 54.6 m | 12.4 m | 18.5 m (24) | 12.7 m |
| 10 | 15.7 m | 334.1 m | 833420.3 m | 13.2 m | 67.1 m | 14.1 m | 23.8 m (25) | 14.8 m |
| 11 | 17.9 m | 415.9 m | 972175.5 m | 14.0 m | 81.4 m | 16.5 m | 35.4 m (23) | 16.4 m |
| 12 | 20.7 m | 32383.3 m | 1110977.5 m | 15.9 m | 96.7 m | 18.6 m | 47.8 m (23) | 19.4 m |
| 13 | 23.2 m | 65523.8 m | 1249823.7 m | 17.9 m | 112.6 m | 20.4 m | 45.5 m (25) | 21.5 m |
| 14 | 25.4 m | 119132.3 m | 1388720.8 m | 21.5 m | 131.5 m | 23.5 m | 51.5 m (25) | 23.8 m |
| 15 | 28.9 m | 159637.2 m | 1527677.8 m | 23.5 m | 149.1 m | 25.3 m | 56.1 m (37) | 26.5 m |
| 16 | 36.5 m | 165179.1 m | 1666699.1 m | 26.9 m | 167.0 m | 29.5 m | 95.0 m (30) | 31.5 m |
| 17 | 42.2 m | 198468.5 m | 1805792.7 m | 29.5 m | 188.5 m | 32.9 m | 118.5 m (31) | 36.4 m |
| 18 | 48.5 m | 233946.7 m | 1944958.4 m | 32.1 m | 211.9 m | 36.4 m | 136.5 m (31) | 41.3 m |
| 19 | 55.3 m | 310099.8 m | 2084190.0 m | 35.5 m | 236.0 m | 40.5 m | 148.4 m (31) | 49.0 m |
| 20 | 61.6 m | 380420.3 m | 2223487.4 m | 39.3 m | 261.9 m | 43.5 m | 164.4 m (33) | 55.4 m |
| 21 | 65.8 m | 474797.5 m | 2362847.0 m | 42.6 m | 291.4 m | 45.6 m | 160.3 m (35) | 60.9 m |
| 22 | 74.7 m | 550167.0 m | 2502280.7 m | 46.6 m | 317.5 m | 49.9 m | 158.3 m (47) | 66.4 m |
| 23 | 81.0 m | 596681.6 m | 2641781.2 m | 51.2 m | 347.8 m | 54.0 m | 141.9 m (38) | 72.7 m |
| 24 | 92.8 m | 633455.5 m | 2781341.9 m | 54.8 m | 379.1 m | 58.5 m | 170.7 m (39) | 80.0 m |
| 25 | 104.8 m | 670256.9 m | 2920983.5 m | 61.6 m | 414.1 m | 63.0 m | 191.4 m (39) | 87.8 m |
| 26 | 117.5 m | 707030.2 m | 3060704.0 m | 65.0 m | 447.8 m | 67.3 m | 222.5 m (39) | 103.5 m |
| 27 | 123.5 m | 754929.0 m | 3200506.0 m | 68.5 m | 482.1 m | 71.3 m | 252.4 m (42) | 114.5 m |
| 28 | 131.8 m | 819518.6 m | 3294033.4 m | 71.4 m | 509.9 m | 74.9 m | 271.0 m (41) | 118.6 m |

## Without manoeuvres

Satellites whose orbit was changed by a manoeuvre after the start date (error above 5 km) are left out here: 22 of 202 satellite-starts.

| Day | Position median | Position p90 | Clock rel. median | Clock rel. p90 |
|---:|---:|---:|---:|---:|
| 1 | 1.0 m | 2.3 m | 0.3 m | 0.8 m |
| 2 | 1.3 m | 4.4 m | 0.9 m | 2.4 m |
| 3 | 2.1 m | 7.1 m | 1.9 m | 4.6 m |
| 4 | 3.4 m | 10.9 m | 3.2 m | 7.9 m |
| 5 | 4.9 m | 15.4 m | 4.3 m | 13.0 m |
| 6 | 6.7 m | 21.5 m | 6.1 m | 19.7 m |
| 7 | 8.7 m | 29.1 m | 8.4 m | 27.0 m |
| 8 | 10.3 m | 37.0 m | 10.5 m | 35.8 m |
| 9 | 12.9 m | 48.4 m | 13.1 m | 44.9 m |
| 10 | 15.0 m | 62.9 m | 14.7 m | 56.7 m |
| 11 | 17.0 m | 78.9 m | 17.8 m | 70.3 m |
| 12 | 19.5 m | 98.4 m | 21.6 m | 83.5 m |
| 13 | 21.4 m | 113.6 m | 23.8 m | 97.8 m |
| 14 | 23.9 m | 123.0 m | 25.0 m | 117.9 m |
| 15 | 27.1 m | 138.9 m | 26.2 m | 134.3 m |
| 16 | 32.0 m | 169.4 m | 28.0 m | 152.4 m |
| 17 | 37.6 m | 191.9 m | 31.4 m | 174.1 m |
| 18 | 43.6 m | 212.9 m | 35.3 m | 196.7 m |
| 19 | 49.0 m | 241.4 m | 40.0 m | 219.6 m |
| 20 | 55.4 m | 273.1 m | 45.3 m | 243.9 m |
| 21 | 61.1 m | 290.6 m | 50.3 m | 268.9 m |
| 22 | 67.7 m | 318.3 m | 54.8 m | 290.5 m |
| 23 | 73.0 m | 310.9 m | 59.2 m | 328.1 m |
| 24 | 84.1 m | 345.7 m | 63.7 m | 358.8 m |
| 25 | 93.4 m | 400.3 m | 66.4 m | 390.8 m |
| 26 | 103.5 m | 427.8 m | 71.2 m | 423.3 m |
| 27 | 113.2 m | 452.4 m | 76.0 m | 456.9 m |
| 28 | 117.4 m | 487.1 m | 80.0 m | 483.9 m |

## Worst satellite-days (position)

| Start | PRN | Day | Position median | Position max | Eclipse min |
|---|---:|---:|---:|---:|---:|
| 2026-10-05 | 12 | 28 | 3249830 m | 3294033 m | 0 |
| 2026-10-05 | 12 | 27 | 3132099 m | 3200506 m | 15 |
| 2026-10-05 | 12 | 26 | 2992241 m | 3060704 m | 30 |
| 2026-10-05 | 12 | 25 | 2852466 m | 2920984 m | 60 |
| 2026-10-05 | 12 | 24 | 2712771 m | 2781342 m | 60 |
| 2026-10-05 | 12 | 23 | 2573150 m | 2641781 m | 90 |
| 2026-09-28 | 25 | 28 | 2544153 m | 2577542 m | 30 |
| 2026-09-28 | 25 | 27 | 2461153 m | 2512282 m | 75 |
| 2026-10-05 | 12 | 22 | 2433594 m | 2502281 m | 90 |
| 2026-09-28 | 25 | 26 | 2359681 m | 2411008 m | 90 |
| 2026-10-05 | 12 | 21 | 2294110 m | 2362847 m | 90 |
| 2026-09-28 | 25 | 25 | 2258455 m | 2309806 m | 60 |
| 2026-09-28 | 12 | 28 | 2274790 m | 2308357 m | 45 |
| 2026-09-28 | 12 | 27 | 2154817 m | 2223608 m | 90 |
| 2026-10-05 | 12 | 20 | 2154696 m | 2223487 m | 90 |

## Worst satellite-days (relative clock)

| Start | PRN | Day | Clock rel. median |
|---|---:|---:|---:|
| 2026-10-05 | 6 | 28 | 666 m |
| 2026-10-19 | 6 | 28 | 656 m |
| 2026-08-31 | 6 | 28 | 636 m |
| 2026-10-05 | 6 | 27 | 629 m |
| 2026-10-19 | 6 | 27 | 620 m |
| 2026-09-28 | 6 | 28 | 610 m |
| 2026-09-21 | 6 | 28 | 605 m |
| 2026-09-07 | 6 | 28 | 600 m |
| 2026-08-31 | 6 | 27 | 599 m |
| 2026-10-05 | 6 | 26 | 582 m |
| 2026-10-19 | 6 | 26 | 578 m |
| 2026-09-28 | 6 | 27 | 574 m |
| 2026-09-21 | 6 | 27 | 570 m |
| 2026-09-07 | 6 | 27 | 565 m |
| 2026-09-07 | 20 | 28 | 561 m |

## Generator notes per start

### srp-ecom2-2026-08-31

```
checks ok: True
OK   CRC of all blocks
OK   at least 24 satellites (28)
OK   file vs. own prediction (median 0.9 m, max 11.7 m)
OK   file vs. IGS prediction (median nan m, 0 comparisons)
OK   file vs. broadcast ephemerides (median 2.3 m, 265 comparisons)
block 2 PRN 28 M0: h3 clipped
block 2 PRN 28 omega: h3 clipped
block 4 PRN 28 M0: h3 clipped
block 4 PRN 28 omega: h3 clipped
```

### srp-ecom2-2026-09-07

```
checks ok: True
OK   CRC of all blocks
OK   at least 24 satellites (29)
OK   file vs. own prediction (median 0.9 m, max 11.5 m)
OK   file vs. IGS prediction (median nan m, 0 comparisons)
OK   file vs. broadcast ephemerides (median 2.1 m, 274 comparisons)
PRN 25: 40337.1 m residual error over 5.0 days
block 1 PRN 28 M0: h3 clipped
block 1 PRN 28 omega: h3 clipped
block 3 PRN 28 M0: h3 clipped
block 3 PRN 28 omega: h3 clipped
```

### srp-ecom2-2026-09-14

```
checks ok: True
OK   CRC of all blocks
OK   at least 24 satellites (29)
OK   file vs. own prediction (median 0.9 m, max 11.3 m)
OK   file vs. IGS prediction (median nan m, 0 comparisons)
OK   file vs. broadcast ephemerides (median 2.1 m, 275 comparisons)
PRN 23: 2938.2 m residual error over 5.0 days
block 2 PRN 28 M0: h3 clipped
block 2 PRN 28 omega: h3 clipped
block 4 PRN 28 M0: h3 clipped
block 4 PRN 28 omega: h3 clipped
```

### srp-ecom2-2026-09-21

```
checks ok: True
OK   CRC of all blocks
OK   at least 24 satellites (29)
OK   file vs. own prediction (median 0.9 m, max 11.2 m)
OK   file vs. IGS prediction (median nan m, 0 comparisons)
OK   file vs. broadcast ephemerides (median 2.0 m, 278 comparisons)
PRN 1: 3290.1 m residual error over 5.0 days
block 1 PRN 28 M0: h3 clipped
block 1 PRN 28 omega: h3 clipped
block 3 PRN 28 M0: h3 clipped
block 3 PRN 28 omega: h3 clipped
block 4 PRN 28 M0: h3 clipped
block 4 PRN 28 omega: h3 clipped
```

### srp-ecom2-2026-09-28

```
checks ok: True
OK   CRC of all blocks
OK   at least 24 satellites (29)
OK   file vs. own prediction (median 0.9 m, max 11.1 m)
OK   file vs. IGS prediction (median nan m, 0 comparisons)
OK   file vs. broadcast ephemerides (median 2.0 m, 278 comparisons)
PRN 15: 4446.0 m residual error over 5.0 days
block 2 PRN 28 M0: h3 clipped
block 2 PRN 28 omega: h3 clipped
block 3 PRN 28 M0: h3 clipped
block 3 PRN 28 omega: h3 clipped
block 4 PRN 28 M0: h3 clipped
block 4 PRN 28 omega: h3 clipped
```

### srp-ecom2-2026-10-05

```
checks ok: True
OK   CRC of all blocks
OK   at least 24 satellites (29)
OK   file vs. own prediction (median 0.9 m, max 14.3 m)
OK   file vs. IGS prediction (median nan m, 0 comparisons)
OK   file vs. broadcast ephemerides (median 2.1 m, 280 comparisons)
block 1 PRN 28 M0: h3 clipped
block 1 PRN 28 omega: h3 clipped
block 2 PRN 28 M0: h3 clipped
block 2 PRN 28 omega: h3 clipped
block 3 PRN 28 M0: h3 clipped
block 3 PRN 28 omega: h3 clipped
block 4 PRN 28 M0: h3 clipped
block 4 PRN 28 omega: h3 clipped
```

### srp-ecom2-2026-10-12

```
skipped: only 0 satellites could be fitted (data gap in the orbit files?)
```

### srp-ecom2-2026-10-19

```
checks ok: True
OK   CRC of all blocks
OK   at least 24 satellites (29)
OK   file vs. own prediction (median 0.9 m, max 14.2 m)
OK   file vs. IGS prediction (median nan m, 0 comparisons)
OK   file vs. broadcast ephemerides (median 2.1 m, 280 comparisons)
block 1 PRN 28 M0: h3 clipped
block 1 PRN 28 omega: h3 clipped
block 2 PRN 28 M0: h3 clipped
block 2 PRN 28 omega: h3 clipped
block 4 PRN 28 M0: h3 clipped
block 4 PRN 28 omega: h3 clipped
```

