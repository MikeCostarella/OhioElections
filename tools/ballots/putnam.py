from lib import County, NOTE_ORDER, NOTE_PLACES

SITE = "https://www.boe.ohio.gov/putnam/"
NOTICE = "https://www.boe.ohio.gov/putnam/c/upload/FWAB_11November46Day.pdf"
BALLOTS = "https://lookup.boe.ohio.gov/vtrapp/putnam/ballotlist.aspx"

TWPS = ["BLANCHARD", "GREENSBURG", "JACKSON", "JENNINGS", "LIBERTY", "MONROE", "MONTEREY", "OTTAWA", "PALMER", "PERRY", "PLEASANT", "RILEY",
        "SUGAR CREEK", "UNION", "VAN BUREN"]


def build():
    # The SoS file lists townships as "BLANCHARD TWP." (with a period); villages are clean ("FORT JENNINGS VILLAGE" -> "Fort Jennings Village").
    rename = {f"{t} TWP.": f"{t.title()} Township" for t in TWPS}
    c = County("putnam", "Putnam", "39137", rename=rename)
    c.src("putnam-46day", "Putnam County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election (revised 9/18/2026)", NOTICE)
    c.src("putnam-ballots", "Putnam County Board of Elections: official sample ballots for all 69 precinct splits, November 3, 2026 (state ballot lookup)", BALLOTS)
    C = I = ["putnam-46day", "putnam-ballots"]
    c.links = [
        {"label": "Board of Elections", "url": SITE},
        {"label": "Election information", "url": "https://www.boe.ohio.gov/putnam/election-info/"},
        {"label": "Federal write-in absentee ballot notices", "url": "https://www.boe.ohio.gov/putnam/election-info/federal-write-in-absentee-ballots/"},
        {"label": "Sample ballots by precinct", "url": BALLOTS},
        {"label": "Candidate and voter tools", "url": "https://www.boe.ohio.gov/putnam/candidate-voter-tools/"},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://www.boe.ohio.gov/putnam/election-info/election-results/"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue, and the Board's sample ballots for each precinct, "
               "which give the full ballot wording and show which precincts vote on each issue (the notice gives no precinct lists for local issues).",
               NOTE_ORDER, NOTE_PLACES,
               "The Board's notice and sample ballots do not give local issue numbers."]
    P = c.p; SD = c.sd

    # --- Federal, state legislative, appeals (all of Putnam County is in the 9th Congressional, 1st Senate, 82nd House and 3rd Appeals districts) ---
    c.contest("congress-9", "U.S. House", "Representative to Congress", [("Marcy Kaptur", "DEM"), ("Derek Merrin", "REP")], detail="9th District", src=C)
    c.contest("senate-1", "Ohio General Assembly", "State Senator", [("Craig S. Riedel", "REP")], detail="1st District · full term commencing January 1, 2027", src=C)
    c.contest("rep-82", "Ohio General Assembly", "State Representative", [("Christopher Elder", "LIB"), ("Roy W. Klopfenstein", "REP"), ("Maddux McCray", "DEM")],
              detail="82nd District", src=C)
    c.contest("appeals-3-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Mark C. Miller", "REP")], detail="3rd District · full term commencing February 9, 2027", src=C)

    # --- County offices ---
    c.contest("commissioner", "County offices", "County Commissioner", [("Jeff Vance", "REP")], detail="Full term commencing January 1, 2027", src=C)
    c.contest("auditor", "County offices", "County Auditor", [("Robert L. Benroth", "REP")], detail="Full term commencing March 8, 2027", src=C)
    c.contest("clerk-of-courts", "County offices", "Clerk of the Court of Common Pleas", [("Susan R. Maag", "REP")], detail="Unexpired term ending December 31, 2028", src=C)
    NP = " · no party label on the ballot"
    # The notice prints "(Rep)" after Schroeder; Common Pleas judges carry no party label on the general-election ballot.
    c.contest("cp-probate-juvenile", "Court of Common Pleas", "Judge of the Court of Common Pleas, Probate/Juvenile Division", ["Barry E. Schroeder"],
              detail="Full term commencing February 9, 2027" + NP, src=C)

    # --- Issues (unnumbered; listed in the notice's order). Places follow the sample ballots: the Board's precincts (001-025) each cover a
    # township with the villages inside it, and the ballot splits show which part votes on each levy. Estimates are the sample ballots' wording
    # ("market value"); the notice says "appraised value" for several. ---
    FIRE = ("Fire apparatus, mechanical resuscitators or other fire equipment and appliances, buildings or sites, sources of water supply, fire-alarm communications, "
            "firefighting companies or permanent, part-time or volunteer firefighting, emergency medical service, administrative or communications personnel "
            "(including employer contributions), ambulance equipment, and ambulance, paramedic or other emergency medical services.")
    est = lambda total, per: f"{total} a year; {per} for each $100,000 of market value"
    c.levy("columbus-grove-pleasant-fire", "Columbus Grove/Pleasant Township Joint Fire District", P("COLUMBUS GROVE VILLAGE", "PLEASANT TWP."), "Renewal", FIRE,
           "2 mills", "5 years, commencing in 2027", "2028", est("$202,260", "$52"),
           area="Columbus Grove Village and Pleasant Township (precincts 023 Columbus Grove Corp., 024 Pleasant Twp.)", src=I)
    CONT = P("CONTINENTAL VILLAGE"); CA = "Continental Village (precinct 008 Monroe Twp./Continental, split 1)"
    c.levy("continental-current", "Village of Continental", CONT, "Renewal", "Current expenses.", "1.5 mills", "5 years, commencing in 2027", "2028",
           est("$25,000", "$36"), area=CA, src=I)
    c.levy("continental-police", "Village of Continental", CONT, "Renewal", "Police protection.", "2 mills", "5 years, commencing in 2027", "2028",
           est("$34,000", "$48"), area=CA, src=I)
    c.levy("continental-streets", "Village of Continental", CONT, "Renewal", "General construction, reconstruction, resurfacing and repair of streets, roads and bridges in the village.",
           "2 mills", "5 years, commencing in 2027", "2028", est("$34,000", "$48"), area=CA, src=I,
           note="The Village of Continental has three renewal levies on this ballot (current expenses, police, streets).")
    # 11 mills and $230 per $100,000 are as printed in both the notice and the sample ballot.
    c.levy("gilboa-current", "Village of Gilboa", P("GILBOA VILLAGE"), "Renewal", "Current expenses.", "11 mills", "3 years, commencing in 2027", "2028",
           est("$21,650", "$230"), area="Gilboa Village (precinct 001 Blanchard Twp., split 1)", src=I)
    c.levy("greensburg-twp-roads", "Greensburg Township", P("GREENSBURG TWP."), "Renewal", "Township road repair.", "1 mill", "5 years, commencing in 2027", "2028",
           est("$47,570", "$26"), area="Greensburg Township (precinct 002)", src=I)
    c.levy("jackson-twp-roads", "Jackson Township", P("JACKSON TWP."), "Renewal", "General construction, reconstruction, resurfacing and repair of roads.", "5 mills",
           "5 years, commencing in 2027", "2028", est("$163,050", "$116"), area="Jackson Township (precinct 003)", src=I)
    c.levy("miller-city-current", "Village of Miller City", P("MILLER CITY VILLAGE"), "Renewal", "Current expenses.", "1.8 mills", "5 years, commencing in 2027", "2028",
           est("$4,370", "$37"), area="Miller City Village (precinct 021 Palmer Twp., split 1)", src=I)
    # The sample ballots put this levy on the Ottawa Village (013-015) and Glandorf (012) precincts as well as Ottawa Twp. East and West.
    c.levy("ottawa-twp-fire", "Ottawa Township (including Ottawa and Glandorf villages)", P("OTTAWA TWP.", "OTTAWA VILLAGE", "GLANDORF VILLAGE"), "Renewal", "Fire protection.",
           "1.35 mills", "5 years, commencing in 2027", "2028", est("$107,017", "$34"),
           area="Ottawa Township, Ottawa Village and Glandorf Village (precincts 012-016, 025)", src=I)
    c.levy("ottawa-fire-personnel", "Village of Ottawa", P("OTTAWA VILLAGE"), "Renewal", "Payment of permanent, part-time or volunteer fire department personnel.", "1.1 mills",
           "5 years, commencing in 2027", "2028", est("$109,220", "$26"), area="Ottawa Village (precincts 013-015 Ottawa Corp. 1-3)", src=I)
    # Palmer's fire levy is on every Palmer split, Miller City included; the road levy is not on the Miller City split.
    c.levy("palmer-twp-fire", "Palmer Township (including Miller City)", P("PALMER TWP.", "MILLER CITY VILLAGE"), "Renewal", "Fire protection.", "0.7 mill",
           "5 years, commencing in 2027", "2028", est("$21,420", "$15"), area="Palmer Township and Miller City Village (precinct 021)", src=I)
    c.levy("palmer-twp-roads", "Palmer Township", P("PALMER TWP."), "Renewal", "Road repair.", "1 mill", "5 years, commencing in 2027", "2028",
           est("$34,070", "$23"), area="Palmer Township outside Miller City (precinct 021, splits 2-4)", src=I)
    c.levy("perry-twp-fire", "Perry Township (including Cloverdale and Dupont)", P("PERRY TWP.", "CLOVERDALE VILLAGE", "DUPONT VILLAGE"), "Renewal", "Fire protection.",
           "2 mills", "5 years, commencing in 2027", "2028", est("$35,240", "$27"), area="Perry Township, Cloverdale Village and Dupont Village (precinct 022)", src=I)
    c.levy("union-twp-fire", "Union Township (including Kalida)", P("UNION TWP.", "KALIDA VILLAGE"), "Renewal", "Providing fire protection.", "0.25 mill",
           "5 years, commencing in 2027", "2028", est("$19,130", "$5"), area="Union Township and Kalida Village (precincts 019 Kalida Corp., 020 Union Twp.)", src=I)
    # Same issue as hancock.py's mccomb-bond.
    c.issue("mccomb-bond", "levy", "McComb Local School District (Hancock, Putnam and Wood)", "School district income tax (0.25%) and bond issue ($23,815,000)",
            SD("MCCOMB LOCAL SD (HANCOCK)"), area="McComb Local School District (Hancock, Putnam and Wood)",
            levy={"type": "Income tax and bond issue", "purpose": "Income tax for current expenses; bonds for constructing school facilities, including a new K-12 building.",
                  "mills": "6.99 mills (bond)", "term": "Income tax for a continuing period beginning January 1, 2027; bonds up to 37 years", "estimate": "$23,815,000 principal; $245 for each $100,000 of market value"},
            text="Shall the McComb Local School District be authorized to do both of the following: 1. Impose an annual income tax of 0.25% on the school district income of individuals, "
                 "for a continuing period of time, beginning January 1, 2027, for the purpose of current expenses? 2. Issue bonds for the purpose of constructing school facilities, "
                 "including constructing a new K-12 building and including under a program of the Ohio Facilities Construction Commission, and renovating, repairing, improving and "
                 "expanding existing school facilities; furnishing and equipping the same; improving the sites thereof; and acquiring real estate and interests therein in the principal "
                 "amount of $23,815,000, to be repaid annually over a maximum period of 37 years, and levy a property tax outside the ten-mill limitation estimated by the county auditor "
                 "to average over the bond repayment period 6.99 mills for each $1 of taxable value, which amounts to $245 for each $100,000 of the county auditor's market value, "
                 "to pay the annual debt charges on the bonds, and to pay debt charges on any notes issued in anticipation of those bonds?", src=I)
    c.issue("paulding-evsd-income-tax", "question", "Paulding Exempted Village School District (Paulding and Putnam)", "School district income tax: 0.75% additional, 5 years, for permanent improvements",
            SD("PAULDING EX VILL SD (PAULDING)"), area="Paulding Exempted Village School District (Putnam County part: precinct 008 Monroe Twp./Continental split 3, 022 Perry Twp. split 5)",
            text="Shall an annual income tax of 0.75 per cent on the school district income of individuals be imposed by Paulding Exempted Village School District, for five years, "
                 "beginning January 1, 2027, for the purpose of permanent improvements?", src=I)
    return c
