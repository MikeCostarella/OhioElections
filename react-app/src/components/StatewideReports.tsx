import { useMemo, useState } from "react";
import type { Ballot, Contest, ResultsFile } from "../data/types";
import { COUNTIES, type County } from "../data/counties";
import { fmtInt, pct, share, shortTime } from "../data/load";

/* Statewide reports: the Secretary of State's file, all 88 counties. Shared helpers live in ReportsView; the few
   needed here are duplicated rather than exported, so each file reads on its own. */

type Cell = string | number;
const pts = (n: number) => `${n > 0 ? "+" : ""}${n.toFixed(1)}`;
const avg = (xs: number[]) => (xs.length ? xs.reduce((a, b) => a + b, 0) / xs.length : 0);
const median = (xs: number[]) => { if (!xs.length) return 0; const s = [...xs].sort((a, b) => a - b); const m = s.length >> 1; return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2; };
const countyName = (slug: string) => COUNTIES.find((c) => c.slug === slug)?.name ?? slug;
const first = (n: string) => n.split(" / ")[0];

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
function Bar({ v, lead }: { v: number; lead?: boolean }) {
  return <span className={`rbar${lead ? " lead" : ""}`} aria-hidden="true"><span style={{ width: `${Math.max(0, Math.min(100, v))}%` }} /></span>;
}
function ExportBtn({ onClick }: { onClick: () => void }) {
  return <button type="button" className="csv-btn" onClick={onClick} title="Download this table as CSV">⬇ CSV</button>;
}

export type StateReportId = "results" | "counties" | "turnout" | "lean";
export const STATE_REPORTS: { id: StateReportId; label: string }[] = [
  { id: "results", label: "Statewide results" },
  { id: "counties", label: "Counties ranked" },
  { id: "turnout", label: "Turnout by county" },
  { id: "lean", label: "Party lean by county" },
];

interface Props {
  report: StateReportId;
  county: County | null;
  state: Ballot;
  sres: ResultsFile;
  file: (n: string) => string;
}

export default function StatewideReports({ report, county, state, sres, file }: Props) {
  const contests = useMemo(() => state.contests.filter((c) => sres.contests[c.id]), [state, sres]);
  const issues = useMemo(() => state.issues.filter((q) => sres.issues[q.id]), [state, sres]);
  return (
    <>
      {report === "results" && <ResultsReport contests={contests} issues={issues} sres={sres} file={file} />}
      {report === "counties" && <CountiesReport county={county} contests={contests} issues={issues} sres={sres} file={file} />}
      {report === "turnout" && <TurnoutReport county={county} sres={sres} file={file} />}
      {report === "lean" && <LeanReport county={county} contests={contests} sres={sres} file={file} />}
    </>
  );
}

/* ---------------- Statewide results: every statewide race and issue, with counties led ---------------- */

