from lib import County, NOTE_ORDER, NOTE_PLACES

SITE = "https://boe.ottawa.oh.gov/"
UP = "https://boe.ottawa.oh.gov/wp-content/uploads/"
SAMPLE = UP + "2026/09/2026-General-Election-Sample.pdf"
CAND = UP + "2026/09/Candidates-GN26-1.csv"
ISSUES = UP + "2026/10/November-2026-Issues.pdf"
NOTICE = UP + "2026/09/46-Day-Notice-GN26.pdf"


def build():
    # The SoS file writes Put-in-Bay Township as "PUT- IN- BAY TWP"; the Board calls Catawba Township "Catawba Island".
    rename = {
        "PUT- IN- BAY TWP": "Put-in-Bay Township",
        "PUT-IN-BAY VILLAGE": "Put-in-Bay Village",
        "CATAWBA TWP": "Catawba Island Township",
    }
    c = County("ottawa", "Ottawa", "39123", rename=rename)
    c.src("ottawa-sample", "Ottawa County Board of Elections: sample ballots for every precinct, November 3, 2026 General Election", SAMPLE)
    c.src("ottawa-cand", "Ottawa County Board of Elections: candidate list, November 3, 2026 General Election", CAND)
    c.src("ottawa-issues", "Ottawa County Board of Elections: November 2026 issues list", ISSUES)
    C = ["ottawa-sample", "ottawa-cand"]; I = ["ottawa-sample", "ottawa-issues"]
    c.links = [
        {"label": "Board of Elections", "url": SITE},
        {"label": "Sample ballots (all precincts)", "url": SAMPLE},
        {"label": "46-day election notice", "url": NOTICE},
    ]
    c.results_links = [{"label": "Board of Elections: past results", "url": SITE + "past-results-election-summaries-absentee-ballot-request-totals/"}]
    c.notes = ["Taken from the Board of Elections' sample ballots, which give every precinct's ballot with the full wording of each issue, "
               "checked against the Board's candidate list and issues list. (The Board's 46-day notice is a scanned image.)",
               NOTE_ORDER, NOTE_PLACES,
               "Local issue numbers run 4 to 19; Issue 3 is the statewide question."]
    P = c.p; D = c.district; SD = c.sd
    N = lambda n: f"Issue {n}"
    est = lambda total, per: f"{total} a year; {per} for each $100,000 of the county auditor's market value"

    # --- Federal, state legislative, appeals ---
    # All of Ottawa County is in the 9th Congressional and 2nd Senate districts; the 2nd Senate seat is not up in 2026.
    # Allen and Clay Townships (with Clay Center and Genoa) are in the 44th House district, the rest of the county in the 89th.
    c.contest("congress-9", "U.S. House", "Representative to Congress", [("Marcy Kaptur", "DEM"), ("Derek Merrin", "REP")], detail="9th District", src=C)
    c.contest("rep-44", "Ohio General Assembly", "State Representative", [("David J. Fournier", "DEM"), ("Edward L. Schimmel", "REP"), ("Lyndsey A. Stough", "Nonparty")],
              detail="44th District (also in Lucas and Wood Counties)", places=D("rep", 44), src=C)
    c.contest("rep-89", "Ohio General Assembly", "State Representative", [("Easton Michael Retzke", "DEM"), ("Caleb Stidham", "REP")],
              detail="89th District (also in Erie County)", places=D("rep", 89), src=C)
    c.contest("appeals-6-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Michael R. Goulding", "REP")], detail="6th District · full term commencing February 9, 2027", src=C)
    c.contest("appeals-6-0210", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Myron C. Duhart", "DEM"), ("CJ Kamm", "REP")], detail="6th District · full term commencing February 10, 2027", src=C)

    # --- County offices ---
    c.contest("commissioner", "County offices", "County Commissioner", [("Donald A. Douglas", "REP"), ("Susan Mulligan", "DEM")],
              detail="Full term commencing January 1, 2027", src=C)
    c.contest("auditor", "County offices", "County Auditor", [("Katherine Adams", "REP"), ("Michelle Kreager", "DEM")], src=C)
    # The candidate list flags Meyers as a write-in, but the sample ballots print her name with "Democratic".
    c.contest("clerk-of-courts", "County offices", "Clerk of the Court of Common Pleas", [("Christopher Enoch", "REP"), ("Jenni Meyers", "DEM")],
              detail="Unexpired term ending December 31, 2028", src=C)
    # The candidate list gives Toris as "Non-Partisan"; the ballot prints no party.
    c.contest("engineer", "County offices", "County Engineer", [("Daniel Toris Jr.", "Nonparty")], detail="Unexpired term ending December 31, 2028", src=C)
    c.contest("coroner", "County offices", "County Coroner", [("Matthew N. Widmer", "REP")], detail="Unexpired term ending December 31, 2028", src=C)
    # The candidate list gives Hany "Republican" and Winters "Non-Partisan"; judges carry no party label on the ballot.
    NP = " · no party label on the ballot"
    c.contest("cp-gen", "Court of Common Pleas", "Judge of the Court of Common Pleas", ["Bruce Winters"], detail="Full term commencing February 9, 2027" + NP, src=C)
    c.contest("cp-probate-juvenile", "Court of Common Pleas", "Judge of the Court of Common Pleas, Probate/Juvenile Division", ["Frederick C. Hany II"],
              detail="Full term commencing February 9, 2027" + NP, src=C)

    # --- Issues (numbers from the sample ballots; Issue 3 is statewide) ---
    GEN = SD("GENOA AREA LOCAL SD (OTTAWA)")
    GA = "Genoa Area Local School District, Ottawa County part (Allen 2 Genoa and Clay Center, Allen 3 and 4, Clay 1, 2, 3 Genoa Schools, Clay 4)"
    c.levy("issue-4", "Genoa Area Local School District", GEN, "Renewal", "Current operating expenses.", "4.75 mills (estimated average)",
           "5 years, commencing in 2027", "2028", "$1,300,000 a year (fixed sum); $166 for each $100,000 of the county auditor's market value", number=N(4), area=GA,
           note="A fixed-sum levy renewing an existing levy. The county auditor certified the district's carry-over balance in excess of the preceding year's "
                "general fund expenditures as $0 (0%).", src=I)
    c.levy("issue-5", "Genoa Area Local School District", GEN, "Renewal", "Education technology.", "0.5 mill",
           "5 years, commencing in 2027", "2028", est("$112,841", "$13"), number=N(5), area=GA, src=I)
    # Same question as wood.py's lake-income-tax.
    c.issue("issue-6", "question", "Lake Local School District (Wood and Ottawa)", "School district income tax: 1%, continuing, for current expenses", SD("LAKE LOCAL SD (WOOD)"),
            number=N(6), area="Lake Local School District, Ottawa County part (Allen 2 Lake)",
            text="Shall an annual income tax of 1% on the earned income of individuals residing in the school district be imposed by the Lake Local School District, "
                 "for a continuing period of time, beginning January 1, 2027, for the purpose of current expenses?", src=I)
    # The joint district is the Mental Health and Recovery Services Board of Seneca, Ottawa, Sandusky and Wyandot Counties; Seneca County votes on its
    # own 0.7-mill, 10-year renewal (seneca.py's mhrs). The Ottawa ballot does not name the board.
    c.levy("issue-7", "Ottawa County", "county", "Renewal",
           "Necessary requirements of the County's alcohol, drug addiction, and mental health joint county service district.", "0.7 mill",
           "10 years, commencing in 2027", "2028", est("$1,482,063", "$25"), number=N(7),
           note="The joint county district is served by the Mental Health and Recovery Services Board of Seneca, Ottawa, Sandusky and Wyandot Counties "
                "(as named on Seneca County's ballot); Seneca County votes on its own renewal.", src=I)
    c.levy("issue-8", "Village of Elmore", P("ELMORE VILLAGE"), "Renewal", "General construction, reconstruction, resurfacing, and repair of the streets, roads, and bridges.",
           "2.5 mills", "5 years, commencing in 2027", "2028", est("$57,607", "$55"), number=N(8), area="Elmore Village (Harris 1 Elmore)", src=I)
    c.levy("issue-9", "Village of Genoa", P("GENOA VILLAGE"), "Renewal", "Operating, maintaining, and improving Veterans Memorial Park.",
           "1.3 mills", "5 years, commencing in 2027", "2028", est("$46,397", "$28"), number=N(9), area="Genoa Village (Clay 1 and Clay 2 Genoa Vill)", src=I)
    c.levy("issue-10", "Village of Marblehead", P("MARBLEHEAD VILLAGE"), "Renewal and decrease",
           "General construction, reconstruction, resurfacing, and repair of streets, roads, and bridges; constructing, rehabilitating, repairing, or maintaining sidewalks, "
           "walkways, trails, bicycle pathways, or similar improvements; or acquiring land for them.",
           "1 mill (renewal of part of an existing levy, being a reduction of 1 mill)", "5 years, commencing in 2026", "2027", est("$250,800", "$35"), number=N(10),
           area="Marblehead Village (Dan 1 Marblehead)", src=I)
    c.issue("issue-11", "question", "Village of Oak Harbor", "Municipal income tax: 0.5% increase (to 1.5%) for police, streets and sidewalks", P("OAK HARBOR VILLAGE"),
            number=N(11), area="Oak Harbor Village (Salem 1, 2 and 3 Oak Harbor)",
            text="Shall the Ordinance providing for a 0.5 per cent levy increase, for a total of one and one-half percent, on income for providing police protection, and street "
                 "and sidewalk improvements, terminating existing property tax levies for those same purposes, while also allowing a one-half of one percent credit against "
                 "additional tax be passed?", src=I)
    c.levy("issue-12", "City of Port Clinton", P("PORT CLINTON CITY"), "Renewal",
           "Fire protection: fire apparatus and equipment, buildings and sites, water supply, fire-alarm lines, firefighting and EMS personnel, and ambulance and emergency medical services.",
           "1.9 mills", "5 years, commencing in 2026", "2027", est("$279,000", "$37"), number=N(12), area="Port Clinton City (PC 1A to 4A, including PC 1A Bay)", src=I)
    c.levy("issue-14", "Benton Township", P("BENTON TWP", "ROCKY RIDGE VILLAGE"), "Renewal", "Maintaining and operating cemeteries.",
           "0.5 mill", "5 years, commencing in 2027", "2028", est("$29,089", "$9"), number=N(14), area="Benton Township, including Rocky Ridge Village (Benton 2 and 3)", src=I)
    c.levy("issue-16", "Clay Township", P("CLAY TWP", "GENOA VILLAGE"), "Renewal", "Maintaining and operating cemeteries.",
           "0.5 mill", "5 years, commencing in 2027", "2028", est("$47,000", "$10"), number=N(16), area="Clay Township, including Genoa Village (Clay 1 to 4)", src=I)
    MB = "Put-in-Bay Township, Middle Bass precinct (PIB Middle Bass)"
    c.levy("issue-18", "Put-in-Bay Township (precinct Put-in-Bay Middle Bass)", P("PUT- IN- BAY TWP"), "Renewal",
           "Fire protection: fire apparatus and equipment, buildings and sites, water supply, fire-alarm lines, firefighting and EMS personnel, and ambulance and emergency medical services.",
           "2 mills", "5 years, commencing in 2026", "2027", est("$62,146", "$41"), number=N(18), area=MB, src=I)
    c.levy("issue-19", "Put-in-Bay Township (precinct Put-in-Bay Middle Bass)", P("PUT- IN- BAY TWP"), "Renewal", "Maintenance and upkeep of the Middle Bass Town Hall.",
           "1 mill", "5 years, commencing in 2026", "2027", est("$31,073", "$20"), number=N(19), area=MB, src=I)

    # --- Local liquor options ---
    # Precinct Allen 2 takes in the Clay Center Village voters (ballot style "Allen 2 Genoa, Allen 2 Clay Center").
    c.issue("issue-13", "liquor", "Allen Township", "Local liquor option: Chippewa Country Club (Sunday)", P("ALLEN TWP", "CLAY CENTER VILLAGE"), number=N(13),
            area="Precinct Allen 2 (Allen Township, including Clay Center Village)",
            text="Shall the sale of wine and mixed beverages, and spirituous liquor be permitted for sale on Sunday by Chippewa Operations L.L.C., dba Chippewa Country Club "
                 "an applicant for a D-6 liquor permit who is engaged in the business of operating a golf club at 23550 State Route 579, Curtice (Allen Township), OH 43412 "
                 "in this precinct?", src=I)
    c.issue("issue-15", "liquor", "Catawba Island Township", "Local liquor option: Midway Stop & Go (Sunday)", P("CATAWBA TWP"), number=N(15),
            area="Precinct Catawba Island 3",
            text="Shall the sales of wine and mixed beverages be permitted for sale on Sunday by Midway Stop & Go, L.L.C., an applicant for a D-6 liquor permit who is engaged "
                 "in the business of operating a carryout/grocery store at 1871 B NE Catawba Road, Port Clinton Catawba Island Township, OH 43452 in this precinct?", src=I)
    # Precinct Clay 2's only ballot style is "Clay 2 Genoa Vill" (it also votes on the Genoa Village levy).
    c.issue("issue-17", "liquor", "Clay Township", "Local liquor option: Cocina de Carlos (Sunday)", P("GENOA VILLAGE"), number=N(17),
            area="Precinct Clay 2 (Genoa Village)",
            text="Shall the sale of beer, wine and mixed beverages, and spirituous liquor be permitted for sale on Sunday by Santoro Genoa LLC, dba Cocina de Carlos an applicant "
                 "for a D-6 liquor permit who is engaged in the business of a full service restaurant at 22060 W State Route 51, Clay Township, Genoa, OH 43430 in this precinct?", src=I)
    return c
