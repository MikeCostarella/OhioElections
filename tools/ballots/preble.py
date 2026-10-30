from lib import County, NOTE_ORDER, NOTE_PLACES

NOTICE = "https://www.boe.ohio.gov/preble/c/upload/FWAB_11November46Day.pdf"
WITHDRAWN = "https://www.boe.ohio.gov/preble/c/pdf/WithdrawlAndWriteinList.pdf"

def build():
    # Raw names display correctly ("COLLEGE CORNER VILLAGE" -> "College Corner Village"); no renames needed.
    c = County("preble", "Preble", "39135")
    c.src("preble-46day", "Preble County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election (revised 10/15/2026)", NOTICE)
    c.src("preble-withdrawn", "Preble County Board of Elections: Candidate Withdrawal and Write-in list, November 3, 2026 General Election", WITHDRAWN)
    S = ["preble-46day"]; A = ["preble-46day", "preble-withdrawn"]
    c.links = [
        {"label": "Board of Elections", "url": "https://www.boe.ohio.gov/preble/"},
        {"label": "Election info", "url": "https://www.boe.ohio.gov/preble/election-info/"},
        {"label": "Sample ballots by precinct", "url": "https://lookup.boe.ohio.gov/vtrapp/preble/ballotlist.aspx"},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://www.boe.ohio.gov/preble/election-info/"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it "
               "and gives each local issue's full ballot wording.",
               NOTE_ORDER, NOTE_PLACES,
               "College Corner lies partly in Butler County and Verona partly in Montgomery County. Only the Preble County parts vote on this Board's ballot."]
    P = c.p; D = c.district
    NP = " · no party label on the ballot"

    # --- Federal, state legislative, appeals ---
    # All of Preble County is in the 8th Congressional, 5th Senate and 40th House districts (notice: "All Precincts").
    c.contest("congress-8", "U.S. House", "Representative to Congress", [("Warren Davidson", "REP"), ("Vanessa Enoch", "DEM")],
              detail="8th District (Hamilton, Butler (part), Preble, Darke and Miami (part) counties)", src=S)
    c.contest("senate-5", "Ohio General Assembly", "State Senator", [("Jeffrey Harris", "DEM"), ("Phil Plummer", "REP")], detail="5th District", src=S)
    c.contest("rep-40", "Ohio General Assembly", "State Representative", [("Rodney Creech", "REP"), ("Timothy B. Hornbacker", "DEM"), ("Joshua A. Umbaugh", "LIB")],
              detail="40th District", src=S)
    # Same contests as butler.py/warren.py/clermont.py/clinton.py. Preble's notice also lists withdrawn write-ins Victor M. Haddad and Curt Carl Hartman (left out).
    c.contest("appeals-12-0101", "Ohio Court of Appeals", "Judge of the Court of Appeals",
              [("Matthew Byrne", "REP", "Withdrew September 16, 2026; his name may still appear on the ballot, but votes for him will not count"),
               ("Willa Concannon", "Write-in")],
              detail="12th District (Butler, Brown, Clermont, Clinton, Fayette, Madison, Preble and Warren counties) · full term commencing January 1, 2027", src=A)
    c.contest("appeals-12-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Robert A. Hendrickson", "REP")],
              detail="12th District (Butler, Brown, Clermont, Clinton, Fayette, Madison, Preble and Warren counties) · full term commencing February 9, 2027", src=S)

    # --- County offices ---
    c.contest("commissioner", "County offices", "County Commissioner", [("Harold Niehaus", "REP")], detail="Full term commencing January 1, 2027", src=S)
    # The notice gives no term for County Auditor.
    c.contest("auditor", "County offices", "County Auditor", [("Lavon Wright", "REP")], src=S)
    c.contest("clerk-of-courts", "County offices", "Clerk of the Court of Common Pleas", [("Shonda Haynes", "REP")], detail="Unexpired term ending December 31, 2028", src=S)
    c.contest("cp-probate-juv", "Court of Common Pleas", "Judge of the Court of Common Pleas, Probate/Juvenile Division", ["Jenifer K. Overmyer"],
              detail="Full term commencing February 9, 2027" + NP, src=S)

    # --- Township offices ---
    # Notice precincts 081 Lanier Twp Southeast-P, 115 Lanier Twp Southeast-S, 117 Lanier Twp Northwest and 107 West Alexandria Village South
    # (the part of West Alexandria in Lanier Township).
    c.contest("lanier-trustee", "Township offices", "Township Trustee (Lanier Township)", ["Jason Earich", "Cooper Shockey"],
              detail="Unexpired term ending December 31, 2029" + NP, places=P("LANIER TOWNSHIP", "WEST ALEXANDRIA VILLAGE"),
              area="Lanier Township (incl. West Alexandria Village South precinct)", src=S)

    est = lambda total, per: f"{total} a year; {per} for each $100,000 of the county auditor's market value"
    N = lambda n: f"Issue {n}"
    # The notice numbers local issues 4-12 (Issue 3 is the statewide amendment); there are no Issues 1 or 2 on Preble's ballot.

    # --- Countywide ---
    c.levy("issue-4", "Preble County", "county", "Renewal",
           "Senior citizen services and facilities, through the Preble County Council on Aging, Inc. or its successor.", "1.5 mills",
           "5 years, commencing in 2027", "2028", est("$1,558,850", "$39"), number=N(4), src=S)

    # --- Villages ---
    c.levy("issue-5", "Village of Camden", P("CAMDEN VILLAGE"), "Renewal", "Police operating expenses.", "6 mills",
           "5 years, commencing in 2027", "2028", est("$100,990", "$113"), number=N(5), area="Camden Village (precincts 063 Camden Village 1, 065 Camden Village 2)", src=S)
    # Same levy as butler.py's issue-9 (Butler numbers it Issue 9; filed with this Board, which numbers it Issue 6).
    c.levy("issue-6", "Village of College Corner (Preble and Butler)", P("COLLEGE CORNER VILLAGE"), "Renewal", "Fire.", "5.2 mills",
           "5 years, commencing in 2026", "2027", est("$12,270", "$29"), number=N(6),
           note="Filed with the Preble County Board of Elections; Butler County's ballot numbers it Issue 9.",
           text="Fire apparatus, equipment and appliances, buildings and sites, water supply, fire-alarm communications, payment of firefighters "
                "(including the firefighter employers' pension contribution), ambulance equipment, and ambulance, paramedic or other emergency medical "
                "services operated by a fire department or firefighting company, and other related costs.", src=S)
    c.levy("issue-7", "Village of West Elkton", P("WEST ELKTON VILLAGE"), "Renewal", "Emergency medical services.", "1.25 mills",
           "5 years, commencing in 2026", "2027", est("$3,310", "$12"), number=N(7), src=S)
    c.levy("issue-8", "Village of Lewisburg", P("LEWISBURG VILLAGE"), "Renewal", "Parks and recreation.", "1 mill",
           "5 years, commencing in 2027", "2028", est("$29,690", "$23"), number=N(8), area="Lewisburg Village (precincts 089 North, 091 South)", src=S)
    c.issue("issue-9", "question", "Village of West Alexandria", "Municipal income tax: increase from 1% to 2% for general operating expenses",
            P("WEST ALEXANDRIA VILLAGE"), number=N(9), area="West Alexandria Village (precincts 105 North, 107 South)",
            text="Shall the Ordinance providing for a 1 per cent levy increase on income from 1 per cent to 2 per cent for the purpose of general "
                 "operating expenses, effective January 1, 2027, be passed?", src=S)

    # --- Townships ---
    # Notice precincts: 049 Harrison Twp West-T, 089/091 Lewisburg Village North/South, 093 Verona Village, 095 Harrison Twp Northeast,
    # 097 Harrison Twp Southeast-N, 099 Harrison Twp West-N, 113 Harrison Twp Southeast-B.
    c.levy("issue-10", "Harrison Township", P("HARRISON TOWNSHIP", "LEWISBURG VILLAGE", "VERONA VILLAGE"), "Additional", "Maintaining and operating cemeteries.", "1 mill",
           "Continuing period of time, commencing in 2026", "2027", est("$103,570", "$35"), number=N(10),
           area="Harrison Township, including Lewisburg and Verona villages", src=S)
    c.levy("issue-11", "Jackson Township", P("JACKSON TOWNSHIP"), "Renewal", "Fire protection and ambulance/emergency service.", "2 mills",
           "3 years, commencing in 2027", "2028", est("$70,260", "$47"), number=N(11), src=S)
    # Notice precincts 041 Eldorado Village, 047 West Manchester Village, 057 Monroe Twp.
    c.levy("issue-12", "Monroe Township", P("MONROE TOWNSHIP", "ELDORADO VILLAGE", "WEST MANCHESTER VILLAGE"), "Renewal", "Cemetery maintenance.", "0.5 mill",
           "5 years, commencing in 2026", "2027", est("$27,270", "$27"), number=N(12),
           area="Monroe Township, including Eldorado and West Manchester villages", src=S)
    return c
