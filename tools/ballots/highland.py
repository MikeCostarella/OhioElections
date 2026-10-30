from lib import County, NOTE_ORDER, NOTE_PLACES

SITE = "https://www.boe.ohio.gov/highland/"
NOTICE = "https://www.boe.ohio.gov/highland/c/upload/FWAB_11November46Day.pdf"
BALLOTS = "https://lookup.boe.ohio.gov/vtrapp/highland/ballotlist.aspx"

APPEALS_4 = "4th District"


def build():
    # Raw SoS names ("BRUSHCREEK TOWNSHIP", "HILLSBORO CITY", "SINKING SPRING VILLAGE") already display correctly; no renames needed.
    c = County("highland", "Highland", "39071")
    c.src("highland-46day", "Highland County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election (revised October 6, 2026)", NOTICE)
    c.src("highland-ballots", "Highland County Board of Elections: precinct sample ballots, November 3, 2026 General Election (election data updated October 12, 2026)", BALLOTS)
    S = ["highland-46day", "highland-ballots"]
    c.links = [
        {"label": "Board of Elections", "url": SITE},
        {"label": "Federal write-in absentee ballot notices", "url": "https://www.boe.ohio.gov/highland/election-info/federal-write-in-absentee-ballots/"},
        {"label": "Candidate filings", "url": "https://lookup.boe.ohio.gov/vtrapp/highland/cfis.aspx"},
        {"label": "Sample ballots by precinct", "url": BALLOTS},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://www.boe.ohio.gov/highland/election-info/election-results/"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it, "
               "checked against the Board's precinct sample ballots. Issue wording is from the notice and matches the sample ballots.",
               NOTE_ORDER, NOTE_PLACES,
               "Court of Appeals: Peter B. Abele (Republican) is still printed on the main ballot for the 4th District seat; the Board's notice marks him "
               "withdrawn due to death, and a supplemental 4th District Court of Appeals ballot lists Jayme Hartley Fountain (Republican) and "
               "Todd L. Grace (Democratic). The supplemental ballot is shown here."]
    P = c.p; D = c.district; SD = c.sd
    N = lambda n: f"Issue {n}"

    # --- Federal, state legislative, appeals (every precinct is in the 15th Congressional, 17th Senate, 91st House and 4th Appeals districts) ---
    c.contest("congress-15", "U.S. House", "Representative to Congress", [("Brennan Barrington", "LIB"), ("Mike Carey", "REP"), ("Don Leonard", "DEM")],
              detail="15th District", places=D("cong", 15), src=S)
    c.contest("senate-17", "Ohio General Assembly", "State Senator", [("Brian A. Deer", "DEM"), ("Shane Wilkin", "REP")],
              detail="17th District", places=D("sen", 17), src=S)
    c.contest("rep-91", "Ohio General Assembly", "State Representative", [("Bob Peterson", "REP"), ("Amy Wright", "DEM")],
              detail="91st District", places=D("rep", 91), src=S)
    # The notice (revised 10/6/2026) lists Abele "(Withdrawn due to death)", "Tony L. Grace (Dem)" and Jayme Hartley Fountain (Rep);
    # the supplemental ballot spells the Democrat "Todd L. Grace", as in Ross, Scioto and Pickaway.
    c.contest("appeals-4-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Jayme Hartley Fountain", "REP"), ("Todd L. Grace", "DEM")],
              detail=APPEALS_4 + " · full term commencing February 9, 2027", src=["highland-ballots", "highland-46day"])

    # --- County ---
    c.contest("commissioner", "County offices", "County Commissioner", [("Brad Roades", "REP"), ("Howard Zody", "Nonparty")],
              detail="Full term commencing January 1, 2027", src=S)
    c.contest("auditor", "County offices", "County Auditor", [("Alex J. Butler", "REP")], detail="Full term commencing March 8, 2027", src=S)
    NP = " · no party label on the ballot"
    for id, office, cs in [
        ("cp-general", "Judge of the Court of Common Pleas, General Division", ["John W. Judkins"]),
        ("cp-juvenile-probate", "Judge of the Court of Common Pleas, Juvenile and Probate Division", ["Denny Kirk"]),
    ]:
        c.contest(id, "Court of Common Pleas", office, cs, detail="Full term commencing February 9, 2027" + NP, src=S)

    # --- Issues (numbered 1-6 in the notice and on the sample ballots) ---
    c.issue("issue-1", "question", "East Clinton Local School District (Clinton and Highland)", "School district income tax: 1.25 percent, 5 years, current expenses",
            SD("EAST CLINTON LOCAL SD (CLINTON)"), number=N(1), area="Precincts Fairfield W (split 2), Penn (splits 2 and 4) and Union (split 3)",
            text="Shall an annual income tax of 1.25 per cent on the earned income of individuals residing in the school district be imposed by East Clinton "
                 "Local School District, for 5 years, beginning January 1, 2027, for the purpose of current expenses?", src=S)
    c.levy("issue-2", "Miami Trace Local School District (Fayette, Clinton, Highland, Pickaway and Ross)", SD("MIAMI TRACE LOCAL SD (FAYETTE)"), "Renewal",
           "Current operating expenses (fixed-sum levy of $1,900,000 a year).", "2.2 mills (estimated average)", "5 years, commencing in 2027", "2028",
           "$1,900,000 a year; $77 for each $100,000 of market value", number=N(2), area="Precinct Fairfield E (split 2)", src=S)
    # Sinking Spring Village has no precinct of its own; its voters are in the Brushcreek precincts, all four of which vote on Issue 3.
    c.levy("issue-3", "Brushcreek Township", P("BRUSHCREEK TOWNSHIP", "SINKING SPRING VILLAGE"), "Additional", "Emergency medical services.",
           "2 mills", "5 years, commencing in 2026", "2027", "$98,076 a year; $70 for each $100,000 of appraised value", number=N(3),
           area="Brushcreek precincts (splits 1-4)", src=S)
    c.levy("issue-4", "Marshall Township", P("MARSHALL TOWNSHIP"), "Renewal", "Maintaining and operating cemeteries.", "0.5 mill",
           "5 years, commencing in 2026", "2027", "$13,139 a year; $11 for each $100,000 of market value", number=N(4), area="Marshall precincts", src=S)
    c.levy("issue-5", "New Market Township", P("NEW MARKET TOWNSHIP"), "Renewal", "Maintaining and operating township cemeteries.", "0.5 mill",
           "5 years, commencing in 2026", "2027", "$19,757 a year; $10 for each $100,000 of market value", number=N(5), area="New Market precincts", src=S)
    c.issue("issue-6", "liquor", "City of Hillsboro", "Local liquor option: F.O.E. Aerie 1161 Hillsboro (Sunday)", P("HILLSBORO CITY"), number=N(6),
            area="Precinct Hillsboro 2 NW",
            text="Shall the sale of wine and mixed beverages, and spirituous liquor be permitted for sale on Sunday by F.O.E. Aerie 1161 Hillsboro an applicant "
                 "for a D-6 liquor permit who is engaged in the business of operating a fraternal organization at 126-32 Governor Trimble Place, "
                 "Hillsboro, Ohio 45133 in this precinct?", src=S)
    return c
