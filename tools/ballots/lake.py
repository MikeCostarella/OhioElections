from lib import County, NOTE_ORDER, NOTE_PLACES

def build():
    c = County("lake", "Lake", "39085")
    c.src("lake-cand", "Lake County Board of Elections: November 3, 2026 General Election candidate list (updated 10/15/2026)",
          "https://wpassets.lakecountyohio.gov/wp-content/uploads/sites/12/2026/10/15161638/2026-Candidate-Filings.pdf")
    c.src("lake-issues", "Lake County Board of Elections: certified questions and issues, November 3, 2026 (updated 8/25/2026)",
          "https://wpassets.lakecountyohio.gov/wp-content/uploads/sites/12/2026/10/01155449/Issues-for-11-3-26.pdf")
    C = ["lake-cand"]; I = ["lake-issues"]
    c.links = [
        {"label": "Board of Elections", "url": "https://www.lakecountyohio.gov/boe/"},
        {"label": "Sample ballots", "url": "https://www.lakecountyohio.gov/boe/sample-ballots/"},
    ]
    c.results_links = [{"label": "Board of Elections", "url": "https://www.lakecountyohio.gov/boe/"}]
    c.notes = ["Taken from the Board of Elections' candidate list and its certified questions and issues (the Board's summary language).", NOTE_ORDER, NOTE_PLACES]

    c.contest("congress-14", "U.S. House", "Representative to Congress", [("David P. Joyce", "REP"), ("Maria Jukic", "DEM")], detail="14th District", src=C)
    c.contest("rep-23", "Ohio General Assembly", "State Representative", [("Julie A. Belich", "REP"), ("Daniel P. Troy", "DEM")], detail="23rd District", places=c.district("rep", 23), src=C)
    c.contest("rep-57", "Ohio General Assembly", "State Representative", [("Belinda Grassi", "Nonparty"), ("Jesse Styles", "REP"), ("Rick Walker", "DEM")], detail="57th District", places=c.district("rep", 57), src=C)
    c.contest("commissioner-0101", "County offices", "County Commissioner", [("John T. Plecnik", "REP"), ("Tom Trombley", "DEM")], detail="Term commencing January 1, 2027", src=C)
    c.contest("commissioner-ute", "County offices", "County Commissioner", [("Lisa Lewins", "DEM"), ("Morgan R. McIntosh", "REP")], detail="Unexpired term ending January 1, 2029", src=C)
    c.contest("auditor", "County offices", "County Auditor", [("Christopher A. Galloway", "REP")], detail="Term commencing March 8, 2027", src=C)
    c.contest("appeals-11-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Marisa L. Cornachio", "REP")], detail="11th District · term commencing February 9, 2027", src=C)
    c.contest("appeals-11-0210", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Robert J. Patton", "REP")], detail="11th District · term commencing February 10, 2027", src=C)
    NP = " · no party label on the ballot"
    c.contest("cp-dr", "Court of Common Pleas", "Judge of the Court of Common Pleas, Domestic Relations Division", ["Jeffrey H. Black"], detail="Term commencing January 2, 2027" + NP, src=C)
    c.contest("cp-juv", "Court of Common Pleas", "Judge of the Court of Common Pleas, Juvenile Division", ["Michael L. DeLeone"], detail="Term commencing January 4, 2027" + NP, src=C)
    c.contest("cp-gen", "Court of Common Pleas", "Judge of the Court of Common Pleas, General Division", ["John P. O'Donnell"], detail="Term commencing January 5, 2027" + NP, src=C)
    c.contest("cp-probate", "Court of Common Pleas", "Judge of the Court of Common Pleas, Probate Division", ["Mark J. Bartolotta"], detail="Term commencing February 9, 2027" + NP, src=C)
    c.contest("mentor-council-w3", "Municipal offices", "Mentor City Council, Ward 3", ["Jessie Baginski", "Charles E. Pinkerman"], detail="Unexpired term ending December 31, 2027 · Ward 3 voters only",
              places=c.p("MENTOR CITY"), area="Mentor City Ward 3", src=C)

    est = lambda total, per: f"{total} a year; {per} for each $100,000 of market value"
    c.levy("issue-4", "Kirtland Local School District", c.sd("KIRTLAND LOCAL SD (LAKE)"), "Renewal", "Current operating expenses of the district.", "4.36 mills",
           "5 years, commencing in 2027", "2028", est("$2,278,636", "$134"), number="Issue 4", area="Kirtland Local School District (7 precincts + Geauga)", src=I)
    c.levy("issue-5", "Mentor Exempted Village School District", c.sd("MENTOR EX VILL SD (LAKE)"), "Additional", "Current expenses.", "3.5 mills",
           "5 years, commencing in 2026", "2027", est("$9,613,354", "$123"), number="Issue 5", area="Mentor Exempted Village School District (45 precincts + Geauga)", src=I)
    c.issue("issue-6", "question", "Painesville City Local School District", "Proposed school district income tax: 1.25%", c.sd("PAINESVILLE CITY LOCAL SD (LAKE)"), number="Issue 6", area="Painesville City Local School District (9 precincts)",
            text="Shall an annual income tax of 1.25 per cent on the earned income of individuals residing in the school district be imposed by Painesville City Local School District, for a continuing period of time, beginning January 1, 2027, for the purpose of current expenses?", src=I)
    c.issue("issue-7", "question", "Riverside Local School District", "Proposed school district income tax: 1%", c.sd("RIVERSIDE LOCAL SD (LAKE)"), number="Issue 7", area="Riverside Local School District (30 precincts + Geauga)",
            text="Shall an annual income tax of 1 per cent on the earned income of individuals residing in the school district be imposed by Riverside Local School District, for a continuing period of time, beginning January 1, 2027, for the purpose of current expenses and permanent improvements?", src=I)
    c.issue("issue-8", "question", "Willoughby-Eastlake City School District", "Proposed school district income tax: 0.75%", c.sd("WILLOUGHBY-EASTLAKE CITY SD"), number="Issue 8", area="Willoughby-Eastlake City School District (49 precincts)",
            text="Shall an annual income tax of 0.75 per cent on the earned income of individuals residing in the school district be imposed by Willoughby-Eastlake City School District, for a continuing period of time, beginning January 1, 2027, for the purpose of current expenses?", src=I)
    c.levy("issue-9", "Eastlake City", c.p("EASTLAKE CITY"), "Renewal", "Current operating expenses.", "1.8 mills", "5 years, commencing in 2027", "2028", est("$575,463", "$16"), number="Issue 9", area="Eastlake City (12 precincts)", src=I)
    c.levy("issue-10", "Kirtland City", c.p("KIRTLAND CITY"), "Renewal", "Senior citizen and community recreational facilities and programs.", "0.85 mill", "5 years, commencing in 2026", "2027", est("$156,412", "$11"), number="Issue 10", area="Kirtland City (4 precincts)", src=I)
    c.levy("issue-11", "Willoughby City", c.p("WILLOUGHBY CITY"), "Renewal", "General construction, reconstruction, resurfacing, and repair of streets, roads, and bridges.", "2 mills", "5 years, commencing in 2026", "2027", est("$1,267,480", "$37"), number="Issue 11", area="Willoughby City (18 precincts)", src=I)
    c.levy("issue-12", "Willoughby City", c.p("WILLOUGHBY CITY"), "Renewal", "Current expenses.", "0.9 mill", "5 years, commencing in 2026", "2027", est("$157,186", "$3"), number="Issue 12", area="Willoughby City (18 precincts)", src=I)
    c.levy("issue-13", "Willowick City", c.p("WILLOWICK CITY"), "Renewal", "Parks and recreation.", "0.5 mill", "5 years, commencing in 2026", "2027", est("$70,824", "$5"), number="Issue 13", area="Willowick City (9 precincts)", src=I)
    c.issue("issue-14", "liquor", "Eastlake City", "Local liquor option: Vine Gas (Sunday)", c.p("EASTLAKE CITY"), number="Issue 14", area="Eastlake City Ward 1 Precinct A",
            text="Shall the sale of wine and mixed beverages be permitted for sale on Sunday by Vine Gas LLC DBA Vine Gas, an applicant for a D-6 liquor permit, who is engaged in the business of a convenience store and gas station at 33610 - 33632 - 33650 Vine St., Eastlake, Ohio 44095 in this precinct?", src=I)
    c.issue("issue-15", "liquor", "Willowick City", "Local liquor option: Lakeshore Gas (Sunday)", c.p("WILLOWICK CITY"), number="Issue 15", area="Willowick City Ward 3 Precinct C",
            text="Shall the sale of wine and mixed beverages be permitted for sale on Sunday by Lakeshore Gas LLC DBA Lakeshore Gas, an applicant for a D-6 liquor permit, who is engaged in the business of a convenience store and gas station at 29000 Lakeshore Blvd., Willowick, Ohio 44095 in this precinct?", src=I)
    c.issue("issue-16", "question", "Perry Village", "Proposed ordinance (by petition): Village Fiscal Officer duties on data center agreements", c.p("PERRY VILLAGE"), number="Issue 16", area="Perry Village (1 precinct)",
            text="The Proposed Ordinance amends Chapter 133.01 \"Established; Power and Duties\" of the Codified Ordinances of the Village of Perry regarding the duties of the Village Fiscal Officer before signing Village agreements with a hyperscale data center involving tax abatements, PILOT Programs, or any special tax designation. Shall the proposed ordinance amending Chapter 133.01 \"Established; Power and Duties\" of the Codified Ordinances of the Village of Perry be adopted?", src=I)
    c.levy("issue-17", "Concord Township", c.p("CONCORD TOWNSHIP"), "Renewal", "Fire.", "2.7 mills", "5 years, commencing in 2027", "2028", est("$1,795,434", "$49"), number="Issue 17", area="Concord Township (15 precincts)", src=I)
    c.levy("issue-18", "Madison Township", c.p("MADISON TOWNSHIP"), "Renewal", "Police.", "1.9 mills", "5 years, commencing in 2027", "2028", est("$587,707", "$33"), number="Issue 18", area="Madison Township (10 precincts)", src=I)
    return c
