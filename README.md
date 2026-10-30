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
| `OhioElections/#/trumbull/2026-11-03/results` | Where the results are published |
| `OhioElections/#/about` | About |

County slugs are the lower-case county name with spaces removed (`vanwert`).

## Data

```
react-app/public/data/
├── elections.json                     # elections the app knows about
├── state/2026-11-03.json              # statewide contests + state issues (every county)
└── county/
    ├── index.json                     # which counties have local data, per election
    └── trumbull/2026-11-03.json       # county + local contests, local issues, places, links
```

Every contest and issue cites the Board document it came from (`sources`). `places` (cities, villages, townships) drives the "Where you live" filter; `area` keeps the Board's own precinct wording. Candidates are shown alphabetically by last name because Ohio rotates ballot order by precinct.

### Adding a county

1. Get the Board of Elections' candidate list, issues list and 46-day notice (Form 120) for the election.
2. Copy `county/trumbull/2026-11-03.json` to `county/<slug>/2026-11-03.json` and replace its contests, issues, places, sources and links.
3. Add the slug to `county/index.json`.
4. Run `npm run check:data` (also runs in the deploy workflow).

## Running it

PowerShell:

```powershell
cd C:\projects\OhioElections\react-app
npm ci
npm run check:data
npm run dev
```

Created by Mike Costarella, Costarella Innovations, LLC.
