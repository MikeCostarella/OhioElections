"""Shared code for turning a Board of Elections' election-night report into
react-app/public/data/results/<county>/<election>.json.

The first (and so far only) report format is the tabulator "Summary Results Report" that
Trumbull County posts as a PDF: a STATISTICS block, then one block per contest —

    Governor and Lieutenant Governor
    Vote For 1
    TOTAL  VOTE %
    DEM Amy Acton and David Pepper   18,033   62.20%
    ...
    Write-In Totals                      30    0.10%
    Total Votes Cast                 28,990  100.00%

The parser works on plain text lines. It accepts either a PDF (read with pdfplumber) or a
text dump made in Chrome with pdfjs-dump.js (lines joined with " | "), because most Board
sites refuse plain HTTP clients but open fine in a browser.
"""
from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime
from typing import Callable, Iterable

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATA = os.path.join(ROOT, "react-app", "public", "data")
# What a county's title_map returns for a report block that is deliberately left out (an option the
# ballot file doesn't carry): listed under "skipped" instead of "unmatched".
IGNORE = "-"
PARTIES = ("DEM", "REP", "LIB", "GRN", "OTHER", "OPC", "NON", "IND", "NP")

NUM = r"-?[\d,]+"
# "DEM Amy Acton and David Pepper | 18,033 | 62.20%" (pdf.js dump, cells joined with " | ") or
# "DEM Amy Acton and David Pepper 18,033 62.20%" (pdfplumber). Without a per cent — "For the Tax Levy | 0",
# nobody has voted yet — the pipe is required, or a title ending in a number ("AUS 17") would read as a row.
ROW = re.compile(rf"^(?P<name>.*?[^\d,|\s].*?)(?:\s*\|\s*(?P<votes>{NUM})(?:\s*\|\s*(?P<pct>[\d.]+)%)?|\s+(?P<votes2>{NUM})\s+(?P<pct2>[\d.]+)%)\s*$")
# A wrapped row: the name on one line, the numbers alone on the next ("37,482 | 42.30%").
NUMS_ONLY = re.compile(rf"^(?P<votes>{NUM})\s*\|?\s*(?P<pct>[\d.]+)%\s*$")
TITLE_SKIP = re.compile(r"^(SUMMARY RESULTS REPORT|GENERAL ELECTION|PRIMARY ELECTION|SPECIAL ELECTION|NOVEMBER|MAY|AUGUST|MARCH|.*\bPage \d+ of\b|=== PAGE|TOTAL\s*\|?\s*VOTE %)")

YES_WORDS = re.compile(r"^(YES|FOR THE |FOR |APPROVAL|SHALL .* BE APPROVED)", re.I)
NO_WORDS = re.compile(r"^(NO$|NO\b|AGAINST|REJECTION)", re.I)


def clean_line(s: str) -> str:
    """Normalise whitespace; keep the " | " cell separators of a pdf.js dump."""
    return re.sub(r"\s+", " ", s).strip()


def unpipe(s: str) -> str:
    return re.sub(r"\s*\|\s*", " ", s).strip()


def to_int(s: str) -> int:
    return int(s.replace(",", ""))


# ---------------------------------------------------------------- reading the report

def lines_from_pdf(path: str) -> list[str]:
    import pdfplumber  # only needed for PDFs

    out: list[str] = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            out.extend(text.splitlines())
    return out


def lines_from_text(path: str) -> list[str]:
    with open(path, encoding="utf-8") as f:
        return f.read().splitlines()


def read_report(path: str) -> list[str]:
    return lines_from_pdf(path) if path.lower().endswith(".pdf") else lines_from_text(path)


# ---------------------------------------------------------------- parsing

class Block:
    """One contest or issue in the report: its title and its rows (name, votes)."""

    def __init__(self, title: str):
        self.title = title
        self.rows: list[tuple[str, int]] = []
        self.total = 0
        self.write_in = 0

    def __repr__(self) -> str:
        return f"<{self.title}: {self.rows} total={self.total}>"


class Report:
    def __init__(self) -> None:
        self.blocks: list[Block] = []
        self.stats: dict[str, str] = {}
        self.stage: str | None = None
        self.unofficial = True
        self.report_time: datetime | None = None


