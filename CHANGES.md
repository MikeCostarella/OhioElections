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
