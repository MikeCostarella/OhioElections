from lib import County, NOTE_ORDER, NOTE_PLACES

SITE = "https://crawfordcountyohioboe.gov/"
NOTICE = "https://crawfordcountyohioboe.gov/wp-content/uploads/46-Day-notice-11-3-2026.pdf"
CAND = "https://crawfordcountyohioboe.gov/wp-content/uploads/General-Election-Candidates-11-3-2026.pdf"
ISSUES = "https://crawfordcountyohioboe.gov/wp-content/uploads/Final-General-Election-Issues-11-3-2026.pdf"


def build():
    # Default display names are right. The notice's combined precincts: "Holmes - Texas" (30.1-2 Holmes Township, 30.3-4 Texas Township),
    # "Lykens - Tod" (37.1 Lykens Township, 37.2-3 Tod Township), "Sandusky - Whetstone North" (Sandusky Township, north Whetstone Township
    # and part of North Robinson); Jackson Township votes in Crestline 2A. Splits read from the Holmes and Lykens levies' precinct lists.
    c = County("crawford", "Crawford", "39033")
    c.src("crawford-46day", "Crawford County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election", NOTICE)
    c.src("crawford-cand", "Crawford County Board of Elections: candidates, November 3, 2026 General Election", CAND)
    c.src("crawford-issues", "Crawford County Board of Elections: issues (ballot wording), November 3, 2026 General Election", ISSUES)
    C = ["crawford-46day", "crawford-cand"]; I = ["crawford-46day", "crawford-issues"]
    c.links = [
        {"label": "Board of Elections", "url": SITE},
        {"label": "Voter tools", "url": "https://crawfordcountyohioboe.gov/voter-tools/"},
        {"label": "Who is running? (candidates and issues)", "url": "https://crawfordcountyohioboe.gov/who-is-running/"},
        {"label": "Am I registered? / Sample ballot", "url": "https://crawford-voterview.boe.ohio.gov/VoterView/RegistrantSearch.do"},
    ]
    c.results_links = [{"label": "Board of Elections", "url": SITE}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it, "
               "checked against the Board's candidate list and issues list (which gives the full ballot wording).",
               NOTE_ORDER, NOTE_PLACES,
               "Local issue numbers (4 to 18) are from the Board's notice; Issue 3 is the statewide question."]
    P = c.p; SD = c.sd
    N = lambda n: f"Issue {n}"
    est = lambda total, per: f"{total} a year; {per} for each $100,000 of the county auditor's market value"

    # --- Federal, state legislative, appeals (all of Crawford County is in each district; no State Senate race) ---
    c.contest("congress-5", "U.S. House", "Representative to Congress", [("Bob Latta", "REP"), ("Brian A. Shaver", "DEM"), ("Michael J. Veloff", "LIB")],
              detail="5th District", src=C)
    c.contest("rep-87", "Ohio General Assembly", "State Representative", [("Lora Covrett", "DEM"), ("Jeffrey A. McClain", "REP"), ("Craig Swartz", "Nonparty")],
              detail="87th District · full term commencing January 1, 2027", src=C)
    c.contest("appeals-3-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Mark C. Miller", "REP")], detail="3rd District · full term commencing February 9, 2027", src=C)

    # --- County offices ---
    c.contest("commissioner", "County offices", "County Commissioner", [("Tim Ley", "REP")], detail="Full term commencing January 1, 2027", src=C)
    c.contest("auditor", "County offices", "County Auditor", [("Robyn M. Sheets", "REP")], detail="Full term commencing March 8, 2027", src=C)
    NP = " · no party label on the ballot"
    c.contest("cp-gen", "Court of Common Pleas", "Judge of the Court of Common Pleas, General Division", ["Sean E. Leuthold"],
              detail="Full term commencing February 9, 2027" + NP, src=C)
    c.contest("cp-probate-juvenile", "Court of Common Pleas", "Judge of the Court of Common Pleas, Probate/Juvenile Division", ["Matthew E. Crall"],
              detail="Full term commencing February 9, 2027" + NP, src=C)

    # --- Issues, in the notice's order ---
    # Same question as richland.py's crestline-evsd-income-tax. The notice also lists Galion 2A (split 3); the voter file has no Galion City voters in the district.
    c.issue("crestline-evsd-income-tax", "question", "Crestline Exempted Village School District (Crawford and Richland counties)",
            "School district income tax: additional 0.75%, continuing, for current expenses", SD("CRESTLINE EX VILL SD (CRAWFORD)") + P("GALION CITY"),
            area="Crestline Exempted Village School District, Crawford County part (Crestline 1A, 2A, 3A, 4A; Galion 2A split 3; Vernon Township split 3)", number=N(4),
            text="Shall an annual income tax of 0.75 percent on the earned income of individuals residing in the school district be imposed by the Crestline Exempted Village "
                 "School District, for a continuing period of time, beginning January 1, 2027, for the purpose of current expenses?", src=I)
    c.levy("issue-5", "Ridgedale Local School District (Marion, Crawford and Wyandot counties)", SD("RIDGEDALE LOCAL SD (MARION)"), "Renewal",
           "Current expenses (fixed sum of $575,034).", "2.44 mills (estimated average)", "5 years, commencing in 2027", "2028",
           estimate=est("$575,034", "$85"), number=N(5), area="Ridgedale Local School District, Crawford County part (Dallas Township split 2)",
           note="The county auditor certified the district's carry-over balance above the prior year's general fund expenditures as $0 (0% of those expenditures).", src=I)
    c.issue("issue-6", "question", "Wynford Local School District", "School district income tax: 1.75%, 10 years, for current expenses", SD("WYNFORD LOCAL SD (CRAWFORD)"),
            area="Wynford Local School District (Bucyrus 1B, 3A, 3B, 3C, 4A splits 2; Bucyrus Township split 3; Chatfield Township split 3; Dallas Township split 3; "
                 "Holmes-Texas splits 2 and 4; Liberty Township split 2; Lykens-Tod splits 1 and 3)", number=N(6),
            text="Shall an annual income tax of 1.75 percent on the earned income of individuals residing in the school district be imposed by the Wynford Local School District "
                 "for 10 years, beginning January 1, 2027, for the purpose of current expenses?", src=I)
    # Special districts placed from the notice's precinct lists (whole precincts, or the Holmes and Tod splits of the combined precincts).
    c.levy("issue-7", "Crawford County West Joint Ambulance District", P("BUCYRUS TOWNSHIP", "DALLAS TOWNSHIP", "HOLMES TOWNSHIP", "LYKENS TOWNSHIP", "TOD TOWNSHIP"),
           "Renewal", "Ambulance service and emergency medical service.", "1.5 mills", "5 years, commencing in 2026", "2027", estimate=est("$233,702", "$33"), number=N(7),
           area="Bucyrus Township, Dallas Township, Holmes-Texas (splits 1 and 2, Holmes Township), Lykens-Tod", src=I)
    c.levy("issue-8", "Life First Ambulance District",
           P("AUBURN TOWNSHIP", "TIRO VILLAGE", "CHATFIELD TOWNSHIP", "CHATFIELD VILLAGE", "CRANBERRY TOWNSHIP", "NEW WASHINGTON VILLAGE", "LIBERTY TOWNSHIP",
             "SANDUSKY TOWNSHIP", "WHETSTONE TOWNSHIP", "NORTH ROBINSON VILLAGE"),
           "Renewal", "Ambulance service and emergency medical service.", "2 mills", "5 years, commencing in 2026", "2027", estimate=est("$761,676", "$43"), number=N(8),
           area="Auburn, Chatfield, Cranberry and Liberty townships (with Tiro, Chatfield and New Washington), Sandusky-Whetstone North (with part of North Robinson), Whetstone Township South",
           src=I)
    c.levy("issue-9", "Wyandot East Fire District", P("TOD TOWNSHIP"), "Renewal", "Providing and maintaining fire protection services.",
           "2.5 mills", "5 years, commencing in 2026", "2027", estimate=est("$76,990", "$32"), number=N(9), area="Lykens-Tod (splits 2 and 3, Tod Township)", src=I)
    c.issue("issue-10", "question", "City of Bucyrus", "Municipal income tax: 0.1%, 4 years, for city parks and the city pool", P("BUCYRUS CITY"),
            area="Bucyrus 1A to 4B", number=N(10),
            text="Shall the Ordinance of the Bucyrus City Council providing for a one-tenth of one percent (0.100%) levy on income, for a period of four (4) years, commencing on "
                 "January 1, 2027, to provide funds for operating, maintaining, repairing, reconstructing, renovating, equipping, furnishing and improving the City owned parks "
                 "(Aumiller Park, Lions Field Park, Harmon Park, Picking Park and the Schines Art Park), including the City owned swimming pool and its ancillary facilities, "
                 "concession stands, restrooms, parking, playground equipment and site improvements, and the payment of debt service charges on securities issued for those purposes, be passed?",
            src=I)
    # Same questions as richland.py's two Galion items.
    GAL = P("GALION CITY"); GAL_J = "City of Galion (Crawford and Richland counties)"; GAL_AREA = "Galion 1A to 4C"
    c.issue("galion-council-president-term", "question", GAL_J, "Change the term of the President of Council from 2 years to 4 years", GAL, area=GAL_AREA, number=N(11),
            text="Shall the term of office for the President of the legislative authority of the City of Galion be changed from two (2) years to four (4) years beginning "
                 "January 1 after the next municipal election, be passed?", src=I)
    c.issue("galion-council-at-large-term", "question", GAL_J, "Change the terms of at-large members of Council from 2 years to 4 years", GAL, area=GAL_AREA, number=N(12),
            text="Shall the terms of office for the legislative authority of the City of Galion be changed from two (2) years to four (4) years for its “at-large” members "
                 "beginning January 1 after the next municipal election with the First, Second, Third, and Fourth Wards elected to a two (2) year term and then four (4) years thereafter, be passed?",
            src=I)
    c.issue("issue-13", "liquor", "City of Galion", "Local liquor option: L.O.O.M. Lodge Galion (Sunday)", GAL, area="Galion precinct 4B", number=N(13),
            text="Shall the sale of wine and mixed beverages, and spirituous liquor be permitted for sale on Sunday by L.O.O.M. Lodge Galion an applicant for a D-6 liquor permit "
                 "who is engaged in the business of operating a fraternal organization at 520 S. Market St., Galion, Ohio 44833 in this precinct?", src=I)
    c.levy("issue-14", "Bucyrus Township", P("BUCYRUS TOWNSHIP"), "Renewal", "Road improvement.", "1 mill", "5 years, commencing in 2026", "2027",
           estimate=est("$25,144", "$15"), number=N(14), area="Bucyrus Township", src=I)
    c.levy("issue-15", "Chatfield Township", P("CHATFIELD TOWNSHIP", "CHATFIELD VILLAGE"), "Renewal", "Protection against fire.", "1.8 mills", "5 years, commencing in 2026", "2027",
           estimate=est("$264,305", "$37"), number=N(15), area="Chatfield Township (including Chatfield Village)", src=I)
    c.levy("issue-16", "Dallas Township", P("DALLAS TOWNSHIP"), "Renewal", "Fire protection.", "2.5 mills", "5 years, commencing in 2026", "2027",
           estimate=est("$26,823", "$31"), number=N(16), area="Dallas Township", src=I)
    c.levy("issue-17", "Holmes Township", P("HOLMES TOWNSHIP"), "Additional", "Current expenses.", "1.75 mills", "5 years, commencing in 2026", "2027",
           estimate=est("$108,881", "$61"), number=N(17), area="Holmes-Texas (splits 1 and 2, Holmes Township)", src=I)
    # The Board's wording prints "$100,00"; read as $100,000. This levy runs 3 years.
    c.levy("issue-18", "Lykens Township", P("LYKENS TOWNSHIP"), "Renewal", "Fire equipment.", "2 mills", "3 years, commencing in 2026", "2027",
           estimate=est("$79,458", "$42"), number=N(18), area="Lykens-Tod (split 1, Lykens Township)", src=I)
    return c
