import { useEffect, useMemo, useState } from "react";
import BuildStamp from "./components/BuildStamp";
import MainMenu, { VIEW_LABELS, type AppView } from "./components/MainMenu";
import BallotView from "./components/BallotView";
import ResultsView from "./components/ResultsView";
import About from "./components/About";
import CountyPicker from "./components/CountyPicker";
import { COUNTIES, countyBySlug, votersUrl } from "./data/counties";
import { daysUntil, loadCountyBallot, loadCountyIndex, loadElections, loadStateBallot, longDate } from "./data/load";
import type { Ballot, CountyIndex, Election } from "./data/types";

const ELECTION_STATS_URL = "https://mikecostarella.github.io/CurrentElectionStatistics/";
const COUNTIES_HUB_URL = "https://mikecostarella.github.io/OhioCounties/";

/**
 * Routes live in the hash so other fleet apps can deep-link:
 *   #/                                  county picker
 *   #/about                             about page
 *   #/<county>[/<election>[/<view>[/<place>]]]
 * e.g. #/trumbull/2026-11-03/ballot/Hubbard%20City
 */
interface Route { slug: string; election: string; view: AppView; place: string }

function parseHash(): Route {
  const parts = location.hash.replace(/^#\/?/, "").split("/").map(decodeURIComponent);
  if (parts[0] === "about") return { slug: "", election: "", view: "about", place: "" };
  const view = (parts[2] as AppView) in VIEW_LABELS ? (parts[2] as AppView) : "ballot";
  return { slug: countyBySlug(parts[0] ?? "") ? parts[0].toLowerCase() : "", election: parts[1] ?? "", view, place: parts[3] ?? "" };
}

function toHash(r: Route): string {
  if (!r.slug) return r.view === "about" ? "#/about" : "#/";
  const segs = [r.slug, r.election, r.view, r.place].filter(Boolean).map(encodeURIComponent);
  return `#/${segs.join("/")}`;
}

export default function App() {
  const [route, setRoute] = useState<Route>(parseHash);
  const [elections, setElections] = useState<Election[]>([]);
  const [index, setIndex] = useState<CountyIndex>({});
  const [state, setState] = useState<Ballot | null>(null);
  const [local, setLocal] = useState<Ballot | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([loadElections(), loadCountyIndex()])
      .then(([e, i]) => { setElections(e); setIndex(i); })
      .catch((e) => setError(String(e)));
    const onHash = () => setRoute(parseHash());
    window.addEventListener("hashchange", onHash);
    return () => window.removeEventListener("hashchange", onHash);
  }, []);

  // Most recent election is the default.
  const election = useMemo(
    () => elections.find((e) => e.id === route.election) ?? [...elections].sort((a, b) => b.date.localeCompare(a.date))[0],
    [elections, route.election],
  );
  const county = route.slug ? countyBySlug(route.slug) ?? null : null;
  const loaded = election ? index[election.id] ?? [] : [];
  const hasLocal = !!county && loaded.includes(county.slug);

  const go = (patch: Partial<Route>) => {
    const next = { ...route, ...patch };
    const h = toHash(next);
    if (h !== location.hash) location.hash = h; else setRoute(next);
  };

  useEffect(() => {
    if (!election) return;
    setState(null);
    loadStateBallot(election.id).then(setState).catch((e) => setError(String(e)));
  }, [election]);

  useEffect(() => {
    setLocal(null);
    if (!election || !county || !hasLocal) return;
    loadCountyBallot(county.slug, election.id).then(setLocal).catch((e) => setError(String(e)));
  }, [election, county, hasLocal]);

  const places = local?.places ?? [];
  const place = places.includes(route.place) ? route.place : "";
  const days = election ? daysUntil(election.date) : null;
  const showPicker = !county && route.view !== "about";

  useEffect(() => {
    document.title = county ? `${county.name} County — Ohio Elections` : "Ohio Elections";
  }, [county]);

  return (
    <div className="app">
      <header className="masthead">
        <div className="masthead-left">
          <MainMenu view={route.view} onViewChange={(v) => go({ view: v })} county={county} onChooseCounty={() => go({ slug: "", place: "", view: "ballot" })} />
          <div>
            <h1>Ohio Elections {county && <span className="state">{county.name} County</span>}</h1>
            <div className="sub">What is on the ballot, county by county, from the Boards of Elections</div>
          </div>
        </div>
        <div className="credit">Created by: Mike Costarella</div>
      </header>

      {election && (
        <div className="stats">
          <label className="pick">County{" "}
            <select value={county?.slug ?? ""} onChange={(e) => go({ slug: e.target.value, place: "", view: route.view === "about" ? "ballot" : route.view })}>
              <option value="">Choose…</option>
              {COUNTIES.map((c) => <option key={c.slug} value={c.slug}>{c.name}{loaded.includes(c.slug) && loaded.length < COUNTIES.length ? " ●" : ""}</option>)}
            </select>
          </label>
          {elections.length > 1 && (
            <label className="pick">Election{" "}
              <select value={election.id} onChange={(e) => go({ election: e.target.value })}>
                {elections.map((e) => <option key={e.id} value={e.id}>{e.label}</option>)}
              </select>
            </label>
          )}
          {places.length > 0 && route.view === "ballot" && (
            <label className="pick">Where you live{" "}
              <select value={place} onChange={(e) => go({ place: e.target.value })}>
                <option value="">All of {county?.name} County</option>
                {places.map((p) => <option key={p} value={p}>{p}</option>)}
              </select>
            </label>
          )}
          <span className="right">
            <b>{election.label}</b> · {longDate(election.date)}
            {days !== null && days > 0 && <> · <b>{days}</b> day{days === 1 ? "" : "s"} away</>}
            {days === 0 && <> · <b>today</b>, polls 6:30 AM–7:30 PM</>}
          </span>
        </div>
      )}

      {county && (
        <nav className="related" aria-label="Related apps">
          <span className="related-label">Related apps</span>
          <a className="related-btn" href={votersUrl(county)} target="_blank" rel="noopener noreferrer">
            <b>{county.name} County Voters ↗</b><span>Who is registered and who voted</span>
          </a>
          <a className="related-btn" href={ELECTION_STATS_URL} target="_blank" rel="noopener noreferrer">
            <b>Election Statistics ↗</b><span>The early vote, statewide</span>
          </a>
          <a className="related-btn" href={COUNTIES_HUB_URL} target="_blank" rel="noopener noreferrer">
            <b>Ohio Counties hub ↗</b><span>Every county app in the fleet</span>
          </a>
        </nav>
      )}

      <main className="body">
        {county && route.view !== "about" && (
          <div className="view-head">
            <h2 className="view-title">{VIEW_LABELS[route.view]}{place ? ` · ${place}` : ""}</h2>
            <div className="view-tabs seg" role="tablist">
              {(["ballot", "results"] as AppView[]).map((v) => (
                <button key={v} type="button" role="tab" aria-selected={route.view === v} className={route.view === v ? "active" : ""} onClick={() => go({ view: v })}>{VIEW_LABELS[v]}</button>
              ))}
            </div>
            <div className="quick-links">
              {(local?.links ?? []).slice(0, 2).map((l) => <a key={l.url} href={l.url} target="_blank" rel="noopener noreferrer">{l.label} ↗</a>)}
            </div>
          </div>
        )}
        {error && <p className="note error">Could not load the data: {error}</p>}
        {showPicker && <CountyPicker loaded={loaded} onPick={(slug) => go({ slug, place: "", view: "ballot" })} />}
        {route.view === "about" && !county && <><h2 className="view-title">{VIEW_LABELS.about}</h2><About loadedCounties={loaded.map((s) => countyBySlug(s)?.name ?? s)} /></>}
        {route.view === "about" && county && <About loadedCounties={loaded.map((s) => countyBySlug(s)?.name ?? s)} />}
        {county && route.view === "ballot" && (state && (!hasLocal || local)
          ? <BallotView county={county} state={state} local={local} place={place} />
          : !error && <p className="note">Loading…</p>)}
        {county && route.view === "results" && election && <ResultsView county={county} election={election} local={local} />}
      </main>
      <BuildStamp />
    </div>
  );
}