function ResultsReport({ contests, issues, sres, file }: { contests: Contest[]; issues: Ballot["issues"]; sres: ResultsFile; file: (n: string) => string }) {
  const p = sres.precincts;
  const reporting = Object.values(sres.counties ?? {}).filter((c) => c.precincts && c.precincts.reporting >= c.precincts.total).length;
  type Row = { c: Contest; name: string; party?: string; votes: number; sh: number; led: number; lead: boolean };
  const rows: Row[] = [];
  for (const c of contests) {
    const r = sres.contests[c.id];
    const led = new Map<string, number>();
    for (const x of Object.values(r.counties ?? {})) { const top = [...x.candidates].sort((a, b) => b.votes - a.votes)[0]; if (top) led.set(top.name, (led.get(top.name) ?? 0) + 1); }
    const leadName = [...r.candidates].sort((a, b) => b.votes - a.votes)[0]?.name;
    const byVotes = [...c.candidates].sort((a, b) => (r.candidates.find((x) => x.name === b.name)?.votes ?? -1) - (r.candidates.find((x) => x.name === a.name)?.votes ?? -1));
    for (const k of byVotes) {
      const v = r.candidates.find((x) => x.name === k.name)?.votes;
      if (v === undefined) continue;
      rows.push({ c, name: k.name, party: k.party, votes: v, sh: share(v, r.total), led: led.get(k.name) ?? 0, lead: k.name === leadName });
    }
  }
  const groups: [string, Row[]][] = [];
  for (const row of rows) { const g = row.c.group; const last = groups[groups.length - 1]; if (last && last[0] === g) last[1].push(row); else groups.push([g, [row]]); }
  const nCounties = Object.keys(sres.contests[contests[0]?.id]?.counties ?? {}).length || 88;

  return (
    <>
      <section className="stat-row">
        <Tile label="Ballots cast" value={sres.ballotsCast !== undefined ? fmtInt(sres.ballotsCast) : "—"} sub={sres.registered !== undefined ? `of ${fmtInt(sres.registered)} registered` : undefined} />
        <Tile label="Turnout" value={sres.turnout !== undefined ? `${sres.turnout.toFixed(1)}%` : "—"} sub="all of Ohio" />
        <Tile label="Election Day precincts" value={p ? `${fmtInt(p.reporting)} of ${fmtInt(p.total)}` : "—"} sub={p ? (p.reporting >= p.total ? "all reporting" : "reporting") : undefined} />
        <Tile label="Counties fully reporting" value={sres.counties ? `${reporting} of ${Object.keys(sres.counties).length}` : "—"} />
        <Tile label="Report" value={shortTime(sres.asOf)} sub="Secretary of State" />
      </section>
      <section>
        <h3 className="section-title">Statewide races <span className="count">{contests.length}</span><ExportBtn onClick={() => downloadCsv(file("ohio-results"), ["Race", "Candidate", "Party", "Votes", "Share", "Counties led"], rows.map((r) => [r.c.office, r.name, r.party ?? "", r.votes, r.sh.toFixed(1), r.led]))} /></h3>
        <div className="tbl-wrap"><table className="rtable compact">
          <thead><tr><th>Candidate</th><th className="num">Votes</th><th className="bar">Share</th><th className="num">Counties led</th><th className="bar">Of {nCounties}</th></tr></thead>
          {groups.map(([g, rs]) => (
            <tbody key={g}>
              <tr className="grp"><td colSpan={5}>{g}</td></tr>
              {rs.map((r) => (
                <tr key={r.c.id + r.name}>
                  <td className="who"><b>{r.name}</b>{r.party && <span className="party-tag">{r.party}</span>}<div className="sub">{r.c.office}{r.c.detail ? ` · ${r.c.detail}` : ""}{r.lead ? " · leading statewide" : ""}</div></td>
                  <td className="num">{fmtInt(r.votes)}</td>
                  <td className="bar"><Bar v={r.sh} lead={r.lead} /><span className="sub-inline">{r.sh.toFixed(1)}%</span></td>
                  <td className="num">{r.led || ""}</td>
                  <td className="bar">{r.led ? <><Bar v={share(r.led, nCounties)} lead={r.lead} /><span className="sub-inline">{pct(r.led, nCounties)}</span></> : ""}</td>
                </tr>
              ))}
            </tbody>
          ))}
        </table></div>
      </section>
      {issues.length > 0 && (
        <section>
          <h3 className="section-title">State issues <span className="count">{issues.length}</span><ExportBtn onClick={() => downloadCsv(file("ohio-issues"), ["Issue", "Yes", "No", "Yes share", "Counties yes", "Counties no"], issues.map((q) => { const r = sres.issues[q.id]; const cs = Object.values(r.counties ?? {}); return [q.title, r.yes, r.no, share(r.yes, r.total).toFixed(1), cs.filter((x) => x.yes > x.no).length, cs.filter((x) => x.no > x.yes).length]; }))} /></h3>
          <div className="tbl-wrap"><table className="rtable compact">
            <thead><tr><th>Issue</th><th className="num">Yes</th><th className="num">No</th><th className="bar">Yes share</th><th className="num">Counties yes</th><th className="num">Counties no</th></tr></thead>
            <tbody>{issues.map((q) => { const r = sres.issues[q.id]; const cs = Object.values(r.counties ?? {}); const y = share(r.yes, r.total); return (
              <tr key={q.id}>
                <td className="race">{q.number && <span className="issue-num">{q.number}</span>} <b>{q.title}</b></td>
                <td className="num">{fmtInt(r.yes)}</td><td className="num">{fmtInt(r.no)}</td>
                <td className="bar"><Bar v={y} lead={r.yes > r.no} /><span className="sub-inline">{y.toFixed(1)}%</span></td>
                <td className="num">{cs.filter((x) => x.yes > x.no).length}</td><td className="num">{cs.filter((x) => x.no > x.yes).length}</td>
              </tr>
            ); })}</tbody>
          </table></div>
        </section>
      )}
      <p className="note">"Counties led" is how many of the 88 counties the candidate has the most votes in so far — a map-free picture of where the vote came from, not a call. Statewide totals are from the Secretary of State's election-night feed.</p>
    </>
  );
}

