from lib import County, NOTE_ORDER, NOTE_PLACES, NOTE_UNKNOWN

SITE = "https://www.boe.ohio.gov/ashland/"
NOTICE = "https://www.boe.ohio.gov/ashland/c/upload/FWAB_11November46Day.pdf"
CANDIDATES = "https://www.boe.ohio.gov/ashland/c/upload/Election_CandidateList.pdf"
ISSUES = "https://www.boe.ohio.gov/ashland/c/upload/Election_QuestionsandIssues.pdf"
BALLOTS = "https://lookup.boe.ohio.gov/vtrapp/ashland/ballotlist.aspx"


def build():
    # The SoS file names every township "<NAME>-COMBINED" (Green as "GREEN TWP-COMBINED"); the Board writes "Clear Creek" as two words.
    # "MIFFLIN VILLAGE" and "MIFFLIN-COMBINED" (the township) are separate places.
    T = {"CLEARCREEK-COMBINED": "Clear Creek Township", "GREEN TWP-COMBINED": "Green Township"}
    for raw in ["HANOVER", "JACKSON", "LAKE", "MIFFLIN", "MILTON", "MOHICAN", "MONTGOMERY", "ORANGE", "PERRY", "RUGGLES", "SULLIVAN", "TROY", "VERMILLION"]:
        T[f"{raw}-COMBINED"] = raw.capitalize() + " Township"
    c = County("ashland", "Ashland", "39005", rename=T)
    c.src("ashland-46day", "Ashland County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election (revised 9/11/2026)", NOTICE)
    c.src("ashland-candidates", "Ashland County Board of Elections: official candidate list, 2026 General Election", CANDIDATES)
    c.src("ashland-issues", "Ashland County Board of Elections: official list of questions and issues, 2026 General Election", ISSUES)
    c.src("ashland-ballots", "Ashland County Board of Elections: precinct sample ballots, November 3, 2026 General Election", BALLOTS)
    C = ["ashland-46day"]; I = ["ashland-ballots", "ashland-46day", "ashland-issues"]
    c.links = [
        {"label": "Board of Elections", "url": SITE},
        {"label": "Election information", "url": "https://www.boe.ohio.gov/ashland/election-info/"},
        {"label": "Candidate list", "url": CANDIDATES},
        {"label": "Questions and issues list", "url": ISSUES},
        {"label": "Sample ballots by precinct", "url": BALLOTS},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://www.boe.ohio.gov/ashland/election-info/election-results/"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it, "
               "checked against the Board's candidate and issues lists. Issue wording is from the Board's precinct sample ballots.",
               NOTE_ORDER, NOTE_PLACES, NOTE_UNKNOWN,
               "Ashland County's ballots do not number local issues (only statewide Issue 3 is numbered); see your sample ballot for the order of the issues."]
    P = c.p; SD = c.sd

    # --- Federal, state legislative, appeals (the 7th Congressional, 67th House and 5th Appeals districts cover the whole county;
    #     no State Senate race: the 22nd District is not up in 2026) ---
    c.contest("congress-7", "U.S. House", "Representative to Congress", [("Brian Poindexter", "DEM"), ("Max Miller", "REP")], detail="7th District", src=C)
    c.contest("rep-67", "Ohio General Assembly", "State Representative", [("Heather L. Sample", "DEM"), ("Melanie Miller", "REP")], detail="67th District", src=C)
    c.contest("appeals-5", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Matthew George", "REP")], detail="5th District · term commencing February 9, 2027", src=C)

    # --- County offices ---
    c.contest("commissioner", "County offices", "County Commissioner", [("Sandy Bally", "DEM"), ("Brandon Carpenter", "REP")], detail="Term commencing January 1, 2027", src=C)
    # The term date is from the Board's candidate list; the notice and ballot give none.
    c.contest("auditor", "County offices", "County Auditor", [("Cindy Funk", "REP")], detail="Term commencing March 8, 2027", src=["ashland-candidates", "ashland-46day"])
    NP = " · no party label on the ballot"
    c.contest("cp-probate-juvenile", "Court of Common Pleas", "Judge of the Court of Common Pleas, Probate/Juvenile Division", ["Karen DeSanto Kellogg"],
              detail="Term commencing February 9, 2027" + NP, src=C)

    # --- Countywide ---
    c.levy("ashland-human-services", "Ashland County", "county", "Renewal",
           "Human or social services: operating expenses of the public children services agency and the care and placement costs of children, and the operation of senior citizens' services and facilities.",
           "2 mills", "5 years, commencing in 2026", "2027", estimate="$3,083,167 a year; $49 per $100,000 of market value", area="Ashland County (all precincts)", src=I)
    # The 46-day notice says "for 5 years"; the ballot and the Board's issues list say 3 years.
    c.levy("ashland-dale-roy", "Ashland County", "county", "Renewal and increase",
           "Operation of Dale-Roy programs and facilities by the Ashland County Board of Developmental Disabilities (renewal of 2.1 mills and an increase of 1.0 mill).",
           "3.1 mills", "3 years, commencing in 2027", "2028", estimate="$4,704,229 a year; $77 per $100,000 of market value", area="Ashland County (all precincts)", src=I,
           note="The Board's 46-day notice lists this levy as 5 years; the ballot and the Board's issues list say 3 years.")

    # --- School districts and library ---
    c.levy("ashland-csd-current", "Ashland City School District (Ashland and Richland counties)", SD("ASHLAND CITY SD"), "Renewal", "Current expenses.", "9.9 mills",
           "Continuing, commencing in 2027", "2028", estimate="$5,684,595 a year; $210 per $100,000 of market value",
           area="Ashland City 1-A to 4-C (precincts 1–14); Mifflin (part); Milton 1 and 3; Montgomery 1 (part), 2 (part) and 3; Orange 1 (part); Perry (part)", src=I)
    LP = SD("LOUDONVILLE-PERRYSVILLE EX VILL SD (ASHLAND)")
    LP_AREA = "Loudonville 1 and 2, Green 1 (part), Green 2, Lake (part)"
    c.issue("loudonville-perrysville-bond-income-tax", "levy", "Loudonville-Perrysville Exempted Village School District (Ashland, Knox and Richland counties)",
            "School district income tax (0.25%, 30 years) and bond issue ($16,400,000)", LP, area=LP_AREA,
            levy={"type": "Income tax and bond issue", "purpose": "Income tax for current expenses; bonds for constructing, renovating, repairing, expanding, furnishing and equipping school facilities and improving their sites.",
                  "mills": "2.85 mills (bond, estimated average)", "term": "Income tax 30 years from January 1, 2027; bonds up to 37 years",
                  "estimate": "$16,400,000 principal; $100 for each $100,000 of market value (bond)"},
            text="Shall Loudonville-Perrysville Exempted Village School District be authorized to do both of the following: (1) Impose an annual income tax of 0.25% on the school district "
                 "income of individuals, for a period of 30 years, beginning January 1, 2027, for the purpose of current expenses? (2) Issue bonds for the purpose of constructing school "
                 "facilities, renovating, repairing, expanding, improving, and constructing additions to school facilities; furnishing and equipping; and improving the sites thereof the same "
                 "in the principal amount of $16,400,000, to be repaid annually over a maximum period of 37 years, and levy a property tax outside the ten-mill limitation estimated by the "
                 "county auditor to average over the bond repayment period 2.85 mills for each $1 of taxable value, which amounts to $100 for each $100,000 of the county auditor's market "
                 "value, to pay the annual debt charges on the bonds, and to pay debt charges on any notes issued in anticipation of those bonds?", src=I)
    c.levy("loudonville-library", "Loudonville Public Library (Ashland, Knox and Richland counties)", LP, "Renewal", "Current expenses.", "0.8 mill", "5 years, commencing in 2027", "2028",
           estimate="$178,719 a year; $19 per $100,000 of market value", area=LP_AREA, src=I)
    # Jackson 2 (part) and Perry (part) vote on both; the JVSD's Ashland County part here is exactly the Northwestern district's precincts.
    NW = SD("NORTHWESTERN LOCAL SD (WAYNE)")
    NW_AREA = "Jackson 2 (part), Perry (part)"
    c.levy("northwestern-lsd-current", "Northwestern Local School District (Wayne and Ashland)", NW, "Renewal (fixed sum)", "Current operating expenses ($456,400 a year).",
           "1.8 mills (estimated average)", "5 years, commencing in 2026", "2027", "$456,400 a year; $63 for each $100,000 of market value", area=NW_AREA, src=I)
    c.levy("wayne-jvsd", "Wayne County Joint Vocational School District (Wayne, Ashland, Holmes, Medina and Stark)", NW, "Renewal", "General permanent improvements.", "0.5 mill",
           "5 years, commencing in 2027", "2028", "$1,480,860 a year; $11 for each $100,000 of market value", area=NW_AREA, src=I)

    # --- Fire and ambulance districts (not in the voter file; placed from the notice's and ballots' precinct lists) ---
    # Precinct Clear Creek (splits 1-4) is the whole township; Savannah and Bailey Lakes villages have no precincts of their own and vote there.
    c.levy("clear-creek-fire", "Clear Creek Fire District", P("CLEARCREEK-COMBINED", "SAVANNAH VILLAGE", "BAILEY LAKES VILLAGE"), "Additional",
           "Fire protection and emergency medical services.", "4 mills", "5 years, commencing in 2027", "2028",
           estimate="$265,119 a year; $140 per $100,000 of market value", area="Clear Creek precinct (all splits)", src=I)
    # Precincts Green 1 and Green 2 (Perrysville Village votes in them); the Loudonville precincts' Green Township part does not vote on these.
    GP = P("GREEN TWP-COMBINED", "PERRYSVILLE VILLAGE")
    for id, mills, est in [("green-perrysville-fire-2mill", "2 mills", "$180,807 a year; $41 per $100,000 of market value"),
                           ("green-perrysville-fire-1mill", "1 mill", "$97,274 a year; $23 per $100,000 of market value")]:
        c.levy(id, "Green-Perrysville Joint Fire District", GP, "Renewal", "Fire protection and emergency medical services.", mills, "5 years, commencing in 2027", "2028",
               estimate=est, area="Green 1 and Green 2 precincts", src=I)
    # In the Board's issues list ("issues from overlaps") and on the Ruggles and Troy ballots, but missing from the 46-day notice. Same question as huron.py's.
    c.levy("firelands-ambulance", "Firelands Ambulance Service District (Huron and Ashland)", P("RUGGLES-COMBINED", "TROY-COMBINED"), "Renewal",
           "Ambulance service, emergency medical service, or both.", "1 mill", "5 years, commencing in 2026", "2027", "$134,120 a year; $24 per $100,000 of market value",
           area="Firelands Ambulance Service District, Ashland County part (Ruggles and Troy precincts)", src=["ashland-ballots", "ashland-issues"],
           note="Not listed in the Board's 46-day notice; it is on the Board's issues list and on the Ruggles and Troy sample ballots.")

    # --- Townships ---
    c.levy("green-twp-cemetery", "Green Township", GP, "Renewal", "Maintaining and operating Greenlawn Union Cemetery.", "0.2 mill", "5 years, commencing in 2027", "2028",
           estimate="$15,322 a year; $2 per $100,000 of market value", area="Green 1 and Green 2 precincts", src=I)
    c.levy("lake-twp-roads", "Lake Township", P("LAKE-COMBINED"), "Renewal", "General construction, reconstruction, resurfacing and repair of streets, roads and bridges.", "1.5 mills",
           "5 years, commencing in 2027", "2028", estimate="$21,000 a year; $24 per $100,000 of market value", area="Lake precinct (all splits)", src=I)
    c.levy("troy-twp-cemeteries", "Troy Township", P("TROY-COMBINED"), "Renewal", "Maintaining and operating cemeteries.", "0.5 mill", "5 years, commencing in 2027", "2028",
           estimate="$14,590 a year; $11 per $100,000 of market value", area="Troy precinct", src=I)

    # --- Local liquor option ---
    c.issue("liquor-loudonville-trails-end", "liquor", "Village of Loudonville", "Local liquor option: Trails End Pizza Company (Sunday)", P("LOUDONVILLE VILLAGE"), area="Loudonville precinct 2",
            text="Shall the sale of wine and mixed beverages, and spirituous liquor be permitted for sale on Sunday by Trails End Pizza Company, Ltd, an applicant for a D-6 liquor permit "
                 "who is engaged in the business of operating a restaurant at 3052 and 3052C State Route 3, Loudonville, OH 44842, in this precinct?", src=I)
    return c
