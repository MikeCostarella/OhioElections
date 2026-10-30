from lib import County, NOTE_ORDER, NOTE_PLACES, NOTE_UNKNOWN

CAND = "https://www.starkcountyohio.gov/Board%20of%20Elections/Candidates%20List%20General.pdf"
ISS = "https://www.starkcountyohio.gov/Board%20of%20Elections/General%202026_issues%20list_w%20numbers.pdf"

def build():
    c = County("stark", "Stark", "39151")
    c.src("stark-cand", "Stark County Board of Elections: candidates list, November 3, 2026 General Election (10/15/2026)", CAND)
    c.src("stark-issues", "Stark County Board of Elections: questions and issues list, November 3, 2026 General Election", ISS)
    C = ["stark-cand"]; I = ["stark-issues"]
    c.links = [{"label": "Board of Elections", "url": "https://www.starkcountyohio.gov/government/offices/board_of_elections/index.php"},
               {"label": "Ohio sample ballot lookup", "url": "https://www.ohiosos.gov/elections/voters/toolkit/sample-ballot/"}]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://www.starkcountyohio.gov/government/offices/board_of_elections/index.php"}]
    c.notes = ["Taken from the Board of Elections' candidates list and its questions and issues list, which gives each issue as a one-line summary; "
               "the full wording is on the sample ballot.", NOTE_ORDER, NOTE_PLACES, NOTE_UNKNOWN]
    D = c.district; P = c.p; SD = c.sd

    c.contest("congress-6", "U.S. House", "Representative to Congress", [("Elizabeth Kirtley", "DEM"), ("Michael A. Rulli", "REP")], detail="6th District", places=D("cong", 6), src=C)
    c.contest("congress-13", "U.S. House", "Representative to Congress", [("Emilia Sykes", "DEM"), ("Sandeep Dixit", "Non-party"), ("Carey Coleman", "REP")], detail="13th District", places=D("cong", 13), src=C)
    c.contest("appeals-5", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Matthew George", "REP")], detail="5th District · term commencing February 9, 2027", src=C)
    c.contest("senate-29", "Ohio General Assembly", "State Senator", [("Thomas West", "DEM"), ("Jane Timken", "REP")], detail="29th District", places=D("sen", 29), src=C)
    c.contest("senate-31", "Ohio General Assembly", "State Senator", [("Laura Sirot", "DEM"), ("Al Landis", "REP")], detail="31st District", places=D("sen", 31), src=C)
    for n, cs in {48: [("Nick Morris", "DEM"), ("Christina M. Hagan", "REP")], 49: [("Krista L. Allison", "DEM"), ("Jim Thomas", "REP")],
                  50: [("Rylan Zachary Finzer", "DEM"), ("Matthew Kishman", "REP")], 51: [("Amanda Fontana", "DEM"), ("Jodi Salvo", "REP")]}.items():
        c.contest(f"rep-{n}", "Ohio General Assembly", "State Representative", cs, detail=f"{n}th District", places=D("rep", n), src=C)
    c.contest("commissioner", "County offices", "County Commissioner", [("Tony M. Townsend", "DEM"), ("Alan Harold", "REP")], src=C)
    c.contest("auditor", "County offices", "County Auditor", [("Chalice E. Brown", "DEM"), ("Angela Kinsey", "REP")], src=C)
    NP = " · no party label on the ballot"
    c.contest("cp-gen-0101", "Court of Common Pleas", "Judge of the Court of Common Pleas, General Division", ["Kristin G. Farmer"], detail="Term commencing January 1, 2027" + NP, src=C)
    c.contest("cp-gen-0104", "Court of Common Pleas", "Judge of the Court of Common Pleas, General Division", ["Frank G. Forchione"], detail="Term commencing January 4, 2027" + NP, src=C)
    c.contest("cp-gen-0209", "Court of Common Pleas", "Judge of the Court of Common Pleas, General Division", ["Kristen S. Moore", "Jennifer L. Dave"], detail="Term commencing February 9, 2027" + NP, src=C)
    c.contest("cp-probate", "Court of Common Pleas", "Judge of the Court of Common Pleas, Probate Division", ["Curt Werren"], detail=NP.strip(" ·"), src=C)

    N = lambda n: f"Issue {n}"
    L = [
        (4, "Stark County District Library", "county", "Renewal and increase", "Current expenses (renewal of 2 mills and increase of 0.3 mill).", "2.3 mills", "8 years, commencing in 2027"),
        (None, "Wayne County Joint Vocational School District (Wayne, Ashland, Holmes, Medina and Stark)", None, "Renewal", "General permanent improvements.", "0.5 mill", "5 years, commencing in 2027"),
        (6, "Sandy Valley Local School District (Stark, Carroll and Tuscarawas)", SD("SANDY VALLEY LOCAL SD (STARK)"), "Renewal", "Current expenses.", "2.3 mills", "5 years, commencing in 2027"),
        (7, "Massillon City School District", SD("MASSILLON CITY SD"), "Renewal", "Current expenses.", "4.9 mills", "5 years, commencing in 2027"),
        (8, "Alliance City School District (Stark, Columbiana and Mahoning)", SD("ALLIANCE CITY SD"), "Renewal", "General permanent improvements.", "2 mills", "5 years, commencing in 2027"),
        (10, "Village of East Sparta", P("EAST SPARTA VILLAGE"), "Renewal", "Current expenses.", "6.5 mills", "5 years, commencing in 2026"),
        (11, "Village of East Sparta", P("EAST SPARTA VILLAGE"), "Renewal", "Police.", "3 mills", "5 years, commencing in 2026"),
        (13, "Village of Beach City", P("BEACH CITY VILLAGE"), "Additional", "Roads.", "5 mills", "5 years, commencing in 2026"),
        (17, "Village of Magnolia (Stark and Carroll)", P("MAGNOLIA VILLAGE"), "Renewal", "Police.", "4 mills", "5 years, commencing in 2027"),
        (22, "Pike Township Fire District", P("PIKE"), "Renewal", "Fire.", "1 mill", "5 years, commencing in 2027"),
        (23, "Nimishillen Township", P("NIMISHILLEN"), "Additional", "Fire.", "3 mills", "5 years, commencing in 2027"),
        (24, "Lake Township Fire District", P("LAKE"), "Additional", "Fire.", "2.75 mills", "5 years, commencing in 2026"),
        (25, "Lawrence Township Fire District", P("LAWRENCE"), "Renewal", "Fire.", "0.5 mill", "5 years, commencing in 2027"),
        (26, "Plain Township Road District", P("PLAIN"), "Renewal", "Roads.", "1.5 mills", "5 years, commencing in 2027"),
        (27, "Marlboro Township", P("MARLBORO"), "Renewal", "Roads.", "2 mills", "5 years, commencing in 2027"),
        (28, "Paris Township Road District Number One", P("PARIS"), "Additional", "Roads.", "2 mills", "5 years, commencing in 2026"),
        (29, "Lexington Township", P("LEXINGTON"), "Additional", "Roads.", "1.5 mills", "5 years, commencing in 2027"),
        (30, "Perry Township", P("PERRY"), "Renewal", "Roads.", "2 mills", "5 years, commencing in 2026"),
    ]
    for n, jur, places, t, purpose, mills, term in L:
        c.levy(f"issue-{n}" if n else "wayne-jvsd", jur, places, t, purpose, mills, term, number=N(n) if n else None, src=I,
               note=None if n else "Listed without an issue number on the Board's list.")
    c.issue("issue-5", "levy", "Plain Local School District", "Bond issue: $116,802,000 for school buildings and facilities", SD("PLAIN LOCAL SD (STARK)"), number=N(5),
            levy={"type": "Bond issue", "purpose": "Constructing, furnishing, equipping, renovating and improving school district buildings and facilities and their sites, and demolishing existing buildings.", "mills": "3.5 mills", "term": "Up to 37 years, commencing in 2026", "estimate": "$116,802,000 principal"}, src=I)
    c.issue("issue-9", "question", "Stark Area Regional Transit Authority (SARTA)", "Continuation of 0.25% sales and use tax for transit, 10 years", "county", number=N(9), area="All of Stark County",
            text="Continuation of the 0.25% sales and use tax for all transit purposes, for 10 years.", src=I)
    c.issue("issue-18", "question", "Village of Navarre", "Additional 0.25% income tax for police", P("NAVARRE VILLAGE"), number=N(18), text="Additional ¼% income tax, for police purposes.", src=I)
    c.issue("issue-19", "question", "Village of Wilmot", "Additional 0.25% income tax for village operations", P("WILMOT VILLAGE"), number=N(19),
            text="Additional ¼% income tax, for general use of operations, maintenance, new equipment, extension, enlargement of village services and facilities and capital improvements.", src=I)
    LQ = [
        (12, "City of Alliance", "ALLIANCE CITY", "Alliance 1-B", "Mom's Drive Thru (Sunday)", "Sunday sales of wine and mixed beverages; Hanny Rahi, L.L.C., dba Mom's Drive Thru, 840 Diehl Court, Alliance."),
        (14, "Lake Township", "LAKE", "Lake Township A", "Hartville Mini Mart (wine and mixed beverages)", "Sale of wine and mixed beverages; CNEPAL, L.L.C., dba Hartville Mini Mart, 260 S. Prospect Avenue, Hartville."),
        (15, "Lake Township", "LAKE", "Lake Township A", "Hartville Mini Mart (beer)", "Sale of beer; CNEPAL, L.L.C., dba Hartville Mini Mart, 260 S. Prospect Avenue, Hartville."),
        (16, "Paris Township", "PARIS", "Paris Township A", "Tipsy Teller Urban Winery (Sunday)", "Sunday sales of wine and mixed beverages; Tipsy Farmer Winery LLC, dba Tipsy Teller Urban Winery LLC, 123 N. Main Street, Minerva."),
        (20, "City of Canal Fulton", "CANAL FULTON CITY", "Canal Fulton B", "Dragonfly Tea Room & Gift Shop (Sunday)", "Sunday sales of beer, wine and mixed beverages; Dragonfly Tea Room & Gift Shop, LLC, 215 Market St. W, Canal Fulton."),
        (21, "City of Massillon", "MASSILLON CITY", "Massillon 5-B", "9th St Event Center (Sunday)", "Sunday sales of wine and mixed beverages and spirituous liquor; Lamoore Enterprises Inc, dba 9th St Event Center, 1008 9th St. SW, 1st Fl Unit C only, Massillon."),
        (31, "Lake Township", "LAKE", "Lake Township 10", "The Cedar Room", "Sale of beer, wine and mixed beverages; The Boyd Wholesale Group, LLC d/b/a The Cedar Room, 13069 Cleveland Ave., Uniontown."),
    ]
    for n, jur, raw, pct, biz, text in LQ:
        c.issue(f"issue-{n}", "liquor", jur, f"Local liquor option: {biz}", P(raw), number=N(n), area=f"Precinct {pct}", text=text, src=I)
    return c
