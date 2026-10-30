from lib import County, NOTE_ORDER, NOTE_PLACES

SITE = "https://www.boe.ohio.gov/vanwert/"
NOTICE = "https://www.boe.ohio.gov/vanwert/c/upload/FWAB_11November46Day.pdf"
BALLOTS = "https://lookup.boe.ohio.gov/vtrapp/vanwert/ballotlist.aspx"


def build():
    # Default display names are right ("VAN WERT CITY" -> "Van Wert City", "MIDDLE POINT VILLAGE" -> "Middle Point Village").
    # Delphos is shared with Allen County (allen.py); Scott Village is shared with Paulding County.
    c = County("vanwert", "Van Wert", "39161")
    c.src("vanwert-46day", "Van Wert County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election (revised 9/8/2026)", NOTICE)
    c.src("vanwert-ballots", "Van Wert County Board of Elections: official sample ballots for all 47 precinct splits, November 3, 2026 (state ballot lookup)", BALLOTS)
    C = I = ["vanwert-46day", "vanwert-ballots"]
    c.links = [
        {"label": "Board of Elections", "url": SITE},
        {"label": "Election information", "url": "https://www.boe.ohio.gov/vanwert/election-info/"},
        {"label": "Federal write-in absentee ballot notices", "url": "https://www.boe.ohio.gov/vanwert/election-info/federal-write-in-absentee-ballots/"},
        {"label": "Sample ballots by precinct", "url": BALLOTS},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://www.boe.ohio.gov/vanwert/election-info/election-results/"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it, "
               "checked against the Board's sample ballots, which give the full ballot wording and the county auditor's estimates.",
               NOTE_ORDER, NOTE_PLACES,
               "The Board's notice and sample ballots do not give local issue numbers."]
    P = c.p; SD = c.sd

    # --- Federal, state legislative, appeals (all of Van Wert County is in the 4th Congressional, 1st Senate, 82nd House and 3rd Appeals districts) ---
    # The notice spells "Kolasinki"; the sample ballots print "Joshua D. Kolasinski", as in allen.py. Neither prints a party for Tackett.
    c.contest("congress-4", "U.S. House", "Representative to Congress", [("Jim Jordan", "REP"), ("Joshua D. Kolasinski", "DEM"), ("Tracey L. Tackett", "Nonparty")],
              detail="4th District", src=C)
    c.contest("senate-1", "Ohio General Assembly", "State Senator", [("Craig S. Riedel", "REP")], detail="1st District · full term commencing January 1, 2027", src=C)
    c.contest("rep-82", "Ohio General Assembly", "State Representative", [("Christopher Elder", "LIB"), ("Roy W. Klopfenstein", "REP"), ("Maddux McCray", "DEM")],
              detail="82nd District", src=C)
    c.contest("appeals-3-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Mark C. Miller", "REP")], detail="3rd District · full term commencing February 9, 2027", src=C)

    # --- County offices ---
    # The commissioner contest has a write-in line on the sample ballots (a certified write-in, not listed).
    c.contest("commissioner", "County offices", "County Commissioner", [("Thad Lichtensteiger", "REP")], detail="Full term commencing January 1, 2027", src=C)
    # Neither the notice nor the sample ballots give the auditor's term.
    c.contest("auditor", "County offices", "County Auditor", [("Arica L. Wermer", "REP")], src=C)
    c.contest("prosecutor", "County offices", "Prosecuting Attorney", [("Dillon W. Staas, IV", "REP")], detail="Unexpired term ending December 31, 2028", src=C)
    NP = " · no party label on the ballot"
    # The term date comes from the sample ballots (the notice gives none).
    c.contest("cp-juvenile-probate", "Court of Common Pleas", "Judge of the Court of Common Pleas, Juvenile/Probate Division", ["Eva J. Yarger"],
              detail="Full term commencing February 9, 2027" + NP, src=C)

    # --- Issues (unnumbered in the Board's documents; listed in the notice's order) ---
    est = lambda total, per: f"{total} a year; {per} for each $100,000 of the county auditor's market value"
    # The notice and the Convoy sample ballot both carry two Convoy Village operating renewals with identical wording and estimates.
    for n in (1, 2):
        c.levy(f"convoy-operating-{n}", "Village of Convoy", P("CONVOY VILLAGE"), "Renewal", "Operating expenses.", "2 mills",
               "5 years, commencing in 2027", "2028", est("$8,957", "$14"), area="Convoy Village (precinct Convoy 23/1)",
               note="Convoy Village has two 2-mill operating renewals on this ballot, with the same wording and estimate.", src=I)
    # Venedocia lies in Jennings and York townships: precincts Jennings 1 (17/1) and York 2 (31/2).
    c.levy("venedocia-fire", "Village of Venedocia", P("VENEDOCIA VILLAGE"), "Renewal", "Fire protection.", "1.2 mills",
           "5 years, commencing in 2027", "2028", est("$1,282", "$24"), area="Venedocia Village (precincts Jennings 1, York 2)", src=I)
    c.levy("jackson-twp-fire-ems", "Jackson Township", P("JACKSON TOWNSHIP"), "Renewal", "Fire and EMS service.", "1.8 mills",
           "5 years, commencing in 2027", "2028", est("$43,900", "$40"), area="Jackson Township (precinct Jackson 16/1)", src=I)
    c.levy("liberty-twp-fire", "Liberty Township (excluding the Village of Ohio City)", P("LIBERTY TOWNSHIP"), "Renewal", "Fire protection.", "1.4 mills",
           "3 years, commencing in 2027", "2028", est("$36,392", "$27"), area="Liberty Township outside Ohio City (precinct Liberty 19/1)", src=I)
    # Precincts Union 1 and 2. The voter file puts all of Union Township's own voters in Crestview LSD, and the Union 2 ballot has no Crestview levy,
    # so Union 2 is the Scott Village part (Wayne Trace LSD); Scott Village added by hand.
    c.levy("union-twp-current", "Union Township", P("UNION TOWNSHIP") + P("SCOTT VILLAGE"), "Renewal", "Current expenses.", "1 mill",
           "5 years, commencing in 2027", "2028", est("$24,811", "$11"), area="Union Township (precincts Union 1, Union 2)", src=I)
    # The fire district is not in the voter file; placed from the notice's precinct list (Washington West 1 only; Middle Point votes in its own precinct).
    c.levy("washington-west-fire", "Washington Township West Fire District", P("WASHINGTON TOWNSHIP"), "Renewal", "Fire and EMS services.", "1 mill",
           "5 years, commencing in 2027", "2028", est("$23,002", "$19"), area="Washington Township West Fire District (precinct Washington West 1, 28/1)", src=I)
    # The park district is not in the voter file; placed from the notice's precinct list (Convoy 23/1, Tully 24/1).
    c.levy("tully-convoy-park", "Tully-Convoy Park District", P("CONVOY VILLAGE", "TULLY TOWNSHIP"), "Renewal",
           "Current operating expense and future improvements.", "1 mill", "5 years, commencing in 2027", "2028", est("$69,086", "$23"),
           area="Tully-Convoy Park District (precincts Convoy 23/1, Tully 24/1)", src=I)
    c.levy("crestview-lsd-pi", "Crestview Local School District", SD("CRESTVIEW LOCAL SD (VANWERT)"), "Renewal", "Permanent improvements.", "2 mills",
           "5 years, commencing in 2027", "2028", est("$221,314", "$26"),
           area="Crestview Local School District (precincts Harrison, Convoy, Tully, Union 1, Wren 1 and 2, Pleasant North 2)", src=I)
    # Same levy as allen.py's delphos-csd-current.
    c.levy("delphos-csd-current", "Delphos City School District", SD("DELPHOS CITY SD"), "Renewal", "Current expenses.", "5.5 mills",
           "5 years, commencing in 2027", "2028", est("$929,532", "$83"),
           area="Delphos City School District (Allen and Van Wert counties; Van Wert County precincts Delphos 3A, 3B, 4A, Jennings 2, Washington East, Washington West 2)",
           src=I)
    # Same issue as allen.py's and auglaize.py's spencerville-lsd-income-tax.
    c.issue("spencerville-lsd-income-tax", "question", "Spencerville Local School District", "School district income tax: 1% renewal for 5 years, for current expenses",
            SD("SPENCERVILLE LOCAL SD (ALLEN)"),
            area="Spencerville Local School District (Allen, Auglaize and Van Wert counties; Van Wert County precincts Jennings 1, Jennings 4)",
            text="Shall an annual income tax of 1% on the school district income of individuals and of estates be imposed by Spencerville Local School District, "
                 "to renew an income tax (or income taxes) expiring at the end of 2027, for 5 years, beginning January 1, 2028, for the purpose of current expenses?",
            src=I)
    return c
