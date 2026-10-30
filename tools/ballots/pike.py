from lib import County, NOTE_ORDER, NOTE_PLACES

SITE = "https://www.boe.ohio.gov/pike/"
NOTICE = "https://www.boe.ohio.gov/pike/c/upload/FWAB_11November46Day.pdf"
BALLOTS = "https://lookup.boe.ohio.gov/vtrapp/pike/ballotlist.aspx"

APPEALS_4 = "4th District"


def build():
    # Raw SoS names already display correctly except the misspelled "JACKSON TOWNSHP".
    # The Board's precincts "Ward 1" to "Ward 5" are Waverly (SoS "WAVERLY VILLAGE").
    c = County("pike", "Pike", "39131", rename={"JACKSON TOWNSHP": "Jackson Township"})
    c.src("pike-46day", "Pike County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election (revised September 14, 2026)", NOTICE)
    c.src("pike-ballots", "Pike County Board of Elections: precinct sample ballots, November 3, 2026 General Election (retrieved October 30, 2026)", BALLOTS)
    S = ["pike-46day", "pike-ballots"]
    c.links = [
        {"label": "Board of Elections", "url": SITE},
        {"label": "Candidates & Issues", "url": "https://www.boe.ohio.gov/pike/election-info/candidates-and-issues/"},
        {"label": "Federal write-in absentee ballot notices", "url": "https://www.boe.ohio.gov/pike/election-info/federal-write-in-absentee-ballots/"},
        {"label": "Sample ballots by precinct", "url": BALLOTS},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://www.boe.ohio.gov/pike/election-info/election-results/"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it, "
               "checked against the Board's precinct sample ballots. Issue wording is from the notice and matches the sample ballots.",
               NOTE_ORDER, NOTE_PLACES,
               "The Board's notice and sample ballots do not give local issue numbers; see your sample ballot for the order.",
               "Court of Appeals: the 46-day notice (revised September 14, 2026) lists Peter B. Abele (Republican) for the 4th District seat; he withdrew "
               "after his death, and the Board's sample ballots list Jayme Hartley Fountain (Republican) and Todd L. Grace (Democratic), as shown here."]
    P = c.p; D = c.district; SD = c.sd

    # --- Federal, state legislative, appeals (every precinct is in the 2nd Congressional, 17th Senate, 91st House and 4th Appeals districts) ---
    c.contest("congress-2", "U.S. House", "Representative to Congress", [("Jen Mazzuckelli", "DEM"), ("David J. Taylor", "REP")],
              detail="2nd District", places=D("cong", 2), src=S)
    c.contest("senate-17", "Ohio General Assembly", "State Senator", [("Brian A. Deer", "DEM"), ("Shane Wilkin", "REP")],
              detail="17th District", places=D("sen", 17), src=S)
    c.contest("rep-91", "Ohio General Assembly", "State Representative", [("Bob Peterson", "REP"), ("Amy Wright", "DEM")],
              detail="91st District", places=D("rep", 91), src=S)
    # The notice lists only Peter B. Abele (Rep); the sample ballots list Fountain and Grace, as in Ross, Scioto and Highland.
    c.contest("appeals-4-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Jayme Hartley Fountain", "REP"), ("Todd L. Grace", "DEM")],
              detail=APPEALS_4 + " · full term commencing February 9, 2027", src=["pike-ballots", "pike-46day"])

    # --- County ---
    c.contest("commissioner", "County offices", "County Commissioner", [("Neil Edward Leist", "REP"), ("Bob Thompson", "DEM")],
              detail="Full term commencing January 1, 2027", src=S)
    c.contest("auditor", "County offices", "County Auditor", [("Davida K. Brown", "REP")], detail="Full term commencing March 8, 2027", src=S)
    NP = " · no party label on the ballot"
    c.contest("cp-probate-juvenile", "Court of Common Pleas", "Judge of the Court of Common Pleas, Probate and Juvenile Division", ["Paul Price"],
              detail="Full term commencing February 9, 2027" + NP, src=S)

    # --- Issues (unnumbered in the notice and on the sample ballots; listed in the notice's order) ---
    c.levy("pike-dd", "Pike County", "county", "Additional",
           "Developmental disabilities programs and services, including The Kemper Connection school-age program, and the facilities of the Pike County Board of Developmental Disabilities.",
           "2 mills", "5 years, commencing in 2026", "2027", "$1,327,292 a year; $70 for each $100,000 of market value", src=S)
    c.issue("piketon-liquor-dutchess", "liquor", "Piketon Village", "Local liquor option: Piketon Dutchess (Sunday)", P("PIKETON VILLAGE"),
            area="Precinct Piketon Village",
            text="Shall the sale of wine and mixed beverages and spirituous liquor be permitted for sale on Sunday by Englefield, Inc. dba Piketon Dutchess "
                 "an applicant for a D-6 liquor permit who is engaged in the business of operating a carryout/grocery store at 615 S. West St, Piketon, OH 45661 "
                 "in this precinct?", src=S)
    TWP = [
        ("benton-twp-cemeteries", "Benton Township", ["BENTON TOWNSHIP"], "Maintaining and operating cemeteries.", "1.6 mills",
         "$31,194 a year; $28 for each $100,000 of market value", "Precinct Benton Township"),
        ("mifflin-twp-fire", "Mifflin Township", ["MIFFLIN TOWNSHIP"], "Fire protection.", "1 mill",
         "$8,809 a year; $9 for each $100,000 of market value", "Precinct Mifflin Township"),
        ("pebble-twp-cemeteries", "Pebble Township", ["PEBBLE TOWNSHIP"], "Maintaining and operating cemeteries.", "1.5 mills",
         "$71,164 a year; $41 for each $100,000 of market value", "Precinct Pebble Township (splits 1 and 2)"),
        ("perry-twp-fire", "Perry Township", ["PERRY TOWNSHIP"], "Fire protection.", "2 mills",
         "$11,258 a year; $17 for each $100,000 of market value", "Precinct Perry Township"),
        ("seal-piketon-fire", "Seal Township and Piketon Village", ["SEAL TOWNSHIP", "PIKETON VILLAGE"], "Fire protection.", "1 mill",
         "$56,318 a year; $26 for each $100,000 of market value", "Precincts Seal Township and Piketon Village"),
    ]
    for id, jur, raws, purpose, mills, est, area in TWP:
        c.levy(id, jur, P(*raws), "Renewal", purpose, mills, "5 years, commencing in 2027", "2028", est, area=area, src=S)
    # The notice's precinct cell for this option reads "Seal Township/1, Piketon Village/1", but only the Seal Township sample ballot carries it.
    c.issue("seal-twp-liquor-grove-patio", "liquor", "Seal Township", "Local liquor option: Grove & Patio (Sunday)", P("SEAL TOWNSHIP"),
            area="Precinct Seal Township",
            text="Shall the sale of wine and mixed beverages and spirituous liquor be permitted for sale on Sunday by Clemmons Investments LLC dba Grove & Patio "
                 "an applicant for a D-6 liquor permit who is engaged in the business of operating a restaurant/bar at 5495 Wakefield Mound Road, "
                 "Seal Township, Piketon, OH 45661 in this precinct?", src=S)
    for id, jur, raws, purpose, mills, est, area in [
        ("sunfish-twp-fire", "Sunfish Township", ["SUNFISH TOWNSHIP"], "Fire protection.", "1.5 mills",
         "$19,822 a year; $15 for each $100,000 of market value", "Precinct Sunfish Township (splits 1 and 2)"),
        ("union-twp-cemeteries", "Union Township", ["UNION TOWNSHIP"], "Maintaining and operating cemeteries.", "1 mill",
         "$7,255 a year; $7 for each $100,000 of market value", "Precinct Union Township"),
    ]:
        c.levy(id, jur, P(*raws), "Renewal", purpose, mills, "5 years, commencing in 2027", "2028", est, area=area, src=S)
    # Same id, title and wording as ross.py (the Pike Board files this issue). Pee Pee Township A split 2 and Jackson Township split 3 are not in
    # the district per the notice and sample ballots; the voter file puts all of Pee Pee and most of Jackson in it.
    c.issue("waverly-csd-income-tax", "question", "Waverly City School District (Pike and Ross)", "School district income tax: 0.5 percent, 5 years, current expenses",
            SD("WAVERLY CITY SD"),
            area="Precincts Ward 1 to Ward 5 (Waverly), Jackson Township (splits 1 and 2), Pebble Township (split 1), Pee Pee Township A (split 1) and Pee Pee Township B",
            text="Shall an annual income tax of 0.5 per cent on the earned income of individuals residing in the school district be imposed by the Waverly City School District, "
                 "for a period of 5 years, beginning January 1, 2027, for the purpose of current expenses?", src=S)
    c.issue("waverly-ward5-liquor-aerie", "liquor", "Waverly", "Local liquor option: F.O.E. Aerie 2227 Waverly (Sunday)", P("WAVERLY VILLAGE"),
            area="Precinct Ward 5 (Waverly)",
            text="Shall the sale of wine and mixed beverages and spirituous liquor be permitted for sale on Sunday by F.O.E. Aerie 2227 Waverly an applicant "
                 "for a D-6 Liquor Permit who is engaged in the business of operating a fraternal organization at 243 W. North St, Waverly, OH 45690 "
                 "in this precinct?", src=S)
    return c
