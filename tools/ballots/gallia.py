from lib import County, NOTE_ORDER, NOTE_PLACES

SITE = "https://www.boe.ohio.gov/gallia/"
NOTICE = "https://www.boe.ohio.gov/gallia/c/upload/FWAB_11November46Day.pdf"
BALLOTS = "https://lookup.boe.ohio.gov/vtrapp/gallia/ballotlist.aspx"


def build():
    # The SoS file calls Gallipolis a village; the Board's notice and ballots say "Gallipolis City" (precincts 001-003).
    # Other raw names ("ADDISON TWP", "RIO GRANDE VILLAGE") already display correctly.
    c = County("gallia", "Gallia", "39053", rename={"GALLIPOLIS VILLAGE": "Gallipolis City"})
    c.src("gallia-46day", "Gallia County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election (revised September 18, 2026)", NOTICE)
    c.src("gallia-ballots", "Gallia County Board of Elections: precinct sample ballots, November 3, 2026 General Election (election data updated October 5, 2026)", BALLOTS)
    S = ["gallia-46day", "gallia-ballots"]
    B = ["gallia-ballots", "gallia-46day"]
    c.links = [
        {"label": "Board of Elections", "url": SITE},
        {"label": "Federal write-in absentee ballot notices", "url": "https://www.boe.ohio.gov/gallia/election-info/federal-write-in-absentee-ballots/"},
        {"label": "Sample ballots by precinct", "url": BALLOTS},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://www.boe.ohio.gov/gallia/election-info/election-results/"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it, "
               "checked against the Board's precinct sample ballots. Terms of office and issue wording are from the sample ballots.",
               NOTE_ORDER, NOTE_PLACES,
               "The Board's notice and sample ballots do not give local issue numbers.",
               "Court of Appeals: the 46-day notice (revised September 18, 2026) lists Peter B. Abele for the 4th District seat; he withdrew "
               "due to death, and the Board's sample ballots list Jayme Hartley Fountain (Republican) and Todd L. Grace (Democratic), as shown here."]
    P = c.p; D = c.district

    # --- Federal, state legislative, appeals (every precinct is in the 2nd Congressional, 17th Senate, 93rd House and 4th Appeals districts) ---
    c.contest("congress-2", "U.S. House", "Representative to Congress", [("Jen Mazzuckelli", "DEM"), ("David J. Taylor", "REP")],
              detail="2nd District", places=D("cong", 2), src=S)
    c.contest("senate-17", "Ohio General Assembly", "State Senator", [("Brian A. Deer", "DEM"), ("Shane Wilkin", "REP")],
              detail="17th District", places=D("sen", 17), src=S)
    c.contest("rep-93", "Ohio General Assembly", "State Representative", [("Jessica Harper", "DEM"), ("Jason Stephens", "REP")],
              detail="93rd District", places=D("rep", 93), src=S)
    # The notice lists only Peter B. Abele (Rep); the sample ballots (data of 10/5/2026) list Fountain and Grace.
    c.contest("appeals-4-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Jayme Hartley Fountain", "REP"), ("Todd L. Grace", "DEM")],
              detail="4th District · full term commencing February 9, 2027", src=B)

    # --- County ---
    c.contest("commissioner", "County offices", "County Commissioner", [("Tony Hughes", "REP")],
              detail="Full term commencing January 1, 2027", src=S)
    # The ballot gives no term for the auditor; the notice gives "Full 4 Year Term Commencing 03/08/2027".
    c.contest("auditor", "County offices", "County Auditor", [("Robbie Jacks", "REP")],
              detail="Full term commencing March 8, 2027", src=S)
    # Unlike most counties, Gallia's sample ballots (and the notice) print "Republican" under Jason D. Holdren; following the
    # Common Pleas convention he carries no party tag here, and the detail says what the ballot shows.
    c.contest("cp-probate-juvenile", "Court of Common Pleas", "Judge of the Court of Common Pleas, Juvenile and Probate Division", ["Jason D. Holdren"],
              detail="Full term commencing February 9, 2027 · the ballot prints a Republican party label for this race", src=B)

    # --- Issues (unnumbered; listed in the notice's order) ---
    est = lambda total, per: f"{total} a year; {per} for each $100,000 of market value"
    SP = P("SPRINGFIELD TWP")
    SEVEN = "7 Eleven, Inc., dba 7-Eleven Store 47556H, operating a carryout/grocery store at 2323 State Route 850, Bidwell (Springfield Township 2)"
    c.issue("liquor-7-eleven-springfield", "liquor", "Springfield Township", "Local liquor option: 7-Eleven (beer, wine and mixed beverages)", SP,
            area="Springfield Township precinct Springfield Twp 2",
            text=f"Sale of beer, wine and mixed beverages by {SEVEN}, an applicant for C-1, C-2 liquor permits.", src=B)
    c.issue("liquor-7-eleven-springfield-sunday", "liquor", "Springfield Township", "Local liquor option: 7-Eleven (Sunday wine and mixed beverages)", SP,
            area="Springfield Township precinct Springfield Twp 2",
            text=f"Sunday sale of wine and mixed beverages by {SEVEN}, an applicant for a D-6 liquor permit.", src=B)
    c.levy("clay-twp-fire", "Clay Township", P("CLAY TWP"), "Renewal",
           "Fire apparatus, equipment, buildings, water supply, fire alarm lines, firefighting and emergency medical personnel, and ambulance, paramedic or other emergency medical services.",
           "1.3 mills", "5 years, commencing in 2027", "2028", est("$30,652", "$31"), area="Clay Township precinct", src=B)
    # The notice lists precinct 019/1; both Perry Township ballot styles carry the levy.
    c.levy("perry-twp-fire", "Perry Township", P("PERRY TWP"), "Renewal",
           "Fire apparatus, equipment, buildings, water supply, fire alarm lines, and firefighting and emergency medical personnel.",
           "1 mill", "5 years, commencing in 2027", "2028", est("$20,005", "$24"), area="Perry Township precinct", src=B)
    return c
