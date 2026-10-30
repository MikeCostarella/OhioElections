from lib import County, NOTE_ORDER, NOTE_PLACES

SITE = "https://votehamiltoncountyohio.gov/"
NOTICE = "https://votehamiltoncountyohio.gov/wp-content/uploads/2026/09/G26-46-Day-Notice-9-15-26.pdf"
CAND = "https://votehamiltoncountyohio.gov/wp-content/uploads/2026/10/November-2026-All-Certified-Candidates-Profile-.pdf"
ISSUES = "https://votehamiltoncountyohio.gov/wp-content/uploads/2026/09/Nov-2026-QUESTIONS-AND-ISSUES-Filed-2.pdf"
BALLOT = "https://votehamiltoncountyohio.gov/wp-content/uploads/2026/09/November-2026-Ballot-Issues.pdf"

TWPS = ["ANDERSON", "COLERAIN", "COLUMBIA", "CROSBY", "DELHI", "GREEN", "HARRISON", "MIAMI", "SPRINGFIELD", "SYCAMORE", "SYMMES", "WHITEWATER"]
SILVERTON = ["SILVERTON A", "SILVERTON B", "SILVERTON C"]
ST_BERNARD = ["ST BERNARD 1-A", "ST BERNARD 2-A", "ST BERNARD 3-A", "ST BERNARD 4-A"]


