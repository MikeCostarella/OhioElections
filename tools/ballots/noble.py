from lib import County, NOTE_ORDER, NOTE_PLACES

NOTICE = "https://www.boe.ohio.gov/noble/c/upload/FWAB_11November46Day.pdf"
BALLOTS = "https://lookup.boe.ohio.gov/vtrapp/noble/ballotlist.aspx"


def build():
    # Raw SoS names display correctly by default ("DEXTER CITY VILLAGE" -> "Dexter City Village", "BELLE VALLEY VILLAGE"); no renames needed.
    c = County("noble", "Noble", "39121")
    c.src("noble-46day", "Noble County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election (revised 9/16/2026)", NOTICE)
    c.src("noble-ballots", "Noble County Board of Elections: official sample ballots for all 19 precincts (43 ballot styles), November 3, 2026 (state ballot lookup; full ballot wording)", BALLOTS)
    S = ["noble-46day", "noble-ballots"]
    c.links = [
        {"label": "Board of Elections", "url": "https://www.boe.ohio.gov/noble/"},
        {"label": "Sample ballots by precinct", "url": BALLOTS},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://www.boe.ohio.gov/noble/election-info/election-results/"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it, "
               "checked against the Board's precinct sample ballots (which give the full ballot wording and the auditor's estimates).",
               NOTE_ORDER, NOTE_PLACES,
               "The Board's notice and sample ballots do not give local issue numbers; see your sample ballot."]
    P = c.p

    # --- Federal, state legislative, appeals (whole county: 12th Congressional, 95th House, 7th Appeals; State Senate District 30 is not up) ---
    c.contest("congress-12", "U.S. House", "Representative to Congress", [("Troy Balderson", "REP"), ("Jerrad Christian", "DEM")], detail="12th District", src=S)
    c.contest("rep-95", "Ohio General Assembly", "State Representative", [("Paul Cameron", "DEM"), ("Ty Moore", "REP")], detail="95th District", src=S)
    c.contest("appeals-7-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Molly K. Johnson", "REP")], detail="7th District · full term commencing February 9, 2027", src=S)
    c.contest("appeals-7-0210", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Mark Anthony Hanni", "REP"), ("Katherine Rudzik", "DEM")], detail="7th District · full term commencing February 10, 2027", src=S)

    # --- County offices ---
    c.contest("commissioner-0101", "County offices", "County Commissioner", [("Floyd Allen Fraley", "REP")], detail="Full term commencing January 1, 2027", src=S)
    c.contest("commissioner-unexpired", "County offices", "County Commissioner", [("Brian D. Carter", "REP")], detail="Unexpired term ending January 1, 2029", src=S)
    c.contest("auditor", "County offices", "County Auditor", [("Kyle Smith", "REP")], detail="Full 4-year term commencing March 8, 2027", src=S)
    c.contest("coroner", "County offices", "County Coroner", [("Clayton Alan Spencer", "REP")], detail="Unexpired term ending December 31, 2028", src=S)
    NP = " · no party label on the ballot"
    # The notice lists Kelly Ann Riddle as (Dem); the ballot prints no party.
    c.contest("cp-0418", "Court of Common Pleas", "Judge of the Court of Common Pleas", ["Kelly Ann Riddle"], detail="Full 6-year term commencing April 18, 2027" + NP, src=S)

    # --- Issues (unnumbered; listed in the notice's order) ---
    est = lambda total, per: f"{total} a year; {per} for each $100,000 of market value"
    ALL = "Noble County (all precincts)"
    c.levy("enoch-current", "Enoch Township", P("ENOCH TOWNSHIP"), "Renewal", "Current operating expenses.", "2 mills",
           "5 years, commencing in 2027", "2028", estimate=est("$32,134", "$200"), area="Enoch precinct (014, splits 1 and 2)", src=S)
    # Precincts 002 split 2 (Brookfield/Noble, the Noble Township part), 007 Ava/Belle Valley (both splits) and 008 Maple Heights:
    # Noble Township including the Village of Belle Valley.
    c.levy("noble-twp-fire-ems", "Noble Township", P("NOBLE TOWNSHIP", "BELLE VALLEY VILLAGE"), "Renewal", "Fire protection and emergency medical services.", "0.5 mill",
           "5 years, commencing in 2027", "2028", estimate=est("$39,397", "$50"),
           area="Brookfield/Noble (002, split 2), Ava/Belle Valley (007) and Maple Heights (008) precincts", src=S,
           note="The Board's notice describes this levy as fire protection only; the ballot says fire protection and emergency medical services.")
    # Precincts 004 Center East/Sarahsville, 005 Center West and 011 split 2 (Caldwell One/Two, the part of Caldwell Village in Center Township;
    # the voter file puts 15 Caldwell Village voters in Center Township).
    c.levy("center-twp-cemetery", "Center Township", P("CENTER TOWNSHIP", "SARAHSVILLE VILLAGE", "CALDWELL VILLAGE"), "Renewal", "Cemetery operating fund.", "0.4 mill",
           "5 years, commencing in 2027", "2028", estimate=est("$26,048", "$40"),
           area="Center East/Sarahsville (004), Center West (005) and Caldwell One/Two (011, split 2 only) precincts", src=S)
    c.levy("county-osu-extension", "Noble County", "county", "Renewal",
           "Providing revenue to the Ohio Cooperative Extension Services fund for 4-H, agriculture and natural resources, home economics, and economic development.",
           "1 mill", "5 years, commencing in 2027", "2028", estimate=est("$772,962", "$100"), area=ALL, src=S)
    c.levy("county-911", "Noble County", "county", "Additional", "Maintaining and operating 911 systems and 911 dispatching.",
           "0.5 mill", "5 years, commencing in 2026", "2027", estimate=est("$433,946", "$50"), area=ALL, src=S)
    c.levy("county-senior-citizens", "Noble County", "county", "Renewal and increase",
           "Providing or maintaining senior citizens services or facilities, including the Noble County senior nutrition program, medical escort and transportation service, "
           "and maintenance and operation of the Noble County Senior Center.",
           "0.6 mill", "5 years, commencing in 2027", "2028", estimate=est("$498,939", "$60"), area=ALL, src=S,
           note="A renewal of 0.4 mill and an increase of 0.2 mill.")
    c.levy("elk-general", "Elk Township", P("ELK TOWNSHIP"), "Renewal", "General operating expenses.", "2 mills",
           "5 years, commencing in 2027", "2028", estimate=est("$16,815", "$200"), area="Elk precinct (015, splits 1–3)", src=S)
    c.levy("summerfield-current", "Village of Summerfield", P("SUMMERFIELD VILLAGE"), "Renewal", "Current operating expenses.", "4 mills",
           "5 years, commencing in 2027", "2028", estimate=est("$7,212", "$400"), area="Marion/Summerfield precinct (006, split 2 Summerfield Village only)", src=S)
    return c