/* ---------------- Counties ranked: pick a race or issue, see all 88 counties ---------------- */

function CountiesReport({ county, contests, issues, sres, file }: { county: County | null; contests: Contest[]; issues: Ballot["issues"]; sres: ResultsFile; file: (n: string) => string }) {
  const options = [...contests.map((c) => ({ id: `c:${c.id}`, label: `${c.office}${c.detail ? ` · ${c.detail}` : ""}` })), ...issues.map((q) => ({ id: `q:${q.id}`, label: `${q.number ? `${q.number}: ` : ""}${q.title}` }))];
  const [pick, setPick] = useState(options[0]?.id ?? "");
  const [sort, setSort] = useState<"share" | "name" | "votes">("share");
  const [kind, id] = pick.split(":") as ["c" | "q", string];

  if (kind === "c") {
    const c = contests.find((x) => x.id === id);
    const r = c ? sres.contests[c.id] : undefined;
    if (!c || !r?.counties) return <p className="note">No county numbers for this race.</p>;
    const cands = [...r.candidates].sort((a, b) => b.votes - a.votes).map((k) => ({ name: k.name, party: c.candidates.find((x) => x.name === k.name)?.party }));
    const lead = cands[0], next = cands[1];
    const rows = Object.entries(r.counties).map(([slug, x]) => {
      const sh = (name: string) => share(x.candidates.find((k) => k.name === name)?.votes ?? 0, x.total);
      const top = [...x.candidates].sort((a, b) => b.votes - a.votes)[0];
      return { slug, name: countyName(slug), total: x.total, shares: cands.map((k) => sh(k.name)), top: top?.name, margin: next ? sh(lead.name) - sh(next.name) : sh(lead.name) };
    });
    rows.sort((a, b) => sort === "name" ? a.name.localeCompare(b.name) : sort === "votes" ? b.total - a.total : b.margin - a.margin);
    const mine = rows.find((x) => x.slug === county?.slug);
    const rankOf = (slug: string) => [...rows].sort((a, b) => b.margin - a.margin).findIndex((x) => x.slug === slug) + 1;
    const ledBy = new Map<string, number>();
    for (const x of rows) if (x.top) ledBy.set(x.top, (ledBy.get(x.top) ?? 0) + 1);
    const label = (n: string) => first(n);
    return (
      <>
        <div className="filters">
          <label className="pick">Race or issue{" "}
            <select value={pick} onChange={(e) => setPick(e.target.value)}>{options.map((o) => <option key={o.id} value={o.id}>{o.label}</option>)}</select>
          </label>
          <div className="seg small" role="group" aria-label="Order">
            <button type="button" className={sort === "share" ? "active" : ""} onClick={() => setSort("share")}>Best for {label(lead.name)} first</button>
            <button type="button" className={sort === "votes" ? "active" : ""} onClick={() => setSort("votes")}>Most votes</button>
            <button type="button" className={sort === "name" ? "active" : ""} onClick={() => setSort("name")}>A–Z</button>
          </div>
        </div>
        <section className="stat-row">
          {cands.slice(0, 3).map((k) => <Tile key={k.name} label={`${label(k.name)}${k.party ? ` (${k.party})` : ""}`} value={pct(r.candidates.find((x) => x.name === k.name)!.votes, r.total)} sub={`statewide · leads ${ledBy.get(k.name) ?? 0} of ${rows.length} counties`} />)}
          {mine && county && <Tile label={`${county.name} County`} value={`${label(lead.name)} ${mine.shares[0].toFixed(1)}%`} sub={`margin ${pts(mine.margin)} pts · rank ${rankOf(mine.slug)} of ${rows.length} for ${label(lead.name)}`} />}
        </section>
        <section>
          <h3 className="section-title">{c.office}{c.detail ? ` · ${c.detail}` : ""} <span className="count">{rows.length} counties</span><ExportBtn onClick={() => downloadCsv(file(`ohio-counties-${c.id}`), ["County", "Votes", ...cands.map((k) => `${label(k.name)} share`), "Leading", `${label(lead.name)} margin pts`], rows.map((x) => [x.name, x.total, ...x.shares.map((s) => s.toFixed(1)), x.top ? label(x.top) : "", x.margin.toFixed(1)]))} /></h3>
          <div className="tbl-wrap"><table className="rtable compact">
            <thead><tr><th className="num">#</th><th>County</th><th className="num">Votes</th>{cands.map((k) => <th key={k.name} className="num">{label(k.name)}{k.party && <span className="party-tag">{k.party}</span>}</th>)}<th className="bar">{label(lead.name)} share</th><th className="num">Margin</th></tr></thead>
            <tbody>{rows.map((x, i) => (
              <tr key={x.slug} className={x.slug === county?.slug ? "mine" : ""}>
                <td className="num sub">{i + 1}</td>
                <td className="race"><b>{x.name}</b>{x.slug === county?.slug && <span className="sub-inline"> ◀ yours</span>}</td>
                <td className="num">{fmtInt(x.total)}</td>
                {x.shares.map((s, j) => <td key={j} className={`num ${x.top === cands[j].name ? "led" : ""}`}>{s.toFixed(1)}%</td>)}
                <td className="bar"><Bar v={x.shares[0]} lead={x.top === lead.name} /></td>
                <td className={`num ${Math.abs(x.margin) < 2 ? "close" : ""}`}>{pts(x.margin)}</td>
              </tr>
            ))}</tbody>
          </table></div>
        </section>
        <p className="note">Margin is {label(lead.name)}'s share minus {next ? `${label(next.name)}'s` : "nothing"} in that county, in points; a negative margin is a county {next ? label(next.name) : ""} leads. The bold share marks who leads each county. Orange: under 2 points.</p>
      </>
    );
  }

  const q = issues.find((x) => x.id === id);
  const r = q ? sres.issues[q.id] : undefined;
  if (!q || !r?.counties) return <p className="note">No county numbers for this issue.</p>;
  const rows = Object.entries(r.counties).map(([slug, x]) => ({ slug, name: countyName(slug), total: x.total, yes: x.yes, no: x.no, sh: share(x.yes, x.total) }));
  rows.sort((a, b) => sort === "name" ? a.name.localeCompare(b.name) : sort === "votes" ? b.total - a.total : b.sh - a.sh);
  const mine = rows.find((x) => x.slug === county?.slug);
  const rank = [...rows].sort((a, b) => b.sh - a.sh).findIndex((x) => x.slug === county?.slug) + 1;
  return (
    <>
      <div className="filters">
        <label className="pick">Race or issue{" "}
          <select value={pick} onChange={(e) => setPick(e.target.value)}>{options.map((o) => <option key={o.id} value={o.id}>{o.label}</option>)}</select>
        </label>
        <div className="seg small" role="group" aria-label="Order">
          <button type="button" className={sort === "share" ? "active" : ""} onClick={() => setSort("share")}>Highest yes first</button>
          <button type="button" className={sort === "votes" ? "active" : ""} onClick={() => setSort("votes")}>Most votes</button>
          <button type="button" className={sort === "name" ? "active" : ""} onClick={() => setSort("name")}>A–Z</button>
        </div>
      </div>
      <section className="stat-row">
        <Tile label="Yes, statewide" value={pct(r.yes, r.total)} sub={`${fmtInt(r.yes)} votes`} />
        <Tile label="No, statewide" value={pct(r.no, r.total)} sub={`${fmtInt(r.no)} votes`} />
        <Tile label="Counties yes / no" value={`${rows.filter((x) => x.yes > x.no).length} / ${rows.filter((x) => x.no > x.yes).length}`} />
        {mine && county && <Tile label={`${county.name} County`} value={`${mine.sh.toFixed(1)}% yes`} sub={`rank ${rank} of ${rows.length}`} />}
      </section>
      <section>
        <h3 className="section-title">{q.number ? `${q.number}: ` : ""}{q.title} <span className="count">{rows.length} counties</span><ExportBtn onClick={() => downloadCsv(file(`ohio-counties-${q.id}`), ["County", "Votes", "Yes", "No", "Yes share"], rows.map((x) => [x.name, x.total, x.yes, x.no, x.sh.toFixed(1)]))} /></h3>
        <div className="tbl-wrap"><table className="rtable compact">
          <thead><tr><th className="num">#</th><th>County</th><th className="num">Votes</th><th className="num">Yes</th><th className="num">No</th><th className="bar">Yes share</th></tr></thead>
          <tbody>{rows.map((x, i) => (
            <tr key={x.slug} className={x.slug === county?.slug ? "mine" : ""}>
              <td className="num sub">{i + 1}</td>
              <td className="race"><b>{x.name}</b>{x.slug === county?.slug && <span className="sub-inline"> ◀ yours</span>}</td>
              <td className="num">{fmtInt(x.total)}</td><td className="num">{fmtInt(x.yes)}</td><td className="num">{fmtInt(x.no)}</td>
              <td className="bar"><Bar v={x.sh} lead={x.yes > x.no} /><span className={`sub-inline ${Math.abs(x.sh - 50) < 2 ? "close" : ""}`}>{x.sh.toFixed(1)}%</span></td>
            </tr>
          ))}</tbody>
        </table></div>
      </section>
    </>
  );
}

/* ---------------- Turnout by county ---------------- */

function TurnoutReport({ county, sres, file }: { county: County | null; sres: ResultsFile; file: (n: string) => string }) {
  const [sort, setSort] = useState<"turnout" | "ballots" | "name">("turnout");
  const rows = Object.entries(sres.counties ?? {}).map(([slug, x]) => ({ slug, name: countyName(slug), registered: x.registered ?? 0, ballots: x.ballotsCast ?? 0, turnout: x.turnout ?? share(x.ballotsCast ?? 0, x.registered ?? 0), p: x.precincts }));
  if (!rows.length) return <p className="note">The statewide file has no per-county turnout yet (it is added by the results tool; re-run <code>tools/results/sos.py</code>).</p>;
  rows.sort((a, b) => sort === "name" ? a.name.localeCompare(b.name) : sort === "ballots" ? b.ballots - a.ballots : b.turnout - a.turnout);
  const byT = [...rows].sort((a, b) => b.turnout - a.turnout);
  const mine = rows.find((x) => x.slug === county?.slug);
  const rank = byT.findIndex((x) => x.slug === county?.slug) + 1;
  const hi = byT[0], lo = byT[byT.length - 1];
  const stateT = sres.turnout ?? share(sres.ballotsCast ?? 0, sres.registered ?? 0);
  return (
    <>
      <section className="stat-row">
        <Tile label="Ohio turnout" value={`${stateT.toFixed(1)}%`} sub={sres.ballotsCast !== undefined ? `${fmtInt(sres.ballotsCast)} of ${fmtInt(sres.registered ?? 0)}` : undefined} />
        <Tile label="Median county" value={`${median(rows.map((x) => x.turnout)).toFixed(1)}%`} sub={`${rows.length} counties`} />
        <Tile label="Highest" value={`${hi.turnout.toFixed(1)}%`} sub={`${hi.name} County`} />
        <Tile label="Lowest" value={`${lo.turnout.toFixed(1)}%`} sub={`${lo.name} County`} />
        {mine && county && <Tile label={`${county.name} County`} value={`${mine.turnout.toFixed(1)}%`} sub={`rank ${rank} of ${rows.length} · ${pts(mine.turnout - stateT)} pts vs. Ohio`} />}
      </section>
      <div className="filters">
        <div className="seg small" role="group" aria-label="Order">
          <button type="button" className={sort === "turnout" ? "active" : ""} onClick={() => setSort("turnout")}>Turnout</button>
          <button type="button" className={sort === "ballots" ? "active" : ""} onClick={() => setSort("ballots")}>Ballots cast</button>
          <button type="button" className={sort === "name" ? "active" : ""} onClick={() => setSort("name")}>A–Z</button>
        </div>
      </div>
      <section>
        <h3 className="section-title">Turnout by county <span className="count">{rows.length}</span><ExportBtn onClick={() => downloadCsv(file("ohio-turnout"), ["County", "Registered", "Ballots cast", "Turnout", "Precincts reporting", "Precincts"], rows.map((x) => [x.name, x.registered, x.ballots, x.turnout.toFixed(2), x.p?.reporting ?? "", x.p?.total ?? ""]))} /></h3>
        <div className="tbl-wrap"><table className="rtable compact">
          <thead><tr><th className="num">#</th><th>County</th><th className="num">Registered</th><th className="num">Ballots cast</th><th className="bar">Turnout</th><th className="num">vs. Ohio</th><th className="num">Precincts</th></tr></thead>
          <tbody>{rows.map((x, i) => (
            <tr key={x.slug} className={x.slug === county?.slug ? "mine" : ""}>
              <td className="num sub">{i + 1}</td>
              <td className="race"><b>{x.name}</b>{x.slug === county?.slug && <span className="sub-inline"> ◀ yours</span>}</td>
              <td className="num">{fmtInt(x.registered)}</td><td className="num">{fmtInt(x.ballots)}</td>
              <td className="bar"><Bar v={x.turnout} lead={x.turnout >= stateT} /><span className="sub-inline">{x.turnout.toFixed(1)}%</span></td>
              <td className="num">{pts(x.turnout - stateT)}</td>
              <td className="num">{x.p ? <>{x.p.reporting} of {x.p.total}{x.p.reporting < x.p.total && <span className="close"> ·</span>}</> : ""}</td>
            </tr>
          ))}</tbody>
        </table></div>
      </section>
      <p className="note">Registered voters, ballots counted and turnout per county from the Secretary of State's election summary. Orange bars are counties at or above the statewide turnout; an orange dot marks a county with Election Day precincts still out.</p>
    </>
  );
}

/* ---------------- Party lean by county: average DEM − REP margin across the statewide partisan races ---------------- */

function LeanReport({ county, contests, sres, file }: { county: County | null; contests: Contest[]; sres: ResultsFile; file: (n: string) => string }) {
  const [sort, setSort] = useState<"lean" | "spread" | "name">("lean");
  // Statewide races with both a DEM and a REP candidate.
  const races = contests.flatMap((c) => { const d = c.candidates.find((k) => k.party === "DEM"), r = c.candidates.find((k) => k.party === "REP"); return d && r && sres.contests[c.id]?.counties ? [{ c, d: d.name, r: r.name }] : []; });
  if (!races.length) return <p className="note">No statewide race with both a Democrat and a Republican has county numbers yet.</p>;
  const stateMargin = avg(races.map(({ c, d, r }) => { const s = sres.contests[c.id]; return share(s.candidates.find((k) => k.name === d)?.votes ?? 0, s.total) - share(s.candidates.find((k) => k.name === r)?.votes ?? 0, s.total); }));
  const slugs = Object.keys(sres.contests[races[0].c.id].counties!);
  const rows = slugs.map((slug) => {
    const ms = races.map(({ c, d, r }) => { const x = sres.contests[c.id].counties![slug]; if (!x) return undefined; return share(x.candidates.find((k) => k.name === d)?.votes ?? 0, x.total) - share(x.candidates.find((k) => k.name === r)?.votes ?? 0, x.total); }).filter((m): m is number => m !== undefined);
    const lean = avg(ms);
    const hi = Math.max(...ms), lo = Math.min(...ms);
    const bestD = races[ms.indexOf(hi)], bestR = races[ms.indexOf(lo)];
    return { slug, name: countyName(slug), lean, spread: hi - lo, demRaces: ms.filter((m) => m > 0).length, n: ms.length, bestD: `${first(bestD.c.candidates.find((k) => k.party === "DEM")!.name)} ${pts(hi)}`, bestR: `${first(bestR.c.candidates.find((k) => k.party === "REP")!.name)} ${pts(-lo)}` };
  });
  rows.sort((a, b) => sort === "name" ? a.name.localeCompare(b.name) : sort === "spread" ? b.spread - a.spread : b.lean - a.lean);
  const byLean = [...rows].sort((a, b) => b.lean - a.lean);
  const mine = rows.find((x) => x.slug === county?.slug);
  const rank = byLean.findIndex((x) => x.slug === county?.slug) + 1;
  const demCounties = rows.filter((x) => x.lean > 0).length;
  const fmtLean = (m: number) => `${m > 0 ? "D" : m < 0 ? "R" : "even"} ${Math.abs(m).toFixed(1)}`;
  return (
    <>
      <section className="stat-row">
        <Tile label="Ohio lean" value={fmtLean(stateMargin)} sub={`average DEM − REP margin across ${races.length} statewide races`} />
        <Tile label="Counties leaning D / R" value={`${demCounties} / ${rows.length - demCounties}`} sub="by average margin" />
        <Tile label="Most Democratic" value={fmtLean(byLean[0].lean)} sub={`${byLean[0].name} County`} />
        <Tile label="Most Republican" value={fmtLean(byLean[byLean.length - 1].lean)} sub={`${byLean[byLean.length - 1].name} County`} />
        {mine && county && <Tile label={`${county.name} County`} value={fmtLean(mine.lean)} sub={`rank ${rank} of ${rows.length}, most Democratic first · ${pts(mine.lean - stateMargin)} pts vs. Ohio`} />}
      </section>
      <div className="filters">
        <div className="seg small" role="group" aria-label="Order">
          <button type="button" className={sort === "lean" ? "active" : ""} onClick={() => setSort("lean")}>Most Democratic first</button>
          <button type="button" className={sort === "spread" ? "active" : ""} onClick={() => setSort("spread")}>Most ticket-splitting</button>
          <button type="button" className={sort === "name" ? "active" : ""} onClick={() => setSort("name")}>A–Z</button>
        </div>
        <span className="muted" style={{ fontSize: 12 }}>{races.map((x) => x.c.office).join(" · ")}</span>
      </div>
      <section>
        <h3 className="section-title">Party lean by county <span className="count">{rows.length}</span><ExportBtn onClick={() => downloadCsv(file("ohio-party-lean"), ["County", "Average DEM − REP pts", "vs. Ohio pts", "Races DEM leads", "Races", "Spread pts", "Strongest DEM margin", "Strongest REP margin"], rows.map((x) => [x.name, x.lean.toFixed(1), (x.lean - stateMargin).toFixed(1), x.demRaces, x.n, x.spread.toFixed(1), x.bestD, x.bestR]))} /></h3>
        <div className="tbl-wrap"><table className="rtable compact">
          <thead><tr><th className="num">#</th><th>County</th><th className="bar">Lean</th><th className="num">Average margin</th><th className="num">vs. Ohio</th><th className="num">Races D leads</th><th className="num">Spread</th><th>Strongest DEM margin</th><th>Strongest REP margin</th></tr></thead>
          <tbody>{rows.map((x, i) => {
            const d = Math.max(0, Math.min(100, 50 + x.lean / 2));
            return (
              <tr key={x.slug} className={x.slug === county?.slug ? "mine" : ""}>
                <td className="num sub">{i + 1}</td>
                <td className="race"><b>{x.name}</b>{x.slug === county?.slug && <span className="sub-inline"> ◀ yours</span>}</td>
                <td className="bar"><span className="split" aria-hidden="true"><span className="d" style={{ width: `${d}%` }} /><span className="r" style={{ width: `${100 - d}%` }} /></span></td>
                <td className="num">{fmtLean(x.lean)}</td>
                <td className="num">{pts(x.lean - stateMargin)}</td>
                <td className="num">{x.demRaces} of {x.n}</td>
                <td className={`num ${x.spread >= 15 ? "close" : ""}`}>{x.spread.toFixed(1)}</td>
                <td className="sub">{x.bestD}</td><td className="sub">{x.bestR}</td>
              </tr>
            );
          })}</tbody>
        </table></div>
      </section>
      <p className="note">Lean is the county's average DEM share minus REP share across the statewide races that have one of each, in points. The bar is centred at even; full left is D+100. Spread is the gap between the county's best Democratic and best Republican margins — how much its voters split tickets (orange at 15 points or more).</p>
    </>
  );
}
