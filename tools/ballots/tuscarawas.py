from lib import County, NOTE_ORDER, NOTE_PLACES

NOTICE = "https://www.boe.ohio.gov/tuscarawas/c/upload/FWAB_11November46Day.pdf"
CANDISS = "https://www.boe.ohio.gov/tuscarawas/c/upload/election_candiss.pdf"


def build():
    c = County("tuscarawas", "Tuscarawas", "39157")
    c.src("tuscarawas-46day", "Tuscarawas County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election (revised 9/18/2026)", NOTICE)
    c.src("tuscarawas-candiss", "Tuscarawas County Board of Elections: official filings (certified candidates and issues), November 3, 2026 General Election", CANDISS)
    S = ["tuscarawas-46day", "tuscarawas-candiss"]
    c.links = [
        {"label": "Board of Elections", "url": "https://www.boe.ohio.gov/tuscarawas/"},
        {"label": "Election information", "url": "https://www.boe.ohio.gov/tuscarawas/election-info/"},
        {"label": "Sample ballots by precinct", "url": "https://lookup.boe.ohio.gov/vtrapp/tuscarawas/ballotlist.aspx"},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://www.boe.ohio.gov/tuscarawas/"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it, "
               "checked against the Board's list of certified candidates and issues. Issue wording is the Board's summary; the full wording is on the sample ballot.",
               NOTE_ORDER, NOTE_PLACES]
    P = c.p; D = c.district; SD = c.sd
    NP = " · no party label on the ballot"

    # --- Federal, state legislative ---
    c.contest("congress-6", "U.S. House", "Representative to Congress", [("Elizabeth Ann Kirtley", "DEM"), ("Michael A. Rulli", "REP")], detail="6th District", places=D("cong", 6), src=S)
    c.contest("senate-31", "Ohio General Assembly", "State Senator", [("Laura Sirot", "DEM"), ("Al Landis", "REP")], detail="31st District", places=D("sen", 31), src=S)
    c.contest("rep-51", "Ohio General Assembly", "State Representative", [("Amanda Fontana", "DEM"), ("Jodi Salvo", "REP")], detail="51st District", places=D("rep", 51), src=S)
    # Neither Board document lists a 5th District Court of Appeals race (Stark, Licking and others list Matthew George); left out.

    # --- County offices ---
    c.contest("commissioner", "County offices", "County Commissioner", [("Kent A. Watson", "DEM"), ("Kristin R. Zemis", "REP")], detail="Full term commencing January 1, 2027", src=S)
    c.contest("auditor", "County offices", "County Auditor", [("Joe Rinehart", "DEM"), ("Lisa Contini", "REP")], detail="Full term commencing March 8, 2027", src=S)
    c.contest("prosecutor", "County offices", "Prosecuting Attorney", [("R. Scott Deedrick", "REP")], detail="Unexpired term ending December 31, 2028", src=S)

    # --- Common Pleas ---
    c.contest("cp-0101", "Court of Common Pleas", "Judge of the Court of Common Pleas", ["Ryan Styer", "Christine M. Weimer"], detail="Unexpired term ending December 31, 2028" + NP, src=S)
    c.contest("cp-0102", "Court of Common Pleas", "Judge of the Court of Common Pleas", ["Michael J. Ernest"], detail="Full term commencing January 2, 2027" + NP, src=S)
    c.contest("cp-probate", "Court of Common Pleas", "Judge of the Court of Common Pleas, Probate Division", ["Adam W. Wilgus"], detail="Full term commencing February 9, 2027" + NP, src=S)

    N = lambda n: f"Issue {n}"
    est = lambda total, per: f"{total} a year; {per} for each $100,000 of market value"

    # Issue 4: levy decrease by petition (Claymont City SD).
    c.issue("issue-4", "levy", "Claymont City School District", "Tax levy decrease (by petition): 5 mills to 2 mills, current operating expenses and general permanent improvements",
            SD("CLAYMONT CITY SD"), number=N(4),
            area="Claymont City School District (precincts 0029–0032, 0057/1, 0057/2, 0058/1, 0059/1, 0065/1, 0074/1, 0077/2)",
            levy={"type": "Decrease (by petition)", "purpose": "Current operating expenses and general permanent improvements (continuing levy approved March 17, 2020).",
                  "mills": "From 5 mills to 2 mills", "term": "Continuing period of time",
                  "estimate": "Now $1,309,022 a year ($127 for each $100,000 of market value); after the decrease $523,609 a year ($51 for each $100,000)"},
            text="Shall the rate of tax be reduced from 5 mills to 2 mills?", src=S)

    L = [
        # (n, jurisdiction, places, type, purpose, mills, term, firstDue, estimate, area)
        (5, "Arrowhead Joint Fire District", P("GNADENHUTTEN VILLAGE", "CLAY TOWNSHIP"), "Renewal", "Current expenses.", "4 mills", "5 years, commencing in 2027", "2028", est("$225,855", "$79"),
         "Arrowhead Joint Fire District (precincts 0036/1, 0037/1, 0037/2: Gnadenhutten and Clay Township)"),
        (6, "Sandy Valley Local School District (Stark, Carroll and Tuscarawas)", SD("SANDY VALLEY LOCAL SD (STARK)"), "Renewal", "Current operating expenses.", "2.3 mills", "5 years, commencing in 2027", "2028", est("$750,000", "$81"),
         "Sandy Valley Local School District, Tuscarawas County part (precincts 0069/1, 0070/1)"),
        # Precincts 47/4–47/5 (Roswell) and 49/3 (Barnhill) are not in the fire district.
        (7, "Goshen Township Fire District", P("GOSHEN TOWNSHIP"), "Renewal", "Fire and ambulance.", "2.15 mills", "5 years, commencing in 2027", "2028", est("$224,788", "$53"),
         "Goshen Township Fire District (precincts 0047/1–0047/3, 0048/1–0048/2, 0049/1–0049/2, 0050/1–0050/2)"),
        (8, "Tuscarawas County", "county", "Additional", "Community programs and services authorized by the county board of developmental disabilities, and developmental disabilities facilities.",
         "1.2 mills", "10 years, commencing in 2026", "2027", est("$4,214,524", "$42"), "All of Tuscarawas County"),
        (9, "City of New Philadelphia", P("NEW PHILADELPHIA CITY"), "Additional", "Parks and recreation.", "2.4 mills", "5 years, commencing in 2026", "2027", est("$1,335,678", "$84"), None),
        (10, "City of Uhrichsville", P("UHRICHSVILLE CITY"), "Renewal", "Current expenses.", "2.8 mills", "5 years, commencing in 2026", "2027", est("$141,637", "$41"), None),
        (12, "Village of Bolivar", P("BOLIVAR VILLAGE"), "Renewal", "Street construction projects.", "2.9 mills", "5 years, commencing in 2027", "2028", est("$33,396", "$40"), None),
        (13, "Village of Bolivar", P("BOLIVAR VILLAGE"), "Renewal", "Current expenses.", "1.8 mills", "5 years, commencing in 2027", "2028", est("$20,729", "$25"), None),
        (14, "Village of Dennison", P("DENNISON VILLAGE"), "Renewal", "Current operating expenses.", "1.5 mills", "5 years, commencing in 2027", "2028", est("$48,988", "$25"), None),
        (15, "Village of Gnadenhutten", P("GNADENHUTTEN VILLAGE"), "Renewal", "Current operating expenses.", "3 mills", "5 years, commencing in 2027", "2028", est("$38,174", "$27"), None),
        (16, "Village of Roswell", P("ROSWELL VILLAGE"), "Renewal and increase", "Current operating expenses (renewal of 5 mills and increase of 0.5 mill).", "5.5 mills", "5 years, commencing in 2027", "2028", est("$10,547", "$110"), None),
        (17, "Village of Roswell", P("ROSWELL VILLAGE"), "Renewal and increase", "Refuse service for village residents (renewal of 5.5 mills and increase of 2.1 mills).", "7.6 mills", "5 years, commencing in 2027", "2028", est("$17,056", "$182"), None),
        (18, "Village of Sugarcreek", P("SUGARCREEK VILLAGE"), "Renewal", "Current expenses.", "2 mills", "5 years, commencing in 2026", "2027", est("$147,585", "$33"), None),
        (19, "Village of Tuscarawas", P("TUSCARAWAS VILLAGE"), "Renewal", "Park maintenance.", "1 mill", "5 years, commencing in 2026", "2027", est("$13,870", "$19"), None),
        (20, "Village of Tuscarawas", P("TUSCARAWAS VILLAGE"), "Additional", "Police protection for village residents.", "2.8 mills", "Continuing period of time, commencing in 2026", "2027", est("$69,315", "$98"), None),
        (21, "Bucks Township (excluding the Village of Baltic)", P("BUCKS TOWNSHIP"), "Additional", "General construction, reconstruction, resurfacing and repair of streets, roads and bridges.", "2 mills", "5 years, commencing in 2026", "2027", est("$100,233", "$70"),
         "Bucks Township outside Baltic (precincts 0035/1–0035/3)"),
        (22, "Fairfield Township", P("FAIRFIELD TOWNSHIP"), "Renewal", "Fire apparatus and fire alarm lines, and emergency ambulance and emergency medical services.", "1.5 mills", "5 years, commencing in 2027", "2028", est("$29,051", "$6"), None),
        (23, "Oxford Township (excluding the Village of Newcomerstown)", P("OXFORD TOWNSHIP"), "Renewal", "Fire protection.", "0.85 mill", "5 years, commencing in 2026", "2027", est("$48,357", "$21"),
         "Oxford Township outside Newcomerstown (precinct 0063/1)"),
        # Precincts 47/5 and 57/2 are the Union Township parts of Roswell and Dennison.
        (24, "Union Township", P("UNION TOWNSHIP", "ROSWELL VILLAGE", "DENNISON VILLAGE"), "Renewal", "Fire and ambulance services.", "1 mill", "5 years, commencing in 2027", "2028", est("$40,673", "$18"),
         "Union Township (precincts 0074/1, 0074/2, plus the Union Township parts of Roswell 0047/5 and Dennison 0057/2)"),
        (25, "Warren Township", P("WARREN TOWNSHIP"), "Renewal", "Maintaining and operating cemeteries.", "0.4 mill", "5 years, commencing in 2027", "2028", est("$40,010", "$8"), None),
        (26, "Warren Township", P("WARREN TOWNSHIP"), "Renewal", "Fire protection and ambulance service.", "0.3 mill", "5 years, commencing in 2027", "2028", est("$29,091", "$5"), None),
        (27, "Wayne Township", P("WAYNE TOWNSHIP"), "Renewal", "Current expenses.", "0.4 mill", "5 years, commencing in 2027", "2028", est("$21,523", "$8"), None),
    ]
    for n, jur, places, t, purpose, mills, term, due, estimate, area in L:
        c.levy(f"issue-{n}", jur, places, t, purpose, mills, term, due, estimate, number=N(n), area=area, src=S)

    c.issue("issue-11", "question", "Village of Barnhill", "Surrender of corporate powers (by petition)", P("BARNHILL VILLAGE"), number=N(11),
            text="Shall the village known as Village of Barnhill surrender its corporate power?", src=S)

    c.issue("issue-28", "liquor", "City of Uhrichsville", "Local liquor option: Uhrichsville Duchess (Sunday)", P("UHRICHSVILLE CITY"), number=N(28), area="Uhrichsville precinct 1 (0029, all splits)",
            text="Sunday sale of wine and mixed beverages by Englefield, Inc., dba Uhrichsville Duchess (D-6 permit applicant, off-premise sales), a carryout/grocery at 110 E. McCauley Drive, Uhrichsville.", src=S)
    c.issue("issue-29", "liquor", "Village of Bolivar", "Local liquor option: Army & Navy Union Garrison 1982 Bolivar (Sunday)", P("BOLIVAR VILLAGE"), number=N(29), area="Bolivar Village precinct (0052, all splits)",
            text="Sunday sale of beer, wine and mixed beverages and spirituous liquor by Army & Navy Union Garrison 1982 Bolivar (D-6 permit applicant, on-premise sales), a non-profit veterans organization at 165 Canal Street, Bolivar.", src=S)
    c.issue("issue-30", "liquor", "Village of Dennison", "Local liquor option: Holy Moley Brewing Co. (Sunday)", P("DENNISON VILLAGE"), number=N(30), area="Dennison Village precinct 2 (0058, all splits)",
            text="Sunday sale of spirituous liquor by O.B.M. Productions, L.L.C., dba Holy Moley Brewing Co. (D-6 permit holder, on-premise sales), a brewery at 306 Grant St., Dennison.", src=S)
    c.issues.sort(key=lambda q: int(q["id"].split("-")[1]))
    return c
