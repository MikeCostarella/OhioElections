"""Mahoning County: the Board posts a tabulator Summary Results Report PDF in its Document Center
("Final Unofficial" on election night; https://vote.mahoningcountyoh.gov/DocumentCenter/View/2678/Final-Unofficial).
The document number changes per election — check the Board's home page for the current link.

    python mahoning.py                      # fetch the PDF and parse it
    python mahoning.py --pdf summary.pdf
    python mahoning.py --text dump.txt      # a pdfjs-dump.js text dump (see README)

Layout notes: titles are prefixed "For"; there are no "Total Votes Cast" rows (lib sums the rows);
the five "Judge of the Court of Common Pleas" blocks are told apart by their candidates (lib does
that when a title maps to nothing).
"""
from __future__ import annotations

import re
import sys

import lib

COUNTY, SLUG, ELECTION = "Mahoning", "mahoning", "2026-11-03"
URL = "https://vote.mahoningcountyoh.gov/DocumentCenter/View/2678/Final-Unofficial"
SOURCE = {"label": "Mahoning County Board of Elections: Summary Results Report (final unofficial)", "url": URL}

# Report title (regex, case-insensitive) -> ballot id; lib.IGNORE skips a block the ballot file doesn't carry.
# Titles not listed here (the judges) are matched by their candidates.
TITLES: list[tuple[str, str]] = [
    # statewide
    (r"^For Governor and Lieutenant Governor", "governor"),
    (r"^For Attorney General", "attorney-general"),
    (r"^For Auditor of State", "auditor-of-state"),
    (r"^For Secretary of State", "secretary-of-state"),
    (r"^For Treasurer of State", "treasurer-of-state"),
    (r"^For U\.?S\.? Senator", "us-senate"),
    (r"^Issue 3 - Require Voter ID", "state-issue-3"),
    # county and district
    (r"^For Representative to Congress 6th", "congress-6"),
    (r"^For Representative to Congress 14th", "congress-14"),
    (r"^For State Senator", "senate-33"),
    (r"^For State Representative 58th", "rep-58"),
    (r"^For State Representative 59th", "rep-59"),
    (r"^For County Commissioner", "commissioner"),
    (r"^For County Auditor", "auditor"),
    # levies
    (r"^Issue 4 - Mahoning County Board Develop", "mcbdd"),
    (r"^Canfield City renewal of \.35 mills for police", "canfield-police"),
    (r"^Austintown Township renewal of 0\.8 mill for parks", "austintown-parks"),
    (r"^Austintown Township renewal of 0\.5 mill for senior", "austintown-seniors"),
    (r"^Boardman Township additional of 2\.75 mills for police and fire", "boardman-safety"),
    (r"^Poland Township renewal of 2 mills for roads", "poland-twp-roads"),
    (r"^Springfield Township renewal of 1\.5 mills for fire", "springfield-fire"),
    (r"^Springfield Township renewal of 1\.5 mills for current expenses", "springfield-current"),
    (r"^New Middletown Village renewal of 1\.5 mills for roads", "new-middletown-roads"),
    (r"^Poland Village renewal of 1 mill for police", "poland-village-police"),
    (r"^Boardman Schools renewal of 3\.72 mills", "boardman-lsd"),
    (r"^Canfield Schools additional tax of 5\.9 mills", "canfield-lsd"),
    (r"^Lowellville Schools renewal of 4 mills", "lowellville-lsd"),
    (r"^Poland Schools renewal of 3\.57 mills for emergency", "poland-lsd-emergency"),
    (r"^Poland Schools renewal of 1 mill for permanent", "poland-lsd-pi"),
    (r"^West Branch Schools additional tax of 1 mills", "west-branch-lsd"),
    (r"^Fairfield Township \(Renewal\) of 1\.6 mills", "fairfield-twp-roads"),
    (r"^Perry Township \(Additional Tax\) for 1\.5 mills for Police", "perry-twp-police"),
    (r"^Salem City \(Renewal\) 1\.3 mills for Recreational", "salem-rec"),
    (r"^Alliance Schools renewal of 2 mills for buildings", "alliance-csd"),
    # liquor options (precinct code first, as the Board titles them)
    (r"^YGN2 D - Local Option for Sunday Sales at Lorenzino", "liquor-yo-2d-lorenzinos"),
    (r"^YGN6 H Weekly sales Gateway Gas Mart", "liquor-yo-6h-gateway-weekly"),
    (r"^YGN6 H Sunday sales for Gateway Gas Mart", "liquor-yo-6h-gateway-sunday"),
    (r"^CMP3 B - Sunday sales 12st St\. Party Shop", "liquor-campbell-3b-12th"),
    (r"^AUS 17 Local Option Sunday Sales", "liquor-aust-17-rulli"),
    (r"^BDM 25 Local Option Sunday Sales Rulli Brothers", "liquor-board-25-rulli"),
    (r"^BDM 9 Local Option for weekly sales Tobacco City", "liquor-board-9-tobacco"),
    (r"^BDM 9 \(Sunday Sales\) Tobacco City", lib.IGNORE),        # the ballot file lists Tobacco City once
    (r"^BDM 9 \(Weekly\) Indian Grocery Store", "liquor-board-9-singh"),
    (r"^BDM 9 \(Sunday Stores\) Indian Store", lib.IGNORE),       # the ballot file lists Singh & 3 Brothers once
    (r"^BDM 15 \(Sunday Sales\) Millionaire Express", "liquor-board-15-millionaire"),
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
