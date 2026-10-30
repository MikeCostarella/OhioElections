from lib import County, NOTE_ORDER, NOTE_PLACES

SITE = "https://www.boe.ohio.gov/washington/"
NOTICE = "https://www.boe.ohio.gov/washington/c/upload/FWAB_11November46Day.pdf"
BALLOTS = "https://lookup.boe.ohio.gov/vtrapp/washington/ballotlist.aspx"


def build():
    # Raw SoS names ("ADAMS TWP", "BEVERLY VILLAGE", "MARIETTA CITY") already display correctly; no renames needed.
    c = County("washington", "Washington", "39167")
    c.src("washington-46day", "Washington County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election (revised September 18, 2026)", NOTICE)
    c.src("washington-ballots", "Washington County Board of Elections: precinct sample ballots, November 3, 2026 General Election (election data updated October 5, 2026)", BALLOTS)
    S = ["washington-46day", "washington-ballots"]
    c.links = [
        {"label": "Board of Elections", "url": SITE},
        {"label": "Federal write-in absentee ballot notices", "url": "https://www.boe.ohio.gov/washington/election-info/federal-write-in-absentee-ballots"},
        {"label": "Sample ballots by precinct", "url": BALLOTS},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://www.boe.ohio.gov/washington/election-info/election-results/"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it, "
               "checked against the Board's precinct sample ballots. Issue wording is from the sample ballots.",
               NOTE_ORDER, NOTE_PLACES,
               "The Board's notice and sample ballots do not give local issue numbers.",
               "Court of Appeals: the 46-day notice lists Peter B. Abele (Republican) for the 4th District seat, but the Board's sample ballots list "
               "Jayme Hartley Fountain (Republican) and Todd L. Grace (Democratic); the sample ballots are shown here."]
    P = c.p; D = c.district

    # --- Federal, state legislative, appeals (all precincts are in the 2nd Congressional, 94th House and 4th Appeals districts) ---
    c.contest("congress-2", "U.S. House", "Representative to Congress", [("Jen Mazzuckelli", "DEM"), ("David J. Taylor", "REP")],
              detail="2nd District", places=D("cong", 2), src=S)
    c.contest("rep-94", "Ohio General Assembly", "State Representative", [("Kevin Ritter", "REP"), ("Wenda Sheard", "DEM")],
              detail="94th District", places=D("rep", 94), src=S)
    # The notice (revised 9/18/2026) lists Peter B. Abele (Rep); the sample ballots (data of 10/5/2026) list Fountain and Grace.
    c.contest("appeals-4-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Jayme Hartley Fountain", "REP"), ("Todd L. Grace", "DEM")],
              detail="4th District · full term commencing February 9, 2027",
              src=["washington-ballots", "washington-46day"])

    # --- County ---
    c.contest("commissioner-0101", "County offices", "County Commissioner", [("Stephanie Lang", "REP"), ("Brian G. Whalin", "DEM")],
              detail="Full term commencing January 1, 2027", src=S)
    c.contest("commissioner-0102", "County offices", "County Commissioner", [("Justin A. Harris", "Nonparty"), ("Ronald Gregory Nohe", "REP"), ("John B. Rauch", "DEM")],
              detail="Unexpired term ending January 1, 2029", src=S)
    c.contest("auditor", "County offices", "County Auditor", [("Matthew Livengood", "REP")],
              detail="Full term commencing March 2, 2027", src=S)
    c.contest("prosecutor", "County offices", "Prosecuting Attorney", [("Joseph Patrick Derkin", "REP")],
              detail="Unexpired term ending December 31, 2028", src=S)
    NP = " · no party label on the ballot"
    # The notice tags Nicole Tipton Coil "(Rep)"; the sample ballot prints no party for Common Pleas judges.
    for id, office, date, cs in [
        ("cp-unexpired", "Judge of the Court of Common Pleas, General Division", "Unexpired term ending December 31, 2028", ["Nicole Tipton Coil"]),
        ("cp-probate-juvenile", "Judge of the Court of Common Pleas, Probate/Juvenile Division", "Full term commencing February 9, 2027", ["Timothy A. Williams"]),
    ]:
        c.contest(id, "Court of Common Pleas", office, cs, detail=date + NP, src=S)

    # --- Issues (unnumbered; listed in the notice's order) ---
    est = lambda total, per: f"{total} a year; {per} for each $100,000 of market value"
    c.levy("county-library", "Washington County Public Library", "county", "Additional", "Current expenses of the library.", "0.5 mill",
           "10 years, commencing in 2026", "2027", est("$1,140,880", "$18"), area="Countywide", src=S)
    c.levy("county-mental-health", "Washington County", "county", "Renewal",
           "Essential prevention, treatment, and recovery programs for children, adolescents, and adults at risk for mental illness and substance use disorders.",
           "0.5 mill", "5 years, commencing in 2027", "2028", est("$815,668", "$18"), area="Countywide", src=S)
    c.levy("county-911", "Washington County", "county", "Renewal", "Operation of a 911 system.", "0.35 mill",
           "5 years, commencing in 2026", "2027", est("$539,124", "$12"), area="Countywide", src=S)
    c.levy("newport-twp-fire", "Newport Township", P("NEWPORT TWP"), "Renewal", "Fire and emergency protection.", "3 mills",
           "5 years, commencing in 2027", "2028", est("$123,641", "$105"), area="Newport precincts 0045/1 and 0045/2", src=S)
    c.levy("watertown-twp-fire", "Watertown Township", P("WATERTOWN TWP"), "Renewal", "Fire protection, ambulance and emergency medical services.", "1.5 mills",
           "5 years, commencing in 2027", "2028", est("$49,851", "$53"), area="Watertown precincts 0055/1 and 0055/2",
           note="The sample ballot gives $53 for each $100,000 of market value; the 46-day notice gives $52.", src=S)
    c.levy("wesley-twp-fire", "Wesley Township", P("WESLEY TWP"), "Renewal", "Fire protection, ambulance and emergency medical services.", "4 mills",
           "5 years, commencing in 2027", "2028", est("$101,567", "$140"), area="Wesley precincts 0056/1 and 0056/2", src=S)
    # The notice lists "0052 - All Splits"; only the Beverly Village split (0052/1) has the question on its sample ballot.
    c.issue("liquor-beverly-legion-sunday", "liquor", "Village of Beverly", "Local liquor option: American Legion Post 389 (Sunday sales, D-4 permit)",
            P("BEVERLY VILLAGE"), area="Beverly Village precinct Beverly/Waterford 0052/1",
            text="Shall the sale of wine and mixed beverages and spirituous liquor be permitted for sale on Sunday by The American Legion, Post 389 "
                 "a holder of a D-4 liquor permit who is engaged in the business of a private veterans' membership club at 114 Fifth St, Beverly, OH 45715 "
                 "in this precinct? (by petition)", src=S)
    return c
