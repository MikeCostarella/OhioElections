from lib import County, NOTE_ORDER, NOTE_PLACES

SITE = "https://www.boe.ohio.gov/logan/"
NOTICE = "https://www.boe.ohio.gov/logan/c/upload/FWAB_11November46Day.pdf"
BALLOTS = "https://lookup.boe.ohio.gov/vtrapp/logan/ballotlist.aspx"


def build():
    # Default display names are right ("MCARTHUR TWP" -> "McArthur Township", "VALLEY-HI VILLAGE" -> "Valley-Hi Village");
    # only DeGraff needs the Board's spelling.
    c = County("logan", "Logan", "39091", rename={"DEGRAFF VILLAGE": "DeGraff Village"})
    c.src("logan-46day", "Logan County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election (revised 9/17/2026)", NOTICE)
    c.src("logan-ballots", "Logan County Board of Elections: official sample ballots for all 69 precinct splits, November 3, 2026 (state ballot lookup)", BALLOTS)
    C = I = ["logan-46day", "logan-ballots"]
    B = ["logan-ballots"]
    c.links = [
        {"label": "Board of Elections", "url": SITE},
        {"label": "Candidates & issues", "url": "https://www.boe.ohio.gov/logan/election-info/candidates-issues/"},
        {"label": "Sample ballots by precinct", "url": BALLOTS},
        {"label": "Who are my elected officials?", "url": "https://lookup.boe.ohio.gov/vtrapp/logan/cnm.aspx"},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://www.boe.ohio.gov/logan/election-info/election-results/"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it "
               "and gives the full ballot wording of each issue, checked against the Board's sample ballots for all 69 precinct splits. "
               "The notice leaves out the State Senate (1st District) and Court of Appeals races, which are taken from the sample ballots.",
               NOTE_ORDER, NOTE_PLACES,
               "The Board's notice does not give local issue numbers."]
    P = c.p; D = c.district; SD = c.sd

    # --- Federal, state legislative, appeals (the 12th Senate seat is not on the ballot) ---
    # The notice prints no party for Tackett (an independent candidate), as in allen.py and union.py.
    c.contest("congress-4", "U.S. House", "Representative to Congress", [("Jim Jordan", "REP"), ("Joshua D. Kolasinski", "DEM"), ("Tracey L. Tackett", "Nonparty")],
              detail="4th District", src=C)
    # Not in the 46-day notice; on the sample ballots of the 28 precinct splits in the 83rd House District (same candidate as hancock.py).
    c.contest("senate-1", "Ohio General Assembly", "State Senator", [("Craig S. Riedel", "REP")], detail="1st District · full term commencing January 1, 2027",
              places=D("sen", 1), area="Bloomfield, Bokescreek, West Mansfield, McArthur, Richland, Belle Center, Rushcreek, Stokes, Lakeview, Washington, Russells Point, Huntsville",
              src=B)
    c.contest("rep-83", "Ohio General Assembly", "State Representative", [("Sheila Coressel", "DEM"), ("Ty Mathews", "REP")], detail="83rd District",
              places=D("rep", 83), area="Bloomfield, Bokescreek, West Mansfield, McArthur, Richland, Belle Center, Rushcreek, Stokes, Lakeview, Washington, Russells Point, Huntsville",
              src=C)
    c.contest("rep-85", "Ohio General Assembly", "State Representative", [("Tim Barhorst", "REP"), ("Victoria Maddox", "DEM")], detail="85th District",
              places=D("rep", 85), area="Bellefontaine, Harrison, Jefferson, Lake, Liberty, West Liberty, Miami/Quincy, DeGraff, Monroe, Perry, Pleasant, Union, Zane",
              src=C)
    # Not in the 46-day notice; on all 69 sample ballots (same race as hancock.py, allen.py and union.py).
    c.contest("appeals-3-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Mark C. Miller", "REP")], detail="3rd District · full term commencing February 9, 2027", src=B)

    # --- County offices ---
    c.contest("commissioner", "County offices", "County Commissioner", [("Michael E. Yoder", "REP")], detail="Term commencing January 1, 2027", src=C)
    c.contest("auditor", "County offices", "County Auditor", [("Jack Reser", "REP")], detail="Term commencing March 8, 2027", src=C)
    NP = " · no party label on the ballot"
    c.contest("cp-family", "Court of Common Pleas", "Judge of the Court of Common Pleas, Family Division", ["Miranda Warren", "Sarah J. Warren"],
              detail="Full 6-year term commencing February 9, 2027" + NP, src=C)

    # --- Issues (unnumbered in the Board's notice; listed in the notice's order) ---
    est = lambda total, per: f"{total} a year; {per} for each $100,000 of market value"
    c.levy("dd-levy", "Logan County", "county", "Additional", "Community developmental disabilities programs and services (Logan County Board of Developmental Disabilities).",
           "2 mills", "5 years, commencing in 2026", "2027", est("$4,200,000", "$70"), src=I)
    c.issue("sales-tax", "question", "Logan County", "County sales and use tax: renewal of 0.5% for 5 years for permanent improvements", "county",
            text="The Board of County Commissioners of Logan County proposes to levy a sales and use tax in the amount of 0.5% for the purpose of providing additional revenue "
                 "for the general fund for the acquisition, construction, equipping or repairing of a class or group of permanent improvements, to wit 25% for the county roads "
                 "and bridges and storm water improvements limited to the right of way, 25% for use by the Sheriff for safety forces services and equipment, infrastructure of "
                 "permanent improvements to service and protect the safety of all Logan County, 20% for township, roads and bridges and stormwater improvements within the right "
                 "of way, 20% for city and village roads and bridges and stormwater within the right of way and 10% for economic development and land use planning for a period "
                 "of 5 years. Shall the resolution of the Logan County Commissioners proposing the continuation of the current 0.5% sales and use tax be approved?", src=I)
    c.levy("west-liberty-current", "Village of West Liberty", P("WEST LIBERTY VILLAGE"), "Renewal", "Current expense.", "5 mills", "5 years, commencing in 2027", "2028",
           est("$130,000", "$89"), area="West Liberty 1", src=I)
    c.issue("bellefontaine-csd-income-tax", "question", "Bellefontaine City School District", "School district income tax: 1% on earned income, continuing, for current expenses",
            SD("BELLEFONTAINE CITY SD"), area="Bellefontaine (all wards), Harrison 1, Lake 1, Liberty 2, Union 1",
            text="Shall an annual income tax of 1% on the earned income of individuals residing in the school district be imposed by the Bellefontaine City School District, "
                 "for a continuing period of time, beginning January 1, 2027, for the purpose of current expenses?", src=I)
    c.levy("mcarthur-fire", "McArthur Township, excluding Huntsville", P("MCARTHUR TWP"), "Renewal", "Fire protection.", "1.25 mills", "3 years, commencing in 2026", "2027",
           est("$57,000", "$24"), area="McArthur 1 and 2", src=I)
    # The notice lists the Stokes, Lakeview, Washington and Russells Point precincts, all in Logan County.
    c.levy("indian-lake-ambulance", "Indian Lake Joint Ambulance District",
           P("STOKES TWP", "LAKEVIEW VILLAGE", "WASHINGTON TWP", "RUSSELLS POINT VILLAGE"), "Additional", "Emergency medical services.", "8 mills",
           "5 years, commencing in 2026", "2027", est("$4,150,000", "$280"),
           area="Stokes North 1, Stokes South-East 1, Stokes West 1–4, Lakeview 1, Washington North 1, Washington South 1, Russells Point 1", src=I)

    # --- Local liquor options ---
    SPEEDWAY = "7 Eleven, Inc., dba Speedway #42739H, {what}, who is engaged in the business of operating a carryout/grocery store at 1330 U.S. Highway 68 N, Bellefontaine"
    for id, title, text in [
        ("liquor-speedway", "Local liquor option: Speedway #42739H (beer, wine and mixed beverages)",
         "Sale of beer, wine and mixed beverages by " + SPEEDWAY.format(what="an applicant for C-1 and C-2 liquor permits") + "."),
        ("liquor-speedway-sunday", "Local liquor option: Speedway #42739H (Sunday, wine and mixed beverages)",
         "Sunday sale of wine and mixed beverages by " + SPEEDWAY.format(what="an applicant for a D-6 liquor permit") + "."),
    ]:
        c.issue(id, "liquor", "City of Bellefontaine", title, P("BELLEFONTAINE CITY"), area="Bellefontaine precinct Third Ward A", text=text, src=I)
    return c
