import { useState } from "react";
import { COUNTIES } from "../data/counties";

interface Props {
  loaded: string[];
  onPick: (slug: string) => void;
}

/** All 88 counties; any without local ballot data yet are marked "Statewide ballot" and listed last. */
export default function CountyPicker({ loaded, onPick }: Props) {
  const [q, setQ] = useState("");
  const list = COUNTIES.filter((c) => c.name.toLowerCase().includes(q.trim().toLowerCase()));
  return (
    <div className="picker">
      <p className="lead">Choose a county to see what is on its ballot.</p>
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
