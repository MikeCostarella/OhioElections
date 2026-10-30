from lib import County, NOTE_ORDER, NOTE_PLACES

SITE = "https://www.boe.ohio.gov/athens/"
NOTICE = "https://www.boe.ohio.gov/athens/c/upload/FWAB_11November46Day.pdf"
ISSUE_NOTICES = "https://www.boe.ohio.gov/athens/c/pdfs/NoticeOfElection26General.pdf"


def build():
    # Raw SoS names ("TRIMBLE TOWNSHIP", "TRIMBLE VILLAGE", "ATHENS CITY") already display correctly; no renames needed.
    c = County("athens", "Athens", "39009")
    c.src("athens-46day", "Athens County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election (revised October 22, 2026)", NOTICE)
    c.src("athens-notices", "Athens County Board of Elections: notices of election on local questions and issues, November 3, 2026 General Election (dated October 15, 2026)", ISSUE_NOTICES)
    C = ["athens-46day"]; I = ["athens-notices", "athens-46day"]
    c.links = [
        {"label": "Board of Elections", "url": SITE},
        {"label": "Candidates and Issues", "url": "https://www.boe.ohio.gov/athens/election-info/candidates-and-issues/"},
        {"label": "Sample ballots by precinct", "url": "https://lookup.boe.ohio.gov/vtrapp/athens/ballotlist.aspx"},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://www.boe.ohio.gov/athens/election-info/election-results/"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it; "
               "issue wording is from the Board's notices of election on each local question and issue.",
               NOTE_ORDER, NOTE_PLACES,
               "Local issue numbers are 1, 2 and 4 to 29: Issue 3 is the statewide question.",
               "Issues 23 and 24 (Lee Township fire protection) are two separate renewals with the same wording, rate and term in the Board's notices."]
    P = c.p; D = c.district; SD = c.sd
    N = lambda n: f"Issue {n}"
    est = lambda total, per: f"{total} a year; {per} for each $100,000 of the county auditor's market value"

    # --- Federal, state legislative, appeals (all precincts are in the 2nd Congressional and 4th Appeals districts; no State Senate race) ---
    c.contest("congress-2", "U.S. House", "Representative to Congress", [("Jen Mazzuckelli", "DEM"), ("David J. Taylor", "REP")],
              detail="2nd District", places=D("cong", 2), src=C)
    c.contest("rep-94", "Ohio General Assembly", "State Representative", [("Kevin Ritter", "REP"), ("Wenda Sheard", "DEM")],
              detail="94th District", places=D("rep", 94), src=C)
    c.contest("rep-95", "Ohio General Assembly", "State Representative", [("Paul Cameron", "DEM"), ("Ty Moore", "REP")],
              detail="95th District", places=D("rep", 95), src=C)
    c.contest("appeals-4-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Jayme Hartley Fountain", "REP"), ("Todd L. Grace", "DEM")],
              detail="4th District · full term commencing February 9, 2027", src=C)

    # --- County ---
    c.contest("commissioner", "County offices", "County Commissioner", [("Autumn Brown", "DEM"), ("Sarah Danielle Smith", "REP")],
              detail="Full term commencing January 1, 2027", src=C)
    c.contest("auditor", "County offices", "County Auditor", [("Jill A. Davidson", "REP")], detail="Full term commencing March 8, 2027", src=C)
    NP = " · no party label on the ballot"
    c.contest("cp-general", "Court of Common Pleas", "Judge of the Court of Common Pleas, General Division", ["Patrick Lang"],
              detail="Full term commencing February 9, 2027" + NP, src=C)
    c.contest("cp-probate-juvenile", "Court of Common Pleas", "Judge of the Court of Common Pleas, Probate/Juvenile Division", ["Zachary Lane Saunders"],
              detail="Full term commencing February 9, 2027" + NP, src=C)

    # --- Issues ---
    c.issue("issue-1", "question", "Alexander Local School District (Athens, Meigs and Vinton)", "School district income tax: 0.75 percent, 5 years, current expenses",
            SD("ALEXANDER LOCAL SD (ATHENS)"), number=N(1),
            area="Precincts Alexander East, Alexander West, Athens Baker (part), Albany Village, Lee Township, Lodi Township, New Marshfield (part) and Waterloo (part)",
            text="Shall an annual income tax of 0.75 percent on the earned income of individuals residing in the school district be imposed by Alexander Local School District, "
                 "for 5 years, beginning January 1, 2027, for the purpose of current expenses?", src=I)
    c.issue("issue-2", "question", "Athens City School District", "School district income tax (renewal): 1 percent, continuing, current operating expenses",
            SD("ATHENS CITY SD"), number=N(2),
            text="Shall an annual income tax of 1 percent on earned income of individuals residing in the school district be imposed by the Athens City School District, "
                 "to renew an income tax expiring at the end of 2028, for a continuing period of time, beginning January 1, 2029, for the purpose of current operating expenses?", src=I)

    # Local liquor options. Precinct codes are inconsistent: Issue 4 is printed as "0023 - Nelsonville 2" in both documents, but the
    # 46-day notice's own State Rep list has 0019/1-Nelsonville 2 (0023/1 is Alexander West); Lodi Township is 0038/1 in the 46-day
    # notice but "Precinct 0044" in the notices of election. The precinct names are used here.
    c.issue("issue-4", "liquor", "City of Nelsonville", "Local liquor option: The Mine Tavern (Sunday sales)", P("NELSONVILLE CITY"), number=N(4),
            area="Nelsonville City precinct Nelsonville 2",
            text="Shall the sale of wine and mixed beverages and spirituous liquor be permitted for sale on Sunday by Gatway LLC, dba The Mine Tavern, an applicant for and a holder of "
                 "a D-6, D-1, D-2, D-3 and D-3A liquor permits authorizing on/off premise sales who is engaged in the business of operating a bar/restaurant at "
                 "14 Public Square & Back Patio, Nelsonville, OH 45764 in this precinct?", src=I)
    LODI = P("LODI TOWNSHIP")
    c.issue("issue-5", "liquor", "Lodi Township", "Local liquor option: Big 33 LLC (C-1, C-2 and D-6 permits)", LODI, number=N(5), area="Lodi Township precinct",
            text="Shall the sale of beer, wine and mixed beverages be permitted by Big 33 LLC, an applicant for a C1, C2 and D6 liquor permit(s), who is engaged in the business of "
                 "family-oriented, full service gas station, convenience store and food service at 12100 Pleasanton Road, Athens, OH 45701 in this precinct?", src=I)
    c.issue("issue-6", "liquor", "Lodi Township", "Local liquor option: Big 33 LLC (Sunday sales)", LODI, number=N(6), area="Lodi Township precinct",
            text="Shall the sale of beer, wine and mixed beverages be permitted for sale on Sunday by Big 33 LLC, an applicant for a C1, C2 and D6 liquor permit(s), who is engaged in the "
                 "business of family-oriented, full service gas station, convenience store and food service at 12100 Pleasanton Road, Athens, OH 45701 in this precinct?", src=I)

    c.levy("issue-7", "Athens County", "county", "Additional", "Maintenance and operation of the Athens City-County Health Department.", "1 mill",
           "10 years, commencing in 2026", "2027", est("$1,520,051", "$35"), number=N(7), src=I)

    # Villages
    c.levy("issue-8", "Village of Albany", P("ALBANY VILLAGE"), "Additional", "Street maintenance.", "3 mills", "5 years, commencing in 2026", "2027",
           est("$63,273", "$105"), number=N(8), src=I)
    AMES_V = P("AMESVILLE VILLAGE")
    c.levy("issue-9", "Village of Amesville", AMES_V, "Renewal", "Police department, equipment and personnel.", "2 mills", "5 years, commencing in 2027", "2028",
           est("$3,864", "$54"), number=N(9), src=I)
    c.levy("issue-10", "Village of Amesville", AMES_V, "Renewal", "Current expenses.", "2 mills", "5 years, commencing in 2027", "2028",
           est("$3,864", "$54"), number=N(10), src=I)
    c.levy("issue-11", "Village of Buchtel (Athens and Hocking)", P("BUCHTEL VILLAGE"), "Additional", "Current expenses.", "5 mills", "5 years, commencing in 2026", "2027",
           est("$32,611", "$175"), number=N(11), src=I)
    c.levy("issue-12", "Village of Chauncey", P("CHAUNCEY VILLAGE"), "Renewal", "Current expenses.", "5 mills", "5 years, commencing in 2026", "2027",
           est("$30,475", "$128"), number=N(12), src=I)
    JV = P("JACKSONVILLE VILLAGE")
    c.levy("issue-13", "Village of Jacksonville", JV, "Renewal", "Fire protection.", "5 mills", "5 years, commencing in 2027", "2028",
           est("$17,677", "$134"), number=N(13), src=I)
    c.levy("issue-14", "Village of Jacksonville", JV, "Renewal", "Current expenses.", "5.3 mills", "5 years, commencing in 2027", "2028",
           est("$18,956", "$144"), number=N(14), src=I)

    # Townships
    c.levy("issue-15", "Alexander Township (excluding Albany Village)", P("ALEXANDER TOWNSHIP"), "Renewal", "Fire protection.", "1 mill",
           "5 years, commencing in 2027", "2028", est("$112,912", "$35"), number=N(15), area="Precincts Alexander East and Alexander West", src=I)
    AMES_T = P("AMES TOWNSHIP"); AMES_A = "Ames Township precincts (excluding Amesville Village)"
    c.levy("issue-16", "Ames Township (excluding Amesville Village)", AMES_T, "Renewal", "Fire protection.", "1 mill",
           "5 years, commencing in 2026", "2027", est("$20,000", "$19"), number=N(16), area=AMES_A, src=I)
    c.levy("issue-17", "Ames Township (excluding Amesville Village)", AMES_T, "Renewal", "Road maintenance.", "2 mills",
           "5 years, commencing in 2026", "2027", est("$52,631", "$54"), number=N(17), area=AMES_A, src=I)
    # Includes the part of Athens City in Canaan Township (precincts 0013/2 and 0013/3, Athens 4-1).
    CAN = P("CANAAN TOWNSHIP", "ATHENS CITY"); CAN_A = "Canaan Township precincts and Athens 4-1 (part), the part of Athens City in Canaan Township"
    c.levy("issue-18", "Canaan Township (including Athens City)", CAN, "Renewal", "Fire protection.", "0.4 mill",
           "5 years, commencing in 2027", "2028", est("$19,935", "$10"), number=N(18), area=CAN_A, src=I)
    c.levy("issue-19", "Canaan Township (including Athens City)", CAN, "Renewal", "Maintaining and operating cemeteries.", "0.5 mill",
           "5 years, commencing in 2027", "2028", est("$28,371", "$15"), number=N(19), area=CAN_A, src=I)
    CAR = P("CARTHAGE TOWNSHIP")
    c.levy("issue-20", "Carthage Township", CAR, "Additional", "General construction, reconstruction, resurfacing and repair of streets, roads and bridges.", "3 mills",
           "5 years, commencing in 2027", "2028", est("$121,111", "$105"), number=N(20),
           note="The 46-day notice calls this a road maintenance levy; the purpose shown is from the Board's notice of election.", src=I)
    c.levy("issue-21", "Carthage Township", CAR, "Additional", "Maintaining and operating cemeteries.", "0.6 mill",
           "5 years, commencing in 2027", "2028", est("$24,222", "$21"), number=N(21), src=I)
    c.levy("issue-22", "Dover Township (excluding Chauncey Village)", P("DOVER TOWNSHIP"), "Renewal",
           "General construction, reconstruction, resurfacing and repair of streets, roads and bridges.", "2 mills",
           "5 years, commencing in 2027", "2028", est("$98,473", "$59"), number=N(22), area="Precincts Dover East and Dover West",
           note="The 46-day notice calls this a road maintenance levy; the purpose shown is from the Board's notice of election.", src=I)
    LEE = P("LEE TOWNSHIP")
    for n in (23, 24):
        c.levy(f"issue-{n}", "Lee Township (excluding Albany Village)", LEE, "Renewal",
               "Fire fighting facilities, equipment and personnel, including paramedics and other emergency services.", "0.5 mill",
               "5 years, commencing in 2027", "2028", est("$28,760", "$12"), number=N(n), area="Lee Township precinct",
               note="Issues 23 and 24 are two separate Lee Township fire levies with the same wording in the Board's notices.", src=I)
    c.levy("issue-25", "Lodi Township", LODI, "Renewal", "Fire protection.", "1 mill",
           "5 years, commencing in 2026", "2027", est("$37,031", "$29"), number=N(25), src=I)
    c.levy("issue-26", "Rome Township", P("ROME TOWNSHIP"), "Renewal", "Road maintenance including dust control.", "5.5 mills",
           "5 years, commencing in 2027", "2028", est("$153,046", "$174"), number=N(26), src=I)
    c.levy("issue-27", "Troy Township (excluding Coolville Village)", P("TROY TOWNSHIP"), "Additional",
           "General construction, reconstruction, resurfacing and repair of streets and bridges.", "2 mills",
           "5 years, commencing in 2026", "2027", est("$110,377", "$70"), number=N(27), area="Precincts Troy East and Troy West", src=I)
    c.levy("issue-28", "Troy Township (including Coolville Village)", P("TROY TOWNSHIP", "COOLVILLE VILLAGE"), "Renewal", "Maintaining and operating cemeteries.", "0.9 mill",
           "5 years, commencing in 2027", "2028", est("$48,559", "$26"), number=N(28), area="Precincts Coolville Village, Troy East and Troy West", src=I)
    c.levy("issue-29", "York Township (including Nelsonville and Buchtel)", P("YORK TOWNSHIP", "NELSONVILLE CITY", "BUCHTEL VILLAGE"), "Additional",
           "Maintaining and operating cemeteries.", "1 mill", "5 years, commencing in 2026", "2027", est("$132,610", "$35"), number=N(29),
           area="Precincts Nelsonville 1 to 4, Buchtel Village and York Township", src=I)
    return c
