from lib import County, NOTE_ORDER, NOTE_PLACES

SITE = "https://www.boe.ohio.gov/vinton/"
NOTICE = "https://www.boe.ohio.gov/vinton/c/upload/FWAB_11November46Day.pdf"
BALLOTS = "https://lookup.boe.ohio.gov/vtrapp/vinton/ballotlist.aspx"


def build():
    # Raw SoS names ("ELK TOWNSHIP", "MCARTHUR VILLAGE", "ZALESKI VILLAGE") already display correctly; no renames needed.
    c = County("vinton", "Vinton", "39163")
    c.src("vinton-46day", "Vinton County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election (revised September 18, 2026)", NOTICE)
    c.src("vinton-ballots", "Vinton County Board of Elections: precinct sample ballots, November 3, 2026 General Election (election data updated October 5, 2026)", BALLOTS)
    S = ["vinton-46day", "vinton-ballots"]
    B = ["vinton-ballots", "vinton-46day"]
    c.links = [
        {"label": "Board of Elections", "url": SITE},
        {"label": "Federal write-in absentee ballot notices", "url": "https://www.boe.ohio.gov/vinton/election-info/federal-write-in-absentee-ballots/"},
        {"label": "Sample ballots by precinct", "url": BALLOTS},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://www.boe.ohio.gov/vinton/election-info/election-results/"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it, "
               "checked against the Board's precinct sample ballots. Issue wording is from the sample ballots.",
               NOTE_ORDER, NOTE_PLACES,
               "The Board's notice and sample ballots do not give local issue numbers.",
               "Court of Appeals: the 46-day notice (revised September 18, 2026) lists Peter B. Abele for the 4th District seat, but the Board's "
               "sample ballots list Jayme Hartley Fountain (Republican) and Todd L. Grace (Democratic); the sample ballots are shown here."]
    P = c.p; D = c.district; SD = c.sd

    # --- Federal, state legislative, appeals (every precinct is in the 2nd Congressional, 17th Senate, 92nd House and 4th Appeals districts) ---
    c.contest("congress-2", "U.S. House", "Representative to Congress", [("Jen Mazzuckelli", "DEM"), ("David J. Taylor", "REP")],
              detail="2nd District", places=D("cong", 2), src=S)
    c.contest("senate-17", "Ohio General Assembly", "State Senator", [("Brian A. Deer", "DEM"), ("Shane Wilkin", "REP")],
              detail="17th District", places=D("sen", 17), src=S)
    # The notice prints "Mark Glenn Johnson"; the ballots print "Mark Johnson", as in hocking.py.
    c.contest("rep-92", "Ohio General Assembly", "State Representative", [("Mark Johnson", "REP"), ("Sarah Senff", "DEM")],
              detail="92nd District", places=D("rep", 92), src=S)
    # The notice (revised 9/18/2026) lists Peter B. Abele with no party; the sample ballots (data of 10/5/2026) list Fountain and Grace.
    c.contest("appeals-4-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Jayme Hartley Fountain", "REP"), ("Todd L. Grace", "DEM")],
              detail="4th District · full term commencing February 9, 2027", src=B)

    # --- County ---
    c.contest("commissioner", "County offices", "County Commissioner", [("Steven Ray Hammond", "DEM"), ("C. Scott Ward", "REP")],
              detail="Full term commencing January 1, 2027", src=S)
    c.contest("auditor", "County offices", "County Auditor", [("Cindy Ann Waugh", "REP")],
              detail="Full term commencing March 8, 2027", src=S)
    NP = " · no party label on the ballot"
    # The notice calls it "Probate Court Judge, Juvenile Division"; the ballot title is "Judge of the Court of Common Pleas (Juvenile Division)".
    c.contest("cp-juvenile", "Court of Common Pleas", "Judge of the Court of Common Pleas, Juvenile Division", ["Jeffrey Randolph Griffith"],
              detail="Full term commencing February 9, 2027" + NP, src=B)

    # --- Township offices (one seat each; the notice heads both "Trustee (2 seats)" but says 1 to be elected, as the ballots do) ---
    c.contest("richland-trustee", "Township offices", "Township Trustee (Richland Township)", ["Travis G. Faught"],
              detail="Unexpired term ending December 31, 2029" + NP, places=P("RICHLAND TOWNSHIP"),
              area="Richland Township (precincts Richland Northwest and Richland Southeast)", src=B)
    # Matthew Ryan Carter is a certified write-in (notice); not listed.
    c.contest("swan-trustee", "Township offices", "Township Trustee (Swan Township)", ["Nathan Leland Durr", "Jerrod Loren Schorr"],
              detail="Unexpired term ending December 31, 2029" + NP, places=P("SWAN TOWNSHIP"),
              area="Swan Township (precincts Swan Township 1 and 2)", src=B)

    est = lambda total, per: f"{total} a year; {per} for each $100,000 of the county auditor's market value"

    # --- Issues (unnumbered; listed in the notice's order) ---
    c.levy("county-health", "Vinton County", "county", "Renewal",
           "Providing sufficient funds to carry out the health programs of the Vinton County health district.", "1 mill",
           "5 years, commencing in 2027", "2028", est("$457,712", "$26"), src=B)

    HAM = P("HAMDEN VILLAGE"); HAM_A = "Precincts Hamden North and Hamden South"
    c.levy("hamden-police", "Village of Hamden", HAM, "Renewal",
           "Providing and maintaining motor vehicles, communications, other equipment, buildings and sites used directly in the operation of a police department, "
           "police, communications or administrative personnel, contracted police protection, ambulance or emergency medical services operated by a police department, "
           "and other related costs.", "6 mills", "5 years, commencing in 2027", "2028", est("$34,962", "$118"), area=HAM_A, src=B)
    c.levy("hamden-fire", "Village of Hamden", HAM, "Renewal",
           "Providing and maintaining fire apparatus, mechanical resuscitators, underwater rescue and recovery equipment, appliances, buildings and sites, "
           "sources of water supply, fire-alarm communications, firefighting, emergency medical service, administrative or communications personnel, "
           "ambulance equipment and services, and other related costs.", "3 mills", "5 years, commencing in 2027", "2028", est("$22,874", "$80"), area=HAM_A, src=B)

    MCA = P("MCARTHUR VILLAGE"); MCA_A = "Precincts McArthur East, McArthur Northwest and McArthur Southwest"
    c.levy("mcarthur-operating", "Village of McArthur", MCA, "Renewal", "Current operating expenses.", "4 mills",
           "4 years, commencing in 2026", "2027", est("$69,833", "$85"), area=MCA_A, src=B)
    c.levy("mcarthur-police", "Village of McArthur", MCA, "Renewal",
           "Providing and maintaining motor vehicles, communications, other equipment, buildings and sites used directly in the operation of a police department, "
           "police, communications or administrative personnel, contracted police protection, and ambulance or emergency medical services operated by a police department.",
           "3.5 mills", "4 years, commencing in 2026", "2027", est("$61,104", "$75"), area=MCA_A, src=B)
    c.levy("mcarthur-parks", "Village of McArthur", MCA, "Renewal", "Parks and recreational purposes.", "1 mill",
           "4 years, commencing in 2026", "2027", est("$17,400", "$21"), area=MCA_A, src=B)

    c.levy("knox-roads", "Knox Township", P("KNOX TOWNSHIP"), "Renewal",
           "General construction, reconstruction, resurfacing, and repair of streets, roads, and bridges.", "2 mills",
           "5 years, commencing in 2026", "2027", est("$17,528", "$31"), area="Precincts Knox Township 1 and 2", src=B)
    c.levy("madison-cemeteries", "Madison Township (including Zaleski Village)", P("MADISON TOWNSHIP", "ZALESKI VILLAGE"), "Renewal",
           "Maintaining and operating cemeteries.", "1 mill", "5 years, commencing in 2026", "2027", est("$14,352", "$14"),
           area="Precincts Zaleski Corp and Madison Township", src=B)
    c.levy("swan-cemeteries", "Swan Township", P("SWAN TOWNSHIP"), "Renewal",
           "Maintaining and operating cemeteries.", "0.5 mill", "5 years, commencing in 2026", "2027", est("$10,213", "$4"),
           area="Precincts Swan Township 1 and 2", src=B)
    c.levy("wilkesville-garbage", "Wilkesville Township (including Wilkesville Village)", P("WILKESVILLE TOWNSHIP", "WILKESVILLE VILLAGE"), "Renewal",
           "Collection and disposal of garbage or refuse, including yard waste.", "0.5 mill", "5 years, commencing in 2026", "2027", est("$103,807", "$11"),
           area="Precincts Wilkesville Corp and Wilkesville Township", src=B)

    # Shared with athens.py (issue-1 there). Only precinct Knox Township 2 votes on it in Vinton.
    c.issue("alexander-income-tax", "question", "Alexander Local School District (Athens, Meigs and Vinton)",
            "School district income tax: 0.75 percent, 5 years, current expenses",
            SD("ALEXANDER LOCAL SD (ATHENS)"), area="Precinct Knox Township 2 (the part of Knox Township in the district)",
            text="Shall an annual income tax of 0.75 percent on the earned income of individuals residing in the school district be imposed by Alexander Local School District, "
                 "for 5 years, beginning January 1, 2027, for the purpose of current expenses?", src=B)
    return c
