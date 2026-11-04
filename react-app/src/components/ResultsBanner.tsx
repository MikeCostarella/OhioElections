import type { ResultsFile } from "../data/types";
import { fmtInt, shortTime } from "../data/load";

/** One line above the ballot on election night: what is counted so far, as of when, from where. */
export default function ResultsBanner({ r, countyName }: { r: ResultsFile; countyName: string }) {
  const p = r.precincts;
  const official = r.status === "official";
  return (
    <div className={`results-banner ${official ? "official" : "unofficial"}`} role="status" aria-live="polite">
      <span className={`status-tag ${r.status}`}>{official ? "Official" : "Unofficial"}</span>
      <span>as of <b>{shortTime(r.asOf)}</b></span>
      {r.stage && !official && <span>· counted so far: <b>{r.stage}</b></span>}
      {p && <span>· Election Day precincts reporting: <b>{p.reporting} of {p.total}</b></span>}
      {r.ballotsCast !== undefined && <span>· ballots cast: <b>{fmtInt(r.ballotsCast)}</b>{r.turnout !== undefined && <> ({r.turnout.toFixed(2)}% turnout)</>}</span>}
      <span className="src">· <a href={r.source.url} target="_blank" rel="noopener noreferrer">{r.source.label || `${countyName} County Board of Elections`} ↗</a></span>
    </div>
  );
}
