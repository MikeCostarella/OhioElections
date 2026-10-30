from lib import County, NOTE_ORDER, NOTE_PLACES

NOTICE = "https://cms2.revize.com/revize/butlercountyboe/2026/November/FWAB%2046%20day.pdf"
CAND = "https://elections.bcohio.gov/2026/November/PetitionActivityReport.pdf"
ISSUES = "https://elections.bcohio.gov/2026/November/NovemberBallotList.pdf"

def build():
    c = County("butler", "Butler", "39017")
    c.src("butler-46day", "Butler County Board of Elections: 46-day FWAB election notice, November 3, 2026 General Election (updated 10/02/2026)", NOTICE)
    c.src("butler-cand", "Butler County Board of Elections: Candidate & Petition Activity report, November 3, 2026 General Election", CAND)
    c.src("butler-issues", "Butler County Board of Elections: November ballot issue list (Issues & Local Options), November 3, 2026 General Election", ISSUES)
    S = ["butler-46day", "butler-cand"]; I = ["butler-46day", "butler-issues"]
    c.links = [
        {"label": "Board of Elections", "url": "https://elections.bcohio.gov/"},
        {"label": "Sample ballot lookup", "url": "https://electionlink.bcohio.gov/TEDElectionLink/VoterServices/voter/el-sample-ballot"},
    ]
    c.results_links = [{"label": "Board of Elections: live results", "url": "https://liveresults.boe.ohio.gov/widgets/butleroh/2026-11-03/index.html"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice and its candidate and issue lists. The notice gives each issue's "
               "type, millage or rate and term only; the full wording is on the sample ballot.", NOTE_ORDER, NOTE_PLACES,
               "Sharonville and Monroe lie partly in Hamilton and Warren counties; College Corner lies mostly in Preble County. "
               "Only the Butler County parts vote on this Board's ballot."]
    D = c.district; P = c.p; SD = c.sd
    NP = " · no party label on the ballot"

    c.contest("congress-8", "U.S. House", "Representative to Congress", [("Warren Davidson", "REP"), ("Vanessa Enoch", "DEM")],
              detail="8th District (Hamilton, Butler (part), Preble, Darke and Miami (part) counties)", places=D("cong", 8), src=S)
    c.contest("congress-10", "U.S. House", "Representative to Congress", [("Kristina Knickerbocker", "DEM"), ("Thomas F. McMasters", "LIB"), ("Mike Turner", "REP")],
              detail="10th District (Montgomery, Butler (part) and Greene counties)", places=D("cong", 10), src=S)
    # The notice puts precinct StClair2.7MI in the 5th Senate and 40th House districts; the voter file has no St. Clair voters there, so add it.
    STC = P("ST CLAIR TOWNSHIP")
    c.contest("senate-5", "Ohio General Assembly", "State Senator", [("Jeffrey Harris", "DEM"), ("Phil Plummer", "REP")], detail="5th District", places=sorted(set(D("sen", 5) + STC)), src=S)
    for n, cs in {40: [("Rodney Creech", "REP"), ("Timothy B. Hornbacker", "DEM"), ("Joshua A. Umbaugh", "LIB")],
                  45: [("Jennifer Gross", "REP"), ("Jayson Ameer Rasheed", "DEM")],
                  46: [("Thomas Hall", "REP"), ("Benjamin McCall", "DEM")],
                  47: [("Jordan Haire", "DEM"), ("Diane Mullins", "REP"), ("Jason Purviance", "LIB")]}.items():
        c.contest(f"rep-{n}", "Ohio General Assembly", "State Representative", cs, detail=f"{n}th District", places=sorted(set(D("rep", n) + (STC if n == 40 else []))), src=S)
    c.contest("appeals-12-0101", "Ohio Court of Appeals", "Judge of the Court of Appeals",
              [("Matthew Byrne", "REP", "Withdrew September 16, 2026; his name may still appear on the ballot, but votes for him will not count"),
               ("Willa Concannon", "Write-in")],
              detail="12th District (Butler, Brown, Clermont, Clinton, Fayette, Madison, Preble and Warren counties) · full term commencing January 1, 2027", src=S)
    c.contest("appeals-12-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Robert A. Hendrickson", "REP")],
              detail="12th District (Butler, Brown, Clermont, Clinton, Fayette, Madison, Preble and Warren counties) · full term commencing February 9, 2027", src=S)
    c.contest("commissioner", "County offices", "County Commissioner", [("Mike Miller", "DEM"), ("Michael V. Ryan", "REP")], src=S)
    c.contest("auditor", "County offices", "County Auditor", [("Amy Hines", "DEM"), ("Nancy Nix", "REP")], src=S)
    for id, office, date, name in [
        ("cp-gen-0101", "Judge of the Court of Common Pleas, General Division", "January 1, 2027", "Jennifer McElfresh"),
        ("cp-gen-0103", "Judge of the Court of Common Pleas, General Division", "January 3, 2027", "Daniel Haughey"),
        ("cp-gen-0209", "Judge of the Court of Common Pleas, General Division", "February 9, 2027", "Michael A. Oster, Jr."),
        ("cp-juv", "Judge of the Court of Common Pleas, Juvenile Division", "January 2, 2027", "Erik D. Niehaus"),
        ("cp-probate", "Judge of the Court of Common Pleas, Probate Division", "February 9, 2027", "John M. Holcomb"),
    ]:
        c.contest(id, "Court of Common Pleas", office, [name], detail=f"Full term commencing {date}" + NP, src=S)

    N = lambda n: f"Issue {n}"
    c.issue("issue-1", "question", "Fairfield City School District", "School district income tax: 1.25% for 5 years, for current expenses", SD("FAIRFIELD CITY SD"), number=N(1),
            text="Income tax on earnings, 1.25%, 5 years, for current expenses.", src=I)
    c.issue("issue-2", "levy", "Lakota Local School District", "Bond issue: $223,483,492 for school facilities", SD("LAKOTA LOCAL SD (BUTLER)"), number=N(2),
            levy={"type": "Bond issue", "purpose": "School facilities.", "term": "37 years", "estimate": "$223,483,492 principal"}, src=I)
    c.issue("issue-4", "question", "Northwest Local School District (Hamilton and Butler)", "School district income tax: 1.5%, continuing, for current expenses", SD("NORTHWEST LOCAL SD (HAMILTON)"), number=N(4),
            text="Income tax on earnings, 1.5%, for a continuing period of time, for current expenses. Filed with the Hamilton County Board of Elections.", src=I)
    c.issue("issue-5", "question", "Southwest Local School District (Hamilton and Butler)", "School district income tax: 0.25%, continuing, for current expenses", SD("SOUTHWEST LOCAL SD (HAMILTON)"), number=N(5),
            text="Income tax on earnings, 0.25%, for a continuing period of time, for current expenses. Filed with the Hamilton County Board of Elections.", src=I)
    c.levy("issue-6", "Butler County", "county", "Renewal", "Mental health.", "1 mill", "10 years", number=N(6), src=I)
    c.issue("issue-7", "question", "City of Oxford", "Charter amendments: Sections 2.12, 3.05, 4.01, 4.02(7), 9.07 and 10.01", P("OXFORD CITY"), number=N(7), src=I)
    c.issue("issue-8", "question", "City of Oxford", "Charter amendment: Section 2.11(4)", P("OXFORD CITY"), number=N(8), src=I)
    c.levy("issue-9", "Village of College Corner (Preble and Butler)", P("COLLEGE CORNER VILLAGE"), "Renewal", "Fire.", "5.2 mills", "5 years", number=N(9),
           note="Filed with the Preble County Board of Elections.", src=I)
    c.levy("issue-10", "Village of New Miami", P("NEW MIAMI VILLAGE"), "Additional", "Police.", "5 mills", "5 years", number=N(10), src=I)
    c.levy("issue-11", "Village of New Miami", P("NEW MIAMI VILLAGE"), "Additional", "Fire.", "3 mills", "Continuing", number=N(11), src=I)
    c.levy("issue-12", "Fairfield Township Police District", P("FAIRFIELD TOWNSHIP"), "Additional", "Police.", "2.99 mills", "Continuing", number=N(12), src=I)
    c.levy("issue-13", "Hanover Township Fire District", P("HANOVER TOWNSHIP"), "Additional", "Fire.", "3.5 mills", "5 years", number=N(13), src=I)
    c.levy("issue-14", "Madison Township Fire District", P("MADISON TOWNSHIP"), "Renewal", "Fire and EMS.", "3 mills", "5 years", number=N(14), src=I)
    c.issue("issue-15", "liquor", "City of Middletown", "Local liquor option: Broken Barrel Bar & Grill (Sunday sales)", P("MIDDLETOWN CITY"), number=N(15),
            area="Middletown City precinct MIDD2WD3", src=I)
    c.issue("issue-16", "liquor", "West Chester Township", "Local liquor option: Wawa 7229 (Sunday sales)", P("WEST CHESTER TWP"), number=N(16),
            area="West Chester Township precinct WC39", src=I)
    c.issue("issue-17", "question", "City of Trenton", "Charter amendment: Article IX, Section 9.06, \"Prohibition of Construction of a Data Center\"", P("TRENTON CITY"), number=N(17), src=I)
    return c
