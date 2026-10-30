from lib import County, NOTE_ORDER, NOTE_PLACES

SITE = "https://www.boe.ohio.gov/brown/"
NOTICE = "https://www.boe.ohio.gov/brown/c/upload/FWAB_11November46Day.pdf"
BALLOTS = "https://lookup.boe.ohio.gov/vtrapp/brown/ballotlist.aspx"


def build():
    # The SoS file spells the village "MT. ORAB VILLAGE"; the Board's notice and ballot lookup say "Village of Mount Orab" / "MOUNT ORAB VILLAGE".
    # Other names display correctly by default ("BYRD TWP" -> "Byrd Township").
    # Bethel-Tate Local SD (clermont.py "bethel-tate-current") has no Brown County voters in the SoS file and is not on Brown's notice.
    c = County("brown", "Brown", "39015", rename={"MT. ORAB VILLAGE": "Mount Orab Village"})
    c.src("brown-46day", "Brown County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election", NOTICE)
    c.src("brown-ballots", "Brown County Board of Elections: precinct sample ballots, November 3, 2026 General Election (full ballot wording)", BALLOTS)
    S = ["brown-46day", "brown-ballots"]
    c.links = [
        {"label": "Board of Elections", "url": SITE},
        {"label": "Election information", "url": "https://www.boe.ohio.gov/brown/election-info/"},
        {"label": "Sample ballots by precinct", "url": BALLOTS},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://www.boe.ohio.gov/brown/election-info/election-results/"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it, "
               "checked against the Board's precinct sample ballots (which give the full ballot wording).",
               NOTE_ORDER, NOTE_PLACES,
               "The Board's notice and sample ballots do not give local issue numbers; see your sample ballot."]
    P = c.p; D = c.district

    # --- Federal, state legislative, appeals (all precincts are in the 2nd Congressional and 12th Appeals districts; State Senate District 14 is not up) ---
    c.contest("congress-2", "U.S. House", "Representative to Congress", [("Jen Mazzuckelli", "DEM"), ("David J. Taylor", "REP")],
              detail="2nd District · full term commencing January 3, 2027", places=D("cong", 2), src=S)
    c.contest("rep-63", "Ohio General Assembly", "State Representative", [("Adam C. Bird", "REP"), ("Debbie Davidson", "DEM")],
              detail="63rd District (Clermont and part of Brown) · full term commencing January 1, 2027", places=D("rep", 63), src=S)
    c.contest("rep-90", "Ohio General Assembly", "State Representative", [("Collin Docterman", "DEM"), ("Justin Pizzulli", "REP")],
              detail="90th District · full term commencing January 1, 2027", places=D("rep", 90), src=S)
    # Brown's 9/11 notice also lists write-ins Victor M. Haddad and Curt Carl Hartman; both withdrew later (Warren County's notice: 9/28 and 10/2),
    # so only Concannon is listed, as in butler.py, warren.py and clermont.py. Byrne's name is still printed on the ballot.
    c.contest("appeals-12-0101", "Ohio Court of Appeals", "Judge of the Court of Appeals",
              [("Matthew Byrne", "REP", "Withdrawn; his name is still on the ballot, but votes for him will not count"),
               ("Willa Concannon", "Write-in")],
              detail="12th District (Butler, Brown, Clermont, Clinton, Fayette, Madison, Preble and Warren counties) · full term commencing January 1, 2027", src=S)
    c.contest("appeals-12-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Robert A. Hendrickson", "REP")],
              detail="12th District (Butler, Brown, Clermont, Clinton, Fayette, Madison, Preble and Warren counties) · full term commencing February 9, 2027", src=S)

    # --- County offices ---
    c.contest("commissioner", "County offices", "County Commissioner", [("Frank Fussnecker", "REP")], detail="Full term commencing January 1, 2027", src=S)
    c.contest("auditor", "County offices", "County Auditor", [("Jill Hall", "REP")], detail="Full term commencing March 8, 2027", src=S)
    c.contest("coroner", "County offices", "Coroner", [("Steven A. Battaglia", "DEM")], detail="Unexpired term ending December 31, 2028", src=S)
    NP = " · no party label on the ballot"
    c.contest("cp-general", "Court of Common Pleas", "Judge of the Court of Common Pleas, General Division", ["Zac Corbin"],
              detail="Full term commencing February 9, 2027" + NP, src=S)
    c.contest("cp-probate", "Court of Common Pleas", "Judge of the Court of Common Pleas, Probate Division", ["Val E. Lewis, II"],
              detail="Full term commencing February 9, 2027" + NP, src=S)

    # --- Issues (unnumbered in the Board's documents; listed in the notice's order) ---
    FIRE = ("Fire and EMS: fire apparatus and equipment, buildings and sites, fire-alarm communications, firefighting and emergency medical service personnel, "
            "and ambulance, paramedic or other emergency medical services operated by a fire department or firefighting company.")
    # Notice: precincts 0070/1, 0080/1 and 0081/1 (Mt Orab North and the other two Mount Orab precincts in the Board's lookup).
    c.levy("mount-orab-fire", "Village of Mount Orab", P("MT. ORAB VILLAGE"), "Renewal", FIRE, "2 mills", "5 years, commencing in 2026", "2027",
           estimate="$112,300 per year ($40 per $100,000 of market value)", area="Mount Orab Village (precincts 0070, 0080 and 0081)", src=S)
    c.levy("ripley-streets", "Village of Ripley", P("RIPLEY VILLAGE"), "Additional",
           "General construction, reconstruction, resurfacing and repair of streets, roads and bridges in municipal corporations.", "2.5 mills",
           "5 years, commencing in 2027", "2028", estimate="$82,521 per year ($88 per $100,000 of market value)", area="Ripley Village (precinct 0310)", src=S)
    c.levy("russellville-ems", "Village of Russellville", P("RUSSELLVILLE VILLAGE"), "Renewal", "Ambulance service, emergency medical service, or both.", "2 mills",
           "5 years, commencing in 2027", "2028", estimate="$19,494 per year ($70 per $100,000 of market value)",
           area="Russellville Village (precinct 0130/1, Jefferson Russ)", src=S)
    c.levy("russellville-fire", "Village of Russellville", P("RUSSELLVILLE VILLAGE"), "Renewal", FIRE, "4 mills",
           "5 years, commencing in 2027", "2028", estimate="$38,988 per year ($140 per $100,000 of market value)",
           area="Russellville Village (precinct 0130/1, Jefferson Russ)", src=S)
    c.levy("green-twp-fire", "Green Township (unincorporated area)", P("GREEN TWP"), "Additional", FIRE, "1 mill",
           "Continuing period of time, commencing in 2026", "2027", estimate="$50,656 per year ($35 per $100,000 of market value)",
           area="Green Township unincorporated area (precincts 0090 and 0091)", src=S)
    c.issue("liquor-wildflowers", "liquor", "Eagle Township", "Local liquor option: Wildflowers Reserve LLC", P("EAGLE TWP"),
            area="Eagle Township precinct 0050 (all splits)",
            text="Local option for a particular location (by petition): sale of beer, wine and mixed beverages, and spirituous liquor by Wildflowers Reserve LLC, "
                 "an applicant for D-1, D-2 and D-3 liquor permits, operating a full-service, family-oriented banquet and wedding facility at "
                 "12577 US Hwy 62, Eagle Twp., Sardinia.", src=S)
    c.issue("liquor-wildflowers-sunday", "liquor", "Eagle Township", "Local liquor option: Wildflowers Reserve LLC (Sunday)", P("EAGLE TWP"),
            area="Eagle Township precinct 0050 (all splits)",
            text="Local option for a particular location (by petition): Sunday sale of wine and mixed beverages and spirituous liquor by Wildflowers Reserve LLC, "
                 "an applicant for a D-6 liquor permit, operating a full-service, family-oriented banquet and wedding facility at "
                 "12577 US Hwy 62, Eagle Twp., Sardinia.", src=S)
    return c
