# Election-night results

Builds `react-app/public/data/results/<county>/<election>.json` from each Board of Elections' election-night report. The app reads that file beside the ballot and, while the count is unofficial, re-reads it every two minutes.

- `sos.py` — the Secretary of State's election-night API (liveresults.ohiosos.gov): every county's statewide offices, Supreme Court, Congress, Court of Appeals, General Assembly and statewide issues, in ~90 requests. Writes `results/state/<election>.json` (statewide totals with each county's numbers under `counties`) and a county file for every county that has no Board module. `sos-dump.js` is the Chrome fallback if the API refuses scripts.
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

## Notes for future elections (learned Nov 3–4, 2026)

**Getting at the reports.** Both Boards' sites refuse non-browser clients: `lib.fetch` got HTTP 403 from the cloud session *and* from the proxied shell on lvp-01, so every refresh on election night went through Chrome — open any page on the Board's own site, run `pdfjs-dump.js` in the console (Claude in Chrome's javascript tool works too), copy the `<main id="pdftext">` text to `downloads/<county>.txt`, run `<county>.py --text`. Whether the GitHub Actions runner is refused too is untested; the workflow just logs "skipped" if so. A results refresh is therefore a hands-on step, not a cron: plan for it.

**Per-county report locations and timing (2026 general):**

| County | Where the report is | Format | Posted |
|---|---|---|---|
| Trumbull | `https://boe.co.trumbull.oh.gov/pdfs/Election%20Summary.pdf` — same URL overwritten through the night; `HEAD` it and compare `Last-Modified` before parsing. Appears on the Election Results page as a dated PDF only after the canvass. | Summary Results Report PDF; a one-page second report (a late-added question) is appended as the last page | 7:36 PM absentee/early (0 of 158 precincts); 10:01 PM all 158 precincts |
| Mahoning | Home page `https://vote.mahoningcountyoh.gov/` → "Final Unofficial" link into the Document Center (`/DocumentCenter/View/<n>/Final-Unofficial`; `<n>` changes per election — 2678 this time) | Summary Results Report PDF, no "Total Votes Cast" rows, titles prefixed "For", duplicate judge titles | 9:22 PM, all 212 precincts (file dated 6:06 AM next day) |

**Parser gotchas seen so far** (all handled in `lib.py`; check a new county's dump for others):
- A long candidate name wraps as name / numbers / rest-of-name (Mahoning's Ramaswamy/McColley).
- Rows with no votes yet print `For the Tax Levy | 0` with no per cent; titles can end in a number (`AUS 17`), so a per-cent-less row needs the pipe.
- Party codes vary: `OTHER` (Trumbull) vs `OPC` (Mahoning) for the same candidate; `lib.PARTIES` lists them.
- The report's candidate names differ from the ballot file's (`David P. Joyce` vs `David Joyce`, `and` vs `/` for tickets, truncation): matching is by the first person's last name.
- A Board may run one ballot-file issue as two report blocks (weekly and Sunday liquor options): map one and `lib.IGNORE` the other, and note it in CHANGES.md.
- The statewide ballot file can list a candidate a county's tabulator omits (Aidan Michael Jeffery in Trumbull): the app shows "No total reported yet", which is right.

**Statewide feed (sos.py).** The SoS election-night site is "Ohio Decides", https://liveresults.ohiosos.gov/ (not electionresults.ohiosos.gov, which does not exist; the SoS data portal at data.ohiosos.gov only has certified results). Its JSON API, all GET: `/Api/v1/Contest/getCountyList`, `getContestList` (objectId → display name with district/term), `GetContestsByCounty?countyId=`, `GetContestDetailsObject?contestName=&contestObjectId=&resultsLevel=State` (one contest by county), `GetElectionSummaryCsv` (registered / ballots / turnout / precincts per county), `getStatistics`, and `download?filename=VSSC1622XmlFileBlob` (the whole election as NIST 1500-100 XML). Vote counts are `candidatesRunning[].vCount`; write-ins are rows with `isWriteIn`; `tcVotes` excludes write-ins. Party codes are single letters (D, R, L, OP, WI). The two Supreme Court seats share a `name` in the county response — use `getContestList`'s display name (term date) to tell them apart. No last-updated time is served; `asOf` is the fetch time. On Nov 4 2026 the SoS county numbers matched Trumbull's and Mahoning's Board reports exactly.

**Status changes.** Re-run each county on the certified report after the canvass (the header says OFFICIAL RESULTS) so `status` flips to `official` and the app stops polling.
