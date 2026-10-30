# Ballot generator

Builds `react-app/public/data/county/<county>/2026-11-03.json` for the counties with a spec here.
Trumbull's file was written by hand before the generator existed and is not regenerated.

- `place_summary.py`: turns a county's SoS voter file (from its `*CountyVoters/SourceData`) into `places/<county>.json`, which records the districts each city, village and township's voters are in. Only counts per place, no voter records.
- `<county>.py`: that county's contests and issues, typed from the Board of Elections' own documents (linked in each file's `sources`).
- `lib.py`: shared helpers. District and school-district lookups come from the place summary, so "Where you live" is computed, not typed.
- `run.py`: regenerates every county listed in it.

PowerShell:

```powershell
cd C:\projects\OhioElections\tools\ballots; python run.py
cd C:\projects\OhioElections\react-app; npm run check:data
```

Adding a county: summarise its voter file with `place_summary.py`, write `<county>.py` from the Board's candidate and issue lists (copy the closest existing spec), add it to `run.py`, run it, and add the slug to `react-app/public/data/county/index.json`.
