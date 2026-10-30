from lib import County, NOTE_ORDER, NOTE_PLACES

SITE = "https://www.mercercountyoh.gov/county-services/elections/"
NOTICE = "https://www.mercercountyoh.gov/bskpdf/46-day--updated-10-15-26/"


def build():
    # Default display names are right: "BLACKCREEK TWP" -> "Blackcreek Township", "ST. HENRY VILLAGE" -> "St. Henry Village".
    # Burkettsville Village is shared with Darke County (darke.py); nothing on Mercer's ballot is Burkettsville-only.
    c = County("mercer", "Mercer", "39107")
    c.src("mercer-46day", "Mercer County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election (updated 10/15/2026)", NOTICE)
    S = ["mercer-46day"]
    c.links = [
        {"label": "Board of Elections", "url": SITE},
        {"label": "Voter information", "url": "https://www.mercercountyoh.gov/county-services/elections/board-of-elections-voter-information/"},
        {"label": "Sample ballot (look up your registration)", "url": "https://www.mercercountyoh.gov/county-services/elections/sample-ballot/"},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://www.mercercountyoh.gov/county-services/elections/board-of-elections-election-results/"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it "
               "and gives the ballot wording of each issue.",
               NOTE_ORDER, NOTE_PLACES,
               "The Board's notice does not give local issue numbers; see your sample ballot for them."]
    P = c.p

    # All of Mercer County is in the 4th Congressional, 84th House and 12th Senate districts; the 12th Senate seat is not up in 2026.
    # The notice prints no party for Tracey L. Tackett; named and tagged as in allen.py/auglaize.py/shelby.py.
    c.contest("congress-4", "U.S. House", "Representative to Congress", [("Jim Jordan", "REP"), ("Joshua D. Kolasinski", "DEM"), ("Tracey L. Tackett", "Nonparty")],
              detail="4th District", src=S)
    c.contest("rep-84", "Ohio General Assembly", "State Representative", [("Arienne C. Childrey", "DEM"), ("Angie King", "REP")], detail="84th District", src=S)
    c.contest("appeals-3-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Mark C. Miller", "REP")], detail="3rd District · full term commencing February 9, 2027", src=S)

    # --- County offices ---
    c.contest("commissioner", "County offices", "County Commissioner", [("David Buschur", "REP")], detail="Full term commencing January 1, 2027", src=S)
    # The notice prints "FTC 3/14/2027" for the auditor (Auglaize's and Darke's notices give March 8, 2027); kept as the Board printed it.
    c.contest("auditor", "County offices", "County Auditor", [("Jeffrey S. Larmore", "REP")], detail="Full term commencing March 14, 2027", src=S)
    c.contest("coroner", "County offices", "County Coroner", [("Alyssa Tobe", "REP")], detail="Unexpired term ending December 31, 2028", src=S)
    NP = " · no party label on the ballot"
    # The notice prints "R" after Gilmore; Common Pleas judges carry no party label on the general-election ballot.
    c.contest("cp-probate-juvenile", "Court of Common Pleas", "Judge of the Court of Common Pleas, Probate/Juvenile Division", ["Matthew L. Gilmore"],
              detail="Full term commencing February 9, 2027" + NP, src=S)

    # --- Local issues (unnumbered in the notice; listed in the notice's order) ---
    est = lambda total, per: f"{total} a year; {per} for each $100,000 of the county auditor's market value"
    c.levy("center-twp-fire", "Township of Center", P("CENTER TWP"), "Renewal", "Fire protection.", "1.95 mills",
           "5 years, commencing in 2027", "2028", est("$68,214", "$38"), area="Center Township (precinct Center 12.1)", src=S)
    # Precinct Dublin 27.1 only: Rockford Village votes in its own precinct and is not on this levy.
    c.levy("dublin-twp-fire", "Township of Dublin", P("DUBLIN TWP"), "Renewal", "Fire protection.", "2.2 mills",
           "5 years, commencing in 2027", "2028", est("$111,355", "$46"), area="Dublin Township (precinct Dublin 27.1)", src=S)
    c.levy("hopewell-twp-fire", "Township of Hopewell", P("HOPEWELL TWP"), "Renewal and increase",
           "Fire protection (renewal of 1.95 mills and an increase of 0.30 mill).", "2.25 mills",
           "5 years, commencing in 2027", "2028", est("$94,550", "$49"), area="Hopewell Township (precincts Hopewell 33.1, 33.2)", src=S)
    c.levy("liberty-twp-fire", "Township of Liberty", P("LIBERTY TWP"), "Renewal", "Fire protection.", "1.4 mills",
           "5 years, commencing in 2027", "2028", est("$40,274", "$27"), area="Liberty Township (precincts Liberty 34.1–34.3)", src=S)
    # Marion East 29.1–29.4 and Marion West 30.1–30.2; Chickasaw Village is not in the notice's precinct list.
    c.levy("marion-twp-fire", "Township of Marion", P("MARION TWP"), "Renewal", "Fire protection.", "2.4 mills",
           "5 years, commencing in 2027", "2028", est("$272,060", "$54"), area="Marion Township (precincts Marion East 29.1–29.4, Marion West 30.1–30.2)", src=S)
    c.levy("mendon-operating", "Village of Mendon", P("MENDON VILLAGE"), "Renewal", "Current operating expenses.", "2.6 mills",
           "5 years, commencing in 2026", "2027", est("$10,296", "$33"), area="Mendon Village (precinct Mendon Village 28.1)", src=S)
    return c
