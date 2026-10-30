from lib import County, NOTE_ORDER, NOTE_PLACES

SITE = "https://www.williamscountyoh.gov/150/Board-of-Elections"
NOTICE = "https://www.williamscountyoh.gov/DocumentCenter/View/4018"
NOTICE100 = "https://www.williamscountyoh.gov/DocumentCenter/View/3957"
BALLOTS = "https://lookup.boe.ohio.gov/vtrapp/williams/ballotlist.aspx"


def build():
    # Default display names are right ("HOLIDAY CITY VILLAGE" -> "Holiday City Village"); St. Joseph Township takes the Board's spelling.
    c = County("williams", "Williams", "39171", rename={"SAINT JOSEPH TWP": "St. Joseph Township"})
    c.src("williams-46day", "Williams County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election", NOTICE)
    c.src("williams-ballots", "Williams County Board of Elections: official sample ballots for all 44 precinct splits, November 3, 2026 (state ballot lookup)", BALLOTS)
    C = I = ["williams-46day", "williams-ballots"]
    c.links = [
        {"label": "Board of Elections", "url": SITE},
        {"label": "46-day election notice", "url": NOTICE},
        {"label": "100-day election notice", "url": NOTICE100},
        {"label": "Sample ballots by precinct", "url": BALLOTS},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://www.williamscountyoh.gov/152/Election-Results"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it, "
               "checked against the Board's sample ballots for all 44 precinct splits, which give the full wording of each issue.",
               NOTE_ORDER, NOTE_PLACES,
               "Local issue numbers run 4 to 13; Issue 3 is the statewide question."]
    P = c.p; SD = c.sd
    N = lambda n: f"Issue {n}"
    est = lambda total, per: f"{total} a year; {per} for each $100,000 of the county auditor's market value"

    # --- Federal, state legislative, appeals (all of Williams County is in each district) ---
    # The notice also lists a certified write-in for Congress (Kathy McKinstry); write-ins are not listed.
    c.contest("congress-9", "U.S. House", "Representative to Congress", [("Marcy Kaptur", "DEM"), ("Derek Merrin", "REP")], detail="9th District", src=C)
    # Same candidate as hancock.py and logan.py.
    c.contest("senate-1", "Ohio General Assembly", "State Senator", [("Craig S. Riedel", "REP")], detail="1st District · full term commencing January 1, 2027", src=C)
    c.contest("rep-81", "Ohio General Assembly", "State Representative", [("Patti Rockey", "REP"), ("David Swanson", "DEM")],
              detail="81st District · full term commencing January 1, 2027", src=C)
    # Same races (and ids) as lucas.py, wood.py and ottawa.py.
    c.contest("appeals-6-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Michael R. Goulding", "REP")], detail="6th District · full term commencing February 9, 2027", src=C)
    c.contest("appeals-6-0210", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Myron C. Duhart", "DEM"), ("CJ Kamm", "REP")], detail="6th District · full term commencing February 10, 2027", src=C)

    # --- County offices ---
    c.contest("commissioner", "County offices", "County Commissioner", [("Bartley E. Westfall", "REP")], detail="Full term commencing January 1, 2027", src=C)
    c.contest("auditor", "County offices", "County Auditor", [("Vickie L. Grimm", "REP")], detail="Full term commencing March 8, 2027", src=C)
    NP = " · no party label on the ballot"
    # The notice gives only "term commencing 2027"; the date is from the sample ballots.
    c.contest("cp-probate-juvenile", "Court of Common Pleas", "Judge of the Court of Common Pleas, Juvenile and Probate Division", ["Karen K. Gallagher"],
              detail="Full term commencing February 9, 2027" + NP, src=C)

    # --- Issues, in the notice's order ---
    c.issue("issue-4", "question", "North Central Local School District", "School district income tax: 1% on earned income, continuing, for current expenses",
            SD("NORTH CENTRAL LOCAL SD (WILLIAMS)"),
            area="North Central Local School District (Bridgewater; Jefferson splits 4 and 6, including Holiday City; Madison; Pioneer; Millcreek split 2)", number=N(4),
            text="Shall an annual income tax of 1 percent on the earned income of individuals residing in the school district be imposed by North Central Local School District, "
                 "for a continuing period of time, beginning January 1, 2027, for the purpose of current expenses?", src=I)
    # The notice calls it a fixed-sum levy; the ballot wording says it renews an existing levy.
    # Same levy (id, jurisdiction, purpose) as defiance.py's central-lsd-current; same figures.
    c.levy("central-lsd-current", "Central Local School District (Defiance and Williams)", SD("CENTRAL LOCAL SD (DEFIANCE)"), "Renewal",
           "Current operating expenses (fixed-sum levy of $615,000 a year).", "2.57 mills (estimated average)", "5 years, commencing in 2027", "2028",
           estimate=est("$615,000", "$90"), number=N(5), area="Central Local School District, Williams County part (Center South split 2, Pulaski South split 2)", src=I,
           text="Shall a fixed-sum levy renewing an existing levy be imposed by the Central Local School District for the purpose of paying the current operating expenses "
                "of the district in the sum of $615,000 and a levy of taxes to be made outside of the ten-mill limitation estimated by the county auditor to average 2.57 mills "
                "for each $1 of taxable value, which amounts to $90 for each $100,000 of the county auditor's market value, for a period of 5 years, commencing in 2027, "
                "first due in calendar year 2028?")
    c.levy("issue-6", "Williams County", "county", "Renewal", "Educational activities related to agriculture, natural resources and 4-H programs (OSU Extension).",
           "0.4 mill", "5 years, commencing in 2027", "2028", estimate=est("$311,924", "$8"), number=N(6), src=I)
    c.levy("issue-7", "Williams County", "county", "Additional", "Senior citizens services and maintaining the department's vehicles and facilities (Department of Aging).",
           "1 mill", "5 years, commencing in 2026", "2027", estimate=est("$1,182,325", "$35"), number=N(7), src=I)
    # Same levy (id, jurisdiction, purpose) as defiance.py's four-county-adamhs; same figures.
    # The notice prints ".07 mill"; the ballot wording gives 0.7 mill ($13 per $100,000).
    c.levy("four-county-adamhs", "Four County ADAMhs Board (Defiance, Fulton, Henry and Williams)", "county", "Renewal",
           "Current expenses of the Four County Board of Alcohol, Drug Addiction and Mental Health Services District.", "0.7 mill",
           "5 years, commencing in 2027", "2028", estimate=est("$2,293,020", "$13"), number=N(8), area="Williams County", src=I)

    # --- Local liquor options ---
    c.issue("issue-9", "liquor", "Village of Montpelier", "Local liquor option: Casa Del Rey Mexican Grill (Sunday)", P("MONTPELIER VILLAGE"),
            area="Montpelier precinct Montpelier A", number=N(9),
            text="Shall the sale of wine and mixed beverages, and spirituous liquor be permitted for sale on Sunday by Golden Indian Creek L.L.C., (dba Casa Del Rey Mexican Grill) "
                 "an applicant for a D-6 liquor permit who is engaged in the business of operating a restaurant at 311 W. Main Street, Montpelier Ohio 43543 in this precinct?", src=I)
    c.issue("issue-10", "liquor", "Pulaski Township", "Local liquor option: Bryan Sunoco (beer, wine and mixed beverages)", P("PULASKI TWP"),
            area="Pulaski Township precinct Pulaski South", number=N(10),
            text="Shall the sale of beer, wine and mixed beverages be permitted by Shukrana Distributors, L.L.C., dba Bryan Sunoco, an applicant for a C-1, C-2 liquor permit, "
                 "who is engaged in the business of operating a carryout/grocery store at 2042 County Road 15, Bryan (Pulaski Township), Ohio 43506 in this precinct?", src=I)
    c.issue("issue-11", "liquor", "Pulaski Township", "Local liquor option: Bryan Sunoco (Sunday)", P("PULASKI TWP"),
            area="Pulaski Township precinct Pulaski South", number=N(11),
            text="Shall the sale of wine and mixed beverages be permitted for sale on Sunday by Shukrana Distributors, L.L.C., dba Bryan Sunoco, an applicant for a D-6 liquor permit, "
                 "who is engaged in the business of operating a carryout/grocery store at 2042 County Road 15, Bryan (Pulaski Township), Ohio 43506 in this precinct?", src=I)

    # --- Township and village levies ---
    # Precinct 012 Florence covers Florence Township with Edon and Blakeslee villages; all three of its ballot styles carry Issue 12.
    c.levy("issue-12", "Florence Township and Village of Edon", P("FLORENCE TWP", "EDON VILLAGE", "BLAKESLEE VILLAGE"), "Additional",
           "Maintaining and operating the Edon Union Cemetery.", "0.5 mill", "5 years, commencing in 2027", "2028", estimate=est("$38,498", "$18"), number=N(12),
           area="Florence precinct (Florence Township, Edon and Blakeslee)", src=I)
    # The notice lists precincts 007 Brady and 008 West Unity.
    c.levy("issue-13", "Brady Township", P("BRADY TWP", "WEST UNITY VILLAGE"), "Renewal", "Fire protection.", "0.5 mill", "5 years, commencing in 2026", "2027",
           estimate=est("$12,896", "$5"), number=N(13), area="Brady and West Unity precincts (Brady Township including West Unity)", src=I)
    return c
