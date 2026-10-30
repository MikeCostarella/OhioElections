from lib import County, NOTE_ORDER, NOTE_PLACES

SITE = "https://allen.boe.ohio.gov/"
# The Board posts its 46-day notice as a Dropbox file (2026_GENERAL_FWAB.pdf, revised 9/8/2026), linked from its election page.
ELECTION = "https://allen.boe.ohio.gov/2026/07/23/general-election-november-3-2026/"


def build():
    # The SoS file lists townships as "Township Amanda"; cities and villages are clean ("BLUFFTON VILLAGE" -> "Bluffton Village").
    # Bluffton is shared with Hancock County; it has no contests or issues of its own on Allen's ballot.
    rename = {f"Township {t}": f"{t} Township" for t in
              ("Amanda", "American", "Auglaize", "Bath", "Jackson", "Marion", "Monroe", "Perry", "Richland", "Shawnee", "Spencer", "Sugar Creek")}
    c = County("allen", "Allen", "39003", rename=rename)
    c.src("allen-46day", "Allen County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election (revised 9/8/2026)", ELECTION)
    S = ["allen-46day"]
    c.links = [
        {"label": "Board of Elections", "url": SITE},
        {"label": "General Election, November 3, 2026", "url": ELECTION},
        {"label": "Sample ballots by precinct", "url": "https://lookup.boe.ohio.gov/vtrapp/allen/ballotlist.aspx"},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": SITE}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it. "
               "Issue wording is the Board's; the full wording is on the sample ballot.",
               NOTE_ORDER, NOTE_PLACES,
               "The Board's notice does not give local issue numbers; see your sample ballot for them."]
    P = c.p; D = c.district; SD = c.sd

    # All of Allen County is in the 4th Congressional, 78th House and 12th Senate districts; the 12th Senate seat is not up in 2026.
    # The notice prints no party for Tackett (an independent candidate), as in clark.py.
    c.contest("congress-4", "U.S. House", "Representative to Congress", [("Jim Jordan", "REP"), ("Joshua D. Kolasinski", "DEM"), ("Tracey L. Tackett", "Nonparty")],
              detail="4th District", places=D("cong", 4), src=S)
    c.contest("rep-78", "Ohio General Assembly", "State Representative", [("Jeffrey R. Givan", "DEM"), ("Matt Huffman", "REP")], detail="78th District", places=D("rep", 78), src=S)
    c.contest("appeals-3-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Mark C. Miller", "REP")], detail="3rd District · term commencing February 9, 2027", src=S)
    c.contest("commissioner", "County offices", "County Commissioner", [("Lew Modic", "DEM"), ("Brian Winegardner", "REP")], detail="Term commencing January 1, 2027", src=S)
    c.contest("auditor", "County offices", "County Auditor", [("Rachael S. Gilroy", "REP")], detail="Term commencing March 8, 2027", src=S)
    NP = " · no party label on the ballot"
    # The notice prints "(Rep)" after Kohlrieser; Common Pleas judges carry no party label on the general-election ballot.
    c.contest("cp-probate", "Court of Common Pleas", "Judge of the Court of Common Pleas, Probate Division", ["Todd E. Kohlrieser"],
              detail="Term commencing February 9, 2027" + NP, src=S)

    # --- Local issues (unnumbered in the notice; listed in the notice's order) ---
    c.issue("lima-referendum-022-26", "question", "City of Lima", "Referendum on Ordinance No. 022-26 (Cable Road Improvement Project land acquisition)", P("LIMA CITY"),
            area="Lima City (all precincts, 1A–7C)",
            text="Shall ordinance no. 022-26 proposing the Mayor purchase or accept donations of real property for the Cable Road Improvement Project (PID 112573) "
                 "along Cable Road, from Latham Avenue to College Park West Drive, be approved? (Referendum by petition.)", src=S)
    c.levy("delphos-csd-current", "Delphos City School District", SD("DELPHOS CITY SD"), "Renewal", "Current expenses.", "5.5 mills", "5 years, commencing in 2027", "2028",
           "$929,532 a year; $83 for each $100,000 of market value", area="Delphos City School District (Delphos 1A, 1B, 2A, 2B, Marion A, B, Spencer A)", src=S)
    c.levy("lima-csd-pi-current", "Lima City School District", SD("LIMA CITY SD"), "Renewal",
           "Acquisition, construction, enlargement, renovation and financing of general permanent improvements, and current operating expenses.", "5.99 mills",
           "5 years, commencing in 2027", "2028", "$1,836,189 a year; $142 for each $100,000 of market value",
           area="Lima City School District (Lima 1A–7C, American E and K)", src=S)
    c.levy("perry-lsd-current", "Perry Local School District", SD("PERRY LOCAL SD (ALLEN)"), "Renewal", "Current expenses.", "4.9 mills", "5 years, commencing in 2026", "2027",
           "$605,689 a year; $89 for each $100,000 of market value", area="Perry Local School District (Lima 5D, 6C, Perry A, B, C)", src=S)
    c.issue("spencerville-lsd-income-tax", "question", "Spencerville Local School District", "School district income tax: 1% renewal for 5 years, for current expenses",
            SD("SPENCERVILLE LOCAL SD (ALLEN)"), area="Spencerville Local School District (Amanda E, N, Spencerville A, B, Spencer A)",
            text="Annual income tax of 1% on the school district income of individuals, to renew an income tax expiring at the end of 2027, for 5 years, "
                 "beginning January 1, 2028, for current expenses.", src=S)
    c.levy("monroe-twp-fire", "Monroe Township", P("Township Monroe", "CAIRO VILLAGE"), "Renewal",
           "Fire apparatus, buildings, water supply, fire alarm lines, firefighters, and ambulance, paramedic or other emergency medical services.", "0.5 mill",
           "5 years, commencing in 2026", "2027", "$26,644 a year; $9 for each $100,000 of market value", area="Monroe Township and Cairo Village (Cairo, Monroe E, W)", src=S)
    PT = P("Township Perry")
    for id, mills, amt, per in [("perry-twp-fire-1", "1 mill", "$123,771", "$19"), ("perry-twp-fire-1-5", "1.5 mills", "$185,656", "$29")]:
        c.levy(id, "Perry Township", PT, "Renewal",
               "Fire apparatus, buildings, water supply, fire-alarm communications, firefighting, EMS, administrative or communications personnel, and ambulance, paramedic or other emergency medical services.",
               mills, "5 years, commencing in 2027", "2028", f"{amt} a year; {per} for each $100,000 of market value", area="Perry Township (Perry A, B, C)",
               note="Perry Township has two fire/EMS renewals on this ballot (1 mill and 1.5 mills).", src=S)
    c.levy("sugar-creek-twp-current", "Sugar Creek Township", P("Township Sugar Creek"), "Renewal", "Current expenses.", "2 mills", "5 years, commencing in 2027", "2028",
           "$85,210 a year; $33 for each $100,000 of market value", area="Sugar Creek Township (Sugar Creek)", src=S)
    c.issue("liquor-richland-a-racetrac", "liquor", "Richland Township", "Local liquor option: RaceTrac (Sunday)", P("Township Richland"), area="Richland Township precinct Richland A",
            text="Sunday sale of wine and mixed beverages by RaceTrac, Inc., an applicant for a D-6 liquor permit, operating a carryout/grocery store at 6452 Reppert Road, Lima "
                 "(local option for a particular use at a business location, by petition).", src=S)
    return c
