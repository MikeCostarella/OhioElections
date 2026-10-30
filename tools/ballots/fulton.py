from lib import County, NOTE_ORDER, NOTE_PLACES

SITE = "https://www.boe.ohio.gov/fulton/"
NOTICE = "https://www.boe.ohio.gov/fulton/c/upload/FWAB_11November46Day.pdf"
ISSUES = "https://www.boe.ohio.gov/fulton/c/upload/Election_IssuesList.pdf"
PROOFS = "https://www.boe.ohio.gov/fulton/c/upload/Ballot_BallotProofs.pdf"


def build():
    # Raw SoS names ("SWANCREEK TWP", "WAUSEON CITY", "ARCHBOLD VILLAGE") already display correctly; no renames needed.
    c = County("fulton", "Fulton", "39051")
    c.src("fulton-46day", "Fulton County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election (revised September 18, 2026)", NOTICE)
    c.src("fulton-proofs", "Fulton County Board of Elections: ballot proofs for review, every precinct, November 3, 2026 General Election", PROOFS)
    c.src("fulton-issues", "Fulton County Board of Elections: issue list report, November 3, 2026 General Election (August 11, 2026)", ISSUES)
    C = ["fulton-46day", "fulton-proofs"]; I = ["fulton-46day", "fulton-proofs", "fulton-issues"]
    c.links = [
        {"label": "Board of Elections", "url": SITE},
        {"label": "Election information", "url": "https://www.boe.ohio.gov/fulton/election-info/"},
        {"label": "Candidate filings", "url": "https://lookup.boe.ohio.gov/vtrapp/fulton/cfis.aspx"},
        {"label": "Am I registered? / Sample ballot", "url": "https://lookup.boe.ohio.gov/vtrapp/fulton/vtrlookup.aspx"},
        {"label": "Sample ballots by precinct", "url": "https://lookup.boe.ohio.gov/vtrapp/fulton/ballotlist.aspx"},
        {"label": "Precincts and polling locations", "url": "https://www.boe.ohio.gov/fulton/precinct-and-polling-location-info/"},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://www.boe.ohio.gov/fulton/election-info/election-results/"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it, "
               "checked against the Board's ballot proofs for every precinct and its issue list. Issue wording is from the ballot proofs.",
               NOTE_ORDER, NOTE_PLACES,
               "Local issue numbers run 1 to 20. Fulton County also numbers the Pettisville Local School District levy \"Issue 3\", the same number as the statewide question; "
               "both appear on Pettisville ballots."]
    P = c.p; SD = c.sd
    N = lambda n: f"Issue {n}"

    # --- Federal, state legislative, appeals (all of Fulton County is in each district) ---
    # The notice also lists Matthew Althaus (Lib); he is not on the Board's ballot proofs, nor in Lucas, Wood, Erie or Ottawa. Kathy McKinstry is a write-in.
    c.contest("congress-9", "U.S. House", "Representative to Congress", [("Marcy Kaptur", "DEM"), ("Derek Merrin", "REP")], detail="9th District", src=C)
    c.contest("senate-1", "Ohio General Assembly", "State Senator", [("Craig S. Riedel", "REP")], detail="1st District · full term commencing January 1, 2027", src=C)
    c.contest("rep-81", "Ohio General Assembly", "State Representative", [("Patti Rockey", "REP"), ("David Swanson", "DEM")], detail="81st District", src=C)
    c.contest("appeals-6-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Michael R. Goulding", "REP")], detail="6th District · full term commencing February 9, 2027", src=C)
    c.contest("appeals-6-0210", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Myron C. Duhart", "DEM"), ("CJ Kamm", "REP")], detail="6th District · full term commencing February 10, 2027", src=C)

    # --- County offices ---
    # Brinda S. Miller has no party label in the notice or on the ballot proofs.
    c.contest("commissioner", "County offices", "County Commissioner", [("Brinda S. Miller", "Nonparty"), ("Jeff Rupp", "REP")], detail="Full term commencing January 1, 2027", src=C)
    c.contest("commissioner-unexpired", "County offices", "County Commissioner", [("Ronald J. Lumbrezer", "REP")], detail="Unexpired term ending January 2, 2029", src=C)
    c.contest("auditor", "County offices", "County Auditor", [("Brett J. Kolb", "REP")], detail="Full term commencing March 8, 2027", src=C)
    # Unlike other counties, the notice prints "(Rep)" and the Board's ballot proofs print "Republican" under Stiriz; kept without a party tag per the
    # convention for Common Pleas judges, with the detail saying what the proofs show.
    c.contest("cp-probate-juv", "Court of Common Pleas", "Judge of the Court of Common Pleas, Probate/Juvenile Division", ["Stacey L. Stiriz"],
              detail="Full term commencing February 9, 2027 · the Board's ballot proofs print \"Republican\" under the name", src=C)

    # --- Issues (numbered as on the ballot) ---
    c.issue("issue-1", "question", "Evergreen Local School District (Fulton and Lucas)", "School district income tax: 0.25% renewal, 5 years", SD("EVERGREEN LOCAL SD (FULTON)"), number=N(1),
            area="Evergreen Local School District (Fulton County part: Amboy/Metamora, Chesterfield, Fulton 012/1, Pike 018/2, Royalton/Lyons)",
            text="Shall an annual income tax of 0.25% on the school district income of individuals residing in the school district be imposed by the Evergreen Local School District "
                 "to renew an income tax expiring at the end of 2027 for 5 years, beginning January 1, 2028, for the purpose of providing for current expenses?", src=I)
    # Same id, jurisdiction and title as defiance.py; Fulton's ballot numbers it Issue 2.
    c.levy("four-county-adamhs", "Four County ADAMhs Board (Defiance, Fulton, Henry and Williams)", "county", "Renewal",
           "Current expenses of the Four County Board of Alcohol, Drug Addiction and Mental Health Services District.", "0.7 mill",
           "5 years, commencing in 2027", "2028", "$2,293,020 a year; $13 for each $100,000 of market value", number=N(2), area="Fulton County", src=I)
    c.levy("issue-3", "Pettisville Local School District (Fulton and Henry)", SD("PETTISVILLE LOCAL SD (FULTON)"), "Renewal", "General permanent improvements.", "2.5 mills",
           "5 years, commencing in 2026", "2027", estimate="$188,972 per year", number=N(3),
           area="Pettisville Local School District (Fulton County part: Pettisville 009/1 and 009/2, Dover 010/2)", src=I)
    # The Swanton Public Library levy is placed on the ballot through the Swanton Local School District (the issue list files it under the district),
    # so the district's boundaries are used here; Lucas County shows the same levy as "boundaries not mapped".
    c.levy("issue-4", "Swanton Public Library (Fulton and Lucas)", SD("SWANTON LOCAL SD (FULTON)"), "Renewal", "Current expenses of the Swanton Public Library.", "1 mill",
           "5 years, commencing in 2026", "2027", estimate="$220,002 per year", number=N(4),
           area="Swanton Local School District (Fulton County part: Fulton 012/2, Swanton Fulton, Swanton Swancreek, Swancreek East One, Swancreek East Two 023/1)", src=I)
    c.issue("issue-5", "question", "Wauseon Exempted Village School District", "School district income tax: 1.75% renewal, continuing", SD("WAUSEON EX VILL SD (FULTON)"), number=N(5),
            area="Wauseon Exempted Village School District (Wauseon One–Five, Clinton East, Dover 010/1, York 029/2)",
            text="Shall an annual income tax of 1.75% on the earned income of individuals residing in the school district be imposed by the Wauseon Exempted Village School District "
                 "to renew an income tax expiring at the end of 2027, for a continuing period of time, beginning January 1, 2028, for the purpose of current expenses?", src=I)
    # The notice gives the precinct as "016 - All Splits"; the ballot proofs number Archbold Three 015 (016 is German) and carry both options on its ballot.
    AR = P("ARCHBOLD VILLAGE")
    c.issue("issue-6", "liquor", "Village of Archbold", "Local liquor option: Casey's General Store #5152 (Sunday)", AR, number=N(6), area="Archbold precinct Archbold Three",
            text="Shall the sale of wine and mixed beverages be permitted for sale on Sunday by Casey's Marketing Co., doing business as Casey's General Store #5152, an applicant for a D-6 "
                 "liquor permit, at 705 S. Defiance Street, Archbold, in this precinct?", src=I)
    c.issue("issue-7", "liquor", "Village of Archbold", "Local liquor option: Archbold One Stop Center (Sunday)", AR, number=N(7), area="Archbold precinct Archbold Three",
            text="Shall the sale of wine and mixed beverages be permitted for sale on Sunday by Archbold One Stop Center, L.L.C., dba Archbold One Stop Center (Marathon), an applicant for a D-6 "
                 "liquor permit, at 1191 S. Defiance Street, Archbold, in this precinct?", src=I)
    WA = P("WAUSEON CITY")
    c.issue("issue-8", "question", "City of Wauseon", "Charter amendment: new Section 6.10 (Department of Building and Zoning)", WA, number=N(8),
            text="Shall the Charter of the City of Wauseon be amended to include a new Section 6.10 which would create a new Department of Building and Zoning?", src=I)
    c.levy("issue-9", "City of Wauseon", WA, "Additional", "Parks and recreation.", "1.6 mills", "5 years, commencing in 2026", "2027", estimate="$292,394 per year", number=N(9), src=I)
    DE = P("DELTA VILLAGE")
    c.levy("issue-10", "Village of Delta", DE, "Renewal",
           "Police department: motor vehicles, communications, other equipment, buildings and sites used directly in its operation, salaries of police personnel, "
           "and the officers' contribution required under section 742.33 of the Revised Code.", "5 mills", "5 years, commencing in 2027", "2028",
           estimate="$242,064 per year", number=N(10), src=I)
    c.issue("issue-11", "question", "Village of Delta", "Municipal income tax: change the use of the existing 0.5% water-fund income tax", DE, number=N(11),
            text="Shall Ordinance No. 19-2026, modifying the authorized use of the previously approved 0.5% municipal income tax revenue currently dedicated to the water fund, so that such revenue "
                 "may be used for the general fund and/or police fund for employee wages, employee benefits, operating expenditures, and capital expenditures, be passed?", src=I)
    LY = P("LYONS VILLAGE")
    c.levy("issue-12", "Village of Lyons", LY, "Renewal", "Current operating expenses.", "4.1 mills", "5 years, commencing in 2027", "2028", estimate="$34,715 per year", number=N(12), src=I)
    c.levy("issue-13", "Village of Lyons", LY, "Renewal", "Parks and recreation.", "0.5 mill", "5 years, commencing in 2027", "2028", estimate="$4,234 per year", number=N(13), src=I)
    # Precinct 001 (Amboy/Metamora, both splits) votes on it, so Metamora Village is included.
    c.levy("issue-14", "Amboy Township", P("AMBOY TWP", "METAMORA VILLAGE"), "Renewal",
           "Fire apparatus, equipment, buildings and sites, firefighting and emergency medical service personnel, ambulance equipment and emergency medical services.",
           "1 mill", "5 years, commencing in 2027", "2028", estimate="$68,563 per year", number=N(14), area="Amboy Township (precinct Amboy/Metamora)", src=I)
    c.levy("issue-15", "Chesterfield Township", P("CHESTERFIELD TWP"), "Renewal",
           "Fire apparatus, appliances, buildings and sites, firefighting and emergency medical service personnel, ambulance equipment and emergency medical services.",
           "0.7 mill", "5 years, commencing in 2027", "2028", estimate="$35,721 per year", number=N(15), src=I)
    CL = P("CLINTON TWP", "WAUSEON CITY")
    CLA = "Clinton Township, including the City of Wauseon (Wauseon One–Five, Clinton East, Pettisville 009/1)"
    for n, type, purpose, mills, est in [
        (16, "Renewal", "Current expenses.", "0.3 mill", "$71,967 per year"),
        (17, "Additional", "Fire protection.", "1 mill", "$271,603 per year"),
        (18, "Renewal", "Maintenance and operation of the cemeteries in Clinton Township.", "0.15 mill", "$32,787 per year"),
        (19, "Additional", "Road improvements.", "1 mill", "$271,613 per year"),
    ]:
        c.levy(f"issue-{n}", "Clinton Township (including the City of Wauseon)", CL, type, purpose, mills, "5 years, commencing in 2026", "2027", estimate=est, number=N(n), area=CLA, src=I)
    c.levy("issue-20", "York Township (excluding the Village of Delta)", P("YORK TWP"), "Renewal", "General construction, reconstruction, resurfacing and repair of roads.", "1 mill",
           "5 years, commencing in 2026", "2027", estimate="$70,555 per year", number=N(20), area="York Township outside Delta (Delta Two 027/1, Delta Three 028/1, York 029/1 and 029/2)", src=I)
    return c
