# Ohio Elections

What is on the ballot in each Ohio county — candidates, the statewide issue, and the local tax levies, questions and liquor options — taken from the county Boards of Elections, with links to where the results are published.

**Live site:** https://mikecostarella.github.io/OhioElections/

It is the third piece of the fleet's election apps:

- **`<County>CountyVoters`** — who is registered and who voted, per county
- **CurrentElectionStatistics** — the early vote, rolled up statewide
- **OhioElections** (this repo) — what is on the ballot, and how it came out

One statewide app, county-scoped views: the ballot data is a few KB per county, the statewide races are shared by all 88, and adding a county is a data file rather than a new repo.

## Deep links

Routes live in the URL hash so other fleet apps can link straight to a county:

| Link | Opens |
|---|---|
| `OhioElections/#/` | County picker |
| `OhioElections/#/trumbull` | Trumbull County, latest election |
| `OhioElections/#/trumbull/2026-11-03/ballot/Hubbard%20City` | Just what Hubbard City votes on |
| `OhioElections/#/trumbull/2026-11-03/results` | Every race and issue with its standing, and where the results are published |
| `OhioElections/#/trumbull/2026-11-03/reports` | Reports for the county (ballot makeup, turnout and roll-off, county vs. statewide, party lines, issues and levies) and for all of Ohio (statewide results, counties ranked, turnout and party lean by county) — each table downloadable as CSV |
| `OhioElections/#/reports/2026-11-03/turnout` | Statewide reports, no county: `results`, `counties`, `turnout` or `lean` |
| `OhioElections/#/about` | About |

County slugs are the lower-case county name with spaces removed (`vanwert`).

## Data

```
react-app/public/data/
├── elections.json                     # elections the app knows about
├── state/2026-11-03.json              # statewide contests + state issues (every county)
├── county/
│   ├── index.json                     # which counties have local data, per election
│   └── trumbull/2026-11-03.json       # county + local contests, local issues, places, links
└── results/
    └── trumbull/2026-11-03.json       # the Board's count, by contest/issue id (election night → certified)
```

Every contest and issue cites the Board document it came from (`sources`). `places` (cities, villages, townships) drives the "Where you live" filter; `area` keeps the Board's own precinct wording. Candidates are shown alphabetically by last name because Ohio rotates ballot order by precinct.

### Election-night results

`react-app/public/data/results/<county>/2026-11-03.json` holds each county's count, keyed by the same contest and issue ids as the ballot. The app shows it beside each race and issue and, while the count is unofficial, re-reads it every two minutes. `tools/results/` builds the file from each Board's election-night report (see [`tools/results/README.md`](tools/results/README.md)); `.github/workflows/results.yml` runs that every 10 minutes on election night and redeploys when a count changes.

### Adding a county

Counties after Trumbull are generated: see [`tools/ballots/README.md`](tools/ballots/README.md). In short, summarise the county's SoS voter file into `tools/ballots/places/<county>.json`, write `tools/ballots/<county>.py` from the Board's candidate and issue lists, run `python run.py`, add the slug to `county/index.json`, and run `npm run check:data` (also run by the deploy workflow).

## Running it

PowerShell:

```powershell
cd C:\projects\OhioElections\react-app
npm ci
npm run check:data
npm run dev
```

Created by Mike Costarella, Costarella Innovations, LLC.
