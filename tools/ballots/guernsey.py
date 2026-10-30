from lib import County, NOTE_ORDER, NOTE_PLACES

SITE = "https://boe.guernseycounty.gov/"
NOTICE = "https://boe.guernseycounty.gov/wp-content/uploads/2026/10/46-day-notice-Nov.-3-2026-General-update-10-7-26.pdf"
BALLOTS = "https://lookup.boe.ohio.gov/vtrapp/guernsey/ballotlist.aspx"


def build():
    # The Board has its own site (boe.guernseycounty.gov), not boe.ohio.gov/guernsey.
    # Raw SoS names display correctly by default ("LORE CITY VILLAGE" -> "Lore City Village", "PLEASANT CITY VILLAGE", "QUAKER CITY VILLAGE").
    c = County("guernsey", "Guernsey", "39059")
    c.src("guernsey-46day", "Guernsey County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election (updated 10/7/2026)", NOTICE)
    c.src("guernsey-ballots", "Guernsey County Board of Elections: official sample ballots for all 35 precincts, November 3, 2026 (state ballot lookup; full ballot wording)", BALLOTS)
    S = ["guernsey-46day", "guernsey-ballots"]
    c.links = [
        {"label": "Board of Elections", "url": SITE},
        {"label": "Sample ballots by precinct", "url": BALLOTS},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": SITE}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it, "
               "checked against the Board's precinct sample ballots (which give the full ballot wording and the auditor's estimates).",
               NOTE_ORDER, NOTE_PLACES,
               "The Board's notice and sample ballots do not give local issue numbers; see your sample ballot."]
    P = c.p; D = c.district; SD = c.sd

    # --- Federal, state legislative, appeals (whole county: 12th Congressional, 5th Appeals; State Senate District 30 is not up) ---
    c.contest("congress-12", "U.S. House", "Representative to Congress", [("Troy Balderson", "REP"), ("Jerrad Christian", "DEM")], detail="12th District · 2-year term", src=S)
    c.contest("senate-31", "Ohio General Assembly", "State Senator", [("Al Landis", "REP"), ("Laura Sirot", "DEM")], detail="31st District", places=D("sen", 31), src=S)
    c.contest("rep-95", "Ohio General Assembly", "State Representative", [("Paul Cameron", "DEM"), ("Ty Moore", "REP")], detail="95th District", places=D("rep", 95), src=S)
    # Kris Geis has no party on the notice or the ballot (muskingum.py: "Nonparty").
    c.contest("rep-97", "Ohio General Assembly", "State Representative", [("Kris Geis", "Nonparty"), ("Tim Godwin", "LIB"), ("Adam P. Holmes", "REP")],
              detail="97th District", places=D("rep", 97), src=S)
    c.contest("appeals-5", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Matthew George", "REP")], detail="5th District · term commencing February 9, 2027", src=S)

    # --- County offices ---
    c.contest("commissioner", "County offices", "County Commissioner", [("Tom Hannon", "DEM"), ("Dave Wilson", "REP")], detail="Full term commencing January 1, 2027", src=S)
    c.contest("auditor", "County offices", "County Auditor", [("Cory Johnson", "REP")], detail="4-year term", src=S)
    NP = " · no party label on the ballot"
    c.contest("cp-probate-juvenile", "Court of Common Pleas", "Judge of the Court of Common Pleas, Probate/Juvenile Division", ["David B. Bennett"],
              detail="Full term commencing February 9, 2027" + NP, src=S)

    # --- Issues (unnumbered; listed in the notice's order) ---
    est = lambda total, per: f"{total} a year; {per} for each $100,000 of market value"
    ALL = "Guernsey County (all 35 precincts)"
    c.levy("library", "Guernsey County District Public Library", "county", "Renewal", "Current expenses.", "1 mill", "5 years, commencing in 2027", "2028",
           estimate=est("$962,977", "$19"), area=ALL, src=S)
    c.levy("senior-meals-on-wheels", "Guernsey County", "county", "Renewal",
           "Guernsey County Senior Citizens Center, Inc. Meals on Wheels Program: maintaining and operating the Meals on Wheels Program for senior citizens.",
           "0.75 mill", "5 years, commencing in 2027", "2028", estimate=est("$914,994", "$22"), area=ALL, src=S)
    c.levy("sheriff-911", "Guernsey County", "county", "Renewal", "Maintaining and operating the Guernsey County Sheriff's Department enhanced 911 system.",
           "1 mill", "5 years, commencing in 2027", "2028", estimate=est("$1,060,439", "$23"), area=ALL, src=S)
    c.levy("children-services", "Guernsey County", "county", "Additional", "Providing funds for children services (Guernsey County Children Services).",
           "1.25 mills", "10 years, commencing in 2026", "2027", estimate=est("$1,753,704", "$44"), area=ALL, src=S)

    c.levy("old-washington-current", "Village of Old Washington", P("OLD WASHINGTON VILLAGE"), "Renewal", "Current expenses.", "1 mill",
           "5 years, commencing in 2027", "2028", estimate=est("$1,530", "$7"), area="Old Washington - Wills precinct (035, split 1 Old Washington only)", src=S)
    c.levy("pleasant-city-streets", "Village of Pleasant City", P("PLEASANT CITY VILLAGE"), "Renewal", "Street improvement and maintenance.", "3 mills",
           "5 years, commencing in 2026", "2027", estimate=est("$11,578", "$76"), area="Pleasant City - Valley B precinct (032, split 1 Pleasant City only)", src=S)
    KX = P("KNOX TOWNSHIP")
    c.levy("knox-garbage", "Knox Township", KX, "Renewal", "Disposal of garbage and refuse.", "0.75 mill", "5 years, commencing in 2027", "2028",
           estimate=est("$16,236", "$22"), area="Knox precinct (021)", src=S)
    c.levy("knox-cemeteries", "Knox Township", KX, "Renewal", "Maintaining and operating cemeteries.", "0.5 mill", "5 years, commencing in 2027", "2028",
           estimate=est("$9,557", "$13"), area="Knox precinct (021)", src=S)
    c.levy("liberty-cemeteries", "Liberty Township", P("LIBERTY TOWNSHIP"), "Renewal", "Maintaining and operating cemeteries.", "0.5 mill", "5 years, commencing in 2027", "2028",
           estimate=est("$11,152", "$9"), area="Liberty precinct (022)", src=S)
    c.levy("londonderry-fire", "Londonderry Township", P("LONDONDERRY TOWNSHIP"), "Renewal and decrease", "Fire protection.", "0.5 mill",
           "5 years, commencing in 2027", "2028", estimate=est("$23,389", "$8"), area="Londonderry - Washington precinct (023, split 1 Londonderry Township only)", src=S,
           note="A renewal of part of an existing 1-mill levy, being a reduction of 0.5 mill.")
    c.levy("spencer-cemeteries", "Spencer Township (including Cumberland Village)", P("SPENCER TOWNSHIP", "CUMBERLAND VILLAGE"), "Renewal",
           "Maintaining and operating cemeteries.", "0.6 mill", "5 years, commencing in 2027", "2028", estimate=est("$16,269", "$11"),
           area="Cumberland - Spencer precinct (030)", src=S)
    c.levy("washington-twp-fire", "Washington Township", P("WASHINGTON TOWNSHIP"), "Renewal", "Fire protection.", "1 mill", "5 years, commencing in 2027", "2028",
           estimate=est("$33,074", "$27"), area="Londonderry - Washington precinct (023, split 2 Washington Township only)", src=S)
    WL = P("WESTLAND TOWNSHIP")
    c.levy("westland-fire-ems", "Westland Township", WL, "Renewal", "Fire protection, ambulance, and emergency medical services.", "1.6 mills",
           "5 years, commencing in 2026", "2027", estimate=est("$110,729", "$39"), area="Westland A and Westland B precincts (033, 034)", src=S)
    c.levy("westland-fire", "Westland Township", WL, "Renewal", "Fire protection.", "0.4 mill", "5 years, commencing in 2027", "2028",
           estimate=est("$29,536", "$11"), area="Westland A and Westland B precincts (033, 034)", src=S)
    # Notice: Cambridge 1-A to 4-B (2-A and 2-B split 1 only), Cambridge Twp. A/B/C (split 1), Jefferson - Madison (split 2, Jefferson),
    # Knox (split 1), Liberty, Monroe - Wheeling (splits 2 and 5) -- the same places as the voter file.
    c.levy("cambridge-csd-current", "Cambridge City School District", SD("CAMBRIDGE CITY SD"), "Renewal",
           "Current operating expenses (fixed sum of $1,455,000 a year, outside the ten-mill limitation).", "3.8 mills (estimated average)",
           "5 years, commencing in 2027", "2028", estimate=est("$1,455,000", "$133"), area="Cambridge City School District precincts", src=S)

    # --- Local liquor options ---
    # The notice titles the CBI questions "Precinct 018 Byesville A" but lists them under "018 Byesville B Only"; the sample ballots put both
    # on the Byesville A (0018) ballot only, and the notice's own precinct lists number Byesville A 0018 and Byesville B 0019.
    BV = P("BYESVILLE VILLAGE")
    for id, jur, places, prec, title, text in [
        ("liquor-thirsty-turtle", "City of Cambridge", P("CAMBRIDGE CITY"), "Cambridge 4-B precinct (0008)", "Local liquor option: Thirsty Turtle (Sunday sales)",
         "Local option (by petition, Sunday sales): sale of wine and mixed beverages, or spirituous liquor, on Sunday by Thirsty Turtle LLC, Thirsty Turtle, "
         "an applicant for a D-6 liquor permit engaged in the business of a tavern at 1023 Wheeling Avenue, Cambridge."),
        ("liquor-cbi-d5", "Village of Byesville", BV, "Byesville A precinct (0018)", "Local liquor option: Southeastern Ohio Center for Business and Innovation (CBI)",
         "Local option (by petition): sale of wine and mixed beverages and spirituous liquor by Southeastern Ohio Center for Business and Innovation dba CBI, "
         "an applicant for a D-5 liquor permit, operating a catering / reception hall at 212 Main Avenue, Byesville."),
        ("liquor-cbi-sunday", "Village of Byesville", BV, "Byesville A precinct (0018)", "Local liquor option: Southeastern Ohio Center for Business and Innovation (CBI) (Sunday sales)",
         "Local option (by petition, Sunday sales): sale of wine and mixed beverages and spirituous liquor on Sunday by Southeastern Ohio Center for Business and "
         "Innovation dba CBI, an applicant for a D-6 liquor permit, operating a catering / reception hall at 212 Main Avenue, Byesville."),
    ]:
        c.issue(id, "liquor", jur, title, places, area=prec, text=text, src=S)
    return c
