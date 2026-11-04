# Election-night results

Builds `react-app/public/data/results/<county>/<election>.json` from each Board of Elections' election-night report. The app reads that file beside the ballot and, while the count is unofficial, re-reads it every two minutes.

- `lib.py` — parses the tabulator **Summary Results Report** (the PDF layout Trumbull and many other Ohio Boards post), matches each block to the ballot's contest and issue ids, and writes the JSON.
- `<county>.py` — the county's report URL and its title → id map (`TITLES`). Unmapped titles come out under `"unmatched"` in the JSON and make the script exit 1, so the deploy check catches them.
- `run.py` — refreshes every county listed in it.
- `pdfjs-dump.js` — reads a PDF in Chrome when the Board's site refuses scripts (most do).

PowerShell:

```powershell
cd C:\projects\OhioElections\tools\results; python run.py
cd C:\projects\OhioElections\react-app; npm run check:data
```

One county from a file instead of the live URL:

```powershell
cd C:\projects\OhioElections\tools\results; python trumbull.py --pdf "C:\Users\mike\Downloads\Election Summary.pdf"
cd C:\projects\OhioElections\tools\results; python trumbull.py --text downloads\trumbull.txt
```

## Through the night

The GitHub Actions workflow `.github/workflows/results.yml` runs `run.py` every 10 minutes on election night (enable the schedule in the file the day before; disable it after the canvass), commits any file that changed and redeploys the site. If a Board's site turns the runner away, the log says `fetch failed`; run the county by hand on lvp-01 and commit through Statehouse.

The results file's `status` is `unofficial` until the Board certifies; set it to `official` by re-running the parser on the certified report (its header says OFFICIAL RESULTS), which stops the app's polling.

## Adding a county

1. Find the Board's election-night report. The Summary Results Report PDF parses as is; for an HTML results page or a Clarity/ENR JSON feed, add a reader to `lib.py` that yields the same `Block`s.
2. Copy `trumbull.py`, set `URL`/`SOURCE`, and fill `TITLES` from the report's contest titles — the ids are in `react-app/public/data/county/<county>/<election>.json`.
3. Run it once with `--text` or `--pdf`, fix anything in `unmatched`, and add the module to `run.py`.
