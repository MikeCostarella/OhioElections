import type { Ballot, Election } from "../data/types";
import type { County } from "../data/counties";
import { daysUntil, longDate, SOS } from "../data/load";

interface Props {
  county: County;
  election: Election;
  local: Ballot | null;
}

const STATUS: Record<string, string> = {
  upcoming: "Polls have not closed yet. Results will be posted by the Board of Elections and the Secretary of State.",
  unofficial: "Unofficial results: counted on election night, before provisional and late-arriving mail ballots.",
  official: "Official results, certified after the canvass.",
};

export default function ResultsView({ county, election, local }: Props) {
  const d = daysUntil(election.date);
  const status = local?.results?.status ?? (d >= 0 ? "upcoming" : "unofficial");
  return (
    <div className="about">
      <p><b>{election.label}</b> · {longDate(election.date)}{d > 0 ? ` · in ${d} day${d === 1 ? "" : "s"}` : d === 0 ? " · today" : ""}</p>
      <p>{STATUS[status]}</p>
      <h2>Where the results are published</h2>
      <ul>
        {(local?.results?.links ?? []).map((l) => (
          <li key={l.url}><a href={l.url} target="_blank" rel="noopener noreferrer">{l.label}</a> ({county.name} County)</li>
        ))}
        <li><a href={SOS.results2026} target="_blank" rel="noopener noreferrer">Ohio Secretary of State: 2026 election results and data</a> (every county)</li>
        {!local && <li><a href={SOS.boeDirectory} target="_blank" rel="noopener noreferrer">County Boards of Elections directory</a></li>}
      </ul>
      <p className="muted">Results will be loaded into this app county by county after the canvass, so each race and issue shows its outcome beside it.</p>
    </div>
  );
}
