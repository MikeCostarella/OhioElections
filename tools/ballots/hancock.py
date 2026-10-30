from lib import County, NOTE_ORDER, NOTE_PLACES

SITE = "https://hancockcountyohioelections.gov/"
NOTICE = "https://hancockcountyohioelections.gov/wp-content/uploads/2026/09/46Day-Notice-G26-1.pdf"
CAND = "https://docs.google.com/document/d/1hsyr289kQ_Q32VhOIQeOn_fEeRk04fQecBoveOXyc4Y/view"
ISSUES = "https://docs.google.com/document/d/1NHuHpLqr9Nbrvb-8wiMyaXkd9bW9eZsSHnv_ihl2z2k/view"


def build():
    # Default display names are right ("MCCOMB VILLAGE" -> "McComb Village", "BIGLICK TWP" -> "Biglick Township").
    c = County("hancock", "Hancock", "39063")
    c.src("hancock-46day", "Hancock County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election (September 18, 2026)", NOTICE)
    c.src("hancock-cand", "Hancock County Board of Elections: candidates for the November 3, 2026 General Election (revised August 12, 2026)", CAND)
    c.src("hancock-issues", "Hancock County Board of Elections: issues for the November 3, 2026 General Election (with ballot wording)", ISSUES)
    C = ["hancock-46day", "hancock-cand"]; I = ["hancock-46day", "hancock-issues"]
    c.links = [
        {"label": "Board of Elections", "url": SITE},
        {"label": "What's on the ballot", "url": "https://hancockcountyohioelections.gov/whats-on-the-november-3-2026-general-election-ballot/"},
        {"label": "Am I registered? / Sample ballot", "url": "https://hancock-voterview.boe.ohio.gov/VoterView/RegistrantSearch.do"},
        {"label": "Polling locations", "url": "https://hancockcountyohioelections.gov/polling-locations/"},
    ]
    c.results_links = [
        {"label": "Board of Elections: live election results", "url": "https://hancockcountyohioelections.gov/live/"},
        {"label": "Board of Elections: past election results", "url": "https://hancockcountyohioelections.gov/past-election-results/"},
    ]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it, "
               "checked against the Board's candidate list and issues list (which gives the full ballot wording).",
               NOTE_ORDER, NOTE_PLACES,
               "The Board's notice and issues list do not give local issue numbers; see your sample ballot for them."]
    P = c.p; SD = c.sd

    # --- Federal, state legislative, appeals (all of Hancock County is in each district) ---
    c.contest("congress-5", "U.S. House", "Representative to Congress", [("Bob Latta", "REP"), ("Brian A. Shaver", "DEM"), ("Michael J. Veloff", "LIB")],
              detail="5th District", src=C)
    c.contest("senate-1", "Ohio General Assembly", "State Senator", [("Craig S. Riedel", "REP")], detail="1st District", src=C)
    c.contest("rep-83", "Ohio General Assembly", "State Representative", [("Sheila Coressel", "DEM"), ("Ty Mathews", "REP")], detail="83rd District", src=C)
    c.contest("appeals-3-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Mark C. Miller", "REP")], detail="3rd District · full term commencing February 9, 2027", src=C)

    # --- County offices ---
    c.contest("commissioner", "County offices", "County Commissioner", [("Timothy K. Bechtol", "REP")], detail="Full term commencing January 1, 2027", src=C)
    c.contest("auditor", "County offices", "County Auditor", [("Charity Rauschenberg", "REP")], detail="Full term commencing March 9, 2027", src=C)
    NP = " · no party label on the ballot"
    c.contest("cp-gen", "Court of Common Pleas", "Judge of the Court of Common Pleas", ["Jonathan P. Starn"], detail="Full term commencing January 1, 2027" + NP, src=C)
    c.contest("cp-probate-juvenile", "Court of Common Pleas", "Judge of the Court of Common Pleas, Probate and Juvenile Division", ["Kristen K. Johnson"],
              detail="Full term commencing February 9, 2027" + NP, src=C)

    # --- Issues (unnumbered in the Board's documents; listed in the notice's order) ---
    c.levy("ada-library", "Ada Public Library", P("ORANGE TWP"), "Renewal", "Current expenses of the Library.", "1 mill", "5 years, commencing in 2027", "2028",
           estimate="$102,209 per year", area="Orange Township precinct Orange (54.02)", src=I)
    c.levy("fostoria-current", "City of Fostoria (Hancock, Seneca and Wood)", P("FOSTORIA CITY"), "Renewal", "Current expenses.", "6 mills", "5 years, commencing in 2027", "2028",
           estimate="$1,047,593 per year", area="Fostoria City (Hancock County part: Fostoria South 33.01 and Fostoria North 34.01)", src=I)
    c.levy("adamhs", "Hancock County", "county", "Renewal",
           "Hancock County Board of Alcohol, Drug Addiction and Mental Health Services: continued operations and the expansion of mental health and substance abuse services.",
           "1.3 mills", "5 years, commencing in 2027", "2028", estimate="$3,043,393 per year", src=I)
    c.levy("aging", "Hancock County", "county", "Renewal",
           "Hancock County Agency on Aging (now 50 North): continued operations and the expansion of services to senior residents.",
           "1.2 mills", "5 years, commencing in 2027", "2028", estimate="$2,566,887 per year", src=I)
    c.issue("liquor-marathon-center", "liquor", "City of Findlay", "Local liquor option: Marathon Center for the Performing Arts (Sunday)", P("FINDLAY CITY"),
            area="Findlay precinct 6C (26.01)",
            text="Local option (question 2): Sunday sale of wine and mixed beverages, and spirituous liquor by Hancock County Performing Arts Center, dba Marathon Center for the Performing Arts "
                 "(D-6 permit), 200 West Main Cross Street, Findlay.", src=I)
    # Same precincts as the notice: Blanchard 39.02, Liberty NW 46.02, McComb 53.01, Pleasant 55.01, Portage 56.01.
    c.issue("mccomb-bond", "levy", "McComb Local School District (Hancock and Wood)", "School district income tax (0.25%) and bond issue ($23,815,000)", SD("MCCOMB LOCAL SD (HANCOCK)"),
            area="McComb Local School District (Hancock County part: Blanchard 39.02, Liberty NW 46.02, McComb 53.01, Pleasant 55.01, Portage 56.01)",
            levy={"type": "Income tax and bond issue", "purpose": "Income tax; bonds for constructing school facilities.",
                  "mills": "6.99 mills (bond)", "term": "Income tax beginning January 1, 2027; bonds up to 37 years", "estimate": "$23,815,000 principal"},
            text="Income tax of 0.25% beginning January 1, 2027, and bonds of $23,815,000 for constructing school facilities, repaid over a maximum of 37 years, with a levy estimated at 6.99 mills.", src=I)
    # Hancock's ballot wording says this renews an income tax expiring at the end of 2027.
    c.issue("north-baltimore-income-tax", "question", "North Baltimore Local School District (Hancock and Wood)", "School district income tax: 1%, 5 years, for current expenses",
            SD("NORTH BALTIMORE LOCAL SD (WOOD)"), area="North Baltimore Local School District (Hancock County part: Allen West 36.02)",
            text="Shall an annual income tax of 1% on the earned income of individuals residing in the school district be imposed by the North Baltimore Local School District to renew an income tax "
                 "expiring at the end of 2027, for 5 years, beginning January 1, 2028, for the purpose of current expenses?", src=I)
    return c
