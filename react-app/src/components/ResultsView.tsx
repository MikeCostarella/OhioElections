import type { Ballot, Election, ResultsFile } from "../data/types";
import type { County } from "../data/counties";
import { daysUntil, fmtInt, longDate, shortTime, SOS } from "../data/load";

interface Props {
  county: County;
  election: Election;
  local: Ballot | null;
  results: ResultsFile | null;
}

const STATUS: Record<string, string> = {
  upcoming: "Polls have not closed yet. Results will be posted by the Board of Elections and the Secretary of State.",
  unofficial: "Unofficial results: counted on election night, before provisional and late-arriving mail ballots.",
  official: "Official results, certified after the canvass.",
};

export default function ResultsView({ county, election, local, results }: Props) {
  const d = daysUntil(election.date);
  const status = results?.status ?? local?.results?.status ?? (d >= 0 ? "upcoming" : "unofficial");
  const counted = results ? Object.keys(results.contests).length + Object.keys(results.issues).length : 0;
  const p = results?.precincts;
  return (
    <div className="about">
      <p><b>{election.label}</b> · {longDate(election.date)}{d > 0 ? ` · in ${d} day${d === 1 ? "" : "s"}` : d === 0 ? " · today" : ""}</p>
      <p>{STATUS[status]}</p>
      {results && counted > 0 ? (
        <>
          <h2>{county.name} County count</h2>
          <ul>
            <li>Report time: <b>{shortTime(results.asOf)}</b>{results.stage && results.status === "unofficial" && <> · counted so far: <b>{results.stage}</b></>}</li>
            {p && <li>Election Day precincts reporting: <b>{p.reporting} of {p.total}</b>{p.partial ? ` (${p.partial} partially)` : ""}{p.absenteeReporting !== undefined && <> · absentee/early precincts in: <b>{p.absenteeReporting} of {p.total}</b></>}</li>}
            {results.ballotsCast !== undefined && <li>Ballots cast: <b>{fmtInt(results.ballotsCast)}</b>{results.registered !== undefined && <> of {fmtInt(results.registered)} registered</>}{results.turnout !== undefined && <> · turnout <b>{results.turnout.toFixed(2)}%</b></>}</li>}
            <li>Races and issues with totals: <b>{counted}</b> — shown beside each one on the <b>Ballot</b> view.</li>
            <li>Source: <a href={results.source.url} target="_blank" rel="noopener noreferrer">{results.source.label}</a></li>
          </ul>
          {results.status === "unofficial" && <p className="muted">This page re-reads the Board's count every two minutes while it is unofficial.</p>}
        </>
      ) : (
        <p className="muted">No totals are loaded for {county.name} County yet. When the Board posts its election-night report, each race and issue shows its count beside it on the Ballot view.</p>
      )}
      <h2>Where the results are published</h2>
      <ul>
        {(local?.results?.links ?? []).map((l) => (
          <li key={l.url}><a href={l.url} target="_blank" rel="noopener noreferrer">{l.label}</a> ({county.name} County)</li>
        ))}
        <li><a href={SOS.results2026} target="_blank" rel="noopener noreferrer">Ohio Secretary of State: 2026 election results and data</a> (every county)</li>
        {!local && <li><a href={SOS.boeDirectory} target="_blank" rel="noopener noreferrer">County Boards of Elections directory</a></li>}
      </ul>
    </div>
  );
}
