from lib import County, NOTE_ORDER, NOTE_PLACES

SITE = "https://www.boe.ohio.gov/seneca/"
NOTICE = "https://www.boe.ohio.gov/seneca/c/upload/FWAB_11November46Day.pdf"
BALLOTS = "https://lookup.boe.ohio.gov/vtrapp/seneca/ballotlist.aspx"


def build():
    # Default display names are right ("BIG SPRING TWP" -> "Big Spring Township", "SENECA TWP" -> "Seneca Township").
    # Bellevue City (Erie, Huron, Sandusky and Seneca) has no Seneca County precinct or voters, so erie.py's Bellevue levy is not on this ballot.
    c = County("seneca", "Seneca", "39147")
    c.src("seneca-46day", "Seneca County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election", NOTICE)
    c.src("seneca-ballots", "Seneca County Board of Elections: precinct sample ballots, November 3, 2026 General Election (full ballot wording)", BALLOTS)
    S = ["seneca-46day", "seneca-ballots"]
    c.links = [
        {"label": "Board of Elections", "url": SITE},
        {"label": "Election information", "url": "https://www.boe.ohio.gov/seneca/election-info/"},
        {"label": "Sample ballots by precinct", "url": BALLOTS},
        {"label": "Questions and issues", "url": "https://lookup.boe.ohio.gov/vtrapp/seneca/webqis/qisearch.aspx"},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://www.boe.ohio.gov/seneca/election-info/election-results/"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it, "
               "checked against the Board's precinct sample ballots (which give the full ballot wording).",
               NOTE_ORDER, NOTE_PLACES,
               "The Board's notice and sample ballots do not give local issue numbers; see your sample ballot."]
    P = c.p; SD = c.sd

    # --- Federal, state legislative, appeals (all of Seneca County is in each district; State Senate District 26 is not up) ---
    c.contest("congress-5", "U.S. House", "Representative to Congress", [("Bob Latta", "REP"), ("Brian A. Shaver", "DEM"), ("Michael J. Veloff", "LIB")],
              detail="5th District", src=S)
    c.contest("rep-88", "Ohio General Assembly", "State Representative", [("Gary Click", "REP"), ("Aaron W. Jones", "DEM")], detail="88th District", src=S)
    c.contest("appeals-3-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Mark C. Miller", "REP")], detail="3rd District · full term commencing February 9, 2027", src=S)

    # --- County offices ---
    # The notice spells the independent "David G. Zielger"; the sample ballots print "David G. Ziegler" (used here), with no party label.
    c.contest("commissioner", "County offices", "County Commissioner", [("Bill Frankart", "REP"), ("David G. Ziegler", "Nonparty")],
              detail="Full term commencing January 1, 2027", src=S)
    c.contest("auditor", "County offices", "County Auditor", [("Julie A. Adkins", "REP")], src=S)  # neither document prints a term for this office
    NP = " · no party label on the ballot"
    # The notice says "Probate Division"; the sample ballots say "Probate/Juvenile Division".
    c.contest("cp-probate-juvenile", "Court of Common Pleas", "Judge of the Court of Common Pleas, Probate/Juvenile Division", ["Jay A. Meyer"],
              detail="Full term commencing February 9, 2027" + NP, src=S)

    # --- Issues (unnumbered in the Board's documents; listed in the notice's order) ---
    # Notice precincts: Adams 3, Clinton A2, Liberty A1 & A2, Liberty B1, Pleasant 1, Hopewell A1 and all of Bettsville Village (same places as the voter file).
    c.levy("old-fort-schools", "Old Fort Local School District (Seneca and Sandusky)", SD("OLD FORT LOCAL SD (SENECA)"), "Renewal",
           "Current operating expenses and general permanent improvements.", "6.3 mills (4.30 mills current operating, 2.00 mills permanent improvements)",
           "5 years, commencing in 2027", "2028", estimate="$528,626 per year ($111 per $100,000 of market value)",
           area="Old Fort Local School District (Seneca County part: Adams 3, Bettsville Village, Clinton A2, Hopewell A1, Liberty A1, A2 and B1, Pleasant 1)", src=S)
    c.levy("bettsville-library", "Bettsville Public Library", P("BETTSVILLE VILLAGE", "LIBERTY TWP"), "Renewal", "Current expenses.", "0.4 mill",
           "5 years, commencing in 2027", "2028", estimate="$10,828 per year ($10 per $100,000 of market value)",
           area="Bettsville Village and Liberty Township precincts Liberty A2 and Liberty B1", src=S)
    c.levy("mhrs", "Seneca County", "county", "Renewal",
           "Mental Health and Recovery Services Board of Seneca, Ottawa, Sandusky and Wyandot Counties (and/or its intended successor, the North Central Behavioral Health Board): "
           "operation of community addiction and mental health services providers, and alcohol and drug addiction and mental health facilities in Seneca County.",
           "0.7 mill", "10 years, commencing in 2027", "2028", estimate="$1,043,000 per year ($18 per $100,000 of market value)", src=S)
    c.levy("fostoria-current", "City of Fostoria (Hancock, Seneca and Wood)", P("FOSTORIA CITY"), "Renewal", "Current expenses.", "6 mills", "5 years, commencing in 2027", "2028",
           estimate="$1,047,593 per year", area="Fostoria City (Seneca County part: all Fostoria precincts)", src=S)
    c.levy("green-springs-fire", "Village of Green Springs (Sandusky and Seneca)", P("GREEN SPRINGS VILLAGE"), "Additional", "Fire protection.", "3 mills",
           "5 years, commencing in 2026", "2027", estimate="$69,080 per year ($105 per $100,000 of market value)",
           area="Green Springs Village (Seneca County part)", src=S)
    c.issue("liquor-quarry-campground", "liquor", "Village of Bettsville", "Local liquor option: Kamb, LLC dba The Quarry Campground (Sunday)", P("BETTSVILLE VILLAGE"),
            area="Bettsville Village precinct",
            text="Local option (by petition): Sunday sale of beer, wine and mixed beverages by Kamb, LLC dba The Quarry Campground, an applicant for a C-1, C-2 and D-6 liquor permit "
                 "authorizing off-premise sales, operating a campground and food and beverage carryout at 7800 N. Township Rd 70, Tiffin.", src=S)
    return c
