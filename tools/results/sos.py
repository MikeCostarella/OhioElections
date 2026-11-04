"""Ohio Secretary of State election-night reporting ("Ohio Decides", https://liveresults.ohiosos.gov/).

Its JSON API covers every county for the contests the SoS tracks — statewide offices, Supreme Court,
U.S. Senate and House, Court of Appeals, General Assembly and statewide issues — but not county offices
or local issues (those come from each Board's own report, see trumbull.py / mahoning.py).

    python sos.py                 # fetch everything from the API and write the results files
    python sos.py --bundle f.json # read a bundle saved from Chrome with sos-dump.js (if the API refuses scripts)
    python sos.py --official      # mark the files official (after the SoS certifies)

Writes:
  results/state/<election>.json    statewide totals per contest, with each county's numbers under "counties";
                                   top-level "counties" has each county's registered, ballots, turnout, precincts
  results/<county>/<election>.json for every county that has no Board module in run.py (those keep the
                                   Board's richer file; their SoS numbers still go into the state file)

Endpoints (all GET, JSON): getCountyList; getContestList (objectId -> display name with district or
term, which GetContestsByCounty does not repeat); GetContestsByCounty?countyId=; GetElectionSummaryCsv
(registered, ballots counted, turnout, precincts per county). Vote counts are in candidatesRunning[].vCount;
tickets have primaryCandidate + runningMate; write-ins are rows with isWriteIn; issues are YES/NO rows.
"""
from __future__ import annotations

import csv
import io
import json
import os
import re
import sys
import time
import urllib.request
from datetime import datetime

import lib

