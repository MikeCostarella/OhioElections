import { useMemo, useState } from "react";
import type { Ballot, Contest, ContestResult, Issue, IssueKind, IssueResult, ResultsFile, Source } from "../data/types";
import ResultsBanner from "./ResultsBanner";
import type { County } from "../data/counties";
import { byLastName, fmtInt, pct, SOS } from "../data/load";

interface Props {
  county: County;
  state: Ballot;
  local: Ballot | null;
  place: string;
  results: ResultsFile | null;
}

const KIND_LABELS: Record<Exclude<IssueKind, "state">, string> = {
  levy: "Tax levies",
  question: "Questions",
  liquor: "Liquor options",
};

const KIND_ONE: Record<IssueKind, string> = { state: "State issue", levy: "Tax levy", question: "Question", liquor: "Liquor option" };

const appliesTo = (e: { places?: string[]; coverage?: string }, place: string) =>
  !place || e.coverage === "unknown" || !e.places || e.places.includes(place);

const NOT_MAPPED = "Boundaries not mapped here: check your sample ballot to see whether it is on yours.";

function SourceLinks({ ids, sources }: { ids: string[]; sources: Record<string, Source> }) {
  return (
    <span className="src">
      Source:{" "}
      {ids.map((id, i) => {
        const s = sources[id];
        return s ? (
          <span key={id}>{i > 0 && " · "}<a href={s.url} target="_blank" rel="noopener noreferrer" title={s.label}>{shortSource(s.label)}</a></span>
        ) : null;
      })}
    </span>
  );
}

/** Short link text for a source: "46-day notice", "candidate list", "issues list", "zero report"... (full label in the tooltip). */
function shortSource(label: string): string {
  const l = label.toLowerCase();
  const county = (label.match(/^(\w+) County/) || [])[1];
  const kind = /zero report/.test(l) ? "zero report" : /46-day/.test(l) ? "46-day notice" : /filings/.test(l) ? "filings list"
    : /candidate/.test(l) ? "candidate list" : /issue/.test(l) ? "issues list" : label.split(": ")[1] ?? label;
  return county ? `${county} ${kind}` : kind;
}

/** Google search for a candidate, in a new tab. Local races add the county so common names find the right person. */
function googleUrl(name: string, office: string, county?: string): string {
  const q = [name, office, county ? `${county} County` : "", "Ohio"].filter(Boolean).join(" ");
  return `https://www.google.com/search?q=${encodeURIComponent(q)}`;
}

/** A candidate's name as a search link; a joint ticket ("Amy Acton / David Pepper") gets one link per person. */
function CandidateName({ name, office, county }: { name: string; office: string; county?: string }) {
  const people = name.split(" / ");
  return (
    <span className="cand-name">
      {people.map((n, i) => (
        <span key={n}>
          {i > 0 && " / "}
          <a href={googleUrl(n, office, county)} target="_blank" rel="noopener noreferrer" title={`Search Google for ${n}`}>{n}</a>
        </span>
      ))}
    </span>
  );
}

/** A horizontal vote bar: share of the contest's total, with the count and per cent beside it. */
function VoteBar({ votes, total, lead, label }: { votes: number; total: number; lead?: boolean; label?: string }) {
  const share = total > 0 ? (100 * votes) / total : 0;
  return (
    <div className={`vote ${lead ? "lead" : ""}`} aria-label={`${label ?? ""} ${fmtInt(votes)} votes, ${pct(votes, total)}`.trim()}>
      <div className="vote-track"><div className="vote-fill" style={{ width: `${share}%` }} /></div>
      <span className="vote-n">{fmtInt(votes)}</span>
      <span className="vote-pct">{pct(votes, total)}</span>
    </div>
  );
}

