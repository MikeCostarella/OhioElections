import { useEffect, useMemo, useState } from "react";
import type { Ballot, Contest, Election, Issue, IssueResult, ResultsFile } from "../data/types";
import { COUNTIES, type County } from "../data/counties";
import { fmtInt, loadStateResults, longDate, pct, share } from "../data/load";

interface Props {
  county: County;
  election: Election;
  state: Ballot | null;
  local: Ballot | null;
  results: ResultsFile | null;
}

type ReportId = "ballot" | "turnout" | "statewide" | "party" | "issues";
const REPORTS: { id: ReportId; label: string; needsResults: boolean }[] = [
  { id: "ballot", label: "Ballot makeup", needsResults: false },
  { id: "turnout", label: "Turnout & roll-off", needsResults: true },
  { id: "statewide", label: "County vs. statewide", needsResults: true },
  { id: "party", label: "Party lines", needsResults: true },
  { id: "issues", label: "Issues & levies", needsResults: true },
];

type Cell = string | number;
const pts = (n: number) => `${n > 0 ? "+" : ""}${n.toFixed(1)}`;
const avg = (xs: number[]) => (xs.length ? xs.reduce((a, b) => a + b, 0) / xs.length : 0);
const MAJOR = new Set(["DEM", "REP"]);
/** "Renewal", "Additional"... as the Board filed it; the Board's "Not stated" and a missing type read the same. */
const levyType = (q: Issue) => { const t = q.levy?.type?.trim(); return t && t.toLowerCase() !== "not stated" ? t : "type not stated"; };
/** A contest or issue the whole county votes on; one with a places list is only part of the county. */
const countywide = (x: { places?: string[] }) => x.places === undefined;

