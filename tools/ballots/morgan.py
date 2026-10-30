from lib import County, NOTE_ORDER, NOTE_PLACES

SITE = "https://www.boe.ohio.gov/morgan/"
NOTICE = "https://www.boe.ohio.gov/morgan/c/upload/FWAB_11November46Day.pdf"
BALLOTS = "https://lookup.boe.ohio.gov/vtrapp/morgan/ballotlist.aspx"

# Precincts (from the sample-ballot list): 01 East Bloom, 02 W. Bloom/Deerfield, 03 Bristol/Manchester, 04 Center,
# 05 Homer/Union, 06 Malta, 07/1 Chesterhill, 07/2 Marion, 08 Meigsville, 09/1 McConnelsville A, 09/2 Morgan,
# 10/1-10/2 McConnelsville B and C, 11 Penn, 12/1 Stockport, 12/2 Windsor, 13 York.


def build():
    # Raw SoS names ("BLOOM TOWNSHIP", "MCCONNELSVILLE VILLAGE") already display correctly; no renames needed.
    c = County("morgan", "Morgan", "39115")
    c.src("morgan-46day", "Morgan County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election", NOTICE)
    c.src("morgan-ballots", "Morgan County Board of Elections: precinct sample ballots, November 3, 2026 General Election (election data updated September 8, 2026)", BALLOTS)
    S = ["morgan-46day", "morgan-ballots"]
    c.links = [
        {"label": "Board of Elections", "url": SITE},
        {"label": "Federal write-in absentee ballot notices", "url": "https://www.boe.ohio.gov/morgan/election-info/federal-write-in-absentee-ballots/"},
        {"label": "Sample ballots by precinct", "url": BALLOTS},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://www.boe.ohio.gov/morgan/election-info/election-results/"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it, "
               "checked against the Board's precinct sample ballots. Issue wording is from the sample ballots.",
               NOTE_ORDER, NOTE_PLACES,
               "The Board's notice and sample ballots do not give local issue numbers.",
               "Court of Appeals: the 46-day notice lists Matt Donahue (Republican) for the 5th District seat, but the Board's sample ballots list "
               "Matthew George (Republican); the sample ballots are shown here."]
    P = c.p; D = c.district

    # --- Federal, state legislative, appeals (countywide: 2nd Congressional, 95th House, 5th Appeals; no State Senate race) ---
    c.contest("congress-2", "U.S. House", "Representative to Congress", [("Jen Mazzuckelli", "DEM"), ("David J. Taylor", "REP")],
              detail="2nd District", places=D("cong", 2), src=S)
    c.contest("rep-95", "Ohio General Assembly", "State Representative", [("Paul Cameron", "DEM"), ("Ty Moore", "REP")],
              detail="95th District", places=D("rep", 95), src=S)
    # The notice lists "Matt Donahue (Rep)"; the sample ballots (and every other 5th District county) list Matthew George.
    c.contest("appeals-5", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Matthew George", "REP")],
              detail="5th District · term commencing February 9, 2027", src=["morgan-ballots", "morgan-46day"])

    # --- County offices ---
    c.contest("commissioner", "County offices", "County Commissioner", [("Cecil Mayle", "REP")], detail="Full term commencing January 1, 2027", src=S)
    c.contest("auditor", "County offices", "County Auditor", [("Randy Williams", "REP")], src=S)
    NP = " · no party label on the ballot"
    # The notice and sample ballot tag John A. Wells "Republican" (he is printed with a party on the sample ballot);
    # Common Pleas judges are shown without party per the data conventions.
    c.contest("cp", "Court of Common Pleas", "Judge of the Court of Common Pleas", ["John A. Wells"],
              detail="Full term commencing February 9, 2027" + NP, src=S)

    # --- Issues (unnumbered; listed in the notice's order) ---
    est = lambda total, per: f"{total} a year; {per} for each $100,000 of the county auditor's market value"
    c.levy("mcconnelsville-streets", "Village of McConnelsville", P("MCCONNELSVILLE VILLAGE"), "Renewal",
           "Resurfacing and repair of streets and alleys within the Village of McConnelsville.", "2 mills",
           "5 years, commencing in 2027", "2028", est("$22,958", "$70"), area="McConnelsville precincts A (09/1), B (10/1), C (10/2)", src=S)
    CH = "Chesterhill (precinct 07/1)"
    for id, title, text in [
        ("liquor-rons-auto", "Local liquor option: Ron's Auto & Convenience Center (D-5 permit)",
         "Shall the sale of beer, wine and mixed beverages/spirituous liquor be permitted by DBA Ron's Auto & Convenience Center, an applicant for a D-5 liquor permit, "
         "who is engaged in the business of Convenience Store/Restaurant at 7400 Marion St., Chesterhill, OH 43728 in this precinct?"),
        ("liquor-rons-auto-sunday", "Local liquor option: Ron's Auto & Convenience Center (D-5 permit, Sunday)",
         "Shall the sale of beer, wine and mixed beverages/spirituous liquor be permitted for sale on Sunday by DBA Ron's Auto & Convenience Center, an applicant for a D-5 liquor permit, "
         "who is engaged in the business of Convenience Store/Restaurant at 7400 Marion St., Chesterhill, OH 43728 in this precinct?"),
    ]:
        c.issue(id, "liquor", "Village of Chesterhill", title, P("CHESTERHILL VILLAGE"), area=CH, text=text, src=S)
    c.levy("windsor-fire", "Windsor Township", P("WINDSOR TOWNSHIP"), "Renewal", "Fire protection.", "1 mill",
           "5 years, commencing in 2027", "2028", est("$23,843", "$35"), area="Windsor Township precinct 12/2", src=S)
    c.levy("center-fire", "Center Township", P("CENTER TOWNSHIP"), "Additional", "Fire protection.", "1 mill",
           "5 years, commencing in 2026", "2027", est("$44,500", "$35"), area="Center Township precinct 04/1", src=S)
    c.levy("chesterhill-fire", "Village of Chesterhill", P("CHESTERHILL VILLAGE"), "Renewal", "Fire protection.", "2 mills",
           "5 years, commencing in 2027", "2028", est("$6,802", "$70"), area=CH, src=S)
    # Notice: 5 years; sample ballot: 3 years. The sample ballot is shown.
    c.levy("meigsville-fire", "Meigsville Township", P("MEIGSVILLE TOWNSHIP"), "Renewal", "Fire protection.", "0.6 mill",
           "3 years, commencing in 2027", "2028", est("$7,645", "$21"), area="Meigsville Township precinct 08/1", src=S,
           note="The Board's 46-day notice gives this levy's term as 5 years; the sample ballot (shown here) says 3 years.")
    # Precinct 07/2 is Marion Township outside Chesterhill. Notice estimate $10,077; sample ballot $10,770 (shown).
    c.levy("marion-fire", "Marion Township", P("MARION TOWNSHIP"), "Renewal", "Fire protection.", "1 mill",
           "5 years, commencing in 2027", "2028", est("$10,770", "$35"), area="Marion Township precinct 07/2 (outside Chesterhill)", src=S,
           note="The Board's 46-day notice gives the annual estimate as $10,077; the sample ballot (shown here) says $10,770.")
    c.levy("stockport-streets", "Village of Stockport", P("STOCKPORT VILLAGE"), "Renewal", "Street maintenance within the Village of Stockport.", "2 mills",
           "5 years, commencing in 2027", "2028", est("$17,118", "$70"), area="Stockport precinct 12/1", src=S)
    for id, title, text in [
        ("liquor-triple-nickel", "Local liquor option: Triple Nickel Diner (D-3 permit)",
         "Shall the sale of spirituous liquor be permitted by Triple Nickel Diner LLC, an applicant for a D-3 liquor permit, who is engaged in the business of "
         "operating a restaurant at 1060 High St. Chesterhill, OH 43728 in this precinct?"),
        ("liquor-triple-nickel-sunday", "Local liquor option: Triple Nickel Diner (D-6 permit, Sunday)",
         "Shall the sale of beer, wine and mixed beverages and spirituous liquor be permitted for sale on Sunday by Triple Nickel Diner LLC an applicant for a D-6 liquor permit "
         "and an applicant for or holder of a D-1, D-2, and D-3 liquor permit who is engaged in the business of operating a restaurant at 1060 High St. Chesterhill, OH 43728 in this precinct?"),
    ]:
        c.issue(id, "liquor", "Village of Chesterhill", title, P("CHESTERHILL VILLAGE"), area=CH, text=text, src=S)
    return c
