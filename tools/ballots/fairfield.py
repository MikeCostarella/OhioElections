from lib import County, NOTE_ORDER, NOTE_PLACES

NOTICE = "https://www.boe.ohio.gov/fairfield/c/upload/FWAB_11November46Day.pdf"
CAND = "https://www.boe.ohio.gov/fairfield/c/upload/Election_Candidates.pdf"


def build():
    # Raw names with trailing spaces ("COLUMBUS CITY ", "REYNOLDSBURG CITY ", "WEST RUSHVILLE VILLAGE ") and "TWP" are handled by display().
    c = County("fairfield", "Fairfield", "39045")
    c.src("fairfield-46day", "Fairfield County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election (revised 9/16/2026)", NOTICE)
    c.src("fairfield-cand", "Fairfield County Board of Elections: 2026 General Election certified candidates and issues (issues revised 9/9/2026)", CAND)
    C = ["fairfield-46day", "fairfield-cand"]; I = ["fairfield-46day", "fairfield-cand"]
    c.links = [
        {"label": "Board of Elections", "url": "https://www.boe.ohio.gov/fairfield/"},
        {"label": "Election information", "url": "https://www.boe.ohio.gov/fairfield/election-info/"},
        {"label": "Sample ballots by precinct", "url": "https://lookup.boe.ohio.gov/vtrapp/fairfield/ballotlist.aspx"},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://www.boe.ohio.gov/fairfield/election-info/election-results/"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it, "
               "checked against the Board's certified candidates and issues list. Issue wording is the Board's ballot wording, condensed where long; the full wording is on the sample ballot.",
               NOTE_ORDER, NOTE_PLACES,
               "The Board's notice gives no local issue numbers except for the two City of Columbus charter amendments (#8 and #9); see your sample ballot for the others."]
    P = c.p; D = c.district; SD = c.sd

    # --- Federal, state legislative, appeals ---
    c.contest("congress-12", "U.S. House", "Representative to Congress", [("Troy Balderson", "REP"), ("Jerrad Christian", "DEM")], detail="12th District", src=C)
    c.contest("rep-69", "Ohio General Assembly", "State Representative", [("Kevin D. Miller", "REP"), ("Amy Rigsby", "DEM")], detail="69th District (also in Licking and Perry counties)",
              places=D("rep", 69), src=C)
    c.contest("rep-73", "Ohio General Assembly", "State Representative", [("Jeff LaRe", "REP"), ("Whittney Wood", "DEM")], detail="73rd District", places=D("rep", 73), src=C)
    c.contest("appeals-5", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Matthew George", "REP")], detail="5th District · term commencing February 9, 2027", src=C)

    # --- County offices ---
    c.contest("commissioner", "County offices", "County Commissioner", [("Jeffrey Fix", "REP")], detail="Term commencing January 1, 2027", src=C)
    c.contest("auditor", "County offices", "County Auditor", [("Carri L. Brown", "REP")], detail="Term commencing March 8, 2027", src=C)
    NP = " · no party label on the ballot"
    for id, office, date, cs in [
        ("cp-gen", "General Division", "Term commencing February 9, 2027", ["David Andrew Trimmer"]),
        ("cp-probate-juvenile", "Juvenile/Probate Division", "Term commencing February 9, 2027", ["Terre L. Vandervoort"]),
    ]:
        c.contest(id, "Court of Common Pleas", f"Judge of the Court of Common Pleas, {office}", cs, detail=date + NP, src=C)

    # --- Issues (ids/titles shared with franklin.py and licking.py where it is the same question) ---
    # Pickerington LSD precincts in the notice (Columbus A–F, Liberty A/D, Pickerington, Violet) match the voter file's district.
    PICK = SD("PICKERINGTON LOCAL SD (FAIRFIELD)")
    PICK_AREA = "Columbus precincts A–F, Liberty Township A and D (Pickerington parts), Pickerington A–Q, Violet Township A–R"
    c.issue("pickerington-lsd-tax", "question", "Pickerington Local School District (Fairfield and Franklin)", "School district income tax increase: 0.75% for 10 years", PICK,
            area=PICK_AREA,
            text="Shall an annual income tax of 0.75 per cent on the school district income of individuals be imposed by Pickerington Local School District, for 10 years, "
                 "beginning January 1, 2027, for the purpose of current expenses?", src=I)
    c.levy("pickerington-library", "Pickerington Public Library (Fairfield and Franklin)", PICK, "Additional", "Current expenses.", "1.5 mills", "Continuing, commencing in 2026", "2027",
           estimate="$4,104,440 a year; $53 for each $100,000 of market value", area=PICK_AREA, src=I)

    SWL = SD("SOUTHWEST LICKING LOCAL SD (LICKING)")
    SWL_AREA = "Liberty Township A–D (Southwest Licking parts)"
    c.issue("swl-bond", "levy", "Southwest Licking Local School District (Licking and Fairfield counties)", "Bond issue: $80,710,000 for school facilities", SWL, area=SWL_AREA,
            levy={"type": "Bond issue", "purpose": "Constructing, renovating, expanding, furnishing and equipping school facilities, improving their sites, and acquiring real estate.",
                  "mills": "2.87 mills (estimated average)", "term": "Up to 35 years", "firstDue": "2027", "estimate": "$80,710,000 principal; $100 for each $100,000 of market value"},
            text="Bond issue, principal $80,710,000, maximum 35 years, estimated average 2.87 mills ($100 per $100,000 of market value), commencing in 2026, first due in 2027, for constructing "
                 "school facilities and renovating, repairing, expanding, improving, and constructing additions to school facilities; furnishing and equipping the same; improving the sites "
                 "thereof; and acquiring real estate and interests therein.", src=I)
    c.issue("swl-income-tax", "question", "Southwest Licking Local School District (Licking and Fairfield counties)",
            "School district income tax: replace the 0.75% tax on school district income with a 2% tax on earned income, continuing, for current operating expenses", SWL, area=SWL_AREA,
            text="Shall the existing tax of 0.75% on the school district income of individuals imposed by the Southwest Licking Local School District be replaced by a tax of 2% on the earned income "
                 "of individuals residing in the school district for a continuing period of time, beginning January 1, 2027, for the purpose of paying the cost of current operating expenses? "
                 "If the new tax is not approved, the existing tax will remain in effect under its original authority, for the remainder of its previously approved term.", src=I)
    # The library's Fairfield precincts in the notice are exactly the Southwest Licking parts of Liberty Township.
    c.levy("pataskala-library", "Pataskala Public Library (Licking and Fairfield counties)", SWL, "Renewal", "Current expenses of the library.", "1 mill", "5 years, commencing in 2027", "2028",
           estimate="$901,850 a year; $21 per $100,000 of market value", area=SWL_AREA, src=I)

    COL = P("COLUMBUS CITY ")
    COL_AREA = "Columbus precincts A–F (Fairfield County part)"
    c.issue("issue-8", "question", "City of Columbus", "Charter amendment (by petition): council members elected only by voters in their district", COL, number="Issue 8", area=COL_AREA,
            text="This proposed charter amendment would limit the ability to vote for candidates for Columbus City Council to only those electors living within the districts that those candidates seek to represent. Ballots within council districts would include both citywide races and the district race, and a recall election of a district council member could be started by a petition signed by district electors equal to at least 15% of the votes cast in the district in the preceding mayoral election. Shall the proposed charter amendment be approved?", src=I)
    c.issue("issue-9", "question", "City of Columbus", "Charter amendment (by Council): district-only voting for district seats, at-large seats added, 13-member Council", COL, number="Issue 9", area=COL_AREA,
            text="This proposed charter amendment would limit the ability to vote for candidates for Columbus City Council to only those electors living within the districts that those candidates seek to represent. It adds two at-large council members elected in 2027 and two more elected in 2029 (four-year terms), moving from a nine-member to an eleven- and then a thirteen-member Council; redraws the council district map in 2027 and raises the allowed population variance between districts from 1% to 7.5%; requires district candidates to have lived in their district for a year before the primary; updates expulsion, quorum and vote requirements; sets petition signature requirements (150 district / 250 at-large); and allows recall of district and at-large members by petition. Shall the proposed charter amendment be approved?", src=I)

    c.levy("buckeye-lake-current", "Village of Buckeye Lake (Licking and Fairfield counties)", P("BUCKEYE LAKE VILLAGE"), "Renewal", "Current operating expenses.", "5 mills", "5 years, commencing in 2027", "2028",
           estimate="$409,214 a year; $105 per $100,000 of market value", area="Walnut Township precinct A (Buckeye Lake Village part)", src=I)
    c.levy("madison-twp-roads", "Madison Township (unincorporated territory)", P("MADISON TWP"), "Additional", "General construction, reconstruction, resurfacing and repair of streets, roads and bridges.",
           "1.5 mills", "Continuing period of time, commencing in 2026", "2027", estimate="$121,963 a year; $53 per $100,000 of market value", area="Madison Township precinct A", src=I)
    # Precinct PL-B.FU-PVP holds the Pleasant Township part of Pleasantville Village.
    c.levy("pleasant-twp-fire", "Pleasant Township", P("PLEASANT TWP", "PLEASANTVILLE VILLAGE"), "Additional",
           "Providing and maintaining firefighting facilities, equipment, and personnel, including paramedics and other emergency medical services.",
           "2 mills", "Continuing period of time, commencing in 2026", "2027", estimate="$689,992 a year; $70 per $100,000 of market value",
           area="Pleasant Township A–F (includes the Pleasant Township part of Pleasantville Village)", src=I)

    # --- Local liquor options (Lancaster) ---
    LAN = P("LANCASTER CITY")
    for id, prec, title, text in [
        ("liquor-los-mariachis", "Lancaster precinct 1-E", "Local liquor option: Los Mariachis",
         "Sale of beer, wine and mixed beverages, and spirituous liquor by Los Mariachis of Lancaster, L.L.C., dba Los Mariachis (D-1, D-2, D-3 permits), a restaurant at 1707 River Valley Circle North, Lancaster."),
        ("liquor-los-mariachis-sunday", "Lancaster precinct 1-E", "Local liquor option: Los Mariachis (Sunday)",
         "Sunday sale of wine and mixed beverages and spirituous liquor by Los Mariachis of Lancaster, L.L.C., dba Los Mariachis (D-6 permit), a restaurant at 1707 River Valley Circle North, Lancaster."),
        ("liquor-walmart-3792", "Lancaster precinct 1-E", "Local liquor option: Walmart 3792 (Sunday)",
         "Sunday sale of wine and mixed beverages by Wal Mart Stores East, L.P., dba Walmart 3792 (D-6 permit), a grocery store at 2687 N. Memorial Drive, Lancaster."),
        ("liquor-east-lancaster-duchess", "Lancaster precinct 5-A", "Local liquor option: East Lancaster Duchess (Sunday)",
         "Sunday sale of wine and mixed beverages by Englefield, Inc., dba East Lancaster Duchess (D-6 permit), a carryout/grocery store at 561 E. Main Street, Lancaster."),
    ]:
        c.issue(id, "liquor", "City of Lancaster", title, LAN, area=prec, text=text, src=I)
    return c
