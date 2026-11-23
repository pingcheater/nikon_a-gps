# Hindcast baseline

Start dates (7): 2026-08-31, 2026-09-07, 2026-09-14, 2026-09-21, 2026-09-28, 2026-10-05, 2026-10-19

Each start date: orbits fitted to the data up to 00:00 UTC, file generated, then compared with the IGS rapid
orbits and clocks measured afterwards. Values per satellite and prediction day, then aggregated.
Clock error converted to metres; "relative" removes the error common to all satellites, which the receiver
clock absorbs.

## By prediction day

| Day | Position median | Position p95 | Position max | Clock rel. median | Clock rel. p95 | Clock raw median | Pos. median, eclipsing sats | Pos. median, others |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1.0 m | 7.3 m | 12.9 m | 0.3 m | 0.8 m | 0.5 m | 2.3 m (30) | 0.9 m |
| 2 | 1.4 m | 13.7 m | 2724.9 m | 0.9 m | 2.8 m | 1.1 m | 3.9 m (21) | 1.3 m |
| 3 | 2.1 m | 21.5 m | 100604.5 m | 1.9 m | 5.5 m | 2.0 m | 6.0 m (21) | 2.0 m |
| 4 | 3.4 m | 35.0 m | 338827.4 m | 3.1 m | 9.4 m | 3.3 m | 8.4 m (20) | 3.2 m |
| 5 | 4.8 m | 68.4 m | 411152.0 m | 4.3 m | 15.8 m | 4.5 m | 18.0 m (18) | 4.6 m |
| 6 | 6.8 m | 95.8 m | 483820.5 m | 5.8 m | 22.4 m | 6.2 m | 18.0 m (20) | 6.2 m |
| 7 | 8.9 m | 114.5 m | 556457.6 m | 7.9 m | 31.9 m | 8.6 m | 24.6 m (22) | 8.5 m |
| 8 | 10.8 m | 138.2 m | 628940.6 m | 9.5 m | 42.7 m | 10.3 m | 24.4 m (34) | 10.0 m |
| 9 | 13.6 m | 223.3 m | 701260.8 m | 11.2 m | 54.6 m | 12.4 m | 43.6 m (24) | 12.0 m |
| 10 | 16.1 m | 350.7 m | 833670.1 m | 13.2 m | 67.1 m | 14.1 m | 63.1 m (25) | 14.4 m |
| 11 | 17.5 m | 432.3 m | 972480.5 m | 14.0 m | 81.4 m | 16.5 m | 57.3 m (23) | 16.3 m |
| 12 | 20.2 m | 32381.6 m | 1111332.2 m | 15.9 m | 96.7 m | 18.6 m | 56.4 m (23) | 18.5 m |
| 13 | 22.5 m | 65522.1 m | 1250234.1 m | 17.9 m | 112.6 m | 20.4 m | 67.3 m (25) | 20.8 m |
| 14 | 26.0 m | 119120.7 m | 1389192.1 m | 21.5 m | 131.5 m | 23.5 m | 74.2 m (25) | 23.7 m |
| 15 | 28.7 m | 159623.5 m | 1528182.4 m | 23.5 m | 149.1 m | 25.3 m | 86.7 m (37) | 25.4 m |
| 16 | 36.2 m | 165175.5 m | 1667241.0 m | 26.9 m | 167.0 m | 29.5 m | 108.8 m (30) | 28.6 m |
| 17 | 40.0 m | 198464.4 m | 1806337.1 m | 29.5 m | 188.5 m | 32.9 m | 122.6 m (31) | 32.1 m |
| 18 | 48.4 m | 233901.0 m | 1945498.4 m | 32.1 m | 211.9 m | 36.4 m | 138.9 m (31) | 36.7 m |
| 19 | 58.4 m | 310047.5 m | 2084739.4 m | 35.5 m | 236.0 m | 40.5 m | 156.5 m (31) | 46.0 m |
| 20 | 64.4 m | 380371.5 m | 2224042.0 m | 39.3 m | 261.9 m | 43.5 m | 174.8 m (33) | 51.4 m |
| 21 | 69.7 m | 474807.6 m | 2363405.3 m | 42.6 m | 291.4 m | 45.6 m | 187.3 m (35) | 55.3 m |
| 22 | 75.2 m | 550364.5 m | 2502834.7 m | 46.6 m | 317.5 m | 49.9 m | 187.3 m (47) | 59.7 m |
| 23 | 80.8 m | 596683.6 m | 2642339.8 m | 51.2 m | 347.8 m | 54.0 m | 166.0 m (38) | 65.1 m |
| 24 | 88.0 m | 633457.9 m | 2781914.2 m | 54.8 m | 379.1 m | 58.5 m | 223.6 m (39) | 70.2 m |
| 25 | 96.5 m | 670260.0 m | 2921566.6 m | 61.6 m | 414.1 m | 63.0 m | 234.1 m (39) | 75.3 m |
| 26 | 108.1 m | 707034.5 m | 3061305.2 m | 65.0 m | 447.8 m | 67.3 m | 240.4 m (39) | 84.1 m |
| 27 | 118.4 m | 754025.4 m | 3201124.6 m | 68.5 m | 482.1 m | 71.3 m | 255.0 m (42) | 94.6 m |
| 28 | 128.1 m | 818619.3 m | 3294668.0 m | 71.4 m | 509.9 m | 74.9 m | 234.2 m (41) | 106.3 m |

## Worst satellite-days (position)

| Start | PRN | Day | Position median | Position max | Eclipse min |
|---|---:|---:|---:|---:|---:|
| 2026-10-05 | 12 | 28 | 3250450 m | 3294668 m | 0 |
| 2026-10-05 | 12 | 27 | 3132709 m | 3201125 m | 15 |
| 2026-10-05 | 12 | 26 | 2992834 m | 3061305 m | 30 |
| 2026-10-05 | 12 | 25 | 2853047 m | 2921567 m | 60 |
| 2026-10-05 | 12 | 24 | 2713336 m | 2781914 m | 60 |
| 2026-10-05 | 12 | 23 | 2573708 m | 2642340 m | 90 |
| 2026-09-28 | 25 | 28 | 2544489 m | 2577889 m | 30 |
| 2026-09-28 | 25 | 27 | 2461467 m | 2512607 m | 75 |
| 2026-10-05 | 12 | 22 | 2434150 m | 2502835 m | 90 |
| 2026-09-28 | 25 | 26 | 2359976 m | 2411313 m | 90 |
| 2026-10-05 | 12 | 21 | 2294666 m | 2363405 m | 90 |
| 2026-09-28 | 25 | 25 | 2258726 m | 2310088 m | 60 |
| 2026-09-28 | 12 | 28 | 2275558 m | 2309117 m | 45 |
| 2026-09-28 | 12 | 27 | 2155496 m | 2224318 m | 90 |
| 2026-10-05 | 12 | 20 | 2155249 m | 2224042 m | 90 |

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

