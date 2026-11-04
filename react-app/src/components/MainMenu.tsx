import { useEffect, useRef, useState, type ReactNode } from "react";
import type { County } from "../data/counties";
import { votersUrl } from "../data/counties";

export type AppView = "ballot" | "results" | "reports" | "about";
export const VIEW_LABELS: Record<AppView, string> = {
  ballot: "On the ballot",
  results: "Results",
  reports: "Reports",
  about: "About this app",
};

const GITHUB_REPO_URL = "https://github.com/MikeCostarella/OhioElections";
const MY_WEBSITE_URL = "https://mikecostarella.github.io/MyWebSite/";
const COUNTIES_HUB_URL = "https://mikecostarella.github.io/OhioCounties/";
const ELECTION_STATS_URL = "https://mikecostarella.github.io/CurrentElectionStatistics/";

interface Props {
  view: AppView;
  onViewChange: (v: AppView) => void;
  county: County | null;
  onChooseCounty: () => void;
}

/**
 * The fleet's hamburger accordion menu: View, County (this county's other
 * fleet apps), Links. Opens on click; closes on outside click or Escape.
 */
export default function MainMenu({ view, onViewChange, county, onChooseCounty }: Props) {
  const [open, setOpen] = useState(false);
  const [collapsed, setCollapsed] = useState<Set<string>>(() => new Set(["Links"]));
  const ref = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (!open) return;
    const onDocMouseDown = (e: MouseEvent) => { if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false); };
    const onKey = (e: KeyboardEvent) => { if (e.key === "Escape") setOpen(false); };
    document.addEventListener("mousedown", onDocMouseDown);
    document.addEventListener("keydown", onKey);
    return () => { document.removeEventListener("mousedown", onDocMouseDown); document.removeEventListener("keydown", onKey); };
  }, [open]);

  const toggleSection = (name: string) =>
    setCollapsed((prev) => { const next = new Set(prev); if (next.has(name)) next.delete(name); else next.add(name); return next; });

  const Section = ({ title, children }: { title: string; children: ReactNode }) => {
    const isOpen = !collapsed.has(title);
    return (
      <>
        <button type="button" className="menu-section-label menu-section-toggle" aria-expanded={isOpen} onClick={() => toggleSection(title)}>
          <span>{title}</span>
          <span className="menu-chevron" aria-hidden="true">{isOpen ? "▾" : "▸"}</span>
        </button>
        {isOpen && children}
      </>
    );
  };

  return (
    <div id="main-menu" ref={ref}>
      <button id="main-menu-btn" type="button" aria-label="Menu" aria-haspopup="true" aria-expanded={open} onClick={() => setOpen((o) => !o)}>
        <span className="menu-bars" aria-hidden="true"><span /><span /><span /></span>
      </button>
      {open && (
        <div id="main-menu-dropdown" role="menu">
          <Section title="View">
            {(Object.keys(VIEW_LABELS) as AppView[]).map((v) => (
              <button key={v} type="button" role="menuitemradio" aria-checked={view === v} disabled={!county && v !== "about"}
                className={`menu-item${view === v && county ? " active" : ""}`} onClick={() => { onViewChange(v); setOpen(false); }}>
                {VIEW_LABELS[v]}
              </button>
            ))}
            <button type="button" className="menu-item" role="menuitem" onClick={() => { onChooseCounty(); setOpen(false); }}>Choose a county…</button>
          </Section>
          {county && (
            <Section title={`${county.name} County`}>
              <a className="menu-item menu-link" role="menuitem" href={votersUrl(county)} target="_blank" rel="noopener noreferrer">{county.name} County Voters ↗</a>
            </Section>
          )}
          <Section title="Links">
            <a className="menu-item menu-link" role="menuitem" href={COUNTIES_HUB_URL} target="_blank" rel="noopener noreferrer">Ohio Counties hub ↗</a>
            <a className="menu-item menu-link" role="menuitem" href={ELECTION_STATS_URL} target="_blank" rel="noopener noreferrer">Current Election Statistics ↗</a>
            <a className="menu-item menu-link" role="menuitem" href={MY_WEBSITE_URL} target="_blank" rel="noopener noreferrer">All my projects ↗</a>
            <a className="menu-item menu-link" role="menuitem" href={GITHUB_REPO_URL} target="_blank" rel="noopener noreferrer">Source on GitHub ↗</a>
          </Section>
        </div>
      )}
    </div>
  );
}
