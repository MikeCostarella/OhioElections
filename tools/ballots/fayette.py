from lib import County, NOTE_ORDER, NOTE_PLACES

SITE = "https://www.boe.ohio.gov/fayette/"
NOTICE = "https://www.boe.ohio.gov/fayette/c/upload/FWAB_11November46Day.pdf"
BALLOTS = "https://lookup.boe.ohio.gov/vtrapp/fayette/ballotlist.aspx"

APPEALS_12 = "12th District (Butler, Brown, Clermont, Clinton, Fayette, Madison, Preble and Warren counties)"


def build():
    # The SoS file writes the city "WASHINGTON C.H. CITY" (display() would give "Washington C.h. City"); the Board's ballots say
    # "Washington Court House". "NEW HOLLAND VILLAGE " has a trailing space, which display() strips.
    c = County("fayette", "Fayette", "39047", rename={"WASHINGTON C.H. CITY": "Washington Court House City"})
    c.src("fayette-46day", "Fayette County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election (revised September 18, 2026)", NOTICE)
    c.src("fayette-ballots", "Fayette County Board of Elections: sample ballots for all 42 ballot styles, November 3, 2026 (state ballot lookup, election data updated October 13, 2026)", BALLOTS)
    S = ["fayette-46day", "fayette-ballots"]; B = ["fayette-ballots", "fayette-46day"]
    c.links = [
        {"label": "Board of Elections", "url": SITE},
        {"label": "Federal write-in absentee ballot notices", "url": "https://www.boe.ohio.gov/fayette/election-info/federal-write-in-absentee-ballots/"},
        {"label": "Sample ballots by precinct", "url": BALLOTS},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://www.boe.ohio.gov/fayette/election-info/election-results/"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it, "
               "checked against the Board's sample ballots for all 42 ballot styles. Issue wording is the ballot's.",
               NOTE_ORDER, NOTE_PLACES,
               "Fayette County's ballots do not number local issues (only statewide Issue 3 is numbered)."]
    P = c.p; D = c.district; SD = c.sd
    NP = " · no party label on the ballot"

    # --- Federal, state legislative, appeals (every precinct is in the 15th Congressional, 17th Senate, 91st House and 12th Appeals districts) ---
    # Same contests as madison.py/highland.py/ross.py. Write-in Samuel Ronan (Congress) is not listed.
    c.contest("congress-15", "U.S. House", "Representative to Congress", [("Brennan Barrington", "LIB"), ("Mike Carey", "REP"), ("Don Leonard", "DEM")],
              detail="15th District · full term commencing January 3, 2027", places=D("cong", 15), src=S)
    c.contest("senate-17", "Ohio General Assembly", "State Senator", [("Brian A. Deer", "DEM"), ("Shane Wilkin", "REP")],
              detail="17th District", places=D("sen", 17), src=S)
    c.contest("rep-91", "Ohio General Assembly", "State Representative", [("Bob Peterson", "REP"), ("Amy Wright", "DEM")],
              detail="91st District · full term commencing January 1, 2027", places=D("rep", 91), src=S)
    # Same contests as butler.py/clinton.py/madison.py. The notice marks Byrne "(Withdrawn)" and lists write-ins Victor M. Haddad and
    # Willa Concannon (Haddad withdrew, per the other 12th District specs; left out). The sample ballots still print Byrne.
    c.contest("appeals-12-0101", "Ohio Court of Appeals", "Judge of the Court of Appeals",
              [("Matthew Byrne", "REP", "Withdrew September 16, 2026; his name may still appear on the ballot, but votes for him will not count"),
               ("Willa Concannon", "Write-in")],
              detail=APPEALS_12 + " · full term commencing January 1, 2027", src=S)
    # The notice misprints this term as commencing "2/09/20207"; the ballots give 2-9-2027.
    c.contest("appeals-12-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Robert A. Hendrickson", "REP")],
              detail=APPEALS_12 + " · full term commencing February 9, 2027", src=B)

    # --- County ---
    c.contest("commissioner", "County offices", "County Commissioner", [("Brance Johnson", "REP")], detail="Full term commencing January 1, 2027", src=S)
    c.contest("auditor", "County offices", "County Auditor", [("Brenda Mossbarger", "REP")], detail="Full term commencing March 8, 2027", src=S)
    c.contest("cp-probate-juvenile", "Court of Common Pleas", "Judge of the Court of Common Pleas, Probate/Juvenile Division", ["Carole L. Pontious"],
              detail="Full term commencing February 9, 2027" + NP, src=S)

    # --- Issues (unnumbered; listed in the notice's order) ---
    est = lambda total, per, basis="the county auditor's market": f"{total} a year; {per} for each $100,000 of {basis} value"
    UNION = P("UNION TOWNSHIP")
    c.levy("union-twp-fire", "Union Township", UNION, "Renewal",
           "Fire apparatus, appliances, buildings or sites, sources of water supply, fire-alarm lines, and paying firefighters or fire-fighting companies "
           "or contracting for fire protection.", "1 mill", "5 years, commencing in 2027", "2028", est("$115,505", "$35"),
           area="Union Township precincts Union East, Union North and Union South/West", src=B)
    # Bloomingburg precinct (the village, in Paint Township) votes on it too.
    c.levy("paint-twp-cemeteries", "Paint Township", P("PAINT TOWNSHIP", "BLOOMINGBURG VILLAGE"), "Renewal", "Maintaining and operating cemeteries.", "1 mill",
           "5 years, commencing in 2027", "2028", est("$43,387", "$12"), area="Paint Township precincts Paint (splits 1 and 2) and Bloomingburg", src=B)
    c.levy("perry-twp-fire-ems", "Perry Township", P("PERRY TOWNSHIP"), "Renewal and decrease", "Fire protection and emergency medical services.", "1 mill",
           "5 years, commencing in 2027", "2028", est("$51,418", "$35"), area="Perry Township (splits 1 and 2)",
           note="A renewal of part of an existing levy, reduced by 0.5 mill. The 46-day notice calls it a 1 mill renewal.", src=B)
    # Same levy as pickaway.py's fayette-ems-renewal. Countywide except Jefferson Township (with Jeffersonville) and Perry split 2 (per the notice);
    # the sample ballots also leave it off Jasper split 4. Octa (mostly in Jasper Township) is kept in.
    EMS = sorted(set(c.places) - set(P("JEFFERSON TOWNSHIP", "JEFFERSONVILLE VILLAGE")))
    c.levy("fayette-ems-renewal", "Fayette County Emergency Medical Service District (Fayette and Pickaway)", EMS, "Renewal",
           "Ambulance service, emergency medical service, or both.", "1.90 mills", "3 years, commencing in 2027", "2028", est("$1,482,933", "$49"),
           area="County-wide except Jefferson Township, the Village of Jeffersonville, Perry split 2 and Jasper split 4", src=B)
    c.issue("wch-csd-income-tax", "question", "Washington Court House City School District", "School district income tax renewal: 1 percent, 7 years, current expenses",
            SD("WASHINGTON CH CITY SD"), area="Washington Court House City School District (Washington precincts and parts of Union East and Union South/West)",
            text="Shall an annual income tax of 1.00% on the earned income of individuals residing within the school district be imposed by the Washington Court House "
                 "City School District to renew an income tax expiring at the end of 2027, for 7 years, beginning January 1, 2028, for the purpose of providing for "
                 "current expenses?", src=B)
    c.issue("liquor-pettits-drive-thru-2", "liquor", "Union Township", "Local liquor option: Pettit's Drive Thru 2 (Sunday)", UNION, area="Union Township precinct Union South/West",
            text="Shall the sale of wine and mixed beverages be permitted for sale on Sunday by GL Pettit, LLC dba Pettit's Drive Thru 2, an applicant for a D-6 liquor permit "
                 "who is engaged in the business of operating a carry out/drive thru at 1101 Clinton Ave, Washington CH, Union Township, Ohio 43160, in this precinct?", src=B)
    c.issue("liquor-pettits-grocery", "liquor", "Village of Bloomingburg", "Local liquor option: Pettit's Grocery (Sunday)", P("BLOOMINGBURG VILLAGE"), area="Precinct Bloomingburg",
            text="Shall the sale of wine and mixed beverages be permitted for sale on Sunday by GL Pettit, LLC dba Pettit's Grocery, an applicant for a D-6 liquor permit "
                 "who is engaged in the business of operating a carryout/grocery store at 58 Main St, Bloomingburg, Ohio 43106, in this precinct?",
            note="The 46-day notice lists several permit classes (C-1, C-2, C-2X, D-1, D-2, D-3, D-5, D-5i, A-1-A and/or D-6) for this location; the ballot asks only about Sunday sales under a D-6 permit.",
            src=B)
    # Same question as pickaway.py's, clinton.py's, madison.py's and ross.py's miami-trace-renewal (Issue 2 in highland.py). Filed in Fayette.
    c.levy("miami-trace-renewal", "Miami Trace Local School District (Fayette, Clinton, Highland, Pickaway and Ross)", SD("MIAMI TRACE LOCAL SD (FAYETTE)"), "Renewal",
           "Current operating expenses (fixed-sum levy of $1,900,000 a year).", "2.2 mills (estimated average)", "5 years, commencing in 2027", "2028",
           "$1,900,000 a year; $77 for each $100,000 of market value", area="Everyone living in the Miami Trace Local School District",
           note="A fixed-sum levy renewing an existing levy. The county auditor certified the district's carry-over balance in excess of the preceding year's general fund "
                "expenditures as $0 (0%). The 46-day notice calls it a \"renewal of 1.9 mills\"; the ballot gives $1,900,000, an estimated average of 2.2 mills.",
           src=B)
    # Same levy as pickaway.py's new-holland-cemetery; precinct Marion split 3 is the village's Fayette part.
    c.levy("new-holland-cemetery", "Village of New Holland (Pickaway and Fayette)", P("NEW HOLLAND VILLAGE "), "Renewal", "Maintaining and operating a cemetery.", "1 mill",
           "5 years, commencing in 2027", "2028", est("$8,562", "$15"), area="Precinct Marion split 3 (New Holland)", src=B)
    return c
