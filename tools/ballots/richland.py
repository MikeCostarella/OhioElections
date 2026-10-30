from lib import County, NOTE_ORDER, NOTE_PLACES

NOTICE = "https://www.boe.ohio.gov/richland/c/upload/FWAB_11November46Day.pdf"


def build():
    c = County("richland", "Richland", "39139")
    c.src("richland-46day", "Richland County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election (revised 9/8/2026)", NOTICE)
    S = ["richland-46day"]
    c.links = [
        {"label": "Board of Elections", "url": "https://www.boe.ohio.gov/richland/"},
        {"label": "Election information", "url": "https://www.boe.ohio.gov/richland/election-info/"},
        {"label": "Candidate list", "url": "https://lookup.boe.ohio.gov/vtrapp/richland/cfis.aspx"},
        {"label": "Questions and issues list", "url": "https://lookup.boe.ohio.gov/vtrapp/richland/webqis/default.aspx"},
        {"label": "Sample ballots by precinct", "url": "https://lookup.boe.ohio.gov/vtrapp/richland/ballotlist.aspx"},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://www.boe.ohio.gov/richland/election-info/election-results/"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it. "
               "Issue wording is condensed from the notice; the full wording is on the sample ballot.",
               NOTE_ORDER, NOTE_PLACES,
               "The Board's notice does not give local issue numbers; see your sample ballot for them."]
    P = c.p; D = c.district; SD = c.sd

    # --- Federal, state legislative, appeals (no State Senate race: the 22nd District is not up in 2026) ---
    c.contest("congress-4", "U.S. House", "Representative to Congress", [("Jim Jordan", "REP"), ("Joshua D. Kolasinski", "DEM"), ("Tracey L. Tackett", "Nonparty")],
              detail="4th District", places=D("cong", 4), src=S)
    c.contest("congress-5", "U.S. House", "Representative to Congress", [("Bob Latta", "REP"), ("Brian A. Shaver", "DEM"), ("Michael J. Veloff", "LIB")],
              detail="5th District", places=D("cong", 5), src=S)
    c.contest("rep-76", "Ohio General Assembly", "State Representative", [("Marilyn S. John", "REP"), ("Colton Stidam", "DEM")], detail="76th District", src=S)
    c.contest("appeals-5", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Matthew George", "REP")], detail="5th District · term commencing February 9, 2027", src=S)

    # --- County offices ---
    c.contest("commissioner", "County offices", "County Commissioner", [("Mark Kaufmann", "DEM"), ("Cliff Mears", "REP")], detail="Term commencing January 1, 2027", src=S)
    c.contest("auditor", "County offices", "County Auditor", [("Patrick W. Dropsey", "REP")], detail="Term commencing March 8, 2027", src=S)
    c.contest("clerk-of-courts", "County offices", "Clerk of the Court of Common Pleas", [("Heidi Ewing", "REP")], detail="Unexpired term ending December 31, 2028", src=S)
    NP = " · no party label on the ballot"
    for id, office, date, cs in [
        ("cp-gen", "General Division", "Term commencing February 9, 2027", ["Phillip S. Naumoff"]),
        ("cp-probate", "Probate Division", "Term commencing February 9, 2027", ["Kelly L. Badnell", "Robert A. Franco"]),
    ]:
        c.contest(id, "Court of Common Pleas", f"Judge of the Court of Common Pleas, {office}", cs, detail=date + NP, src=S)

    # --- Municipal issues (listed in the notice's order) ---
    # Galion's Richland County part is precinct Sandusky (split 3); the voter file has no Galion City place, so it is shown for Sandusky Township.
    GAL = P("SANDUSKY TWP")
    GAL_AREA = "City of Galion, Richland County part (precinct Sandusky, split 3)"
    c.issue("galion-council-president-term", "question", "City of Galion (Crawford and Richland counties)", "Change the term of the President of Council from 2 years to 4 years",
            GAL, area=GAL_AREA, text="Change of term: President of Council, from 2 years to 4 years.", src=S)
    c.issue("galion-council-at-large-term", "question", "City of Galion (Crawford and Richland counties)", "Change the terms of at-large members of Council from 2 years to 4 years",
            GAL, area=GAL_AREA, text="Change the terms of office for at-large members of Council from 2 years to 4 years.", src=S)
    SH = P("SHELBY CITY"); SH_AREA = "Shelby 1-A, 1-B, 2-A, 2-B, 3-A, 3-B, 4-A, 4-B"
    c.levy("shelby-health", "City of Shelby", SH, "Renewal", "General operation of the Shelby Department of Health.", "0.9 mill", "5 years, commencing in 2027", "2028", area=SH_AREA, src=S)
    c.levy("shelby-parks", "City of Shelby", SH, "Renewal", "General operation of the Shelby Parks Department.", "0.5 mill", "5 years, commencing in 2027", "2028", area=SH_AREA, src=S)
    BV = P("BELLVILLE VILLAGE")
    c.levy("bellville-cemetery", "Village of Bellville", BV, "Renewal", "Maintaining and operating the village cemetery.", "2 mills", "5 years, commencing in 2027", "2028",
           area="Bellville (precinct Jefferson A)", src=S)
    c.levy("bellville-police", "Village of Bellville", BV, "Renewal",
           "Police department: motor vehicles, communications, equipment and buildings; salaries of police, communications and administrative personnel; ambulance or emergency medical services operated by the police department; and related costs.",
           "3 mills", "5 years, commencing in 2027", "2028", area="Bellville (precinct Jefferson A)", src=S)
    c.levy("lexington-parks", "Village of Lexington", P("LEXINGTON VILLAGE"), "Renewal", "Parks and recreational purposes.", "1 mill", "5 years, commencing in 2027", "2028",
           area="Lexington B, C, E", src=S)
    c.issue("lucas-income-tax", "question", "Village of Lucas", "Municipal income tax: additional 0.75%", P("LUCAS VILLAGE"), area="Lucas (precinct Monroe A, split 2)",
            text="Additional 0.75 per cent income tax for general municipal operations, maintenance, new equipment, extension and enlargement of municipal services and facilities, "
                 "and capital improvements. The notice gives the start as January 1, 2026.", src=S)
    c.levy("plymouth-cemetery", "Village of Plymouth (Richland and Huron counties)", P("PLYMOUTH VILLAGE"), "Renewal", "Operating and maintaining the village cemetery.", "1 mill",
           "5 years, commencing in 2027", "2028", area="Plymouth, Richland County part (precinct Plymouth, split 3)", src=S)
    c.levy("shiloh-current", "Village of Shiloh", P("SHILOH VILLAGE"), "Renewal", "Current expenses.", "2.5 mills", "5 years, commencing in 2026", "2027",
           area="Shiloh (precinct Cass, split 2)", src=S)

    # --- Township issues ---
    c.levy("jefferson-twp-roads", "Jefferson Township (excluding the Village of Bellville)", P("JEFFERSON TWP"), "Renewal", "Construction, reconstruction, resurfacing and repair of township roads and bridges.",
           "2 mills", "5 years, commencing in 2027", "2028", area="Jefferson Township C, D", src=S)
    # The notice also puts Mansfield 1-D splits 1 and 7 in the Madison Township issues; the township's parts of that precinct are coded to Mansfield in the voter file.
    MAD = P("MADISON TWP", "MANSFIELD CITY")
    MAD_AREA = "Madison Township A, D, E, G, I, O, plus Mansfield 1-D (splits 1 and 7)"
    c.levy("madison-twp-fire", "Madison Township", MAD, "Additional",
           "Fire protection and emergency medical services: fire apparatus and equipment, buildings and sites, fire alarm lines, firefighting and EMS personnel, ambulance equipment and services, and related costs.",
           "2.5 mills", "5 years, commencing in 2026", "2027", area=MAD_AREA, src=S)
    c.levy("madison-twp-roads", "Madison Township", MAD, "Additional", "Construction, reconstruction, resurfacing and repair of streets, roads and bridges.", "4 mills",
           "5 years, commencing in 2026", "2027", area=MAD_AREA, src=S)
    c.issue("madison-twp-gas-aggregation", "question", "Madison Township", "Natural gas aggregation (opt-out)", MAD, area=MAD_AREA,
            text="Shall the Township of Madison have the authority to aggregate the retail natural gas loads located in the township, and enter into service agreements for the sale and "
                 "purchase of natural gas, such aggregation to occur automatically except where any person elects to opt out?", src=S)
    c.issue("mifflin-twp-gas-aggregation", "question", "Mifflin Township", "Natural gas aggregation (opt-out), unincorporated area", P("MIFFLIN TWP"), area="Mifflin Township A–E",
            text="Shall the Township of Mifflin have the authority to aggregate the retail natural gas loads located in the unincorporated areas of the township, and for that purpose, "
                 "enter into service agreements to facilitate for those loads the sale and purchase of natural gas, such aggregation to occur automatically for eligible local utility "
                 "customers except where any person is under contract or elects to opt out?", src=S)
    c.levy("monroe-twp-roads", "Monroe Township (excluding the Village of Lucas)", P("MONROE TWP"), "Renewal", "Construction, reconstruction, resurfacing and repair of roads and bridges.",
           "0.75 mill", "5 years, commencing in 2027", "2028", area="Monroe Township A (splits 1 and 3), B", src=S)
    c.levy("sandusky-twp-roads", "Sandusky Township (excluding the Village of Crestline and the City of Galion)", P("SANDUSKY TWP"), "Renewal",
           "Construction, reconstruction, resurfacing and repair of township roads and bridges.", "1.5 mills", "5 years, commencing in 2027", "2028",
           area="Sandusky Township (splits 2, 4 and 5)", src=S)

    # --- School districts ---
    c.levy("ashland-csd-current", "Ashland City School District (Ashland and Richland counties)", SD("ASHLAND CITY SD"), "Renewal", "Current expenses.", "9.9 mills",
           "Continuing, commencing in 2027", "2028", area="Ashland City School District, Richland County part (precinct Mifflin A, split 1)", src=S)
    c.issue("crestline-evsd-income-tax", "question", "Crestline Exempted Village School District (Crawford and Richland counties)",
            "School district income tax: additional 0.75%, continuing, for current expenses", SD("CRESTLINE EX VILL SD (CRAWFORD)"),
            area="Crestline Exempted Village School District, Richland County part (precinct Sandusky, splits 1 and 2)",
            text="Additional income tax of 0.75% for a continuing period of time, commencing January 1, 2027, for current expenses.", src=S)
    LEX = SD("LEXINGTON LOCAL SD (RICHLAND)")
    LEX_J = "Lexington Local School District (Richland and Morrow counties)"
    LEX_AREA = "Lexington Local School District, Richland County part (parts of Mansfield 1-A, 1-B, 1-D, 1-E, 1-F; Perry; Lexington B, C, E; Troy A, B; Washington B, C, D, F)"
    c.issue("lexington-lsd-income-tax", "question", LEX_J, "School district income tax: additional 0.75%, 10 years, for current expenses", LEX, area=LEX_AREA,
            text="Additional income tax of 0.75% for 10 years, commencing January 1, 2027, for current expenses.", src=S)
    c.levy("lexington-lsd-current", LEX_J, LEX, "Renewal", "Current expenses.", "4.8 mills", "5 years, commencing in 2026", "2027", area=LEX_AREA, src=S)
    LP = SD("LOUDONVILLE-PERRYSVILLE EX VILL SD (ASHLAND)")
    LP_AREA = "Monroe Township A (split 1), B (split 1)"
    c.issue("loudonville-perrysville-bond-income-tax", "levy", "Loudonville-Perrysville Exempted Village School District (Ashland, Knox and Richland counties)",
            "School district income tax (0.25%, 30 years) and bond issue ($16,400,000)", LP, area=LP_AREA,
            levy={"type": "Income tax and bond issue", "purpose": "Income tax for current expenses; bonds for constructing, renovating, repairing, expanding, furnishing and equipping school facilities and improving their sites.",
                  "mills": "2.85 mills (bond, estimated average)", "term": "Income tax 30 years from January 1, 2027; bonds up to 37 years", "firstDue": "2028",
                  "estimate": "$16,400,000 principal; $100 for each $100,000 of market value (bond)"},
            text="Impose an annual income tax of 0.25% on the school district income of individuals, for a period of 30 years, beginning January 1, 2027, for the purpose of current expenses; "
                 "and issue bonds for constructing school facilities, renovating, repairing, expanding, improving, and constructing additions to school facilities, furnishing and equipping "
                 "the same, and improving the sites thereof, in the principal amount of $16,400,000, to be repaid annually over a maximum period of 37 years, and levy a property tax outside "
                 "the ten-mill limitation estimated by the county auditor to average over the bond repayment period 2.85 mills, which amounts to $100 for each $100,000 of the county "
                 "auditor's market value, to pay the annual debt charges on the bonds and on any notes issued in anticipation of those bonds.", src=S)
    c.levy("madison-lsd-current", "Madison Local School District", SD("MADISON LOCAL SD (RICHLAND)"), "Renewal", "Renewal of two existing taxes for current expenses.", "14.4 mills",
           "5 years, commencing in 2027", "2028",
           area="Madison Local School District (Madison Township A, D, E, G, I, O; Mifflin Township A–E; Washington A, D; parts of Mansfield 1-C, 1-D, 1-F, 2-F, 5-A, 5-B, 6-B, 6-E)", src=S)
    c.levy("south-central-lsd-improvements", "South Central Local School District (Huron and Richland counties)", SD("SOUTH CENTRAL LOCAL SD (HURON)"), "Renewal", "General improvements.",
           "1 mill", "5 years, commencing in 2027", "2028", area="South Central Local School District, Richland County part (Blooming Grove split 4, Butler Township split 3)", src=S)

    # --- Library (its precincts in the notice are exactly the Loudonville-Perrysville district's) ---
    c.levy("loudonville-library", "Loudonville Public Library (Ashland, Knox and Richland counties)", LP, "Renewal", "Current expenses.", "0.8 mill", "5 years, commencing in 2027", "2028",
           area=LP_AREA, src=S)

    # --- Local liquor options ---
    for id, jur, raw, prec, title, text in [
        ("liquor-mansfield-lexington-ave", "City of Mansfield", "MANSFIELD CITY", "Mansfield precinct 2-C", "Local liquor option: Lexington Ave. Drive Thru (Sunday)",
         "Sunday sale of wine and mixed beverages and spirituous liquor, off-premise sales of wine and mixed beverages and on-premise sales of spirituous liquor, by Baba 1313, Inc., dba Lexington Ave. Drive Thru, 261 Lexington Ave., Mansfield."),
        ("liquor-mansfield-kingwood", "City of Mansfield", "MANSFIELD CITY", "Mansfield precinct 4-B", "Local liquor option: Kingwood Center Gardens (Sunday)",
         "Sunday sale of wine and mixed beverages and spirituous liquor, on/off-premise sales of wine and mixed beverages and on-premise sales of spirituous liquor, by Charles Kelley King 3# Trust dba Kingwood Center Gardens, 50 N. Trimble Rd., Mansfield."),
        ("liquor-shelby-legends", "City of Shelby", "SHELBY CITY", "Shelby precinct 1-A", "Local liquor option: Legends Sports Grill & Pub (Sunday)",
         "Sunday sale of wine and mixed beverages and spirituous liquor, on/off-premise sales of wine and mixed beverages and on-premise sales of spirituous liquor, by LJR Enterprises, Inc., dba Legends Sports Grill & Pub, 63 W. Main St., Shelby."),
        ("liquor-shelby-carry-out", "City of Shelby", "SHELBY CITY", "Shelby precinct 1-B", "Local liquor option: Shelby Carry Out (Sunday)",
         "Sunday sale of wine and mixed beverages, off-premise sales, by NY Singh, LLC dba Shelby Carry Out, 116 N. Gamble St., Shelby."),
        ("liquor-shelby-vfw-291", "City of Shelby", "SHELBY CITY", "Shelby precinct 2-B", "Local liquor option: Ralph Phillips VFW 291 (Sunday)",
         "Sunday sale of wine and mixed beverages and spirituous liquor, on-premise sales, by VFW Post 0291 George Broderick dba Ralph Phillips VFW 291, 34 W. Main St., Shelby."),
    ]:
        c.issue(id, "liquor", jur, title, P(raw), area=prec, text=text, src=S)
    return c