function ContestCard({ c, sources, place, county, res }: { c: Contest; sources: Record<string, Source>; place: string; county?: string; res?: ContestResult }) {
  // Without results: alphabetical (Ohio rotates ballot order). With results: by votes, the leader first.
  const votesOf = (name: string) => res?.candidates.find((r) => r.name === name)?.votes;
  const cands = res
    ? [...c.candidates].sort((a, b) => (votesOf(b.name) ?? -1) - (votesOf(a.name) ?? -1) || byLastName(a, b))
    : [...c.candidates].sort(byLastName);
  const top = res ? Math.max(...res.candidates.map((r) => r.votes), 0) : 0;
  const contested = cands.length > 1;
  const extra = res?.candidates.filter((r) => r.unmatched) ?? [];
  return (
    <article className={`card contest ${res ? "has-results" : ""}`}>
      <h4>{c.office}</h4>
      {c.detail && <div className="detail">{c.detail}</div>}
      <ul className="cands">
        {cands.map((k) => {
          const v = votesOf(k.name);
          const lead = res !== undefined && contested && v !== undefined && v === top && top > 0;
          return (
            <li key={k.name} className={lead ? "leading" : ""}>
              <CandidateName name={k.name} office={c.office} county={county} />
              {k.party && <span className="party-tag" title="Party as printed by the Board of Elections">{k.party}</span>}
              {lead && <span className="lead-tag" title="Most votes so far — not a call">leading</span>}
              {k.note && <span className="cand-note">{k.note}</span>}
              {res && v !== undefined && <VoteBar votes={v} total={res.total} lead={lead} label={k.name} />}
              {res && v === undefined && <span className="cand-note">No total reported yet</span>}
            </li>
          );
        })}
        {extra.map((r) => (
          <li key={r.name}>
            <span className="cand-name">{r.name}</span>
            <VoteBar votes={r.votes} total={res!.total} label={r.name} />
          </li>
        ))}
      </ul>
      {res && (res.writeIn ?? 0) > 0 && <div className="detail">Write-in: {fmtInt(res.writeIn!)} · total votes cast: {fmtInt(res.total)}</div>}
      {res && !(res.writeIn ?? 0) && <div className="detail">Total votes cast: {fmtInt(res.total)}</div>}
      {cands.length === 1 && <div className="detail">Unopposed</div>}
      {c.places && !place && <div className="area"><b>Where:</b> {c.area}</div>}
      {c.coverage === "unknown" && <div className="note-inline">{NOT_MAPPED}</div>}
      <SourceLinks ids={c.sources} sources={sources} />
    </article>
  );
}

function IssueCard({ q, sources, res }: { q: Issue; sources: Record<string, Source>; res?: IssueResult }) {
  const yesLead = res ? res.yes > res.no : false;
  const noLead = res ? res.no > res.yes : false;
  return (
    <article className={`card issue kind-${q.kind} ${res ? "has-results" : ""}`}>
      <div className="issue-head">
        {q.number && <span className="issue-num">{q.number}</span>}
        <span className="kind-tag">{KIND_ONE[q.kind]}</span>
      </div>
      <h4>{q.title}</h4>
      {q.levy && (
        <dl className="levy">
          {q.levy.type && <div><dt>Type</dt><dd>{q.levy.type}</dd></div>}
          {q.levy.mills && <div><dt>Millage</dt><dd>{q.levy.mills}</dd></div>}
          {q.levy.term && <div><dt>Term</dt><dd>{q.levy.term}</dd></div>}
          {q.levy.firstDue && <div><dt>First due</dt><dd>{q.levy.firstDue}</dd></div>}
        </dl>
      )}
      {q.levy?.estimate && <div className="estimate">{q.levy.estimate}</div>}
      {q.text && <p className="ballot-text">{q.text}</p>}
      {q.bullets && <ul className="bullets">{q.bullets.map((b) => <li key={b}>{b}</li>)}</ul>}
      {q.yesNo && <p className="ballot-text">{q.yesNo}</p>}
      {res && (
        <div className="issue-results">
          <div className={`yn ${yesLead ? "lead" : ""}`}><span className="yn-label">{res.yesLabel ?? "Yes"}{yesLead && <span className="lead-tag">leading</span>}</span><VoteBar votes={res.yes} total={res.total} lead={yesLead} label={res.yesLabel ?? "Yes"} /></div>
          <div className={`yn ${noLead ? "lead" : ""}`}><span className="yn-label">{res.noLabel ?? "No"}{noLead && <span className="lead-tag">leading</span>}</span><VoteBar votes={res.no} total={res.total} lead={noLead} label={res.noLabel ?? "No"} /></div>
          <div className="detail">Total votes cast: {fmtInt(res.total)}</div>
        </div>
      )}
      {q.area && q.area !== q.jurisdiction && <div className="area"><b>Where:</b> {q.area}</div>}
      {q.coverage === "unknown" && <div className="note-inline">{NOT_MAPPED}</div>}
      {q.note && <div className="note-inline">{q.note}</div>}
      <SourceLinks ids={q.sources} sources={sources} />
    </article>
  );
}

function group<T>(items: T[], key: (t: T) => string): [string, T[]][] {
  const m = new Map<string, T[]>();
  for (const it of items) { const k = key(it); if (!m.has(k)) m.set(k, []); m.get(k)!.push(it); }
  return [...m.entries()];
}

