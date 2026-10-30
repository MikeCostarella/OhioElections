from lib import County, NOTE_ORDER, NOTE_PLACES

SITE = "https://www.boe.ohio.gov/hocking/"
NOTICE = "https://www.boe.ohio.gov/hocking/c/upload/FWAB_11November46Day.pdf"
BALLOTS = "https://lookup.boe.ohio.gov/vtrapp/hocking/ballotlist.aspx"


def build():
    # Raw SoS names ("FALLS TWP", "LOGAN CITY", "MURRAY CITY VILLAGE", "SALTCREEK TWP") already display correctly; no renames needed.
    c = County("hocking", "Hocking", "39073")
    c.src("hocking-46day", "Hocking County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election (updated notification)", NOTICE)
    c.src("hocking-ballots", "Hocking County Board of Elections: precinct sample ballots, November 3, 2026 General Election", BALLOTS)
    S = ["hocking-46day", "hocking-ballots"]; I = ["hocking-ballots", "hocking-46day"]
    c.links = [
        {"label": "Board of Elections", "url": SITE},
        {"label": "Federal write-in absentee ballot notices", "url": "https://www.boe.ohio.gov/hocking/election-info/federal-write-in-absentee-ballots/"},
        {"label": "Candidate list", "url": "https://lookup.boe.ohio.gov/vtrapp/hocking/cfis.aspx"},
        {"label": "Sample ballots by precinct", "url": BALLOTS},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://www.boe.ohio.gov/hocking/election-info/election-results/"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it, "
               "checked against the Board's precinct sample ballots. Issue wording is from the sample ballots.",
               NOTE_ORDER, NOTE_PLACES,
               "Local issues are not numbered in the Board's notice or on the sample ballots; see your sample ballot for the order.",
               "Court of Appeals: Peter B. Abele (Republican) is still printed on the main ballot for the 4th District seat; the Board's notice marks him "
               "deceased, and a supplemental 4th District Court of Appeals ballot lists Jayme Hartley Fountain (Republican) and "
               "Todd L. Grace (Democratic). The supplemental ballot is shown here."]
    P = c.p; D = c.district

    # --- Federal, state legislative, appeals (the notice lists every precinct for each; the voter file agrees) ---
    c.contest("congress-2", "U.S. House", "Representative to Congress", [("Jen Mazzuckelli", "DEM"), ("David J. Taylor", "REP")],
              detail="2nd District", places=D("cong", 2), src=S)
    c.contest("senate-17", "Ohio General Assembly", "State Senator", [("Brian A. Deer", "DEM"), ("Shane Wilkin", "REP")],
              detail="17th District", places=D("sen", 17), src=S)
    c.contest("rep-92", "Ohio General Assembly", "State Representative", [("Mark Johnson", "REP"), ("Sarah Senff", "DEM")],
              detail="92nd District", places=D("rep", 92), src=S)
    # The notice lists "Peter B. Abele - Deceased" above Fountain (Rep) and Grace (Dem); the main sample ballots still print Abele and
    # each precinct's ballot has a supplemental page with Fountain and Grace.
    c.contest("appeals-4-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Jayme Hartley Fountain", "REP"), ("Todd L. Grace", "DEM")],
              detail="4th District · full term commencing February 9, 2027", src=I)

    # --- County ---
    c.contest("commissioner", "County offices", "County Commissioner", [("Michael Schrader", "DEM"), ("Tony Wheeler", "REP")],
              detail="Full term commencing January 1, 2027", src=S)
    # Neither the notice nor the sample ballot gives the auditor's term.
    c.contest("auditor", "County offices", "County Auditor", [("Christopher D. Robers", "REP")], src=S)
    NP = " · no party label on the ballot"
    # The notice calls it the Probate/Juvenile Division; the ballot title is "Domestic / Juvenile and Probate Division".
    c.contest("cp-domestic-juvenile-probate", "Court of Common Pleas", "Judge of the Court of Common Pleas, Domestic/Juvenile and Probate Division",
              ["Jonah M. Saving"], detail="Full term commencing February 9, 2027" + NP, src=I)

    # --- Issues (unnumbered in the notice and on the sample ballots; listed in the notice's order) ---
    est = lambda a, per: f"${a} a year; ${per} for each $100,000 of the county auditor's market value"
    c.levy("county-senior-services", "Hocking County", "county", "Renewal", "Providing and maintaining senior citizen services and facilities.", "0.5 mill",
           "5 years, commencing in 2027", "2028", est("487,604", 9), area="Hocking County (all precincts)", src=I)
    # "Falls Township - Unincorporated": on the Falls 1-3 ballots only, not Logan City's.
    c.levy("falls-fire", "Falls Township (unincorporated)", P("FALLS TWP"), "Renewal and increase",
           "Fire protection (renewal of 1.2 mills and increase of 0.25 mill).", "1.45 mills",
           "5 years, commencing in 2027", "2028", est("198,018", 27), area="Precincts Falls 1, Falls 2 and Falls 3", src=I)
    c.levy("good-hope-fire", "Good Hope Township", P("GOOD HOPE TWP"), "Renewal", "Fire protection.", "0.5 mill",
           "5 years, commencing in 2027", "2028", est("55,027", 8), area="Good Hope precinct", src=I)
    c.levy("laurel-roads", "Laurel Township", P("LAUREL TWP"), "Renewal", "General construction, reconstruction, resurfacing and repair of roads.", "0.5 mill",
           "5 years, commencing in 2027", "2028", est("48,089", 7), area="Laurel precinct",
           note="The 46-day notice calls this a road improvements levy; the purpose shown is the sample ballot's.", src=I)
    c.levy("saltcreek-roads", "Saltcreek Township", P("SALTCREEK TWP"), "Renewal", "Road improvements.", "2 mills",
           "5 years, commencing in 2026", "2027", est("55,559", 22), area="Saltcreek precinct", src=I)
    # Same levy as athens.py's issue-11 (Athens County numbers it Issue 11; Hocking prints no number).
    c.levy("buchtel-current", "Village of Buchtel (Athens and Hocking)", P("BUCHTEL VILLAGE"), "Additional", "Current expenses.", "5 mills",
           "5 years, commencing in 2026", "2027", est("32,611", 175), area="Ward precinct (part): Buchtel Village", src=I)
    c.levy("laurelville-current", "Village of Laurelville", P("LAURELVILLE VILLAGE"), "Renewal and increase",
           "Current expenses (renewal of 5 mills and increase of 1.5 mills).", "6.5 mills",
           "5 years, commencing in 2027", "2028", est("38,694", 176), area="Perry 1 precinct (part): Laurelville Village", src=I)
    MC = P("MURRAY CITY VILLAGE"); MCA = "Ward precinct (part): Murray City Village"
    for id, purpose, mills, e, note in [
        ("murray-city-current-1", "Current expenses (#1).", "5 mills", est("14,930", 94), "Murray City has two current-expense renewals on this ballot (#1 and #2), each 5 mills."),
        ("murray-city-current-2", "Current expenses (#2).", "5 mills", est("14,930", 94), "Murray City has two current-expense renewals on this ballot (#1 and #2), each 5 mills."),
        ("murray-city-police", "Policing services.", "4 mills", est("11,942", 75), None),
        ("murray-city-streets", "Street maintenance.", "3 mills", est("8,958", 56), None),
        ("murray-city-fire", "Fire protection.", "2.5 mills", est("7,465", 47), None),
    ]:
        c.levy(id, "Village of Murray City", MC, "Renewal", purpose, mills, "5 years, commencing in 2027", "2028", e, area=MCA, note=note, src=I)
    return c