ELECTION = "2026-11-03"
BASE = "https://liveresults.ohiosos.gov"
SOURCE = {"label": "Ohio Secretary of State: election night reporting (unofficial)", "url": BASE + "/"}
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) OhioElections/1.0 (mikecostarella.github.io/OhioElections)", "Accept": "application/json, text/plain, */*"}

# Counties whose results come from their own Board module (run.py): the SoS file is not written for them.
BOARD_COUNTIES = {"trumbull", "mahoning"}

STATEWIDE: list[tuple[str, str]] = [
    (r"^Governor and Lieutenant Governor", "governor"),
    (r"^Attorney General", "attorney-general"),
    (r"^Auditor of State", "auditor-of-state"),
    (r"^Secretary of State", "secretary-of-state"),
    (r"^Treasurer of State", "treasurer-of-state"),
    (r"^U\.S\. Senator", "us-senate"),
]


def slug_of(county: str) -> str:
    return county.lower().replace(" ", "").replace(".", "")


def title_map(title: str) -> str | None:
    for pat, cid in STATEWIDE:
        if re.search(pat, title, re.I):
            return cid
    m = re.match(r"^Justice of the Supreme Court - Term Commencing (\d\d)/(\d\d)/(\d{4})", title)
    if m:
        return f"supreme-court-{m.group(3)}-{m.group(1)}-{m.group(2)}"
    m = re.match(r"^State Issue (\d+)", title)
    if m:
        return f"state-issue-{m.group(1)}"
    return None  # district races: matched by their candidates (lib.build_results)


# ---------------------------------------------------------------- fetching

def get(path: str, retries: int = 3) -> str:
    for i in range(retries):
        try:
            req = urllib.request.Request(BASE + path, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read().decode("utf-8-sig")
        except Exception as e:  # noqa: BLE001
            if i == retries - 1:
                raise
            print(f"retry {path}: {e}", file=sys.stderr)
            time.sleep(2)
    raise RuntimeError("unreachable")


def fetch_bundle() -> dict:
    """The same shape sos-dump.js saves: counties, contests, summaryCsv, byCounty{countyName: response}."""
    counties = json.loads(get("/Api/v1/Contest/getCountyList"))
    contests = json.loads(get("/Api/v1/Contest/getContestList"))
    summary = get("/Api/v1/Contest/GetElectionSummaryCsv")
    by_county = {}
    for c in counties:
        by_county[c["name"]] = json.loads(get(f"/Api/v1/Contest/GetContestsByCounty?countyId={c['value']}"))
        print(".", end="", flush=True)
    print()
    return {"fetched": datetime.now().astimezone().isoformat(timespec="seconds"), "counties": counties, "contests": contests, "summaryCsv": summary, "byCounty": by_county}


# ---------------------------------------------------------------- parsing

def contest_names(contests: list) -> dict[str, str]:
    """objectId -> display name ("Justice of the Supreme Court - Term Commencing 01/01/2027")."""
    out = {}
    for g in contests:
        for c in g["contestGroupings"]:
            out[c["contestObjectId"]] = c["displayName"]
    return out


def summary_rows(csv_text: str) -> dict[str, dict]:
    rows = {}
    for row in csv.DictReader(io.StringIO(csv_text)):
        row = {k.strip(): (v or "").strip().strip('="') for k, v in row.items() if k}
        rows[row["County"]] = row
    return rows


def county_blocks(resp: dict, names: dict[str, str]) -> lib.Report:
    """One county's GetContestsByCounty response as parser blocks, so lib.build_results can match it."""
    rep = lib.Report()
    rep.unofficial = True
    for c in resp["contestList"]:
        b = lib.Block(names.get(c["objectId"], c["name"]))
        for k in c["candidatesRunning"]:
            votes = int(k.get("vCount") or 0)
            if k.get("isWriteIn"):
                b.write_in += votes
                continue
            name = k["primaryCandidate"]
            if k.get("runningMate"):
                name = f"{name} / {k['runningMate']}"
            b.rows.append((name, votes))
        b.total = int(c.get("tcVotes") or 0) or sum(v for _, v in b.rows) + b.write_in
        b.precincts = (c.get("reportedPrecincts"), c.get("totalPrecincts"))
        rep.blocks.append(b)
    return rep


def build(bundle: dict, official: bool = False) -> tuple[dict, dict[str, dict]]:
    names = contest_names(bundle["contests"])
    stats = summary_rows(bundle["summaryCsv"])
    as_of = bundle.get("fetched") or datetime.now().astimezone().isoformat(timespec="seconds")
    status = "official" if official else "unofficial"
    with open(os.path.join(lib.DATA, "county", "index.json"), encoding="utf-8") as f:
        index = json.load(f)[ELECTION]

    state: dict = {"scope": "state", "election": ELECTION, "status": status, "asOf": as_of, "source": SOURCE, "contests": {}, "issues": {}, "counties": {}}
    tot = stats.get("Totals", {})
    state["registered"] = lib.to_int(tot["Registered Voters"])
    state["ballotsCast"] = lib.to_int(tot["Ballots Counted"])
    state["turnout"] = float(tot["Unofficial Voter Turnout"])
    state["precincts"] = {"reporting": lib.to_int(tot["Election Day Precincts Reporting"]), "total": lib.to_int(tot["Total Precincts"])}

    county_files: dict[str, dict] = {}
    problems = []
    for county, resp in bundle["byCounty"].items():
        slug = slug_of(county)
        if slug not in index:
            problems.append(f"{county}: no ballot file")
            continue
        rep = county_blocks(resp, names)
        res = lib.build_results(county=county, slug=slug, election=ELECTION, report=rep, source=SOURCE, title_map=title_map)
        res["status"] = status
        res["asOf"] = as_of
        row = stats.get(county)
        if row:
            res["registered"] = lib.to_int(row["Registered Voters"])
            res["ballotsCast"] = lib.to_int(row["Ballots Counted"])
            res["turnout"] = float(row["Unofficial Voter Turnout"])
            res["precincts"] = {"reporting": lib.to_int(row["Election Day Precincts Reporting"]), "total": lib.to_int(row["Total Precincts"])}
            # per-county turnout in the state file, for the app's statewide reports
            state["counties"][slug] = {"registered": res["registered"], "ballotsCast": res["ballotsCast"], "turnout": res["turnout"], "precincts": res["precincts"]}
        county_files[slug] = res
        # statewide roll-up: the state ballot's ids only
        for cid, c in res["contests"].items():
            if cid in STATE_IDS:
                s = state["contests"].setdefault(cid, {"total": 0, "writeIn": 0, "candidates": [], "counties": {}})
                s["total"] += c["total"]
                s["writeIn"] += c.get("writeIn", 0)
                s["counties"][slug] = {"total": c["total"], "candidates": c["candidates"]}
                for k in c["candidates"]:
                    hit = next((x for x in s["candidates"] if x["name"] == k["name"]), None)
                    if hit:
                        hit["votes"] += k["votes"]
                    else:
                        s["candidates"].append({"name": k["name"], "votes": k["votes"]})
        for iid, i in res["issues"].items():
            if iid in STATE_IDS:
                s = state["issues"].setdefault(iid, {"total": 0, "yes": 0, "no": 0, "yesLabel": i.get("yesLabel"), "noLabel": i.get("noLabel"), "counties": {}})
                s["total"] += i["total"]; s["yes"] += i["yes"]; s["no"] += i["no"]
                s["counties"][slug] = {"total": i["total"], "yes": i["yes"], "no": i["no"]}
    for s in state["contests"].values():
        if not s["writeIn"]:
            del s["writeIn"]
        s["candidates"].sort(key=lambda k: -k["votes"])
    if problems:
        state["unmatched"] = problems
    return state, county_files


def _state_ids() -> set[str]:
    with open(os.path.join(lib.DATA, "state", f"{ELECTION}.json"), encoding="utf-8") as f:
        b = json.load(f)
    return {c["id"] for c in b["contests"]} | {i["id"] for i in b["issues"]}


STATE_IDS = _state_ids()


def main(argv: list[str]) -> int:
    official = "--official" in argv
    if "--bundle" in argv:
        with open(argv[argv.index("--bundle") + 1], encoding="utf-8") as f:
            bundle = json.load(f)
    else:
        try:
            bundle = fetch_bundle()
        except Exception as e:  # noqa: BLE001
            print(f"fetch failed: {e}\nSave a bundle from Chrome with sos-dump.js and pass --bundle <file>.", file=sys.stderr)
            return 2
        os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), "downloads"), exist_ok=True)
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "downloads", f"sos-{ELECTION}.json"), "w", encoding="utf-8") as f:
            json.dump(bundle, f)
    state, county_files = build(bundle, official)
    d = os.path.join(lib.DATA, "results", "state")
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, f"{ELECTION}.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(state, f, indent=1, ensure_ascii=False)
        f.write("\n")
    written = unmatched = 0
    for slug, res in county_files.items():
        if res.get("unmatched"):
            unmatched += 1
            print(f"{slug}: unmatched {res['unmatched']}")
        if slug in BOARD_COUNTIES:
            continue
        lib.write_results(res, slug)
        written += 1
    print(f"state: {len(state['contests'])} contests, {len(state['issues'])} issues, {state['precincts']['reporting']}/{state['precincts']['total']} precincts, {state['ballotsCast']:,} ballots")
    print(f"counties: {len(county_files)} parsed, {written} written (Board counties kept: {sorted(BOARD_COUNTIES & set(county_files))}), {unmatched} with unmatched contests")
    if state.get("unmatched"):
        print("problems:", state["unmatched"])
    return 1 if unmatched or state.get("unmatched") else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
