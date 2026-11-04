import { useState } from "react";
import { COUNTIES } from "../data/counties";
import { STATE_REPORTS, type StateReportId } from "./StatewideReports";

interface Props {
  loaded: string[];
  onPick: (slug: string) => void;
  /** False until the elections list is loaded. */
  statewide: boolean;
  onStatewide: (report: StateReportId) => void;
}

const STATE_BLURB: Record<StateReportId, string> = {
  results: "Every statewide race and State Issue 3, with the counties each candidate leads",
  counties: "All 88 counties ranked for any race or issue",
  turnout: "Registered, ballots cast and turnout, county by county",
  lean: "How Democratic or Republican each county ran, and how much it split tickets",
};

/** All 88 counties; any without local ballot data yet are marked "Statewide ballot" and listed last. */
export default function CountyPicker({ loaded, onPick, statewide, onStatewide }: Props) {
  const [q, setQ] = useState("");
  const list = COUNTIES.filter((c) => c.name.toLowerCase().includes(q.trim().toLowerCase()));
  return (
    <div className="picker">
      <section className="statewide-panel" aria-labelledby="statewide-title">
        <div className="statewide-head">
          <h2 id="statewide-title">Statewide reports</h2>
          <span className="sub">All 88 counties, from the Secretary of State's election-night feed · every table downloads as CSV</span>
        </div>
        <div className="statewide-grid">
          {STATE_REPORTS.map((r) => (
            <button key={r.id} type="button" className="related-btn" disabled={!statewide} onClick={() => onStatewide(r.id)}>
              <b>{r.label} →</b><span>{STATE_BLURB[r.id]}</span>
            </button>
          ))}
        </div>
      </section>
      <p className="lead">Or choose a county to see what is on its ballot, its results and its own reports.</p>
      <input type="search" className="search" placeholder="Filter counties" value={q} onChange={(e) => setQ(e.target.value)} aria-label="Filter counties" autoFocus />
      <div className="county-grid">
        {[...list].sort((a, b) => Number(loaded.includes(b.slug)) - Number(loaded.includes(a.slug)) || a.name.localeCompare(b.name)).map((c) => (
          <button key={c.fips} type="button" className={`county-btn${loaded.includes(c.slug) ? " full" : ""}`} onClick={() => onPick(c.slug)}>
            {c.name}
            {!loaded.includes(c.slug) && <span className="sub">Statewide ballot</span>}
          </button>
        ))}
      </div>
    </div>
  );
}
