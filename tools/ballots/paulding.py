from lib import County, NOTE_ORDER, NOTE_PLACES

SITE = "https://www.boe.ohio.gov/paulding/"
NOTICE = "https://www.boe.ohio.gov/paulding/c/upload/FWAB_11November46Day.pdf"
BALLOTS = "https://lookup.boe.ohio.gov/vtrapp/paulding/ballotlist.aspx"


def build():
    # Default display names are right except Oakwood ("OAKWOOD VILLAGE PAULDING" in the SoS file, to tell it from other Oakwoods).
    # Scott Village is shared with Van Wert County (vanwert.py); the Paulding EVSD reaches into Putnam County (putnam.py).
    c = County("paulding", "Paulding", "39125", rename={"OAKWOOD VILLAGE PAULDING": "Oakwood Village"})
    c.src("paulding-46day", "Paulding County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election (revised 9/14/2026)", NOTICE)
    S = ["paulding-46day"]
    c.links = [
        {"label": "Board of Elections", "url": SITE},
        {"label": "Election information", "url": "https://www.boe.ohio.gov/paulding/election-info/"},
        {"label": "Federal write-in absentee ballot notices", "url": "https://www.boe.ohio.gov/paulding/election-info/federal-write-in-absentee-ballots/"},
        {"label": "Sample ballots by precinct", "url": BALLOTS},
        {"label": "Candidate and voter tools", "url": "https://www.boe.ohio.gov/paulding/candidate-voter-tools/"},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://www.boe.ohio.gov/paulding/election-info/election-results/"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it "
               "and gives the issues' ballot wording.",
               NOTE_ORDER, NOTE_PLACES,
               "The Board's notice does not give local issue numbers; see your sample ballot for them."]
    P = c.p; SD = c.sd

    # --- Federal, state legislative, appeals (all of Paulding County is in the 9th Congressional, 1st Senate, 82nd House and 3rd Appeals districts) ---
    # Kathy McKinstry is a certified write-in for Congress (not listed).
    c.contest("congress-9", "U.S. House", "Representative to Congress", [("Marcy Kaptur", "DEM"), ("Derek Merrin", "REP")], detail="9th District", src=S)
    c.contest("senate-1", "Ohio General Assembly", "State Senator", [("Craig S. Riedel", "REP")], detail="1st District · full term commencing January 1, 2027", src=S)
    c.contest("rep-82", "Ohio General Assembly", "State Representative", [("Christopher Elder", "LIB"), ("Roy W. Klopfenstein", "REP"), ("Maddux McCray", "DEM")],
              detail="82nd District", src=S)
    c.contest("appeals-3-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Mark C. Miller", "REP")], detail="3rd District · full term commencing February 9, 2027", src=S)

    # --- County offices (no Common Pleas judge is on Paulding's notice) ---
    c.contest("commissioner", "County offices", "County Commissioner", [("Michael E. Iler", "REP")], detail="Full term commencing January 1, 2027", src=S)
    c.contest("auditor", "County offices", "County Auditor", [("Angie G. Stoller", "REP")], detail="Full term commencing March 8, 2027", src=S)
    c.contest("prosecutor", "County offices", "Prosecuting Attorney", [("Matthew Miller", "REP")], detail="Unexpired term ending December 31, 2028", src=S)

    # --- Issues (unnumbered; listed in the notice's order). Precinct numbers follow the absentee list's PRSID/PRECNAME: 01 Auglaize, 02 Benton,
    # 03 Blue Creek, 04 Brown (with Melrose and Oakwood), 05 Carryall, 06 Antwerp, 07 Crane & Cecil, 08 Emerald, 09 Harrison, 10 Jackson & Broughton,
    # 11 Latty Twp. & Grover Hill, 12 Paulding Twp. & Latty Village, 13-15 Paulding Village 1-3 (15 is the Jackson Township part), 16 Washington. ---
    est = lambda total, per: f"{total} a year; {per} for each $100,000 of the county auditor's market value"
    c.levy("grover-hill-ems", "Village of Grover Hill", P("GROVER HILL VILLAGE"), "Renewal", "Providing emergency medical service.", "0.5 mill",
           "5 years, commencing in 2026", "2027", est("$880", "$5"), area="Grover Hill Village (precinct 11/2 Latty Twp. & Grover Hill)", src=S,
           text="A renewal of a tax for the benefit of Grover Hill Village for the purpose of providing emergency medical service, that the county auditor estimates "
                "will collect $880 annually, at a rate not exceeding 0.5 mill for each $1 of taxable value, which amounts to $5 for each $100,000 of the county auditor's "
                "market value, for 5 years, commencing in 2026, first due in calendar year 2027.")
    PV = P("PAULDING VILLAGE"); PVA = "Paulding Village (precincts 13/1, 14/1, 15/1 Paulding Village 1-3)"
    c.issue("paulding-income-tax-streets", "question", "Village of Paulding", "Municipal income tax: 0.10% additional, 5 years, for streets", PV, area=PVA, src=S,
            text="Shall the Ordinance providing for an additional 0.10 per cent levy on income, for 5 years, for the purpose of street construction, reconstruction, "
                 "repair, maintenance, and related street infrastructure improvements be passed?")
    c.issue("paulding-income-tax-pool", "question", "Village of Paulding", "Municipal income tax: 0.10% additional, 5 years, for the village swimming pool", PV, area=PVA, src=S,
            note="The Village of Paulding has two separate 0.10% income tax questions on this ballot (streets and swimming pool).",
            text="Shall the Ordinance providing for an additional 0.10 per cent levy on income, for 5 years, for the purpose of acquiring, constructing, improving, "
                 "repairing, operating, maintaining, and equipping the village swimming pool and related facilities be passed?")
    # Precincts 10/1-3 (Jackson Township with Broughton) and 15/1 (the part of Paulding Village in Jackson Township).
    c.levy("jackson-twp-fire", "Jackson Township (including Broughton and part of Paulding Village)", P("JACKSON TOWNSHIP", "BROUGHTON VILLAGE", "PAULDING VILLAGE"),
           "Renewal", "Fire protection.", "0.6 mill", "5 years, commencing in 2026", "2027", est("$10,941", "$5"),
           area="Jackson Township, Broughton Village and the Jackson Township part of Paulding Village (precincts 10/1, 10/2, 10/3, 15/1)", src=S,
           text="A renewal of a tax for the benefit of Jackson Township for the purpose of fire protection, that the county auditor estimates will collect $10,941 annually, "
                "at a rate not exceeding 0.6 mill for each $1 of taxable value, which amounts to $5 for each $100,000 of the county auditor's market value, "
                "for 5 years, commencing in 2026, first due in calendar year 2027.")
    # Precincts 11/1 and 11/2: Latty Township with Grover Hill (Latty Village lies in Paulding Township, precinct 12, and does not vote on it).
    c.levy("latty-twp-fire", "Latty Township (including Grover Hill)", P("LATTY TOWNSHIP", "GROVER HILL VILLAGE"), "Additional",
           "Providing protection against fire, maintaining fire equipment and apparatus, and supporting fire and rescue services.", "1.25 mills",
           "5 years, commencing in 2026", "2027", est("$49,826", "$44"), area="Latty Township and Grover Hill Village (precincts 11/1, 11/2)", src=S,
           text="An additional tax for the benefit of Latty Township for the purpose of providing protection against fire, maintaining fire equipment & apparatus & "
                "support fire and rescue services, that the county auditor estimates will collect $49,826 annually, at a rate not exceeding 1.25 mills for each $1 of "
                "taxable value, which amounts to $44 for each $100,000 of the county auditor's market value, for 5 years, commencing in 2026, first due in calendar year 2027.")
    c.levy("washington-twp-fire", "Washington Township", P("WASHINGTON TOWNSHIP"), "Renewal", "Fire protection.", "1 mill", "5 years, commencing in 2027", "2028",
           est("$16,285", "$13"), area="Washington Township (precincts 16/1, 16/2, 16/3)", src=S,
           text="A renewal of a tax for the benefit of Washington Township for the purpose of fire protection, that the county auditor estimates will collect $16,285 "
                "annually, at a rate not exceeding 1 mill for each $1 of taxable value, which amounts to $13 for each $100,000 of the county auditor's market value, "
                "for 5 years, commencing in 2027, first due in calendar year 2028.")
    # Same issue as putnam.py's paulding-evsd-income-tax. The notice's precinct list (01/1, 04/1-3, 07/1, 07/3, 08/1, 10/1, 12/1, 13/1, 14/1, 14/2, 15/1, 16/1)
    # matches the voter file's Paulding EVSD places.
    c.issue("paulding-evsd-income-tax", "question", "Paulding Exempted Village School District (Paulding and Putnam)", "School district income tax: 0.75% additional, 5 years, for permanent improvements",
            SD("PAULDING EX VILL SD (PAULDING)"),
            area="Paulding Exempted Village School District (Paulding and Putnam counties; Paulding County precincts 01/1, 04/1-3, 07/1, 07/3, 08/1, 10/1, 12/1, 13/1, 14/1, 14/2, 15/1, 16/1)",
            text="Shall an annual income tax of 0.75 per cent on the school district income of individuals be imposed by Paulding Exempted Village School District, for five years, "
                 "beginning January 1, 2027, for the purpose of permanent improvements?", src=S)
    return c
