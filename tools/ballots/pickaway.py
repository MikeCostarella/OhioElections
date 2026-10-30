from lib import County, NOTE_ORDER, NOTE_PLACES

SITE = "https://www.boe.ohio.gov/pickaway/"
NOTICE = "https://www.boe.ohio.gov/pickaway/c/upload/FWAB_11November46Day.pdf"
BALLOTS = "https://lookup.boe.ohio.gov/vtrapp/pickaway/ballotlist.aspx"

APPEALS_4 = "4th District"


def build():
    # Raw SoS names mix "... TWP" and "... TOWNSHIP" ("DARBY TOWNSHIP", "DEERCREEK TOWNSHIP"); both display as "... Township".
    # "HARRISBURG VILLAGE " and "NEW HOLLAND VILLAGE " have trailing spaces, which display() strips. Deercreek and Saltcreek
    # are spelled as one word by the Board too, so no renames are needed.
    c = County("pickaway", "Pickaway", "39129")
    c.src("pickaway-46day", "Pickaway County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election (revised September 8, 2026)", NOTICE)
    c.src("pickaway-ballots", "Pickaway County Board of Elections: precinct sample ballots, November 3, 2026 General Election (election data updated October 5, 2026)", BALLOTS)
    S = ["pickaway-46day", "pickaway-ballots"]
    c.links = [
        {"label": "Board of Elections", "url": SITE},
        {"label": "Federal write-in absentee ballot notices", "url": "https://www.boe.ohio.gov/pickaway/election-info/federal-write-in-absentee-ballots/"},
        {"label": "Sample ballots by precinct", "url": BALLOTS},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://www.boe.ohio.gov/pickaway/election-info/election-results/"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it, "
               "checked against the Board's precinct sample ballots. Issue wording is from the sample ballots.",
               NOTE_ORDER, NOTE_PLACES,
               "The Board's notice and sample ballots do not give local issue numbers.",
               "Court of Appeals: the 46-day notice lists Peter B. Abele (Republican) for the 4th District seat, but the Board's sample ballots list "
               "Jayme Hartley Fountain (Republican) and Todd L. Grace (Democratic); the sample ballots are shown here."]
    P = c.p; D = c.district; SD = c.sd

    # --- Federal, state legislative, appeals (every precinct is in the 15th Congressional, 3rd Senate, 12th House and 4th Appeals districts) ---
    c.contest("congress-15", "U.S. House", "Representative to Congress", [("Brennan Barrington", "LIB"), ("Mike Carey", "REP"), ("Don Leonard", "DEM")],
              detail="15th District", places=D("cong", 15), src=S)
    c.contest("senate-3", "Ohio General Assembly", "State Senator", [("Stacie A. Baker", "DEM"), ("Michele Reynolds", "REP")],
              detail="3rd District", places=D("sen", 3), src=S)
    c.contest("rep-12", "Ohio General Assembly", "State Representative", [("Brian Stewart", "REP"), ("Lee Yarsky", "DEM")],
              detail="12th District", places=D("rep", 12), src=S)
    # The notice (revised 9/8/2026) lists Peter B. Abele; the sample ballots (data of 10/5/2026) list Fountain and Grace, as in Ross and Scioto.
    c.contest("appeals-4-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Jayme Hartley Fountain", "REP"), ("Todd L. Grace", "DEM")],
              detail=APPEALS_4 + " · full term commencing February 9, 2027", src=["pickaway-ballots", "pickaway-46day"])

    # --- County (write-ins Sherri Fahringer for Commissioner and Seth Yates for Coroner are not listed) ---
    c.contest("commissioner", "County offices", "County Commissioner", [("Jay H. Wippel", "REP")], detail="Full term commencing January 1, 2027", src=S)
    c.contest("auditor", "County offices", "County Auditor", [("Brad Washburn", "REP")], detail="Full term commencing March 8, 2027", src=S)
    c.contest("coroner", "County offices", "Coroner", [("Brad Cotton", "DEM")], detail="Unexpired term ending December 31, 2028", src=S)
    NP = " · no party label on the ballot"
    c.contest("cp-probate-juvenile", "Court of Common Pleas", "Judge of the Court of Common Pleas, Juvenile and Probate Division", ["Shelly R. Harsha"],
              detail="Full term commencing February 9, 2027" + NP, src=S)

    # --- Issues (unnumbered; listed in the notice's order) ---
    est = lambda total, per, basis="market": f"{total} a year; {per} for each $100,000 of {basis} value"
    c.levy("pickaway-parks", "Pickaway County Park District", "county", "Renewal and increase",
           "Parks and recreation: maintaining existing facilities, developing new trails and parks, and helping cities, villages and townships improve their parks and trails "
           "(renewal of 0.5 mill and an increase of 0.25 mill).", "0.75 mill", "10 years, commencing in 2027", "2028", est("$1,466,613", "$20"), src=S)
    c.issue("ashville-edgeconnex-referendum", "question", "Village of Ashville", "Referendum (by petition): EdgeConneX development and supply agreement term summary",
            P("ASHVILLE VILLAGE"), area="Ashville precincts Ashville-East, Ashville-Northeast, Ashville-Northwest and Ashville-West",
            text="Referendum on a Village Council resolution approving a Development and Supply Agreement Term Summary with EdgeConneX, which intends to build two data "
                 "center buildings on about 195 acres in the village and, through an affiliate, a natural gas behind-the-meter power generating facility on the property. "
                 "Shall the resolution enacting approval of a development and supply agreement term summary with EdgeConneX be approved?", src=S)
    NH = P("NEW HOLLAND VILLAGE ")
    c.levy("new-holland-cemetery", "Village of New Holland (Pickaway and Fayette)", NH, "Renewal", "Maintaining and operating a cemetery.", "1 mill",
           "5 years, commencing in 2027", "2028", est("$8,562", "$15"), area="Precinct Perry/New Holland 1", src=S)
    c.levy("williamsport-ems", "Village of Williamsport", P("WILLIAMSPORT VILLAGE"), "Renewal", "Ambulance service, emergency medical service, or both.", "3.65 mills",
           "5 years, commencing in 2027", "2028", est("$101,403", "$96"), area="Precinct Deercreek/Williamsport 1", src=S)
    c.levy("monroe-twp-fire", "Monroe Township", P("MONROE TWP"), "Additional",
           "Fire apparatus, equipment, buildings and sites, fire-alarm communications, firefighting and emergency medical personnel, ambulance equipment "
           "and ambulance, paramedic or other emergency medical services.", "1.75 mills", "5 years, commencing in 2027", "2028", est("$186,540", "$61"), src=S)
    c.levy("walnut-twp-cemeteries", "Walnut Township", P("WALNUT TWP"), "Renewal", "Maintaining and operating township cemeteries.", "0.4 mill",
           "5 years, commencing in 2027", "2028", est("$72,913", "$8"), area="Walnut Township precincts Walnut-East and Walnut-West", src=S)
    c.levy("miami-trace-renewal", "Miami Trace Local School District (Fayette, Clinton, Highland, Pickaway and Ross)", SD("MIAMI TRACE LOCAL SD (FAYETTE)"), "Renewal",
           "Current operating expenses (fixed-sum levy of $1,900,000 a year).", "2.2 mills (estimated average)", "5 years, commencing in 2027", "2028",
           "$1,900,000 a year; $77 for each $100,000 of market value", area="Precincts Perry/New Holland 1 and 2", src=S)
    # Same issue as Franklin County's Issue 6 (franklin.py); unnumbered on Pickaway's ballot. The voter file puts part of
    # Darby Township and Harrisburg Village's Pickaway voters in the South-Western City School District.
    c.issue("issue-6", "levy", "South-Western City School District (Franklin and Pickaway)", "Bond issue: $220,000,000 for new Westland and Grove City high schools and other school facilities",
            SD("SOUTH-WESTERN CITY SD"), area="Precincts Darby-North 2 and 3",
            levy={"type": "Bond issue", "purpose": "Constructing, furnishing and equipping a new Westland High School and new Grove City High School, with related site improvements; constructing, renovating, repairing, expanding and improving other school facilities.",
                  "mills": "2.26 mills (estimated average)", "term": "Up to 38 years", "firstDue": "2027", "estimate": "$220,000,000 principal; $79 for each $100,000 of market value"},
            note="Issue 6 in Franklin County; unnumbered on Pickaway County's ballot.", src=S)
    c.levy("deercreek-twp-roads", "Deercreek Township (excluding the Village of Williamsport)", P("DEERCREEK TOWNSHIP"), "Additional",
           "General construction, reconstruction, resurfacing and repair of streets, roads and bridges.", "3 mills", "5 years, commencing in 2026", "2027",
           est("$123,801", "$105"), area="Precincts Deercreek/Williamsport 2 and 3",
           note="The 46-day notice gives $122,019 a year, \"appraised value\" and a term commencing in 2025 (first due 2026); the sample ballot's figures are shown.", src=S)
    c.levy("perry-twp-roads", "Perry Township (excluding the Village of New Holland)", P("PERRY TWP"), "Additional",
           "General construction, reconstruction, resurfacing and repair of streets, roads and bridges.", "2.5 mills", "5 years, commencing in 2027", "2028",
           est("$75,623", "$88"), area="Precincts Perry/New Holland 2, 3 and 4", src=S)
    # Special districts placed from the notice's precinct lists: precinct Perry/New Holland 1 is the New Holland Village precinct
    # (it alone votes on the village cemetery levy); Darby Clarks Lake, Darby-North 1-2 and Darby-South are Darby Township precincts.
    c.levy("fayette-ems-renewal", "Fayette County Emergency Medical Service District (Fayette and Pickaway)", NH, "Renewal",
           "Ambulance service, emergency medical service, or both.", "1.90 mills", "3 years, commencing in 2027", "2028", est("$1,482,933", "$49"),
           area="Precinct Perry/New Holland 1", src=S)
    DARBY = P("DARBY TOWNSHIP"); DARBY_AREA = "Precincts Darby Clarks Lake, Darby-North 1 and 2, and Darby-South"
    c.levy("sterling-ambulance-renewal", "Sterling Joint Ambulance District", DARBY, "Renewal", "Current expenses.", "1.8 mills", "5 years, commencing in 2027", "2028",
           est("$489,825", "$36", "appraised"), area=DARBY_AREA, src=S)
    c.levy("tri-county-fire-additional", "Tri-County Joint Fire District", DARBY, "Additional",
           "Current expenses; fire apparatus, equipment, buildings and sites, fire-alarm communications, firefighting and emergency medical personnel, "
           "ambulance equipment and ambulance, paramedic or other emergency medical services.", "2.5 mills", "5 years, commencing in 2027", "2028",
           est("$710,410", "$88"), area=DARBY_AREA, src=S)
    # Harrisburg Village's Pickaway voters are in the South-Western district, which votes only in Darby-North 2 and 3, so they are in precinct Darby-North.
    c.issue("liquor-laxmi-mart", "liquor", "Darby Township", "Local liquor option: Laxmi Mart (Harrisburg Marathon Mart) (Sunday)", P("DARBY TOWNSHIP", "HARRISBURG VILLAGE "),
            area="Precinct Darby-North (all splits)",
            text="Shall the sale of wine and mixed beverages be permitted for sale on Sunday by Laxmi Mart, L.L.C. (dba Harrisburg Marathon Mart), an applicant for a D-6 liquor permit "
                 "operating a carryout/grocery store at 9109 U.S. 62, Orient (Darby Township), in this precinct?", src=S)
    ASH = P("ASHVILLE VILLAGE")
    c.issue("liquor-ashville-east-sunday", "liquor", "Village of Ashville", "Local liquor option: Sunday sales in precinct Ashville East", ASH, area="Ashville precinct Ashville-East",
            text="Shall the sale of intoxicating liquor, of the same types as may be legally sold in this precinct on other days of the week, be permitted in Ashville East for "
                 "consumption on the premises where sold, on Sunday, at licensed premises where the sale of food and other goods and services exceeds fifty percent of the "
                 "total gross receipts of the permit holder at the premises?", src=S)
    c.issue("liquor-off-the-rails", "liquor", "Village of Ashville", "Local liquor option: Off The Rails (Sunday)", ASH, area="Ashville precinct Ashville-West",
            text="Shall the sale of wine and mixed beverages, and spirituous liquor be permitted for sale on Sunday by Xenial, L.L.C., dba Off The Rails, an applicant for a D-6 "
                 "liquor permit operating a bar/restaurant at 60 W. Main Street, Ashville, in this precinct?", src=S)
    return c
