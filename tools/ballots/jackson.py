from lib import County, NOTE_ORDER, NOTE_PLACES

SITE = "https://www.boe.ohio.gov/jackson/"
NOTICE = "https://www.boe.ohio.gov/jackson/c/upload/FWAB_11November46Day.pdf"
BALLOTS = "https://lookup.boe.ohio.gov/vtrapp/jackson/ballotlist.aspx"


def build():
    # Raw SoS names ("BLOOMFIELD TWP", "JACKSON CITY", "OAK HILL VILLAGE") already display correctly.
    c = County("jackson", "Jackson", "39079")
    c.src("jackson-46day", "Jackson County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election (revised October 15, 2026)", NOTICE)
    c.src("jackson-ballots", "Jackson County Board of Elections: precinct sample ballots, November 3, 2026 General Election (election data updated October 6, 2026)", BALLOTS)
    S = ["jackson-46day", "jackson-ballots"]
    B = ["jackson-ballots", "jackson-46day"]
    c.links = [
        {"label": "Board of Elections", "url": SITE},
        {"label": "Federal write-in absentee ballot notices", "url": "https://www.boe.ohio.gov/jackson/election-info/federal-write-in-absentee-ballots/"},
        {"label": "Sample ballots by precinct", "url": BALLOTS},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://www.boe.ohio.gov/jackson/election-info/election-results/"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it, "
               "checked against the Board's precinct sample ballots. Issue wording is from the sample ballots and matches the notice.",
               NOTE_ORDER, NOTE_PLACES,
               "The Board's notice and sample ballots do not give local issue numbers.",
               "Court of Appeals: Peter B. Abele (Republican) is still printed on the sample ballots for the 4th District seat; the Board's notice "
               "(revised October 15, 2026) says votes for him will not be counted due to his death and lists the replacement candidates certified "
               "October 5, 2026, Jayme Hartley Fountain (Republican) and Todd L. Grace (Democratic), as shown here."]
    P = c.p; D = c.district

    # --- Federal, state legislative, appeals (every precinct is in the 2nd Congressional, 17th Senate, 93rd House and 4th Appeals districts) ---
    c.contest("congress-2", "U.S. House", "Representative to Congress", [("Jen Mazzuckelli", "DEM"), ("David J. Taylor", "REP")],
              detail="2nd District", places=D("cong", 2), src=S)
    c.contest("senate-17", "Ohio General Assembly", "State Senator", [("Brian A. Deer", "DEM"), ("Shane Wilkin", "REP")],
              detail="17th District", places=D("sen", 17), src=S)
    c.contest("rep-93", "Ohio General Assembly", "State Representative", [("Jessica Harper", "DEM"), ("Jason Stephens", "REP")],
              detail="93rd District", places=D("rep", 93), src=S)
    # The sample ballots (data of 10/6/2026) still list Peter B. Abele; the notice (revised 10/15/2026) marks him dead and lists the
    # replacement candidates certified 10/5/2026, as in Ross, Scioto, Athens and Lawrence.
    c.contest("appeals-4-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Jayme Hartley Fountain", "REP"), ("Todd L. Grace", "DEM")],
              detail="4th District · full term commencing February 9, 2027", src=S)

    # --- County ---
    c.contest("commissioner", "County offices", "County Commissioner", [("Jon Hensler", "REP")],
              detail="Full term commencing January 1, 2027", src=S)
    c.contest("auditor", "County offices", "County Auditor", [("Tiffany Ridgeway", "REP")],
              detail="Full term commencing March 8, 2027", src=S)
    c.contest("prosecutor", "County offices", "Prosecuting Attorney", [("Trenton Brown Douthett", "REP")],
              detail="Unexpired term ending December 31, 2028", src=S)
    NP = " · no party label on the ballot"
    c.contest("cp-probate-juvenile", "Court of Common Pleas", "Judge of the Court of Common Pleas, Probate/Juvenile Division", ["Justin W. Skaggs"],
              detail="Full term commencing February 9, 2027" + NP, src=S)

    # --- Issues (unnumbered; listed in the notice's order) ---
    c.levy("liberty-fire", "Liberty Township", P("LIBERTY TWP"), "Renewal",
           "Providing and maintaining fire apparatus, appliances, buildings or sites therefor for fire protection.", "1.5 mills",
           "5 years, commencing in 2027", "2028", "$75,576 a year; $125 for each $100,000 of market value",
           area="Liberty 1 and Liberty 2 precincts", src=B)
    c.issue("liquor-stockroom-601", "liquor", "City of Jackson", "Local liquor option: Stockroom 601 (D-6 permit, Sunday sales)", P("JACKSON CITY"),
            area="Jackson City precinct Jackson 1-A",
            text="Shall the sale of wine and mixed beverages and spirituous liquor be permitted for sale on Sunday by AAC Mgmt., L.L.C., dba Stockroom 601 "
                 "an applicant for a D-6 liquor permit who is engaged in the business of operating a restaurant/bar at 601 E. Main St, Jackson, OH 45640 "
                 "in this precinct?", src=B)
    c.issue("liquor-amvets-84", "liquor", "City of Jackson", "Local liquor option: Amvets Post 84 (D-6 permit, Sunday sales)", P("JACKSON CITY"),
            area="Jackson City precinct Jackson 3-A",
            text="Shall the sale of wine and mixed beverages and spirituous liquor be permitted for sale on Sunday by Amvets Post 84 Jackson, dba Amvets Post 84 "
                 "an applicant for a D-6 liquor permit who is engaged in the business of operating a fraternal organization at 208 Broadway St, Jackson, OH 45640 "
                 "in this precinct?", src=B)
    return c
