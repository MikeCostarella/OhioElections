from lib import County, NOTE_ORDER, NOTE_PLACES

NOTICE = "https://www.boe.ohio.gov/clark/c/upload/FWAB_11November46Day.pdf"

def build():
    # Raw names are clean ("SPRINGFIELD CITY", "TREMONT CITY VILLAGE" -> "Tremont City Village"); no renames needed.
    c = County("clark", "Clark", "39023")
    c.src("clark-46day", "Clark County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election", NOTICE)
    S = ["clark-46day"]
    c.links = [
        {"label": "Board of Elections", "url": "https://www.boe.ohio.gov/clark/"},
        {"label": "Election info", "url": "https://www.boe.ohio.gov/clark/election-info/"},
        {"label": "Sample ballots by precinct", "url": "https://lookup.boe.ohio.gov/vtrapp/clark/ballotlist.aspx"},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://www.boe.ohio.gov/clark/election-info/election-results/"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it. "
               "Issue wording is the Board's summary; the full wording is on the sample ballot.",
               NOTE_ORDER, NOTE_PLACES,
               "The Board's notice does not give local issue numbers; see your sample ballot for them."]
    P = c.p; D = c.district; SD = c.sd

    # 4th and 15th Congressional, 71st and 74th House districts; the 10th Senate district is not up in 2026.
    # The notice prints no party for Tackett (an independent candidate) and spells him "Tracy"; Delaware and Richland list "Tracey L. Tackett".
    c.contest("congress-4", "U.S. House", "Representative to Congress", [("Jim Jordan", "REP"), ("Joshua D. Kolasinski", "DEM"), ("Tracey L. Tackett", "Nonparty")],
              detail="4th District", places=D("cong", 4), src=S)
    c.contest("congress-15", "U.S. House", "Representative to Congress", [("Brennan Barrington", "LIB"), ("Mike Carey", "REP"), ("Don Leonard", "DEM")],
              detail="15th District", places=D("cong", 15), src=S)
    c.contest("rep-71", "Ohio General Assembly", "State Representative", [("Levi Dean", "REP"), ("Krista Magaw", "DEM")], detail="71st District", places=D("rep", 71), src=S)
    c.contest("rep-74", "Ohio General Assembly", "State Representative", [("Darrell E. Jackson", "DEM"), ("Bernard Willis", "REP")], detail="74th District", places=D("rep", 74), src=S)
    c.contest("appeals-2-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Chris Epley", "REP")], detail="2nd District · term commencing February 9, 2027", src=S)
    c.contest("commissioner", "County offices", "County Commissioner", [("Sasha Rittenhouse", "REP"), ("Bradley Soles", "DEM")], src=S)
    # Seth Evans has no party on the notice: he filed as an independent.
    c.contest("commissioner-unexpired", "County offices", "County Commissioner", [("Seth Evans", "Nonparty"), ("Greg R. Kaffenbarger", "REP")],
              detail="Unexpired term ending January 1, 2029", src=S)
    c.contest("auditor", "County offices", "County Auditor", [("Hillary Hamilton", "REP")], src=S)
    c.contest("recorder", "County offices", "County Recorder", [("Bonnie Sakaitis", "REP")], detail="Unexpired term ending December 31, 2028", src=S)
    c.contest("coroner", "County offices", "County Coroner", [("Aamir Khan", "DEM"), ("Joel Macy", "REP")], detail="Unexpired term ending December 31, 2028", src=S)
    NP = " · no party label on the ballot"
    c.contest("cp-probate", "Court of Common Pleas", "Judge of the Court of Common Pleas, Probate Division", ["Richard P. Carey"], detail="No party label on the ballot", src=S)

    # --- Local issues (unnumbered in the notice) ---
    HT = P("HARMONY TOWNSHIP", "SOUTH VIENNA VILLAGE")
    HJ = "Harmony Township (including the Village of South Vienna)"
    HA = "Harmony Township and South Vienna Village (Harm 1 and Harm 2)"
    c.levy("harmony-ems-69816", HJ, HT, "Renewal", "Ambulance service and emergency medical services.", "1 mill", "5 years, commencing in 2027", "2028",
           "$69,816 a year; $35 for each $100,000 of appraised value", area=HA, src=S)
    c.levy("harmony-ems-73201", HJ, HT, "Renewal", "Ambulance service and emergency medical services.", "1 mill", "5 years, commencing in 2027", "2028",
           "$73,201 a year; $35 for each $100,000 of appraised value", area=HA, note="Harmony Township has two 1-mill ambulance/EMS renewals on this ballot.", src=S)
    c.levy("green-ems", "Green Township (including the Village of Clifton)", P("GREEN TOWNSHIP", "CLIFTON VILLAGE"), "Additional", "Ambulance service, emergency medical service, or both.",
           "1.5 mills", "5 years, commencing in 2026", "2027", "$204,302 a year; $53 for each $100,000 of market value",
           area="Green Township and Clifton Village, Clark County part (Green 1 and 2)", src=S)
    # The notice adds Springfield City precincts 1 (split 2) and 26 (splits 2 and 3) to the township's own T-1 to T-8.
    c.levy("springfield-twp-police", "Springfield Township", P("SPRINGFIELD TOWNSHIP", "SPRINGFIELD CITY"), "Additional", "Police protection.", "0.5 mill",
           "5 years, commencing in 2026", "2027", "$245,685 a year; $18 for each $100,000 of market value",
           area="Springfield Township (T-1 to T-8), plus Springfield City 1 (split 2) and 26 (splits 2 and 3)", src=S)
    c.issue("clark-shawnee-lsd-tax", "question", "Clark-Shawnee Local School District", "School district income tax: 0.5% on earned income for 5 years, for current expenses",
            SD("CLARK-SHAWNEE LOCAL SD (CLARK)"), area="Clark-Shawnee Local School District (Springfield City parts, Bethel 6 split 3, Springfield Township)",
            text="Annual income tax of 0.5% on the earned income of individuals residing in the school district, for 5 years, beginning January 1, 2027, for current expenses.", src=S)
    # Same issue as greene.py's southeastern-lsd-tax. Clark's voter file labels the district correctly.
    c.issue("southeastern-lsd-tax", "question", "Southeastern Local School District (Clark and Greene)", "School district income tax: 0.5% for 5 years, for current expenses",
            SD("SOUTHEASTERN LOCAL SD (CLARK)"), area="Southeastern Local School District (Gree 2 split 1, Harm 1 split 2, Harm 2 split 3, Chas, Chas Twp)",
            text="Proposed income tax of 0.50% on the school district income of individuals, for 5 years, beginning January 1, 2027, for current expenses.", src=S)
    c.levy("bethel-police", "Bethel Township (unincorporated area)", P("BETHEL TOWNSHIP"), "Renewal", "Police protection, including ambulance or emergency medical services operated by a police department.",
           "1.75 mills", "5 years, commencing in 2027", "2028", "$398,541 a year; $61 for each $100,000 of market value",
           area="Bethel Township unincorporated area (Beth 1–4, Beth 5 split 1, Beth 6)", src=S)
    BT = P("BETHEL TOWNSHIP", "DONNELSVILLE VILLAGE")
    BJ = "Bethel Township (unincorporated area, including the Village of Donnelsville)"
    for id, amt, basis in [("bethel-fire-370217", "$370,217", "appraised"), ("bethel-fire-415580", "$415,580", "market"), ("bethel-fire-219729", "$219,729", "market")]:
        c.levy(id, BJ, BT, "Renewal", "Fire protection and ambulance, paramedic or other emergency medical services.", "2 mills", "5 years, commencing in 2027", "2028",
               f"{amt} a year; $70 for each $100,000 of {basis} value", area="Bethel Township and Donnelsville Village (Beth 1–6)",
               note="Bethel Township has three 2-mill fire renewals on this ballot.", src=S)
    c.levy("donnelsville-current", "Village of Donnelsville", P("DONNELSVILLE VILLAGE"), "Renewal", "Current operating expenses.", "7 mills", "5 years, commencing in 2027", "2028",
           "$28,661 a year; $245 for each $100,000 of market value", area="Donnelsville Village (Beth 5 split 2)", src=S)
    c.issue("south-charleston-income-tax", "question", "Village of South Charleston", "Municipal income tax: 0.25% renewal for 9 years, for streets and public highways",
            P("SOUTH CHARLESTON VILLAGE"), area="South Charleston Village (Chas 1)",
            text="Continue an existing 0.25% levy on income for 9 years, commencing January 1, 2027, for the care, supervision and control of public highways, streets, avenues, alleys, sidewalks, "
                 "public grounds, bridges, aqueducts and viaducts within the Village of South Charleston.", src=S)
    c.issue("new-carlisle-income-tax", "question", "City of New Carlisle", "Municipal income tax: additional 0.5% for fire and emergency medical services", P("NEW CARLISLE CITY"),
            area="New Carlisle City (Carl 1–5)", text="Ordinance providing for a 0.5% levy on income for fire and emergency medical services.", src=S)
    NW = SD("NORTHWESTERN LOCAL SD (CLARK)")
    NWA = "Northwestern Local School District (Germ 1–5, Mfld 4 split 2, Pike 1 split 1, Pike 2)"
    c.levy("northwestern-lsd-pi", "Northwestern Local School District", NW, "Renewal", "Permanent improvements.", "1 mill", "5 years, commencing in 2026", "2027",
           "$225,394 a year; $35 for each $100,000 of market value", area=NWA, src=S)
    c.levy("northwestern-lsd-current", "Northwestern Local School District", NW, "Renewal", "Current operating expenses (fixed sum of $1,756,160).", "4.32 mills (estimated average)",
           "5 years, commencing in 2026", "2027", "$151 for each $100,000 of market value", area=NWA, src=S)
    c.levy("german-police", "German Township (excluding the Village of Tremont City)", P("GERMAN TOWNSHIP"), "Additional", "Police protection, including ambulance or emergency medical services operated by a police department.",
           "1 mill", "5 years, commencing in 2026", "2027", "$133,459 a year; $35 for each $100,000 of market value",
           area="German Township unincorporated area (Germ 1–4, Germ 5 split 1)", src=S)
    c.levy("pleasant-ems", "Pleasant Township (including the Village of Catawba)", P("PLEASANT TOWNSHIP", "CATAWBA VILLAGE"), "Renewal",
           "Ambulance or emergency medical services operated by a fire department or firefighting company.", "1.8 mills", "5 years, commencing in 2027", "2028",
           "$93,774 a year; $63 for each $100,000 of market value", area="Pleasant Township and Catawba Village (Ples 1 and 2)", src=S)
    c.levy("tecumseh-lsd-current", "Tecumseh Local School District", SD("TECUMSEH LOCAL SD (CLARK)"), "Renewal", "Current operating expenses (fixed sum of $712,000).", "1.31 mills (estimated average)",
           "5 years, commencing in 2027", "2028", "$46 for each $100,000 of market value",
           area="Tecumseh Local School District (Carl 1–5, Beth 1–5, Beth 6 splits 1 and 2, Pike 1 split 2)", src=S)
    c.issue("springfield-gas-aggregation", "question", "City of Springfield", "Natural gas aggregation (opt-out)", P("SPRINGFIELD CITY"),
            area="Springfield City 1–27, plus T-5 split 2, T-7 split 2 and T-8 split 2",
            text="Authority to aggregate the retail natural gas loads in the City of Springfield and enter into service agreements for the sale and purchase of natural gas, "
                 "with aggregation occurring automatically except where a person elects to opt out.", src=S)
    c.levy("health-district", "Clark County Combined Health District (excluding the City of New Carlisle)", [x for x in c.places if x != "New Carlisle City"], "Renewal",
           "Health district programs.", "1 mill", "5 years, commencing in 2027", "2028", "$2,663,976 a year; $35 for each $100,000 of appraised value",
           area="All of Clark County except New Carlisle (Carl 1–5)", src=S)

    # --- Local liquor options ---
    for id, raw, jur, prec, title, text in [
        ("liquor-youngs-jersey-dairy", "MAD RIVER TOWNSHIP", "Mad River Township", "Mad River Township precinct MR-5", "Local liquor option: Young's Jersey Dairy (Sunday)",
         "Sunday sale of wine and mixed beverages and spirituous liquor by Youngs Jersey Dairy, Inc., dba Young's Jersey Dairy, a D-6 permit applicant (restaurant/entertainment venue), 6880 Springfield Xenia Road."),
        ("liquor-silver-swan", "SPRINGFIELD TOWNSHIP", "Springfield Township", "Springfield Township precinct T-8", "Local liquor option: Silver Swan Marathon (Sunday)",
         "Sunday sale of wine and mixed beverages by Springfield Fuel Center, Inc., dba Silver Swan Marathon, a D-6 permit applicant (carryout/grocery store), 3880 E. National Road."),
        ("liquor-new-enon-brewing", "ENON VILLAGE", "Village of Enon", "Enon precinct ENON 2", "Local liquor option: New Enon Brewing (Sunday)",
         "Sunday sale of beer, wine and spirituous liquor by New Enon Brewing LLC, a D-6 permit applicant (brewery and winery with a taproom), 160 N. Xenia Dr., Enon."),
        ("liquor-food-fusion", "SPRINGFIELD CITY", "City of Springfield", "Springfield precinct CITY 12", "Local liquor option: Food Fusion Restaurant (Sunday)",
         "Sunday sale of wine, mixed beverages and spirituous liquor by Food Fusion Restaurant, a D-6 permit applicant (full-service restaurant), 1805 W. First St."),
    ]:
        c.issue(id, "liquor", jur, title, P(raw), area=prec, text=text, src=S)
    # New Carlisle precincts CARL 1, 4 and 5 each vote on the four precinct-wide options.
    for prec, num in [("CARL 1", "028"), ("CARL 4", "031"), ("CARL 5", "032")]:
        k = prec.lower().replace(" ", "")
        for sfx, title, text in [
            ("beer", "Local liquor option: beer", "Sale of beer under permits for on-premises consumption only, and for both on-premises and off-premises consumption."),
            ("liquor-glass", "Local liquor option: spirituous liquor by the glass", "Sale of spirituous liquor by the glass."),
            ("wine", "Local liquor option: wine and mixed beverages", "Sale of wine and mixed beverages under permits for on-premise consumption only, and for both on-premise and off-premise consumption."),
            ("sunday", "Local liquor option: Sunday on-premises sales", "Sunday sale of intoxicating liquor, of the same types legally sold in the precinct on other days, for consumption on the premises where sold."),
        ]:
            c.issue(f"liquor-new-carlisle-{k}-{sfx}", "liquor", "City of New Carlisle", title, P("NEW CARLISLE CITY"), area=f"New Carlisle precinct {prec} ({num})", text=text, src=S)
    return c
