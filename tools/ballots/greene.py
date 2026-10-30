from lib import County, NOTE_ORDER, NOTE_PLACES

NOTICE = "https://www.boe.ohio.gov/greene/c/upload/FWAB_11November46Day.pdf"
CAND = "https://www.boe.ohio.gov/greene/c/upload/Election_CandidatesList.pdf"
ISSUES = "https://www.boe.ohio.gov/greene/c/upload/Election_QIList.pdf"

def build():
    # Raw names: townships are bare ("BEAVERCREEK", "CAESARSCREEK", "XENIA"), so the default bare="Township"
    # gives "Beavercreek Township", "Caesarscreek Township" etc., matching the Board's spelling (precinct "CAESARSCREEK 460").
    c = County("greene", "Greene", "39057")
    c.src("greene-46day", "Greene County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election", NOTICE)
    c.src("greene-cand", "Greene County Board of Elections: certified candidates, November 3, 2026 General Election (revised June 30, 2026)", CAND)
    c.src("greene-issues", "Greene County Board of Elections: local questions and issues list, November 3, 2026 General Election", ISSUES)
    C = ["greene-46day", "greene-cand"]; I = ["greene-46day", "greene-issues"]
    c.links = [
        {"label": "Board of Elections", "url": "https://www.boe.ohio.gov/greene/"},
        {"label": "Election info", "url": "https://www.boe.ohio.gov/greene/election-info/"},
        {"label": "Sample ballots by precinct", "url": "https://lookup.boe.ohio.gov/vtrapp/greene/ballotlist.aspx"},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://www.boe.ohio.gov/greene/election-info/election-night-results"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it, "
               "checked against the Board's certified candidate list and local questions and issues list. Issue wording is the Board's summary; the full wording is on the sample ballot.",
               NOTE_ORDER, NOTE_PLACES]
    P = c.p; D = c.district; SD = c.sd

    # The 10th Congressional, 70th/71st House and 2nd Appeals districts cover all of Greene; the 10th Senate district is not up in 2026.
    c.contest("congress-10", "U.S. House", "Representative to Congress", [("Kristina Knickerbocker", "DEM"), ("Thomas F. McMasters", "LIB"), ("Mike Turner", "REP")], detail="10th District", src=C)
    c.contest("rep-70", "Ohio General Assembly", "State Representative", [("Brian Lampton", "REP"), ("Kim McCarthy", "DEM")], detail="70th District", places=D("rep", 70), src=C)
    c.contest("rep-71", "Ohio General Assembly", "State Representative", [("Levi Dean", "REP"), ("Krista Magaw", "DEM")], detail="71st District", places=D("rep", 71), src=C)
    c.contest("appeals-2-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Chris Epley", "REP")], detail="2nd District · term commencing February 9, 2027", src=C)
    c.contest("commissioner", "County offices", "County Commissioner", [("Dick Gould", "REP")], detail="Term commencing January 1, 2027", src=C)
    c.contest("treasurer", "County offices", "County Treasurer", [("Amanda L. Jenkins", "REP")], detail="Unexpired term ending September 2, 2029", src=C)
    c.contest("auditor", "County offices", "County Auditor", [("Kraig A. Hagler", "REP")], src=C)
    NP = " · no party label on the ballot"
    for id, office, date, cs in [
        ("cp-0102", "General Division", "Term commencing January 2, 2027", ["Michael A. Buckwalter"]),
        ("cp-probate", "Probate Division", "Term commencing February 9, 2027", ["Wayne Waite"]),
        ("cp-dr", "Domestic Relations Division", "Term commencing January 1, 2027", ["Cynthia Martin"]),
    ]:
        c.contest(id, "Court of Common Pleas", f"Judge of the Court of Common Pleas, {office}", cs, detail=date + NP, src=C)

    N = lambda n: f"Issue {n}"
    est = lambda per: f"{per} for each $100,000 of market value"
    c.levy("issue-4", "Greene County", "county", "Renewal", "Roads and bridges.", "0.25 mill", "5 years, commencing in 2026", "2027", est("$5"), number=N(4), src=I)
    c.issue("issue-5", "question", "City of Beavercreek", "Municipal income tax: 1% for general municipal operations", P("BEAVERCREEK CITY"), number=N(5),
            text="Proposed 1% municipal income tax, commencing in 2027, for general municipal operations.", src=I)
    c.levy("issue-6", "City of Bellbrook", P("BELLBROOK CITY"), "Renewal", "Current expenses.", "1.3 mills", "5 years, commencing in 2026", "2027", est("$28"), number=N(6), src=I)
    BV = P("BOWERSVILLE VILLAGE")
    c.levy("issue-7", "Village of Bowersville", BV, "Renewal", "Current expenses.", "3.5 mills", "5 years, commencing in 2028", "2029", est("$84"), number=N(7), src=I)
    c.levy("issue-8", "Village of Bowersville", BV, "Renewal", "Current expenses.", "2.6 mills", "5 years, commencing in 2028", "2029", est("$45"), number=N(8), src=I)
    SVV = P("SPRING VALLEY VILLAGE")
    c.levy("issue-9", "Village of Spring Valley", SVV, "Additional", "Streets and roads.", "2 mills", "5 years, commencing in 2027", None, est("$70"), number=N(9), src=I)
    c.levy("issue-10", "Village of Spring Valley", SVV, "Renewal", "Streets.", "0.25 mill", "5 years, commencing in 2026", None, est("$6"), number=N(10), src=I)
    c.levy("issue-11", "Village of Spring Valley", SVV, "Renewal", "Streets and roads.", "1 mill", "5 years, commencing in 2026", None, est("$22"), number=N(11), src=I)
    c.levy("issue-12", "Village of Spring Valley", SVV, "Renewal", "Current expenses.", "2.3 mills", "5 years", None, est("$51"), number=N(12), src=I)
    SV = P("SPRING VALLEY VILLAGE", "SPRING VALLEY")
    c.levy("issue-13", "Spring Valley Township (including the Village of Spring Valley)", SV, "Renewal", "Current expenses.", "1 mill", "5 years, commencing in 2027", None, est("$23"),
           number=N(13), area="Spring Valley Village and Spring Valley Township", src=I)
    c.levy("issue-14", "Village of Cedarville", P("CEDARVILLE VILLAGE"), "Renewal", "Current expenses.", "2.6 mills", "5 years, commencing in 2026", "2027", est("$12"), number=N(14), src=I)
    c.levy("issue-15", "Cedarville Township (including the Village of Cedarville)", P("CEDARVILLE VILLAGE", "CEDARVILLE"), "Renewal", "Fire and EMS.", "1 mill", "5 years, commencing in 2027", "2028", est("$22"),
           number=N(15), area="Cedarville Village and Cedarville Township", src=I)
    c.levy("issue-16", "Ross Township", P("ROSS"), "Renewal", "Fire and EMS.", "1.5 mills", "5 years, commencing in 2027", "2028", est("$11"), number=N(16), src=I)
    JT = P("JEFFERSON", "BOWERSVILLE VILLAGE")
    c.levy("issue-17", "Jefferson Township (including the Village of Bowersville)", JT, "Renewal", "Fire and EMS.", "1.5 mills", "5 years, commencing in 2027", "2028", est("$19"),
           number=N(17), area="Jefferson Township and Bowersville Village", src=I)
    c.levy("issue-18", "Jefferson Township (including the Village of Bowersville)", JT, "Renewal", "Fire and EMS.", "2 mills", "5 years, commencing in 2027", "2028", est("$17"),
           number=N(18), area="Jefferson Township and Bowersville Village", src=I)
    c.levy("issue-19", "New Jasper Township", P("NEW JASPER"), "Additional", "Fire and EMS.", "2 mills", "5 years, commencing in 2027", "2028", est("$70"), number=N(19), src=I)
    c.levy("issue-20", "Miami Township (including the Villages of Yellow Springs and Clifton)", P("MIAMI", "YELLOW SPRINGS VILLAGE", "CLIFTON VILLAGE"), "Additional", "Fire and EMS.", "0.8 mill",
           "Continuing period of time, commencing in 2026", None, est("$28"), number=N(20), area="Miami Township, Yellow Springs Village and Clifton Village",
           note="The Board's list gives both \"5 years\" and \"CPT\" (continuing period of time) for this levy; the township describes it as a permanent levy.", src=I)
    c.levy("issue-21", "Spring Valley Township (including the Village of Spring Valley)", SV, "Renewal", "Current expenses.", "0.30 mill", "5 years, commencing in 2027", None, est("$2"),
           number=N(21), area="Spring Valley Village and Spring Valley Township", src=I)
    c.issue("issue-22", "question", "City of Xenia", "Charter amendment: Sections 4.01(G)(2), 4.05(A), 5.01(B), 9.04(C)(3) and 13.01, Articles XI and XII", P("XENIA CITY"), number=N(22),
            text="Proposed amendments to Section 4.01(G)(2), Section 4.05(A), Section 5.01(B), Section 9.04(C)(3), Article XI, Article XII and Section 13.01 of the Xenia City Charter.", src=I)

    # Unnumbered in Greene County's lists.
    c.issue("fairborn-liquor-205", "liquor", "City of Fairborn", "Local liquor option: Amvets Post 0444 (Sunday)", P("FAIRBORN CITY"), area="Fairborn precinct 205",
            text="Sunday sale of wine and mixed beverages, and spirituous liquor by Amvets Post 0444, holder of a D-6 liquor permit.", note="Unnumbered in Greene County.", src=I)
    c.issue("xenia-liquor-303", "liquor", "City of Xenia", "Local liquor option: VFW Post 2402 Cooper Jordan Memorial (Sunday)", P("XENIA CITY"), area="Xenia precinct 303",
            text="Sunday sale of beer, wine and mixed beverages, and spirituous liquor by VFW Post 2402 Cooper Jordan Memorial, holder of a D-6 liquor permit.", note="Unnumbered in Greene County.", src=I)
    # Kettering is mostly in Montgomery County (Issues 15-19 there). The notice lists Greene precincts 090/2 and 150/2;
    # the voter file puts Greene's Kettering voters in Beavercreek 090 and Sugarcreek 151.
    KT = P("KETTERING CITY")
    KA = "Kettering (Greene County part: precincts 090 split 2 and 150 split 2)"
    for id, title, text in [
        ("kettering-charter-appeals", "Charter amendment: Sections 7-3 and 7-5 (appeals to Council)", "Amend Section 7-3, Appeals from the Planning Commission to Council, and Section 7-5, Appeals from the Board of Zoning Appeals to Council."),
        ("kettering-charter-pronouns", "Charter amendment: gender-neutral wording", "Amend Sections 3-2, 3-3, 3-6, 3-8, 5-1, 5-2, 5-3, 5-4, 5-5, 5-6, 5-7, 8-3 and 8-4 to change the use of gender-specific pronouns to the corresponding nouns."),
        ("kettering-charter-ordinances", "Charter amendment: Section 4-3 (procedure of passage of ordinances)", "Amend Section 4-3, Procedure of Passage of Ordinances."),
        ("kettering-charter-powers", "Charter amendment: Section 7-2 (powers and duties)", "Amend Section 7-2, Powers and Duties."),
        ("kettering-charter-manager", "Charter amendment: Sections 5-2 and 6-2 (the Manager; department directors)", "Amend Article V, Section 5-2, The Manager, and Article VI, Section 6-2, Department Directors."),
    ]:
        c.issue(id, "question", "City of Kettering (Montgomery and Greene)", title, KT, area=KA, text=text,
                note="Unnumbered in Greene County's lists; Montgomery County numbers the Kettering charter amendments Issues 15-19.", src=I)
    # Southeastern Local SD is a Clark County district; the SoS voter file labels its Greene voters "SOUTHEAST LOCAL SD (PORTAGE)"
    # (Cedarville 411 and Ross 475 precincts, matching the notice's 411/3 and 475/3).
    c.issue("southeastern-lsd-tax", "question", "Southeastern Local School District (Clark and Greene)", "School district income tax: 0.5% for 5 years, for current expenses",
            SD("SOUTHEAST LOCAL SD (PORTAGE)"), area="Cedarville Township precinct 411 (split 3) and Ross Township precinct 475 (split 3)",
            text="Proposed income tax of 0.50% on the school district income of individuals, for 5 years, beginning January 1, 2027, for current expenses.",
            note="Unnumbered in Greene County.", src=I)
    return c