/** Quote and save a table as CSV, named after the county, election and report. */
function downloadCsv(filename: string, header: string[], rows: Cell[][]) {
  const cell = (x: Cell) => { const t = String(x); return /[",\n]/.test(t) ? `"${t.replace(/"/g, '""')}"` : t; };
  const csv = [header, ...rows].map((r) => r.map(cell).join(",")).join("\n");
  const url = URL.createObjectURL(new Blob([csv], { type: "text/csv;charset=utf-8;" }));
  const a = document.createElement("a");
  a.href = url; a.download = filename;
  document.body.appendChild(a); a.click(); document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

function Tile({ label, value, sub }: { label: string; value: string; sub?: string }) {
  return <div className="stat"><div className="stat-label">{label}</div><div className="stat-value">{value}</div>{sub && <div className="stat-sub">{sub}</div>}</div>;
}

/** A thin bar for a share, 0–100. */
function Bar({ v, lead }: { v: number; lead?: boolean }) {
  return <span className={`rbar${lead ? " lead" : ""}`} aria-hidden="true"><span style={{ width: `${Math.max(0, Math.min(100, v))}%` }} /></span>;
}

function ExportBtn({ onClick }: { onClick: () => void }) {
  return <button type="button" className="csv-btn" onClick={onClick} title="Download this table as CSV">⬇ CSV</button>;
}

/**
 * The Reports view: the same ballot and totals as the other two tabs, summed up the ways
 * people ask about them — what is on the ballot, who turned out and where the vote fell off,
 * how the county compares with the state, how the parties did, and what passed.
 * Every table downloads as CSV. Nothing here calls a race.
 */
export default function ReportsView({ county, election, state, local, results }: Props) {
  const [report, setReport] = useState<ReportId>(results ? "turnout" : "ballot");
  const [sres, setSres] = useState<ResultsFile | null>(null);

  useEffect(() => {
    let on = true;
    setSres(null);
    loadStateResults(election.id).then((r) => { if (on) setSres(r); }).catch(() => { /* optional */ });
    return () => { on = false; };
  }, [election.id]);

  const stateIds = useMemo(() => new Set(state?.contests.map((c) => c.id) ?? []), [state]);
  const contests = useMemo(() => [...(state?.contests ?? []), ...(local?.contests ?? [])], [state, local]);
  const issues = useMemo(() => [...(state?.issues ?? []), ...(local?.issues ?? [])], [state, local]);
  const official = results?.status === "official";
  const file = (name: string) => `${county.slug}-${election.id}-${name}.csv`;

  const head = (
    <div className="filters">
      <div className="seg" role="tablist" aria-label="Report">
        {REPORTS.map((r) => (
          <button key={r.id} type="button" role="tab" aria-selected={report === r.id} className={report === r.id ? "active" : ""} onClick={() => setReport(r.id)}>{r.label}</button>
        ))}
      </div>
      <span className="muted" style={{ fontSize: 12 }}>{county.name} County · {election.label} · {longDate(election.date)}{results ? ` · ${official ? "official" : "unofficial"} totals` : " · no totals yet"}</span>
    </div>
  );

  const current = REPORTS.find((r) => r.id === report)!;
  if (current.needsResults && !results) {
    return (
      <div className="results reports">
        {head}
        <p className="note" style={{ marginTop: 0 }}>No totals are loaded for {county.name} County yet, so this report is empty. The <b>Ballot makeup</b> report works before the count; the others fill in once the Board's totals are in.</p>
      </div>
    );
  }

  return (
    <div className="results reports">
      {head}
      {!official && results && current.needsResults && <p className="note" style={{ marginTop: 0 }}>Unofficial totals, counted on election night. "Passing", "leading" and every share below describe the count so far, not a call.</p>}
      {report === "ballot" && <BallotReport county={county} contests={contests} issues={issues} places={local?.places ?? []} stateIds={stateIds} file={file} />}
      {report === "turnout" && results && <TurnoutReport county={county} contests={contests} issues={issues} results={results} sres={sres} file={file} />}
      {report === "statewide" && results && <StatewideReport county={county} contests={contests} issues={issues} results={results} sres={sres} stateIds={stateIds} file={file} />}
      {report === "party" && results && <PartyReport county={county} contests={contests} results={results} sres={sres} stateIds={stateIds} file={file} />}
      {report === "issues" && results && <IssuesReport issues={issues} results={results} official={official} file={file} />}
    </div>
  );
}

/* ---------------- Ballot makeup: what is on the ballot, before any count ---------------- */

function BallotReport({ county, contests, issues, places, stateIds, file }: { county: County; contests: Contest[]; issues: Issue[]; places: string[]; stateIds: Set<string>; file: (n: string) => string }) {
  const candidates = contests.reduce((n, c) => n + c.candidates.length, 0);
  const unopposed = contests.filter((c) => c.candidates.length === 1);
  const parties = new Map<string, number>();
  for (const c of contests) for (const k of c.candidates) parties.set(k.party ?? "Nonpartisan", (parties.get(k.party ?? "Nonpartisan") ?? 0) + 1);
  const groups: { group: string; contests: number; candidates: number; unopposed: number; scope: string }[] = [];
  for (const c of contests) {
    let g = groups.find((x) => x.group === c.group);
    if (!g) { g = { group: c.group, contests: 0, candidates: 0, unopposed: 0, scope: stateIds.has(c.id) ? "Statewide" : "County / district" }; groups.push(g); }
    g.contests++; g.candidates += c.candidates.length; if (c.candidates.length === 1) g.unopposed++;
  }
  const kinds = new Map<string, number>();
  for (const q of issues) { const k = q.kind === "levy" ? `Tax levy · ${levyType(q)}` : q.kind === "state" ? "State issue" : q.kind === "question" ? "Local question" : "Liquor option"; kinds.set(k, (kinds.get(k) ?? 0) + 1); }
  const juris = new Map<string, number>();
  for (const q of issues) juris.set(q.jurisdiction, (juris.get(q.jurisdiction) ?? 0) + 1);
  const jrows = [...juris.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));

  return (
    <>
      <section className="stat-row">
        <Tile label="Contests" value={fmtInt(contests.length)} sub={`${stateIds.size} statewide · ${contests.length - stateIds.size} county / district`} />
        <Tile label="Candidates" value={fmtInt(candidates)} sub={`${unopposed.length} unopposed race${unopposed.length === 1 ? "" : "s"}`} />
        <Tile label="Issues" value={fmtInt(issues.length)} sub={`${issues.filter((q) => q.kind === "levy").length} tax levies`} />
        <Tile label="Places" value={places.length ? fmtInt(places.length) : "—"} sub={places.length ? "cities, villages and townships" : "no local ballot loaded"} />
      </section>

      <section>
        <h3 className="section-title">Contests by office group <span className="count">{groups.length}</span><ExportBtn onClick={() => downloadCsv(file("ballot-groups"), ["Group", "Scope", "Contests", "Candidates", "Unopposed"], groups.map((g) => [g.group, g.scope, g.contests, g.candidates, g.unopposed]))} /></h3>
        <div className="tbl-wrap"><table className="rtable compact">
          <thead><tr><th>Group</th><th>Scope</th><th className="num">Contests</th><th className="num">Candidates</th><th className="num">Unopposed</th></tr></thead>
          <tbody>{groups.map((g) => <tr key={g.group}><td className="race"><b>{g.group}</b></td><td>{g.scope}</td><td className="num">{g.contests}</td><td className="num">{g.candidates}</td><td className="num">{g.unopposed || ""}</td></tr>)}</tbody>
        </table></div>
      </section>

      <div className="two-col">
        <section>
          <h3 className="section-title">Candidates by party<ExportBtn onClick={() => downloadCsv(file("ballot-parties"), ["Party", "Candidates"], [...parties.entries()].map(([p, n]) => [p, n]))} /></h3>
          <div className="tbl-wrap"><table className="rtable compact narrow">
            <thead><tr><th>Party</th><th className="num">Candidates</th><th className="num">Share</th></tr></thead>
            <tbody>{[...parties.entries()].sort((a, b) => b[1] - a[1]).map(([p, n]) => <tr key={p}><td className="race"><b>{p}</b></td><td className="num">{n}</td><td className="num">{pct(n, candidates)}</td></tr>)}</tbody>
          </table></div>
        </section>
        <section>
          <h3 className="section-title">Issues by kind<ExportBtn onClick={() => downloadCsv(file("ballot-issue-kinds"), ["Kind", "Issues"], [...kinds.entries()].map(([k, n]) => [k, n]))} /></h3>
          <div className="tbl-wrap"><table className="rtable compact narrow">
            <thead><tr><th>Kind</th><th className="num">Issues</th></tr></thead>
            <tbody>{[...kinds.entries()].sort((a, b) => b[1] - a[1]).map(([k, n]) => <tr key={k}><td className="race"><b>{k}</b></td><td className="num">{n}</td></tr>)}</tbody>
          </table></div>
        </section>
      </div>

      {unopposed.length > 0 && (
        <section>
          <h3 className="section-title">Unopposed races <span className="count">{unopposed.length}</span><ExportBtn onClick={() => downloadCsv(file("ballot-unopposed"), ["Race", "Detail", "Candidate", "Party"], unopposed.map((c) => [c.office, c.detail ?? "", c.candidates[0].name, c.candidates[0].party ?? ""]))} /></h3>
          <div className="tbl-wrap"><table className="rtable compact">
            <thead><tr><th>Race</th><th>Candidate</th></tr></thead>
            <tbody>{unopposed.map((c) => <tr key={c.id}><td className="race"><b>{c.office}</b>{c.detail && <div className="sub">{c.detail}</div>}</td><td className="who">{c.candidates[0].name}{c.candidates[0].party && <span className="party-tag">{c.candidates[0].party}</span>}</td></tr>)}</tbody>
          </table></div>
        </section>
      )}

      {jrows.length > 0 && (
        <section>
          <h3 className="section-title">Issues by jurisdiction <span className="count">{jrows.length}</span><ExportBtn onClick={() => downloadCsv(file("ballot-issue-jurisdictions"), ["Jurisdiction", "Issues"], jrows)} /></h3>
          <div className="tbl-wrap"><table className="rtable compact">
            <thead><tr><th>Jurisdiction</th><th className="num">Issues</th><th>What</th></tr></thead>
            <tbody>{jrows.map(([j, n]) => <tr key={j}><td className="race"><b>{j}</b></td><td className="num">{n}</td><td className="sub">{issues.filter((q) => q.jurisdiction === j).map((q) => q.levy?.mills ? `${q.levy.type ?? "levy"} ${q.levy.mills}` : q.kind).join(" · ")}</td></tr>)}</tbody>
          </table></div>
        </section>
      )}
      <p className="note">{county.name} County's ballot as the Board of Elections filed it; statewide offices and State Issue 3 are on every county's ballot.</p>
    </>
  );
}

/* ---------------- Turnout & roll-off: who voted, and how far down the ballot ---------------- */

function TurnoutReport({ county, contests, issues, results, sres, file }: { county: County; contests: Contest[]; issues: Issue[]; results: ResultsFile; sres: ResultsFile | null; file: (n: string) => string }) {
  const crows = contests.flatMap((c) => { const r = results.contests[c.id]; return r ? [{ id: c.id, label: c.office + (c.detail ? ` · ${c.detail}` : ""), group: c.group, total: r.total, writeIn: r.writeIn ?? 0, whole: countywide(c) }] : []; });
  const irows = issues.flatMap((q) => { const r = results.issues[q.id]; return r ? [{ id: q.id, label: q.title, group: q.jurisdiction, total: r.total, writeIn: 0, whole: countywide(q) }] : []; });
  const max = Math.max(0, ...crows.map((r) => r.total), ...irows.map((r) => r.total));
  // The Board's ballots-cast figure is the denominator; failing that, the busiest contest.
  const ballots = results.ballotsCast ?? max;
  const fromBoard = results.ballotsCast !== undefined;
  const rolloff = (t: number) => (ballots > 0 ? 100 - share(t, ballots) : 0);
  const p = results.precincts;
  const whole = crows.filter((r) => r.whole);
  const topRace = whole.length ? whole.reduce((a, b) => (b.total > a.total ? b : a)) : null;
  const lowRace = whole.length ? whole.reduce((a, b) => (b.total < a.total ? b : a)) : null;
  const all = [...crows, ...irows];
  const partial = all.filter((r) => !r.whole).length;
  const rows = (xs: typeof all) => xs.map((r) => [r.label, r.group, r.whole ? "Countywide" : "Part of county", r.total, pct(r.total, ballots), r.whole ? rolloff(r.total).toFixed(1) : ""] as Cell[]);

  const table = (xs: typeof all, title: string, name: string) => xs.length > 0 && (
    <section>
      <h3 className="section-title">{title} <span className="count">{xs.length}</span><ExportBtn onClick={() => downloadCsv(file(name), ["Contest", "Group", "Scope", "Votes cast", "Of ballots", "Roll-off pts"], rows(xs))} /></h3>
      <div className="tbl-wrap"><table className="rtable compact">
        <thead><tr><th>Contest</th><th className="num">Votes cast</th><th className="bar">Of ballots cast</th><th className="num">Roll-off</th></tr></thead>
        <tbody>{xs.map((r) => {
          const ro = rolloff(r.total);
          return (
            <tr key={r.id}>
              <td className="race"><b>{r.label}</b><div className="sub">{r.group}{r.writeIn ? ` · ${fmtInt(r.writeIn)} write-in` : ""}</div></td>
              <td className="num">{fmtInt(r.total)}</td>
              <td className="bar"><Bar v={share(r.total, ballots)} /><span className="sub-inline">{pct(r.total, ballots)}</span></td>
              <td className={`num ${r.whole && ro >= 10 ? "close" : ""}`}>{!r.whole ? <span className="sub-inline">part of county</span> : ro > 0 ? `−${ro.toFixed(1)} pts` : "—"}</td>
            </tr>
          );
        })}</tbody>
      </table></div>
    </section>
  );

  return (
    <>
      <section className="stat-row">
        <Tile label="Registered" value={results.registered !== undefined ? fmtInt(results.registered) : "—"} sub={`${county.name} County`} />
        <Tile label="Ballots cast" value={fmtInt(ballots)} sub={fromBoard ? "as the Board reports" : "busiest contest (no Board figure)"} />
        <Tile label="Turnout" value={results.turnout !== undefined ? `${results.turnout.toFixed(1)}%` : "—"} sub={sres?.turnout !== undefined ? `statewide ${sres.turnout.toFixed(1)}% · ${results.turnout !== undefined ? `${pts(results.turnout - sres.turnout)} pts` : ""}` : undefined} />
        <Tile label="Precincts" value={p ? `${p.reporting} of ${p.total}` : "—"} sub={p ? (p.reporting === p.total ? "all reporting" : "Election Day precincts reporting") : undefined} />
        <Tile label="Top of ticket" value={topRace ? pct(topRace.total, ballots) : "—"} sub={topRace ? `voted in ${topRace.label}` : undefined} />
        <Tile label="Furthest roll-off" value={lowRace ? `−${rolloff(lowRace.total).toFixed(1)} pts` : "—"} sub={lowRace ? `${lowRace.label} (countywide races only)` : undefined} />
      </section>
      <p className="note" style={{ marginTop: 0 }}>Roll-off is the share of ballots that left a contest blank (or voted for more or fewer than allowed): ballots cast minus the Board's total votes in the contest, in points; orange at 10 or more. It is only figured for contests and issues the whole county votes on{partial ? ` — the ${partial} district and local ones that only part of the county sees show their votes but no roll-off` : ""}.</p>
      {table(crows, "Races", "rolloff-races")}
      {table(irows, "Issues", "rolloff-issues")}
    </>
  );
}

/* ---------------- County vs. statewide: every statewide race and issue, this county against Ohio and the other 87 ---------------- */

function StatewideReport({ county, contests, issues, results, sres, stateIds, file }: { county: County; contests: Contest[]; issues: Issue[]; results: ResultsFile; sres: ResultsFile | null; stateIds: Set<string>; file: (n: string) => string }) {
  const countyName = (slug: string) => COUNTIES.find((c) => c.slug === slug)?.name ?? slug;

  type Row = { contest: Contest; name: string; party?: string; cVotes: number; cShare: number; sShare?: number; rank?: number; of?: number; top?: { county: string; share: number }; lead: boolean };
  const rows: Row[] = [];
  for (const c of contests) {
    if (!stateIds.has(c.id)) continue;
    const r = results.contests[c.id];
    if (!r) continue;
    const sr = sres?.contests[c.id];
    const leadName = [...r.candidates].sort((a, b) => b.votes - a.votes)[0]?.name;
    const byVotes = [...c.candidates].sort((a, b) => (r.candidates.find((x) => x.name === b.name)?.votes ?? -1) - (r.candidates.find((x) => x.name === a.name)?.votes ?? -1));
    for (const k of byVotes) {
      const cv = r.candidates.find((x) => x.name === k.name)?.votes;
      if (cv === undefined) continue;
      const row: Row = { contest: c, name: k.name, party: k.party, cVotes: cv, cShare: share(cv, r.total), lead: k.name === leadName };
      if (sr) {
        const sv = sr.candidates.find((x) => x.name === k.name)?.votes;
        if (sv !== undefined) row.sShare = share(sv, sr.total);
        if (sr.counties) {
          const ranked = Object.entries(sr.counties).map(([slug, x]) => ({ slug, s: share(x.candidates.find((y) => y.name === k.name)?.votes ?? 0, x.total) })).sort((a, b) => b.s - a.s);
          const i = ranked.findIndex((x) => x.slug === county.slug);
          if (i >= 0) { row.rank = i + 1; row.of = ranked.length; }
          if (ranked[0]) row.top = { county: countyName(ranked[0].slug), share: ranked[0].s };
        }
      }
      rows.push(row);
    }
  }

  type IRow = { issue: Issue; yes: number; no: number; cShare: number; sShare?: number; rank?: number; of?: number; top?: { county: string; share: number } };
  const irows: IRow[] = [];
  for (const q of issues) {
    if (q.kind !== "state") continue;
    const r = results.issues[q.id];
    if (!r) continue;
    const row: IRow = { issue: q, yes: r.yes, no: r.no, cShare: share(r.yes, r.total) };
    const sr = sres?.issues[q.id];
    if (sr) {
      row.sShare = share(sr.yes, sr.total);
      if (sr.counties) {
        const ranked = Object.entries(sr.counties).map(([slug, x]) => ({ slug, s: share(x.yes, x.total) })).sort((a, b) => b.s - a.s);
        const i = ranked.findIndex((x) => x.slug === county.slug);
        if (i >= 0) { row.rank = i + 1; row.of = ranked.length; }
        if (ranked[0]) row.top = { county: countyName(ranked[0].slug), share: ranked[0].s };
      }
    }
    irows.push(row);
  }

  // Groups in ballot order.
  const groups: [string, Row[]][] = [];
  for (const row of rows) { const g = row.contest.group; const last = groups[groups.length - 1]; if (last && last[0] === g) last[1].push(row); else groups.push([g, [row]]); }
  const diffs = rows.filter((r) => r.sShare !== undefined && r.party && MAJOR.has(r.party)).map((r) => ({ r, d: r.cShare - r.sShare! }));
  const most = diffs.length ? diffs.reduce((a, b) => (Math.abs(b.d) > Math.abs(a.d) ? b : a)) : null;
  const differs = groups.flatMap(([, rs]) => rs).filter((r) => r.lead && r.sShare !== undefined).filter((r) => {
    const sr = sres?.contests[r.contest.id]; if (!sr) return false;
    const sLead = [...sr.candidates].sort((a, b) => b.votes - a.votes)[0]; return sLead && sLead.name !== r.name;
  });

  return (
    <>
      <section className="stat-row">
        <Tile label="Statewide races counted" value={fmtInt(groups.reduce((n, [, rs]) => n + new Set(rs.map((r) => r.contest.id)).size, 0))} sub={sres ? "statewide file from the Secretary of State" : "statewide file not published yet"} />
        <Tile label="County differs" value={fmtInt(differs.length)} sub={differs.length ? differs.map((r) => r.contest.office).join(", ") : "county leader is the statewide leader in every race"} />
        <Tile label="Biggest gap" value={most ? `${pts(most.d)} pts` : "—"} sub={most ? `${most.r.name.split(" / ")[0]} (${most.r.contest.office}) vs. statewide` : undefined} />
        <Tile label="Turnout" value={results.turnout !== undefined ? `${results.turnout.toFixed(1)}%` : "—"} sub={sres?.turnout !== undefined ? `statewide ${sres.turnout.toFixed(1)}%` : undefined} />
      </section>
      {rows.length > 0 && (
        <section>
          <h3 className="section-title">Statewide races <span className="count">{rows.length} candidates</span><ExportBtn onClick={() => downloadCsv(file("county-vs-statewide"), ["Race", "Candidate", "Party", "County votes", "County share", "Statewide share", "Diff pts", "Rank of 88", "Top county", "Top county share"], rows.map((r) => [r.contest.office, r.name, r.party ?? "", r.cVotes, r.cShare.toFixed(1), r.sShare?.toFixed(1) ?? "", r.sShare !== undefined ? (r.cShare - r.sShare).toFixed(1) : "", r.rank ?? "", r.top?.county ?? "", r.top?.share.toFixed(1) ?? ""]))} /></h3>
          <div className="tbl-wrap"><table className="rtable compact">
            <thead><tr><th>Candidate</th><th className="num">County votes</th><th className="bar">County share</th><th className="num">Statewide</th><th className="num">Diff</th><th className="num">Rank</th><th>Strongest county</th></tr></thead>
            {groups.map(([g, rs]) => (
              <tbody key={g}>
                <tr className="grp"><td colSpan={7}>{g}</td></tr>
                {rs.map((r) => {
                  const d = r.sShare !== undefined ? r.cShare - r.sShare : undefined;
                  return (
                    <tr key={r.contest.id + r.name}>
                      <td className="who"><b>{r.name}</b>{r.party && <span className="party-tag">{r.party}</span>}<div className="sub">{r.contest.office}{r.lead ? " · leading here" : ""}</div></td>
                      <td className="num">{fmtInt(r.cVotes)}</td>
                      <td className="bar"><Bar v={r.cShare} lead={r.lead} /><span className="sub-inline">{r.cShare.toFixed(1)}%</span></td>
                      <td className="num">{r.sShare !== undefined ? `${r.sShare.toFixed(1)}%` : "—"}</td>
                      <td className={`num ${d !== undefined && Math.abs(d) >= 5 ? "close" : ""}`}>{d !== undefined ? `${pts(d)} pts` : ""}</td>
                      <td className="num">{r.rank ? <>{r.rank}<span className="sub-inline"> of {r.of}</span></> : ""}</td>
                      <td className="sub">{r.top ? `${r.top.county} · ${r.top.share.toFixed(1)}%` : ""}</td>
                    </tr>
                  );
                })}
              </tbody>
            ))}
          </table></div>
        </section>
      )}
      {irows.length > 0 && (
        <section>
          <h3 className="section-title">State issues <span className="count">{irows.length}</span><ExportBtn onClick={() => downloadCsv(file("state-issues-vs-statewide"), ["Issue", "County yes", "County no", "County yes share", "Statewide yes share", "Diff pts", "Rank of 88", "Top county", "Top county yes share"], irows.map((r) => [r.issue.title, r.yes, r.no, r.cShare.toFixed(1), r.sShare?.toFixed(1) ?? "", r.sShare !== undefined ? (r.cShare - r.sShare).toFixed(1) : "", r.rank ?? "", r.top?.county ?? "", r.top?.share.toFixed(1) ?? ""]))} /></h3>
          <div className="tbl-wrap"><table className="rtable compact">
            <thead><tr><th>Issue</th><th className="num">Yes</th><th className="num">No</th><th className="bar">County yes share</th><th className="num">Statewide yes</th><th className="num">Diff</th><th className="num">Rank</th><th>Highest yes share</th></tr></thead>
            <tbody>{irows.map((r) => {
              const d = r.sShare !== undefined ? r.cShare - r.sShare : undefined;
              return (
                <tr key={r.issue.id}>
                  <td className="race">{r.issue.number && <span className="issue-num">{r.issue.number}</span>} <b>{r.issue.title}</b></td>
                  <td className="num">{fmtInt(r.yes)}</td><td className="num">{fmtInt(r.no)}</td>
                  <td className="bar"><Bar v={r.cShare} lead={r.yes > r.no} /><span className="sub-inline">{r.cShare.toFixed(1)}%</span></td>
                  <td className="num">{r.sShare !== undefined ? `${r.sShare.toFixed(1)}%` : "—"}</td>
                  <td className={`num ${d !== undefined && Math.abs(d) >= 5 ? "close" : ""}`}>{d !== undefined ? `${pts(d)} pts` : ""}</td>
                  <td className="num">{r.rank ? <>{r.rank}<span className="sub-inline"> of {r.of}</span></> : ""}</td>
                  <td className="sub">{r.top ? `${r.top.county} · ${r.top.share.toFixed(1)}%` : ""}</td>
                </tr>
              );
            })}</tbody>
          </table></div>
        </section>
      )}
      <p className="note">County shares are from the Board's report; statewide shares and the 88-county ranking are from the Secretary of State's election-night file, which can be a few minutes apart from the Board's. Rank 1 is the county where the candidate (or "yes") ran strongest. Diff is county share minus statewide share, orange at 5 points or more.</p>
    </>
  );
}

/* ---------------- Party lines: how the two major parties did, race by race ---------------- */

function PartyReport({ county, contests, results, sres, stateIds, file }: { county: County; contests: Contest[]; results: ResultsFile; sres: ResultsFile | null; stateIds: Set<string>; file: (n: string) => string }) {
  type Row = { contest: Contest; dem?: { name: string; votes: number }; rep?: { name: string; votes: number }; total: number; demShare: number; repShare: number; margin: number; sMargin?: number; statewide: boolean };
  const rows: Row[] = [];
  for (const c of contests) {
    const r = results.contests[c.id];
    if (!r) continue;
    const pick = (party: string) => { const k = c.candidates.find((x) => x.party === party); const v = k ? r.candidates.find((x) => x.name === k.name)?.votes : undefined; return k && v !== undefined ? { name: k.name, votes: v } : undefined; };
    const dem = pick("DEM"), rep = pick("REP");
    if (!dem && !rep) continue;
    const demShare = share(dem?.votes ?? 0, r.total), repShare = share(rep?.votes ?? 0, r.total);
    const row: Row = { contest: c, dem, rep, total: r.total, demShare, repShare, margin: demShare - repShare, statewide: stateIds.has(c.id) };
    const sr = sres?.contests[c.id];
    if (sr && dem && rep) {
      const sd = sr.candidates.find((x) => x.name === dem.name)?.votes, sp = sr.candidates.find((x) => x.name === rep.name)?.votes;
      if (sd !== undefined && sp !== undefined) row.sMargin = share(sd, sr.total) - share(sp, sr.total);
    }
    rows.push(row);
  }
  const contested = rows.filter((r) => r.dem && r.rep);
  const sw = contested.filter((r) => r.statewide);
  const swMargin = avg(sw.map((r) => r.margin));
  const swState = sw.filter((r) => r.sMargin !== undefined);
  const stateMargin = avg(swState.map((r) => r.sMargin!));
  const bestDem = contested.length ? contested.reduce((a, b) => (b.margin > a.margin ? b : a)) : null;
  const bestRep = contested.length ? contested.reduce((a, b) => (b.margin < a.margin ? b : a)) : null;
  const spread = sw.length > 1 ? Math.max(...sw.map((r) => r.margin)) - Math.min(...sw.map((r) => r.margin)) : null;
  const demWins = contested.filter((r) => r.margin > 0).length, repWins = contested.filter((r) => r.margin < 0).length;
  const name = (n: string) => n.split(" / ")[0];

  const groups: [string, Row[]][] = [];
  for (const row of rows) { const g = row.contest.group; const last = groups[groups.length - 1]; if (last && last[0] === g) last[1].push(row); else groups.push([g, [row]]); }

  return (
    <>
      <section className="stat-row">
        <Tile label="Contested D vs. R races" value={fmtInt(contested.length)} sub={`DEM leading ${demWins} · REP leading ${repWins}${rows.length > contested.length ? ` · ${rows.length - contested.length} with one major party` : ""}`} />
        <Tile label="County lean, statewide races" value={sw.length ? `${swMargin > 0 ? "D" : "R"} ${pts(Math.abs(swMargin)).replace("+", "")}` : "—"} sub={sw.length ? `average DEM − REP margin across ${sw.length} race${sw.length === 1 ? "" : "s"}` : undefined} />
        <Tile label="Ohio, same races" value={swState.length ? `${stateMargin > 0 ? "D" : "R"} ${pts(Math.abs(stateMargin)).replace("+", "")}` : "—"} sub={swState.length ? `${county.name} runs ${pts(swMargin - stateMargin)} pts more Democratic than Ohio` : "statewide file not published yet"} />
        <Tile label="Ticket splitting" value={spread !== null ? `${spread.toFixed(1)} pts` : "—"} sub={spread !== null ? "spread between the best and worst DEM − REP margins, statewide races" : undefined} />
        <Tile label="Best DEM race" value={bestDem ? `${pts(bestDem.margin)} pts` : "—"} sub={bestDem ? `${name(bestDem.dem!.name)} · ${bestDem.contest.office}` : undefined} />
        <Tile label="Best REP race" value={bestRep ? `${pts(-bestRep.margin)} pts` : "—"} sub={bestRep ? `${name(bestRep.rep!.name)} · ${bestRep.contest.office}` : undefined} />
      </section>
      <section>
        <h3 className="section-title">Partisan races <span className="count">{rows.length}</span><ExportBtn onClick={() => downloadCsv(file("party-lines"), ["Race", "Scope", "DEM candidate", "DEM votes", "DEM share", "REP candidate", "REP votes", "REP share", "DEM − REP pts", "Statewide DEM − REP pts", "County vs Ohio pts"], rows.map((r) => [r.contest.office + (r.contest.detail ? ` (${r.contest.detail})` : ""), r.statewide ? "Statewide" : "County / district", r.dem?.name ?? "", r.dem?.votes ?? "", r.dem ? r.demShare.toFixed(1) : "", r.rep?.name ?? "", r.rep?.votes ?? "", r.rep ? r.repShare.toFixed(1) : "", r.dem && r.rep ? r.margin.toFixed(1) : "", r.sMargin?.toFixed(1) ?? "", r.sMargin !== undefined ? (r.margin - r.sMargin).toFixed(1) : ""]))} /></h3>
        <div className="tbl-wrap"><table className="rtable compact">
          <thead><tr><th>Race</th><th>Democrat</th><th className="num">Share</th><th>Republican</th><th className="num">Share</th><th className="bar">D − R split</th><th className="num">Margin</th><th className="num">Ohio</th><th className="num">vs. Ohio</th></tr></thead>
          {groups.map(([g, rs]) => (
            <tbody key={g}>
              <tr className="grp"><td colSpan={9}>{g}</td></tr>
              {rs.map((r) => {
                const two = r.demShare + r.repShare;
                const dTwo = two > 0 ? (100 * r.demShare) / two : 0;
                const both = r.dem && r.rep;
                return (
                  <tr key={r.contest.id}>
                    <td className="race"><b>{r.contest.office}</b>{r.contest.detail && <div className="sub">{r.contest.detail}</div>}</td>
                    <td className="who">{r.dem ? name(r.dem.name) : <span className="muted">—</span>}</td>
                    <td className="num">{r.dem ? `${r.demShare.toFixed(1)}%` : ""}</td>
                    <td className="who">{r.rep ? name(r.rep.name) : <span className="muted">—</span>}</td>
                    <td className="num">{r.rep ? `${r.repShare.toFixed(1)}%` : ""}</td>
                    <td className="bar">{both ? <span className="split" aria-hidden="true"><span className="d" style={{ width: `${dTwo}%` }} /><span className="r" style={{ width: `${100 - dTwo}%` }} /></span> : <span className="muted sub-inline">unopposed by the other party</span>}</td>
                    <td className={`num ${both && Math.abs(r.margin) < 2 ? "close" : ""}`}>{both ? <>{r.margin > 0 ? "D" : r.margin < 0 ? "R" : "tie"} {Math.abs(r.margin).toFixed(1)}</> : ""}</td>
                    <td className="num">{r.sMargin !== undefined ? <>{r.sMargin > 0 ? "D" : "R"} {Math.abs(r.sMargin).toFixed(1)}</> : r.statewide ? "" : <span className="sub-inline">{countywide(r.contest) ? "county" : "district"}</span>}</td>
                    <td className={`num ${r.sMargin !== undefined && Math.abs(r.margin - r.sMargin) >= 5 ? "close" : ""}`}>{r.sMargin !== undefined ? `${pts(r.margin - r.sMargin)}` : ""}</td>
                  </tr>
                );
              })}
            </tbody>
          ))}
        </table></div>
      </section>
      <p className="note">Shares are of all votes in the contest, so a Libertarian or write-in keeps the two from summing to 100; the split bar is the two-party share. Margin is DEM share minus REP share in points; "vs. Ohio" is how much more Democratic (+) or Republican (−) the county ran than the state in the same race. Nonpartisan races (courts, boards) are left out.</p>
    </>
  );
}

/* ---------------- Issues & levies: what is passing, by kind and jurisdiction ---------------- */

function IssuesReport({ issues, results, official, file }: { issues: Issue[]; results: ResultsFile; official: boolean; file: (n: string) => string }) {
  const [sort, setSort] = useState<"ballot" | "yes">("ballot");
  type Row = { issue: Issue; r: IssueResult; yes: number; kind: string; passing: boolean; tied: boolean };
  const kindOf = (q: Issue) => (q.kind === "levy" ? `Levy · ${levyType(q)}` : q.kind === "state" ? "State issue" : q.kind === "question" ? "Question" : "Liquor option");
  const rows: Row[] = issues.flatMap((q) => { const r = results.issues[q.id]; return r && r.total > 0 ? [{ issue: q, r, yes: share(r.yes, r.total), kind: kindOf(q), passing: r.yes > r.no, tied: r.yes === r.no }] : []; });
  const passing = rows.filter((r) => r.passing).length, failing = rows.filter((r) => !r.passing && !r.tied).length;
  const levies = rows.filter((r) => r.issue.kind === "levy");
  const closest = rows.length ? rows.reduce((a, b) => (Math.abs(b.yes - 50) < Math.abs(a.yes - 50) ? b : a)) : null;
  const byKind = new Map<string, Row[]>();
  for (const r of rows) byKind.set(r.kind, [...(byKind.get(r.kind) ?? []), r]);
  const kinds = [...byKind.entries()].sort((a, b) => b[1].length - a[1].length);
  const word = (p: boolean) => (official ? (p ? "Passed" : "Failed") : (p ? "Passing" : "Failing"));
  const list = sort === "yes" ? [...rows].sort((a, b) => b.yes - a.yes) : rows;

  return (
    <>
      <section className="stat-row">
        <Tile label="Issues counted" value={fmtInt(rows.length)} sub={`${levies.length} tax levies · ${rows.length - levies.length} questions, options and state issues`} />
        <Tile label={word(true)} value={fmtInt(passing)} sub={rows.length ? pct(passing, rows.length) + " of issues" : undefined} />
        <Tile label={word(false)} value={fmtInt(failing)} sub={rows.some((r) => r.tied) ? `${rows.filter((r) => r.tied).length} tied` : undefined} />
        <Tile label="Levies" value={levies.length ? `${levies.filter((r) => r.passing).length} of ${levies.length}` : "—"} sub={levies.length ? `${word(true).toLowerCase()} · average yes ${avg(levies.map((r) => r.yes)).toFixed(1)}%` : undefined} />
        <Tile label="Closest" value={closest ? `${closest.yes.toFixed(1)}% yes` : "—"} sub={closest ? closest.issue.title : undefined} />
      </section>
      <section>
        <h3 className="section-title">By kind <span className="count">{kinds.length}</span><ExportBtn onClick={() => downloadCsv(file("issues-by-kind"), ["Kind", "Issues", word(true), word(false), "Average yes share"], kinds.map(([k, rs]) => [k, rs.length, rs.filter((r) => r.passing).length, rs.filter((r) => !r.passing && !r.tied).length, avg(rs.map((r) => r.yes)).toFixed(1)]))} /></h3>
        <div className="tbl-wrap"><table className="rtable compact">
          <thead><tr><th>Kind</th><th className="num">Issues</th><th className="num">{word(true)}</th><th className="num">{word(false)}</th><th className="bar">Average yes share</th></tr></thead>
          <tbody>{kinds.map(([k, rs]) => { const a = avg(rs.map((r) => r.yes)); return (
            <tr key={k}><td className="race"><b>{k}</b></td><td className="num">{rs.length}</td><td className="num">{rs.filter((r) => r.passing).length}</td><td className="num">{rs.filter((r) => !r.passing && !r.tied).length}</td><td className="bar"><Bar v={a} lead={a > 50} /><span className="sub-inline">{a.toFixed(1)}%</span></td></tr>
          ); })}</tbody>
        </table></div>
      </section>
      <section>
        <h3 className="section-title">Every issue <span className="count">{rows.length}</span>
          <span className="seg small" role="group" aria-label="Order"><button type="button" className={sort === "ballot" ? "active" : ""} onClick={() => setSort("ballot")}>Ballot order</button><button type="button" className={sort === "yes" ? "active" : ""} onClick={() => setSort("yes")}>Yes share</button></span>
          <ExportBtn onClick={() => downloadCsv(file("issues"), ["Issue", "Kind", "Jurisdiction", "Mills", "Term", "Yes", "No", "Yes share", "Standing"], list.map((r) => [r.issue.title, r.kind, r.issue.jurisdiction, r.issue.levy?.mills ?? "", r.issue.levy?.term ?? "", r.r.yes, r.r.no, r.yes.toFixed(1), r.tied ? "Tied" : word(r.passing)]))} /></h3>
        <div className="tbl-wrap"><table className="rtable compact">
          <thead><tr><th>Issue</th><th>Jurisdiction</th><th className="num">Yes</th><th className="num">No</th><th className="bar">Yes share</th><th>Standing</th></tr></thead>
          <tbody>{list.map((r) => (
            <tr key={r.issue.id}>
              <td className="race">{r.issue.number && <span className="issue-num">{r.issue.number}</span>} <b>{r.issue.title}</b><div className="sub">{r.kind}{r.issue.levy?.mills ? ` · ${r.issue.levy.mills}` : ""}{r.issue.levy?.term ? ` · ${r.issue.levy.term}` : ""}</div></td>
              <td className="who">{r.issue.jurisdiction}</td>
              <td className="num">{fmtInt(r.r.yes)}</td><td className="num">{fmtInt(r.r.no)}</td>
              <td className="bar"><Bar v={r.yes} lead={r.passing} /><span className={`sub-inline ${Math.abs(r.yes - 50) < 2 ? "close" : ""}`}>{r.yes.toFixed(1)}%</span></td>
              <td><span className={`standing ${r.tied ? "" : r.passing ? "yes" : "no"}`}>{r.tied ? "Tied" : word(r.passing)}</span></td>
            </tr>
          ))}</tbody>
        </table></div>
      </section>
      <p className="note">An issue passes with more yes than no votes. Issues with no votes reported are left out. Levy kinds (renewal, additional, replacement) are as the Board filed them.</p>
    </>
  );
}
