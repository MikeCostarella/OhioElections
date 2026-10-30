from lib import County, NOTE_ORDER, NOTE_PLACES

SITE = "https://vote.warrencountyohio.gov/"
NOTICE = "https://vote.warrencountyohio.gov/doc/Voting/46_Day_notice_for_November_3_2026.pdf"
ISSUES = "https://vote.warrencountyohio.gov/CandIssues/UpcomingIssues/Index"
ISSUE_DOC = "https://vote.warrencountyohio.gov/doc/CandIssues/Elections/20261103/Issues/"


def build():
    # The SoS file names Butlerville (Harlan Township) "BUTLER VILLAGE".
    c = County("warren", "Warren", "39165", rename={"BUTLER VILLAGE": "Butlerville Village"})
    c.src("warren-46day", "Warren County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election (revised October 15, 2026)", NOTICE)
    c.src("warren-issues", "Warren County Board of Elections: upcoming issues, November 3, 2026 (ballot wording for each issue)", ISSUES)
    S = ["warren-46day"]; I = ["warren-issues", "warren-46day"]
    c.links = [
        {"label": "Board of Elections", "url": SITE},
        {"label": "Upcoming issues", "url": ISSUES},
        {"label": "Sample ballots by precinct", "url": "https://lookup.boe.ohio.gov/vtrapp/warren/ballotlist.aspx"},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://vote.warrencountyohio.gov/Results/VotingArchives/Index"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it; "
               "issue wording is from the Board's ballot language for each issue.", NOTE_ORDER, NOTE_PLACES,
               "Carlisle, Franklin, Middletown, Monroe, Loveland and Springboro lie partly in Butler, Montgomery, Hamilton or Clermont counties. "
               "Only the Warren County parts vote on this Board's ballot.",
               "Local issue numbers start at 4: Issue 3 is the statewide question, and there are no Issues 1 or 2."]
    D = c.district; P = c.p; SD = c.sd
    NP = " · no party label on the ballot"

    c.contest("congress-1", "U.S. House", "Representative to Congress", [("Eric Conroy", "REP"), ("Greg Landsman", "DEM"), ("Nathan Weise", "LIB")],
              detail="1st District", src=S)
    c.contest("senate-7", "Ohio General Assembly", "State Senator", [("Zac Haines", "REP"), ("Cara Jacob", "DEM")], detail="7th District (Hamilton and Warren)", src=S)
    c.contest("rep-55", "Ohio General Assembly", "State Representative", [("Paul Michael Kurtz", "DEM"), ("Philip L. Pirdy", "LIB"), ("C. Michelle Teska", "REP")],
              detail="55th District", places=D("rep", 55), src=S)
    c.contest("rep-56", "Ohio General Assembly", "State Representative", [("Laalitya Acharya", "DEM"), ("Adam Mathews", "REP")], detail="56th District", places=D("rep", 56), src=S)
    c.contest("appeals-12-0101", "Ohio Court of Appeals", "Judge of the Court of Appeals",
              [("Matthew Byrne", "REP", "Withdrew September 16, 2026; his name may still appear on the ballot, but votes for him will not count"),
               ("Willa Concannon", "Write-in")],
              detail="12th District (Butler, Brown, Clermont, Clinton, Fayette, Madison, Preble and Warren counties) · full term commencing January 1, 2027", src=S)
    c.contest("appeals-12-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Robert A. Hendrickson", "REP")],
              detail="12th District (Butler, Brown, Clermont, Clinton, Fayette, Madison, Preble and Warren counties) · full term commencing February 9, 2027", src=S)
    c.contest("commissioner", "County offices", "County Commissioner", [("Katherine Bowles", "LIB"), ("Tom Grossmann", "REP"), ("Ian Logan", "DEM")],
              detail="Full term commencing January 1, 2027", src=S)
    c.contest("auditor", "County offices", "County Auditor", [("Matt Nolan", "REP")], detail="Full term commencing March 8, 2027", src=S)
    c.contest("cp-gen", "Court of Common Pleas", "Judge of the Court of Common Pleas, General Division", ["Gary A. Loxley"],
              detail="Full term commencing February 8, 2027" + NP, src=S)
    c.contest("cp-probate-juv", "Court of Common Pleas", "Judge of the Court of Common Pleas, Probate and Juvenile Division", ["Joseph W. Kirby"],
              detail="Full term commencing February 1, 2027" + NP, src=S)

    N = lambda n: f"Issue {n}"
    c.issue("issue-4", "question", "Franklin City School District", "School district income tax: 1.25% for 5 years, for current expenses", SD("FRANKLIN CITY SD"), number=N(4),
            text="Annual income tax of 1.25% on the earned income of individuals residing in the school district, for 5 years, beginning January 1, 2027, for current expenses.",
            src=["warren-issues"])
    # The 46-day notice lists Lebanon City A-N, Mason A-B, Clearcreek, South Lebanon B, Turtlecreek, Union, Washington A and Wayne C precincts.
    c.issue("issue-5", "question", "Lebanon City School District", "School district income tax: 1% for 10 years, for current expenses", SD("LEBANON CITY SD"), number=N(5),
            text="Annual income tax of 1% on the earned income of individuals residing in the school district, for 10 years, beginning January 1, 2027, for current expenses.", src=I)
    c.levy("issue-6", "Mental Health Recovery Board Serving Warren and Clinton Counties", "county", "Renewal", "Current expenses.", "1 mill", "5 years, commencing in 2027", "2028",
           estimate="$7,677,198 per year; $16 per $100,000 of market value", number=N(6), area="Warren County", src=I)
    c.levy("issue-7", "Warren County", "county", "Renewal", "Providing or maintaining senior citizens services.", "1.21 mills", "5 years, commencing in 2026", "2027",
           estimate="$9,016,446 per year; $22 per $100,000 of market value", number=N(7), src=I)
    # The notice lists Franklin City A-I, Springboro City 3A and Carlisle 1A-3A (and repeats "Franklin City A-I", apparently for Franklin Township A-I).
    c.levy("issue-8", "Franklin Township (excluding the City of Middletown)", P("FRANKLIN TOWNSHIP", "FRANKLIN CITY", "CARLISLE CITY", "SPRINGBORO CITY"), "Renewal",
           "Providing or maintaining senior services or facilities.", "0.25 mill", "5 years, commencing in 2027", "2028",
           estimate="$143,801 per year; $5 per $100,000 of market value", number=N(8),
           area="Franklin Township, Franklin City, Carlisle and Springboro precinct 3A (not Middletown)", src=I)
    # The notice adds precinct Lebanon City E; the voter file puts no Lebanon voters in Turtlecreek Township, so add it.
    c.levy("issue-9", "Turtlecreek Township", P("TURTLECREEK TOWNSHIP", "LEBANON CITY"), "Additional",
           "Fire apparatus, equipment, buildings, firefighting and emergency medical personnel, and ambulance and emergency medical services.", "4.5 mills",
           "Continuing period of time, commencing in 2026", "2027", estimate="$3,592,748 per year; $158 per $100,000 of market value", number=N(9),
           area="Turtlecreek Township A–K and Lebanon City precinct E", src=I)
    return c
