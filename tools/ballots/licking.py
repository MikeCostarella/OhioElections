from lib import County, NOTE_ORDER, NOTE_PLACES

NOTICE = "https://www.boe.ohio.gov/licking/c/upload/FWAB_11November46Day.pdf"
CAND = "https://www.boe.ohio.gov/licking/c/upload/ELECTION_Candidates.pdf"
ISSUES = "https://www.boe.ohio.gov/licking/c/upload/ELECTION_Issues.pdf"


def build():
    c = County("licking", "Licking", "39089", rename={"MC KEAN TWP": "McKean Township"})
    c.src("licking-46day", "Licking County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election", NOTICE)
    c.src("licking-cand", "Licking County Board of Elections: certified candidates, November 3, 2026 General Election (August 28, 2026)", CAND)
    c.src("licking-issues", "Licking County Board of Elections: filed issues list, November 3, 2026 General Election (revised 9/1/2026)", ISSUES)
    C = ["licking-46day", "licking-cand"]; I = ["licking-46day", "licking-issues"]
    c.links = [
        {"label": "Board of Elections", "url": "https://www.boe.ohio.gov/licking/"},
        {"label": "Election information", "url": "https://www.boe.ohio.gov/licking/election-info/"},
        {"label": "Sample ballots by precinct", "url": "https://lookup.boe.ohio.gov/vtrapp/licking/ballotlist.aspx"},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://www.boe.ohio.gov/licking/election-info/election-results/"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it, "
               "checked against the Board's certified candidate list and filed issues list. Issue wording is the Board's summary; the full wording is on the sample ballot.",
               NOTE_ORDER, NOTE_PLACES,
               "The Board's notice and issues list do not give local issue numbers; see your sample ballot for them."]
    P = c.p; D = c.district; SD = c.sd

    # --- Federal, state legislative, appeals ---
    c.contest("congress-12", "U.S. House", "Representative to Congress", [("Troy Balderson", "REP"), ("Jerrad Christian", "DEM")], detail="12th District", src=C)
    # The notice puts precinct Heath 2-B/5 in the 68th District; the voter file has no Heath voters there.
    c.contest("rep-68", "Ohio General Assembly", "State Representative", [("Mason Blankenship", "DEM"), ("Thad Claggett", "REP")], detail="68th District",
              places=sorted(set(D("rep", 68) + P("HEATH CITY"))), src=C)
    c.contest("rep-69", "Ohio General Assembly", "State Representative", [("Kevin D. Miller", "REP"), ("Amy Rigsby", "DEM")], detail="69th District (also in Fairfield and Perry counties)",
              places=D("rep", 69), src=C)
    c.contest("appeals-5", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Matthew George", "REP")], detail="5th District · term commencing February 9, 2027", src=C)

    # --- County offices ---
    c.contest("commissioner", "County offices", "County Commissioner", [("Kathy McLeish", "DEM"), ("Mark A. Van Buren", "REP")], detail="4-year term", src=C)
    c.contest("auditor", "County offices", "County Auditor", [("Michael L. Smith", "REP")], detail="4-year term", src=C)
    NP = " · no party label on the ballot"
    for id, office, date, cs in [
        ("cp-gen", "General Division", "Term commencing February 9, 2027", ["Thomas M. Marcelain"]),
        ("cp-dr", "Domestic Relations Division", "Term commencing January 1, 2027", ["Robert D. Essex", "Richard P. Wright"]),
        ("cp-probate-juvenile", "Probate/Juvenile Division", "Term commencing February 9, 2027", ["Michael DalSanto", "Deborah G. Lang"]),
    ]:
        c.contest(id, "Court of Common Pleas", f"Judge of the Court of Common Pleas, {office}", cs, detail=date + NP, src=C)

    # --- Issues (unnumbered in the Board's documents; listed in the Board's order) ---
    c.levy("licking-park", "Licking Park District", "county", "Renewal", "Parks, trails, and recreational purposes.", ".375 mill", "5 years, commencing in 2027", "2028",
           estimate="$2,274,412 a year; $10 per $100,000 of market value", area="Licking County (all 96 precincts)", src=I)

    HE = P("HEATH CITY")
    for i, (title, text) in enumerate([
        ("Charter amendment: Sections 4.06, 4.07 and 4.08 (emergency resolutions)",
         "Shall Sections 4.06, 4.07, and 4.08 be amended to remove all provisions for emergency resolutions and to provide that any resolution shall take effect, unless a later time be specified therein, immediately upon its passage?"),
        ("Charter amendment: Section 4.12 (Planning Commission deadline on rezoning, 30 to 60 days)",
         "Shall Section 4.12 of the Charter of the City of Heath be amended to extend, from 30 days to 60 days, the deadline for the Planning Commission to cause rezoning ordinances or resolutions to be returned to the Clerk of Council together with the Commission's written recommendations?"),
        ("Charter amendment: publication of ordinances and notices (Section 4.13)",
         "Shall applicable sections of the Charter of the City of Heath be amended to allow municipal ordinances, resolutions, statements, orders, proclamations, notices, and reports to be published in accordance with Ohio Revised Code section 731.21 and to strike an unconstitutional provision in section 4.13 of the Charter?"),
    ], 1):
        c.issue(f"heath-charter-{i}", "question", "City of Heath", title, HE, area="Heath 1-A, 1-B, 2-A, 2-B, 3-A, 3-B", text=text, src=I)

    PA = P("PATASKALA CITY")
    for i, (title, text) in enumerate([
        ("Charter amendment: Charter Revision Commission recommendations (Sections 3.02, 4.14, 5.04, 5.05, 6.02, 6.03, 8.02, 9.01, 10.02, 11.01)",
         "Shall Sections 3.02 (Composition, Term and Qualifications of Council), 4.14 (Publication of Ordinances and Resolutions), 5.04 (City Administrator), 5.05 (Powers of City Administrator), "
         "6.02 (Director of Finance), 6.03 (Other Administrative Departments), 8.02 (Contracting Powers and Procedures), 9.01 (Nominations), 10.02 (Recall), and 11.01 (Removal of Officials) "
         "be amended as recommended by the Charter Revision Commission?"),
        ("Charter amendment: Section 3.07 (salaries of elected officials)",
         "Shall Section 3.07 (Salaries of Elected Officials) be amended as recommended by the Charter Revision Commission?"),
        ("Charter amendment: Section 7.04 (Parks and Recreation Board)",
         "Shall Section 7.04 (Parks and Recreation Board) be amended as recommended by the Charter Revision Commission?"),
        ("Charter amendment: new Section 11.09 prohibiting a data center",
         "Shall Section 11.09 (Prohibition of a Data Center) be added thereby prohibiting the construction of a data center within the City limits?"),
    ], 1):
        c.issue(f"pataskala-charter-{i}", "question", "City of Pataskala", title, PA, area="Pataskala 1-A through 4-B (8 precincts)", text=text, src=I)

    c.levy("buckeye-lake-current", "Village of Buckeye Lake (Licking and Fairfield counties)", P("BUCKEYE LAKE VILLAGE"), "Renewal", "Current operating expenses.", "5 mills", "5 years, commencing in 2027", "2028",
           estimate="$409,214 a year; $105 per $100,000 of market value", area="Buckeye Lake Village", src=I)
    c.levy("hanover-village-fire", "Village of Hanover", P("HANOVER VILLAGE"), "Renewal", "Fire protection and emergency medical services in the Village.", "1.5 mills", "5 years, commencing in 2026", "2027",
           estimate="$41,644 a year; $30 per $100,000 of market value", src=I)
    c.issue("granville-data-center", "question", "Village of Granville", "Charter amendment: new Section 10.12 prohibiting a data center", P("GRANVILLE VILLAGE"),
            area="Granville Village A, B, C",
            text="Shall Section 10.12 (Prohibition of a Data Center) be added thereby prohibiting the construction of a data center within the City limits?", src=I)

    L = [
        ("bowling-green-fire", "Bowling Green Township", ["BOWLING GREEN TWP"], "Renewal", "Fire protection and emergency medical services.", "1 mill", "5 years, commencing in 2027", "2028",
         "$44,234 a year; $20 per $100,000 of market value", None),
        ("eden-fire", "Eden Township", ["EDEN TWP"], "Renewal", "Fire protection and emergency medical services.", "1 mill", "5 years, commencing in 2026", "2027",
         "$33,022 a year; $29 per $100,000 of market value", "Eden-Fallsbury Township precinct (Eden Township part)"),
        ("granville-twp-greenspace", "Granville Township", ["GRANVILLE TWP", "GRANVILLE VILLAGE"], "Renewal", "Protecting or preserving greenspace.", "1 mill", "5 years, commencing in 2027", "2028",
         "$362,731 a year; $21 per $100,000 of market value", "Granville Township A–C and Granville Village A–C"),
        ("hanover-twp-fire", "Hanover Township", ["HANOVER TWP", "HANOVER VILLAGE"], "Renewal", "Fire protection and emergency medical services.", "1 mill", "5 years, commencing in 2027", "2028",
         "$103,694 a year; $26 per $100,000 of market value", "Hanover Township and Hanover Village (split 1)"),
        ("licking-twp-fire", "Licking Township", ["LICKING TWP", "HEATH CITY", "BUCKEYE LAKE VILLAGE"], "Additional", "Fire protection and emergency medical services.", "4 mills", "Continuing period of time, commencing in 2026", "2027",
         "$1,084,469 a year; $140 per $100,000 of market value", "Licking Township A–C, Heath 2-B/4 and 3-B/3, Buckeye Lake Village/2"),
        ("mary-ann-fire", "Mary Ann Township", ["MARY ANN TWP"], "Renewal", "Fire protection and emergency medical services.", "1.5 mills", "5 years, commencing in 2027", "2028",
         "$88,270 a year; $42 per $100,000 of market value", None),
        ("newark-twp-roads", "Newark Township", ["NEWARK TWP", "NEWARK CITY"], "Additional", "General construction, reconstruction, resurfacing and repair of streets, roads and bridges.", "1.5 mills", "5 years, commencing in 2026", "2027",
         "$174,566 a year; $53 per $100,000 of market value", "Newark Township, plus Newark City splits 5-B/2, 5-E/2, 6-A/2, 6-B/2, 6-D/2, 6-E/5, 7-B/2"),
        ("washington-twp-roads", "Washington Township (unincorporated area)", ["WASHINGTON TWP"], "Renewal", "General construction, reconstruction, resurfacing, and repair of streets, roads and bridges.", "3 mills", "5 years, commencing in 2027", "2028",
         "$167,894 a year; $89 per $100,000 of market value", "Washington Township (unincorporated area only)"),
    ]
    for id, jur, raws, t, purpose, mills, term, fd, est, area in L:
        c.levy(id, jur, P(*raws), t, purpose, mills, term, fd, estimate=est, area=area, src=I)
    c.issue("perry-twp-zoning", "question", "Perry Township", "Proposed zoning plan for the unincorporated territory of the township", P("PERRY TWP"),
            text="A resolution of the Township of Perry, enacted in accordance with its comprehensive plan and Chapter 519 of the Ohio Revised Code, establishing zoning regulations for the "
                 "unincorporated territory of the township, to conserve and protect property values and rights, secure the most appropriate use of land, guide the orderly development of "
                 "agricultural, residential, commercial, and industrial areas, and promote the public health, safety, morals, comforts, convenience, and general welfare.", src=I)

    # The library's precincts in the notice are exactly the Southwest Licking Local School District's.
    SWL = SD("SOUTHWEST LICKING LOCAL SD (LICKING)")
    SWL_AREA = ("Etna Township A/3, B, C, D; Harrison Township A–E (incl. Kirkersville); Pataskala 1-B/1, 3-A/1, 3-B/1, 3-B/3, 4-A/1, 4-B/1; "
                "St. Albans Township B-Alexandria/2; Union Township A/3, B/2; Reynoldsburg 3-B/2")
    c.levy("pataskala-library", "Pataskala Public Library (Licking and Fairfield counties)", SWL, "Renewal", "Current expenses of the library.", "1 mill", "5 years, commencing in 2027", "2028",
           estimate="$901,850 a year; $21 per $100,000 of market value", area=SWL_AREA, src=I)
    c.issue("swl-income-tax", "question", "Southwest Licking Local School District (Licking and Fairfield counties)",
            "School district income tax: replace the 0.75% tax on school district income with a 2% tax on earned income, continuing, for current operating expenses", SWL, area=SWL_AREA,
            text="Shall the existing tax of 0.75% on the school district income of individuals imposed by the Southwest Licking Local School District be replaced by a tax of 2% on the earned income "
                 "of individuals residing in the school district for a continuing period of time, beginning January 1, 2027, for the purpose of paying the cost of current operating expenses? "
                 "If the new tax is not approved, the existing tax will remain in effect under its original authority, for the remainder of its previously approved term.", src=I)
    c.issue("swl-bond", "levy", "Southwest Licking Local School District (Licking and Fairfield counties)", "Bond issue: $80,710,000 for school facilities", SWL, area=SWL_AREA,
            levy={"type": "Bond issue", "purpose": "Constructing, renovating, expanding, furnishing and equipping school facilities, improving their sites, and acquiring real estate.",
                  "mills": "2.87 mills (estimated average)", "term": "Up to 35 years", "firstDue": "2027", "estimate": "$80,710,000 principal; $100 for each $100,000 of market value"},
            text="Bond issue, principal $80,710,000, maximum 35 years, estimated average 2.87 mills ($100 per $100,000 of market value), commencing in 2026, first due in 2027, for constructing "
                 "school facilities and renovating, repairing, expanding, improving, and constructing additions to school facilities; furnishing and equipping the same; improving the sites "
                 "thereof; and acquiring real estate and interests therein.", src=I)

    # --- Local liquor options ---
    for id, jur, raw, prec, title, text in [
        ("liquor-johnstown-duchess", "City of Johnstown", "JOHNSTOWN CITY", "Johnstown precinct A", "Local liquor option: Johnstown Duchess (Sunday)",
         "Sunday sale of wine and mixed beverages, off-premise sales, by Englefield, Inc., dba Johnstown Duchess, 233 W. Coshocton St., Johnstown."),
        ("liquor-granville-milling", "City of Johnstown", "JOHNSTOWN CITY", "Johnstown precinct B", "Local liquor option: Granville Milling Company Country Store (Sunday)",
         "Sunday sale of wine and mixed beverages, off-premise sales, by Granville Milling Co, known as Granville Milling Company Country Store, 11891 Johnstown-Utica Rd., Johnstown."),
        ("liquor-union-st-duchess", "City of Newark", "NEWARK CITY", "Newark precinct 2-B", "Local liquor option: Union St. Duchess (Sunday)",
         "Sunday sale of wine and mixed beverages, off-premise sales, by Englefield, Inc., dba Union St. Duchess, 224 Union St., Newark."),
        ("liquor-mill-wheel", "City of Newark", "NEWARK CITY", "Newark precinct 2-B", "Local liquor option: Mill Wheel Tavern (Sunday)",
         "Sunday sale of wine and mixed beverages and spirituous liquor, on-premise sales, by Newarks Gateway South, Inc., dba Mill Wheel Tavern (Naughty Pine Pizza), 495 Wehrle Ave., Newark."),
        ("liquor-etna-duchess", "Etna Township", "ETNA  TWP", "Etna Township precinct C", "Local liquor option: Etna Duchess (Sunday)",
         "Sunday sale of wine and mixed beverages, off-premise sales, by Englefield, Inc., dba Etna Duchess, 10202 Hazelton Etna Rd. SW, Pataskala (Etna Township)."),
    ]:
        c.issue(id, "liquor", jur, title, P(raw), area=prec, text=text, src=I)
    return c
