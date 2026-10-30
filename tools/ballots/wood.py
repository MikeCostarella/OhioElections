from lib import County, NOTE_ORDER, NOTE_PLACES

SITE = "https://boe.woodcountyohio.gov/"
NOTICE = "https://boe.woodcountyohio.gov/DocumentCenter/View/1022/46-Day-Notice"
CAND = "https://boe.woodcountyohio.gov/DocumentCenter/View/1006/Candidate-List"
ISSUES = "https://boe.woodcountyohio.gov/DocumentCenter/View/1005/Q-and-I-List"


def build():
    # The SoS file lists unincorporated township voters by precinct ("PERRYSBURG TWP BELMONT", "PRBG TWP STARBRIGHT");
    # "PORTAGE WEST" is Portage Township's west precinct (Board precinct 800, Portage West).
    rename = {
        "BLOOM TWP NORTH": "Bloom Township", "BLOOM TWP SOUTH": "Bloom Township",
        "GRAND RAPIDS TWP PARK": "Grand Rapids Township",
        "HENRY TWP HAMMANSBURG": "Henry Township",
        "LAKE TWP EAST": "Lake Township", "LAKE TWP LATCHA": "Lake Township", "LAKE TWP NORTH": "Lake Township", "LAKE TWP UNION": "Lake Township",
        "MIDDLETON TWP DUNBRIDGE": "Middleton Township", "MIDDLETON TWP NORTH": "Middleton Township",
        "MIDDLETON TWP SOUTH": "Middleton Township", "MIDDLETON TWP WEST": "Middleton Township",
        "MONTGOMERY TWP NE": "Montgomery Township", "MONTGOMERY TWP SE": "Montgomery Township", "MONTGOMERY TWP WEST": "Montgomery Township",
        "PERRY TWP EAST": "Perry Township", "PERRY TWP PERRY": "Perry Township",
        "PERRYSBURG TWP BELMONT": "Perrysburg Township", "PERRYSBURG TWP ECKEL": "Perrysburg Township", "PERRYSBURG TWP FORD": "Perrysburg Township",
        "PERRYSBURG TWP FT MEIGS": "Perrysburg Township", "PERRYSBURG TWP GLENWOOD": "Perrysburg Township", "PERRYSBURG TWP HAMLET": "Perrysburg Township",
        "PERRYSBURG TWP NORTH": "Perrysburg Township", "PERRYSBURG TWP SOUTH": "Perrysburg Township",
        "PRBG TWP FALLEN TIMBERS": "Perrysburg Township", "PRBG TWP STARBRIGHT": "Perrysburg Township",
        "PORTAGE TWP EAST": "Portage Township", "PORTAGE WEST": "Portage Township",
        "TROY TWP NORTH": "Troy Township", "TROY TWP SOUTH": "Troy Township",
        "WESTON TWP WILLOW": "Weston Township",
    }
    c = County("wood", "Wood", "39173", rename=rename)
    c.src("wood-46day", "Wood County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election (September 18, 2026)", NOTICE)
    c.src("wood-cand", "Wood County Board of Elections: certified candidate list, November 3, 2026 General Election (certified 8/26/2026)", CAND)
    c.src("wood-issues", "Wood County Board of Elections: certified questions and issues list, November 3, 2026 General Election (September 3, 2026)", ISSUES)
    C = ["wood-46day", "wood-cand"]; I = ["wood-46day", "wood-issues"]
    c.links = [
        {"label": "Board of Elections", "url": SITE},
        {"label": "Am I registered? / What's on my ballot? / Where do I vote?", "url": "https://votertools.woodcountyohio.gov/TEDElectionLink/VoterServices/launchpad"},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://boe.woodcountyohio.gov/174/Election-Results"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it, "
               "checked against the Board's certified candidate list and questions and issues list. Issue wording is the Board's summary; the full wording is on the sample ballot.",
               NOTE_ORDER, NOTE_PLACES,
               "The Board's notice and issues list do not give local issue numbers; see your sample ballot for them."]
    P = c.p; D = c.district; SD = c.sd

    # --- Federal, state legislative, appeals (no State Senate race in Wood County this year) ---
    c.contest("congress-5", "U.S. House", "Representative to Congress", [("Bob Latta", "REP"), ("Brian A. Shaver", "DEM"), ("Michael J. Veloff", "LIB")],
              detail="5th District", places=D("cong", 5), src=C)
    c.contest("congress-9", "U.S. House", "Representative to Congress", [("Marcy Kaptur", "DEM"), ("Derek Merrin", "REP")],
              detail="9th District", places=D("cong", 9), src=C)
    c.contest("rep-44", "Ohio General Assembly", "State Representative", [("David J. Fournier", "DEM"), ("Edward L. Schimmel", "REP"), ("Lyndsey A. Stough", "Nonparty")],
              detail="44th District (also in Lucas County)", places=D("rep", 44), src=C)
    c.contest("rep-75", "Ohio General Assembly", "State Representative", [("Haraz N. Ghanbari", "REP"), ("Richard J. Rettig", "DEM")],
              detail="75th District", places=D("rep", 75), src=C)
    c.contest("appeals-6-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Michael R. Goulding", "REP")], detail="6th District · full term commencing February 9, 2027", src=C)
    c.contest("appeals-6-0210", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Myron C. Duhart", "DEM"), ("CJ Kamm", "REP")], detail="6th District · full term commencing February 10, 2027", src=C)

    # --- County offices ---
    c.contest("commissioner", "County offices", "County Commissioner", [("Joseph R. DeMare", "Nonparty"), ("Ryan E. Lee", "REP"), ("Brenna Reynolds", "DEM")],
              detail="Term commencing January 1, 2027", src=C)
    c.contest("auditor", "County offices", "County Auditor", [("Matthew R. Oestreich", "REP"), ("Mark Wongrowski", "DEM")], detail="Term commencing March 8, 2027", src=C)
    NP = " · no party label on the ballot"
    c.contest("cp-gen", "Court of Common Pleas", "Judge of the Court of Common Pleas", ["Paul A. Dobson", "Joel M. Kuhlman"], detail="Term commencing January 1, 2027" + NP, src=C)
    c.contest("cp-probate", "Court of Common Pleas", "Judge of the Court of Common Pleas, Probate Division", ["Megan E. Newlove", "Doug Ruck"], detail="Term commencing February 9, 2027" + NP, src=C)

    # --- Issues (unnumbered in the Board's documents; listed in the Board's order) ---
    c.levy("wood-senior", "Wood County", "county", "Renewal", "Providing or maintaining senior services or facilities.", "1 mill", "5 years, commencing in 2026", "2027", src=I)
    # Library district from the notice's precinct list (Board precinct numbers: 010-146 Bowling Green, 210 Center, 230 Freedom,
    # 340 Jackson, 370-432 Lake Twp/Millbury/Walbridge, 440 Liberty, 460/490 Middleton, 500 Milton, 550/590 Montgomery NE/SE,
    # 601 Perry East, 630-671 Perrysburg Twp, 761 Plain, 800 Portage West, 810-830 Northwood, 900 Troy North, 960 Webster).
    # Partly-included precincts are shown for the whole place, with the villages inside them (Bradner, Custar, West Milton).
    LIB = P("BOWLING GREEN CITY", "CENTER TOWNSHIP", "FREEDOM TOWNSHIP", "JACKSON TWP", "HOYTVILLE VILLAGE", "LAKE TWP EAST", "MILLBURY VILLAGE",
            "WALBRIDGE VILLAGE", "LIBERTY TWP", "MIDDLETON TWP NORTH", "MILTON TWP", "CUSTAR VILLAGE", "WEST MILTON VILLAGE", "MONTGOMERY TWP NE",
            "BRADNER VILLAGE", "RISINGSUN VILLAGE", "PERRY TWP EAST", "PERRYSBURG TWP NORTH", "PLAIN TWP", "PORTAGE WEST", "PORTAGE VILLAGE",
            "NORTHWOOD CITY", "TROY TWP NORTH", "WEBSTER TWP")
    c.levy("wcdpl", "Wood County District Public Library", LIB, "Renewal", "Current expenses.", "0.8 mill", "6 years, commencing in 2027", "2028",
           area="Wood County District Public Library district: Bowling Green, Lake Township (with Millbury and Walbridge), Northwood (except part of precinct D), "
                "Jackson Township and Portage West, and parts of Center, Freedom, Liberty, Middleton, Milton, Montgomery, Perry, Perrysburg, Plain, Troy and Webster townships", src=I)
    c.levy("bowling-green-parks", "City of Bowling Green", P("BOWLING GREEN CITY"), "Renewal and increase", "Recreational purposes of Bowling Green City Parks and Recreation.",
           "2.95 mills (renewal of 2 mills plus an increase of 0.95 mill)", "5 years, commencing in 2026", "2027", src=I)
    c.levy("fostoria-current", "City of Fostoria (Hancock, Seneca and Wood)", P("FOSTORIA CITY"), "Renewal", "Current expenses.", "6 mills", "5 years, commencing in 2027", "2028",
           area="Fostoria City (Wood County part)", src=I)
    c.levy("center-fire", "Center Township", P("CENTER TOWNSHIP"), "Renewal", "Fire and ambulance.", "1.2 mills", "4 years, commencing in 2026", "2027", src=I)
    c.levy("freedom-fire", "Freedom Township", P("FREEDOM TOWNSHIP", "PEMBERVILLE VILLAGE"), "Renewal", "Fire and ambulance.", "3 mills", "3 years, commencing in 2026", "2027",
           area="Freedom Township (including Pemberville Village)", src=I)
    c.levy("jackson-roads", "Jackson Township", P("JACKSON TWP", "HOYTVILLE VILLAGE"), "Renewal", "Streets and bridges.", "3 mills", "5 years, commencing in 2027", "2028",
           area="Jackson Township (including Hoytville Village)", src=I)
    c.levy("milton-roads", "Milton Township", P("MILTON TWP", "CUSTAR VILLAGE", "WEST MILTON VILLAGE"), "Renewal", "Streets and bridges.", "2.5 mills", "5 years, commencing in 2026", "2027",
           area="Milton Township (including Custar and West Milton villages)", src=I)
    c.levy("perry-fire", "Perry Township", P("PERRY TWP EAST", "PERRY TWP PERRY", "WEST MILLGROVE VILLAGE"), "Renewal", "Fire protection.", "2 mills", "3 years, commencing in 2027", "2028",
           area="Perry Township (including West Millgrove Village)", src=I)
    c.levy("perrysburg-twp-fire", "Perrysburg Township", P("PERRYSBURG TWP NORTH"), "Additional", "Fire and EMS.", "3.5 mills", "5 years, commencing in 2026", "2027", src=I)
    c.levy("webster-fire", "Webster Township", P("WEBSTER TWP"), "Renewal", "EMS and fire.", "3.1 mills", "3 years, commencing in 2027", "2028", src=I)
    c.levy("grand-rapids-streets", "Village of Grand Rapids", P("GRAND RAPIDS VILLAGE"), "Renewal", "Street construction and reconstruction.", "2 mills", "5 years, commencing in 2027", "2028", src=I)
    RS = P("RISINGSUN VILLAGE")
    c.levy("risingsun-current-1", "Village of Risingsun", RS, "Renewal", "Current expenses.", "1.3 mills", "4 years, commencing in 2027", "2028", src=I)
    c.levy("risingsun-current-2", "Village of Risingsun", RS, "Renewal", "Current expenses.", "6.3 mills", "5 years, commencing in 2027", "2028", src=I)
    c.levy("risingsun-parks", "Village of Risingsun", RS, "Additional", "Maintenance and improvements of parks.", "0.5 mill", "5 years, commencing in 2027", "2028", src=I)

    # The notice also lists precinct Montgomery NE split 3 (550.3); the voter file has no Montgomery voters in the district.
    c.issue("eastwood-bond", "levy", "Eastwood Local School District", "School district income tax (0.5%) and bond issue ($54,965,000)",
            SD("EASTWOOD LOCAL SD (WOOD)") + P("MONTGOMERY TWP NE"),
            levy={"type": "Income tax and bond issue", "purpose": "Income tax; bonds for constructing school facilities.",
                  "mills": "6.49 mills (bond)", "term": "Income tax beginning January 1, 2027; bonds up to 37 years", "estimate": "$54,965,000 principal"},
            text="Income tax of 0.5% beginning January 1, 2027, and bonds of $54,965,000 for constructing school facilities, repaid over a maximum of 37 years, with a levy estimated at 6.49 mills.", src=I)
    # The notice also lists precinct Northwood A split 2 (810.2); the voter file has no Northwood voters in the district.
    c.issue("lake-income-tax", "question", "Lake Local School District", "School district income tax: 1%, continuing", SD("LAKE LOCAL SD (WOOD)") + P("NORTHWOOD CITY"),
            text="Shall an annual income tax of 1% on the earned income of individuals residing in the school district be imposed by the Lake Local School District, for a continuing period of time, beginning January 1, 2027?", src=I)
    c.issue("mccomb-bond", "levy", "McComb Local School District (Hancock and Wood)", "School district income tax (0.25%) and bond issue ($23,815,000)", SD("MCCOMB LOCAL SD (HANCOCK)"),
            area="McComb Local School District (Wood County part: Jackson Township precincts 340 splits 1 and 4)",
            levy={"type": "Income tax and bond issue", "purpose": "Income tax; bonds for constructing school facilities.",
                  "mills": "6.99 mills (bond)", "term": "Income tax beginning January 1, 2027; bonds up to 37 years", "estimate": "$23,815,000 principal"},
            text="Income tax of 0.25% beginning January 1, 2027, and bonds of $23,815,000 for constructing school facilities, repaid over a maximum of 37 years, with a levy estimated at 6.99 mills.", src=I)
    c.issue("north-baltimore-income-tax", "question", "North Baltimore Local School District", "School district income tax: 1%, 5 years, for current expenses", SD("NORTH BALTIMORE LOCAL SD (WOOD)"),
            text="Shall an annual income tax of 1% on the earned income of individuals residing in the school district be imposed by the North Baltimore Local School District, for 5 years, beginning January 1, 2028, for the purpose of current expenses?", src=I)
    c.levy("lake-twp-roads", "Lake Township Road District", P("LAKE TWP EAST"), "Additional", "Streets and roads.", "2 mills", "5 years, commencing in 2026", "2027",
           area="Lake Township (unincorporated: East, North, Latcha and Union precincts)", src=I)
    c.levy("middleton-twp-roads", "Middleton Township Road District", P("MIDDLETON TWP NORTH"), "Renewal", "Streets and bridges.", "2 mills", "3 years, commencing in 2026", "2027",
           area="Middleton Township (unincorporated: precincts North, South and Dunbridge)", src=I)
    # Placed from the notice's precinct list: all of Montgomery Township precincts West, NE and SE.
    c.levy("south-east-ambulance", "South East Ambulance District", P("MONTGOMERY TWP NE", "BRADNER VILLAGE", "WAYNE VILLAGE", "RISINGSUN VILLAGE"), "Additional",
           "Ambulance service and emergency medical services.", "3 mills", "5 years, commencing in 2026", "2027",
           area="Montgomery Township precincts West, NE and SE (including Bradner, Risingsun and Wayne villages)", src=I)
    c.issue("liquor-woodbury-market", "liquor", "Lake Township", "Local liquor option: Woodbury Market Inc. (Sunday)", P("LAKE TWP EAST"), area="Lake Township East precinct (370)",
            text="Sunday sales by Woodbury Market Inc. in this precinct.", src=I)
    c.issue("liquor-pinky-blinders", "liquor", "City of Perrysburg", "Local liquor option: Pinky Blinders, LLC (Sunday)", P("PERRYSBURG CITY"), area="Perrysburg precinct B (700)",
            text="Sunday sales by Pinky Blinders, LLC in this precinct.", src=I)
    return c
