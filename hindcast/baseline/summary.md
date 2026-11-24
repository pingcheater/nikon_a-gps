# Hindcast baseline

Start dates (7): 2026-08-31, 2026-09-07, 2026-09-14, 2026-09-21, 2026-09-28, 2026-10-05, 2026-10-19

Each start date: orbits fitted to the data up to 00:00 UTC, file generated, then compared with the IGS rapid
orbits and clocks measured afterwards. Values per satellite and prediction day, then aggregated.
Clock error converted to metres; "relative" removes the error common to all satellites, which the receiver
clock absorbs.

## By prediction day

| Day | Position median | Position p95 | Position max | Clock rel. median | Clock rel. p95 | Clock raw median | Pos. median, eclipsing sats | Pos. median, others |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1.0 m | 7.3 m | 12.9 m | 0.4 m | 2.3 m | 0.5 m | 2.3 m (30) | 0.9 m |
| 2 | 1.4 m | 13.7 m | 2724.9 m | 0.6 m | 5.2 m | 1.0 m | 3.9 m (21) | 1.3 m |
| 3 | 2.1 m | 21.5 m | 100604.5 m | 1.0 m | 7.6 m | 1.9 m | 5.9 m (21) | 2.0 m |
| 4 | 3.4 m | 35.0 m | 338827.4 m | 1.3 m | 10.4 m | 2.5 m | 8.4 m (20) | 3.2 m |
| 5 | 4.8 m | 68.4 m | 411152.0 m | 1.4 m | 11.7 m | 2.8 m | 18.0 m (18) | 4.6 m |
| 6 | 6.8 m | 95.8 m | 483820.5 m | 1.4 m | 14.2 m | 3.5 m | 18.0 m (20) | 6.2 m |
| 7 | 8.9 m | 114.5 m | 556457.6 m | 2.2 m | 15.8 m | 4.1 m | 24.6 m (22) | 8.5 m |
| 8 | 10.8 m | 138.2 m | 628940.6 m | 2.1 m | 18.8 m | 5.2 m | 24.4 m (34) | 10.0 m |
| 9 | 13.6 m | 223.3 m | 701260.8 m | 2.7 m | 32.0 m | 6.1 m | 43.6 m (24) | 12.0 m |
| 10 | 16.1 m | 350.7 m | 833670.1 m | 3.4 m | 37.7 m | 7.7 m | 63.1 m (25) | 14.4 m |
| 11 | 17.5 m | 432.3 m | 972480.5 m | 4.3 m | 41.1 m | 9.0 m | 57.3 m (23) | 16.3 m |
| 12 | 20.2 m | 32381.6 m | 1111332.2 m | 4.5 m | 46.3 m | 9.9 m | 56.4 m (23) | 18.5 m |
| 13 | 22.5 m | 65522.1 m | 1250234.1 m | 4.5 m | 52.0 m | 11.1 m | 67.3 m (25) | 20.8 m |
| 14 | 26.0 m | 119120.7 m | 1389192.1 m | 5.3 m | 54.7 m | 12.7 m | 74.2 m (25) | 23.7 m |
| 15 | 28.7 m | 159623.5 m | 1528182.4 m | 6.1 m | 64.9 m | 14.4 m | 86.7 m (37) | 25.4 m |
| 16 | 36.2 m | 165175.5 m | 1667241.0 m | 7.4 m | 77.7 m | 15.5 m | 108.8 m (30) | 28.6 m |
| 17 | 40.0 m | 198464.4 m | 1806337.1 m | 8.8 m | 88.6 m | 17.6 m | 122.6 m (31) | 32.1 m |
| 18 | 48.4 m | 233901.0 m | 1945498.4 m | 9.6 m | 99.6 m | 19.3 m | 138.9 m (31) | 36.7 m |
| 19 | 58.4 m | 310047.5 m | 2084739.4 m | 10.4 m | 110.2 m | 20.7 m | 156.5 m (31) | 46.0 m |
| 20 | 64.4 m | 380371.5 m | 2224042.0 m | 10.7 m | 120.8 m | 22.9 m | 174.8 m (33) | 51.4 m |
| 21 | 69.7 m | 474807.6 m | 2363405.3 m | 11.8 m | 127.2 m | 27.1 m | 187.3 m (35) | 55.3 m |
| 22 | 75.2 m | 550364.5 m | 2502834.7 m | 12.3 m | 140.5 m | 29.2 m | 187.3 m (47) | 59.7 m |
| 23 | 80.8 m | 596683.6 m | 2642339.8 m | 14.2 m | 123.8 m | 33.9 m | 166.0 m (38) | 65.1 m |
| 24 | 87.7 m | 633457.9 m | 2781914.2 m | 15.4 m | 133.3 m | 37.5 m | 223.6 m (39) | 70.2 m |
| 25 | 94.7 m | 670260.0 m | 2921566.6 m | 16.7 m | 143.2 m | 40.5 m | 234.1 m (39) | 75.3 m |
| 26 | 107.5 m | 707034.5 m | 3061305.2 m | 17.9 m | 153.9 m | 42.4 m | 240.4 m (39) | 84.1 m |
| 27 | 117.0 m | 754025.4 m | 3201124.6 m | 19.1 m | 163.2 m | 45.4 m | 255.0 m (42) | 94.6 m |
| 28 | 128.1 m | 818619.3 m | 3294668.0 m | 19.5 m | 172.6 m | 47.6 m | 234.2 m (41) | 106.3 m |

