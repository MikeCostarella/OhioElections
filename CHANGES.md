# Changes

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
