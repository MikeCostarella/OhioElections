import { useMemo, useState } from "react";
import type { Ballot, Contest, Issue, IssueKind, Source } from "../data/types";
import type { County } from "../data/counties";
import { byLastName, SOS } from "../data/load";

interface Props {
  county: County;
  state: Ballot;
  local: Ballot | null;
  place: string;
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

function ContestCard({ c, sources, place }: { c: Contest; sources: Record<string, Source>; place: string }) {
  const cands = [...c.candidates].sort(byLastName);
  return (
    <article className="card contest">
      <h4>{c.office}</h4>
      {c.detail && <div className="detail">{c.detail}</div>}
      <ul className="cands">
        {cands.map((k) => (
          <li key={k.name}>
            <span className="cand-name">{k.name}</span>
            {k.party && <span className="party-tag" title="Party as printed by the Board of Elections">{k.party}</span>}
            {k.note && <span className="cand-note">{k.note}</span>}
          </li>
        ))}
      </ul>
      {cands.length === 1 && <div className="detail">Unopposed</div>}
      {c.places && !place && <div className="area"><b>Where:</b> {c.area}</div>}
      {c.coverage === "unknown" && <div className="note-inline">{NOT_MAPPED}</div>}
      <SourceLinks ids={c.sources} sources={sources} />
    </article>
  );
}

function IssueCard({ q, sources }: { q: Issue; sources: Record<string, Source> }) {
  return (
    <article className={`card issue kind-${q.kind}`}>
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

export default function BallotView({ county, state, local, place }: Props) {
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
  const toggleKind = (k: string) => setKinds((prev) => { const n = new Set(prev); if (n.has(k)) n.delete(k); else n.add(k); return n.size ? n : prev; });
  const localTotal = local ? local.issues.filter((i) => appliesTo(i, place)).length : 0;

  return (
    <div className="ballot">
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
            <div className="grid">{cs.map((c) => <ContestCard key={c.id} c={c} sources={sources} place={place} />)}</div>
          </div>
        ))}
      </section>

      <section>
        <h3 className="section-title">State issue</h3>
        <div className="grid wide">{stateIssues.map((i) => <IssueCard key={i.id} q={i} sources={sources} />)}</div>
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
              <div className="grid wide">{is.map((i) => <IssueCard key={i.id} q={i} sources={sources} />)}</div>
            </div>
          ))}
        </section>
      )}

      {[...(state.notes ?? []), ...(local?.notes ?? [])].map((n) => <p key={n} className="note">{n}</p>)}
      <p className="note">Data checked against the sources on {local?.retrieved ?? state.retrieved}.</p>
    </div>
  );
}
