# A-GPS file for the Nikon D5300 (NML_28A.ee)

Nikon no longer provides the A-GPS file `NML_28A.ee` (since 2026). This project regenerates it every day from
freely available orbit data of the International GNSS Service (IGS) and publishes it at a fixed address.
The file works with the D5300 and the COOLPIX P330, P510 and P520.

**Download:** [https://github.com/pingcheater/nikon_a-gps/releases/download/current/NML_28A.ee](https://github.com/pingcheater/nikon_a-gps/releases/download/current/NML_28A.ee)

Current state and check results: [status.md](status.md)

## Using the file in the camera

1. Copy the file to the `NIKON` folder on the memory card.
2. In the camera menu, switch off location recording and select "Update A-GPS file".
3. The camera then shows the expiry date of the file (28 days after generation).

The fresher the file, the more accurate the prediction (see [Accuracy](#accuracy)). Download it again before each trip.

## How it works

1. `agps/download.py` downloads precise orbits (rapid, ultra-rapid), Earth rotation parameters and broadcast
   ephemerides from BKG.
2. `agps/orbit.py` fits an orbit model to the last 1 to 5 days for each satellite (JGM-3 gravity field up to
   degree 8, Sun, Moon, solid Earth tides, solar radiation pressure) and propagates it 28 days ahead.
   Satellites with a manoeuvre in the fit window are fitted over a shorter arc.
3. Satellite clocks are predicted with a quadratic fit to the IGS clock values of the last 5 days.
4. `agps/generate.py` fits one ephemeris set per 6-hour window, encodes everything in the Nikon format and checks
   the finished file against the IGS prediction and the current broadcast ephemerides. If a check fails, the file
   is discarded and the previous one stays online.
5. `agps/nml28a.py` reads and writes the file format; the format description is in the module header.

The daily workflow runs at 00:00 UTC with the options `clock=quad5,srp=ecom2` (see [Model choices](#model-choices)).

Run locally: `pip install -r requirements.txt`, then `python -m agps.generate --out out --opts clock=quad5,srp=ecom2`.

## Accuracy

Measured with the hindcast described below: 7 start dates between 31 Aug and 19 Oct 2026, each file compared with
the orbits and clocks the IGS measured afterwards. Median over all satellites, satellites with a manoeuvre left out.

| Day of prediction | Orbit, median | Orbit, worst 10 % | Orbit, satellites in Earth's shadow | Clock, median |
|---:|---:|---:|---:|---:|
| 1 | 1.0 m | 2.3 m | 1.8 m | 0.5 m |
| 7 | 8.7 m | 29 m | 15 m | 2.3 m |
| 14 | 24 m | 123 m | 50 m | 5.2 m |
| 21 | 61 m | 291 m | 136 m | 11 m |
| 28 | 117 m | 487 m | 206 m | 19 m |

The clock error is the part that differs between satellites; an error common to all satellites is absorbed by the
receiver clock. Orbit and clock values come from separate hindcast runs (`srp-ecom2` and `clock-quad5`); the clock
model does not affect the orbit.

Manoeuvres: in 22 of 202 satellite-starts a satellite manoeuvred within the 28 days. Its predicted orbit is then off
by hundreds to thousands of kilometres. No prediction can avoid this; a fresh download can.

## Model choices

All variants were compared against the original model (`baseline`) with the same 7 start dates.

| Variant | Result | Used |
|---|---|---|
| `clock=quad5`: quadratic clock fit to 5 days of IGS clocks instead of the drift from the broadcast ephemeris | clock error on day 14: 5.2 m instead of 25 m, on day 28: 19 m instead of 80 m; day 1: 0.5 m instead of 0.3 m | yes |
| `srp=ecom2`: ECOM2 solar radiation pressure model (9 parameters) instead of ECOM1 (5 parameters) | worst 10 % of satellites 15–25 % better on all days, satellites in the Earth's shadow up to 45 % better until day 21; median 2–12 m worse in weeks 3 and 4 | yes |
| `srp=ecom2,arc=7`: ECOM2 fitted over 7 instead of 5 days | worse than ECOM2 with 5 days on most days (day 14: 30 m instead of 24 m) | no |

ECOM2 was chosen because satellites with a large error slow down the camera's search more than the median suggests,
and the file is usually used in its first two weeks. Results of every run are in the folder [`hindcast/`](hindcast/).

## Hindcast

The workflow "Hindcast" (Actions tab, run manually) generates files as if it were an earlier date and compares them
with the orbits and clocks measured later. Inputs:

- `first_start`, `count`, `step_days`: start dates (the last one must be at least 29 days ago)
- `opts`: model options, e.g. `clock=quad5,srp=ecom2`; empty = original model
- `label`: name of the result folder under `hindcast/`; empty = derived from the options

Each start date runs as a separate job; a start date without complete IGS data is marked as skipped.
Locally: `python -m agps.hindcast run --start 2026-09-07 --opts clock=quad5`, then
`python -m agps.hindcast summary --inp hc --out hindcast/test`.

## Archive

One file per ISO week is archived under [Releases → archive](https://github.com/pingcheater/nikon_a-gps/releases/tag/archive).
Each file is valid for 28 days from its date; rename it to `NML_28A.ee` before use. The archive keeps a record of the
files actually published, for later checks of the full pipeline.

## Limitations

- Accuracy decreases with the age of the file, see [Accuracy](#accuracy).
- The prediction cannot know about orbit manoeuvres after the file was generated.
- PRN 1, 22 and 30 carry no orbit data, as in all original Nikon files (2015–2026).
- The data source can have gaps: BKG holds no rapid orbits for 6–11 Oct 2026, so the start date 12 Oct is missing
  from the hindcast.
- The format was reverse engineered; tested with one D5300.

## Data sources

- Orbits, clocks, Earth rotation, broadcast ephemerides: IGS, provided by BKG (`igs.bkg.bund.de`)
- Gravity field: JGM-3 (`data/JGM3.gfc`), taken from the project duncaneddy/brahe
  (MIT licence, see `data/LICENSE-brahe.txt`)

## Disclaimer

Unofficial project with no affiliation to Nikon Corporation. Nikon, D5300 and COOLPIX are trademarks of their
respective owners. The file format was reverse engineered. Use at your own risk; no guarantee of accuracy.

## Acknowledgements

Thanks to [prof-pguth](https://github.com/prof-pguth), [waziwoo](https://github.com/waziwoo)
and [cowbutt](https://github.com/cowbutt) for collecting original Nikon A-GPS files in
[git_microdem issue #5](https://github.com/prof-pguth/git_microdem/issues/5). Their archives
made it possible to reverse engineer the file format.

## Licence

MIT, see `LICENSE`.
