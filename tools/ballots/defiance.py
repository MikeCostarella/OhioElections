from lib import County, NOTE_ORDER, NOTE_PLACES

SITE = "https://www.boe.ohio.gov/defiance/"
NOTICE = "https://www.boe.ohio.gov/defiance/c/upload/FWAB_11November46Day.pdf"
BALLOTS = "https://lookup.boe.ohio.gov/vtrapp/defiance/ballotlist.aspx"


def build():
    # Default display names are right ("NEY VILLAGE" -> "Ney Village", "HICKSVILLE TOWNSHIP" -> "Hicksville Township").
    c = County("defiance", "Defiance", "39039")
    c.src("defiance-46day", "Defiance County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election (revised 10/15/2026)", NOTICE)
    c.src("defiance-ballots", "Defiance County Board of Elections: official sample ballots for all 46 precinct splits, November 3, 2026 (state ballot lookup)", BALLOTS)
    C = I = ["defiance-46day", "defiance-ballots"]
    c.links = [
        {"label": "Board of Elections", "url": SITE},
        {"label": "Election information", "url": "https://www.boe.ohio.gov/defiance/election-info/"},
        {"label": "Federal write-in absentee ballot notices", "url": "https://www.boe.ohio.gov/defiance/election-info/federal-write-in-absentee-ballots/"},
        {"label": "Sample ballots by precinct", "url": BALLOTS},
        {"label": "Candidate and voter tools", "url": "https://www.boe.ohio.gov/defiance/candidate-voter-tools/"},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://www.boe.ohio.gov/defiance/election-info/election-results/"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it, "
               "checked against the Board's sample ballots, which give the full ballot wording and the county auditor's estimates.",
               NOTE_ORDER, NOTE_PLACES,
               "The Board's notice and sample ballots do not give local issue numbers."]
    P = c.p; D = c.district; SD = c.sd

    # --- Federal, state legislative, appeals (all of Defiance County is in the 9th Congressional, 1st Senate and 3rd Appeals districts) ---
    # Kathy McKinstry is a certified write-in for Congress (not listed).
    c.contest("congress-9", "U.S. House", "Representative to Congress", [("Marcy Kaptur", "DEM"), ("Derek Merrin", "REP")], detail="9th District", src=C)
    c.contest("senate-1", "Ohio General Assembly", "State Senator", [("Craig S. Riedel", "REP")], detail="1st District · full term commencing January 1, 2027", src=C)
    # House: the notice's precinct lists match the voter file (81st: Adams 013, Farmer 017, Milford 025/1-3, Ney 026, Tiffin 032, Washington 033).
    c.contest("rep-81", "Ohio General Assembly", "State Representative", [("Patti Rockey", "REP"), ("David Swanson", "DEM")], detail="81st District",
              places=D("rep", 81), src=C)
    c.contest("rep-82", "Ohio General Assembly", "State Representative", [("Christopher Elder", "LIB"), ("Roy W. Klopfenstein", "REP"), ("Maddux McCray", "DEM")],
              detail="82nd District", places=D("rep", 82), src=C)
    c.contest("appeals-3-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Mark C. Miller", "REP")], detail="3rd District · full term commencing February 9, 2027", src=C)

    # --- County offices ---
    c.contest("commissioner-0101", "County offices", "County Commissioner", [("Joe L. Eureste", "DEM"), ("Dana Phipps", "REP")], detail="Full term commencing January 1, 2027", src=C)
    c.contest("commissioner-unexpired", "County offices", "County Commissioner", [("Mike Armstrong", "DEM"), ("Matthew J. Koester", "REP")], detail="Unexpired term ending January 2, 2029", src=C)
    c.contest("auditor", "County offices", "County Auditor", [("John Hancock", "DEM"), ("Vickie S. Myers", "REP")], detail="Full term commencing March 8, 2027", src=C)
    NP = " · no party label on the ballot"
    c.contest("cp-probate-juvenile", "Court of Common Pleas", "Judge of the Court of Common Pleas, Probate and Juvenile Division", ["Timothy C. Holtsberry", "Erin S. Strausbaugh"],
              detail="Full term commencing February 9, 2027" + NP, src=C)
    c.contest("cp-gen-dr", "Court of Common Pleas", "Judge of the Court of Common Pleas, General and Domestic Relations Division", ["Carson Slade"],
              detail="Full term commencing February 9, 2027" + NP, src=C)

    # --- Issues (unnumbered in the Board's documents; listed in the notice's order) ---
    c.levy("defiance-library", "Defiance Public Library System", "county", "Renewal and increase",
           "Current expenses of the library (renewal of 0.75 mill and an increase of 0.9 mill).", "1.65 mills", "35 years, commencing in 2026", "2027",
           "$1,942,369 a year; $47 for each $100,000 of market value", src=I,
           text="A renewal of 0.75 mill and an increase of 0.9 mill for each $1 of taxable value to constitute a tax for the benefit of the Defiance Public Library System "
                "for the purpose of current expenses of the library that the county auditor estimates will collect $1,942,369 annually, at a rate not exceeding 1.65 mills "
                "for each $1 of taxable value, which amounts to $47 for each $100,000 of the county auditor's market value, for 35 years, commencing in 2026, "
                "first due in calendar year 2027.")
    c.issue("defiance-charter-data-center", "question", "City of Defiance", "Charter amendment: prohibit construction of a data center (Article I, Section 1.12)",
            P("DEFIANCE CITY"), area="Defiance City (wards 1-A to 4-D, precincts 001–012)", src=I,
            text="Shall the Charter of the City of Defiance be amended to add Section 1.12 to Article I to read as follows? Article I, Section 1.12. Prohibition of a Data Center. "
                 "(A) The construction of a data center is hereby prohibited. (B) As used in this Section, \"construction\" shall mean the erection of one or more buildings, "
                 "infrastructure, facilities, and related activities, which include preparations and modifications for same, for a common purpose. "
                 "(C) As used in this Section, \"data center\" shall mean one or more buildings or physical facilities or infrastructure, located on a single real property parcel "
                 "or on contiguous, adjacent, or otherwise aggregated real property parcels that: (1) Are used primarily or exclusively for digital information services such as "
                 "the management, storage, processing, and dissemination of electronic data and information through the use of computer systems, servers, networking equipment, "
                 "and related components, including equipment cooling systems; and (2) Has an aggregate monthly demand or peak load of greater than twenty-five (25) megawatts, "
                 "however derived from any energy source, or a combination thereof. (D) This Section is self-executing.")
    c.levy("hicksville-fire", "Village of Hicksville", P("HICKSVILLE VILLAGE"), "Renewal",
           "Fire apparatus, appliances, buildings or sites, water supply, fire alarm lines, permanent, part-time or volunteer firefighters or firefighting companies "
           "(including the firefighter employer's contribution), ambulance equipment, and ambulance or emergency medical services operated by a fire department or firefighting company.",
           "2 mills", "5 years, commencing in 2026", "2027", "$97,250 a year; $44 for each $100,000 of market value",
           area="Hicksville Village (Hicksville Village A–C, precincts 019–021)", src=I)
    # The notice (revised 10/15) lists Ney Village (026/1) with Washington Township (033/1); the Ney sample ballot (data of 9/17) does not show this levy. Following the notice.
    c.levy("washington-twp-fire", "Washington Township (including Ney Village)", P("WASHINGTON TOWNSHIP", "NEY VILLAGE"), "Renewal",
           "Fire apparatus, appliances, buildings or sites, water supply, fire alarm lines, permanent, part-time or volunteer firefighters or firefighting companies "
           "(including the firefighter employers' contribution), ambulance equipment, and ambulance, paramedic or other emergency medical services operated by a fire department or firefighting company.",
           "1.5 mills", "5 years, commencing in 2027", "2028", "$31,507 a year; $19 for each $100,000 of market value",
           area="Washington Township and Ney Village (precincts 026/1, 033/1)", src=I,
           note="The Board's 46-day notice lists Ney Village with Washington Township for this levy; the Ney Village sample ballot posted in September does not show it.")
    # School districts: the notice's precinct lists match the voter file (Ayersville: Defiance 4-C/4-D parts, Highland A/B, South Richland;
    # Central: Delaware, Farmer, Mark, Milford part, Ney, Sherwood, Washington; Northeastern: Defiance 3-B/3-C/3-D parts, Adams, Noble A/B, North Richland, Tiffin).
    c.levy("ayersville-lsd-current", "Ayersville Local School District", SD("AYERSVILLE LOCAL SD (DEFIANCE)"), "Renewal", "Current expenses.", "1.3 mills",
           "5 years, commencing in 2027", "2028", "$135,721 a year; $46 for each $100,000 of market value",
           area="Ayersville Local School District (precincts 011/2, 012/3, 022/1, 023/1, 031/1)", src=I)
    c.levy("central-lsd-current", "Central Local School District (Defiance and Williams)", SD("CENTRAL LOCAL SD (DEFIANCE)"), "Renewal",
           "Current operating expenses (fixed-sum levy of $615,000 a year).", "2.57 mills (estimated average)", "5 years, commencing in 2027", "2028",
           "$615,000 a year; $90 for each $100,000 of market value",
           area="Central Local School District (Defiance County part: precincts 016/1, 017/1, 024/1, 025/2, 026/1, 030/1, 033/1)", src=I,
           text="Shall a fixed-sum levy renewing an existing levy be imposed by the Central Local School District for the purpose of paying the current operating expenses "
                "of the district in the sum of $615,000 and a levy of taxes to be made outside of the ten-mill limitation estimated by the county auditor to average 2.57 mills "
                "for each $1 of taxable value, which amounts to $90 for each $100,000 of the county auditor's market value, for a period of 5 years, commencing in 2027, "
                "first due in calendar year 2028?")
    c.levy("northeastern-lsd-current", "Northeastern Local School District", SD("NORTHEASTERN LOCAL SD (DEFIANCE)"), "Renewal", "Current expenses.", "9.9 mills",
           "10 years, commencing in 2027", "2028", "$3,633,339 a year; $196 for each $100,000 of market value",
           area="Northeastern Local School District (precincts 007/3, 008/3, 008/4, 009/3, 013/1, 027/1, 028/1, 029/1, 032/1)", src=I)
    c.levy("four-county-adamhs", "Four County ADAMhs Board (Defiance, Fulton, Henry and Williams)", "county", "Renewal",
           "Current expenses of the Four County Board of Alcohol, Drug Addiction and Mental Health Services District.", "0.7 mill",
           "5 years, commencing in 2027", "2028", "$2,293,020 a year; $13 for each $100,000 of market value", area="Defiance County", src=I)
    return c