def parse_summary_report(raw_lines: Iterable[str]) -> Report:
    """Walks the report line by line. Layouts seen so far:
    Trumbull — STATISTICS block, "Total Votes Cast" closes each contest, one-line titles.
    Mahoning — "Statistics", no total rows (total = sum of rows + write-ins), titles prefixed "For",
    a long candidate name wrapped as name / numbers / rest-of-name, duplicate judge titles."""
    rep = Report()
    block: Block | None = None
    pending: str | None = None     # a title (before "Vote For") or a wrapped candidate name (before its numbers)
    wrapped_last = False           # the last row's name was wrapped: a bare text line next is its continuation
    in_stats = False
    for raw in raw_lines:
        line = clean_line(raw)
        if not line or line.upper() == "TOTAL":
            continue
        up = line.upper()
        if "OFFICIAL RESULTS" in up or "FINAL UNOFFICIAL" in up:
            rep.unofficial = "UNOFFICIAL" in up
        if up.startswith("GENERAL ELECTION") or up.startswith("PRIMARY ELECTION") or up.startswith("SPECIAL ELECTION"):
            rest = unpipe(line).split(" ", 2)[2:]  # e.g. "ABSENTEE AND EARLY"
            if rest and rest[0].strip():
                rep.stage = rest[0].strip().capitalize()
            continue
        m = re.search(r"Election Summary - (\d{2}/\d{2}/\d{4} \d{2}:\d{2}[AP]M)", line)
        if m:
            t = datetime.strptime(m.group(1), "%m/%d/%Y %I:%M%p")
            if rep.report_time is None or t > rep.report_time:
                rep.report_time = t
            continue
        if TITLE_SKIP.match(line):
            continue
        if up == "STATISTICS":
            in_stats = True
            block = None
            pending = None
            continue
        if in_stats:
            m = re.match(r"^(.+?)\s+(\d[\d,]*(?: of \d+)?|[\d.]+%)$", unpipe(line))
            if m:
                rep.stats[m.group(1).strip()] = m.group(2)
                continue
            in_stats = False  # first contest title ends the block
        if re.match(r"^Vote For \d+$", line, re.I):
            if pending:
                block = Block(unpipe(pending))
                rep.blocks.append(block)
                pending = None
            wrapped_last = False
            continue
        if block is not None:
            m = NUMS_ONLY.match(line)
            if m and pending:  # the numbers of a wrapped candidate name
                block.rows.append((unpipe(pending), to_int(m.group("votes"))))
                pending = None
                wrapped_last = True
                continue
            m = ROW.match(line)
            if m:
                name = unpipe(m.group("name"))
                votes = to_int(m.group("votes") or m.group("votes2"))
                low = name.lower()
                if low.startswith("total votes cast"):
                    block.total = votes
                    block = None
                elif low.startswith("write-in"):
                    block.write_in = votes
                elif low.startswith("not assigned"):
                    pass  # write-in votes not yet assigned to a named write-in candidate
                else:
                    block.rows.append((name, votes))
                pending = None
                wrapped_last = False
                continue
            if wrapped_last and block.rows and not pending:  # "McColley": the rest of the wrapped name
                n, v = block.rows[-1]
                block.rows[-1] = (f"{n} {n and ' ' or ''}{line}".replace("  ", " "), v)
                wrapped_last = False
                continue
            pending = line  # a wrapped candidate name, or the next contest's title
            wrapped_last = False
            continue
        # Between blocks: (the start of) a contest title; a title can wrap onto two lines.
        pending = f"{pending} {line}" if pending else line
    for b in rep.blocks:
        b.title = unpipe(b.title)  # reports without "Total Votes Cast" rows
        if not b.total:
            b.total = sum(v for _, v in b.rows) + b.write_in
    return rep


# ---------------------------------------------------------------- matching to the ballot

def strip_party(name: str) -> tuple[str | None, str]:
    for p in PARTIES:
        if name.startswith(p + " "):
            return p, name[len(p) + 1:].strip()
    return None, name


def last_name(person: str) -> str:
    person = re.sub(r"\s*\(.*?\)", "", person)
    person = re.split(r",", person)[0]
    parts = [w for w in re.split(r"\s+", person.strip()) if w and not re.match(r"^(Jr\.?|Sr\.?|II|III|IV)$", w, re.I)]
    return re.sub(r"[^a-z]", "", parts[-1].lower()) if parts else ""


def first_person(name: str) -> str:
    return re.split(r"\s+and\s+|\s*/\s*", name)[0]


def match_candidate(report_name: str, ballot_names: list[str]) -> str | None:
    """The ballot's name for a report row, by the first person's last name (tickets print
    "A and B" in the report and "A / B" on the ballot; the tabulator also truncates long names)."""
    _, bare = strip_party(report_name)
    ln = last_name(first_person(bare))
    hits = [b for b in ballot_names if last_name(first_person(b)) == ln]
    if len(hits) == 1:
        return hits[0]
    if len(hits) > 1:  # same last name twice: use first name too
        fn = re.sub(r"[^a-z]", "", first_person(bare).split()[0].lower())
        hits2 = [b for b in hits if re.sub(r"[^a-z]", "", first_person(b).split()[0].lower()) == fn]
        if len(hits2) == 1:
            return hits2[0]
    return None


def yes_no(rows: list[tuple[str, int]]) -> tuple[tuple[str, int], tuple[str, int]] | None:
    if len(rows) != 2:
        return None
    a, b = rows
    if YES_WORDS.match(a[0]) and NO_WORDS.match(b[0]):
        return a, b
    if YES_WORDS.match(b[0]) and NO_WORDS.match(a[0]):
        return b, a
    return None


