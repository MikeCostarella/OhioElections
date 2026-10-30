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

## Notes for adding more counties

Done for 2026-11-03: Trumbull (hand-written), Mahoning, Columbiana, Ashtabula, Lake, Cuyahoga, Geauga, Summit, Stark, Portage, Medina, Lorain, Franklin, Hamilton, Montgomery, Lucas, Butler, Warren, Delaware, Clermont, Licking, Greene, Fairfield, Clark, Wood, Richland, Wayne, Miami, Allen, Tuscarawas, Muskingum, Ross, Erie, Hancock, Scioto, Belmont, Jefferson, Marion, Union, Knox, Athens, Washington, Pickaway, Sandusky, Huron, Lawrence, Seneca, Darke, Ashland, Shelby, Auglaize, Brown, Logan, Crawford, Highland, Ottawa, Clinton, Madison, Fulton, Mercer, Preble, Champaign, Defiance, Guernsey, Williams, Coshocton, Perry, Morrow, Putnam, Henry, Hardin, Carroll, Hocking, Jackson, Van Wert, Gallia, Fayette, Pike.
Adams, Harrison, Holmes, Meigs, Monroe, Morgan, Noble, Paulding, Vinton, Wyandot — all 88 counties are done for 2026-11-03.

Some counties (Henry, Mercer, Morrow) don't use lookup.boe.ohio.gov; their sample ballots are only in VoterView.

**Notices can leave races out.** Logan's notice omits the Court of Appeals and a Senate race that are on its ballots; check the sample ballots for appeals/senate races when the notice lacks them.

Sample ballots on lookup.boe.ohio.gov: when get_page_text is refused, javascript_tool can run the search and fetch each `getballot.aspx` PDF for pdf.js.

**Precinct numbers.** Several notices (Delaware, Tuscarawas, Miami, Belmont, Wood) list precincts by number only. Match them to names via the order of PRECINCT_CODE in the SoS file, the PRSID/PRECNAME columns of the county's absentee CSV, or the Board's precinct results; check against a liquor option's named precinct.

**Sample ballots.** lookup.boe.ohio.gov/vtrapp/<county>/ballotlist.aspx sometimes opens from Chrome (Scioto, Jefferson); `getballot.aspx` PDFs read with pdf.js.

**Scanned notices.** Wood's 46-day notice has no text layer; it was read with Tesseract.js OCR in the browser on pdf.js-rendered pages. Check another Board list (candidates, Q&I) against the OCR.

**Unnumbered issues.** Delaware, Clermont and Licking print no local issue numbers in their notices: use descriptive ids and the "see your sample ballot" note (licking.py). Joint vocational districts can be placed from the notice's precinct list (clermont.py, medina.py).

**Voter-file gaps.** Franklin's SoS file has empty school-district columns, so `c.sd()` can't be used there; its school issues are placed from the 46-day notice's precinct lists. Elsewhere, when the notice lists a precinct the voter file doesn't put in a district, add that place by hand (`c.sd(...) + c.p(...)`) with a comment.

**Finding the documents.** Use the Board's site (each spec's `links` has it). In order of preference:
1. A 46-day FWAB election notice. It lists every contest and issue with its precincts.
2. A candidate list plus an issues list or issue synopsis.
3. The precinct sample ballots on lookup.boe.ohio.gov, the last resort (Geauga).

boe.ohio.gov PDFs and most county sites aren't reachable from a cloud session or a script. Open them in Chrome (Claude in Chrome):
- Import pdf.js 4.4.168 from cdnjs on the PDF's own origin, fetch the PDF, and group the text items by y-coordinate into lines.
- Write the result into the page as `<main><pre>` and read it with get_page_text.
- Watch out for scanned PDFs (no text layer); Lorain's "Ballot Text" is one, so look for another document.
- lookup.boe.ohio.gov is blocked to the extension. Geauga's ballots were downloaded with a PowerShell loop over `getballot.aspx?elect=20261103G&prsid=<precinct>&bpty=X` and parsed with pdfplumber (drop chars with size >= 16, the watermark).

**Places.** Run `place_summary.py` on the county's SoS voter file first. Raw place names vary by county:
- `County(rename={...})` fixes odd ones, e.g. `SHALERSVILLE TOWNSHP`, `ROCHESTER TWP & VIL`, `VERMILION CITY ` with a trailing space.
- Precinct-split places (Hamilton's `SILVERTON A/B/C`, Lucas's `PRECINCT WASHINGTON 1/2`) get one display name via `rename`; lib lists it once.
- `bare="Township"` (the default) appends "Township" to bare names like Stark's "JACKSON". Cuyahoga uses `bare=None`.

**Mapping issues to places.** Use the tools in `lib.py`:
- `c.district("cong"|"rep"|"sen", n)` for legislative districts.
- `c.sd("<SoS school district name>")` for school levies. Print the district names from the place json first.
- `c.p(...)` for the city, village or township itself. Use it for liquor options too, and put the precinct in `area`.
- `"county"` for countywide.
- `None` for districts the voter file can't place (park, ambulance and JVSD districts). Those show as "boundaries not mapped".

**Data conventions:**
- Common Pleas judges get no party (plain names, with "no party label on the ballot" in the detail).
- Appeals and congressional candidates get party tags.
- Watch for issue numbers reused across districts (Geauga) and for unnumbered items (Stark's Wayne JVSD).
- Greg Levy (other party, U.S. Senate) is already in the state file.

**Check before handing off:**
- Run `python run.py`, then `npm run check:data` and `npm run build` in react-app.
- Spot-check `#/<county>/2026-11-03/ballot/<Place>` in `npm run preview`.
- Add a CHANGES.md entry.
