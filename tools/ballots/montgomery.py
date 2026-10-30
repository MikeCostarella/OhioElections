from lib import County, NOTE_ORDER, NOTE_PLACES

NOTICE = "https://www.montgomery.boe.ohio.gov/wp-content/uploads/2021/01/46-Day-FWAB-11.3.2026-General-Election-1.pdf"
ISSUES = "https://www.montgomery.boe.ohio.gov/wp-content/uploads/2021/02/9.11.2026-Issues-List.pdf"
CAND = "https://www.montgomery.boe.ohio.gov/wp-content/uploads/2023/10/10.16.2026-Candidate-Petition-Report.pdf"

def build():
    c = County("montgomery", "Montgomery", "39113")
    c.src("montgomery-46day", "Montgomery County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election", NOTICE)
    c.src("montgomery-cand", "Montgomery County Board of Elections: 2026 candidate report (October 16, 2026)", CAND)
    c.src("montgomery-issues", "Montgomery County Board of Elections: November 3, 2026 ballot issues list (September 11, 2026)", ISSUES)
    S = ["montgomery-46day"]; C = ["montgomery-46day", "montgomery-cand"]; I = ["montgomery-46day", "montgomery-issues"]
    c.links = [
        {"label": "Board of Elections", "url": "https://www.montgomery.boe.ohio.gov/"},
        {"label": "Current election", "url": "https://www.montgomery.boe.ohio.gov/current-election/"},
        {"label": "Sample ballots by precinct", "url": "https://lookup.boe.ohio.gov/vtrapp/montgomery/ballotlist.aspx"},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://www.montgomery.boe.ohio.gov/election-results/"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it, "
               "checked against the Board's candidate report and ballot issues list. Issue wording is the Board's summary; the full wording is on the sample ballot.",
               NOTE_ORDER, NOTE_PLACES]
    P = c.p; D = c.district; SD = c.sd

    c.contest("congress-10", "U.S. House", "Representative to Congress", [("Kristina Knickerbocker", "DEM"), ("Thomas F. McMasters", "LIB"), ("Mike Turner", "REP")], detail="10th District", src=C)
    c.contest("senate-5", "Ohio General Assembly", "State Senator", [("Jeffrey Harris", "DEM"), ("Phil Plummer", "REP")], detail="5th District", places=D("sen", 5), src=C)
    for n, sfx, cs in [
        (36, "th", [("Chuck Horn", "Non-party"), ("Rose Lounsbury", "DEM"), ("Andrea White", "REP")]),
        (37, "th", [("Tom Herner", "DEM"), ("Tom Young", "REP")]),
        (38, "th", [("Desiree Tims", "DEM")]),
        (39, "th", [("Mark Campbell", "REP"), ("Daquan Neal", "DEM")]),
        (40, "th", [("Rodney Creech", "REP"), ("Timothy B. Hornbacker", "DEM"), ("Joshua A. Umbaugh", "LIB")]),
    ]:
        c.contest(f"rep-{n}", "Ohio General Assembly", "State Representative", cs, detail=f"{n}{sfx} District", places=D("rep", n), src=C)
    c.contest("appeals-2-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Chris Epley", "REP")], detail="2nd District · term commencing February 9, 2027", src=C)
    c.contest("commissioner", "County offices", "County Commissioner", [("Margie Christie", "REP"), ("Carolyn Rice", "DEM")], detail="Term commencing January 1, 2027", src=C)
    c.contest("auditor", "County offices", "County Auditor", [("Karl Keith", "DEM"), ("Tammy L. Murphy", "REP")], src=C)
    NP = " · no party label on the ballot"
    for id, office, date, cs in [
        ("cp-0101", "General Division", "Term commencing January 1, 2027", ["Susan D. Solle"]),
        ("cp-0102", "General Division", "Term commencing January 2, 2027", ["Anne Keeton", "Derek Muncy"]),
        ("cp-0103", "General Division", "Term commencing January 3, 2027", ["Michele S.H. Henne", "Kelly D. Madzey"]),
        ("cp-0701", "General Division", "Term commencing July 1, 2027", ["Steve Abshire", "Richard Glennon"]),
        ("cp-0702", "General Division", "Term commencing July 2, 2027", ["Elizabeth A. Ellis"]),
        ("cp-probate", "Probate Division", "Term commencing February 9, 2027", ["David Brannon", "Cassandra A. Rice"]),
        ("cp-juvenile", "Juvenile Division", "Unexpired term ending December 31, 2028", ["Hope L. Smalls", "Nicholas Sylvain"]),
    ]:
        c.contest(id, "Court of Common Pleas", f"Judge of the Court of Common Pleas, {office}", cs, detail=date + NP, src=C)
    NL = P("NEW LEBANON VILLAGE")
    c.contest("new-lebanon-council", "Municipal offices", "New Lebanon Village Council", ["Nicole Adkins", "Rob Dennis"], detail="Unexpired term ending December 31, 2029 · vote for 1",
              places=NL, area="New Lebanon Village (Jackson-New Lebanon A–B, Perry-New Lebanon)", src=C)

    N = lambda n: f"Issue {n}"
    c.levy("issue-4", "Dayton City School District", SD("DAYTON CITY SD"), "Additional", "Current operating expenses (5 mills) and general permanent improvements (2 mills).", "7 mills", "Continuing period of time, commencing in 2026", "2027",
           number=N(4), area="Dayton City School District", src=I)
    c.issue("issue-5", "question", "Miamisburg City School District", "School district income tax: 0.5%, continuing, for current expenses", SD("MIAMISBURG CITY SD") + P("WEST CARROLLTON CITY"), number=N(5),
            area="Miamisburg City School District (German Township A–B splits, Miamisburg, Miami Township parts, West Carrollton A split 3)",
            text="Income tax of 0.50% on the school district income of individuals, for a continuing period of time, commencing January 1, 2027, for current expenses.", src=I)
    c.levy("issue-6", "Oakwood City School District", SD("OAKWOOD CITY SD"), "Renewal", "General permanent improvements.", "1.8 mills", "Continuing period of time, commencing in 2027", "2028", number=N(6), area="Oakwood City School District", src=I)
    c.levy("issue-7", "Northridge Local School District", SD("NORTHRIDGE LOCAL SD (MONTG)"), "Additional", "General permanent improvements.", "2.2 mills", "Continuing period of time, commencing in 2026", "2027", number=N(7), area="Northridge Local School District", src=I)
    BV = P("BROOKVILLE CITY")
    for n, secs in [(8, "the Preamble and parts of Sections 1, 2 and 3"), (9, "parts of Sections 4, 5 and 6"), (10, "parts of Sections 7, 8, 9 and 12"), (11, "parts of Sections 10 and 11")]:
        title = "Charter amendment: " + secs[0].upper() + secs[1:]
        c.issue(f"issue-{n}", "question", "City of Brookville", title, BV, number=N(n), text=f"Amend {secs} of the Brookville City Charter.", src=I)
    c.issue("issue-12", "liquor", "City of Dayton", "Local liquor option: Shamrock Athletic Club (Sunday)", P("DAYTON CITY"), number=N(12), area="Dayton precinct 12-C",
            text="Local option (5-R, question 2): Sunday sale of beer, wine and mixed beverages, and spirituous liquor by Shamrock Athletic Club, 820 Linden Ave., Dayton.", src=I)
    c.issue("issue-13", "liquor", "City of Dayton", "Local liquor option: University of Dayton (Sunday)", P("DAYTON CITY"), number=N(13), area="Dayton precinct 13-A",
            text="Local option (5-R, question 2): Sunday sale of wine and mixed beverages, and spirituous liquor by the University of Dayton, 1801 Edwin C. Moses Boulevard S., Dayton.", src=I)
    c.issue("issue-14", "liquor", "City of Huber Heights", "Local liquor option: Villa Tavern (Sunday)", P("HUBER HEIGHTS CITY"), number=N(14), area="Huber Heights precinct 1-D",
            text="Local option (5-R, question 2): Sunday sale of wine and mixed beverages, and spirituous liquor by CWA Management, L.L.C., dba Villa Tavern, 6303 Rip Rap Road, Huber Heights.", src=I)
    KT = P("KETTERING CITY")
    for n, title, text in [
        (15, "Charter amendment: Sections 7-3 and 7-5 (appeals to Council)", "Amend Section 7-3, Appeals from the Planning Commission to Council, and Section 7-5, Appeals from the Board of Zoning Appeals to Council."),
        (16, "Charter amendment: gender-neutral wording", "Amend Sections 3-2, 3-3, 3-6, 3-8, 5-1, 5-2, 5-3, 5-4, 5-5, 5-6, 5-7, 8-3 and 8-4 to change the use of gender-specific pronouns to the corresponding nouns."),
        (17, "Charter amendment: Section 4-3 (procedure of passage of ordinances)", "Amend Section 4-3, Procedure of Passage of Ordinances."),
        (18, "Charter amendment: Section 7-2 (powers and duties)", "Amend Section 7-2, Powers and Duties."),
        (19, "Charter amendment: Sections 5-2 and 6-2 (the Manager; department directors)", "Amend Article V, Section 5-2, The Manager, and Article VI, Section 6-2, Department Directors."),
    ]:
        c.issue(f"issue-{n}", "question", "City of Kettering", title, KT, number=N(n), text=text, src=I)
    c.levy("issue-20", "City of Oakwood", P("OAKWOOD CITY"), "Renewal", "Current expenses.", "2.72 mills", "5 years, commencing in 2026", "2027", number=N(20), src=I)
    c.issue("issue-21", "question", "City of Union", "Municipal income tax: additional 1% for police and fire department operations", P("UNION CITY"), number=N(21),
            text="Additional 1% increase in the municipal income tax, for a continuing period of time, commencing January 1, 2027, for police and fire department operations.", src=I)
    c.issue("issue-22", "liquor", "Village of New Lebanon", "Local liquor option: American Legion Post 762", NL, number=N(22), area="New Lebanon precinct PNLB (Perry-New Lebanon)",
            text="Local option (5-R, question 1): sale of beer, wine and mixed beverages, and spirituous liquor by AL Post 762, 519 E. Main St., New Lebanon.", src=I)
    c.levy("issue-23", "German Township (incorporated and unincorporated)", P("GERMAN TOWNSHIP", "GERMANTOWN CITY"), "Renewal", "Providing or maintaining senior citizens services or facilities.", "1 mill", "5 years, commencing in 2027", "2028",
           number=N(23), area="German Township A–B and Germantown A–D", src=I)
    c.levy("issue-24", "Jackson Township (unincorporated area and the Village of Farmersville)", P("JACKSON TOWNSHIP", "FARMERSVILLE VILLAGE", "NEW LEBANON VILLAGE"), "Additional", "Parks and recreational purposes.", "2 mills", "10 years, commencing in 2026", "2027",
           number=N(24), area="Farmersville, Jackson Township A–B, Jackson-New Lebanon A (split 2)", src=I)
    c.levy("issue-25", "Jefferson Township", P("JEFFERSON TOWNSHIP", "DAYTON CITY"), "Additional", "Current expenses.", "3 mills", "5 years, commencing in 2026", "2027",
           number=N(25), area="Jefferson Township A–D, plus Dayton 14-A (split 3) and 14-C (split 3)", src=I)
    return c
