from lib import County, NOTE_ORDER, NOTE_PLACES

SITE = "https://boe.morrowcountyohio.gov/"
# The Board's site links only the primary's notices; the general-election 46-day notice is posted beside them but not linked.
NOTICE = "https://boe.morrowcountyohio.gov/2026/2026%20General%2046%20Day%20Notice.pdf"
CANDS = "https://boe.morrowcountyohio.gov/2026/2026%20GENERAL%20CERTIFIED%20CANDIDATES%20MORROW.pdf"
ISSUES = "https://boe.morrowcountyohio.gov/candidates___issues/index.php"


def build():
    # The SoS file abbreviates North/South Bloomfield; the Board spells them out.
    c = County("morrow", "Morrow", "39117", rename={"N. BLOOMFIELD TOWNSHIP": "North Bloomfield Township",
                                                     "S. BLOOMFIELD TOWNSHIP": "South Bloomfield Township"})
    # The notice names precincts by number and school-district code: 006 Bennington Twp West (Marengo), 012 Cardington Village East,
    # 024 Chester Township West (Chesterville), 033 Franklin Township, 066 Lincoln Township East (Fulton), 069 Lincoln Township West,
    # 072 North Bloomfield Twp East, 084 Peru Township, 087/090 South Bloomfield Twp East/West (Sparta), 093 Troy Township,
    # 102 Westfield Township (numbers and names from the Board's May 2026 primary notice).
    # The Morrow voter file has no school-district columns, so school issues are placed from the notice's precinct lists.
    c.src("morrow-46day", "Morrow County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election", NOTICE)
    c.src("morrow-candidates", "Morrow County Board of Elections: candidates certified, November 3, 2026 General Election", CANDS)
    c.src("morrow-issues", "Morrow County Board of Elections: official questions and issues ballot language, November 3, 2026 General Election", ISSUES)
    C = ["morrow-46day"]; CC = ["morrow-46day", "morrow-candidates"]; I = ["morrow-issues", "morrow-46day"]
    c.links = [
        {"label": "Board of Elections", "url": SITE},
        {"label": "Candidates & issues", "url": ISSUES},
        {"label": "Election notices", "url": "https://boe.morrowcountyohio.gov/election_notices/index.php"},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://boe.morrowcountyohio.gov/new_page/index.php"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it, "
               "checked against the Board's certified candidate list. Issue wording is from the Board's official questions and issues ballot language.",
               NOTE_ORDER, NOTE_PLACES]
    P = c.p
    N = lambda n: f"Issue {n}"

    # --- Federal, state legislative, appeals (all of Morrow County is in each district; no State Senate race) ---
    c.contest("congress-4", "U.S. House", "Representative to Congress", [("Jim Jordan", "REP"), ("Joshua D. Kolasinski", "DEM"), ("Tracey L. Tackett", "Nonparty")],
              detail="4th District", src=C)
    c.contest("rep-87", "Ohio General Assembly", "State Representative", [("Lora Covrett", "DEM"), ("Jeffrey A. McClain", "REP"), ("Craig Swartz", "Nonparty")],
              detail="87th District", src=C)
    c.contest("appeals-5", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Matthew George", "REP")], detail="5th District · term commencing February 9, 2027", src=C)

    # --- County offices ---
    c.contest("commissioner", "County offices", "County Commissioner", [("Jon W. Mason", "REP")], detail="Term commencing January 1, 2027", src=CC)
    c.contest("auditor", "County offices", "County Auditor", [("Conni McChesney", "REP")], detail="Full term commencing March 8, 2027", src=CC)

    # --- Issues (numbered as in the notice; State Issue 3 is in the state file) ---
    est = lambda per: f"{per} for each $100,000 of market value"
    LEX = P("N. BLOOMFIELD TOWNSHIP", "TROY TOWNSHIP")
    LEX_J = "Lexington Local School District (Richland and Morrow counties)"
    LEX_AREA = "Lexington Local School District, Morrow County part (North Bloomfield Township East and Troy Township precincts)"
    c.levy("issue-1", LEX_J, LEX, "Renewal", "Current operating expenses (fixed-sum levy of $2,680,000 a year).", "4.8 mills (estimated average)",
           "5 years, commencing in 2026", "2027", estimate=f"$2,680,000 a year; {est('$168')}", number=N(1), area=LEX_AREA, src=I,
           text="Shall a fixed-sum levy renewing an existing levy be imposed by the Lexington Local School District for the purpose of paying the current operating expenses "
                "of the district in the sum of $2,680,000 and a levy of taxes to be made outside of the ten-mill limitation estimated by the county auditor to average 4.8 mills "
                "for each $1 of taxable value, which amounts to $168 for each $100,000 of the county auditor's market value, for a period of 5 years, commencing in 2026, "
                "first due in calendar year 2027? The county auditor has certified that the amount by which the carry-over balance in the district's general operating budget "
                "from the preceding fiscal year exceeds the district's general fund expenditures made in the preceding fiscal year is $0, which is 0% of those expenditures.")
    c.issue("issue-2", "question", LEX_J, "School district income tax: 0.75%, 10 years, for current expenses", LEX, number=N(2), area=LEX_AREA, src=I,
            text="Shall an annual income tax of 0.75% on the earned income of individuals residing in the school district be imposed by the Lexington Local School District, "
                 "for 10 years, beginning January 1, 2027, for the purpose of current expenses?")
    c.levy("issue-3", "Delaware Area Career Center (joint vocational school district; Delaware, Franklin, Marion, Morrow and Union counties)",
           P("PERU TOWNSHIP", "WESTFIELD TOWNSHIP"), "Renewal and decrease",
           "Improving, renovating, remodeling, enlarging, furnishing and equipping school buildings and facilities (0.40 mill) and current expenses (0.35 mill); "
           "renewal of part of an existing levy, a reduction of 0.95 mill.",
           "0.75 mill", "10 years, commencing in 2026", "2027", estimate=f"$5,773,576 a year; {est('$18')}", number=N(3),
           area="Peru Township and Westfield Township precincts (Buckeye Valley school district parts)", src=I)
    c.levy("issue-4", "Morrow County", "county", "Renewal", "Provision, maintenance and operation of services and facilities for older citizens.",
           "0.5 mill", "5 years, commencing in 2027", "2028", estimate=f"$472,502 a year; {est('$11')}", number=N(4), area="Morrow County (all precincts)", src=I)
    c.levy("issue-5", "Delaware-Morrow Mental Health & Recovery Services Board (Delaware and Morrow counties)", "county", "Renewal and increase",
           "Current expenses (renewal of 1.5 mills and an increase of 0.5 mill).", "2 mills", "5 years, commencing in 2027", "2028",
           estimate=f"$23,005,505 a year; {est('$50')}", number=N(5), area="Morrow County (all precincts)", src=I)
    c.issue("issue-6", "liquor", "Village of Cardington", "Local liquor option: Cardington Duchess (Sunday)", P("CARDINGTON VILLAGE"), number=N(6),
            area="Cardington Village East precinct", src=I,
            text="Sunday sale of wine and mixed beverages by Englefield, Inc., dba Cardington Duchess (D-6 permit applicant), a carryout / grocery store at 101 Gilead Street, Cardington.")

    CV = P("CHESTERVILLE VILLAGE"); FV = P("FULTON VILLAGE")
    L = [
        ("issue-7", "Village of Chesterville", CV, "Current operating expenses.", "1 mill", "5 years, commencing in 2026", "2027", f"$3,499 a year; {est('$28')}", "Chesterville precinct (Chester Township West)"),
        ("issue-8", "Village of Chesterville", CV, "Current operating expenses.", "3 mills", "5 years, commencing in 2026", "2027", f"$10,497 a year; {est('$85')}", "Chesterville precinct (Chester Township West)"),
        ("issue-9", "Village of Fulton", FV, "Current expenses.", "3 mills", "5 years, commencing in 2027", "2028", f"$10,088 a year; {est('$55')}", "Fulton precinct (Lincoln Township East)"),
        ("issue-10", "Village of Fulton", FV, "Maintaining and operating sewage disposal plants and facilities.", "4 mills", "5 years, commencing in 2027", "2028", f"$15,411 a year; {est('$87')}", "Fulton precinct (Lincoln Township East)"),
        ("issue-11", "Village of Fulton", FV, "General construction, reconstruction, resurfacing and repair of streets, roads and bridges.", "3.5 mills", "5 years, commencing in 2026", "2027", f"$13,662 a year; {est('$77')}", "Fulton precinct (Lincoln Township East)"),
        ("issue-12", "Village of Marengo", P("MARENGO VILLAGE"), "Current expenses.", "2.5 mills", "5 years, commencing in 2026", "2027", f"$10,000 a year; {est('$59')}", "Marengo precinct (Bennington Township West)"),
        ("issue-13", "Village of Sparta", P("SPARTA VILLAGE"), "Current expenses.", "3.4 mills", "5 years, commencing in 2027", "2028", f"$7,411 a year; {est('$80')}", "Sparta precinct (South Bloomfield Township West)"),
    ]
    for id, jur, places, purpose, mills, term, fd, e, area in L:
        c.levy(id, jur, places, "Renewal", purpose, mills, term, fd, estimate=e, number=N(int(id.split("-")[1])), area=area, src=I)

    FR = P("FRANKLIN TOWNSHIP"); FR_AREA = "Franklin Township (all splits)"
    c.issue("issue-14", "question", "Franklin Township (unincorporated area; zoning by the Morrow County Commissioners)", "Zoning plan for the unincorporated area of Franklin Township",
            FR, number=N(14), area=FR_AREA, src=I,
            text="Morrow County Commissioners have proposed a zoning resolution for the unincorporated area of Franklin Township to promote the public health, safety, comfort "
                 "and general welfare of the community, to conserve and protect property and property values, to secure the most appropriate use of land and to facilitate "
                 "adequate but economical provision of public improvements, all in accordance with a comprehensive plan. Shall the zoning plan for the unincorporated area "
                 "of Franklin Township, as adopted by the Morrow County Commissioners, be approved?")
    c.levy("issue-15", "Franklin Township", FR, "Additional",
           "Fire apparatus, appliances, buildings or sites, or payment of permanent, part-time or volunteer firefighters or firefighting companies.",
           "1.5 mills", "5 years, commencing in 2026", "2027", estimate=f"$104,000 a year; {est('$53')}", number=N(15), area=FR_AREA, src=I)
    c.issue("issue-16", "liquor", "Franklin Township (unincorporated area)", "Local liquor option: Franklin Township Economic Revitalization District (all days, including Sunday)",
            FR, number=N(16), area=FR_AREA, src=I,
            text="Sale of beer and intoxicating liquor on all days of the week, including Sunday, at the Franklin Township Economic Revitalization District, a community facility "
                 "(R.C. 4301.01) west of I-71 near the U.S. 95 / I-71 interchange, including parcel F14-001-00-080-08. Placed on the ballot by resolution.")
    c.levy("issue-17", "Lincoln Township", P("LINCOLN TOWNSHIP", "FULTON VILLAGE"), "Renewal", "Maintaining and operating cemeteries.", "0.7 mill",
           "5 years, commencing in 2027", "2028", estimate=f"$24,446 a year; {est('$10')}", number=N(17), area="Lincoln Township East (including Fulton) and West", src=I)
    c.levy("issue-18", "South Bloomfield Township", P("S. BLOOMFIELD TOWNSHIP", "SPARTA VILLAGE"), "Renewal",
           "Fire apparatus, rescue and other fire equipment, buildings and sites; firefighting companies or firefighters; emergency medical service, ambulance equipment "
           "and ambulance, paramedic or other EMS provided by a fire department.",
           "3.25 mills", "5 years, commencing in 2027", "2028", estimate=f"$186,000 a year; {est('$71')}", number=N(18),
           area="South Bloomfield Township East and West (including Sparta)", src=I)
    return c
