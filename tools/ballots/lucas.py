from lib import County, NOTE_ORDER, NOTE_PLACES, NOTE_UNKNOWN

SITE = "https://www.lucascountyohiovotes.gov/"
CURRENT = "https://www.lucascountyohiovotes.gov/current_election/index.php"
NOTICE = "https://drive.google.com/file/d/1p6mXWYthggS-LEMaEOuhdFVna2iDQrGf/view"
CAND = "https://drive.google.com/file/d/1hAKSNgQ7n_OD7Rf0KVVMQRVwustgovgx/view"
ISSUES = "https://drive.google.com/file/d/1Zc8AM6pH3XAK8OpRk98Q7x2mre3dcoEU/view"


def build():
    # The SoS file splits Washington and Waterville townships by precinct and lists Springfield as "unincorporated".
    rename = {
        "PRECINCT WASHINGTON 1": "Washington Township", "PRECINCT WASHINGTON 2": "Washington Township",
        "PRECINCT WATERVILLE TOWNSHIP A": "Waterville Township", "PRECINCT WATERVILLE TOWNSHIP B": "Waterville Township",
        "SPRINGFIELD UNINCORP": "Springfield Township",
    }
    c = County("lucas", "Lucas", "39095", rename=rename)
    c.src("lucas-46day", "Lucas County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election (revised 9/17/2026)", NOTICE)
    c.src("lucas-cand", "Lucas County Board of Elections: candidates list, November 3, 2026 General Election (9/11/2026)", CAND)
    c.src("lucas-issues", "Lucas County Board of Elections: issue list report, November 3, 2026 General Election (9/22/2026)", ISSUES)
    C = ["lucas-46day", "lucas-cand"]; I = ["lucas-46day", "lucas-issues"]
    c.links = [
        {"label": "Board of Elections", "url": SITE},
        {"label": "Current election", "url": CURRENT},
        {"label": "Am I registered? / Sample ballot / Polling place", "url": "https://www.lucascountyohiovotes.gov/vtrapp/lucas/vtrlookup.aspx"},
    ]
    c.results_links = [{"label": "Board of Elections: historic election results", "url": "https://www.lucascountyohiovotes.gov/historic_election_results/index.php"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it, "
               "checked against the Board's candidates list and issue list. Issue wording is the notice's summary; the full wording is on the sample ballot.",
               NOTE_ORDER, NOTE_PLACES, NOTE_UNKNOWN,
               "Local issue numbers start at 4: Issue 3 is the statewide question, and there are no Issues 1 or 2."]
    D = c.district; P = c.p; SD = c.sd

    c.contest("congress-9", "U.S. House", "Representative to Congress", [("Marcy Kaptur", "DEM"), ("Derek Merrin", "REP")], detail="9th District", src=C)
    c.contest("senate-11", "Ohio General Assembly", "State Senator", [("Paula Hicks-Hudson", "DEM"), ("Kenneth W. Sharp", "LIB"), ("James Nowak", "REP")],
              detail="11th District", places=D("sen", 11), src=C)
    for n, cs in {41: [("Erika White", "DEM"), ("Ian Chamberlin", "REP")],
                  42: [("Elgin Rogers Jr.", "DEM"), ("Robert McMahon", "REP")],
                  43: [("Michele Grim", "DEM"), ("Zach Hall", "LIB"), ("David Karmol", "REP")],
                  44: [("David J. Fournier", "DEM"), ("Edward L. Schimmel", "REP"), ("Lyndsey A. Stough", "Non-party")]}.items():
        c.contest(f"rep-{n}", "Ohio General Assembly", "State Representative", cs, detail=f"{n}{'st' if n == 41 else 'nd' if n == 42 else 'rd' if n == 43 else 'th'} District", places=D("rep", n), src=C)
    c.contest("appeals-6-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Michael R. Goulding", "REP")], detail="6th District · full term commencing February 9, 2027", src=C)
    c.contest("appeals-6-0210", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Myron C. Duhart", "DEM"), ("CJ Kamm", "REP")], detail="6th District · full term commencing February 10, 2027", src=C)
    c.contest("commissioner", "County offices", "County Commissioner", [("Lisa A. Sobecki", "DEM"), ("Brenden Johnson", "LIB"), ("Laura Brown", "REP")], detail="Full term commencing January 1, 2027", src=C)
    c.contest("auditor", "County offices", "County Auditor", [("Katie Moline", "DEM"), ("Carolyn Munn", "REP")], detail="Full term commencing March 8, 2027", src=C)
    NP = " · no party label on the ballot"
    c.contest("cp-gen", "Court of Common Pleas", "Judge of the Court of Common Pleas", ["Ian B. English"], detail="Full term commencing February 9, 2027" + NP, src=C)
    c.contest("cp-dr", "Court of Common Pleas", "Judge of the Court of Common Pleas, Domestic Relations Division", ["Nedal Adya", "Lisa D. McGowan"], detail="Full term commencing January 1, 2027" + NP, src=C)
    c.contest("cp-juv", "Court of Common Pleas", "Judge of the Court of Common Pleas, Juvenile Division", ["Amy E. Stoner"], detail="Full term commencing January 2, 2027" + NP, src=C)
    c.contest("cp-probate", "Court of Common Pleas", "Judge of the Court of Common Pleas, Probate Division", ["Jaime Agnew", "Tom Puffenberger"], detail="Full term commencing February 9, 2027" + NP, src=C)
    c.contest("maumee-council", "Municipal offices", "Maumee City Council", ["Philip A. Leinbach", "John A. Scott"], detail="Unexpired term ending December 31, 2029 · 1 to be elected",
              places=P("MAUMEE CITY"), area="Maumee City", src=C)

    N = lambda n: f"Issue {n}"
    c.issue("issue-4", "question", "Evergreen Local School District (Fulton and Lucas)", "School district income tax: 0.25% renewal, 5 years", SD("EVERGREEN LOCAL SD (FULTON)") + P("HARDING TOWNSHIP"), number=N(4),  # notice lists Harding 1 split 1; the voter file has no Harding voters in the district
            area="Precincts Harding 1 (split 1), Richfield 1, Spencer 1 (split 1), Sylvania P (split 1)",
            text="Renewal of an annual income tax of 0.25% supporting the current expenses of the Evergreen Local School District, for 5 years, commencing January 1, 2028.", src=I)
    c.issue("issue-5", "question", "Maumee City School District", "School district income tax: 1.25% additional, continuing", SD("MAUMEE CITY SD"), number=N(5),
            text="Shall an annual income tax of 1.25% on the earned income of individuals residing in the school district be imposed by the Maumee City School District, for a continuing period of time, beginning January 1, 2027, for the purpose of current expenses?", src=I)
    c.issue("issue-6", "question", "Springfield Local School District", "School district income tax: 0.50% additional, 5 years", SD("SPRINGFIELD LOCAL SD (LUCAS)"), number=N(6),
            text="Shall an annual income tax of one-half per centum (0.50%) on the earned income of individuals residing in the School District be imposed by the Springfield Local School District, for a five (5) year period of time, beginning January 1, 2027, for the purpose of current expenses?", src=I)
    c.issue("issue-7", "question", "Sylvania City School District", "School district income tax (1% additional, continuing) and property tax reduction (4.9 mills to 3.2 mills)", SD("SYLVANIA CITY SD"), number=N(7),
            text="An additional annual income tax of 1% for a continuing period of time, commencing January 1, 2027, for current expenses, together with a reduction of a property tax levy for current expenses from 4.9 mills to 3.2 mills (a reduction of 1.7 mills).", src=I)
    LIB_PLACES = sorted(set(c.places) - {"Swanton Village"})
    c.levy("issue-8", "Toledo-Lucas County Public Library", LIB_PLACES, "Additional", "Current expenses.", "3 mills", "5 years, commencing in 2026", "2027", number=N(8),
           area="All of Lucas County except precincts Harding 1 (split 2), Spencer 1 (split 3) and Swanton 1", src=I)
    c.levy("issue-9", "Toledo City School District", SD("TOLEDO CITY SD") + P("HARDING TOWNSHIP", "OTTAWA HILLS VILLAGE"), "Additional", "Current expenses.", "6.9 mills", "5 years, commencing in 2026", "2027", number=N(9), src=I)
    c.levy("issue-10", "Swanton Public Library (Fulton and Lucas)", None, "Renewal", "Current expenses of the Swanton Public Library.", "1 mill", "5 years, commencing in 2026", "2027", number=N(10),
           area="Precincts Harding 1 (split 2), Spencer 1 (split 3), Swanton 1", src=I)
    c.issue("issue-11", "liquor", "Springfield Township", "Local liquor option: QuikTrip, 6340 Dorr St.", P("SPRINGFIELD UNINCORP"), number=N(11), area="Springfield Township precinct 3",
            text="Sale of wine and mixed beverages by QuikTrip, 6340 Dorr St., Toledo, OH 43615, in this precinct. (The Board's issue list describes it as a Sunday-sales option for QT #7100.)", src=I)
    c.issue("issue-12", "liquor", "City of Waterville", "Local liquor option: Buffalo Wild Wings (Sunday)", P("WATERVILLE CITY"), number=N(12), area="Waterville City precinct 2",
            text="Sunday sale of wine and mixed beverages and spirituous liquor (on-premise, off-premise or on/off-premise sales) by Buffalo Wild Wings, 770 Pray Blvd., Waterville, OH 43566, in this precinct.", src=I)
    c.levy("issue-13", "Lucas County", "county", "Renewal", "Operation and maintenance of the Imagination Station.", "0.17 mill", "5 years, commencing in 2027", "2028", number=N(13), src=I)
    c.issue("issue-14", "question", "City of Sylvania", "Initiative ordinance: Sylvania Resource Conservation and Equal Access Ordinance", P("SYLVANIA CITY"), number=N(14),
            text="Shall the proposed ordinance limiting the use of City resources to assist federal immigration enforcement, except to the extent required by federal or state law, and assuring equal access to all persons to City services, benefits, programs and protections regardless of their immigration status, be adopted?", src=I)
    OR = P("OREGON CITY")
    ORA = "Oregon City (all precincts except Oregon 1 split 1)"
    c.levy("issue-15", "City of Oregon", OR, "Additional", "Providing or maintaining senior citizens services or facilities.", "0.5 mill", "5 years, commencing in 2026", "2027",
           "$375,943 a year; $18 for each $100,000 of market value", number=N(15), area=ORA, src=I)
    TO = P("TOLEDO CITY")
    c.issue("issue-16", "question", "City of Toledo", "Municipal income tax: 0.25% additional, temporary (2027–2030)", TO, number=N(16),
            text="Shall Ordinance (Ordinance No. 301-26) providing for a new temporary one-quarter percent (1/4%) City of Toledo levy on income for the period commencing on January 1, 2027, and ending December 31, 2030, which shall be in addition to the city of Toledo's other levies on income, for the purpose of allocating the levy proceeds to the General Fund to be dedicated to neighborhood safety expenditures, and to police and fire safety force operations, including criminal gang disruption, be passed?", src=I)
    for n, sec, ordn in [(17, "Chapter I, Section 6; Chapter IV, Section 33; Chapter VIII, Section 171", "302-26"),
                         (18, "Chapter III, Sections 14 and 17; Chapter IV, Section 83; Chapter VI, Section 92", "304-26"),
                         (19, "Chapter I, Section 5", "305-26")]:
        c.issue(f"issue-{n}", "question", "City of Toledo", f"Charter amendment: {sec}", TO, number=N(n),
                text=f"To amend {sec} of the City of Toledo charter (Ordinance {ordn}).", src=I)
    MA = P("MAUMEE CITY")
    for n, sec, text in [
        (20, "Article VIII, Sections 2 and 3 (nominations and primaries)", "To amend Article VIII, Sections 2 and 3 of the Charter of the City of Maumee regarding nominating petitions, candidate statements of candidacy, and the scheduling and requirements for non-partisan primary elections."),
        (21, "Article XIII, Section 5 (military service and absences)", "To amend Article XIII, Section 5 of the Charter of the City of Maumee regarding elected officials' retention of office during military service and temporary appointments during absences exceeding ninety (90) days."),
        (22, "Article IX, Section 3 (recall)", "To amend Article IX, Section 3 of the Charter of the City of Maumee regarding the recall of elected officials, including petition requirements, recall election procedures, and the nomination and election of successors."),
    ]:
        c.issue(f"issue-{n}", "question", "City of Maumee", f"Charter amendment: {sec}", MA, number=N(n), text=text, src=I)
    BK = P("BERKEY VILLAGE")
    c.levy("issue-23", "Village of Berkey", BK, "Renewal", "911 operating expenses.", "3 mills", "5 years, commencing in 2027", "2028", number=N(23), area="Precinct Richfield 1 (split 1)", src=I)
    c.levy("issue-24", "Village of Berkey", BK, "Renewal", "Operating expenses of the Village.", "3 mills", "5 years, commencing in 2027", "2028", number=N(24), area="Precinct Richfield 1 (split 1)", src=I)
    for n, sec, text in [
        (25, "Article XIII, Section 8 (data centers)", "Proposed charter amendment to Article XIII, Section 8: the construction of a data center is hereby prohibited."),
        (26, "Article VIII, Section 2", "Proposed amendment to Article VIII, Section 2 of the Charter of the City of Oregon."),
        (27, "Article VIII, Section 3 (nominating procedures)", "Proposed amendment to Article VIII, Section 3 of the Charter of the City of Oregon: nominating procedures for the City of Oregon."),
    ]:
        c.issue(f"issue-{n}", "question", "City of Oregon", f"Charter amendment: {sec}", OR, number=N(n), area=ORA, text=text, src=I)
    c.levy("issue-28", "Springfield Township", P("SPRINGFIELD UNINCORP", "HOLLAND VILLAGE"), "Renewal",
           "Fire protection, fire apparatus, equipment, buildings, water supply and fire-alarm communications, fire-fighting personnel, and ambulance and emergency medical services.",
           "1.8 mills", "5 years, commencing in 2026", "2027", number=N(28), area="Springfield Township precincts 1–18 (including Holland Village voters)", src=I)
    c.levy("issue-29", "Washington Township", P("PRECINCT WASHINGTON 1", "PRECINCT WASHINGTON 2"), "Additional", "Police funding.", "3.25 mills", "Continuing period of time, commencing in 2026", "2027",
           "$202,382 a year; $114 for each $100,000 of market value", number=N(29), src=I)
    c.issue("issue-30", "question", "Monclova Township", "Limited home rule government (ORC 504.01)", P("MONCLOVA TOWNSHIP"), number=N(30),
            text="Resolution of the Board of Trustees of Monclova Township to adopt limited home rule government.", src=I)
    return c
