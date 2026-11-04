export interface Election {
  id: string;
  label: string;
  /** YYYY-MM-DD */
  date: string;
  type: "general" | "primary" | "special";
}

export interface Source {
  label: string;
  url: string;
}

export interface Link {
  label: string;
  url: string;
}

export interface Candidate {
  name: string;
  /** As printed by the Board (DEM, REP, LIB, ...). Absent for nonpartisan races. */
  party?: string;
  /** The Board's own annotation, verbatim in substance. */
  note?: string;
}

export interface Contest {
  id: string;
  group: string;
  office: string;
  detail?: string;
  /** Where it is on the ballot, as the Board words it. */
  area?: string;
  /** Places (cities / villages / townships) whose voters see it; absent = everyone in scope. */
  places?: string[];
  coverage?: Coverage;
  candidates: Candidate[];
  sources: string[];
}

export interface Levy {
  type?: string;
  purpose: string;
  mills?: string;
  term?: string;
  firstDue?: string;
  /** "$812,524 a year; $82 for each $100,000 of market value", as the Board states it. */
  estimate?: string;
}

/** "unknown": a special district (park, ambulance, county council...) whose boundaries are not in the voter file. */
export type Coverage = "unknown";

export type IssueKind = "state" | "levy" | "question" | "liquor";

export interface Issue {
  id: string;
  kind: IssueKind;
  number?: string;
  jurisdiction: string;
  title: string;
  /** Precincts covered, as the Board lists them. */
  area: string;
  places?: string[];
  coverage?: Coverage;
  levy?: Levy;
  text?: string;
  bullets?: string[];
  yesNo?: string;
  note?: string;
  sources: string[];
}

export interface Results {
  status: "upcoming" | "unofficial" | "official";
  links: Link[];
}

/* ---- Election-night / certified totals: data/results/<county>/<election>.json ----
   Kept apart from the ballot file so the ballot stays stable while totals change every few minutes. */

export type ResultsStatus = "unofficial" | "official";

export interface CandidateResult {
  /** The ballot file's candidate name when the tabulator's name could be matched to it; else the Board's name as printed. */
  name: string;
  votes: number;
  /** Set when the tabulator's name did not match a ballot candidate (shown as printed). */
  unmatched?: true;
}

export interface ContestResult {
  /** Total votes cast in the contest, as the Board reports it. */
  total: number;
  writeIn?: number;
  candidates: CandidateResult[];
  /** In the statewide file only: each county's numbers, by county slug. */
  counties?: Record<string, { total: number; candidates: CandidateResult[] }>;
}

export interface IssueResult {
  total: number;
  yes: number;
  no: number;
  /** The Board's wording: "FOR THE TAX LEVY" / "AGAINST THE TAX LEVY", "YES" / "NO"... */
  yesLabel?: string;
  noLabel?: string;
  /** In the statewide file only: each county's numbers, by county slug. */
  counties?: Record<string, { total: number; yes: number; no: number }>;
}

export interface ResultsFile {
  scope: "county" | "state";
  county?: string;
  election: string;
  status: ResultsStatus;
  /** ISO 8601 with offset: when the Board's report was produced. */
  asOf: string;
  /** What is counted so far, as the Board words it: "Absentee and early", "Election Day", ... */
  stage?: string;
  source: Link;
  precincts?: { reporting: number; total: number; partial?: number; absenteeReporting?: number };
  registered?: number;
  ballotsCast?: number;
  /** Per cent, e.g. 22.45 */
  turnout?: number;
  contests: Record<string, ContestResult>;
  issues: Record<string, IssueResult>;
  /** Report titles the tool could not map to a ballot id (so they can be added to the map). */
  unmatched?: string[];
}

export interface Ballot {
  scope: "state" | "county";
  county?: string;
  fips?: string;
  election: string;
  retrieved: string;
  notes?: string[];
  places?: string[];
  sources: Record<string, Source>;
  links?: Link[];
  results?: Results;
  contests: Contest[];
  issues: Issue[];
}

/** Which counties have local ballot data loaded, per election id. */
export type CountyIndex = Record<string, string[]>;
