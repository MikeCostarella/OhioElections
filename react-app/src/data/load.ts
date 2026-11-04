import type { Ballot, CountyIndex, Election, ResultsFile } from "./types";

const base = import.meta.env.BASE_URL;

async function getJson<T>(path: string): Promise<T> {
  const r = await fetch(`${base}${path}`);
  if (!r.ok) throw new Error(`${path}: HTTP ${r.status}`);
  return (await r.json()) as T;
}

export const loadElections = () => getJson<Election[]>("data/elections.json");
export const loadCountyIndex = () => getJson<CountyIndex>("data/county/index.json");
export const loadStateBallot = (election: string) => getJson<Ballot>(`data/state/${election}.json`);
export const loadCountyBallot = (slug: string, election: string) => getJson<Ballot>(`data/county/${slug}/${election}.json`);

/**
 * Election-night totals. Null when the county has none yet (404). Always from the network — the file is
 * rewritten every few minutes on election night, so neither the browser cache nor the service worker may answer.
 */
export async function loadResults(slug: string, election: string): Promise<ResultsFile | null> {
  const r = await fetch(`${base}data/results/${slug}/${election}.json?t=${Date.now()}`, { cache: "no-store" });
  if (r.status === 404) return null;
  if (!r.ok) throw new Error(`results/${slug}/${election}: HTTP ${r.status}`);
  return (await r.json()) as ResultsFile;
}

/** Statewide totals (results/state/<election>.json, from the Secretary of State's feed); null when not published yet. */
export async function loadStateResults(election: string): Promise<ResultsFile | null> {
  const r = await fetch(`${base}data/results/state/${election}.json?t=${Date.now()}`, { cache: "no-store" });
  if (r.status === 404) return null;
  if (!r.ok) throw new Error(`results/state/${election}: HTTP ${r.status}`);
  return (await r.json()) as ResultsFile;
}

/** How often the app re-reads the results file while a count is still unofficial. */
export const RESULTS_POLL_MS = 2 * 60 * 1000;

/** "7:36 PM" for the results banner, in the viewer's locale. */
export function shortTime(iso: string): string {
  const d = new Date(iso);
  return isNaN(d.getTime()) ? iso : d.toLocaleTimeString(undefined, { hour: "numeric", minute: "2-digit" });
}

export const fmtInt = (n: number) => n.toLocaleString("en-US");
export const pct = (n: number, total: number) => (total > 0 ? `${((100 * n) / total).toFixed(1)}%` : "");
export const share = (n: number, total: number) => (total > 0 ? (100 * n) / total : 0);

/** "Tuesday, November 3, 2026" from YYYY-MM-DD, without time-zone drift. */
export function longDate(ymd: string): string {
  const [y, m, d] = ymd.split("-").map(Number);
  return new Date(y, m - 1, d).toLocaleDateString(undefined, { weekday: "long", year: "numeric", month: "long", day: "numeric" });
}

/** Days from today (local) to YYYY-MM-DD; negative once it has passed. */
export function daysUntil(ymd: string): number {
  const [y, m, d] = ymd.split("-").map(Number);
  const t = new Date(); t.setHours(0, 0, 0, 0);
  return Math.round((new Date(y, m - 1, d).getTime() - t.getTime()) / 86400000);
}

const lastName = (n: string) => n.split(" / ")[0].replace(/,.*$/, "").trim().split(/\s+/).pop()!.toLowerCase();
/** Ohio rotates ballot order by precinct, so the app lists names alphabetically by last name. */
export const byLastName = <T extends { name: string }>(a: T, b: T) => lastName(a.name).localeCompare(lastName(b.name));

export const SOS = {
  results2026: "https://www.ohiosos.gov/elections/election-results-and-data/2026/",
  boeDirectory: "https://www.ohiosos.gov/elections/county-boards-of-elections-directory/",
  sampleBallot: "https://www.ohiosos.gov/elections/voters/toolkit/sample-ballot/",
};
