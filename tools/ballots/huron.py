from lib import County, NOTE_ORDER, NOTE_PLACES

SITE = "https://www.huron.boe.ohio.gov/"
NOTICE = "https://www.huron.boe.ohio.gov/wp-content/uploads/46-FWAB-2.0.pdf"
ISSUES = "https://www.huron.boe.ohio.gov/wp-content/uploads/Issue-listing-11.3.2026-with-millage-9-1-2026.pdf"
BALLOTS = "https://lookup.boe.ohio.gov/vtrapp/huron/ballotlist.aspx"


def build():
    # Raw names are clean. Bellevue is shared with Erie, Sandusky and Seneca; Milan Village with Erie; Plymouth Village with Richland.
    c = County("huron", "Huron", "39077")
    c.src("huron-46day", "Huron County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election (revised 9/18/2026)", NOTICE)
    c.src("huron-issues", "Huron County Board of Elections: issues filed for the November 3, 2026 General Election, with millage (9/1/2026)", ISSUES)
    c.src("huron-ballots", "Huron County Board of Elections: sample ballots by precinct, November 3, 2026 General Election", BALLOTS)
    C = ["huron-46day"]; I = ["huron-ballots", "huron-46day", "huron-issues"]
    c.links = [
        {"label": "Board of Elections", "url": SITE},
        {"label": "Sample ballots by precinct", "url": BALLOTS},
        {"label": "Find your polling place", "url": "https://lookup.boe.ohio.gov/vtrapp/huron/pollfinder.aspx"},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://www.huron.boe.ohio.gov/election-results/"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it, "
               "checked against the Board's issues list. Issue wording is from the Board's precinct sample ballots.",
               NOTE_ORDER, NOTE_PLACES,
               "Huron County's ballots do not number local issues (only statewide Issue 3 is numbered)."]
    P = c.p; D = c.district; SD = c.sd

    # --- Federal, state legislative, appeals ---
    # All of Huron County is in the 5th Congressional District. Bellevue 3 and 4, Lyme Township and Wakeman Township and Village are in the
    # 89th House and 2nd Senate districts (the 2nd Senate seat is not up in 2026); the rest of the county is in the 54th House and 13th Senate.
    # Certified write-in Steve Kraus (89th House) is not listed (NOTE_ORDER).
    c.contest("congress-5", "U.S. House", "Representative to Congress", [("Bob Latta", "REP"), ("Brian A. Shaver", "DEM"), ("Michael J. Veloff", "LIB")],
              detail="5th District", src=C)
    c.contest("senate-13", "Ohio General Assembly", "State Senator", [("Gayle Manning", "REP"), ("Joe Miller", "DEM")], detail="13th District (Huron and Lorain)",
              places=D("sen", 13), src=C)
    c.contest("rep-54", "Ohio General Assembly", "State Representative", [("Brenda Buchanan", "DEM"), ("Kellie Deeter", "REP")], detail="54th District",
              places=D("rep", 54), src=C)
    c.contest("rep-89", "Ohio General Assembly", "State Representative", [("Easton Michael Retzke", "DEM"), ("Caleb Stidham", "REP")], detail="89th District",
              places=D("rep", 89), src=C)
    # The notice prints "CJ Kamm III"; the sample ballot prints "CJ Kamm", as erie.py, lucas.py and wood.py have it.
    c.contest("appeals-6-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Michael R. Goulding", "REP")], detail="6th District · full term commencing February 9, 2027", src=C)
    c.contest("appeals-6-0210", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Myron C. Duhart", "DEM"), ("CJ Kamm", "REP")], detail="6th District · full term commencing February 10, 2027", src=C)

    # --- County offices ---
    c.contest("commissioner-0101", "County offices", "County Commissioner", [("Terry Boose", "REP"), ("Cassaundra Fryman", "LIB")], detail="Full term commencing January 1, 2027", src=C)
    # The notice lists Kevin J. Rasnick as "(other)"; the ballot prints no party for him.
    c.contest("commissioner-unexpired", "County offices", "County Commissioner", [("Bob Morgan", "REP"), ("Kevin J. Rasnick", "Nonparty")],
              detail="Unexpired term ending January 2, 2029", src=C)
    c.contest("auditor", "County offices", "County Auditor", [("Roland J. Tkach", "DEM")], detail="Full term commencing March 8, 2027", src=C)
    NP = " · no party label on the ballot"
    c.contest("cp-juvenile-probate", "Court of Common Pleas", "Judge of the Court of Common Pleas, Juvenile and Probate Division", ["Timothy L. Cardwell"],
              detail="Full term commencing February 9, 2027" + NP, src=C)

    est = lambda total, per: f"{total} a year; {per} for each $100,000 of the county auditor's market value"

    # --- Countywide and special districts ---
    # The City of Bellevue has its own health department: the levy is voted on everywhere except Bellevue 3 and 4.
    c.levy("huron-health", "Huron County General Health District", sorted(set(c.places) - {"Bellevue City"}), "Renewal",
           "Meeting the expenses of the programs of the Huron County Board of Public Health.", "0.5 mill", "10 years, commencing in 2027", "2028",
           est("$587,279", "$11"), area="All of Huron County except Bellevue 3 and 4", src=I)
    # The notice's precincts (Fitchville Twp, New London Twp, New London Village #1 and #2) are all of these places.
    c.levy("firelands-ambulance", "Firelands Ambulance Service District (Huron and Ashland)", P("FITCHVILLE TOWNSHIP", "NEW LONDON TOWNSHIP", "NEW LONDON VILLAGE"),
           "Renewal", "Ambulance service, emergency medical service, or both.", "1 mill", "5 years, commencing in 2026", "2027", est("$134,120", "$24"),
           area="Firelands Ambulance Service District, Huron County part (Fitchville Township, New London Township, New London Village #1 and #2)", src=I)
    # Same question as erie.py's issue-5 (the Erie County part is Florence Township).
    c.levy("vermilion-river-ambulance", "Vermilion River Ambulance District (Erie and Huron)", P("TOWNSEND TOWNSHIP", "WAKEMAN TOWNSHIP", "WAKEMAN VILLAGE"),
           "Renewal", "Ambulance and emergency medical services: services, equipment and facilities.", "1 mill", "5 years, commencing in 2027", "2028",
           est("$183,400", "$19"), area="Vermilion River Ambulance District, Huron County part (Townsend Township, Wakeman Township and Wakeman Village)", src=I)
    c.levy("wakeman-fire", "Wakeman Fire District", P("WAKEMAN TOWNSHIP", "WAKEMAN VILLAGE"), "Renewal",
           "Fire apparatus, equipment, buildings and personnel, ambulance equipment and emergency medical services, and related costs.", "2.5 mills",
           "5 years, commencing in 2027", "2028", est("$137,451", "$40"), area="Wakeman Fire District (Wakeman Township and Wakeman Village)", src=I)
    # Same library as lorain.py's issue-6; in Huron County only the Wellington school district part of Clarksfield Township votes.
    c.levy("herrick-library", "Herrick Memorial Library (Huron and Lorain)", P("CLARKSFIELD TOWNSHIP"), "Renewal", "Current expenses.", "1.25 mills",
           "5 years, commencing in 2027", "2028", est("$339,665", "$52"),
           area="Clarksfield Township, Wellington Exempted Village School District part (precinct Clarksfield Twp, split 2)", src=I)

    # --- School district ---
    # Same question as richland.py's south-central-lsd-improvements.
    c.levy("south-central-lsd-improvements", "South Central Local School District (Huron and Richland counties)", SD("SOUTH CENTRAL LOCAL SD (HURON)"), "Renewal",
           "General permanent improvements.", "1 mill", "5 years, commencing in 2027", "2028", est("$101,700", "$24"),
           area="South Central Local School District, Huron County part (Bronson Twp #1 and #2 parts, Fairfield parts, Greenfield Twp part, Greenwich Township, Greenwich Village, North Fairfield, Ripley Township)", src=I)

    # --- Cities and villages ---
    # Same question as erie.py's issue-8.
    c.levy("bellevue-parks", "City of Bellevue (Erie, Huron, Sandusky and Seneca)", P("BELLEVUE CITY"), "Renewal", "Parks and recreation.", "1 mill",
           "5 years, commencing in 2027", "2028", est("$181,373", "$19"), area="Bellevue City, Huron County part (Bellevue 3 and 4)", src=I)
    NWK = P("NORWALK CITY"); NWK_AREA = "Norwalk 1-A to 4-C"
    # The 46-day notice and issues list print ".09 mill"; the ballot says 0.9 mill (the $4 per $100,000 figure is the same in all three).
    c.levy("norwalk-fire", "City of Norwalk", NWK, "Renewal",
           "Fire apparatus, buildings, water supply and fire alarm lines; firefighters' pay and the employer's pension contribution; ambulance equipment and ambulance, paramedic or other emergency medical services operated by the fire department.",
           "0.9 mill", "5 years, commencing in 2027", "2028", est("$82,182", "$4"), area=NWK_AREA,
           note="The Board's 46-day notice and issues list print the rate as .09 mill; the ballot says 0.9 mill.", src=I)
    c.issue("norwalk-charter-council-meetings", "question", "City of Norwalk", "Charter amendment: cancelling regular Council meetings (Article III, Section 3.07)", NWK, area=NWK_AREA,
            text="Shall Article III, Section 3.07 of the Charter of the City of Norwalk be amended to add: Notwithstanding the foregoing, upon the concurrence of the Mayor "
                 "and the President of Council, or in the absence of the President the President Pro Tempore of Council, a regularly scheduled meeting of Council may be "
                 "cancelled due to emergency, inclement weather, or lack of business to consider at the meeting?", src=I)
    c.issue("new-london-income-tax", "question", "Village of New London", "Municipal income tax: continuing the existing 0.5% for police and fire department operations",
            P("NEW LONDON VILLAGE"), area="New London Village #1 and #2",
            text="Shall the Ordinance providing for the continuation of an existing 0.5 per cent levy on income for police and fire department operations be passed?", src=I)
    NF = P("NORTH FAIRFIELD VILLAGE")
    c.levy("north-fairfield-current", "Village of North Fairfield", NF, "Additional", "Current expenses.", "2 mills", "5 years, commencing in 2027", "2028",
           est("$15,465", "$70"), src=I)
    c.levy("north-fairfield-parks", "Village of North Fairfield", NF, "Additional", "Parks and recreation.", "2 mills", "5 years, commencing in 2026", "2027",
           est("$15,460", "$70"), src=I)
    # Same question as richland.py's plymouth-cemetery.
    c.levy("plymouth-cemetery", "Village of Plymouth (Richland and Huron counties)", P("PLYMOUTH VILLAGE"), "Renewal", "Operating and maintaining the village cemetery.", "1 mill",
           "5 years, commencing in 2027", "2028", est("$16,258", "$35"), area="Plymouth, Huron County part (Plymouth Village precinct)", src=I)
    c.issue("monroeville-data-center-advisory", "question", "Village of Monroeville", "Advisory question: allowing data center development in the village", P("MONROEVILLE VILLAGE"),
            text="The purpose of this advisory question is to provide Village Council with public input, realizing the result will not, by itself, approve or prohibit any "
                 "specific data center project. Do you support the Village of Monroeville allowing data center development within the Village limits, provided such "
                 "development complies with Village zoning regulations and applicable development agreements?", src=I)

    # --- Townships ---
    c.levy("bronson-current", "Bronson Township", P("BRONSON TOWNSHIP"), "Renewal", "Current expenses.", "1 mill", "5 years, commencing in 2027", "2028",
           est("$50,400", "$18"), area="Bronson Township #1 and #2", src=I)
    # The notice lists Norwalk Twp North, Norwalk Twp South and Norwalk-Milan (the Huron County part of Milan Village is in Norwalk Township).
    c.levy("norwalk-twp-current", "Norwalk Township (including the Huron County part of Milan Village)", P("NORWALK TOWNSHIP", "MILAN VILLAGE"), "Additional",
           "Current expenses.", "0.75 mill", "5 years, commencing in 2026", "2027", est("$80,725", "$27"),
           area="Norwalk Twp North, Norwalk Twp South and Norwalk-Milan", src=I)
    c.levy("townsend-fire", "Townsend Township", P("TOWNSEND TOWNSHIP"), "Renewal",
           "Fire apparatus, rescue and other fire equipment, buildings and sites, water supply, and fire alarm communications.", "1.5 mills",
           "5 years, commencing in 2027", "2028", est("$47,960", "$22"), src=I)

    # --- Local liquor options (Sunday sales) ---
    # The notice describes Greenwich Beverage Center as "beer, wine and mixed beverages" and Buckeye Pub and Grub as "beer, wine and mixed beverages";
    # the ballot wording (used here) is wine and mixed beverages, and wine, mixed beverages and spirituous liquor.
    LQ = [
        ("liquor-greenwich-beverage-center", "Village of Greenwich", "GREENWICH VILLAGE", "Greenwich Village", "Greenwich Beverage Center (Sunday)",
         "Shall the sale of wine and mixed beverages be permitted for sale on Sunday by NY Brothers, L.L.C., dba Greenwich Beverage Center an applicant for a D-6 liquor permit "
         "who is engaged in the business of carryout/grocery store at 15 W. Main Street, Greenwich, OH 44837 in this precinct?"),
        ("liquor-norwalk-margaritas-factory", "City of Norwalk", "NORWALK CITY", "Precinct Norwalk 1-B", "Cuisine Margaritas Factory (Sunday)",
         "Shall the sale of wine and mixed beverages, and spirituous liquor be permitted for sale on Sunday by Lucky Star Buffet LLC dba Cuisine Margaritas Factory an applicant "
         "for a D-6 liquor permit who is engaged in the business of operating a family-owned Mexican restaurant at 101 Plank Rd., Norwalk, OH 44857 in this precinct?"),
        ("liquor-norwalk-buckeye-pub", "City of Norwalk", "NORWALK CITY", "Precinct Norwalk 3-A", "Buckeye Pub and Grub (Sunday)",
         "Shall the sale of wine and mixed beverages, and spirituous liquor be permitted for sale on Sunday by Buckeye Pub and Grub, LTD an applicant for a D-6 liquor permit "
         "who is engaged in the business of a restaurant and bar at 71 W. Jefferson St. and patio, Norwalk, OH 44857 in this precinct?"),
        ("liquor-norwalk-berrys", "City of Norwalk", "NORWALK CITY", "Precinct Norwalk 3-B", "Berry's on Main (Sunday)",
         "Shall the sale of wine and mixed beverages, and spirituous liquor be permitted for sale on Sunday by HRF Enterprises LLC, dba Berry's on Main an applicant for a D-6 "
         "liquor permit who is engaged in the business of a restaurant and bar at 15 W. Main St., first floor & basement, Norwalk, OH 44857 in this precinct?"),
        ("liquor-new-london-pizza-house", "Village of New London", "NEW LONDON VILLAGE", "Precinct New London Village #2", "New London Pizza House (Sunday)",
         "Shall the sale of wine and mixed beverages, and spirituous liquor be permitted for sale on Sunday by MG3 Holdings LLC dba New London Pizza House an applicant for a "
         "D-6 liquor permit who is engaged in the business of a family restaurant at 2 S. Main St., New London, OH 44851 in this precinct?"),
    ]
    for id, jur, raw, pct, biz, text in LQ:
        c.issue(id, "liquor", jur, f"Local liquor option: {biz}", P(raw), area=pct, text=text, src=I)
    return c
