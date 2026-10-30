import type { Ballot, CountyIndex, Election } from "./types";

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
