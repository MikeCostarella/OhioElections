from lib import County, NOTE_ORDER, NOTE_PLACES

SITE = "https://www.boe.ohio.gov/scioto/"
NOTICE = "https://www.boe.ohio.gov/scioto/c/upload/FWAB_11November46Day.pdf"
BALLOTS = "https://lookup.boe.ohio.gov/vtrapp/scioto/ballotlist.aspx"


def build():
    # Raw SoS names ("RARDEN TOWNSHIP", "RARDEN VILLAGE", "PORTSMOUTH CITY") already display correctly; no renames needed.
    c = County("scioto", "Scioto", "39145")
    c.src("scioto-46day", "Scioto County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election (revised September 18, 2026)", NOTICE)
    c.src("scioto-ballots", "Scioto County Board of Elections: precinct sample ballots, November 3, 2026 General Election (election data updated October 12, 2026)", BALLOTS)
    S = ["scioto-46day", "scioto-ballots"]
    c.links = [
        {"label": "Board of Elections", "url": SITE},
        {"label": "Federal write-in absentee ballot notices", "url": "https://www.boe.ohio.gov/scioto/election-info/federal-write-in-absentee-ballots/"},
        {"label": "Sample ballots by precinct", "url": BALLOTS},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://www.boe.ohio.gov/scioto/election-info/election-results/"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it, "
               "checked against the Board's precinct sample ballots. Issue wording is from the sample ballots.",
               NOTE_ORDER, NOTE_PLACES,
               "The Board's notice and sample ballots do not give local issue numbers.",
               "Court of Appeals: the 46-day notice lists Peter B. Abele for the 4th District seat, but the Board's sample ballots list "
               "Jayme Hartley Fountain (Republican) and Todd L. Grace (Democratic); the sample ballots are shown here."]
    P = c.p; D = c.district

    # --- Federal, state legislative, appeals (all precincts are in the 2nd Congressional, 90th House and 4th Appeals districts) ---
    c.contest("congress-2", "U.S. House", "Representative to Congress", [("Jen Mazzuckelli", "DEM"), ("David J. Taylor", "REP")],
              detail="2nd District", places=D("cong", 2), src=S)
    c.contest("rep-90", "Ohio General Assembly", "State Representative", [("Collin Docterman", "DEM"), ("Justin Pizzulli", "REP")],
              detail="90th District", places=D("rep", 90), src=S)
    # The notice (revised 9/18/2026) lists Peter B. Abele with no party; the sample ballots (data of 10/12/2026) list Fountain and Grace.
    c.contest("appeals-4-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Jayme Hartley Fountain", "REP"), ("Todd L. Grace", "DEM")],
              detail="4th District · full term commencing February 9, 2027",
              src=["scioto-ballots", "scioto-46day"])

    # --- County ---
    c.contest("commissioner-0101", "County offices", "County Commissioner", [("Steven Will Mault", "REP"), ("Abby Spears", "DEM")],
              detail="Full term commencing January 1, 2027", src=S)
    c.contest("commissioner-0102", "County offices", "County Commissioner", [("Merit Smith", "REP")],
              detail="Unexpired term ending January 1, 2029", src=S)
    c.contest("auditor", "County offices", "County Auditor", [("Christopher Blackburn", "REP"), ("Tricia M. Eichenlaub", "DEM")],
              detail="Full term commencing March 8, 2027", src=S)
    NP = " · no party label on the ballot"
    for id, office, date, cs in [
        ("cp-0101", "Judge of the Court of Common Pleas", "Full term commencing January 1, 2027", ["Mark E. Kuhn"]),
        ("cp-0210", "Judge of the Court of Common Pleas", "Full term commencing February 10, 2027", ["Howard H. Harcha III"]),
        ("cp-probate-juvenile", "Judge of the Court of Common Pleas, Probate and Juvenile Division", "Full term commencing February 9, 2027", ["Rebecca L. Bennett"]),
    ]:
        c.contest(id, "Court of Common Pleas", office, cs, detail=date + NP, src=S)

    # --- Issues (unnumbered; listed in the notice's order) ---
    est = lambda total, per: f"{total} a year; {per} for each $100,000 of market value"
    c.levy("portsmouth-streets", "City of Portsmouth", P("PORTSMOUTH CITY"), "Renewal",
           "Operations, maintenance of equipment and capital improvements of street resurfacing.", "1.5 mills", "5 years, commencing in 2027", "2028",
           est("$382,516", "$39"), area="Portsmouth 1-A through 6-C", src=S)
    c.levy("new-boston-flood", "Village of New Boston", P("NEW BOSTON VILLAGE"), "Renewal", "Flood defense.", "1 mill", "5 years, commencing in 2027", "2028",
           est("$32,189", "$7"), area="New Boston 1-A and 2-A", src=S)
    OT = P("OTWAY VILLAGE")
    c.levy("otway-fire", "Village of Otway", OT, "Renewal", "Fire protection.", "1 mill", "5 years, commencing in 2026", "2027",
           est("$893", "$24"), area="Otway/Brush Creek precinct (Otway split)", src=S)
    c.levy("otway-current", "Village of Otway", OT, "Renewal", "Current expenses.", "3 mills", "5 years, commencing in 2026", "2027",
           est("$2,690", "$73"), area="Otway/Brush Creek precinct (Otway split)", src=S)
    c.issue("rarden-surrender", "question", "Village of Rarden", "Surrender of corporate powers (by petition)", P("RARDEN VILLAGE"),
            area="Rarden Vil/Twp precinct (Rarden Village split)",
            text="Shall the village known as Village of Rarden, Ohio, surrender its corporate power?", src=S)
    c.levy("south-webster-current", "Village of South Webster", P("SOUTH WEBSTER VILLAGE"), "Renewal and decrease",
           "Current expenses (renewal of part of an existing 5.5-mill levy, a reduction of 0.5 mill).", "5 mills", "5 years, commencing in 2026", "2027",
           est("$52,044", "$134"), area="South Webster Village", src=S)
    c.levy("clay-twp-police", "Clay Township", P("CLAY TOWNSHIP"), "Renewal",
           "Police protection: motor vehicles, communications, payment of salaries or equipment used directly in the operation of the police department, "
           "and ambulance/emergency medical service by a police department.", "3.8 mills", "3 years, commencing in 2026", "2027",
           est("$287,634", "$92"), area="Clay Township A, B, C and D", src=S)
    NI = P("NILE TOWNSHIP")
    c.levy("nile-twp-cemeteries", "Nile Township", NI, "Renewal and decrease",
           "Maintaining and operating cemeteries (renewal of part of an existing 1-mill levy, a reduction of 0.5 mill).", "0.5 mill", "5 years, commencing in 2027", "2028",
           est("$33,943", "$17"), area="Nile Township A, B and C", src=S)
    c.levy("nile-twp-police", "Nile Township", NI, "Renewal and decrease",
           "Providing police protection (renewal of part of an existing 3-mill levy, a reduction of 1 mill).", "2 mills", "3 years, commencing in 2026", "2027",
           est("$135,775", "$70"), area="Nile Township A, B and C", src=S)
    c.levy("porter-twp-roads", "Porter Township", P("PORTER TOWNSHIP"), "Renewal",
           "Personnel and equipment expenditures associated with road maintenance.", "0.5 mill", "5 years, commencing in 2027", "2028",
           est("$109,335", "$12"), area="Porter A through I", src=S)
    c.levy("washington-twp-police", "Washington Township", P("WASHINGTON TOWNSHIP"), "Renewal",
           "Police protection, including motor vehicles, communications, payment of salaries or equipment used directly in the operation of the police department.",
           "1 mill", "5 years, commencing in 2027", "2028", est("$59,836", "$24"), area="Washington A through E", src=S)
    # The notice lists one local option with both questions; the sample ballot has them as two separate questions.
    PC = P("PORTER TOWNSHIP")
    c.issue("liquor-twin-wheelersburg", "liquor", "Porter Township", "Local liquor option: Twin-Wheelersburg LLC (D-5 permit)", PC, area="Porter Township precinct Porter C",
            text="Sale of beer, wine and mixed beverages and spirituous liquor by Twin-Wheelersburg LLC, an applicant for a D-5 liquor permit, "
                 "operating a family restaurant at 9095 Ohio River Road, Wheelersburg (by petition).", src=S)
    c.issue("liquor-twin-wheelersburg-sunday", "liquor", "Porter Township", "Local liquor option: Twin-Wheelersburg LLC (Sunday)", PC, area="Porter Township precinct Porter C",
            text="Sunday sale of beer, wine and mixed beverages and spirituous liquor by Twin-Wheelersburg LLC, an applicant for a D-6 liquor permit, "
                 "operating a family restaurant at 9095 Ohio River Road, Wheelersburg (by petition).", src=S)
    return c
