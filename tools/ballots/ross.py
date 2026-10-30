from lib import County, NOTE_ORDER, NOTE_PLACES

SITE = "https://www.boe.ohio.gov/ross/"
NOTICE = "https://www.boe.ohio.gov/ross/c/upload/FWAB_11November46Day.pdf"
CAND = "https://www.boe.ohio.gov/ross/c/upload/ELECTION_Candidates.pdf"
ISSUES = "https://www.boe.ohio.gov/ross/c/upload/ELECTION_Issues.pdf"
# Issues led by neighbouring counties' Boards (full wording is in their notices, not Ross's).
PIKE_NOTICE = "https://www.boe.ohio.gov/pike/c/upload/FWAB_11November46Day.pdf"
FAYETTE_NOTICE = "https://www.boe.ohio.gov/fayette/c/upload/FWAB_11November46Day.pdf"

APPEALS_4 = "4th District"


def build():
    # Raw SoS names ("... TWP", "... VILLAGE", "CHILLICOTHE CITY") already display correctly.
    c = County("ross", "Ross", "39141")
    c.src("ross-46day", "Ross County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election (revised October 5, 2026)", NOTICE)
    c.src("ross-cand", "Ross County Board of Elections: candidate list, November 3, 2026 General Election (October 8, 2026)", CAND)
    c.src("ross-issues", "Ross County Board of Elections: issue list, November 3, 2026 General Election", ISSUES)
    c.src("pike-46day", "Pike County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election (Waverly City School District income tax)", PIKE_NOTICE)
    c.src("fayette-46day", "Fayette County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election (Miami Trace Local School District levy)", FAYETTE_NOTICE)
    C = ["ross-46day", "ross-cand"]; I = ["ross-issues", "ross-46day"]
    c.links = [
        {"label": "Board of Elections", "url": SITE},
        {"label": "Candidates & Issues", "url": "https://www.boe.ohio.gov/ross/election-info/candidates-issues/"},
        {"label": "Sample ballots by precinct", "url": "https://lookup.boe.ohio.gov/vtrapp/ross/ballotlist.aspx"},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://www.boe.ohio.gov/ross/election-info/election-results/"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it, "
               "checked against the Board's candidate list and issue list. Issue wording is the Board's summary; the full wording is on the sample ballot. "
               "The Waverly City and Miami Trace school issues are filed in Pike and Fayette counties; their details are from those Boards' notices.",
               NOTE_ORDER, NOTE_PLACES,
               "The Board's notice and issue list do not give local issue numbers; see your sample ballot for them.",
               "The 46-day notice also lists Dan D. Cryder (no party) for County Commissioner; he is not on the Board's candidate list of October 8, 2026, "
               "so he is not listed here."]
    P = c.p; D = c.district; SD = c.sd

    # --- Federal, state legislative, appeals ---
    c.contest("congress-2", "U.S. House", "Representative to Congress", [("Jen Mazzuckelli", "DEM"), ("David J. Taylor", "REP")],
              detail="2nd District", places=D("cong", 2), src=C)
    c.contest("senate-17", "Ohio General Assembly", "State Senator", [("Brian A. Deer", "DEM"), ("Shane Wilkin", "REP")],
              detail="17th District", places=D("sen", 17), src=C)
    c.contest("rep-91", "Ohio General Assembly", "State Representative", [("Bob Peterson", "REP"), ("Amy Wright", "DEM")],
              detail="91st District", places=D("rep", 91), src=C)
    c.contest("rep-92", "Ohio General Assembly", "State Representative", [("Mark Johnson", "REP"), ("Sarah Senff", "DEM")],
              detail="92nd District", places=D("rep", 92), src=C)
    c.contest("appeals-4-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Jayme Hartley Fountain", "REP"), ("Todd L. Grace", "DEM")],
              detail=APPEALS_4 + " · full term commencing February 9, 2027", src=C)

    # --- County ---
    c.contest("commissioner", "County offices", "County Commissioner", [("David S. Pinkerton", "REP")], detail="Full term commencing January 1, 2027", src=C)
    c.contest("auditor", "County offices", "County Auditor", [("Jeff Lehner", "REP")], detail="Full term commencing March 8, 2027", src=C)
    NP = " · no party label on the ballot"
    c.contest("cp-probate-juvenile", "Court of Common Pleas", "Judge of the Court of Common Pleas, Probate/Juvenile Division", ["Jeffrey C. Marks"],
              detail="Full term commencing February 9, 2027" + NP, src=C)

    # --- Issues (unnumbered in the Board's notice and issue list; listed in the notice's order) ---
    # The notice lists only Chillicothe city precincts (1-A to 6-C, some split); the voter file also puts part of
    # Scioto Township in the Chillicothe City School District.
    c.issue("chillicothe-csd-income-tax", "question", "Chillicothe City School District", "School district income tax: 0.75 percent, 5 years, current expenses",
            SD("CHILLICOTHE CITY SD"), area="Chillicothe city precincts 1-A to 6-C (parts of 1-C, 1-D, 2-C and 3-D)",
            text="An annual income tax of 0.75 percent on the earned income of individuals residing in the school district, for 5 years, for current expenses.", src=I)
    c.issue("chillicothe-street-income-tax", "question", "City of Chillicothe", "Municipal income tax: 0.2 percent for street paving, repairs and improvements",
            P("CHILLICOTHE CITY"), area="Chillicothe city precincts 1-A to 6-C",
            text="A levy of 0.2 percent on income, for the exclusive purpose of street paving, repairs, and improvements.", src=I)
    c.issue("waverly-csd-income-tax", "question", "Waverly City School District (Pike and Ross)", "School district income tax: 0.5 percent, 5 years, current expenses",
            SD("WAVERLY CITY SD"), area="Precinct Franklin South/2 (part of Franklin Township)",
            text="Shall an annual income tax of 0.5 per cent on the earned income of individuals residing in the school district be imposed by the Waverly City School District, "
                 "for a period of 5 years, beginning January 1, 2027, for the purpose of current expenses?",
            src=["ross-46day", "pike-46day"])
    c.levy("miami-trace-renewal", "Miami Trace Local School District (Fayette and Ross)", SD("MIAMI TRACE LOCAL SD (FAYETTE)"), "Renewal",
           "Current operating expenses.", "1.9 mills", "5 years", firstDue="2028", area="Precinct Concord Austin/2 (part of Concord Township)",
           note="The Ross Board's notice describes this as a fixed-sum levy renewing an existing levy for current operating expenses; "
                "the millage, term and first year due are from the Fayette County Board's notice.",
           src=["ross-46day", "fayette-46day"])
    # The notice's precinct cell for this issue is cut off ("PAINT TWP, PAXTON BAINBRIDGE, PAXTON, ..."); the voter file
    # also puts Twin Township in the Paint Valley district.
    c.levy("paint-valley-pi", "Paint Valley Local School District", SD("PAINT VALLEY LOCAL SD (ROSS)"), "Renewal",
           "Permanent improvements.", "2.5 mills", "5 years", src=I)
    HUNT = P("HUNTINGTON TWP"); HUNT_AREA = "Huntington Township precincts Hunt North, Hunt East, Hunt South and Hunt West"
    c.levy("huntington-twp-fire", "Huntington Township", HUNT, "Renewal", "Fire and EMS purposes.", "1 mill", "5 years", area=HUNT_AREA, src=I)
    c.issue("huntington-twp-electric-aggregation", "question", "Huntington Township", "Electricity aggregation (opt-out)", HUNT, area=HUNT_AREA,
            text="Proposed ordinance authorizing electricity aggregation with opt-out provisions.", src=I)
    BAIN = P("BAINBRIDGE VILLAGE")
    c.levy("bainbridge-operating-2", "Village of Bainbridge", BAIN, "Renewal", "Operating expenses.", "2 mills", "5 years", area="Precinct Paxton Bainbridge", src=I)
    c.levy("bainbridge-operating-29", "Village of Bainbridge", BAIN, "Renewal", "Operating expenses.", "2.9 mills", "5 years", area="Precinct Paxton Bainbridge", src=I)
    return c
