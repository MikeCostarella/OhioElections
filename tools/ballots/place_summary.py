"""Summarise a county SoS voter file into places/<county>.json for the ballot generator.

For each city / village / township (by voter residence; Cuyahoga's file has none of those
columns, so its places come from the precinct name, e.g. "PARMA HEIGHTS-04-A"), records the
number of voters and which congressional, state rep, state senate, appeals and school
districts they are in. No personal data is kept: only counts per place.

PowerShell:
  cd C:\\projects\\OhioElections\\tools\\ballots; python place_summary.py ..\\..\\..\\MahoningCountyVoters\\SourceData\\SOS_MAHONING_2026-10-23.txt places\\mahoning.json
"""
import csv, sys, re, collections, json

COLS = ["CITY_SCHOOL_DISTRICT", "LOCAL_SCHOOL_DISTRICT", "EXEMPTED_VILL_SCHOOL_DISTRICT", "CONGRESSIONAL_DISTRICT",
        "STATE_REPRESENTATIVE_DISTRICT", "STATE_SENATE_DISTRICT", "COURT_OF_APPEALS"]

def main(src, dst):
    count = collections.Counter()
    m = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
    with open(src, newline="", encoding="latin-1") as fh:
        for row in csv.DictReader(fh):
            p = row["CITY"] or row["VILLAGE"] or row["TOWNSHIP"]
            if not p:
                mm = re.match(r"^(.*?)-\d+-[A-Z]+$", row["PRECINCT_NAME"].strip())
                p = (mm.group(1) if mm else (row["PRECINCT_NAME"] or "?")).strip()
            count[p] += 1
            for c in COLS:
                if row[c]:
                    m[p][c][row[c]] += 1
            if row["VILLAGE"] and row["TOWNSHIP"]:
                m[p]["TWP_OF_VILLAGE"][row["TOWNSHIP"]] += 1
            if row["CITY"] and row["TOWNSHIP"]:
                m[p]["TWP_OF_CITY"][row["TOWNSHIP"]] += 1
    out = {p: {"voters": n, **{c: dict(m[p][c]) for c in m[p]}} for p, n in sorted(count.items())}
    json.dump(out, open(dst, "w"), indent=1)
    print(f"{len(out)} places -> {dst}")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
