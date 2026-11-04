import { useEffect, useMemo, useState } from "react";
import type { Ballot, Contest, ContestResult, Election, ResultsFile } from "../data/types";
import { votersUrl, type County } from "../data/counties";
import { daysUntil, fmtInt, loadStateResults, longDate, pct, share, shortTime, SOS } from "../data/load";
import ResultsBanner from "./ResultsBanner";

interface Props {
  county: County;
  election: Election;
  state: Ballot | null;
  local: Ballot | null;
  results: ResultsFile | null;
}

const STATUS: Record<string, string> = {
  upcoming: "Polls have not closed yet. Results will be posted by the Board of Elections and the Secretary of State.",
  unofficial: "Unofficial results: counted on election night, before provisional and late-arriving mail ballots. \"Leading\" and \"passing\" describe the count so far, not a call.",
  official: "Official results, certified after the canvass.",
};

type Sort = "ballot" | "closest";

/** A contest's standing: candidates by votes, leader, runner-up, margin. */
function standing(c: Contest, r: ContestResult) {
  const votes = (name: string) => r.candidates.find((k) => k.name === name)?.votes;
  const ranked = [...c.candidates].map((k) => ({ ...k, votes: votes(k.name) })).filter((k) => k.votes !== undefined)
    .sort((a, b) => b.votes! - a.votes!);
  const lead = ranked[0];
  const next = ranked[1];
  const margin = lead && next ? lead.votes! - next.votes! : undefined;
  const marginPts = lead && next && r.total > 0 ? share(lead.votes!, r.total) - share(next.votes!, r.total) : undefined;
  return { ranked, lead, next, margin, marginPts, unopposed: c.candidates.length === 1 };
}

