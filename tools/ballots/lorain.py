from lib import County, NOTE_ORDER, NOTE_PLACES

CAND = "https://www.voteloraincountyohio.gov/_files/ugd/2568d0_ef2bd7f0adc244659d5357bfa1879d07.pdf"
ISS = "https://www.voteloraincountyohio.gov/_files/ugd/2568d0_43fda2b6f075408eac60476a8ac14199.pdf"
FWAB = "https://www.voteloraincountyohio.gov/_files/ugd/2568d0_e55c96ca0eed4b9c9ddde5badc61b9e2.pdf"

def build():
    c = County("lorain", "Lorain", "39093", rename={"ROCHESTER TWP & VIL": "Rochester Township & Village", "VERMILION CITY ": "Vermilion City"})
    c.src("lorain-cand", "Lorain County Board of Elections: certified candidate list, 2026 General (9/14/2026)", CAND)
    c.src("lorain-issues", "Lorain County Board of Elections: certified issues list, 2026 General (9/9/2026)", ISS)
    c.src("lorain-46day", "Lorain County Board of Elections: 46-day FWAB notice (issues), November 3, 2026 General Election", FWAB)
    C = ["lorain-cand"]; I = ["lorain-issues", "lorain-46day"]
    c.links = [
        {"label": "Board of Elections", "url": "https://www.voteloraincountyohio.gov/"},
        {"label": "Find your sample ballot", "url": "https://www.voteloraincountyohio.gov/find-ballot"},
    ]
    c.results_links = [{"label": "Board of Elections: results search", "url": "https://www.voteloraincountyohio.gov/elections-results-search"}]
    c.notes = ["Taken from the Board of Elections' certified candidate and issues lists and its 46-day notice, which give each issue as a one-line summary "
               "with the precincts that vote on it; the full wording is on the sample ballot.", NOTE_ORDER, NOTE_PLACES]
    P = c.p; D = c.district; SD = c.sd

    c.contest("congress-5", "U.S. House", "Representative to Congress", [("Bob Latta", "REP"), ("Brian A. Shaver", "DEM"), ("Michael J. Veloff", "LIB")], detail="5th District", src=C)
    c.contest("senate-13", "Ohio General Assembly", "State Senator", [("Gayle Manning", "REP"), ("Joe Miller", "DEM")], detail="13th District", src=C)
    for n, cs in {52: [("Mike Baker", "DEM"), ("Cliff Winkel", "REP")], 53: [("Bradley Lacko", "REP"), ("Matt Lundy", "DEM")],
                  54: [("Brenda Buchanan", "DEM"), ("Kellie Deeter", "REP")]}.items():
        c.contest(f"rep-{n}", "Ohio General Assembly", "State Representative", cs, detail=f"{n}nd District" if n == 52 else f"{n}rd District" if n == 53 else f"{n}th District", places=D("rep", n), src=C)
    c.contest("appeals-9-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Cynthia Curtin", "REP"), ("Betty Sutton", "DEM")], detail="9th District · full term commencing February 9, 2027", src=C)
    c.contest("appeals-9-0210", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Tavia Galonski", "DEM"), ("Nathan Manning", "REP")], detail="9th District · unexpired term ending February 9, 2029", src=C)
    c.contest("commissioner", "County offices", "County Commissioner", [("Jeff Riddell", "REP"), ("Carolyn Y. White", "DEM"), ("Andrew Lipian", "Write-in")], detail="Full term commencing January 1, 2027", src=C)
    c.contest("auditor", "County offices", "County Auditor", [("Elaine M. Seguin", "REP"), ("Craig Snodgrass", "DEM")], detail="Full term commencing March 8, 2027", src=C)
    c.contest("cp-probate", "Court of Common Pleas", "Judge of the Court of Common Pleas, Probate Division", ["James T. Walther"], detail="Full term commencing February 9, 2027 · no party label on the ballot", src=C)

    N = lambda n: f"Issue {n}"
    VMC = P("VERMILION CITY ")
    L = [
        (1, "Amherst Exempted Village School District", SD("AMHERST EX VILL SD (LORAIN)"), "Additional", "Current expenses.", "5.97 mills", "Continuing period of time", None),
        (2, "Clearview Local School District", SD("CLEARVIEW LOCAL SD (LORAIN)"), "Renewal", "Current expenses.", "3.91 mills", "5 years", "Lorain City 4E, part of 5A, 5C, 6C; Sheffield Township North, East and West"),
        (4, "Elyria City School District", SD("ELYRIA CITY SD"), "Additional", "Current expenses.", "8.9 mills", "Continuing period of time", None),
        (5, "Erie County General Health District", VMC, "Renewal", "Funds for the Board of Health to carry out its health program.", "0.2 mill", "5 years", "Vermilion City 1A, 3A/5A, 4A, 5B (the Lorain County part of Vermilion)"),
        (6, "Herrick Memorial Library", P("WELLINGTON TOWNSHIP", "WELLINGTON VILLAGE", "BRIGHTON TOWNSHIP", "PITTSFIELD TOWNSHIP", "ROCHESTER TWP & VIL", "HUNTINGTON TOWNSHIP"),
         "Renewal", "Current expenses.", "1.25 mills", "5 years", "All of Wellington Township, Wellington Village, Brighton Township and Huntington Township; parts of Pittsfield and Rochester"),
        (7, "Lorain County General Health District", sorted(set(c.places) - {"Vermilion City"}), "Renewal", "Operating expenses of the Lorain County General Health District.", "0.5 mill", "5 years", "All of Lorain County except Vermilion City"),
        (9, "Oberlin City School District", SD("OBERLIN CITY SD"), "Renewal", "Education technology.", "1.3 mills", "5 years", None),
        (10, "Strongsville City School District (Cuyahoga and Lorain)", SD("STRONGSVILLE CITY SD"), "Additional", "Current expenses.", "6.7 mills", "5 years", "Part of Columbia Township #2 and #5"),
        (11, "Vermilion Local School District (Erie and Lorain)", SD("VERMILION LOCAL SD (ERIE)"), "Renewal", "Current expenses.", "6.03 mills", "5 years", "Part of Brownhelm Township; Lorain City 8A; Vermilion City 1A, 4A, part of 3A/5A"),
        (12, "Lorain County", "county", "Additional", "Children Services and the Bureau of Children with Medical Handicaps.", "0.45 mill", "5 years", "All of Lorain County"),
        (22, "Village of Kipton", P("KIPTON VILLAGE"), "Renewal", "Permanent sewer improvements.", "2 mills", "5 years", None),
        (27, "Brighton Township", P("BRIGHTON TOWNSHIP"), "Renewal", "Road improvements.", "1 mill", "5 years", None),
        (28, "Columbia Township", P("COLUMBIA TOWNSHIP"), "Renewal", "Road improvements.", "1 mill", "5 years", None),
        (32, "Henrietta Township", P("HENRIETTA TOWNSHIP"), "Renewal", "Road and bridge services.", "1 mill", "5 years", None),
        (33, "Henrietta Township", P("HENRIETTA TOWNSHIP"), "Renewal", "Fire protection.", "0.75 mill", "5 years", None),
        (34, "Sheffield Township", P("SHEFFIELD TOWNSHIP"), "Additional", "Fire and E.M.S.", "2.5 mills", "5 years", None),
    ]
    for n, jur, places, t, purpose, mills, term, area in L:
        c.levy(f"issue-{n}", jur, places, t, purpose, mills, term, number=N(n), area=area, src=I)
    c.issue("issue-8", "question", "Oberlin City School District", "School district income tax: renewal of 0.75% for current expenses, 5 years", SD("OBERLIN CITY SD"), number=N(8),
            text="Renewal of a 0.75% income tax, for current expenses, for 5 years.", src=I)
    c.issue("issue-16", "question", "City of Avon Lake", "Income tax increase from 1.5% to 1.9% for road maintenance, 6 years", P("AVON LAKE CITY"), number=N(16),
            text="Increase of the municipal income tax from 1.5% to 1.9%, for general road maintenance, for 6 years.", src=I)
    c.issue("issue-36", "question", "City of Avon Lake", "Charter amendment: Chapter XIII, rezoning and tax increment financing", P("AVON LAKE CITY"), number=N(36),
            text="Charter amendment to Chapter XIII, concerning rezoning and tax increment financing.", src=I)
    for n, art, what in [(18, "Article V, Sections 1 and 2", "Appointment of positions."), (19, "Article VI, Section 1", "Requirements of positions."), (20, "Article XIV", "Charter Review Commission.")]:
        c.issue(f"issue-{n}", "question", "Village of Grafton", f"Charter amendment: {art}", P("GRAFTON VILLAGE"), number=N(n), text=what, src=I)
    for n, art, what in [(24, "Articles III and IV", "Legislative powers."), (25, "Article VIII", "Write-in candidates."), (26, "Article XI", "Rural water service."),
                         (35, "Article IX", "Initiative and referendum signature requirement.")]:
        c.issue(f"issue-{n}", "question", "City of Vermilion (Erie and Lorain)", f"Charter amendment: {art}", VMC, number=N(n), text=what, area="Vermilion City 1A, 3A/5A, 4A, 5B", src=I)
    LQ = [
        (13, "City of Avon", "AVON CITY", "Avon City 2A", "In Forno Pizza Studio (Sunday)", "Sunday sales; In Forno Pizza Studio LLC dba In Forno Pizza."),
        (14, "City of Avon", "AVON CITY", "Avon City 2B", "Westside Pancake Company (Sunday)", "Sunday sales; Schuster Management, L.L.C., dba Westside Pancake Company."),
        (15, "City of Avon", "AVON CITY", "Avon City 2B", "Strip A Steakhouse (Sunday)", "Sunday sales; Lavender Farms LLC dba Strip A Steakhouse."),
        (17, "City of Elyria", "ELYRIA CITY", "Elyria City 2D", "Nirvana Grocers (Sunday)", "Sunday sales; Nirvana Grocers LLC."),
        (21, "Village of Grafton", "GRAFTON VILLAGE", "Grafton Village 1/2", "CC Saloon (Sunday)", "Sunday sales; CC Saloon, LLC."),
        (23, "City of North Ridgeville", "NORTH RIDGEVILLE CITY", "North Ridgeville City 4F", "Buns and Brews Sports Bar and Grill (Sunday)", "Sunday sales; Buns and Brews Sports Bar and Grill LLC."),
        (29, "Columbia Township", "COLUMBIA TOWNSHIP", "Columbia Township #4", "Columbia Station Eagles (Sunday)", "Sunday sales; Columbia Station Eagles 4003 FOE Inc."),
        (30, "Eaton Township", "EATON TOWNSHIP", "Eaton Township 3", "Sheetz (Sunday)", "Sunday sales; Ohio Springs Inc. d/b/a Sheetz."),
        (31, "Eaton Township", "EATON TOWNSHIP", "Eaton Township 3", "Sheetz (weekday)", "Weekday sales; Ohio Springs Inc. d/b/a Sheetz."),
    ]
    for n, jur, raw, pct, biz, text in LQ:
        c.issue(f"issue-{n}", "liquor", jur, f"Local liquor option: {biz}", P(raw), number=N(n), area=f"Precinct {pct}", text=text, src=I)
    return c
