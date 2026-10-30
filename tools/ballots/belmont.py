from lib import County, NOTE_ORDER, NOTE_PLACES

NOTICE = "https://www.boe.ohio.gov/belmont/c/upload/FWAB_11November46Day.pdf"


def build():
    # The Board's notice calls Bellaire "Bellaire Village" (precinct "002 Bellaire Village 2"), as the voter file does; no rename needed.
    c = County("belmont", "Belmont", "39013")
    c.src("belmont-46day", "Belmont County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election (revised 9/18/2026)", NOTICE)
    S = ["belmont-46day"]
    c.links = [
        {"label": "Board of Elections", "url": "https://www.boe.ohio.gov/belmont/"},
        {"label": "Candidates & issues", "url": "https://www.boe.ohio.gov/belmont/election-info/candidates-issues/"},
        {"label": "Sample ballots by precinct", "url": "https://lookup.boe.ohio.gov/vtrapp/belmont/ballotlist.aspx"},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://www.boe.ohio.gov/belmont/election-info/election-results/"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it "
               "(the Board's issues list for this election was not yet posted). Issue wording is the Board's; the full wording is on the sample ballot.",
               NOTE_ORDER, NOTE_PLACES,
               "The Board's notice does not give local issue numbers; see your sample ballot for them."]
    P = c.p; D = c.district; SD = c.sd

    # --- Federal, state legislative, appeals ---
    c.contest("congress-6", "U.S. House", "Representative to Congress", [("Elizabeth Kirtley", "DEM"), ("Michael A. Rulli", "REP")], detail="6th District", src=S)
    c.contest("rep-95", "Ohio General Assembly", "State Representative", [("Paul Cameron", "DEM"), ("Ty Moore", "REP")], detail="95th District", places=D("rep", 95), src=S)
    c.contest("rep-96", "Ohio General Assembly", "State Representative", [("Ron Ferguson", "REP"), ("Charrie L. Foglio", "DEM")], detail="96th District", places=D("rep", 96), src=S)
    c.contest("appeals-7-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Molly K. Johnson", "REP")], detail="7th District · full term commencing February 9, 2027", src=S)
    c.contest("appeals-7-0210", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Mark Anthony Hanni", "REP"), ("Katherine Rudzik", "DEM")], detail="7th District · full term commencing February 10, 2027", src=S)

    # --- County offices ---
    c.contest("commissioner", "County offices", "County Commissioner", [("Dominic DeFelice", "REP"), ("Franklin Cecil Shaffer Jr.", "DEM")], detail="Full term commencing January 1, 2027", src=S)
    c.contest("auditor", "County offices", "County Auditor", [("Josh Meyer", "REP")], detail="Full term commencing March 8, 2027", src=S)
    NP = " · no party label on the ballot"
    for id, office, date, cs in [
        ("cp-0101", "Judge of the Court of Common Pleas", "Full term commencing January 1, 2027", ["Kevin Flanagan"]),
        ("cp-0209", "Judge of the Court of Common Pleas", "Full term commencing February 9, 2027", ["Chris Berhalter"]),
        ("cp-probate", "Judge of the Court of Common Pleas, Probate Division", "Full term commencing February 9, 2027", ["Albert E. Davies"]),
    ]:
        c.contest(id, "Court of Common Pleas", office, cs, detail=date + NP, src=S)

    # --- Issues (unnumbered in the Board's notice; listed in the notice's order) ---
    est = lambda total, per: f"{total} a year; {per} for each $100,000 of market value"
    c.levy("county-senior-services", "Belmont County", "county", "Renewal and decrease",
           "Providing and maintaining senior services and facilities, including transportation, nutrition and in-home services to elderly residents.",
           "0.75 mill", "5 years, commencing in 2027", "2028", estimate=est("$1,410,000", "$15"), area="Belmont County (all precincts)", src=S,
           note="A renewal of part of an existing levy, being a reduction of 0.75 mill.")
    c.levy("county-911-radio", "Belmont County", "county", "Renewal",
           "Belmont County 911 public safety emergency radio communications system and equipment (radios, infrastructure, dispatch consoles, pagers, mobile data terminals, next generation 911), "
           "maintenance and operations, excluding salaries.",
           "0.75 mill", "5 years, commencing in 2027", "2028", estimate=est("$1,675,000", "$22"), area="Belmont County (all precincts)", src=S)

    c.levy("bridgeport-fire", "Village of Bridgeport", P("BRIDGEPORT VILLAGE"), "Renewal",
           "Replacing or repairing fire and emergency apparatus and equipment, and providing personnel and training for firefighting and emergency medical services.",
           "4 mills", "4 years, commencing in 2027", "2028", estimate=est("$99,000", "$104"), area="Bridgeport Village 1 and 2", src=S)

    HV = P("HOLLOWAY VILLAGE")
    c.levy("holloway-police", "Village of Holloway", HV, "Additional", "Police protection and general law enforcement within corporation limits.",
           "3 mills", "5 years, commencing in 2026", "2027", estimate=est("$13,000", "$105"), src=S)
    c.levy("holloway-current-1-5", "Village of Holloway", HV, "Renewal", "Current expenses.",
           "1.5 mills", "5 years, commencing in 2026", "2027", estimate=est("$5,000", "$33"), src=S)
    c.levy("holloway-current-1-9", "Village of Holloway", HV, "Renewal", "Current expenses.",
           "1.9 mills", "5 years, commencing in 2026", "2027", estimate="$7,000 a year", src=S,
           note="The Board's notice prints the cost as \"$42,000 for each $100,000\" of market value, apparently a misprint; see your sample ballot for the figure.")
    c.levy("holloway-fire", "Village of Holloway", HV, "Renewal", "Fire protection.",
           "1 mill", "5 years, commencing in 2026", "2027", estimate=est("$3,000", "$22"), src=S)
    c.levy("holloway-roads", "Village of Holloway", HV, "Renewal", "Roads and bridges.",
           "6 mills", "5 years, commencing in 2026", "2027", estimate=est("$22,000", "$149"), src=S)

    FT = P("FLUSHING TOWNSHIP")
    FT_JUR = "Flushing Township (excluding the Villages of Flushing and Holloway)"
    c.levy("flushing-twp-fire", FT_JUR, FT, "Additional", "Fire protection with the volunteer fire departments covering areas of Flushing Township.",
           "2.5 mills", "5 years, commencing in 2026", "2027", estimate=est("$89,000", "$88"), area="Flushing Township (precincts 047/1, 047/2)", src=S)
    c.levy("flushing-twp-roads", FT_JUR, FT, "Renewal", "Road and bridge maintenance.",
           "2.5 mills", "5 years, commencing in 2026", "2027", estimate=est("$77,000", "$67"), area="Flushing Township (precincts 047/1, 047/2)", src=S)
    c.levy("mead-twp-roads", "Mead Township (excluding the Village of Shadyside)", P("MEAD TOWNSHIP"), "Renewal",
           "General construction, reconstruction, resurfacing and repair of roads and bridges.",
           "1 mill", "5 years, commencing in 2027", "2028", estimate=est("$130,000", "$19"), area="Mead Township 1 and 2", src=S)
    c.levy("somerset-twp-roads", "Somerset Township", P("SOMERSET TOWNSHIP"), "Renewal and increase",
           "General construction, reconstruction, resurfacing and repairs of roads and bridges within Somerset Township.",
           "1.5 mills", "5 years, commencing in 2027", "2028", estimate=est("$73,000", "$31"), area="Somerset Township 1 and 2", src=S,
           note="A renewal of 1.3 mills of an existing levy and an increase of 0.2 mill.")

    c.issue("martins-ferry-csd-income-tax", "question", "Martins Ferry City School District",
            "School district income tax: 0.75% on earned income for 5 years, for current expenses", SD("MARTINS FERRY CITY SD"),
            area="Martins Ferry 1-A, 2-A, 3-A, 3-B, 4-A; Colerain Township 1, 2/2, 3, 4/1, 4/4, 5/1, 5/3; Pease Township 3/3, 4/1, 4/4, 4/7, 5/3",
            text="Shall an annual income tax of 0.75% on the earned income of individuals residing in the school district be imposed by the Martins Ferry City School District, "
                 "for 5 years, beginning January 1, 2027, for the purpose of current expenses?", src=S)

    # The library's precincts in the notice are exactly the Barnesville Exempted Village School District's places (Wayne Township's precinct 123/1 only;
    # Wilson Village, which shares precinct 123, is in the Switzerland of Ohio district and is not included).
    c.levy("barnesville-library", "Barnesville Hutton Memorial Library",
           P("BARNESVILLE VILLAGE", "FLUSHING TOWNSHIP", "GOSHEN TOWNSHIP", "KIRKWOOD TOWNSHIP", "SOMERSET TOWNSHIP", "WARREN TOWNSHIP", "WAYNE TOWNSHIP"),
           "Renewal", "Current expenses.", "1 mill", "5 years, commencing in 2027", "2028", estimate=est("$222,000", "$23"),
           area="Barnesville Village 1–3; Flushing Township/1; Goshen Township/2; Kirkwood Township/1 and /3; Somerset Township 1 and 2; Warren Township; Wayne Township/1", src=S)
    # Likewise, the St. Clairsville library's precincts match the St. Clairsville-Richland City School District's places.
    c.levy("st-clairsville-library", "St. Clairsville Public Library",
           P("ST. CLAIRSVILLE CITY", "COLERAIN TOWNSHIP", "RICHLAND TOWNSHIP", "SMITH TOWNSHIP", "UNION TOWNSHIP", "WHEELING TOWNSHIP"),
           "Renewal", "Current expenses.", "0.5 mill", "5 years, commencing in 2027", "2028", estimate=est("$281,000", "$13"),
           area="St. Clairsville 1-A through 4-B; Colerain Township 2/1, 4/2; Richland Township 1–5, 6/2, 7/2; Smith Township/2; Union Township 2/1; Wheeling Township 1/1, 2/1", src=S)

    # --- Local liquor options ---
    c.issue("liquor-bellaire-sons-of-italy", "liquor", "Village of Bellaire", "Local liquor option: Sons of Italy #754 (Sunday)", P("BELLAIRE VILLAGE"),
            area="Bellaire Village precinct 2",
            text="Sunday sale of beer, wine and mixed beverages, and spirituous liquor by Sons of Italy #754, an applicant for a D-6 liquor permit and holder of a D-5 permit "
                 "(a 501(c)(8) not-for-profit fraternal organization), at 3348 Belmont St., Bellaire.", src=S)
    c.issue("liquor-powhatan-toms-carryout", "liquor", "Village of Powhatan Point", "Local liquor option: Tom's Carryout (Sunday)", P("POWHATAN POINT VILLAGE"),
            area="Powhatan Point Village precinct",
            text="Sunday sale of beer, wine and mixed beverages by Quick Food N Gas, dba Tom's Carryout, an applicant for a D-6 liquor permit (convenience store), at 329 Hwy 7 N, Powhatan Point.", src=S)
    return c
