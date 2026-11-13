# A-GPS-Datei für Nikon D5300 (NML_28A.ee)

Nikon stellt die A-GPS-Datei `NML_28A.ee` seit 2026 nicht mehr bereit. Dieses Projekt erzeugt sie täglich neu
aus frei verfügbaren Bahndaten des International GNSS Service (IGS) und legt sie unter einer festen Adresse ab.
Die Datei passt für die D5300 sowie COOLPIX P330, P510 und P520.

**Download:** `https://github.com/DEIN-NAME/DEIN-REPO/releases/latest/download/NML_28A.ee`

Aktueller Stand und Prüfergebnisse: [status.md](status.md)

## Benutzung in der Kamera

1. Datei auf die Speicherkarte in den Ordner `NIKON` kopieren.
2. Im Kameramenü die Standortaufzeichnung ausschalten und „A-GPS-Datei aktualisieren“ wählen.
3. Die Kamera zeigt danach das Ablaufdatum der Datei (28 Tage ab Erzeugung).

Je frischer die Datei, desto genauer die Vorhersage. Empfehlung: vor jeder Tour neu laden.

## Einrichtung im eigenen GitHub-Konto

1. Neues öffentliches Repository anlegen und alle Dateien dieses Projekts hochladen (inklusive Ordner `.github`).
2. Reiter **Actions** öffnen, Workflows aktivieren, „A-GPS-Datei aktualisieren“ wählen, **Run workflow**.
3. Nach etwa zehn Minuten liegt die Datei unter **Releases → aktuell**. Danach läuft der Workflow täglich um 15:23 UTC.

Schlägt eine Kontrolle fehl, bricht der Lauf ab, die bisherige Datei bleibt stehen und GitHub schickt eine E-Mail.

## Wie es funktioniert

1. `agps/download.py` lädt Präzisionsbahnen (Rapid, Ultra-Rapid), Erdrotationsparameter und Broadcast-Ephemeriden vom BKG.
2. `agps/orbit.py` passt je Satellit ein Bahnmodell an die letzten 1 bis 5 Tage an (Schwerefeld JGM-3 bis Grad 8, Sonne, Mond,
   Gezeiten, Strahlungsdruck) und rechnet 28 Tage voraus.
3. `agps/generate.py` fittet je 6-Stunden-Fenster einen Ephemeridensatz, kodiert alles im Nikon-Format und prüft die fertige
   Datei gegen die IGS-Prognose und die aktuell ausgesendeten Ephemeriden.
4. `agps/nml28a.py` liest und schreibt das Dateiformat; die Formatbeschreibung steht im Kopf des Moduls.

Lokal ausführen: `pip install -r requirements.txt`, dann `python -m agps.generate --out out`.

## Grenzen

- Die Genauigkeit sinkt mit dem Alter der Datei: wenige Meter am ersten Tag, im Rückblick-Test 7 m (Median) nach 9 Tagen,
  bei Satelliten im Erdschatten bis 260 m. Für die Wochen 3 und 4 fehlen Vergleichswerte.
- Bahnmanöver nach der Erzeugung kann die Vorhersage nicht kennen.
- PRN 1, 22 und 30 bleiben wie in allen Nikon-Originalen (2015–2026) ohne Bahndaten.
- Das Format wurde per Reverse Engineering ermittelt; getestet mit einer D5300.

## Datenquellen

- Bahnen, Erdrotation, Broadcast-Ephemeriden: IGS, bereitgestellt vom BKG (`igs.bkg.bund.de`)
- Schwerefeld: JGM-3 (`data/JGM3.gfc`)