def build():
    rename = {f"{t} TWP.": f"{t.title()} Township" for t in TWPS}
    # The SoS file splits Silverton and St. Bernard by precinct; the Board calls both villages.
    rename.update({r: "Silverton Village" for r in SILVERTON})
    rename.update({r: "St. Bernard Village" for r in ST_BERNARD})
    rename.update({"THE VILLAGE OF INDIAN HILL CITY": "Indian Hill City", "ELMWOOD VILLAGE": "Elmwood Place Village"})
    c = County("hamilton", "Hamilton", "39061", rename=rename)
    c.src("hamilton-46day", "Hamilton County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election", NOTICE)
    c.src("hamilton-cand", "Hamilton County Board of Elections: certified candidate list, November 2026 General Election", CAND)
    c.src("hamilton-issues", "Hamilton County Board of Elections: questions and issues certified, November 3, 2026 General Election", ISSUES)
    c.src("hamilton-ballot", "Hamilton County Board of Elections: ballot issues (ballot wording), November 2026 General Election", BALLOT)
    C = ["hamilton-46day", "hamilton-cand"]; I = ["hamilton-ballot", "hamilton-issues", "hamilton-46day"]
    c.links = [
        {"label": "Board of Elections", "url": SITE},
        {"label": "November 2026 General Election", "url": "https://votehamiltoncountyohio.gov/november-2026-general-election/"},
        {"label": "Find your sample ballot", "url": "https://votehamiltoncountyohio.gov/sample-ballot/"},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://votehamiltoncountyohio.gov/results/"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, certified candidate list and certified questions and issues list; "
               "issue wording is from the Board's ballot issues document. Long charter amendments are condensed; the full wording is on the sample ballot.",
               NOTE_ORDER, NOTE_PLACES,
               "Issue 17 (City of Madeira, Sunday sales in precinct Madeira D) was withdrawn on September 24, 2026 and is not on the ballot. "
               "Local issue numbers start at 4: Issue 3 is the statewide question, and there are no Issues 1 or 2."]
    D = c.district; P = c.p; SD = c.sd

    c.contest("congress-1", "U.S. House", "Representative to Congress", [("Eric Conroy", "REP"), ("Greg Landsman", "DEM"), ("Nathan Weise", "LIB")], detail="1st District", places=D("cong", 1), src=C)
    c.contest("congress-8", "U.S. House", "Representative to Congress", [("Warren Davidson", "REP"), ("Vanessa Enoch", "DEM")], detail="8th District", places=D("cong", 8), src=C)
    c.contest("senate-7", "Ohio General Assembly", "State Senator", [("Zac Haines", "REP"), ("Cara Jacob", "DEM")], detail="7th District (Hamilton and Warren)", places=D("sen", 7), src=C)
    c.contest("senate-9", "Ohio General Assembly", "State Senator", [("Catherine Ingram", "DEM"), ("Linda D. Matthews", "REP")], detail="9th District", places=D("sen", 9), src=C)
    for n, cs in {24: [("Dani Isaacsohn", "DEM")], 25: [("Cecil Thomas", "DEM")], 26: [("Ashley Bryant Bailey", "DEM"), ("Tom Brinkman", "REP")],
                  27: [("Nancy Reed Aichholz", "REP"), ("Rachel Baker", "DEM")], 28: [("Karen Brownlee", "DEM"), ("Jill Cole", "REP")],
                  29: [("Cindy Abrams", "REP"), ("Jonathan R. Bradner", "DEM")], 30: [("Mike Odioso", "REP"), ("Caleb Price", "DEM")]}.items():
        c.contest(f"rep-{n}", "Ohio General Assembly", "State Representative", cs, detail=f"{n}th District", places=D("rep", n), src=C)
    c.contest("appeals-1-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Ginger S. Bock", "DEM")], detail="1st District · term commencing February 9, 2027", src=C)
    c.contest("commissioner", "County offices", "County Commissioner", [("Meeka Owens", "DEM"), ("Jonathan Pearson", "REP")], detail="Term commencing January 1, 2027", src=C)
    c.contest("auditor", "County offices", "County Auditor", [("Jessica E. Miranda", "DEM")], detail="Term commencing March 8, 2027", src=C)
    NP = " · no party label on the ballot"
    GEN = "Judge of the Court of Common Pleas, General Division"
    for id, div, when, cs in [
        ("cp-gen-0101", GEN, "Term commencing January 1, 2027", ["Katie Casch", "Donte Johnson"]),
        ("cp-gen-0102", GEN, "Term commencing January 2, 2027", ["Christian A. Jenkins", "Betsy Sundermann"]),
        ("cp-gen-0104", GEN, "Term commencing January 4, 2027", ["Chris Wagner"]),
        ("cp-gen-0209", GEN, "Term commencing February 9, 2027", ["Roger Bouchard", "Jennifer Branch"]),
        ("cp-gen-0210", GEN, "Term commencing February 10, 2027", ["Dennis Charles Mahoney", "Alan C. Triggs"]),
        ("cp-gen-0211", GEN, "Term commencing February 11, 2027", ["Robert A. Goering", "Latoya S. Maley"]),
        ("cp-gen-0212", GEN, "Term commencing February 12, 2027", ["Wende C. Cross"]),
        ("cp-gen-0213", GEN, "Term commencing February 13, 2027", ["Alison Hatheway"]),
        ("cp-gen-ute-0103", GEN, "Unexpired term ending January 3, 2029", ["Sarah Henry", "Chris McDowell"]),
        ("cp-gen-ute-0114", GEN, "Unexpired term ending January 14, 2029", ["Leah Dinkelacker", "Manisha Kotian"]),
        ("cp-drug", "Judge of the Court of Common Pleas, Drug Court Division", "Term commencing January 3, 2027", ["Nicole L. Sanders"]),
        ("cp-probate", "Judge of the Court of Common Pleas, Probate Division", "Term commencing February 9, 2027", ["Elizabeth A. Tye", "Ralph Winkler"]),
        ("cp-juvenile", "Judge of the Court of Common Pleas, Juvenile Division", "Term commencing February 14, 2027", ["Kari L. Bloom", "Susan Luken"]),
        ("cp-dr", "Judge of the Court of Common Pleas, Domestic Relations Division", "Term commencing July 1, 2027", ["Tiffany Evans"]),
    ]:
        c.contest(id, "Court of Common Pleas", div, cs, detail=when + NP, src=C)

    N = lambda n: f"Issue {n}"
    est = lambda total, per: f"{total} a year; {per} for each $100,000 of the county auditor's market value"

    # School districts
    c.levy("issue-4", "Cincinnati City School District (Cincinnati Public Schools)", SD("CINCINNATI PUBLIC SCHOOLS CITY SD"), "Additional", "Current expenses.", "7 mills",
           "5 years, commencing in 2026", "2027", est("$66,336,723", "$245"), number=N(4), src=I)
    inc = lambda n, sd, raw, rate, term: c.issue(f"issue-{n}", "question", sd, f"School district income tax: {rate}, {term}", SD(raw), number=N(n), src=I,
        text=f"Shall an annual income tax of {rate} on the earned income of individuals residing in the school district be imposed by the {sd}, "
             f"{'for 5 years' if term == '5 years' else 'for a continuing period of time'}, beginning January 1, 2027, for the purpose of current expenses?")
    inc(5, "North College Hill City School District", "NORTH COLLEGE HILL CITY SD", "1.25 percent", "5 years")
    inc(6, "Northwest Local School District (Hamilton and Butler)", "NORTHWEST LOCAL SD (HAMILTON)", "1.5 percent", "continuing")
    inc(7, "Southwest Local School District (Hamilton and Butler)", "SOUTHWEST LOCAL SD (HAMILTON)", "0.25 percent", "continuing")
    c.levy("issue-8", "Sycamore Community City School District", SD("SYCAMORE COMMUNITY CITY SD"), "Additional", "Current expenses and permanent improvements.", "6.95 mills",
           "Continuing period of time, commencing in 2026", "2027", est("$17,993,971", "$243"), number=N(8), src=I)
    c.levy("issue-9", "Winton Woods City School District", SD("WINTON WOODS CITY SD"), "Additional", "Current expenses.", "6.95 mills",
           "Continuing period of time, commencing in 2026", "2027", est("$5,346,642", "$243"), number=N(9), src=I)

    # County
    c.levy("issue-10", "Hamilton County", "county", "Renewal and increase", "Support for children's services and care and placement of children (renewal of 4.51 mills and increase of 1.1 mill).",
           "5.61 mills", "4 years, commencing in 2026", "2027", est("$116,888,718", "$121"), number=N(10), src=I)

    # Cities and villages: levies
    L = [
        (11, "City of Cheviot", ["CHEVIOT CITY"], "Renewal", "Current expenses.", "3 mills", "5 years, commencing in 2026", "2027", "$158,674", "$18"),
        (13, "City of Deer Park", ["DEER PARK CITY"], "Renewal", "Current expenses.", "6.9 mills", "5 years, commencing in 2027", "2028", "$760,420", "$130"),
        (14, "City of Forest Park", ["FOREST PARK CITY"], "Additional", "Fire protection and emergency medical services.", "3.9 mills", "Continuing period of time, commencing in 2026", "2027", "$2,030,169", "$137"),
        (18, "City of Norwood", ["NORWOOD CITY"], "Renewal", "Current operating expenses.", "8 mills", "5 years, commencing in 2027", "2028", "$1,642,311", "$47"),
        (20, "Village of Addyston", ["ADDYSTON VILLAGE"], "Additional", "Improving, maintaining and operating the water supply system.", "1 mill", "5 years, commencing in 2026", "2027", "$18,592", "$35"),
        (21, "Village of Fairfax", ["FAIRFAX VILLAGE"], "Renewal", "Current expenses.", "0.96 mill", "5 years, commencing in 2026", "2027", "$63,093", "$19"),
        (22, "Village of Glendale", ["GLENDALE VILLAGE"], "Renewal", "Current expenses.", "8.5 mills", "4 years, commencing in 2026", "2027", "$890,978", "$195"),
        (23, "Village of Glendale", ["GLENDALE VILLAGE"], "Renewal", "Current expenses.", "2.5 mills", "4 years, commencing in 2026", "2027", "$284,716", "$72"),
        (24, "Village of Golf Manor", ["GOLF MANOR VILLAGE"], "Renewal", "Streets and roads.", "8 mills", "10 years, commencing in 2026", "2027", "$344,919", "$126"),
        (25, "Village of Golf Manor", ["GOLF MANOR VILLAGE"], "Renewal", "Current expenses.", "2 mills", "5 years, commencing in 2026", "2027", "$86,230", "$31"),
        (26, "Village of Greenhills", ["GREENHILLS VILLAGE"], "Renewal", "Current operating expenses.", "3.28 mills", "5 years, commencing in 2026", "2027", "$68,736", "$18"),
        (27, "Village of Lockland", ["LOCKLAND VILLAGE"], "Additional", "Providing and maintaining fire and emergency medical services.", "8 mills", "Continuing period of time, commencing in 2026", "2027", "$601,165", "$280"),
        (28, "Village of Mariemont", ["MARIEMONT VILLAGE"], "Renewal", "Permanent improvements: street repairs, curbs, sidewalks and storm sewers, tree maintenance, parks, erosion control, and equipment and facilities for the Police, Fire, Maintenance and Administrative departments.",
         "3.5 mills", "5 years, commencing in 2027", "2028", "$310,981", "$40"),
        (29, "Village of North Bend", ["NORTH BEND VILLAGE"], "Renewal", "Current operating expenses.", "5 mills", "5 years, commencing in 2026", "2027", "$218,098", "$151"),
        (31, "Village of Terrace Park", ["TERRACE PARK VILLAGE"], "Renewal", "Current expenses.", "5.58 mills", "5 years, commencing in 2026", "2027", "$713,193", "$123"),
        (33, "Miami Township", ["MIAMI TWP.", "ADDYSTON VILLAGE", "CLEVES VILLAGE", "NORTH BEND VILLAGE"], "Renewal", "Current expenses.", "0.46 mill", "5 years, commencing in 2026", "2027", "$181,286", "$10"),
    ]
    for n, jur, raws, t, purpose, mills, term, fd, total, per in L:
        area = "Miami Township, including the villages of Addyston, Cleves and North Bend" if n == 33 else None
        c.levy(f"issue-{n}", jur, P(*raws), t, purpose, mills, term, fd, est(total, per), number=N(n), area=area, src=I)

    # Charter amendments
    c.issue("issue-15", "question", "City of Harrison", "Charter amendment (as reported by City Council)", P("HARRISON CITY"), number=N(15),
            text="Shall the proposed charter amendment as reported by the city council of the City of Harrison be adopted?", src=I)
    c.issue("issue-16", "question", "City of Madeira", "Charter amendment: modernizing the Charter (Articles II–VIII, X–XIV, XVI and XVII)", P("MADEIRA CITY"), number=N(16),
            text="Amend fourteen articles of the Charter to: modernize terminology and gender references and add continuity and severability provisions; allow electronic notice of special Council meetings while raising minimum notice from 24 to 48 hours; "
                 "clarify Council vacancy language; let Council appoint a qualified person to perform the Manager's duties during an extended absence; eliminate the Charter-created Treasurer office, with the Manager authorizing expenditure warrants; "
                 "have Council and the Manager agree each year on a threshold above which contracts and purchases need Council approval, and revise contract notice and bid provisions; revise the Planning Commission's authority and duties and let it and the Board of Zoning Appeals skip meetings when there is no business; "
                 "and replace the Charter's automatic protection of the Hosbrook House, Muchmore House and Railroad Depot with protection only for properties on the National Register of Historic Places or designated historic by City ordinance.", src=I)
    c.issue("issue-19", "question", "City of Wyoming", "Charter amendment: Charter Review Commission recommendations", P("WYOMING CITY"), number=N(19),
            text="Rename the City Treasurer the Finance Director (Section 5.02); retitle Article VI \"Commissions and Boards\"; eliminate the Civil Service Commission sections (6.01, 6.02); "
                 "drop the \"for cause\" requirement for removing board and commission appointees and move that section (11.03) and the virtual-meetings section (11.08) to Article VI; "
                 "add a new Section 6.03 on establishing other commissions and boards; clarify that all City elections are non-partisan (Section 8.01); and make the oath of office gender neutral (Section 11.07).", src=I)
    c.issue("issue-30", "question", "Village of St. Bernard", "Charter amendment: village administration (Articles IV and V)", P(*ST_BERNARD), number=N(30),
            text="Amend Sections 4.01–4.06 and 5.01 to: merge the Safety Director and Service Director into a single Municipal Administrator, selected by the Mayor with Council approval and removable by Council, who heads the police and fire departments; "
                 "merge the elected Auditor and Treasurer into an appointed Finance Director; convert the elected Law Director to an engaged position; retitle the Tax Commissioner as Tax Administrator under the Finance Director; "
                 "and replace the Director of Public Safety and Service on the five-member Planning Commission with a Council member.", src=I)

    # Local liquor options
    LQ = [
        (12, "City of Cincinnati", "CINCINNATI CITY", "Cincinnati 9-D", "ETC Produce Walnut Hills (Sunday)",
         "Shall the sale of wine and mixed beverages be permitted for sale on Sunday by ETC Produce Walnut Hills, L.L.C. a holder of a D-6 liquor permit who is engaged in the business of operating a grocery store at 954 McMillan Street, Cincinnati, Ohio 45206 in this precinct?"),
        (32, "Village of Terrace Park", "TERRACE PARK VILLAGE", "Terrace Park A", "Two Maries (Sunday)",
         "Shall the sale of wine and mixed beverages, and spirituous liquor be permitted for sale on Sunday by Two Maries, LLC an applicant for a D-6 liquor permit who is engaged in the business of operating a bar and restaurant at 704 Wooster Pike, Terrace Park, Ohio 45174 in this precinct?"),
        (34, "Springfield Township", "SPRINGFIELD TWP.", "Springfield C", "Sundy's (Sunday)",
         "Shall the sale of wine and mixed beverages be permitted for sale on Sunday by Sunderman Entertainment Group, Inc. dba Sundy's an applicant for a D-6 liquor permit who is engaged in the business of operating a bar and restaurant at 8603 Winton Road, Cincinnati, Ohio 45231 in this precinct?"),
    ]
    for n, jur, raw, pct, biz, text in LQ:
        c.issue(f"issue-{n}", "liquor", jur, f"Local liquor option: {biz}", P(raw), number=N(n), area=f"Precinct {pct}", text=text, src=I)
    c.issues.sort(key=lambda q: int(q["id"].split("-")[1]))
    return c
