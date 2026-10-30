from lib import County, NOTE_ORDER, NOTE_PLACES

SITE = "https://www.boe.ohio.gov/erie/"
NOTICE = "https://www.boe.ohio.gov/erie/c/upload/FWAB_11November46Day.pdf"
CAND = "https://www.boe.ohio.gov/erie/c/upload/Election_Candidates.pdf"
ISSUES = "https://www.boe.ohio.gov/erie/c/upload/Election_Issues.pdf"


def build():
    # Raw names are clean except "VERMILION CITY " (trailing space, as in lorain.py). Bellevue is shared with Huron, Sandusky and Seneca.
    c = County("erie", "Erie", "39043", rename={"VERMILION CITY ": "Vermilion City"})
    c.src("erie-46day", "Erie County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election", NOTICE)
    c.src("erie-cand", "Erie County Board of Elections: candidate filings, November 3, 2026 General Election", CAND)
    c.src("erie-issues", "Erie County Board of Elections: issue filings, November 3, 2026 General Election", ISSUES)
    C = ["erie-46day", "erie-cand"]; I = ["erie-46day", "erie-issues"]
    c.links = [
        {"label": "Board of Elections", "url": SITE},
        {"label": "Election info", "url": "https://www.boe.ohio.gov/erie/election-info/"},
        {"label": "Candidate and issue filings", "url": "https://www.boe.ohio.gov/erie/election-info/candidate-and-issue-filings/"},
        {"label": "Sample ballots by precinct", "url": "https://lookup.boe.ohio.gov/vtrapp/erie/ballotlist.aspx"},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://www.boe.ohio.gov/erie/election-info/election-results/"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it, "
               "checked against the Board's candidate and issue filings lists. Issue wording is the Board's; the full wording is on the sample ballot.",
               NOTE_ORDER, NOTE_PLACES,
               "Local issue numbers run 1 to 23; Issue 3 is the statewide question."]
    P = c.p; D = c.district; SD = c.sd

    # All of Erie County is in the 9th Congressional, 89th House and 2nd Senate districts; the 2nd Senate seat is not up in 2026.
    # Certified write-ins Kathy McKinstry (Congress) and Steve Kraus (89th House) are not listed (NOTE_ORDER).
    c.contest("congress-9", "U.S. House", "Representative to Congress", [("Marcy Kaptur", "DEM"), ("Derek Merrin", "REP")], detail="9th District", src=C)
    c.contest("rep-89", "Ohio General Assembly", "State Representative", [("Easton Michael Retzke", "DEM"), ("Caleb Stidham", "REP")], detail="89th District", src=C)
    c.contest("appeals-6-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Michael R. Goulding", "REP")], detail="6th District · full term commencing February 9, 2027", src=C)
    c.contest("appeals-6-0210", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Myron C. Duhart", "DEM"), ("CJ Kamm", "REP")], detail="6th District · full term commencing February 10, 2027", src=C)
    c.contest("commissioner", "County offices", "County Commissioner", [("Mindy Kayl", "DEM"), ("Steve Shoffner", "REP")], detail="Full term commencing January 1, 2027", src=C)
    c.contest("auditor", "County offices", "County Auditor", [("Richard Jeffrey", "REP"), ("Paul Meisel", "DEM")], src=C)
    NP = " · no party label on the ballot"
    c.contest("cp-gen", "Court of Common Pleas", "Judge of the Court of Common Pleas, General Division", ["Thomas M. Dusza"], detail="Full term commencing February 9, 2027" + NP, src=C)

    N = lambda n: f"Issue {n}"
    est = lambda total, per: f"{total} a year; {per} for each $100,000 of the county auditor's market value"

    # --- School districts ---
    c.issue("issue-1", "levy", "Margaretta Local School District", "Bond issue: $11,000,000 for a natatorium and fitness/multipurpose center", SD("MARGARETTA LOCAL SD (ERIE)"),
            number=N(1), area="Margaretta Local School District (Bay View, Castalia, Groton Township Margaretta part, Margaretta Township 1–4)",
            levy={"type": "Bond issue", "purpose": "Constructing a natatorium and fitness/multipurpose center; furnishing and equipping them; and improving their sites.",
                  "mills": "2.15 mills (estimated average)", "term": "Up to 20 years, commencing in 2026", "firstDue": "2027",
                  "estimate": "$11,000,000 principal; $76 for each $100,000 of the county auditor's market value"},
            text="Shall bonds be issued by the Margaretta Local School District for the purpose of constructing a natatorium and fitness/multipurpose center; furnishing and equipping the same as necessary; "
                 "and improving the sites thereof in the principal amount of $11,000,000, to be repaid annually over a maximum period of 20 years, and an annual levy of property taxes be made outside "
                 "the 10-mill limitation, estimated by the county auditor to average over the repayment period of the bond issue 2.15 mills for each $1 of taxable value, which amounts to $76 for each "
                 "$100,000 of the county auditor's market value, commencing in 2026, first due in calendar year 2027, to pay the annual debt charges on the bonds, and to pay debt charges on any notes "
                 "issued in anticipation of those bonds?", src=I)
    c.levy("issue-2", "Sandusky City School District", SD("SANDUSKY CITY SD"), "Additional", "Current operating expenses.", "4.9 mills",
           "Continuing period of time, commencing in 2027", "2028", est("$3,396,432", "$172"), number=N(2), src=I)
    # Same question as lorain.py's issue-11 (Lorain numbers it 11).
    c.levy("issue-4", "Vermilion Local School District (Erie and Lorain)", SD("VERMILION LOCAL SD (ERIE)"), "Renewal", "Current expenses.", "6.03 mills (estimated average)",
           "5 years, commencing in 2026", "2027", "$4,250,000 a year (fixed sum); $185 for each $100,000 of the county auditor's market value", number=N(4),
           area="Vermilion Local School District, Erie County part (Vermilion City 1-A to 3-B, Florence Township 1 and 2 Vermilion parts, Vermilion Township 1–5)",
           note="A fixed-sum levy renewing an existing levy.", src=I)

    # --- Special districts and countywide ---
    # The notice gives the ambulance district as Florence Township precincts 1 and 2, i.e. all of Florence Township.
    c.levy("issue-5", "Vermilion River Ambulance District", P("FLORENCE TWP"), "Renewal", "Ambulance and emergency medical services: services, equipment and facilities.", "1 mill",
           "5 years, commencing in 2027", "2028", est("$183,400", "$19"), number=N(5), area="Florence Township (Flo Twp #1 and #2)", src=I)
    c.levy("issue-6", "Erie County", "county", "Renewal",
           "Operation of community addiction services providers and community mental health services providers, and the acquisition, construction, renovation, financing, maintenance and operation of alcohol and drug addiction facilities and mental health facilities.",
           "0.7 mill", "10 years, commencing in 2027", "2028", est("$1,555,645", "$15"), number=N(6), src=I)
    # Same question as lorain.py's issue-5 (the Lorain County part of Vermilion).
    c.levy("issue-7", "Erie County General Health District", "county", "Renewal", "Funds for the Board of Health to carry out its health program.", "0.2 mill",
           "5 years, commencing in 2027", "2028", est("$504,712", "$5"), number=N(7), src=I)

    # --- Cities and villages ---
    c.levy("issue-8", "City of Bellevue (Erie, Huron, Sandusky and Seneca)", P("BELLEVUE CITY"), "Renewal", "Parks and recreation.", "1 mill",
           "5 years, commencing in 2027", "2028", est("$181,373", "$19"), number=N(8), area="Bellevue City, Erie County part (Groton Township precinct, Bellevue City only)", src=I)
    # Same four questions as lorain.py's issues 24, 25, 26 and 35; titles follow lorain.py, text is Erie's description.
    # The issue filings list prints Issue 9's precincts as "Ver 3-B, Ver 3-B"; the notice has "Ver 3-A, Ver 3-B".
    VMC = P("VERMILION CITY ")
    for n, art, what in [(9, "Articles III and IV", "Council meetings and legislative powers."), (10, "Article VIII", "Allowing write-in candidates."),
                         (11, "Article XI", "Rural water services."), (12, "Article IX", "Signature requirements for initiatives and referendums.")]:
        c.issue(f"issue-{n}", "question", "City of Vermilion (Erie and Lorain)", f"Charter amendment: {art}", VMC, number=N(n), text=what,
                area="Vermilion City 1-A, 2-A, 2-B, 3-A, 3-B (the Erie County part of Vermilion)", src=I)
    c.levy("issue-14", "Village of Berlin Heights", P("BERLIN HEIGHTS VILLAGE"), "Renewal", "Current expenses.", "4 mills",
           "5 years, commencing in 2027", "2028", est("$92,717", "$91"), number=N(14), src=I)
    c.levy("issue-15", "Village of Bay View", P("BAY VIEW VILLAGE"), "Renewal", "Current expenses.", "3 mills",
           "5 years, commencing in 2026", "2027", est("$43,818", "$67"), number=N(15), src=I)
    c.levy("issue-16", "Village of Castalia", P("CASTALIA VILLAGE"), "Renewal", "General construction, reconstruction, resurfacing and repair of streets, roads and bridges.", "2.75 mills",
           "5 years, commencing in 2027", "2028", est("$52,744", "$78"), number=N(16), src=I)

    # --- Townships ---
    c.levy("issue-17", "Berlin Township (including the Village of Berlin Heights)", P("BERLIN TWP", "BERLIN HEIGHTS VILLAGE"), "Renewal", "Fire protection and emergency medical services.", "1 mill",
           "5 years, commencing in 2026", "2027", est("$123,509", "$21"), number=N(17), area="Berlin Township and Berlin Heights Village (Ber Vill, Ber Twp #1 and #2)", src=I)
    c.levy("issue-18", "Berlin Township (unincorporated area)", P("BERLIN TWP"), "Renewal", "General construction, reconstruction, resurfacing and repair of streets, roads and bridges.", "1 mill",
           "3 years, commencing in 2026", "2027", est("$99,325", "$20"), number=N(18), area="Berlin Township unincorporated area (Ber Twp #1 and #2)", src=I)
    c.levy("issue-19", "Florence Township", P("FLORENCE TWP"), "Additional", "Fire protection and emergency medical services.", "1.5 mills",
           "5 years, commencing in 2026", "2027", est("$179,505", "$53"), number=N(19), src=I)
    c.levy("issue-20", "Margaretta Township (including the Village of Castalia)", P("MARGARETTA TWP", "CASTALIA VILLAGE"), "Renewal", "Fire protection and emergency medical services.", "2 mills",
           "5 years, commencing in 2026", "2027", est("$258,965", "$46"), number=N(20), area="Margaretta Township and Castalia Village (Cast Vill, Mar Twp #1–#4)", src=I)
    c.levy("issue-21", "Perkins Township", P("PERKINS TWP"), "Renewal", "Fire protection and emergency medical services.", "2.75 mills",
           "5 years, commencing in 2026", "2027", est("$1,234,168", "$67"), number=N(21), src=I)
    c.levy("issue-22", "Perkins Township", P("PERKINS TWP"), "Renewal", "Police protection.", "2.75 mills",
           "5 years, commencing in 2026", "2027", est("$1,234,168", "$67"), number=N(22), src=I)

    # --- Local liquor options ---
    LQ = [
        (13, "City of Vermilion", "VERMILION CITY ", "Vermilion 1-A", "Sur Market & Sundries (Sunday)",
         "Shall the sale of wine and mixed beverages, and spirituous liquor be permitted for sale on Sunday by Sur Market & Sundries, LLC a holder of C-1 and C-2 liquor permits who is engaged in the business of a retail market and grab & go food mart at 5312 Liberty Ave, Vermilion, OH 44089 in this precinct?"),
        (23, "Vermilion Township", "VERMILION TWP", "Vermilion Township #5", "Patio Tavern (Sunday)",
         "Shall the sale of wine and mixed beverages, and spirituous liquor be permitted for sale on Sunday by Patio Tavern, Ltd. an applicant for a D6 permit who is engaged in the business of operating a bar and restaurant at 4708 Cleveland Road E., Huron, Ohio 44839 in this precinct?"),
    ]
    for n, jur, raw, pct, biz, text in LQ:
        c.issue(f"issue-{n}", "liquor", jur, f"Local liquor option: {biz}", P(raw), number=N(n), area=f"Precinct {pct}", text=text, src=I)
    c.issues.sort(key=lambda q: int(q["id"].split("-")[1]))
    return c
