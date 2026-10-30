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
