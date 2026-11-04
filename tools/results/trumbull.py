"""Trumbull County: the Board posts a tabulator Summary Results Report as a PDF and overwrites the
same URL through election night (https://boe.co.trumbull.oh.gov/pdfs/Election%20Summary.pdf).

    python trumbull.py                      # fetch the PDF and parse it
    python trumbull.py --pdf summary.pdf    # parse a downloaded PDF
    python trumbull.py --text dump.txt      # parse a pdfjs-dump.js text dump (see README)

Titles in the report are mapped to the ballot ids in react-app/public/data/county/trumbull/.
Anything unmapped is listed under "unmatched" in the output so it can be added to TITLES below.
"""
from __future__ import annotations

import re
import sys

import lib

COUNTY, SLUG, ELECTION = "Trumbull", "trumbull", "2026-11-03"
URL = "https://boe.co.trumbull.oh.gov/pdfs/Election%20Summary.pdf"
SOURCE = {"label": "Trumbull County Board of Elections: Election Summary (unofficial)", "url": URL}

# Report title (regex, case-insensitive) -> ballot id. Order matters: first match wins.
TITLES: list[tuple[str, str]] = [
    # statewide
    (r"^Governor and Lieutenant Governor", "governor"),
    (r"^Attorney General", "attorney-general"),
    (r"^Auditor of State", "auditor-of-state"),
    (r"^Secretary of State", "secretary-of-state"),
    (r"^Treasurer of State", "treasurer-of-state"),
    (r"^U\.?S\.? Senator", "us-senate"),
    (r"^Justice of the Supreme Court FTC 1-1-2027", "supreme-court-2027-01-01"),
    (r"^Justice of the Supreme Court FTC 1-2-2027", "supreme-court-2027-01-02"),
    (r"^State Issue 3", "state-issue-3"),
    # county
    (r"^Representative to Congress 14th", "congress-14"),
    (r"^State Representative 64th", "state-rep-64"),
    (r"^State Representative 65th", "state-rep-65"),
    (r"^11th District Court of Appeals FTC 2-9-2027", "appeals-11-2027-02-09"),
    (r"^11th District Court of Appeals FTC 2-10-2027", "appeals-11-2027-02-10"),
    (r"^Court of Common Pleas General", "common-pleas-general-2027-01-01"),
    (r"^Court of Common Pleas Probate", "common-pleas-probate-2027-02-09"),
    (r"^County Commissioner FTC 1-1-2027", "commissioner-2027-01-01"),
    (r"^County Auditor", "auditor"),
    # school and district levies
    (r"^Cardinal LSD", "cardinal-lsd"),
    (r"^Lakeview LSD", "lakeview-lsd"),
    (r"^Liberty LSD", "liberty-lsd"),
    (r"^Mathews LSD", "mathews-lsd"),
    (r"^Warren CSD", "warren-csd"),
    (r"^Newton Falls JFD", "newton-falls-jfd"),
    (r"^Hubbard Twp Free Park", "harding-park"),
    # cities and villages
    (r"^Hubbard City Proposed Ordinance Data Centers", "hubbard-data-centers"),
    (r"^Lordstown Village Proposed Change in Income Tax", "lordstown-income-tax"),
    (r"^McDonald Village Safety Services", "mcdonald-safety"),
    (r"^Orangeville Village Current Expenses", "orangeville-current"),
    (r"^Warren City Proposed Ordinance Council Pay", "warren-council-pay"),
    (r"^Newton Falls Village Proposed School Zone Photo Traffic", "newton-falls-traffic"),
    # townships
    (r"^Braceville Twp Fire", "braceville-fire"),
    (r"^Braceville Twp Police", "braceville-police"),
    (r"^Braceville Twp Roads", "braceville-roads"),
    (r"^Champion Twp Police", "champion-police"),
    (r"^Farmington Twp Roads", "farmington-roads"),
    (r"^Greene Twp Proposed Zoning", "greene-zoning"),
    (r"^Gustavus Twp Fire", "gustavus-fire"),
    (r"^Hubbard Twp Roads", "hubbard-twp-roads"),
    (r"^Liberty Twp Fire & EMS Renewal 1 mill", "liberty-fire-1"),
    (r"^Liberty Twp Fire & EMS Renewal 2 mills", "liberty-fire-2"),
    (r"^Liberty Twp Police", "liberty-police"),
    (r"^Mesopotamia Twp Fire", "mesopotamia-fire"),
    (r"^Mesopotamia Twp Roads", "mesopotamia-roads"),
    (r"^Newton Twp Natural Gas", "newton-gas"),
    (r"^Southington Twp Electric", "southington-electric"),
    (r"^Southington Twp Natural Gas", "southington-gas"),
    (r"^Vienna Twp Police", "vienna-police"),
    # liquor options ("LO ...")
    (r"^LO Niles City 3C Eastside", "liquor-niles-eastside"),
    (r"^LO Girard City Pct 3A Girard American Legion", "liquor-girard-legion"),
    (r"^LO Cortland City F Casa Angel Sunday Sales", "liquor-cortland-casa-angel-sunday"),
    (r"^LO Cortland City F Casa Angel$", "liquor-cortland-casa-angel"),
    (r"^LO Newton Twp D Duck Creek", "liquor-newton-duck-creek"),
]


def title_map(title: str) -> str | None:
    for pat, cid in TITLES:
        if re.search(pat, title, re.I):
            return cid
    return None


def build(path: str) -> dict:
    report = lib.parse_summary_report(lib.read_report(path))
    return lib.build_results(county=COUNTY, slug=SLUG, election=ELECTION, report=report, source=SOURCE, title_map=title_map)


def main(argv: list[str]) -> int:
    path = None
    if "--pdf" in argv:
        path = argv[argv.index("--pdf") + 1]
    elif "--text" in argv:
        path = argv[argv.index("--text") + 1]
    else:
        path = lib.os.path.join(lib.os.path.dirname(lib.os.path.abspath(__file__)), "downloads", f"{SLUG}.pdf")
        lib.os.makedirs(lib.os.path.dirname(path), exist_ok=True)
        if not lib.fetch(URL, path):
            print("Could not download the report; pass --pdf <file> or --text <file> instead.", file=sys.stderr)
            return 2
    res = build(path)
    out = lib.write_results(res, SLUG)
    print(lib.summary(res))
    print("wrote", out)
    return 1 if res.get("unmatched") else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
