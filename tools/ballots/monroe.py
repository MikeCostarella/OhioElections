from lib import County, NOTE_ORDER, NOTE_PLACES

SITE = "https://www.boe.ohio.gov/monroe/"
NOTICE = "https://www.boe.ohio.gov/monroe/c/upload/FWAB_11November46Day.pdf"
ISSUES = "https://www.boe.ohio.gov/monroe/c/upload/Election_Issues.pdf"
BALLOTS = "https://lookup.boe.ohio.gov/vtrapp/monroe/ballotlist.aspx"


def build():
    # Raw SoS names already display correctly ("JERUSALEM VILLAGE " has a trailing space, which display() strips); no renames needed.
    c = County("monroe", "Monroe", "39111")
    c.src("monroe-46day", "Monroe County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election (revised 10/15/2026)", NOTICE)
    c.src("monroe-issues", "Monroe County Board of Elections: November 3, 2026 General Election Issues & Levies (September 3, 2026; scanned)", ISSUES)
    c.src("monroe-ballots", "Monroe County Board of Elections: precinct sample ballots, November 3, 2026 General Election (election data updated 09/14/2026)", BALLOTS)
    S = ["monroe-46day", "monroe-ballots"]
    SI = ["monroe-46day", "monroe-issues", "monroe-ballots"]
    c.links = [
        {"label": "Board of Elections", "url": SITE},
        {"label": "Candidate & issue filings", "url": "https://www.boe.ohio.gov/monroe/election-info/filings/"},
        {"label": "Sample ballots by precinct", "url": BALLOTS},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://www.boe.ohio.gov/monroe/election-info/election-results/"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it, "
               "checked against the Board's issues list and precinct sample ballots. Issue wording is the Board's.",
               NOTE_ORDER, NOTE_PLACES,
               "The Board's notice and sample ballots do not give local issue numbers."]
    P = c.p; D = c.district

    # --- Federal, state legislative, appeals (every precinct: 12th Congressional, 96th House, 7th Appeals; the 30th Senate seat is not up) ---
    c.contest("congress-12", "U.S. House", "Representative to Congress", [("Troy Balderson", "REP"), ("Jerrad Christian", "DEM")],
              detail="12th District · full 2-year term commencing January 3, 2027", places=D("cong", 12), src=S)
    c.contest("rep-96", "Ohio General Assembly", "State Representative", [("Ron Ferguson", "REP"), ("Charrie L. Foglio", "DEM")],
              detail="96th District · full 2-year term commencing January 1, 2027", places=D("rep", 96), src=S)
    c.contest("appeals-7-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Molly K. Johnson", "REP")],
              detail="7th District · full term commencing February 9, 2027", src=S)
    c.contest("appeals-7-0210", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Mark Anthony Hanni", "REP"), ("Katherine Rudzik", "DEM")],
              detail="7th District · full term commencing February 10, 2027", src=S)

    # --- County offices ---
    # Sarah Arend has no party label in the notice or on the sample ballot.
    c.contest("commissioner", "County offices", "County Commissioner", [("Sarah Arend", "Nonparty"), ("Mitchell Mick Schumacher", "REP")],
              detail="Full 4-year term commencing January 1, 2027", src=S)
    c.contest("auditor", "County offices", "County Auditor", [("Grant Reusser", "REP"), ("Denise M. Stoneking", "DEM")],
              detail="Full 4-year term commencing March 8, 2027", src=S)
    c.contest("treasurer", "County offices", "County Treasurer", [("Elizabeth Beachy", "REP"), ("Mollie Landefeld", "DEM")],
              detail="Unexpired term ending September 2, 2029", src=S)
    NP = " · no party label on the ballot"
    # The notice tags Chelsea M. Bone "(R)"; the sample ballot prints no party for Common Pleas judges.
    c.contest("cp-probate-juvenile", "Court of Common Pleas", "Judge of the Court of Common Pleas, Probate and Juvenile Division",
              ["Chelsea M. Bone", "James L. Peters"], detail="Full 6-year term commencing February 9, 2027" + NP, src=S)

    # --- Issues (unnumbered; listed in the notice's order) ---
    est = lambda total, per: f"{total} a year; {per} for each $100,000 of market value"
    c.issue("liquor-woodsfield-vfw-5303", "liquor", "Village of Woodsfield", "Local liquor option: V.F.W. Post 5303 (Sunday sales)",
            P("WOODSFIELD VILLAGE"), area="Woodsfield North precinct (04)",
            text="Shall the sale of wine and mixed beverages and spirituous liquor be permitted for sale on Sunday by V.F.W. Post 5303, an applicant for a D-6 "
                 "liquor permit, who is engaged in the business of operating a fraternal organization at 112 N. Sycamore Street, Woodsfield, OH 43793 "
                 "in this precinct? (by petition)", src=SI)
    c.levy("stafford-current", "Stafford Village", P("STAFFORD VILLAGE"), "Renewal", "Current expenses.", "5 mills",
           "5 years, commencing in 2026", "2027", est("$3,114.58", "$95.51"), area="Stafford Village (precinct 07/02)", src=SI)
    c.levy("bethel-twp-fire", "Bethel Township", P("BETHEL TOWNSHIP"), "Renewal", "Fire protection.", "1.5 mills",
           "5 years, commencing in 2026", "2027", est("$7,783", "$16"), area="Bethel Township (precinct 03)", src=SI)
    c.levy("green-twp-roads", "Green Township", P("GREEN TOWNSHIP"), "Renewal",
           "Maintenance, general construction, reconstruction, resurfacing and repair of streets, roads, and bridges in municipal corporations, counties or townships.",
           "1 mill", "5 years, commencing in 2026", "2027", est("$41,860", "$15"), area="Green Township (precinct 08)", src=SI)
    c.levy("lee-twp-cemetery", "Lee Township", P("LEE TOWNSHIP"), "Renewal", "Maintaining and operating the township's cemeteries.", "1 mill",
           "5 years, commencing in 2026", "2027", est("$61,713", "$25.00"), area="Lee Township (precinct 10)", src=SI)
    # Jerusalem Village straddles Malaga and Sunsbury Townships; only its Sunsbury part (precinct 17/04) votes on this levy.
    c.levy("sunsbury-twp-current", "Sunsbury Township (including the Villages of Beallsville, Jerusalem and Wilson)",
           P("SUNSBURY TOWNSHIP", "BEALLSVILLE VILLAGE", "WILSON VILLAGE", "JERUSALEM VILLAGE "), "Additional",
           "Current expenses, including the villages of Beallsville, Jerusalem, and Wilson.", "2 mills",
           "5 years, commencing in 2026", "2027", est("$303,353", "$70"),
           area="Sunsbury precincts 17/01 (Sunsbury Township), 17/02 (Beallsville Village), 17/03 (Wilson Village), 17/04 (Jerusalem Village, Sunsbury part)", src=SI)
    return c