## Without manoeuvres

Satellites whose orbit was changed by a manoeuvre after the start date (error above 5 km) are left out here: 22 of 202 satellite-starts.

| Day | Position median | Position p90 | Clock rel. median | Clock rel. p90 |
|---:|---:|---:|---:|---:|
| 1 | 1.0 m | 2.8 m | 0.5 m | 1.8 m |
| 2 | 1.4 m | 4.9 m | 0.6 m | 1.7 m |
| 3 | 2.1 m | 6.8 m | 1.2 m | 3.8 m |
| 4 | 3.3 m | 12.7 m | 1.4 m | 5.0 m |
| 5 | 4.7 m | 20.1 m | 1.5 m | 6.2 m |
| 6 | 6.5 m | 28.0 m | 1.4 m | 7.5 m |
| 7 | 8.7 m | 38.8 m | 2.3 m | 9.4 m |
| 8 | 10.2 m | 49.3 m | 2.1 m | 11.7 m |
| 9 | 12.8 m | 68.9 m | 2.8 m | 15.0 m |
| 10 | 15.0 m | 84.6 m | 3.6 m | 17.1 m |
| 11 | 17.3 m | 101.0 m | 4.3 m | 21.1 m |
| 12 | 19.1 m | 126.4 m | 4.5 m | 24.1 m |
| 13 | 21.0 m | 154.9 m | 4.5 m | 27.3 m |
| 14 | 23.7 m | 151.9 m | 5.2 m | 29.7 m |
| 15 | 27.6 m | 174.0 m | 6.1 m | 33.4 m |
| 16 | 33.2 m | 223.3 m | 7.4 m | 39.7 m |
| 17 | 38.2 m | 249.5 m | 8.9 m | 43.6 m |
| 18 | 43.0 m | 295.7 m | 9.8 m | 47.8 m |
| 19 | 48.6 m | 340.5 m | 10.5 m | 52.5 m |
| 20 | 54.5 m | 400.7 m | 10.6 m | 56.9 m |
| 21 | 58.7 m | 378.4 m | 11.4 m | 59.8 m |
| 22 | 64.5 m | 426.4 m | 12.2 m | 65.4 m |
| 23 | 69.2 m | 366.3 m | 13.9 m | 70.5 m |
| 24 | 77.3 m | 390.7 m | 15.3 m | 77.3 m |
| 25 | 78.4 m | 424.7 m | 16.6 m | 83.6 m |
| 26 | 85.7 m | 471.9 m | 18.1 m | 88.3 m |
| 27 | 92.7 m | 547.5 m | 19.2 m | 93.6 m |
| 28 | 105.4 m | 574.5 m | 18.9 m | 99.0 m |

