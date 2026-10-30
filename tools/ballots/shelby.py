from lib import County, NOTE_ORDER, NOTE_PLACES

SITE = "https://www.boe.ohio.gov/shelby/"
NOTICE = "https://www.boe.ohio.gov/shelby/c/upload/FWAB_11November46Day.pdf"
BALLOTS = "https://lookup.boe.ohio.gov/vtrapp/shelby/ballotlist.aspx"


def build():
    # Raw names display correctly ("MCLEAN TOWNSHIP" -> "McLean Township", "TURTLECREEK TOWNSHIP"); no renames needed.
    c = County("shelby", "Shelby", "39149")
    c.src("shelby-46day", "Shelby County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election (revised 9/18/2026)", NOTICE)
    c.src("shelby-ballots", "Shelby County Board of Elections: sample ballots by precinct, November 3, 2026 General Election", BALLOTS)
    S = ["shelby-46day", "shelby-ballots"]
    c.links = [
        {"label": "Board of Elections", "url": SITE},
        {"label": "Election info", "url": "https://www.boe.ohio.gov/shelby/election-info/"},
        {"label": "Sample ballots by precinct", "url": BALLOTS},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://www.boe.ohio.gov/shelby/election-info/election-results/"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it, "
               "checked against the Board's sample ballots (which give the full ballot wording).",
               NOTE_ORDER, NOTE_PLACES,
               "Only the Green Township levy has a local issue number in the Board's notice; see your sample ballot for the others."]
    P = c.p

    # All of Shelby County is in the 4th Congressional, 85th House and 12th Senate districts; the 12th Senate seat is not up in 2026.
    # The notice prints "(Ind)" for Tackett; the ballot prints no party, as in allen.py/clark.py.
    # The notice also repeats the congressional candidates in a block mislabeled "STATE REPRESENTATIVE ... Fill 2 Year Term" (Tackett spelled "TACKET");
    # the ballot has one congressional contest and the 85th House race, so that block is ignored.
    c.contest("congress-4", "U.S. House", "Representative to Congress", [("Jim Jordan", "REP"), ("Joshua D. Kolasinski", "DEM"), ("Tracey L. Tackett", "Nonparty")],
              detail="4th District", src=S)
    c.contest("rep-85", "Ohio General Assembly", "State Representative", [("Tim Barhorst", "REP"), ("Victoria Maddox", "DEM")], detail="85th District", src=S)
    c.contest("appeals-3-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Mark C. Miller", "REP")], detail="3rd District · full term commencing February 9, 2027", src=S)
    c.contest("commissioner", "County offices", "County Commissioner", [("David L. Spicer", "REP")], detail="Full term commencing January 1, 2027", src=S)
    c.contest("auditor", "County offices", "County Auditor", [("Amy L. Berning", "REP")], detail="Full term commencing March 8, 2027", src=S)
    NP = " · no party label on the ballot"
    # The notice lists "PROBATE COURT JUDGE ... Commencing 02/08/2027" with "(Rep)"; the ballot says
    # "Judge of the Court of Common Pleas (Probate/Juvenile Division), full term commencing 2-9-2027" with no party. The ballot is used.
    c.contest("cp-probate-juvenile", "Court of Common Pleas", "Judge of the Court of Common Pleas, Probate/Juvenile Division", ["Jeffrey J. Beigel"],
              detail="Full term commencing February 9, 2027" + NP, src=S)

    # --- Countywide (same levy as miami.py) ---
    est = lambda total, per: f"{total} a year; {per} for each $100,000 of the county auditor's market value"
    c.levy("tri-county-mental-health", "Tri-County Board of Recovery and Mental Health Services (Darke, Miami and Shelby counties)", "county", "Renewal",
           "Counseling and supportive services to children and adults through alcohol and drug addiction programs and mental health programs.", "0.6 mill",
           "5 years, commencing in 2027", "2028", est("$2,596,848", "$10"), area="All of Shelby County", src=S)

    # --- Local issues (precincts from the notice; splits matched to places via the SoS file and the absentee list) ---
    # Green Township is the only issue the notice numbers ("Issue #1"); the sample ballot prints no number.
    c.levy("issue-1", "Green Township", P("GREEN TOWNSHIP"), "Renewal and increase",
           "Ambulance and emergency medical services (renewal of 1.2 mills and increase of 0.3 mill).", "1.5 mills",
           "5 years, commencing in 2027", "2028", est("$33,124", "$28"), number="Issue 1", area="Green Township (precincts 0021/1, 0021/2)", src=S)
    # 0035/1 and 0035/3 are Washington Township outside Lockington (0035/2).
    WA = "Washington Township, excluding the Village of Lockington and the City of Sidney (precincts 0035/1, 0035/3)"
    c.levy("washington-twp-fire-renewal", "Washington Township (excluding the Village of Lockington and the City of Sidney)", P("WASHINGTON TOWNSHIP"), "Renewal",
           "General costs and expenses to operate; fire apparatus, appliances, buildings or sites, water supply, and permanent, part-time or volunteer firefighters.",
           "2 mills", "5 years, commencing in 2027", "2028", est("$73,448", "$37"), area=WA, src=S)
    c.levy("washington-twp-fire-additional", "Washington Township (excluding the Village of Lockington and the City of Sidney)", P("WASHINGTON TOWNSHIP"), "Additional",
           "Fire apparatus, appliances, buildings or sites, water supply, and permanent, part-time or volunteer firefighters.",
           "2 mills", "5 years, commencing in 2026", "2027", est("$120,884", "$70"), area=WA, src=S)
    c.levy("port-jefferson-fire", "Village of Port Jefferson", P("PORT JEFFERSON VILLAGE"), "Renewal and increase",
           "Fire apparatus, appliances, buildings or sites, water supply, and permanent, part-time or volunteer firefighters (renewal of 1 mill and increase of 0.5 mill).",
           "1.5 mills", "3 years, commencing in 2027", "2028", est("$6,267", "$38"), area="Port Jefferson Village (precinct 0030/2)", src=S)
    c.levy("houston-fire-district", "Loramie Township, Houston Fire District", P("LORAMIE TOWNSHIP"), "Renewal",
           "Fire apparatus, appliances, buildings or sites, water supply, and permanent, part-time or volunteer firefighters.",
           "1 mill", "5 years, commencing in 2027", "2028", est("$21,347", "$19"), area="Loramie Township, Houston Fire District (precinct 0024/1)", src=S)
    # Precincts 0015-0016 are Cynthian Township, 0026 Fort Loramie Village, 0027 McLean Township, 0032 Turtlecreek Township.
    c.levy("loramie-fire-district", "Loramie Fire District", P("CYNTHIAN TOWNSHIP", "FORT LORAMIE VILLAGE", "MCLEAN TOWNSHIP", "TURTLECREEK TOWNSHIP"), "Renewal",
           "Fire apparatus, appliances, buildings or sites, water supply, and permanent, part-time or volunteer firefighters.",
           "2 mills", "3 years, commencing in 2027", "2028", est("$618,922", "$70"),
           area="Loramie Fire District (Cynthian 0015/1–2 and 0016/1–3, Fort Loramie 0026/1, McLean 0027/1–4, Turtle Creek 0032/1–5)", src=S)
    # 0025/2 is the Village of Russia; the rest of 0024/2-3 and 0025 is Loramie Township.
    c.levy("russia-fire-district", "Loramie Township, Russia Fire District (including the Village of Russia)", P("LORAMIE TOWNSHIP", "RUSSIA VILLAGE"), "Renewal",
           "Fire apparatus, appliances, buildings or sites, water supply, and permanent, part-time or volunteer firefighters.",
           "1.74 mills", "5 years, commencing in 2027", "2028", est("$93,846", "$36"),
           area="Loramie Township Russia Fire District (precincts 0024/2–3, 0025/1–5)", src=S)
    # The notice calls this levy "ADDITIONAL"; the sample ballots say "Proposed Tax Levy (Renewal)" (commencing 2026, first due 2027). The ballot is used.
    # 0035/2 is Lockington Village; Russia Village (0025/2) is not in the district.
    c.levy("houston-ambulance-district", "Houston Joint Ambulance District", P("LORAMIE TOWNSHIP", "WASHINGTON TOWNSHIP", "LOCKINGTON VILLAGE"), "Renewal",
           "Ambulance and emergency medical services.", "2 mills", "5 years, commencing in 2026", "2027", est("$218,679", "$50"),
           area="Houston Joint Ambulance District (Loramie 0024/1–3, 0025/1 and 0025/3–5; Washington 0035/1–3)",
           note="The Board's 46-day notice lists this levy as additional; the sample ballot says renewal.", src=S)
    return c