export default function BallotView({ county, state, local, place, results }: Props) {
  const [kinds, setKinds] = useState<Set<string>>(() => new Set(Object.keys(KIND_LABELS)));
  const [q, setQ] = useState("");

  const contests = useMemo(
    () => [...state.contests, ...(local?.contests ?? [])].filter((c) => appliesTo(c, place)),
    [state, local, place],
  );
  const stateIssues = state.issues;
  const localIssues = useMemo(() => {
    const needle = q.trim().toLowerCase();
    return (local?.issues ?? [])
      .filter((i) => appliesTo(i, place) && kinds.has(i.kind))
      .filter((i) => !needle || [i.jurisdiction, i.title, i.area, i.text ?? "", i.levy?.purpose ?? ""].join(" ").toLowerCase().includes(needle))
      .sort((a, b) => a.jurisdiction.localeCompare(b.jurisdiction));
  }, [local, place, kinds, q]);

  const sources = { ...state.sources, ...(local?.sources ?? {}) };
  const stateIds = new Set(state.contests.map((c) => c.id));
  const toggleKind = (k: string) => setKinds((prev) => { const n = new Set(prev); if (n.has(k)) n.delete(k); else n.add(k); return n.size ? n : prev; });
  const localTotal = local ? local.issues.filter((i) => appliesTo(i, place)).length : 0;

  const cRes = (id: string) => results?.contests[id];
  const iRes = (id: string) => results?.issues[id];
  const counted = results ? Object.keys(results.contests).length + Object.keys(results.issues).length : 0;

  return (
    <div className="ballot">
      {results && counted > 0 && <ResultsBanner r={results} countyName={county.name} />}
      {!local && (
        <p className="banner">
          Only the statewide races and State Issue 3 are loaded for {county.name} County so far. For the county and local races and issues, see the{" "}
          <a href={SOS.boeDirectory} target="_blank" rel="noopener noreferrer">{county.name} County Board of Elections</a> or{" "}
          <a href={SOS.sampleBallot} target="_blank" rel="noopener noreferrer">look up your sample ballot</a>.
        </p>
      )}

      <section>
        <h3 className="section-title">Candidates <span className="count">{contests.length} contests</span></h3>
        {group(contests, (c) => c.group).map(([g, cs]) => (
          <div key={g} className="group">
            <h4 className="group-title">{g}</h4>
            <div className="grid">{cs.map((c) => <ContestCard key={c.id} c={c} sources={sources} place={place} county={stateIds.has(c.id) ? undefined : county.name} res={cRes(c.id)} />)}</div>
          </div>
        ))}
      </section>

      <section>
        <h3 className="section-title">State issue</h3>
        <div className="grid wide">{stateIssues.map((i) => <IssueCard key={i.id} q={i} sources={sources} res={iRes(i.id)} />)}</div>
      </section>

      {local && (
        <section>
          <h3 className="section-title">
            Local questions and issues <span className="count">{localIssues.length === localTotal ? localTotal : `${localIssues.length} of ${localTotal}`}</span>
          </h3>
          <div className="filters">
            <div className="seg" role="group" aria-label="Kinds of issues">
              {Object.entries(KIND_LABELS).map(([k, label]) => (
                <button key={k} type="button" className={kinds.has(k) ? "active" : ""} aria-pressed={kinds.has(k)} onClick={() => toggleKind(k)}>{label}</button>
              ))}
            </div>
            <input type="search" className="search" placeholder="Search issues (e.g. school, fire, Hubbard)" value={q} onChange={(e) => setQ(e.target.value)} aria-label="Search issues" />
          </div>
          {localIssues.length === 0 && <p className="note">No local issues match{place ? ` for ${place}` : ""}.</p>}
          {group(localIssues, (i) => i.jurisdiction).map(([j, is]) => (
            <div key={j} className="group">
              <h4 className="group-title">{j}</h4>
              <div className="grid wide">{is.map((i) => <IssueCard key={i.id} q={i} sources={sources} res={iRes(i.id)} />)}</div>
            </div>
          ))}
        </section>
      )}

      {[...(state.notes ?? []), ...(local?.notes ?? [])].map((n) => <p key={n} className="note">{n}</p>)}
      {results && counted > 0 && results.status === "unofficial" && (
        <p className="note">Totals are the Board of Elections' unofficial count and update every few minutes on election night. "Leading" means the most votes counted so far, not a call. Unofficial results leave out provisional ballots and mail ballots that arrive after Election Day; the Board certifies the official result after the canvass.</p>
      )}
      <p className="note">Data checked against the sources on {local?.retrieved ?? state.retrieved}.</p>
    </div>
  );
}
