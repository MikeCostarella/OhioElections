"""Helpers that turn a county spec + the SoS place summary into an OhioElections ballot file.

Place summaries (places/<county>.json) come from the county's SoS voter file in its
*CountyVoters repo: for every city / village / township (by voter residence), the
congressional, state rep, state senate and school districts its voters are in.
"""
import json, re, os

SMALL = {"of", "on", "the", "and"}
SPECIAL = {"HTS": "Heights", "ST": "St.", "TWP": "Township"}


def tc(word: str) -> str:
    if word.upper() in SPECIAL:
        return SPECIAL[word.upper()]
    if re.match(r"^MC[A-Z]", word):
        return "Mc" + word[2:].capitalize()
    return "-".join(w.capitalize() if w.lower() not in SMALL else w.lower() for w in word.split("-"))


def display(raw: str, typed=True) -> str:
    """'AUSTINTOWN TWP' -> 'Austintown Township'; 'GENEVA-ON-THE-LAKE VILLAGE' -> 'Geneva-on-the-Lake Village'."""
    words = raw.strip().split()
    out = " ".join(tc(w) for w in words)
    out = out[0].upper() + out[1:]
    return out


class County:
    def __init__(self, slug, name, fips):
        self.slug, self.name, self.fips = slug, name, fips
        self.raw = json.load(open(os.path.join(os.path.dirname(__file__), "places", f"{slug}.json")))
        self.raw.pop("?", None)
        self.names = {r: display(r) for r in self.raw}
        self.places = sorted(self.names.values())
        self.sources = {}
        self.contests = []
        self.issues = []
        self.notes = []
        self.links = []
        self.results_links = []

    # --- place lookups -------------------------------------------------
    def p(self, *raws):
        """Display names for raw SoS place names; every one must exist."""
        out = []
        for r in raws:
            if r not in self.raw:
                raise KeyError(f"{self.slug}: no place {r!r}")
            out.append(self.names[r])
        return out

    def where(self, field, value):
        return sorted(self.names[r] for r, v in self.raw.items() if v.get(field, {}).get(value))

    def district(self, kind, num):
        field = {"cong": "CONGRESSIONAL_DISTRICT", "rep": "STATE_REPRESENTATIVE_DISTRICT", "sen": "STATE_SENATE_DISTRICT"}[kind]
        vals = {f"{int(num):02d}", str(int(num))}
        return sorted({self.names[r] for r, v in self.raw.items() for x in vals if v.get(field, {}).get(x)})

    def sd(self, name):
        out = set()
        for r, v in self.raw.items():
            for k in ("CITY_SCHOOL_DISTRICT", "LOCAL_SCHOOL_DISTRICT", "EXEMPTED_VILL_SCHOOL_DISTRICT"):
                if v.get(k, {}).get(name):
                    out.add(self.names[r])
        if not out:
            raise KeyError(f"{self.slug}: no voters in school district {name!r}")
        return sorted(out)

    def all_districts(self, kind):
        field = {"cong": "CONGRESSIONAL_DISTRICT", "rep": "STATE_REPRESENTATIVE_DISTRICT", "sen": "STATE_SENATE_DISTRICT"}[kind]
        return sorted({int(x) for v in self.raw.values() for x in v.get(field, {})})

    # --- builders ------------------------------------------------------
    def src(self, key, label, url):
        self.sources[key] = {"label": label, "url": url}

    def contest(self, id, group, office, cands, detail=None, places=None, area=None, src=None, coverage=None):
        c = {"id": id, "group": group, "office": office}
        if detail:
            c["detail"] = detail
        if places is not None:
            if set(places) == set(self.places):
                places = None
            else:
                c["area"] = area or ", ".join(places)
                c["places"] = places
        if coverage:
            c["coverage"] = coverage
        c["candidates"] = [cand(*x) if isinstance(x, tuple) else cand(x) for x in cands]
        c["sources"] = src or list(self.sources)[:1]
        self.contests.append(c)

    def issue(self, id, kind, jurisdiction, title, places, area=None, src=None, **kw):
        q = {"id": id, "kind": kind, "jurisdiction": jurisdiction, "title": title, "area": area or jurisdiction}
        if places == "county":
            pass
        elif places is None:
            q["coverage"] = "unknown"
        else:
            q["places"] = sorted(set(places))
        for k, v in kw.items():
            if v not in (None, ""):
                q[k] = v
        q["sources"] = src or [list(self.sources)[-1]]
        self.issues.append(q)

    def levy(self, id, jurisdiction, places, type, purpose, mills, term, firstDue=None, estimate=None, number=None, area=None, src=None, note=None, text=None):
        lv = {k: v for k, v in dict(type=type, purpose=purpose, mills=mills, term=term, firstDue=firstDue, estimate=estimate).items() if v}
        title = f"Tax levy ({type.lower()}): {purpose.rstrip('.')}"
        self.issue(id, "levy", jurisdiction, title, places, area=area, src=src, levy=lv, number=number, note=note, text=text)

    def write(self, out_dir, election="2026-11-03", retrieved="2026-10-30"):
        ids = [x["id"] for x in self.contests + self.issues]
        dup = {i for i in ids if ids.count(i) > 1}
        assert not dup, dup
        doc = {
            "scope": "county", "county": self.name, "fips": self.fips, "election": election, "retrieved": retrieved,
            "notes": self.notes, "places": self.places, "sources": self.sources, "links": self.links,
            "results": {"status": "upcoming", "links": self.results_links},
            "contests": self.contests, "issues": self.issues,
        }
        os.makedirs(os.path.join(out_dir, self.slug), exist_ok=True)
        path = os.path.join(out_dir, self.slug, f"{election}.json")
        json.dump(doc, open(path, "w"), indent=2, ensure_ascii=False)
        return path, len(self.contests), len(self.issues)


def cand(name, party=None, note=None):
    return {k: v for k, v in dict(name=name, party=party, note=note).items() if v}


NOTE_ORDER = ("Candidates are listed alphabetically by last name, not in ballot order: Ohio rotates the order of names "
              "from precinct to precinct. Certified write-in candidates are not printed on the ballot and are not listed.")
NOTE_PLACES = ("\"Where you live\" uses the state voter file: a district or school levy is shown for a city, village or "
               "township when any of its voters live in that district. Your exact ballot depends on your precinct.")
NOTE_UNKNOWN = ("Issues marked \"boundaries not mapped\" are for special districts (park, ambulance or similar) whose "
                "boundaries are not in the voter file; they stay listed for every place.")
