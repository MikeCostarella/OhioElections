from lib import County, NOTE_ORDER, NOTE_PLACES

SITE = "https://www.boe.ohio.gov/clinton/"
NOTICE = "https://www.boe.ohio.gov/clinton/c/upload/FWAB_11November46Day.pdf"
ELECTION_NOTICE = "https://www.boe.ohio.gov/clinton/c/upload/Election_NoticeofElection.pdf"
BALLOTS = "https://lookup.boe.ohio.gov/vtrapp/clinton/ballotlist.aspx"


def build():
    # Raw names are clean. Harveysburg Village (2 voters) is shared with Warren; Lynchburg Village (1 voter) with Highland.
    c = County("clinton", "Clinton", "39027")
    c.src("clinton-46day", "Clinton County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election (revised 10/16/2026)", NOTICE)
    c.src("clinton-notices", "Clinton County Board of Elections: notices of election on issues, November 3, 2026 General Election (revised 10/6/2026)", ELECTION_NOTICE)
    c.src("clinton-ballots", "Clinton County Board of Elections: sample ballots by precinct, November 3, 2026 General Election", BALLOTS)
    S = ["clinton-46day"]; I = ["clinton-46day", "clinton-ballots", "clinton-notices"]
    c.links = [
        {"label": "Board of Elections", "url": SITE},
        {"label": "Election information", "url": "https://www.boe.ohio.gov/clinton/election-info/"},
        {"label": "Sample ballots by precinct", "url": BALLOTS},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://www.boe.ohio.gov/clinton/election-info/election-results/"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it, "
               "checked against the Board's notices of election and precinct sample ballots. Issue wording is the ballot's.",
               NOTE_ORDER, NOTE_PLACES,
               "Clinton County's ballots do not number local issues (only statewide Issue 3 is numbered)."]
    P = c.p; D = c.district; SD = c.sd
    NP = " · no party label on the ballot"
    TWPS = P("ADAMS TOWNSHIP", "CHESTER TOWNSHIP", "CLARK TOWNSHIP", "GREEN TOWNSHIP", "JEFFERSON TOWNSHIP", "LIBERTY TOWNSHIP", "MARION TOWNSHIP",
             "RICHLAND TOWNSHIP", "UNION TOWNSHIP", "VERNON TOWNSHIP", "WASHINGTON TOWNSHIP", "WAYNE TOWNSHIP", "WILSON TOWNSHIP")

    # --- Federal, state legislative, appeals ---
    # All of Clinton County is in the 1st Congressional, 71st House and 10th Senate districts; the 10th Senate seat is not up in 2026.
    c.contest("congress-1", "U.S. House", "Representative to Congress", [("Eric Conroy", "REP"), ("Greg Landsman", "DEM"), ("Nathan Weise", "LIB")],
              detail="1st District", src=S)
    c.contest("rep-71", "Ohio General Assembly", "State Representative", [("Levi Dean", "REP"), ("Krista Magaw", "DEM")], detail="71st District", src=S)
    # Same contests as butler.py/warren.py/clermont.py. Clinton's notice also lists withdrawn write-ins Victor M. Haddad and Curt Carl Hartman (left out).
    c.contest("appeals-12-0101", "Ohio Court of Appeals", "Judge of the Court of Appeals",
              [("Matthew Byrne", "REP", "Withdrew September 16, 2026; his name may still appear on the ballot, but votes for him will not count"),
               ("Willa Concannon", "Write-in")],
              detail="12th District (Butler, Brown, Clermont, Clinton, Fayette, Madison, Preble and Warren counties) · full term commencing January 1, 2027", src=S)
    c.contest("appeals-12-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Robert A. Hendrickson", "REP")],
              detail="12th District (Butler, Brown, Clermont, Clinton, Fayette, Madison, Preble and Warren counties) · full term commencing February 9, 2027", src=S)

    # --- County offices ---
    c.contest("commissioner", "County offices", "County Commissioner", [("Mike McCarty", "REP")], detail="Full term commencing January 1, 2027", src=S)
    c.contest("auditor", "County offices", "County Auditor", [("Terence G. Habermehl", "REP")], detail="Full term commencing March 9, 2027", src=S)
    c.contest("cp-probate-juv", "Court of Common Pleas", "Judge of the Court of Common Pleas, Probate/Juvenile Division", ["Chad L. Carey"],
              detail="Full term commencing February 9, 2027" + NP, src=S)

    est = lambda total, per: f"{total} a year; {per} for each $100,000 of the county auditor's market value"

    # --- Countywide ---
    # Same question as warren.py's issue-6 (Warren numbers it 6; unnumbered on Clinton's ballot).
    c.levy("issue-6", "Mental Health Recovery Board Serving Warren and Clinton Counties", "county", "Renewal", "Current expenses.", "1 mill", "5 years, commencing in 2027", "2028",
           estimate="$7,677,198 per year; $16 per $100,000 of market value", area="Clinton County",
           note="Issue 6 in Warren County; unnumbered on Clinton County's ballot.", src=I)
    c.levy("health-district", "Clinton County (Combined Health District)", "county", "Renewal",
           "Health programs of the Clinton County Combined Health District, including child and senior citizen services, control of communicable diseases, "
           "environmental health, health education, bioterrorism response and AIDS education.", "0.5 mill", "5 years, commencing in 2027", "2028",
           est("$458,176", "$9"), src=I)
    c.levy("senior-services", "Clinton County", "county", "Renewal",
           "Senior citizen services or facilities, including home-delivered meals, durable medical equipment, minor emergency home repairs, homemaker, personal care, "
           "medical transportation, chores, respite for caregivers, adult day care, assessment, case management and protective services.", "2.35 mills",
           "5 years, commencing in 2027", "2028", est("$2,696,096", "$57"), src=I)
    # The notice's precincts are every precinct of the 13 townships (the whole unincorporated area).
    c.issue("gas-aggregation", "question", "Clinton County (unincorporated area)", "Natural gas aggregation for the unincorporated area (opt-out)", TWPS,
            area="Unincorporated Clinton County (all township precincts)",
            text="Shall the Board of County Commissioners of Clinton County, Ohio, have the authority to aggregate the retail natural gas loads located in the "
                 "unincorporated area of Clinton County, and for that purpose, enter into service agreements to facilitate the sale and purchase of competitive "
                 "retail natural gas service, with automatic enrollment in the aggregation program unless an eligible customer affirmatively elects to opt out?", src=I)

    # --- School districts ---
    # The notice lists Clark/2, New Vienna/1, Green/2, Sabina A/1 and B/1, Richland/1, Union South A/2, Wayne/1 and /2, and Wilson/1.
    c.issue("east-clinton-lsd-income-tax", "question", "East Clinton Local School District", "School district income tax: 1.25% for 5 years, for current expenses",
            SD("EAST CLINTON LOCAL SD (CLINTON)"),
            text="Shall an annual income tax of 1.25 per cent on the earned income of individuals residing in the school district be imposed by East Clinton "
                 "Local School District, for 5 years, beginning January 1, 2027, for the purpose of current expenses?", src=I)
    # Same question as pickaway.py's and ross.py's miami-trace-renewal; in Clinton County only precinct Wayne/3 votes.
    c.levy("miami-trace-renewal", "Miami Trace Local School District (Fayette, Clinton, Highland, Pickaway and Ross)", SD("MIAMI TRACE LOCAL SD (FAYETTE)"), "Renewal",
           "Current operating expenses (fixed-sum levy of $1,900,000 a year).", "2.2 mills (estimated average)", "5 years, commencing in 2027", "2028",
           "$1,900,000 a year; $77 for each $100,000 of market value", area="Precinct Wayne/3",
           note="A fixed-sum levy renewing an existing levy. The county auditor certified the district's carry-over balance in excess of the preceding year's general fund expenditures as $0 (0%).",
           src=S + ["clinton-ballots"])

    # --- Joint fire district ---
    c.levy("blanchester-marion-fire", "Blanchester-Marion Township Joint Fire District", P("BLANCHESTER VILLAGE", "MARION TOWNSHIP"), "Renewal",
           "Fire protection, ambulance, paramedic or other emergency medical services.", "3.55 mills", "5 years, commencing in 2027", "2028",
           est("$308,493", "$55"), area="Blanchester A, B and C and Marion Township", src=I)

    # --- Cities and villages ---
    WIL = P("WILMINGTON CITY"); WIL_AREA = "Wilmington 1-A to 4-C"
    for ord_, where_, acres, text in [
        ("04", "on SR 730", "119.373",
         "Shall Ordinance No. O-26-04 proposing to change the zoning of real property located on SR 730 (119.373 Acres) in the City of Wilmington, Ohio, be approved?"),
        ("05", "at 1957 SR 730", "65.29",
         "Shall Ordinance No. O-26-05 proposing to change the zoning of real property located at 1957 SR 730 (65.29 acres) in the City of Wilmington, Ohio, be approved?"),
        ("06", "on McGuinn Road", "191.12",
         "Shall ordinance No. O-26-06 proposing to change the zoning of 191.12 acres of real property on McGuinn Road in Wilmington, Ohio, be approved?"),
        ("07", "on US 68 South", "170.11",
         "Shall Ordinance No. O-26-07 proposing to change the zoning of 170.11 acres of real property on US 68 South in Wilmington, Ohio, be approved?"),
    ]:
        c.issue(f"wilmington-referendum-o-26-{ord_}", "question", "City of Wilmington",
                f"Zoning referendum (by petition): Ordinance O-26-{ord_}, rezoning {acres} acres {where_} from Rural Residential to Light Industrial",
                WIL, area=WIL_AREA,
                note=f"Ordinance O-26-{ord_} was adopted by city council on February 19, 2026. A YES vote approves the ordinance; a NO vote rejects it.",
                text=text, src=I)
    c.levy("blanchester-cemeteries", "Village of Blanchester", P("BLANCHESTER VILLAGE"), "Additional", "Maintaining and operating cemeteries.", "1.25 mills",
           "4 years, commencing in 2026", "2027", est("$129,130", "$44"), area="Blanchester A, B and C", src=I)
    MID = P("MIDLAND VILLAGE")
    c.levy("midland-current", "Village of Midland", MID, "Renewal", "Current expenses.", "3 mills", "5 years, commencing in 2027", "2028",
           est("$9,088", "$61"), area="Precinct Jefferson/5", src=I)
    c.levy("midland-police", "Village of Midland", MID, "Renewal", "Providing and maintaining police protection.", "1 mill", "5 years, commencing in 2027", "2028",
           est("$5,120", "$35"), area="Precinct Jefferson/5", src=I)
    c.issue("sabina-income-tax", "question", "Village of Sabina", "Municipal income tax: continuing the existing 0.5% for 5 years, for the police department",
            P("SABINA VILLAGE"), area="Sabina A and B",
            text="Shall the Ordinance providing for the continuation of an existing 0.5 per cent levy on income for 5 years, beginning on July 1, 2027 and ending "
                 "June 30, 2032, for purpose of providing revenue to maintain the Police Department for the Village of Sabina, Ohio, be passed?", src=I)

    # --- Local liquor options ---
    c.issue("liquor-wilmington-2a-wawa", "liquor", "City of Wilmington", "Local liquor option: Wawa #7218 (Sunday sales)", WIL, area="Wilmington precinct 2-A",
            text="Shall the sale of wine and mixed beverages be permitted for sale on Sunday by Wawa Midwest doing business as Wawa # 7218 an applicant for a D6 "
                 "liquor permit authorizing off-premise sales who is engaged in the business of operating family-oriented, full-service convenience stores at "
                 "2094 Rombach Ave, Wilmington, OH 45177 in this precinct?", src=I)
    NV = P("NEW VIENNA VILLAGE")
    c.issue("liquor-new-vienna-pizza-patts", "liquor", "Village of New Vienna", "Local liquor option: Pizza Patts LLC (D-5 permit)", NV, area="New Vienna precinct",
            text="Shall the sale of beer, wine and mixed beverages, and spirituous liquor be permitted by Pizza Patts LLC an applicant for a D-5 liquor permit, who "
                 "is engaged in the business of operating a restaurant and pizzeria at 155 W Main St, New Vienna, OH 45159 in this precinct?", src=I)
    c.issue("liquor-new-vienna-pizza-patts-sunday", "liquor", "Village of New Vienna", "Local liquor option: Pizza Patts LLC (Sunday sales)", NV, area="New Vienna precinct",
            text="Shall the sale of beer, wine and mixed beverages, and spirituous liquor be permitted for sale on Sunday by Pizza Patts LLC an applicant for a D-6 "
                 "liquor permit who is engaged in the business of operating a restaurant and pizzeria at 155 W Main St, New Vienna, OH 45159 in this precinct?", src=I)
    return c