export default function ResultsView({ county, election, state, local, results }: Props) {
  const d = daysUntil(election.date);
  const status = results?.status ?? local?.results?.status ?? (d >= 0 ? "upcoming" : "unofficial");
  const official = status === "official";
  const [sres, setSres] = useState<ResultsFile | null>(null);
  const [sort, setSort] = useState<Sort>("ballot");

  useEffect(() => {
    let on = true;
    setSres(null);
    loadStateResults(election.id).then((r) => { if (on) setSres(r); }).catch(() => { /* statewide totals are optional */ });
    return () => { on = false; };
  }, [election.id]);

  const stateIds = useMemo(() => new Set(state?.contests.map((c) => c.id) ?? []), [state]);
  const contests = useMemo(() => [...(state?.contests ?? []), ...(local?.contests ?? [])], [state, local]);
  const issues = useMemo(() => [...(state?.issues ?? []), ...(local?.issues ?? [])], [state, local]);

  const rows = useMemo(() => {
    if (!results) return [];
    const out = contests.flatMap((c) => { const r = results.contests[c.id]; return r ? [{ c, r, s: standing(c, r) }] : []; });
    if (sort === "closest") out.sort((a, b) => (a.s.marginPts ?? 999) - (b.s.marginPts ?? 999));
    return out;
  }, [contests, results, sort]);
  const irows = useMemo(() => {
    if (!results) return [];
    const out = issues.flatMap((q) => { const r = results.issues[q.id]; return r ? [{ q, r }] : []; });
    if (sort === "closest") out.sort((a, b) => Math.abs(share(a.r.yes, a.r.total) - 50) - Math.abs(share(b.r.yes, b.r.total) - 50));
    return out;
  }, [issues, results, sort]);

  const counted = rows.length + irows.length;
  const p = results?.precincts;
  const links = (
    <>
      <h2>Where the results are published</h2>
      <ul>
        {(local?.results?.links ?? []).map((l) => (
          <li key={l.url}><a href={l.url} target="_blank" rel="noopener noreferrer">{l.label}</a> ({county.name} County)</li>
        ))}
        <li><a href={SOS.results2026} target="_blank" rel="noopener noreferrer">Ohio Secretary of State: 2026 election results and data</a> (every county)</li>
        {!local && <li><a href={SOS.boeDirectory} target="_blank" rel="noopener noreferrer">County Boards of Elections directory</a></li>}
      </ul>
    </>
  );

  if (!results || counted === 0) {
    return (
      <div className="about">
        <p><b>{election.label}</b> · {longDate(election.date)}{d > 0 ? ` · in ${d} day${d === 1 ? "" : "s"}` : d === 0 ? " · today" : ""}</p>
        <p>{STATUS[status]}</p>
        <p className="muted">No totals are loaded for {county.name} County yet. When they are, every race and issue is listed here with its standing, and shown beside each one on the Ballot view.</p>
        {links}
      </div>
    );
  }

  // Groups in ballot order, each with its rows (only used in ballot order; "closest" is one flat list).
  const groups: [string, typeof rows][] = [];
  for (const row of rows) {
    const g = sort === "closest" ? "All races, closest first" : row.c.group;
    const last = groups[groups.length - 1];
    if (last && last[0] === g) last[1].push(row); else groups.push([g, [row]]);
  }
  const stateTurnout = sres?.turnout;

  return (
    <div className="results">
      <ResultsBanner r={results} countyName={county.name} />
      <p className="note" style={{ marginTop: 0 }}>{STATUS[status]}</p>

      <section className="stat-row">
        <div className="stat"><div className="stat-label">Ballots cast</div><div className="stat-value">{results.ballotsCast !== undefined ? fmtInt(results.ballotsCast) : "—"}</div>{results.registered !== undefined && <div className="stat-sub">of {fmtInt(results.registered)} registered</div>}</div>
        <div className="stat"><div className="stat-label">Turnout</div><div className="stat-value">{results.turnout !== undefined ? `${results.turnout.toFixed(1)}%` : "—"}</div>{stateTurnout !== undefined && <div className="stat-sub">statewide {stateTurnout.toFixed(1)}%</div>}</div>
        <div className="stat"><div className="stat-label">Election Day precincts</div><div className="stat-value">{p ? `${p.reporting} of ${p.total}` : "—"}</div>{p && <div className="stat-sub">{p.reporting === p.total ? "all reporting" : "reporting"}</div>}</div>
        <div className="stat"><div className="stat-label">Report</div><div className="stat-value">{shortTime(results.asOf)}</div><div className="stat-sub"><a href={results.source.url} target="_blank" rel="noopener noreferrer">{results.source.label.split(":")[0]} ↗</a></div></div>
        <div className="stat"><div className="stat-label">Who voted</div><div className="stat-value small"><a href={votersUrl(county)} target="_blank" rel="noopener noreferrer">{county.name} County Voters ↗</a></div><div className="stat-sub">registration and voter history</div></div>
      </section>

      <div className="filters">
        <div className="seg" role="group" aria-label="Order">
          <button type="button" className={sort === "ballot" ? "active" : ""} aria-pressed={sort === "ballot"} onClick={() => setSort("ballot")}>Ballot order</button>
          <button type="button" className={sort === "closest" ? "active" : ""} aria-pressed={sort === "closest"} onClick={() => setSort("closest")}>Closest first</button>
        </div>
        <span className="muted" style={{ fontSize: 12 }}>{rows.length} races · {irows.length} issues{sres ? " · statewide column from the Secretary of State" : ""}</span>
      </div>

      {rows.length > 0 && (
        <section>
          <h3 className="section-title">Races <span className="count">{rows.length}</span></h3>
          <div className="tbl-wrap">
            <table className="rtable">
              <thead>
                <tr><th>Race</th><th>{official ? "Winner" : "Leading"}</th><th className="num">Votes</th><th className="num">Share</th><th className="num">Margin</th><th>Runner-up</th><th>Statewide</th></tr>
              </thead>
              {groups.map(([g, rs]) => (
                <tbody key={g}>
                  <tr className="grp"><td colSpan={7}>{g}</td></tr>
                  {rs.map(({ c, r, s }) => {
                    const sr = sres?.contests[c.id];
                    const sLead = sr ? [...sr.candidates].sort((a, b) => b.votes - a.votes)[0] : undefined;
                    const differs = sLead && s.lead && sLead.name !== s.lead.name;
                    return (
                      <tr key={c.id}>
                        <td className="race"><b>{c.office}</b>{c.detail && <div className="sub">{c.detail}</div>}</td>
                        <td className="who">{s.lead ? <><b>{s.lead.name}</b>{s.lead.party && <span className="party-tag">{s.lead.party}</span>}{s.unopposed && <div className="sub">unopposed</div>}</> : <span className="muted">—</span>}</td>
                        <td className="num">{s.lead ? fmtInt(s.lead.votes!) : ""}</td>
                        <td className="num">{s.lead ? pct(s.lead.votes!, r.total) : ""}</td>
                        <td className={`num ${s.marginPts !== undefined && s.marginPts < 2 ? "close" : ""}`}>{s.margin !== undefined ? <>{fmtInt(s.margin)}<div className="sub">{s.marginPts!.toFixed(1)} pts</div></> : ""}</td>
                        <td className="who">{s.next ? <>{s.next.name}{s.next.party && <span className="party-tag">{s.next.party}</span>}<div className="sub">{fmtInt(s.next.votes!)} · {pct(s.next.votes!, r.total)}</div></> : ""}</td>
                        <td className={`who ${differs ? "differs" : ""}`}>{sLead && stateIds.has(c.id) ? <>{sLead.name.split(" / ")[0]} <span className="sub-inline">{pct(sLead.votes, sr!.total)}</span>{differs && <div className="sub">county differs</div>}</> : <span className="muted">{stateIds.has(c.id) ? "" : "district race"}</span>}</td>
                      </tr>
                    );
                  })}
                </tbody>
              ))}
            </table>
          </div>
        </section>
      )}

      {irows.length > 0 && (
        <section>
          <h3 className="section-title">Issues <span className="count">{irows.length}</span></h3>
          <div className="tbl-wrap">
            <table className="rtable">
              <thead>
                <tr><th>Issue</th><th>Jurisdiction</th><th className="num">Yes</th><th className="num">No</th><th className="num">Margin</th><th>Standing</th></tr>
              </thead>
              <tbody>
                {irows.map(({ q, r }) => {
                  const y = share(r.yes, r.total), n = share(r.no, r.total);
                  const tied = r.yes === r.no;
                  const passing = r.yes > r.no;
                  const label = r.total === 0 ? "no votes" : tied ? "tied" : official ? (passing ? "Passed" : "Failed") : (passing ? "Passing" : "Failing");
                  const sr = sres?.issues[q.id];
                  return (
                    <tr key={q.id}>
                      <td className="race">{q.number && <span className="issue-num">{q.number}</span>} <b>{q.title}</b>{q.levy?.mills && <div className="sub">{q.levy.mills}{q.levy.term ? ` · ${q.levy.term}` : ""}</div>}</td>
                      <td className="who">{q.jurisdiction}</td>
                      <td className="num">{fmtInt(r.yes)}<div className="sub">{pct(r.yes, r.total)}</div></td>
                      <td className="num">{fmtInt(r.no)}<div className="sub">{pct(r.no, r.total)}</div></td>
                      <td className={`num ${Math.abs(y - n) < 4 && r.total > 0 ? "close" : ""}`}>{r.total > 0 ? `${Math.abs(y - n).toFixed(1)} pts` : ""}</td>
                      <td><span className={`standing ${r.total === 0 || tied ? "" : passing ? "yes" : "no"}`}>{label}</span>{sr && <div className="sub">statewide yes {pct(sr.yes, sr.total)}</div>}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </section>
      )}

      <div className="about">{links}</div>
    </div>
  );
}