## Worst satellite-days (position)

| Start | PRN | Day | Position median | Position max | Eclipse min |
|---|---:|---:|---:|---:|---:|
| 2026-10-05 | 12 | 28 | 3250450 m | 3294668 m | 0 |
| 2026-10-05 | 12 | 27 | 3132709 m | 3201125 m | 15 |
| 2026-10-05 | 12 | 26 | 2992834 m | 3061305 m | 30 |
| 2026-10-05 | 12 | 25 | 2853047 m | 2921567 m | 60 |
| 2026-10-05 | 12 | 24 | 2713336 m | 2781914 m | 60 |
| 2026-10-05 | 12 | 23 | 2573708 m | 2642340 m | 90 |
| 2026-09-28 | 25 | 28 | 2544504 m | 2577907 m | 30 |
| 2026-09-28 | 25 | 27 | 2461477 m | 2512620 m | 75 |
| 2026-10-05 | 12 | 22 | 2434150 m | 2502835 m | 90 |
| 2026-09-28 | 25 | 26 | 2359980 m | 2411319 m | 90 |
| 2026-10-05 | 12 | 21 | 2294666 m | 2363405 m | 90 |
| 2026-09-28 | 25 | 25 | 2258725 m | 2310089 m | 60 |
| 2026-09-28 | 12 | 28 | 2275535 m | 2309093 m | 45 |
| 2026-09-28 | 12 | 27 | 2155479 m | 2224298 m | 90 |
| 2026-10-05 | 12 | 20 | 2155249 m | 2224042 m | 90 |

## Worst satellite-days (relative clock)

| Start | PRN | Day | Clock rel. median |
|---|---:|---:|---:|
| 2026-09-07 | 3 | 28 | 953 m |
| 2026-09-07 | 3 | 27 | 897 m |
| 2026-09-07 | 3 | 26 | 829 m |
| 2026-09-07 | 3 | 25 | 760 m |
| 2026-09-07 | 3 | 24 | 693 m |
| 2026-09-07 | 3 | 23 | 627 m |
| 2026-09-07 | 3 | 22 | 563 m |
| 2026-09-21 | 3 | 28 | 527 m |
| 2026-09-21 | 3 | 27 | 506 m |
| 2026-09-07 | 3 | 21 | 503 m |
| 2026-09-21 | 3 | 26 | 479 m |
| 2026-09-07 | 3 | 20 | 458 m |
| 2026-09-21 | 3 | 25 | 451 m |
| 2026-08-31 | 27 | 28 | 445 m |
| 2026-08-31 | 3 | 28 | 441 m |

## Generator notes per start

### baseline-2026-08-31

```
checks ok: True
OK   CRC of all blocks
OK   at least 24 satellites (28)
OK   file vs. own prediction (median 0.9 m, max 11.7 m)
OK   file vs. IGS prediction (median nan m, 0 comparisons)
OK   file vs. broadcast ephemerides (median 2.2 m, 265 comparisons)
block 2 PRN 28 M0: h3 clipped
block 2 PRN 28 omega: h3 clipped
block 4 PRN 28 M0: h3 clipped
block 4 PRN 28 omega: h3 clipped
```

### baseline-2026-09-07

```
checks ok: True
OK   CRC of all blocks
OK   at least 24 satellites (29)
OK   file vs. own prediction (median 0.9 m, max 11.5 m)
OK   file vs. IGS prediction (median nan m, 0 comparisons)
OK   file vs. broadcast ephemerides (median 2.1 m, 274 comparisons)
PRN 25: 39679.8 m residual error over 5.0 days
block 1 PRN 28 M0: h3 clipped
block 1 PRN 28 omega: h3 clipped
block 3 PRN 28 M0: h3 clipped
block 3 PRN 28 omega: h3 clipped
```

