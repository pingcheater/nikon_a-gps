# A-GPS file for the Nikon D5300 (NML_28A.ee)

Nikon no longer provides the A-GPS file `NML_28A.ee` (since 2026). This project regenerates it every day from
freely available orbit data of the International GNSS Service (IGS) and publishes it at a fixed address.
The file works with the D5300 and the COOLPIX P330, P510 and P520.

**Download:** [Download](`https://github.com/pingcheater/nikon_a-gps/releases/download/current/NML_28A.ee`)

Current state and check results: [status.md](status.md)

## Using the file in the camera

1. Copy the file to the `NIKON` folder on the memory card.
2. In the camera menu, switch off location recording and select "Update A-GPS file".
3. The camera then shows the expiry date of the file (28 days after generation).

The fresher the file, the more accurate the prediction. Download it again before each trip.

## How it works

1. `agps/download.py` downloads precise orbits (rapid, ultra-rapid), Earth rotation parameters and broadcast
   ephemerides from BKG.
2. `agps/orbit.py` fits an orbit model to the last 1 to 5 days for each satellite (JGM-3 gravity field up to
   degree 8, Sun, Moon, solid Earth tides, solar radiation pressure) and propagates it 28 days ahead.
3. `agps/generate.py` fits one ephemeris set per 6-hour window, encodes everything in the Nikon format and checks
   the finished file against the IGS prediction and the current broadcast ephemerides.
4. `agps/nml28a.py` reads and writes the file format; the format description is in the module header.

Run locally: `pip install -r requirements.txt`, then `python -m agps.generate --out out`.

## Limitations

- Accuracy decreases with the age of the file: a few metres on the first day; in a hindcast test 7 m (median)
  after 9 days, up to 260 m for satellites passing through the Earth's shadow.
- The prediction cannot know about orbit manoeuvres after the file was generated.
- PRN 1, 22 and 30 carry no orbit data, as in all original Nikon files (2015–2026).
- The format was reverse engineered; tested with one D5300.

## Data sources

- Orbits, Earth rotation, broadcast ephemerides: IGS, provided by BKG (`igs.bkg.bund.de`)
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


