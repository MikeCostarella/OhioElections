from lib import County, NOTE_ORDER, NOTE_PLACES

SITE = "https://www.boe.ohio.gov/auglaize/"
NOTICE = "https://www.boe.ohio.gov/auglaize/c/upload/FWAB_11November46Day.pdf"
FWAB = "https://www.boe.ohio.gov/auglaize/election-info/federal-write-in-absentee-ballots/"


def build():
    # Default display names are right: "ST MARYS TOWNSHIP" -> "St. Marys Township", "ST. MARYS CITY" -> "St. Marys City".
    c = County("auglaize", "Auglaize", "39011")
    c.src("auglaize-46day", "Auglaize County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election (revised 9/3/2026)", NOTICE)
    S = ["auglaize-46day"]
    c.links = [
        {"label": "Board of Elections", "url": SITE},
        {"label": "Election information", "url": "https://www.boe.ohio.gov/auglaize/election-info/"},
        {"label": "Federal write-in absentee ballot notices", "url": FWAB},
        {"label": "Sample ballots by precinct", "url": "https://lookup.boe.ohio.gov/vtrapp/auglaize/ballotlist.aspx"},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://www.boe.ohio.gov/auglaize/election-info/election-results/"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it "
               "and gives the full ballot wording of each issue.",
               NOTE_ORDER, NOTE_PLACES,
               "The Board's notice does not give local issue numbers; see your sample ballot for them."]
    P = c.p; D = c.district; SD = c.sd

    # All of Auglaize County is in the 4th Congressional and 12th Senate districts; the 12th Senate seat is not up in 2026.
    # The notice prints "TRACEY TACKETT (Non)"; named "Tracey L. Tackett" as in allen.py and the other 4th District counties.
    c.contest("congress-4", "U.S. House", "Representative to Congress", [("Jim Jordan", "REP"), ("Joshua D. Kolasinski", "DEM"), ("Tracey L. Tackett", "Nonparty")],
              detail="4th District", src=S)
    # House: the notice's precinct lists match the voter file (Duchouquet E/1 and W/1 in the 78th, Duchouquet W/2 in the 84th).
    c.contest("rep-78", "Ohio General Assembly", "State Representative", [("Jeffrey R. Givan", "DEM"), ("Matt Huffman", "REP")], detail="78th District", places=D("rep", 78), src=S)
    c.contest("rep-84", "Ohio General Assembly", "State Representative", [("Arienne C. Childrey", "DEM"), ("Angie King", "REP")], detail="84th District", places=D("rep", 84), src=S)
    c.contest("appeals-3-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Mark C. Miller", "REP")], detail="3rd District · full term commencing February 9, 2027", src=S)

    # --- County offices ---
    c.contest("commissioner", "County offices", "County Commissioner", [("Douglas A. Spencer", "REP")], detail="Full term commencing January 1, 2027", src=S)
    c.contest("auditor", "County offices", "County Auditor", [("Linda M. Bice", "REP")], detail="Full term commencing March 8, 2027", src=S)
    c.contest("prosecutor", "County offices", "County Prosecuting Attorney", [("Benjamin R. Elder", "REP")], detail="Unexpired term ending December 31, 2028", src=S)
    c.contest("treasurer", "County offices", "County Treasurer", [("Mandy Frank", "REP")], detail="Unexpired term ending September 3, 2029", src=S)
    NP = " · no party label on the ballot"
    # The notice prints "(Rep)" after Ferrall; Common Pleas judges carry no party label on the general-election ballot.
    c.contest("cp-gen", "Court of Common Pleas", "Judge of the Court of Common Pleas", ["Zach G. Ferrall"], detail="Full term commencing February 9, 2027" + NP, src=S)

    # --- Local issues (unnumbered in the notice; listed in the notice's order) ---
    c.levy("wapakoneta-parks", "City of Wapakoneta", P("WAPAKONETA CITY"), "Additional",
           "Improvement, operation and maintenance of the City's parks and recreation facilities (playgrounds, athletic fields, sports courts, shelter houses and restrooms, "
           "recreational programs, maintenance and operating expenses).", "2 mills", "5 years, commencing in 2026", "2027",
           "$508,100 a year; $70 for each $100,000 of market value", area="Wapakoneta City (Wapakoneta 1A–4B)", src=S)
    c.levy("logan-twp-roads", "Logan Township (unincorporated area)", P("LOGAN TOWNSHIP"), "Renewal",
           "General construction, reconstruction, resurfacing and repair of streets, roads and bridges.", "1 mill", "5 years, commencing in 2026", "2027",
           "$19,905 a year; $15 for each $100,000 of market value", area="Logan Township, unincorporated area (Logan 1–4)", src=S)
    c.levy("st-marys-twp-police", "St. Marys Township (unincorporated area)", P("ST MARYS TOWNSHIP"), "Additional",
           "Police: motor vehicles, communications and other equipment for a police department, or the cost of contracts with other subdivisions for police protection (R.C. 5705.19(J)).",
           "1.25 mills", "Continuing, commencing in 2026", "2027", "$173,617 a year; $44 for each $100,000 of market value",
           area="St. Marys Township, unincorporated area (St. Marys E/1, E/2, S/1, S/2, W/1)", src=S)
    c.levy("washington-twp-fire", "Washington Township (excluding New Knoxville Village)", P("WASHINGTON TOWNSHIP"), "Additional",
           "Fire apparatus, buildings, water supply, fire alarm lines, firefighters, ambulance equipment, and ambulance, paramedic or other emergency medical services.",
           "3 mills", "5 years, commencing in 2026", "2027", "$152,127 a year; $105 for each $100,000 of market value",
           area="Washington Township outside New Knoxville (Washington 1–3)", src=S)
    WT = P("WAYNE TOWNSHIP", "WAYNESFIELD VILLAGE")
    c.levy("wayne-twp-cemetery", "Wayne Township (including Waynesfield Village)", WT, "Renewal", "Maintaining and operating cemeteries.", "0.7 mill",
           "5 years, commencing in 2026", "2027", "$23,700 a year; $16 for each $100,000 of market value",
           area="Wayne Township and Waynesfield Village (Wayne 1, 2, Waynesfield)", src=S)
    c.levy("wayne-twp-fire", "Wayne Township (including Waynesfield Village)", WT, "Renewal",
           "Payment of firefighting companies and ambulance or emergency medical services operated by a firefighting company.", "0.75 mill",
           "5 years, commencing in 2026", "2027", "$18,940 a year; $13 for each $100,000 of market value",
           area="Wayne Township and Waynesfield Village (Wayne 1, 2, Waynesfield)", src=S)
    c.levy("new-knoxville-fire", "Village of New Knoxville", P("NEW KNOXVILLE VILLAGE"), "Additional",
           "Fire apparatus, resuscitators, underwater rescue equipment and other fire equipment, buildings, water supply, fire-alarm communications, "
           "firefighting, EMS, administrative or communications personnel, ambulance equipment, and ambulance, paramedic or other emergency medical services.",
           "3 mills", "5 years, commencing in 2026", "2027", "$75,693 a year; $105 for each $100,000 of market value", area="New Knoxville Village", src=S)
    SMC = P("ST. MARYS CITY")
    c.issue("liquor-st-marys-1b-guarnieri", "liquor", "City of St. Marys", "Local liquor option: Guarnieri Pizzeria (Sunday)", SMC, area="St. Marys precinct 1-B",
            text="Sunday sale of beer, wine and mixed beverages, and spirituous liquor by Guarnieri Pizzeria LLC, dba Guarnieri Pizzeria, holder of a D-5L permit, "
                 "operating a restaurant and pizzeria at 216 E. Spring St., St. Marys (by petition).", src=S)
    c.issue("liquor-st-marys-2b-duchess", "liquor", "City of St. Marys", "Local liquor option: St. Marys Duchess (Sunday)", SMC, area="St. Marys precinct 2-B",
            text="Sunday sale of wine and mixed beverages by Englefield, Inc., dba St. Marys Duchess, an applicant for a D-6 permit, "
                 "operating a carryout/grocery store at 1502 Executive Drive, St. Marys (by petition).", src=S)
    c.issue("liquor-st-marys-4a-roots", "liquor", "City of St. Marys", "Local liquor option: Roots Pub (Sunday)", SMC, area="St. Marys precinct 4-A",
            text="Sunday sale of wine and mixed beverages, and spirituous liquor by MRD Entertainment LLC, dba Roots Pub, an applicant for a D-6 permit, "
                 "operating a restaurant/bar at 223 E. Spring St., St. Marys (by petition).", src=S)
    c.issue("liquor-st-marys-4a-generations", "liquor", "City of St. Marys", "Local liquor option: Generations Cafe (Sunday)", SMC, area="St. Marys precinct 4-A",
            note="St. Marys precinct 4-A has two Sunday-sales questions on this ballot (Roots Pub and Generations Cafe).",
            text="Local option for a particular use at a business location (by petition): Sunday sale of wine and mixed beverages, and spirituous liquor by SOS Entertainment LLC, "
                 "dba Generations Cafe, an applicant for a D-6 permit, operating a restaurant/bar at 233 E. Spring St., St. Marys.", src=S)
    # Same issue as allen.py's spencerville-lsd-income-tax; the voter file puts Logan and Salem Township voters in the district, matching the notice (Salem/2, Logan/4).
    c.issue("spencerville-lsd-income-tax", "question", "Spencerville Local School District", "School district income tax: 1% renewal for 5 years, for current expenses",
            SD("SPENCERVILLE LOCAL SD (ALLEN)"), area="Spencerville Local School District (Auglaize County part: Logan 4, Salem 2)",
            text="Shall an annual income tax of 1% on the school district income of individuals be imposed by Spencerville Local School District, to renew an income tax "
                 "(or income taxes) expiring at the end of 2027 for 5 years, beginning January 1, 2028, for the purpose of current expenses?", src=S)
    return c
