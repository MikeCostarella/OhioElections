# Changes

# Nov 4, 2026 — Reports tab

- Third tab beside "On the ballot" and "Results" (also in the hamburger View section; route `#/<county>/<election>/reports`). Five reports, each table with a ⬇ CSV download named `<county>-<election>-<report>.csv`:
  - **Ballot makeup** — works before any count: contests by office group (statewide vs. county/district, candidates, unopposed), candidates by party, issues by kind (levy renewal/additional/replacement, question, liquor option, state issue), unopposed races, issues by jurisdiction.
  - **Turnout & roll-off** — registered, ballots cast, turnout against statewide, precincts, top-of-ticket share, furthest roll-off; then every race and issue with votes cast as a share of ballots and the roll-off in points. Roll-off is only figured for contests and issues the whole county votes on (no `places` list); district races and local levies show their votes and "part of county" instead, so a village levy never reads as 99% fatigue.
  - **County vs. statewide** — every statewide candidate and State Issue 3: county votes and share, statewide share from the Secretary of State's file, the difference in points (orange at ±5), the county's rank among the 88 counties for that candidate or "yes", and the strongest county. Tiles: races counted, where the county's leader differs from Ohio's, the biggest gap, turnout.
  - **Party lines** — every race with a DEM and/or REP candidate: both shares, a two-party split bar, DEM − REP margin, the same margin statewide and the county's difference from Ohio. Tiles: contested D-vs-R races and who leads how many, county lean across the statewide races against Ohio's, ticket-splitting spread, best race for each party. Nonpartisan races are left out.
  - **Issues & levies** — passing/failing counts (Passed/Failed once official), levies passing of total with average yes share, closest issue; by kind with pass/fail and average yes; every issue in ballot order or by yes share with a Passing/Failing pill.
