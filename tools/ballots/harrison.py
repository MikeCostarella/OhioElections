from lib import County, NOTE_ORDER, NOTE_PLACES

NOTICE = "https://www.boe.ohio.gov/harrison/c/upload/FWAB_11November46Day.pdf"
BALLOTS = "https://lookup.boe.ohio.gov/vtrapp/harrison/ballotlist.aspx"


def build():
    c = County("harrison", "Harrison", "39067")
    c.src("harrison-46day", "Harrison County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election (revised 9/16/2026)", NOTICE)
    c.src("harrison-ballots", "Harrison County Board of Elections: sample ballots for every precinct, November 3, 2026 General Election", BALLOTS)
    S = ["harrison-46day", "harrison-ballots"]
    c.links = [
        {"label": "Board of Elections", "url": "https://www.boe.ohio.gov/harrison/"},
        {"label": "Election info", "url": "https://www.boe.ohio.gov/harrison/election-info/"},
        {"label": "Sample ballots by precinct", "url": BALLOTS},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://www.boe.ohio.gov/harrison/election-info/election-results/"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it, "
               "checked against the Board's precinct sample ballots. Issue wording is the Board's; the full wording is on your sample ballot.",
               NOTE_ORDER, NOTE_PLACES,
               "The Board's notice and sample ballots do not give local issue numbers; see your sample ballot for the order."]
    P = c.p; SD = c.sd
    NP = " · no party label on the ballot"
    est = lambda total, per: f"{total} a year; {per} for each $100,000 of market value"
    T5 = "5 years, commencing in 2027"

    # --- Federal, state legislative, appeals (each covers the whole county; the 30th Senate seat is not up) ---
    c.contest("congress-6", "U.S. House", "Representative to Congress", [("Elizabeth Kirtley", "DEM"), ("Michael A. Rulli", "REP")], detail="6th District", src=S)
    c.contest("rep-95", "Ohio General Assembly", "State Representative", [("Paul Cameron", "DEM"), ("Ty Moore", "REP")], detail="95th District", src=S)
    c.contest("appeals-7-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Molly K. Johnson", "REP")], detail="7th District · full term commencing February 9, 2027", src=S)
    c.contest("appeals-7-0210", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Mark Anthony Hanni", "REP"), ("Katherine Rudzik", "DEM")], detail="7th District · full term commencing February 10, 2027", src=S)

    # --- County offices and courts ---
    c.contest("commissioner", "County offices", "County Commissioner", [("Dustin Corder", "REP"), ("Michelle Meyer", "Nonparty")], detail="Full term commencing January 1, 2027", src=S)
    # The notice prints "Clint A. Barr"; the sample ballots print "Clint Barr".
    c.contest("auditor", "County offices", "County Auditor", [("Clint Barr", "REP")], detail="Full term commencing March 8, 2027", src=S)
    c.contest("cp-0419", "Court of Common Pleas", "Judge of the Court of Common Pleas", ["T. Shawn Hervey"], detail="Full term commencing April 19, 2027" + NP, src=S)
    # The notice says "Probate Division"; the sample ballots say "Probate and Juvenile Division".
    c.contest("cp-probate-juvenile", "Court of Common Pleas", "Judge of the Court of Common Pleas, Probate and Juvenile Division", ["Matthew Paul Puskarich"],
              detail="Full term commencing February 9, 2027" + NP, src=S)

    # --- County levies (all precincts) ---
    c.levy("county-home", "Harrison County", "county", "Renewal", "Maintenance and operation of the County Home.",
           "1.5 mills", T5, "2028", est("$1,609,394", "$53"), src=S)
    c.levy("county-sheriff", "Harrison County", "county", "Renewal",
           "Police protection, including salaries for police personnel and providing, upgrading and maintaining equipment, by the Sheriff's Office.",
           "1 mill", T5, "2028", est("$1,165,943", "$35"), src=S)
    c.levy("county-extension", "Harrison County", "county", "Renewal",
           "Ohio Cooperative Extension Service Fund for 4-H, agriculture and natural resources, home economics and economic development.",
           "0.75 mill", T5, "2028", est("$827,871", "$26"), src=S)
    c.levy("county-aging", "Harrison County", "county", "Renewal",
           "Providing and maintaining services for senior citizens by the Harrison County Council on Aging.",
           "0.75 mill", T5, "2028", est("$804,697", "$26"), src=S)

    # --- School districts ---
    # Precinct 007/2 (German Township, part).
    c.levy("edison-lsd", "Edison Local School District (Jefferson, Carroll and Harrison)", SD("EDISON LOCAL SD (JEFFERSON)"), "Renewal (fixed sum)", "Current expenses ($1,049,150 a year).",
           "1.85 mills (estimated average)", T5, "2028", est("$1,049,150", "$65"),
           area="Edison Local School District, Harrison County part (German precinct 2)", src=S)
    JVS = "Jefferson County Joint Vocational School District (Jefferson, Belmont, Carroll and Harrison)"
    JVS_AREA = "Jefferson County JVSD, Harrison County part (German precinct 2, Green precinct 3, Shortcreek precincts 2–4)"
    # Precincts 007/2, 008/3, 014/2-4: the Edison and Buckeye Local parts of German, Green and Shortcreek (Adena and Harrisville).
    JP = SD("EDISON LOCAL SD (JEFFERSON)") + SD("BUCKEYE LOCAL SD (JEFFERSON)")
    c.levy("jefferson-jvsd-1", JVS, JP, "Renewal",
           "0.67 mill for current expenses and 0.33 mill for reconditioning or acquiring tools, equipment or furnishings and for repairing, improving, renovating, expanding or reconstructing buildings and sites.",
           "1 mill", "10 years, commencing in 2027", "2028", est("$1,999,864", "$32"), area=JVS_AREA,
           note="One of two separate 1-mill JVS renewals on the ballot.", src=S)
    c.levy("jefferson-jvsd-2", JVS, JP, "Renewal",
           "0.67 mill for current expenses and 0.33 mill for purchasing equipment for buildings and improving buildings.",
           "1 mill", "10 years, commencing in 2027", "2028", est("$1,934,109", "$30"), area=JVS_AREA,
           note="One of two separate 1-mill JVS renewals on the ballot.", src=S)

    # --- Villages ---
    c.levy("cadiz-police", "Village of Cadiz", P("CADIZ VILLAGE"), "Renewal", "Police expenses.", "1 mill", T5, "2028",
           est("$70,141", "$35"), area="Village of Cadiz (precincts 003/2 and 004/1)", src=S)
    # Liquor options: precinct 004/1 (Cadiz Village SW).
    CZ = P("CADIZ VILLAGE")
    c.issue("liquor-cadiz-christophers", "liquor", "Village of Cadiz", "Local liquor option: Christopher's Delights (D-5, D-5i permits)", CZ,
            area="Cadiz Village SW precinct (004/1)",
            text="Shall the sale of spirituous liquor be permitted by Christopher's Delights L.L.C. an applicant for a D-5, D-5i liquor permit(s), who is engaged in the "
                 "business of operating a restaurant at 533 Liggett Lane, Cadiz, OH 43907 in this precinct?", src=S)
    c.issue("liquor-cadiz-christophers-sunday", "liquor", "Village of Cadiz", "Local liquor option: Christopher's Delights (Sunday)", CZ,
            area="Cadiz Village SW precinct (004/1)",
            text="Shall the sale of wine and mixed beverages and spirituous liquor be permitted for sale on Sunday by Christopher's Delights, L.L.C. an applicant for a D-6 "
                 "liquor permit who is engaged in the business of operating a restaurant at 533 Liggett Lane, Cadiz, OH 43907 in this precinct?", src=S)
    FV = P("FREEPORT VILLAGE"); FVA = "Village of Freeport (precinct 006/2)"
    c.levy("freeport-current-089", "Village of Freeport", FV, "Renewal", "Current expenses.", "0.89 mill", "4 years, commencing in 2026", "2027",
           est("$3,056", "$31"), area=FVA, note="One of three separate current-expense renewals for the village on the ballot.", src=S)
    c.levy("freeport-current-1", "Village of Freeport", FV, "Renewal", "Current expenses.", "1 mill", T5, "2028",
           est("$4,117", "$35"), area=FVA, note="One of three separate current-expense renewals for the village on the ballot.", src=S)
    c.levy("freeport-current-35", "Village of Freeport", FV, "Renewal", "Current expenses.", "3.5 mills", T5, "2028",
           est("$14,411", "$123"), area=FVA, note="One of three separate current-expense renewals for the village on the ballot.", src=S)
    c.levy("freeport-street", "Village of Freeport", FV, "Renewal", "Street expenses.", "2.67 mills", T5, "2028",
           est("$10,993", "$93"), area=FVA, src=S)
    c.levy("freeport-fire", "Village of Freeport", FV, "Renewal", "Fire expenses.", "0.89 mill", T5, "2028",
           est("$3,664", "$31"), area=FVA, src=S)
    c.levy("new-athens-current", "Village of New Athens", P("NEW ATHENS VILLAGE"), "Renewal", "Current expenses.", "1 mill", T5, "2028",
           est("$3,541", "$35"), area="Village of New Athens (precinct 002/2)", src=S)

    # --- Townships (precinct lists include the villages inside them) ---
    c.levy("cadiz-twp-cemetery", "Cadiz Township", P("CADIZ TOWNSHIP", "CADIZ VILLAGE"), "Renewal", "Maintenance of Cadiz Union Cemetery.", "0.5 mill", T5, "2028",
           est("$104,284", "$18"), area="Cadiz Township, including the Village of Cadiz (precincts 003/1, 003/2 and 004/1)", src=S)
    c.levy("freeport-twp-fire", "Freeport Township", P("FREEPORT TOWNSHIP", "FREEPORT VILLAGE"), "Renewal", "Fire protection.", "1.5 mills", T5, "2028",
           est("$56,685", "$53"), area="Freeport Township, including the Village of Freeport (precincts 006/1 and 006/2)", src=S)
    c.levy("german-twp-roads", "German Township", P("GERMAN TOWNSHIP"), "Renewal", "General construction, reconstruction, resurfacing and repair of roads.", "2 mills", T5, "2028",
           est("$67,154", "$70"), area="German Township (precincts 007/1 and 007/2)", src=S)
    GT = P("GREEN TOWNSHIP", "HOPEDALE VILLAGE"); GTA = "Green Township, including the Village of Hopedale (precincts 008/1–008/3)"
    c.levy("green-twp-roads", "Green Township", GT, "Additional", "Maintaining and repairing roads and bridges.", "1.5 mills",
           "Continuing period of time, commencing in 2026", "2027", est("$145,400", "$53"), area=GTA, src=S)
    c.levy("green-twp-cemetery", "Green Township", GT, "Renewal", "Cemetery operations.", "0.5 mill", T5, "2028",
           est("$50,196", "$18"), area=GTA, src=S)
    MT = P("MONROE TOWNSHIP", "BOWERSTON VILLAGE"); MTA = "Monroe Township, including the Village of Bowerston (precincts 009/1 and 009/2)"
    MNOTE = "One of three separate fire protection renewals for the township on the ballot."
    c.levy("monroe-twp-fire-05a", "Monroe Township", MT, "Renewal", "Fire protection.", "0.5 mill", T5, "2028",
           est("$64,443", "$18"), area=MTA, note=MNOTE, src=S)
    c.levy("monroe-twp-fire-05b", "Monroe Township", MT, "Renewal", "Fire protection.", "0.5 mill", T5, "2028",
           est("$67,758", "$18"), area=MTA, note=MNOTE, src=S)
    c.levy("monroe-twp-fire-1", "Monroe Township", MT, "Renewal", "Fire protection.", "1 mill", T5, "2028",
           est("$123,818", "$35"), area=MTA, note=MNOTE, src=S)
    return c