def build_results(
    *,
    county: str,
    slug: str,
    election: str,
    report: Report,
    source: dict,
    title_map: Callable[[str], str | None],
    tz: str = "-05:00",
) -> dict:
    """Turn a parsed report into the results JSON, matched to the county's ballot files."""
    with open(os.path.join(DATA, "state", f"{election}.json"), encoding="utf-8") as f:
        state = json.load(f)
    with open(os.path.join(DATA, "county", slug, f"{election}.json"), encoding="utf-8") as f:
        local = json.load(f)
    contests = {c["id"]: c for c in state["contests"] + local["contests"]}
    issues = {i["id"]: i for i in state["issues"] + local["issues"]}

    out_contests: dict = {}
    out_issues: dict = {}
    unmatched: list[str] = []
    skipped: list[str] = []

    def by_candidates(b: Block) -> str | None:
        """For a title the map doesn't settle (five "Judge of the Court of Common Pleas" blocks): the one
        unused contest whose candidates' last names cover every row of the block."""
        hits = []
        for cid, c in contests.items():
            if cid in out_contests:
                continue
            names = [k["name"] for k in c["candidates"]]
            if b.rows and all(match_candidate(n, names) for n, _ in b.rows) and len(b.rows) == len(names):
                hits.append(cid)
        return hits[0] if len(hits) == 1 else None

    for b in report.blocks:
        cid = title_map(b.title)
        if cid == IGNORE:
            skipped.append(b.title)
            continue
        if cid is None:
            cid = by_candidates(b)
        if cid is None:
            unmatched.append(b.title)
            continue
        if cid in issues:
            yn = yes_no(b.rows)
            if yn is None:
                unmatched.append(f"{b.title} (issue rows not yes/no: {[r[0] for r in b.rows]})")
                continue
            (yl, yv), (nl, nv) = yn
            out_issues[cid] = {"total": b.total, "yes": yv, "no": nv, "yesLabel": yl.capitalize(), "noLabel": nl.capitalize()}
        elif cid in contests:
            names = [k["name"] for k in contests[cid]["candidates"]]
            cands = []
            for name, votes in b.rows:
                m = match_candidate(name, names)
                cands.append({"name": m, "votes": votes} if m else {"name": strip_party(name)[1], "votes": votes, "unmatched": True})
            rec: dict = {"total": b.total, "candidates": cands}
            if b.write_in:
                rec["writeIn"] = b.write_in
            out_contests[cid] = rec
        else:
            unmatched.append(f"{b.title} -> {cid} (id not in ballot)")

    st = report.stats
    def of(key: str) -> tuple[int, int] | None:
        v = st.get(key)
        m = re.match(r"^(\d[\d,]*) of (\d+)$", v or "")
        return (to_int(m.group(1)), int(m.group(2))) if m else None

    res: dict = {
        "scope": "county",
        "county": county,
        "election": election,
        "status": "unofficial" if report.unofficial else "official",
        "asOf": (report.report_time or datetime.now()).strftime("%Y-%m-%dT%H:%M:%S") + tz,
        "source": source,
    }
    if report.stage and report.unofficial:
        res["stage"] = report.stage
    eday = of("Election Day Precincts Reporting")
    if eday:
        p = {"reporting": eday[0], "total": eday[1]}
        part = of("Precincts Partially Reported")
        if part and part[0]:
            p["partial"] = part[0]
        absent = of("Absentee/ Early Precincts Reporting") or of("Absentee/Early Precincts Reporting")
        if absent:
            p["absenteeReporting"] = absent[0]
        res["precincts"] = p
    for key, field in (("Registered Voters - Total", "registered"), ("Ballots Cast - Total", "ballotsCast")):
        if key in st and re.match(r"^[\d,]+$", st[key]):
            res[field] = to_int(st[key])
    if "Voter Turnout - Total" in st:
        res["turnout"] = float(st["Voter Turnout - Total"].rstrip("%"))
    res["contests"] = out_contests
    res["issues"] = out_issues
    if skipped:
        res["skipped"] = skipped
    if unmatched:
        res["unmatched"] = unmatched
    return res


def write_results(res: dict, slug: str) -> str:
    d = os.path.join(DATA, "results", slug)
    os.makedirs(d, exist_ok=True)
    path = os.path.join(d, f"{res['election']}.json")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(res, f, indent=2, ensure_ascii=False)
        f.write("\n")
    return path


def summary(res: dict) -> str:
    p = res.get("precincts") or {}
    s = [f"{res['county']} {res['election']} {res['status']} as of {res['asOf']}"]
    if p:
        s.append(f"precincts {p.get('reporting')}/{p.get('total')}")
    s.append(f"{len(res['contests'])} contests, {len(res['issues'])} issues")
    if res.get("unmatched"):
        s.append(f"UNMATCHED: {res['unmatched']}")
    return " · ".join(s)


def fetch(url: str, dest: str) -> bool:
    """Download a report. Boards' sites often refuse non-browser clients; the caller falls back to a
    file (--pdf / --text) when this returns False."""
    try:
        import urllib.request

        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (OhioElections results poller; mikecostarella.github.io/OhioElections)"})
        with urllib.request.urlopen(req, timeout=30) as r, open(dest, "wb") as f:
            f.write(r.read())
        return os.path.getsize(dest) > 1000
    except Exception as e:  # noqa: BLE001
        print(f"fetch failed: {url}: {e}", file=sys.stderr)
        return False
