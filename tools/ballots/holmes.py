from lib import County, NOTE_ORDER, NOTE_PLACES

SITE = "https://www.boe.ohio.gov/holmes/"
NOTICE = "https://www.boe.ohio.gov/holmes/c/upload/FWAB_11November46Day.pdf"
ELECTION_NOTICE = "https://www.boe.ohio.gov/holmes/c/upload/Election_NoticeofElection.pdf"
BALLOTS = "https://lookup.boe.ohio.gov/vtrapp/holmes/ballotlist.aspx"


def build():
    # Raw names: townships are bare ("BERLIN", "WALNUT CREEK"; default bare="Township"), villages end in VILLAGE.
    # "KILLBUCK" (Killbuck Township) and "KILLBUCK VILLAGE" stay separate places. Default display names are right, so no renames.
    # Precincts are whole townships (001-018; Berlin and Millersburg have two each) with numbered splits (e.g. 00704):
    # villages vote in their township's precinct (Baltic in 003 Clark, Holmesville in 007 Prairie, Killbuck in 008 Killbuck,
    # Glenmont in 014 Richland, Loudonville in 018 Washington, Nashville in 009 Knox and 018 Washington).
    c = County("holmes", "Holmes", "39075")
    c.src("holmes-46day", "Holmes County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election (revised 10/15/2026)", NOTICE)
    c.src("holmes-notice", "Holmes County Board of Elections: notice of election on issues and local option questions, November 3, 2026 General Election", ELECTION_NOTICE)
    c.src("holmes-ballots", "Holmes County Board of Elections: precinct sample ballots, November 3, 2026 General Election", BALLOTS)
    S = ["holmes-46day"]; I = ["holmes-46day", "holmes-notice", "holmes-ballots"]
    c.links = [
        {"label": "Board of Elections", "url": SITE},
        {"label": "Election information", "url": "https://www.boe.ohio.gov/holmes/election-info/"},
        {"label": "Notice of election (issues)", "url": ELECTION_NOTICE},
        {"label": "Sample ballots by precinct", "url": BALLOTS},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://www.boe.ohio.gov/holmes/election-info/election-results/"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it, "
               "checked against the Board's notice of election and its precinct sample ballots. Issue details are summarised from the ballot wording.",
               NOTE_ORDER, NOTE_PLACES,
               "Holmes County's ballots do not number local issues (only statewide Issue 3 is numbered); see your sample ballot for the order of the issues."]
    P = c.p; D = c.district; SD = c.sd
    NP = " · no party label on the ballot"
    est = lambda total, per: f"{total} a year; {per} for each $100,000 of market value"

    # --- Federal, state legislative, appeals (the 19th Senate, 98th House and 5th Appeals districts cover the whole county;
    #     Congress: 6th = precincts 003 Clark, 013 Paint, 01601-01602 Saltcreek, 017 Walnut Creek; 12th = the rest) ---
    c.contest("congress-6", "U.S. House", "Representative to Congress", [("Elizabeth Kirtley", "DEM"), ("Michael A. Rulli", "REP")], detail="6th District", places=D("cong", 6), src=S)
    c.contest("congress-12", "U.S. House", "Representative to Congress", [("Troy Balderson", "REP"), ("Jerrad Christian", "DEM")], detail="12th District", places=D("cong", 12), src=S)
    c.contest("senate-19", "Ohio General Assembly", "State Senator", [("Scott Charland", "DEM"), ("Ryan Rivers", "REP")], detail="19th District", src=S)
    c.contest("rep-98", "Ohio General Assembly", "State Representative", [("Scott Grund", "DEM"), ("Mark Hiner", "REP")], detail="98th District", src=S)
    c.contest("appeals-5", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Matthew George", "REP")], detail="5th District · term commencing February 9, 2027", src=S)

    # --- County offices and judges ---
    c.contest("commissioner", "County offices", "County Commissioner", [("Dave Hall", "REP")], detail="Full term commencing January 1, 2027", src=S)
    c.contest("auditor", "County offices", "County Auditor", [("Jackie McKee", "REP")], detail="Full term commencing March 8, 2027", src=S)
    c.contest("sheriff", "County offices", "Sheriff", [("Richard L. Haun Jr.", "REP")], detail="Unexpired term ending December 31, 2028", src=S)
    c.contest("cp-general-dr", "Court of Common Pleas", "Judge of the Court of Common Pleas, General and Domestic Relations Division", ["Sean Warner"],
              detail="Full term commencing February 9, 2027" + NP, src=S)
    c.contest("cp-probate-juvenile", "Court of Common Pleas", "Judge of the Court of Common Pleas, Probate and Juvenile Division", ["Thomas C. Lee"],
              detail="Full term commencing February 9, 2027" + NP, src=S)

    # --- Countywide ---
    c.issue("county-sales-tax", "question", "Holmes County", "Sales and use tax: renewal of 0.25% for county roads and bridges, 5 years", "county",
            area="All of Holmes County",
            text="Shall the resolution of the Holmes County Commissioners proposing a continuation of an existing 0.25 per cent sales and use tax be approved? "
                 "(For the acquisition, construction, equipping or repair of permanent improvements, to-wit, the construction, reconstruction, resurfacing and repair "
                 "of all roads and bridges within the county other than state roads and bridges, for a period of 5 years.)", src=I)

    # --- School districts, library, JVSD (shared with neighbouring counties; ids and wording as in ashland.py, knox.py, richland.py, wayne.py) ---
    LP = SD("LOUDONVILLE-PERRYSVILLE EX VILL SD (ASHLAND)")
    LP_AREA = "Knox Township (split 00902), Washington Township (splits 01803, 01804)"
    c.issue("loudonville-perrysville-bond-income-tax", "levy", "Loudonville-Perrysville Exempted Village School District (Ashland, Knox and Richland counties)",
            "School district income tax (0.25%, 30 years) and bond issue ($16,400,000)", LP, area=LP_AREA,
            levy={"type": "Income tax and bond issue", "purpose": "Income tax for current expenses; bonds for constructing, renovating, repairing, expanding, furnishing and equipping school facilities and improving their sites.",
                  "mills": "2.85 mills (bond, estimated average)", "term": "Income tax 30 years from January 1, 2027; bonds up to 37 years",
                  "estimate": "$16,400,000 principal; $100 for each $100,000 of market value (bond)"},
            text="Shall Loudonville-Perrysville Exempted Village School District be authorized to do both of the following: (1) Impose an annual income tax of 0.25% on the school district "
                 "income of individuals, for a period of 30 years, beginning January 1, 2027, for the purpose of current expenses? (2) Issue bonds for the purpose of constructing school "
                 "facilities, renovating, repairing, expanding, improving, and constructing additions to school facilities; furnishing and equipping; and improving the sites thereof the same "
                 "in the principal amount of $16,400,000, to be repaid annually over a maximum period of 37 years, and levy a property tax outside the ten-mill limitation estimated by the "
                 "county auditor to average over the bond repayment period 2.85 mills for each $1 of taxable value, which amounts to $100 for each $100,000 of the county auditor's market "
                 "value, to pay the annual debt charges on the bonds, and to pay debt charges on any notes issued in anticipation of those bonds?", src=I)
    # The library's precincts in the notice are exactly the Loudonville-Perrysville district's.
    c.levy("loudonville-library", "Loudonville Public Library (Ashland, Knox and Richland counties)", LP, "Renewal", "Current expenses.", "0.8 mill", "5 years, commencing in 2027", "2028",
           estimate="$178,719 a year; $19 per $100,000 of market value", area=LP_AREA, src=I)
    c.issue("triway-lsd-income", "question", "Triway Local School District (Wayne and Holmes)", "School district income tax: 0.75% additional, 3 years, for current expenses",
            SD("TRIWAY LOCAL SD (WAYNE)"), area="Prairie Township (split 00702)",
            text="Shall an annual income tax of 0.75% on the earned income of individuals residing in the school district be imposed by the Triway Local School District, "
                 "for 3 years, beginning January 1, 2027, for the purpose of current expenses?", src=I)
    # The JVSD is not in the voter file; placed from the notice's precinct list (splits 00701, 00702, 00704 of Prairie, which take in
    # Holmesville Village at 00704, and 01602, 01604 of Saltcreek).
    c.levy("wayne-jvsd", "Wayne County Joint Vocational School District (Wayne, Ashland, Holmes, Medina and Stark)", P("PRAIRIE", "HOLMESVILLE VILLAGE", "SALTCREEK"),
           "Renewal", "General permanent improvements.", "0.5 mill", "5 years, commencing in 2027", "2028", est("$1,480,860", "$11"),
           area="Prairie Township (splits 00701, 00702, 00704), Saltcreek Township (splits 01602, 01604)", src=I)

    # --- Village of Holmesville (split 00704). The ballot says "current expenses"; the Board's notice of election names the fund. ---
    HV = P("HOLMESVILLE VILLAGE")
    c.levy("holmesville-street-lights", "Village of Holmesville", HV, "Renewal", "Current expenses (street light fund).", "2 mills", "5 years, commencing in 2027", "2028",
           est("$9,259", "$32"), area="Holmesville Village (Prairie Township split 00704)", src=I)
    c.levy("holmesville-street-maintenance", "Village of Holmesville", HV, "Renewal", "Current expenses (street maintenance fund).", "2.5 mills", "5 years, commencing in 2027", "2028",
           est("$12,950", "$45"), area="Holmesville Village (Prairie Township split 00704)", src=I)

    # --- Townships (township-wide levies are voted on by the whole township precinct, villages included, unless the ballot excludes them) ---
    FIRE_EMS = "Fire protection, the purchase of ambulance equipment, or the provision of ambulance or emergency medical services."
    ROADS = "General construction, reconstruction, resurfacing, and repair of streets, roads, and bridges."
    c.levy("killbuck-twp-fire", "Killbuck Township", P("KILLBUCK", "KILLBUCK VILLAGE"), "Renewal", FIRE_EMS, "3.5 mills", "5 years, commencing in 2027", "2028",
           est("$154,348", "$72"), area="Killbuck Township, including Killbuck Village (precinct 008, splits 00801, 00802)", src=I)
    c.levy("killbuck-twp-roads", "Killbuck Township, excluding Killbuck Village", P("KILLBUCK"), "Additional", ROADS, "1.55 mills", "5 years, commencing in 2026", "2027",
           est("$73,570", "$54"), area="Killbuck Township outside Killbuck Village (split 00801)", src=I)
    c.levy("monroe-twp-roads", "Monroe Township", P("MONROE"), "Renewal", ROADS, "1.5 mills", "5 years, commencing in 2027", "2028",
           est("$48,462", "$22"), area="Monroe Township (precinct 012)", src=I)
    c.levy("paint-twp-roads", "Paint Township", P("PAINT"), "Renewal", "General construction, reconstruction, resurfacing, and repair of streets and roads.", "2 mills",
           "5 years, commencing in 2027", "2028", est("$251,579", "$37"), area="Paint Township (precinct 013)", src=I)
    c.levy("prairie-twp-fire", "Prairie Township", P("PRAIRIE", "HOLMESVILLE VILLAGE"), "Renewal", FIRE_EMS, "2 mills", "5 years, commencing in 2027", "2028",
           est("$118,748", "$31"), area="Prairie Township, including Holmesville Village (precinct 007, all splits)", src=I)
    RI = P("RICHLAND", "GLENMONT VILLAGE")
    RI_AREA = "Richland Township, including Glenmont Village (precinct 014, all splits)"
    c.levy("richland-twp-fire", "Richland Township", RI, "Renewal", "Fire protection and emergency medical services.", "0.5 mill", "5 years, commencing in 2027", "2028",
           est("$14,786", "$10"), area=RI_AREA, src=I)
    c.levy("richland-twp-cemeteries", "Richland Township", RI, "Renewal", "Maintaining and operating cemeteries.", "0.25 mill", "5 years, commencing in 2027", "2028",
           est("$7,393", "$5"), area=RI_AREA, src=I)
    c.levy("saltcreek-twp-roads", "Saltcreek Township", P("SALTCREEK"), "Renewal", ROADS, "1 mill", "5 years, commencing in 2027", "2028",
           est("$139,204", "$22"), area="Saltcreek Township (precinct 016, all splits)", src=I)
    WA = P("WASHINGTON", "LOUDONVILLE VILLAGE", "NASHVILLE VILLAGE")
    c.levy("washington-twp-roads", "Washington Township", WA, "Renewal", ROADS, "2 mills", "5 years, commencing in 2027", "2028",
           est("$116,595", "$35"), area="Washington Township, including its parts of Loudonville and Nashville villages (precinct 018, all splits)", src=I)

    # --- Local liquor options (Washington Township precinct 018, all splits; the business is in Nashville) ---
    for id, title, text in [
        ("liquor-washington-buckeye-deli", "Local liquor option: Buckeye Deli & Pizza",
         "Sale of beer, wine and mixed beverages, and spirituous liquor by Buckeye Deli & Pizza, LLC (D-5 permit applicant, on/off-premise sales), "
         "a bar, restaurant/deli and carry-out store at 124 E Millersburg St, Nashville."),
        ("liquor-washington-buckeye-deli-sunday", "Local liquor option: Buckeye Deli & Pizza (Sunday)",
         "Sunday sale of beer, wine and mixed beverages, and spirituous liquor by Buckeye Deli & Pizza, LLC (D-6 permit applicant, on/off-premise sales), "
         "a bar, restaurant/deli and carry-out store at 124 E Millersburg St, Nashville."),
    ]:
        c.issue(id, "liquor", "Washington Township", title, WA, area="Washington Township precinct (018, all splits)", text=text, src=I)
    return c