### baseline-2026-09-14

```
checks ok: True
OK   CRC of all blocks
OK   at least 24 satellites (29)
OK   file vs. own prediction (median 0.9 m, max 11.2 m)
OK   file vs. IGS prediction (median nan m, 0 comparisons)
OK   file vs. broadcast ephemerides (median 2.2 m, 275 comparisons)
PRN 23: 2937.9 m residual error over 5.0 days
block 2 PRN 28 M0: h3 clipped
block 2 PRN 28 omega: h3 clipped
block 4 PRN 28 M0: h3 clipped
block 4 PRN 28 omega: h3 clipped
```

### baseline-2026-09-21

```
checks ok: True
OK   CRC of all blocks
OK   at least 24 satellites (29)
OK   file vs. own prediction (median 0.9 m, max 11.3 m)
OK   file vs. IGS prediction (median nan m, 0 comparisons)
OK   file vs. broadcast ephemerides (median 2.0 m, 278 comparisons)
PRN 1: 3285.0 m residual error over 5.0 days
block 1 PRN 28 M0: h3 clipped
block 1 PRN 28 omega: h3 clipped
block 3 PRN 28 M0: h3 clipped
block 3 PRN 28 omega: h3 clipped
block 4 PRN 28 M0: h3 clipped
block 4 PRN 28 omega: h3 clipped
```

### baseline-2026-09-28

```
checks ok: True
OK   CRC of all blocks
OK   at least 24 satellites (29)
OK   file vs. own prediction (median 0.9 m, max 11.2 m)
OK   file vs. IGS prediction (median nan m, 0 comparisons)
OK   file vs. broadcast ephemerides (median 2.0 m, 278 comparisons)
PRN 15: 4468.0 m residual error over 5.0 days
block 2 PRN 28 M0: h3 clipped
block 2 PRN 28 omega: h3 clipped
block 3 PRN 28 M0: h3 clipped
block 3 PRN 28 omega: h3 clipped
block 4 PRN 28 M0: h3 clipped
block 4 PRN 28 omega: h3 clipped
```

### baseline-2026-10-05

```
checks ok: True
OK   CRC of all blocks
OK   at least 24 satellites (29)
OK   file vs. own prediction (median 0.9 m, max 14.3 m)
OK   file vs. IGS prediction (median nan m, 0 comparisons)
OK   file vs. broadcast ephemerides (median 2.2 m, 280 comparisons)
block 1 PRN 28 M0: h3 clipped
block 1 PRN 28 omega: h3 clipped
block 2 PRN 28 M0: h3 clipped
block 2 PRN 28 omega: h3 clipped
block 3 PRN 28 M0: h3 clipped
block 3 PRN 28 omega: h3 clipped
block 4 PRN 28 M0: h3 clipped
block 4 PRN 28 omega: h3 clipped
```

### baseline-2026-10-12

```
skipped: only 0 satellites could be fitted (data gap in the orbit files?)
```

### baseline-2026-10-19

```
checks ok: True
OK   CRC of all blocks
OK   at least 24 satellites (29)
OK   file vs. own prediction (median 0.9 m, max 14.2 m)
OK   file vs. IGS prediction (median nan m, 0 comparisons)
OK   file vs. broadcast ephemerides (median 2.3 m, 280 comparisons)
PRN 12: 10.2 m residual error over 5.0 days
PRN 25: 7.2 m residual error over 5.0 days
block 1 PRN 28 M0: h3 clipped
block 1 PRN 28 omega: h3 clipped
block 2 PRN 28 M0: h3 clipped
block 2 PRN 28 omega: h3 clipped
block 4 PRN 28 M0: h3 clipped
block 4 PRN 28 omega: h3 clipped
```

