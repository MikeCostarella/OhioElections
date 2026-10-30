from lib import County, NOTE_ORDER, NOTE_PLACES

SITE = "https://www.unioncountyohio.gov/board-of-elections"
NOTICE = "https://www.unioncountyohio.gov/media/Agencies/Board%20of%20Elections/46%20Day%20notice%20With%20Candidates.pdf"
BALLOTS = "https://lookup.boe.ohio.gov/vtrapp/union/ballotlist.aspx"


def build():
    # Default display names are right: "DUBLIN CITY " (trailing space) -> "Dublin City", "PLAIN CITY VILLAGE" -> "Plain City Village".
    # Dublin and Plain City have no contests or issues of their own on Union County's ballot.
    c = County("union", "Union", "39159")
    c.src("union-46day", "Union County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election (revised 9/15/2026)", NOTICE)
    c.src("union-ballots", "Union County Board of Elections: official sample ballots for all 87 precinct splits, November 3, 2026 (state ballot lookup)", BALLOTS)
    C = I = ["union-46day", "union-ballots"]
    c.links = [
        {"label": "Board of Elections", "url": SITE},
        {"label": "Sample ballots by precinct", "url": BALLOTS},
        {"label": "Who are my elected officials?", "url": "https://lookup.boe.ohio.gov/vtrapp/union/cnm.aspx"},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://www.unioncountyohio.gov/departments/boe/boe-election-results"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it, "
               "checked against the Board's sample ballots for all 87 precinct splits (which give the full ballot wording).",
               NOTE_ORDER, NOTE_PLACES,
               "The Board's notice and sample ballots do not give local issue numbers."]
    P = c.p

    # --- Federal, state legislative, appeals (all of Union County is in each district; the 26th Senate seat is not on the ballot) ---
    # The notice and ballots print no party for Tackett (an independent candidate), as in allen.py.
    c.contest("congress-4", "U.S. House", "Representative to Congress", [("Jim Jordan", "REP"), ("Joshua D. Kolasinski", "DEM"), ("Tracey L. Tackett", "Nonparty")],
              detail="4th District", src=C)
    c.contest("rep-86", "Ohio General Assembly", "State Representative", [("Kent Halloran", "DEM"), ("Ben Weber", "REP")], detail="86th District", src=C)
    c.contest("appeals-3-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Mark C. Miller", "REP")], detail="3rd District · term commencing February 9, 2027", src=C)

    # --- County offices ---
    c.contest("commissioner", "County offices", "County Commissioner", [("Shaun M. Bailey", "REP")], detail="Term commencing January 1, 2027", src=C)
    c.contest("auditor", "County offices", "County Auditor", [("Andrea L. Weaver", "REP")], detail="Term commencing March 8, 2027", src=C)
    NP = " · no party label on the ballot"
    c.contest("cp-gen", "Court of Common Pleas", "Judge of the Court of Common Pleas, General Division", ["David Phillips"],
              detail="Term commencing February 9, 2027" + NP, src=C)
    c.contest("cp-probate-juvenile", "Court of Common Pleas", "Judge of the Court of Common Pleas, Probate and Juvenile Divisions", ["Rick Rodger"],
              detail="Term commencing February 9, 2027" + NP, src=C)

    # --- Issues (unnumbered in the Board's documents; listed in the notice's order) ---
    est = lambda total, per: f"{total} a year; {per} for each $100,000 of market value"
    # Darby 1 split 5 and Dover 2 split 3 are the parts of Marysville in those townships' precincts.
    c.issue("marysville-charter-referendum", "question", "City of Marysville", "Charter amendment (by petition): new Section 4.03, referendum petitions",
            P("MARYSVILLE CITY"), area="Marysville 1–18, Darby 1 (split 5), Dover 2 (split 3)",
            text="Shall Article IV, Section 4.03 of the Charter of the City of Marysville be enacted as follows: Section 4.03 Referendum Petition. The electors reserve to "
                 "themselves the powers of initiative and referendum to the extent permitted and by the procedure provided by this Charter and the Law and Constitution of Ohio. "
                 "Notwithstanding any other provision of this Charter or Ohio Law, whoever files a referendum petition regarding any proposed ordinance or measure shall not be "
                 "required to file a certified copy of the proposed ordinance or measure with the Director of Finance, or any person performing the function of city auditor for "
                 "the municipality, before circulating such petition. Notwithstanding any other provision of this Charter or Ohio law, a referendum petition must be signed by "
                 "ten percent of the number of electors in the city who voted for governor in the most recent general election for the office of governor in the municipal "
                 "corporation and must be filed with the Director of Finance.", src=I)
    c.levy("richwood-roads", "Village of Richwood", P("RICHWOOD VILLAGE"), "Renewal", "Maintaining and repairing roads.", "3 mills", "5 years, commencing in 2027", "2028",
           est("$99,400", "$63"), area="Richwood 1 and 2", src=I)
    c.levy("magnetic-springs-current", "Village of Magnetic Springs", P("MAGNETIC SPRINGS VILLAGE"), "Renewal", "Current operating expenses.", "5 mills",
           "5 years, commencing in 2027", "2028", est("$12,500", "$83"), area="Leesburg 3 (Magnetic Springs)", src=I)
    c.levy("jerome-police", "Jerome Township (unincorporated area)", P("JEROME TOWNSHIP"), "Renewal",
           "Police protection as a result of contracts made with other political subdivisions.", "1.2 mills", "5 years, commencing in 2027", "2028",
           est("$662,900", "$19"), area="Jerome 1–10 (unincorporated area)", src=I)
    c.levy("millcreek-police", "Millcreek Township", P("MILLCREEK TOWNSHIP"), "Renewal", "Police protection provided by the Union County Sheriff's Office.", "2.15 mills",
           "5 years, commencing in 2027", "2028", est("$122,500", "$50"), area="Millcreek 1–3", src=I)
    c.levy("paris-fire", "Paris Township (unincorporated area)", P("PARIS TOWNSHIP"), "Renewal",
           "Fire protection, firefighting and emergency medical services: fire apparatus, appliances, buildings and sites, water supply, fire-alarm telegraph, firefighting and "
           "EMS personnel, ambulance equipment and services, and the costs of contracts with other political subdivisions for police protection.",
           "5.9 mills", "3 years, commencing in 2027", "2028", est("$311,000", "$104"), area="Paris (unincorporated area)", src=I)
    c.levy("union-twp-current", "Union Township (including the Village of Milford Center)", P("UNION TOWNSHIP", "MILFORD CENTER VILLAGE"), "Renewal", "Current expenses.",
           "1 mill", "5 years, commencing in 2027", "2028", est("$35,200", "$13"), area="Union, Milford Center", src=I)
    c.levy("york-twp-current", "York Township", P("YORK TOWNSHIP"), "Renewal", "Current expenses.", "1 mill", "5 years, commencing in 2027", "2028",
           est("$53,100", "$20"), area="York 1–5", src=I)
    # The notice lists only Richwood 1, Richwood 2 and Claibourne; the Board's sample ballots also carry this levy in Jackson and York 4 and 5.
    c.levy("nuc-fire", "Northern Union County Joint Fire and EMS District", P("RICHWOOD VILLAGE", "CLAIBOURNE TOWNSHIP", "JACKSON TOWNSHIP", "YORK TOWNSHIP"), "Additional",
           "Fire protection, firefighting and emergency medical services: fire apparatus, mechanical resuscitators, underwater rescue and recovery equipment, buildings and sites, "
           "water supply, fire-alarm communications, firefighting, EMS, administrative and communications personnel, ambulance equipment and services.",
           "3 mills", "Continuing period of time, commencing in 2026", "2027", est("$619,000", "$105"), area="Richwood 1 and 2, Claibourne, Jackson, York 4 and 5",
           note="The Board's 46-day notice lists Richwood 1, Richwood 2 and Claibourne; its sample ballots also include Jackson and York 4 and 5.", src=I)
    # Same levy as delaware.py's dacc-levy; in Union County only Millcreek 3 votes on it.
    c.levy("dacc-levy", "Delaware Area Career Center (joint vocational school district; Delaware, Franklin, Marion, Morrow and Union counties)", P("MILLCREEK TOWNSHIP"),
           "Renewal and decrease",
           "Improving, renovating, remodeling, enlarging, furnishing and equipping school buildings and facilities (0.40 mill) and current expenses (0.35 mill); renewal of part of an existing levy, a reduction of 0.95 mill.",
           "0.75 mill", "10 years, commencing in 2026", "2027", est("$5,773,576", "$18"), area="Millcreek 3", src=I)

    # --- Local liquor options ---
    MEIJER = ("Meijer Store Limited Partnership, doing business as Meijer, {what}, family-owned grocery & home goods superstore at or near the NE corner of US 33 & Hyland Croy Rd. "
              "(Parcel #1700310390010), Jerome Twp., Plain City")
    for id, jur, raw, prec, title, text in [
        ("liquor-chefs-parlour", "Village of Richwood", "RICHWOOD VILLAGE", "Richwood 2", "Local liquor option: Chefs' Parlour (Sunday)",
         "Sunday sale of wine and mixed beverages, and spirituous liquor by Chefs' Parlour LLC, applicant for a D-6 permit, restaurant and bar at 2 S. Franklin St, Richwood."),
        ("liquor-happenstance", "City of Marysville", "MARYSVILLE CITY", "Marysville 6", "Local liquor option: Happenstance Brewing Project (Sunday)",
         "Sunday sale of wine and mixed beverages, and spirituous liquor by Dubbel Tap LLC dba Happenstance Brewing Project, applicant for a D-6 permit, brewery/brewpub at 410 E 4th St., Marysville."),
        ("liquor-meijer", "Jerome Township", "JEROME TOWNSHIP", "Jerome 10", "Local liquor option: Meijer (spirituous liquor)",
         "Sale of spirituous liquor by " + MEIJER.format(what="operator of a State of Ohio liquor agency store") + "."),
        ("liquor-meijer-sunday-spirits", "Jerome Township", "JEROME TOWNSHIP", "Jerome 10", "Local liquor option: Meijer (Sunday, spirituous liquor)",
         "Sunday sale of spirituous liquor by " + MEIJER.format(what="applicant for a State of Ohio liquor agency store") + "."),
        ("liquor-meijer-sunday-wine", "Jerome Township", "JEROME TOWNSHIP", "Jerome 10", "Local liquor option: Meijer (Sunday, wine and mixed beverages)",
         "Sunday sale of wine and mixed beverages by " + MEIJER.format(what="applicant for a D-6 permit") + "."),
    ]:
        c.issue(id, "liquor", jur, title, P(raw), area=prec, text=text, src=I)
    return c
