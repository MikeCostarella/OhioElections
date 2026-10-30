from lib import County, NOTE_ORDER, NOTE_PLACES

SITE = "https://www.boe.ohio.gov/meigs/"
NOTICE = "https://www.boe.ohio.gov/meigs/c/upload/FWAB_11November46Day.pdf"
BALLOTS = "https://lookup.boe.ohio.gov/vtrapp/meigs/ballotlist.aspx"


def build():
    # Raw SoS names ("BEDFORD TOWNSHIP", "MIDDLEPORT VILLAGE", "RUTLAND VILLAGE") already display correctly.
    c = County("meigs", "Meigs", "39105")
    c.src("meigs-46day", "Meigs County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election (revised October 5, 2026)", NOTICE)
    c.src("meigs-ballots", "Meigs County Board of Elections: precinct sample ballots, November 3, 2026 General Election (election data updated October 5, 2026)", BALLOTS)
    S = ["meigs-46day", "meigs-ballots"]
    B = ["meigs-ballots", "meigs-46day"]
    c.links = [
        {"label": "Board of Elections", "url": SITE},
        {"label": "Federal write-in absentee ballot notices", "url": "https://www.boe.ohio.gov/meigs/election-info/federal-write-in-absentee-ballots/"},
        {"label": "Sample ballots by precinct", "url": BALLOTS},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://www.boe.ohio.gov/meigs/election-info/election-results/"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it, "
               "checked against the Board's precinct sample ballots. Parties, terms of office and issue wording are from the sample ballots.",
               NOTE_ORDER, NOTE_PLACES,
               "The Board's notice and sample ballots do not give local issue numbers.",
               "Racine Village: the sample ballot for the Racine Village precinct carries an additional 3-mill operating levy for the village "
               "that the 46-day notice (revised October 5, 2026) does not list; it is included here from the sample ballot."]
    P = c.p; D = c.district

    # --- Federal, state legislative, appeals (every precinct is in the 2nd Congressional, 94th House and 4th Appeals districts;
    #     the 30th Senate seat is not up this year) ---
    c.contest("congress-2", "U.S. House", "Representative to Congress", [("Jen Mazzuckelli", "DEM"), ("David J. Taylor", "REP")],
              detail="2nd District", places=D("cong", 2), src=S)
    c.contest("rep-94", "Ohio General Assembly", "State Representative", [("Kevin Ritter", "REP"), ("Wenda Sheard", "DEM")],
              detail="94th District", places=D("rep", 94), src=S)
    # Both the notice (revised 10/5/2026) and the sample ballots already list the replacement candidates for Peter B. Abele (died).
    c.contest("appeals-4-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Jayme Hartley Fountain", "REP"), ("Todd L. Grace", "DEM")],
              detail="4th District · full term commencing February 9, 2027", src=S)

    # --- County ---
    c.contest("commissioner", "County offices", "County Commissioner", [("Zachary B. Manuel", "REP")],
              detail="Full term commencing January 1, 2027", src=S)
    # The ballot gives no term for the auditor; the notice gives "Full 4 Year Term Commencing 03/08/2027".
    c.contest("auditor", "County offices", "County Auditor", [("Mary T. Byer-Hill", "REP")],
              detail="Full term commencing March 8, 2027", src=S)
    c.contest("treasurer", "County offices", "County Treasurer", [("Tonya M. Griffin", "REP")],
              detail="Unexpired term ending September 2, 2029", src=S)
    # As in Gallia, the sample ballots print "Republican" under Jeremy L. Fisher; following the Common Pleas convention he carries
    # no party tag here, and the detail says what the ballot shows.
    c.contest("cp-probate-juvenile", "Court of Common Pleas", "Judge of the Court of Common Pleas, Probate/Juvenile Division", ["Jeremy L. Fisher"],
              detail="Full term commencing February 8, 2027 · the ballot prints a Republican party label for this race", src=B)

    # --- Issues (unnumbered; listed in the notice's order) ---
    est = lambda total, per: f"{total} a year; {per} for each $100,000 of market value"
    c.levy("county-senior-citizens", "Meigs County", "county", "Renewal",
           "Providing and maintaining senior citizens services or facilities (Meigs County Council on Aging, Inc. Multipurpose Senior Citizens Center).",
           "1.6 mills", "5 years, commencing in 2027", "2028", est("$707,324", "$55"), src=B)
    c.levy("county-dd", "Meigs County", "county", "Additional",
           "Maintenance, capital construction, and operation for persons with cognitive and other developmental disabilities of the Meigs County Board of Developmental Disabilities.",
           "2 mills", "5 years, commencing in 2027", "2028", est("$1,201,518", "$70"), src=B)
    c.levy("county-sheriff", "Meigs County", "county", "Additional",
           "Operating the Office of the Sheriff, including motor vehicles, communications and other equipment, buildings and sites, and the salaries of "
           "deputies, communications and administrative personnel, and other related operating costs.",
           "2.88 mills", "Continuing, commencing in 2026", "2027", est("$1,730,186", "$100.80"), src=B)
    c.levy("bedford-twp-fire", "Bedford Township", P("BEDFORD TOWNSHIP"), "Additional", "Fire protection and other emergency services.",
           "0.5 mill", "5 years, commencing in 2026", "2027", est("$17,676", "$17"), area="Bedford precincts", src=B)
    c.levy("chester-twp-roads", "Chester Township", P("CHESTER TOWNSHIP"), "Renewal", "Road improvement.",
           "1 mill", "5 years, commencing in 2027", "2028", est("$63,657", "$35"), area="East Chester and West Chester precincts", src=B)
    c.issue("alexander-lsd-income-tax", "question", "Alexander Local School District (Athens, Meigs and Vinton)",
            "School district income tax: 0.75 percent, 5 years, current expenses", c.sd("ALEXANDER LOCAL SD (ATHENS)"), area="Columbia precinct",
            text="Shall an annual income tax of 0.75 percent on the earned income of individuals residing in the school district be imposed by Alexander Local School District, "
                 "for 5 years, beginning January 1, 2027, for the purpose of current expenses?", src=B)
    c.levy("columbia-twp-fire", "Columbia Township", P("COLUMBIA TOWNSHIP"), "Additional", "Construction and structural improvement for the Fire Department.",
           "5 mills", "5 years, commencing in 2026", "2027", est("$247,707", "$175"), area="Columbia precinct", src=B)
    c.levy("lebanon-twp-roads", "Lebanon Township", P("LEBANON TOWNSHIP"), "Renewal", "Road maintenance.",
           "1.5 mills", "5 years, commencing in 2026", "2027", est("$36,788", "$53"), area="Lebanon precincts", src=B)
    c.levy("olive-twp-cemeteries", "Olive Township", P("OLIVE TOWNSHIP"), "Renewal", "Maintaining and operating cemeteries.",
           "1 mill", "5 years, commencing in 2026", "2027", est("$14,293", "$35"), area="North Olive and South Olive precincts", src=B)
    # Rutland Village (its own precinct) votes on the Rutland Township levies.
    RUT = P("RUTLAND TOWNSHIP", "RUTLAND VILLAGE"); RUT_A = "Rutland Village, East Rutland and West Rutland precincts"
    c.levy("rutland-twp-cemeteries", "Rutland Township (including Rutland Village)", RUT, "Renewal", "Maintaining and operating cemeteries.",
           "1 mill", "5 years, commencing in 2027", "2028", est("$21,133", "$35"), area=RUT_A, src=B)
    c.levy("rutland-twp-roads", "Rutland Township (including Rutland Village)", RUT, "Renewal", "Road maintenance.",
           "2.16 mills", "5 years, commencing in 2026", "2027", est("$44,153", "$76"), area=RUT_A, src=B)
    SAL = P("SALEM TOWNSHIP")
    c.levy("salem-twp-fire", "Salem Township", SAL, "Renewal", "Fire Department maintenance.",
           "1 mill", "5 years, commencing in 2026", "2027", est("$21,020", "$35"), area="Salem precinct", src=B)
    c.levy("salem-twp-roads", "Salem Township", SAL, "Renewal", "Road maintenance.",
           "2.92 mills", "5 years, commencing in 2026", "2027", est("$77,391", "$102"), area="Salem precinct", src=B)
    MID = P("MIDDLEPORT VILLAGE"); MID_A = "Middleport 2nd, 3rd and 4th precincts"
    c.levy("middleport-current-expenses", "Middleport Village", MID, "Additional", "Current expenses.",
           "3 mills", "5 years, commencing in 2027", "2028", est("$82,569", "$105"), area=MID_A, src=B)
    c.levy("middleport-fire", "Middleport Village", MID, "Additional", "Fire levy.",
           "2 mills", "5 years, commencing in 2027", "2028", est("$55,046", "$70"), area=MID_A, src=B)
    RAC = P("RACINE VILLAGE")
    # On the Racine Village sample ballot only; not in the 46-day notice (see notes).
    c.levy("racine-operating", "Racine Village", RAC, "Additional", "Additional expense operating levy.",
           "3 mills", "5 years, commencing in 2026", "2027", est("$33,112", "$105"), area="Racine Village precinct", src=["meigs-ballots"])
    SIK = "Stephanie Sikorski D.B.A. Sikorski's Riverway Grill, an applicant for a D-5 liquor permit, who is engaged in the business of restaurant at 301 3rd St., Racine (Racine Village), Oh 45771"
    c.issue("liquor-sikorskis-racine", "liquor", "Racine Village", "Local liquor option: Sikorski's Riverway Grill (D-5 permit)", RAC,
            area="Racine Village precinct",
            text=f"Shall the sale of beer, wine, mixed beverages and spirituous liquor be permitted by {SIK} in this precinct?", src=B)
    c.issue("liquor-sikorskis-racine-sunday", "liquor", "Racine Village", "Local liquor option: Sikorski's Riverway Grill (Sunday sales)", RAC,
            area="Racine Village precinct",
            text=f"Shall the sale of beer, wine, mixed beverages and spirituous liquor be permitted for sale on Sunday by {SIK} in this precinct?", src=B)
    c.levy("syracuse-fire", "Syracuse Village", P("SYRACUSE VILLAGE"), "Renewal", "Fire protection.",
           "1 mill", "5 years, commencing in 2027", "2028", est("$10,139", "$35"), area="Syracuse Village precinct", src=B)
    return c