- Reports that need totals show a one-line "no totals loaded yet" note for counties without a results file; Ballot makeup always works. Language follows status like the Results view; nothing is called.
- **All of Ohio** scope toggle beside the county's name, with four statewide reports from the Secretary of State's file (your county's row is highlighted and ranked in each):
  - **Statewide results** — ballots, turnout, precincts, counties fully reporting; every statewide candidate's votes and share with the number of counties they lead ("counties led", of 88); State Issue 3 with counties yes/no.
  - **Counties ranked** — pick any statewide race or issue: all 88 counties with votes, each candidate's share (leader in bold), the leader's margin, sortable by margin, votes or name.
  - **Turnout by county** — registered, ballots cast, turnout and difference from Ohio for all 88, with Election Day precincts still out flagged; median, highest and lowest.
  - **Party lean by county** — each county's average DEM − REP margin across the statewide races with one of each (8 this time), its difference from Ohio's, how many of those races the Democrat leads, the ticket-splitting spread, and the strongest margin for each party.
- Statewide reports need no county: the county picker opens with a **Statewide reports** panel (one button per report, each describing what it shows) above the county grid; the route is `#/reports[/<election>[/<report>]]` (`results`, `counties`, `turnout`, `lean`), the hamburger menu's Reports item works before a county is chosen, and the page offers "Choose a county…" beside the All-of-Ohio scope.
- `tools/results/sos.py` now writes a top-level `counties` block into `results/state/<election>.json` — each county's registered voters, ballots counted, turnout and precincts from the SoS summary CSV — which the turnout report reads. The state file was regenerated from the saved Nov 4 12:17 PM bundle (otherwise byte-identical); `ResultsFile.counties` added to the types.
- `src/components/ReportsView.tsx` and `StatewideReports.tsx` (new), `reports` added to `AppView`/`VIEW_LABELS` in `MainMenu.tsx`, tab and route in `App.tsx`, report styles (CSV button, inline bars, D/R split bar, highlighted "yours" row, two-column tables) at the end of `global.css`.

# Nov 4, 2026 — Results view

- The Results tab is now a results page. Stat tiles: ballots cast of registered, turnout against the statewide figure, Election Day precincts, report time with the source link, and a link to the county's Voters app. Then every race in a table — leader (party, "unopposed"), votes, share, margin in votes and points (orange under 2 points), runner-up, and a Statewide column from the Secretary of State's file showing the statewide leader and share, flagged "county differs" when the county's leader is not the statewide one. Then every issue — yes/no votes and shares, margin in points, a Passing/Failing pill (Passed/Failed once official), and the statewide yes share for State Issue 3.
- "Ballot order" / "Closest first" toggle; closest sorts races by margin in points and issues by distance from 50%.
- Language follows status: "Leading"/"Passing" while unofficial, "Winner"/"Passed" once a county's file is official. The page never calls a race.
- The statewide file (`results/state/<election>.json`, 188 KB) is loaded only when the Results tab opens; `loadStateResults` in `load.ts`; `counties` fields added to the result types. Counties with no totals keep the old "where the results are published" page.


# Nov 4, 2026 — statewide results feed (all 88 counties)

- `tools/results/sos.py`: the Secretary of State's election-night API ("Ohio Decides", liveresults.ohiosos.gov) — `GetContestsByCounty` for each of the 88 counties plus the contest list and the election summary CSV. Every county now has a results file with its statewide offices, Supreme Court seats, U.S. Senate and House, Court of Appeals and General Assembly races and State Issue 3, with registered voters, ballots counted, turnout and precincts from the summary CSV. Trumbull and Mahoning keep their Board files (local races and issues); the SoS numbers for them matched the Boards' reports exactly.
- `results/state/2026-11-03.json`: statewide totals per contest and issue, with each county's numbers under `counties` — the data for the coming Results view's county-vs-statewide comparison. Not read by the app yet.
- District races are matched to each county's ballot ids by their candidates, with the feed's office and district number as a tie-breaker (two Millers on Henry's ballot); name matching tolerates the feed's punctuation ("Lawson Rowe" / "Lawson-Rowe", "Hunter- Kalagidis"). A contest the feed lists without candidates (the 12th District Court of Appeals seat, term 01/01/2027, in all eight of its counties) is skipped, not an error.
- Tuscarawas ballot: added the 5th District Court of Appeals race (Matthew George) that both Board documents omit — the SoS feed reports 23,911 Tuscarawas votes in it, so it was on the ballot; cited to the feed.
- `run.py` runs `sos` first, then the Board modules. `sos-dump.js` is the Chrome fallback if the API ever refuses scripts (it did not: the direct fetch worked from lvp-01 in about a minute).


# Nov 3, 2026 — election-night totals

- Totals beside every race and issue. A new per-county results file (`react-app/public/data/results/<county>/<election>.json`), kept apart from the ballot file, holds the Board's count: a vote bar, count and share under each candidate (sorted by votes, leader tagged "leading" — never "won"), For/Against bars under each levy and question, total votes cast and write-ins.
- Banner above the ballot: Unofficial/Official, the report time, what is counted so far ("Absentee and early"), Election Day precincts reporting, ballots cast and turnout, and a link to the Board's report. The Results view shows the same count details and keeps the "where the results are published" links.
- While a count is unofficial the app re-reads the results file every two minutes (and when the tab comes back into view); the service worker fetches `data/results/` network-first with a one-hour cache so a stale total is never served.
- Trumbull County loaded from the Board's Election Summary — first the 7:36 PM absentee/early report, then the 10:01 PM report with all 158 Election Day precincts (75,531 ballots, 57.43% turnout): all 17 contests and 36 issues matched to the ballot ids.
- Mahoning County (Nov 4) loaded from the Board's 9:22 PM "Final Unofficial" Summary Results Report (212 of 212 precincts, 90,475 ballots, 58.26% turnout): 22 contests and 30 issues. Its report has no "Total Votes Cast" rows (totals are summed), prefixes titles with "For", wraps one long candidate name over three lines, and titles the five Common Pleas races identically — the parser now handles all four, matching duplicate titles by their candidates. Two liquor blocks are skipped on purpose (`skipped` in the JSON): the Board ran Tobacco City and the Indian Grocery Store as separate weekly and Sunday questions, while the ballot file lists each once.
- Data notes (Mahoning): Salem City's recreation levy and Perry Township's police levy show 0 votes in the report (both are Columbiana County districts with a sliver of Mahoning voters); the report prints Salem's levy as 1.3 mills where the ballot file says 1 mill.
- `tools/results/`: parser for the tabulator "Summary Results Report" PDF (pdfplumber, or a text dump from Chrome via `pdfjs-dump.js` when a Board's site refuses scripts), `trumbull.py` with the report-title → ballot-id map, `run.py`. Unmapped titles come out as `unmatched` and fail the data check.
- `npm run check:data` now validates results files too: ids and candidate names must be on the ballot, votes must not exceed the total, nothing unmatched.
- `.github/workflows/results.yml`: polls the Boards every 10 minutes, commits changed results and calls the deploy workflow (now also `workflow_call`). Schedule on for election week only.
- Types: `ResultsFile`, `ContestResult`, `IssueResult`, `CandidateResult` in `src/data/types.ts`; `loadResults`, `RESULTS_POLL_MS`, `shortTime`, `fmtInt`, `pct` in `src/data/load.ts`; new `ResultsBanner` component.


# OhioElections — first build (Oct 30, 2026)

- New fleet app: React 18 + TypeScript + Vite PWA, hamburger menu (View / County / Links), build stamp, GitHub Pages deploy.
- One statewide app with county-scoped hash routes (`#/<county>/<election>/<view>/<place>`) so OhioCounties, CurrentElectionStatistics and the Voters apps can deep-link.
- 2026 General Election (Nov 3): the statewide ballot for all 88 counties — Governor/Lt. Governor, Attorney General, Auditor, Secretary of State, Treasurer, U.S. Senate, two Ohio Supreme Court seats, and State Issue 3 (voter photo ID).
- Trumbull County full ballot from the Board's candidate list, issues running list and 46-day notice: 9 county/district contests and 35 local questions and issues (22 tax levies, 8 questions, 5 liquor options), each linked to its source PDF.
- "Where you live" filter for Trumbull's 35 cities, villages and townships; kind filter (levies / questions / liquor options) and search over the local issues.
- Results view links to the Board's results page and the Secretary of State's 2026 results; outcomes get loaded after the canvass.
- `npm run check:data` validates the ballot files (sources, places, unique ids, index) and runs before every deploy.
- Other counties show the statewide ballot and a link to their Board until their local data is added.

Data notes (Trumbull):
- The Newton Falls Village photo-traffic-enforcement referendum is on the Board's issues list but not its 46-day notice; it is included and marked.
- Casa Angel's liquor options: the issues list gives Cortland precinct F, the notice gives H; shown as F with a note.
- The candidate list prints the commissioner term as "1/1/25"; the 46-day notice's "FTC 1/1/2027" is used.

# Oct 30, 2026 (later)

- "Related apps" row under the county picker: the county's Voters app, Election Statistics and the Ohio Counties hub as labelled buttons, so the way back to the rest of the fleet is obvious. The Board of Elections links (View your ballot, Where do I vote?) stay as plain links beside the view tabs. The menu keeps its links too.

# Oct 30, 2026 (six more counties)

- Full ballots for Mahoning, Columbiana, Ashtabula, Lake, Cuyahoga and Geauga, each from that county Board of Elections' own documents: Mahoning's filings list, Columbiana's pre-election zero report, Ashtabula's candidate list and issues sheet, Lake's candidate list and certified issues, Cuyahoga's candidate list and issues list (105 issues, ballot wording verbatim).
- "Where you live" for those counties is computed from each county's SoS voter file (in its *CountyVoters repo): a congressional, state rep or state senate district, or a school levy, shows for a city, village or township when any of its voters are in it. New `tools/ballots/` holds the generator (`place_summary.py`, one spec per county, `run.py`).
- Special districts whose boundaries aren't in the voter file (Ashtabula's park and ambulance districts, Cuyahoga County Council districts) stay listed for every place, marked "boundaries not mapped".
- Levy cards show the Board's collection estimate ("$X a year; $Y for each $100,000"); levy fields the Board doesn't give are left out.
- Statewide: Greg Levy (other-party) added to the U.S. Senate race. He is on the Columbiana, Lake, Ashtabula and Cuyahoga Boards' lists; the Trumbull 46-day notice and the Mahoning filings list leave him out.
- Source links are shortened to the county and document ("Lake candidate list"); the full title is in the tooltip.
- Geauga from all 91 of the Board's official precinct sample ballots (downloaded with a one-off script). Its "Where you live" comes from the ballots themselves. Geauga reuses issue numbers across school districts (Issue 4 is Berkshire's income tax in 13 precincts and Kirtland's levy in one; Issue 5 is Cardinal's levy in 9 and Mentor's in one), so each is listed separately.

# Oct 30, 2026 (Summit, Stark, Portage, Medina, Lorain)

- Full ballots for Summit, Stark, Portage, Medina and Lorain (11 counties with local data now, plus Trumbull's original):
  - Summit: the Board's candidate list and 60-day issue synopsis (20 contests, 53 issues).
  - Stark: the Board's candidate list and numbered issues list (15 contests, 29 issues).
  - Portage: the Board's updated 46-day notice (11 contests, 29 issues, including four Mogadore charter amendments).
  - Medina: the Board's 46-day notice (10 contests, 35 issues, including Rittman's 15 charter amendments).
  - Lorain: the Board's certified candidate and issues lists plus its 46-day notice for precincts (10 contests, 35 issues).
- "Where you live" comes from each county's SoS voter file, as before. Stark's file lists townships by bare name ("JACKSON"); the generator adds "Township" (`County(bare=...)`). Odd SoS names are renamed: Summit's NORTHFIELD CTR TP and SAGAMORE HLS TWP, Portage's SHALERSVILLE TOWNSHP, Lorain's ROCHESTER TWP & VIL.
- Stark's fire and road districts are shown for their township. The Wayne County JVSD levy (on Stark's list with no issue number) is marked "boundaries not mapped".

# Oct 30, 2026 (Franklin, Hamilton, Montgomery, Lucas, Butler)

- Full ballots for Franklin, Hamilton, Montgomery, Lucas and Butler (16 counties with local data now, plus Trumbull's original), each from the Board's 46-day FWAB notice, checked against its candidate and issues lists:
  - Franklin: 28 contests, 50 issues (19 liquor options; three unnumbered items: Delaware Area Career Center levy, Pickerington LSD income tax, Pickerington Library levy). The notices of election for individual issues supplied ballot wording and collection estimates.
  - Hamilton: 28 contests, 30 issues. The Board's ballot-issues document supplied the full wording and estimates.
  - Montgomery: 18 contests, 22 issues.
  - Lucas: 15 contests, 27 issues. The Board's documents are Google Drive files linked from lucascountyohiovotes.gov.
  - Butler: 16 contests, 16 issues.
- `lib.py`: precinct-split places renamed to one display name (Hamilton's Silverton A/B/C and St. Bernard 1-A..4-A, Lucas's Washington 1/2 and Waterville A/B) are listed once.

Data notes:
- Franklin's SoS voter file has empty school-district columns, so Franklin's school and special-district issues are placed by matching the 46-day notice's precincts to the voter file's precincts (typed in the spec). Small slices of Lithopolis, Pickerington and Brice that sit in Madison and Truro township precincts are included in those townships' levies.
- Where the 46-day notice lists precincts the voter file doesn't place in a district, the place is added by hand (Montgomery: West Carrollton in Miamisburg CSD Issue 5, New Lebanon in Jackson Twp Issue 24, Dayton in Jefferson Twp Issue 25; Butler: St. Clair Twp in Senate 5 / House 40; Lucas: Harding Twp in Evergreen LSD Issue 4, Harding Twp and Ottawa Hills in Toledo CSD Issue 9).
- Hamilton: Silverton and St. Bernard are shown as villages, as every Board document calls them. Issue 17 (Madeira D Sunday sales) was withdrawn on Sep 24 and is left out. Where the 46-day notice and the later ballot wording differ (Forest Park Issue 14 additional, Issue 10 renewal and increase, Fairfax 0.96 mill), the ballot wording is used.
- Butler: in the Court of Appeals seat starting 1/1/2027, Republican Matthew Byrne withdrew on 9/16 (his votes won't count); write-in Willa Concannon is the only active candidate. Butler's documents give only type, rate and term for issues, so its charter amendments have no ballot text and its levies no estimates.
- Lucas: the Swanton Public Library levy (Fulton and Lucas) is "boundaries not mapped". QuikTrip's liquor option (Issue 11) is "wine and mixed beverages" on the notice and "Sunday sales" on the issue list; the notice's wording is used.
- Franklin has no Issue 39 in any Board document.

# Oct 30, 2026 (fresh ballot data)

- Ballot data (`data/**`) is no longer precached by the service worker. It is fetched network-first (cached copy used offline), so newly added counties show right after a deploy instead of after the old service worker is replaced. Previously a browser that had opened the app earlier kept showing "Only the statewide races..." for counties added since.

# Oct 30, 2026 (Warren, Delaware, Clermont, Licking, Greene)

- Full ballots for Warren, Delaware, Clermont, Licking and Greene (21 counties with local data now, plus Trumbull's original), each from the Board's 46-day FWAB notice:
  - Warren: 10 contests, 6 issues. The Board's per-issue ballot-language PDFs gave wording, estimates and first-due years.
  - Delaware: 11 contests, 28 issues (12 liquor options). The 46-day notice (revised Oct 2) is the Board's only posted ballot document.
  - Clermont: 8 contests, 8 issues. The 46-day notice (revised Sep 15) is the Board's only posted ballot document, plus its withdrawal notice for Matthew Byrne.
  - Licking: 9 contests, 28 issues, checked against the certified candidate list and filed-issues list.
  - Greene: 10 contests, 27 issues, checked against the candidate list and questions-and-issues list.

Data notes:
- Delaware, Clermont and Licking don't number their local issues in any posted Board document; those issues have descriptive ids and a note pointing to the sample ballot for the numbers. Greene leaves eight items unnumbered (two Sunday liquor options, Kettering's five charter amendments, Southeastern Local's income tax); they are marked "Unnumbered in Greene County".
- 12th District Court of Appeals (Warren, Clermont, as in Butler): Republican Matthew Byrne withdrew; write-in Willa Concannon is the only active candidate.
- Warren Issue 4 (Franklin City Schools income tax) is on the Board's issues list but not its 46-day notice; it is sourced to the issues list. The voter file's "BUTLER VILLAGE" is Butlerville.
- Greene: the SoS voter file labels Southeastern Local (Clark) voters "SOUTHEAST LOCAL SD (PORTAGE)"; the spec uses that label. Issue 20 (Miami Township fire/EMS, 0.8 mill) is "5 years" and "CPT" on the Board's list; it is shown as continuing.
- Clermont: the U.S. Grant career center issues are placed from the notice's precinct list (career center districts aren't in the voter file). Clermont and Delaware levies give rate and term only (no estimates).
- Delaware: the notice names precincts by number; they match the Board's precinct names in alphabetical order (checked against the voter file). Township levies that reach into a city or village (Berlin, Concord, Orange) include that place, with the exact precincts in the area text.
- Licking: Heath is added to House 68 by hand (the notice lists a Heath precinct the voter file puts elsewhere). Obvious typos in the Board's issue wording are corrected.

# Oct 30, 2026 (Fairfield, Clark, Wood, Richland, Wayne)

- Full ballots for Fairfield, Clark, Wood, Richland and Wayne (26 counties with local data now, plus Trumbull's original), each from the Board's 46-day FWAB notice:
  - Fairfield: 8 contests, 14 issues, checked against the certified candidates and issues list.
  - Clark: 11 contests, 36 issues (12 New Carlisle liquor options). The notice is the Board's only posted ballot document.
  - Wood: 10 contests, 24 issues, checked against the certified candidate list and Q&I list. The notice is a scanned PDF (read with OCR); its numeric precinct codes were matched to names using the Board's May 2026 precinct results.
  - Richland: 9 contests, 30 issues. The notice is the only Board document readable without the lookup search form.
  - Wayne: 11 contests, 42 issues, checked against the Board's 256-page all-precinct sample ballots. Includes the Doylestown and Chippewa Township merger questions and their merger-commission elections (vote for up to 5; new "Township offices" group).

Data notes:
- None of the five print local issue numbers (Wayne numbers only State Issue 3); issues have descriptive ids and the sample-ballot note.
- Shared issues reuse the neighbouring county's ids and wording: Fairfield's Pickerington LSD/library and Columbus Issues 8–9 (Franklin) and Southwest Licking/Pataskala library/Buckeye Lake (Licking); Clark's Southeastern LSD income tax (Greene); Wayne's Rittman charter amendments (Medina), Norton charter amendments (Summit), Wayne JVSD (Stark) and Canaan fire (Medina).
- Rittman amendment #8 (Section 6.05): Medina's notice says the Law Director must be an "attorney-in-fact", Wayne's says "attorney-at-law"; each county's file follows its own Board.
- Wood's voter file splits townships into precinct pieces (Lake Twp East/Latcha/North/Union, Perrysburg Twp Belmont/…/PRBG Fallen Timbers, Portage West, …); each is renamed to its township. Where the notice's congressional and House precinct lists disagree with the voter file, the voter file is used. Herringshaw withdrew from the commissioner race (Ryan E. Lee is the Republican).
- Wayne: the SoS file's "FREDERICKTOWN VILLAGE" is Fredericksburg. Burbank has two identical 3-mill current-expense renewals; both are on the ballot.
- Clark: Harmony Township's two 1-mill EMS renewals and Bethel Township's three 2-mill fire renewals differ only in the amount collected; each is noted. The probate judge's term start isn't in the notice and is left off.
- Richland: Galion's two council-term questions apply to its small Richland piece (precinct Sandusky split 3) and are shown under Sandusky Township. The Village of Lucas income tax prints "commencing 1/1/2026", kept as printed.

# Oct 30, 2026 (Miami, Allen, Tuscarawas, Muskingum, Ross, Erie, Hancock, Scioto, Belmont, Jefferson)

- Full ballots for ten more counties (36 with local data now, plus Trumbull's original), each from the Board's 46-day FWAB notice:
  - Miami: 9 contests, 13 issues, plus the Board's separate notice for the Piqua special election held the same day (data-center charter amendment and three recall questions).
  - Allen: 6 contests, 10 issues (notice posted as a Dropbox file linked from the Board's election page).
  - Tuscarawas: 9 contests, 27 issues, checked against the certified candidates and issues list.
  - Muskingum: 9 contests, 18 issues.
  - Ross: 8 contests, 9 issues, checked against the candidate list (scanned, read with OCR) and issues list; Waverly CSD and Miami Trace LSD details from the Pike and Fayette Boards' notices.
  - Erie: 7 contests, 22 issues, checked against the candidate and issue filings.
  - Hancock: 8 contests, 7 issues, checked against the Board's candidate and issues lists (Google Docs).
  - Scioto: 9 contests, 13 issues, with wording and estimates from the Board's precinct sample ballots.
  - Belmont: 10 contests, 17 issues.
  - Jefferson: 9 contests, 18 issues, checked against the candidate list, issue list and all 92 precinct sample ballots.

Data notes:
- Only Tuscarawas, Erie and Jefferson number their local issues; the others use descriptive ids and the sample-ballot note.
- 5th District Court of Appeals (Matthew George): on the other 5th District counties' ballots but in neither Tuscarawas document, so it is not listed for Tuscarawas.
- 4th District Court of Appeals: Scioto's 46-day notice lists Peter B. Abele, but its sample ballots (updated Oct 12) and Ross's Oct 8 candidate list have Jayme Hartley Fountain (REP) vs Todd L. Grace (DEM); both counties use the latter.
- Miami: Piqua's Ward 1, 3 and 5 successor candidates weren't named in the special-election notice and aren't listed. Montgomery's City of Union income tax (Issue 21) is not on Miami's notice although 21 Union voters live in Miami County; not added.
- Ross: Dan D. Cryder (commissioner) is on the Oct 5 notice but not the Oct 8 candidate list; left out.
- North Baltimore LSD income tax: Hancock's full ballot wording says it renews a tax expiring at the end of 2027; Wood's entry follows Wood's shorter issues list.
- Erie's Vermilion items reuse Lorain's titles and wording under Erie's own issue numbers.
- Barnhill (Tuscarawas) and Rarden (Scioto) vote on surrendering their village corporate powers. Tuscarawas Issue 4 is a Claymont CSD levy decrease by petition.
- Renames: Allen's reversed township names ("Township Sugar Creek"), Muskingum's "FRAZEYBURG" (Frazeysburg), Jefferson's "MT PLEASANT TWP".
- Misprints kept out: Belmont's Holloway levy "$42,000 for each $100,000" (only the annual figure is shown); Jefferson's 9-1-1 levy years follow the issue list and ballots, not the notice.

# Oct 30, 2026 (Marion, Union, Knox, Athens, Washington, Pickaway, Sandusky, Huron, Lawrence, Seneca)

- Full ballots for ten more counties (46 with local data now, plus Trumbull's original), each from the Board's 46-day FWAB notice, cross-checked against precinct sample ballots wherever lookup.boe.ohio.gov opened (Union 87, Pickaway 65, Washington 64, Lawrence 99 ballot styles; Huron, Knox, Seneca by sample):
  - Marion: 8 contests, 12 issues (notice only).
  - Union: 7 contests, 15 issues (notice at unioncountyohio.gov; wording and estimates from the ballots).
  - Knox: 8 contests, 16 issues.
  - Athens: 8 contests, 28 issues (Issues 1, 2, 4–29), wording from the Board's notices of election.
  - Washington: 9 contests, 7 issues.
  - Pickaway: 8 contests, 16 issues (incl. Ashville's EdgeConneX data-center referendum).
  - Sandusky: 10 contests, 22 issues (the Board publishes a .docx notice, .xlsx candidate list, .txt issues list and all 61 sample ballots on sanduskycountyoh.gov).
  - Huron: 10 contests, 22 issues.
  - Lawrence: 8 contests, 15 issues (8 liquor options).
  - Seneca: 6 contests, 6 issues.

Data notes:
- Only Athens numbers its local issues; the rest use descriptive ids and the sample-ballot note.
- 4th District Court of Appeals: the Washington and Pickaway notices (like Scioto's) list Peter B. Abele, but every sample ballot has Jayme Hartley Fountain (REP) vs Todd L. Grace (DEM); all 4th District counties use the ballots.
- Ross: the Miami Trace LSD renewal is a fixed sum of $1,900,000 a year (about 2.2 mills, per the Pickaway ballot), not "1.9 mills"; corrected.
- Shared items reuse ids and wording: South-Western CSD bond (Franklin Issue 6, Pickaway), DACC (Delaware, Union, Marion), Miami Trace (Ross, Pickaway), Fostoria (Wood, Hancock, Seneca), Green Springs fire and Old Fort LSD (Seneca, Sandusky), Bellevue parks (Erie, Sandusky, Huron), Plymouth cemetery and South Central LSD (Richland, Huron), Loudonville-Perrysville and its library (Richland, Knox).
- Where the ballots and the notice differ, the ballots are used: Huron's Norwalk fire levy is 0.9 mill (notice ".09"); Pickaway's Deercreek road levy amounts and years; Union's Northern Union fire levy also covers Jackson and York townships; Lawrence's Fayette Twp fire levy also covers South Point; Knox's 0.8-mill renewal is the Loudonville library's.
- Voter-file names: Sandusky's Fremont, Clyde and Bellevue precinct pieces are merged; Riley Township's voters are coded as Rice Township (Riley has no place of its own; neither has a local issue). Knox's "GANN VILLAGE" is Brinkhaven. Marion's and Lawrence's "TWP." names and Marion's LaRue are renamed. Lawrence's file calls Fairland Local "FAIRLAWN LOCAL SD (SHELBY)".

# Oct 30, 2026 (Darke, Ashland, Shelby, Auglaize, Brown, Logan, Crawford, Highland, Ottawa, Clinton)

- Full ballots for ten more counties (56 with local data now, plus Trumbull's original), each from the Board's 46-day FWAB notice, cross-checked against precinct sample ballots and candidate/issues lists where posted:
  - Darke: 8 contests, 6 issues (notice only).
  - Ashland: 6 contests, 15 issues (notice, candidate and issues lists, all 68 sample ballots).
  - Shelby: 6 contests, 9 issues.
  - Auglaize: 9 contests, 12 issues.
  - Brown: 10 contests, 7 issues.
  - Logan: 8 contests, 8 issues (all 69 sample ballots).
  - Crawford: 7 contests, 15 issues (Issues 4–18; the Board's own site, crawfordcountyohioboe.gov).
  - Highland: 8 contests, 6 issues (Issues 1–6; all 65 sample ballots).
  - Ottawa: 12 contests, 16 issues (Issues 4–19). The 46-day notice is a scanned image, so the spec is built from the Board's all-precinct sample-ballot PDF.
  - Clinton: 7 contests, 18 issues (incl. four Wilmington zoning referendums by petition).

Data notes:
- 4th District Court of Appeals: Highland's notice marks Peter B. Abele "Withdrawn due to death"; his name stays on the printed ballots and a supplemental ballot lists Jayme Hartley Fountain (REP) vs Todd L. Grace (DEM). That is why the Scioto, Washington and Pickaway notices still show Abele.
- Logan's notice leaves out the Court of Appeals and State Senate 1st District races; both are on its sample ballots and are included. (Tuscarawas's notice also leaves out the 5th District Court of Appeals race; it is still not listed there.)
- 12th District Court of Appeals: Brown's and Clinton's notices also list write-ins Victor M. Haddad and Curt Carl Hartman, who withdrew later; only Willa Concannon is listed, as in Butler, Warren and Clermont.
- Miami Trace LSD renewal ($1,900,000 fixed sum) is on the Ross, Pickaway, Highland and Clinton ballots; all four now name the district "(Fayette, Clinton, Highland, Pickaway and Ross)".
- Shared items reuse ids and wording: Tri-County mental health (Miami, Darke, Shelby), Warren & Clinton recovery board (Warren Issue 6, Clinton), Spencerville LSD (Allen, Auglaize), Crestline EVSD and Galion's council questions (Richland, Crawford), Ashland CSD, Loudonville-Perrysville and its library (Richland, Knox, Ashland), Northwestern LSD and Wayne JVSD (Wayne, Ashland), Firelands Ambulance (Huron, Ashland), Lake Local income tax (Wood, Ottawa).
- Where the ballots and the notice differ, the ballots are used: Ashland's Dale-Roy levy is 3 years (notice 5); Shelby's Houston Joint Ambulance levy is a renewal (notice "additional"). Ashland's Firelands Ambulance renewal is on its issues list and ballots but not its notice.
- Renames: Ashland's "<NAME>-COMBINED" townships (Clearcreek is "Clear Creek Township"), Brown's "MT. ORAB" (Mount Orab), Logan's "DEGRAFF" (DeGraff), Ottawa's "PUT- IN- BAY TWP", "PUT-IN-BAY VILLAGE" and "CATAWBA TWP" (Catawba Island Township).
- Darke's County Coroner seat has no valid candidate filed and is not listed.

# Oct 30, 2026 (Madison, Fulton, Mercer, Preble, Champaign, Defiance, Guernsey, Williams, Coshocton, Perry)

- Full ballots for ten more counties (66 with local data now, plus Trumbull's original), each from the Board's 46-day FWAB notice, cross-checked against precinct sample ballots or ballot proofs where available:
  - Madison: 8 contests, 18 issues (notice, candidate list, final issues list, all 40 sample ballots; seven West Jefferson charter amendments).
  - Fulton: 9 contests, 20 issues (Issues 1–20; the Board's ballot proofs for all 37 styles).
  - Mercer: 7 contests, 6 issues (notice only; the Board is now at mercercountyoh.gov and doesn't use the state ballot lookup).
  - Preble: 10 contests, 9 issues (Issues 4–12; incl. a Lanier Township trustee race).
  - Champaign: 8 contests, 12 issues (all 51 sample ballots; Urbana's data-center charter amendment and the recall of Mayor Bill Bean with its successor race).
  - Defiance: 10 contests, 8 issues (all 46 sample ballots; Defiance City data-center charter amendment).
  - Guernsey: 8 contests, 18 issues (all 35 sample ballots; Board site boe.guernseycounty.gov).
  - Williams: 8 contests, 10 issues (Issues 4–13; all 44 sample ballots; Board site williamscountyoh.gov).
  - Coshocton: 8 contests, 5 issues (Issues 2–6; Board site coshocton.boe.ohio.gov).
  - Perry: 12 contests, 21 issues.

Data notes:
- Shared items reuse ids and wording: Four County ADAMhs (Defiance, Fulton, Williams), Central Local LSD (Defiance, Williams), Evergreen LSD and Swanton library (Lucas, Fulton), College Corner fire (Butler Issue 9, Preble Issue 6), Roseville (Muskingum, Perry), Northwestern LSD (Clark, Champaign), Miami Trace, Sterling Joint Ambulance and Tri-County Joint Fire (Pickaway, Madison), 12th District Court of Appeals (Madison, Preble as in Butler/Warren/Clermont/Clinton).
- Madison's notice leaves out the Range Township fire renewal and the Miami Trace renewal; both are on its issues list and ballots and are included. The Madison EMS levy is $167 per $100,000 on the ballot ($166.25 in the notice and issues list).
- Champaign's health levy is $6 per $100,000 on every ballot but $14 in the notice (0.4 mill works out to about $14); the ballot figure is shown, with a note.
- Fulton: probate judge Stiriz is shown without a party, as for all Common Pleas judges, though the Board's ballot proofs print "Republican" under her name (noted). Matthew Althaus (LIB, 9th District) is on the notice but on none of the ballot proofs and is not listed, as in Lucas, Wood, Erie and Ottawa.
- Williams' notice prints the ADAMhs levy as ".07 mill"; the ballots say 0.7.
- Defiance: the newer notice (10/15) puts Ney Village in the Washington Township fire levy; the 9/17 sample ballots don't. The notice is followed.
- Mercer's auditor term is "3/14/2027" as printed; Perry's Common Pleas General Division term "commencing 7-6-2028" as printed in two Board documents.
- Renames: Perry's "MONDAY CREEK TOWNSHP", Williams' "SAINT JOSEPH TWP" (St. Joseph Township), Madison's "MT. STERLING VILLAGE" (Mt. Sterling Village, the Board's spelling).

# Oct 30, 2026 (Morrow, Putnam, Henry, Hardin, Carroll, Hocking, Jackson, Van Wert, Gallia, Fayette, Pike)

- Full ballots for eleven more counties (77 with local data now, plus Trumbull's original), each from the Board's 46-day FWAB notice, cross-checked against precinct sample ballots where the county uses the state lookup:
  - Morrow: 5 contests, 18 issues (Issues 1–18; full wording from the Board's per-issue PDFs; Board site boe.morrowcountyohio.gov).
  - Putnam: 8 contests, 16 issues (all 69 sample ballots; the notice gives no precincts for local issues, so the ballots place them).
  - Henry: 6 contests, 10 issues (notice only; Henry doesn't use the state ballot lookup).
  - Hardin: 7 contests, 9 issues (incl. the Kenton charter-commission question).
  - Carroll: 8 contests, 12 issues (notice plus the Board's candidates and issues list).
  - Hocking: 7 contests, 12 issues (all 31 sample ballots; five Murray City levies).
  - Jackson: 8 contests, 3 issues (all 36 sample ballots).
  - Van Wert: 8 contests, 11 issues (all 47 sample ballots).
  - Gallia: 7 contests, 4 issues (all 38 sample ballot styles).
  - Fayette: 8 contests, 9 issues (all 42 sample ballots).
  - Pike: 7 contests, 12 issues (all 29 sample ballots).

Data notes:
- 4th District Court of Appeals (Hocking, Jackson, Gallia, Pike): every notice or ballot confirms Peter B. Abele's votes won't count due to his death; Fountain (REP) and Grace (DEM) were certified Oct 5 and are listed.
- McComb LSD is on the Hancock, Putnam and Wood ballots; all three now name it "(Hancock, Putnam and Wood)".
- Fayette's notice gives the Miami Trace renewal as "1.9 mills"; its ballot (like Pickaway's) says a fixed sum of $1,900,000 (about 2.2 mills). Fayette's Perry Township levy is a renewal and decrease on the ballot.
- Shared items reuse ids and wording: Four County ADAMhs and Pettisville LSD (Henry), Waverly CSD (Ross, Pike), Buchtel (Athens, Hocking), Delphos CSD and Spencerville LSD (Allen, Van Wert), Ada library (Hancock, Hardin), Elgin LSD (Marion, Hardin), Lexington LSD and Delaware Area Career Center (Richland/Delaware, Morrow), Sandy Valley, Edison LSD and Jefferson County JVSD (Carroll).
- Morrow's voter file, like Franklin's, has no school-district data; its school issues are placed from the notice's precinct lists.
- Renames: Putnam's "TWP." townships, Hardin's "TAYLOR CREEK TOWNSHP", Pike's "JACKSON TOWNSHP", Morrow's "N./S. BLOOMFIELD", Carroll's "WASH. TWP", Fayette's "WASHINGTON C.H. CITY" (Washington Court House City), Gallia's "GALLIPOLIS VILLAGE" (Gallipolis City, the Board's usage).
- Repeated identical levies on the ballot are kept as separate items: Van Wert's two Convoy operating renewals, Hocking's two Murray City current-expense renewals, Hardin's two Liberty Township park renewals.
- Kenton (Hardin): the notice lists the charter-commission question but no commission candidates.

# Oct 30, 2026 (Adams, Harrison, Holmes, Meigs, Monroe, Morgan, Noble, Paulding, Vinton, Wyandot — all 88 counties)

- Full ballots for the last ten counties. Every Ohio county now has its local contests and issues for the Nov 3, 2026 General Election (88 counties: 864 county/district contests and 1,633 local issues), each from its Board of Elections' own documents:
  - Adams: 7 contests, 16 issues (all 27 sample ballots; countywide EMS and children services levies; Monroe and Sprigg township zoning plans).
  - Harrison: 8 contests, 24 issues (all 34 sample ballots).
  - Holmes: 10 contests, 18 issues (notice of election and all 37 sample-ballot styles; countywide 0.25% sales tax renewal).
  - Meigs: 7 contests, 19 issues (all 30 sample ballots).
  - Monroe: 8 contests, 6 issues (scanned issues list read with OCR; all 32 sample-ballot styles).
  - Morgan: 6 contests, 11 issues (all 24 sample-ballot styles).
  - Noble: 9 contests, 8 issues (all 43 sample-ballot styles).
  - Paulding: 7 contests, 7 issues (notice with full wording).
  - Vinton: 9 contests, 11 issues (all 22 sample ballots; Richland and Swan township trustee races).
  - Wyandot: 5 contests, 12 issues (all 35 sample ballots, posted on the Board's site; Upper Sandusky data-center charter amendment).

Data notes:
- Wyandot's SoS voter file names places by precinct ("ANTRIM TS", "CAREY A", "UPPER A".."F", "NEVADA ANTRIM"); each is renamed to its township, village or city. Sycamore Village has no precinct of its own in the voter file and is counted in Sycamore Township.
- Meigs: Racine Village's additional 3-mill operating levy is on its sample ballot but not in the 46-day notice; included from the ballot.
- Morgan's notice names "Matt Donahue" for the 5th District Court of Appeals; its ballots (and every other 5th District county) have Matthew George.
- Adams' and Vinton's notices still list Peter B. Abele for the 4th District Court of Appeals; the ballots (supplemental in Adams) have Fountain vs Grace.
- Shared items reuse ids and wording: Edison LSD and Jefferson County JVSD (Harrison), Loudonville-Perrysville, its library, Triway LSD and Wayne JVSD (Holmes), Alexander LSD (Meigs, Vinton), Paulding EVSD (Putnam, Paulding), Ridgedale LSD, Wyandot East Fire, Wynford LSD and MHRS (Wyandot).
- Wynford LSD is 1.75% on Wyandot's ballots (notice 1.74%).

# Oct 30, 2026 (candidate search)

- Clicking a candidate's name opens a Google search for that person in a new tab. The search adds the office and "Ohio", and for county and local races the county name, so common names find the right person. Joint tickets (Governor / Lt. Governor) get a separate link for each name. Names look the same as before until hovered.

# Nov 1, 2026 (county picker cleanup)

- County tiles no longer say "Full ballot": every county has one now. A county without local data would still show "Statewide ballot", so the label comes back only where it means something (for example, while a future election is being loaded).
- The county dropdown's "●" marker (county has local data) only shows while some counties are still statewide-only.
- About page says all 88 counties have their full ballot, instead of listing every county name.
