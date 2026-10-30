from lib import County, NOTE_ORDER, NOTE_PLACES

SITE = "https://www.boe.ohio.gov/madison/"
NOTICE = "https://www.boe.ohio.gov/madison/c/upload/FWAB_11November46Day.pdf"
CANDIDATES = "https://www.boe.ohio.gov/madison/c/upload/ELECTION_Candidates.pdf"
ISSUES = "https://www.boe.ohio.gov/madison/c/upload/ELECTION_Issues.pdf"
BALLOTS = "https://lookup.boe.ohio.gov/vtrapp/madison/ballotlist.aspx"

APPEALS_12 = "12th District (Butler, Brown, Clermont, Clinton, Fayette, Madison, Preble and Warren counties)"


def build():
    # The SoS file spells the village "MT. STERLING VILLAGE"; the Board writes "Mt. Sterling" (precinct 0019). Shown as the Board writes it.
    # Plain City Village (Madison part, precincts Plain City East and West) is shared with Union; neither county has a Plain City contest or issue.
    c = County("madison", "Madison", "39097", rename={"MT. STERLING VILLAGE": "Mt. Sterling Village"})
    c.src("madison-46day", "Madison County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election", NOTICE)
    c.src("madison-candidates", "Madison County Board of Elections: candidate list, November 3, 2026 General Election (updated 10/24/2026)", CANDIDATES)
    c.src("madison-issues", "Madison County Board of Elections: certified issues (final), November 3, 2026 General Election", ISSUES)
    c.src("madison-ballots", "Madison County Board of Elections: sample ballots for all 40 precinct splits, November 3, 2026 (state ballot lookup)", BALLOTS)
    S = ["madison-46day", "madison-candidates"]; I = ["madison-issues", "madison-ballots", "madison-46day"]
    c.links = [
        {"label": "Board of Elections", "url": SITE},
        {"label": "Election information", "url": "https://www.boe.ohio.gov/madison/election-info/"},
        {"label": "Sample ballots by precinct", "url": BALLOTS},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://www.boe.ohio.gov/madison/election-info/election-results/"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, candidate list and certified issues list, checked against the Board's "
               "sample ballots for all 40 precinct splits. Issue wording is the ballot's.",
               NOTE_ORDER, NOTE_PLACES,
               "Madison County's ballots do not number local issues (only statewide Issue 3 is numbered); the Village of West Jefferson's "
               "charter amendments are labelled #1 to #7 on the ballot."]
    P = c.p; D = c.district; SD = c.sd
    NP = " · no party label on the ballot"

    # --- Federal, state legislative, appeals ---
    # All of Madison County is in the 15th Congressional, 3rd Senate and 12th House districts (same contests as franklin.py/pickaway.py/clark.py).
    c.contest("congress-15", "U.S. House", "Representative to Congress", [("Brennan Barrington", "LIB"), ("Mike Carey", "REP"), ("Don Leonard", "DEM")],
              detail="15th District", src=S)
    c.contest("senate-3", "Ohio General Assembly", "State Senator", [("Stacie A. Baker", "DEM"), ("Michele Reynolds", "REP")],
              detail="3rd District · full term commencing January 1, 2027", src=S)
    c.contest("rep-12", "Ohio General Assembly", "State Representative", [("Brian Stewart", "REP"), ("Lee Yarsky", "DEM")],
              detail="12th District · full term commencing January 1, 2027", src=S)
    # Same contests as butler.py/warren.py/clermont.py/clinton.py. Madison's notice marks Byrne WITHDRAWN and lists write-ins Concannon,
    # Victor M. Haddad and Curt Carl Hartman (Haddad and Hartman withdrew, per the other 12th District specs; left out). The sample ballots still print Byrne.
    c.contest("appeals-12-0101", "Ohio Court of Appeals", "Judge of the Court of Appeals",
              [("Matthew Byrne", "REP", "Withdrew September 16, 2026; his name may still appear on the ballot, but votes for him will not count"),
               ("Willa Concannon", "Write-in")],
              detail=APPEALS_12 + " · full term commencing January 1, 2027", src=S + ["madison-ballots"])
    # The notice misprints this term as commencing 02/09/2025; the candidate list gives February 9, 2027.
    c.contest("appeals-12-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Robert A. Hendrickson", "REP")],
              detail=APPEALS_12 + " · full term commencing February 9, 2027", src=S)

    # --- County offices ---
    c.contest("commissioner", "County offices", "County Commissioner", [("Tony K. Xenikis", "REP")], detail="Full term commencing January 1, 2027", src=S)
    # Hunter is listed as "Independent" by the Board.
    c.contest("auditor", "County offices", "County Auditor", [("Ashley Cooper", "REP"), ("Jennifer S. Hunter", "Nonparty")],
              detail="Full term commencing March 8, 2027", src=S)
    c.contest("cp-probate-juv", "Court of Common Pleas", "Judge of the Court of Common Pleas, Probate/Juvenile Division", ["Christopher J. Brown"],
              detail="Full term commencing February 9, 2027" + NP, src=S)

    est = lambda total, per, basis="the county auditor's market": f"{total} a year; {per} for each $100,000 of {basis} value"

    # --- Special districts (township precincts from the Board's issues list and sample ballots) ---
    # Precincts Deercreek 1-2, Union 1-2, Monroe/Pike split 1 (Monroe), Paint/Range/Stokes split 1 (Paint), Oak Run,
    # Choctaw Lake East and West, and Somerford 1-3 (Choctaw Lake is in Somerford Township). Pike Township (Monroe/Pike split 2) does not vote.
    CENTRAL = P("DEERCREEK TOWNSHIP", "UNION TOWNSHIP", "MONROE TOWNSHIP", "PAINT TOWNSHIP", "OAK RUN TOWNSHIP", "SOMERFORD TOWNSHIP")
    CENTRAL_AREA = "Deercreek, Union, Monroe, Paint, Oak Run and Somerford townships (including Choctaw Lake East and West)"
    c.levy("madison-ems-district", "Madison County Emergency Medical District", CENTRAL, "Additional", "Ambulance service, emergency medical service, or both.",
           "4.75 mills", "5 years, commencing in 2027", "2028", est("$2,199,290", "$167"), area=CENTRAL_AREA,
           note="The ballot gives $167 per $100,000 of market value; the Board's issues list and 46-day notice give $166.25. "
                "The collection estimate is the same as the Central Townships Joint Fire District levy's in all the Board's documents.", src=I)
    c.levy("central-townships-fire", "Central Townships Joint Fire District", CENTRAL, "Additional",
           "Current expenses; fire apparatus, mechanical resuscitators, underwater rescue and recovery equipment and appliances, buildings and sites, water supply, "
           "fire-alarm communications, firefighting, emergency medical service, administrative and communications personnel, ambulance equipment, and ambulance, "
           "paramedic or other emergency medical services.",
           "4.75 mills", "5 years, commencing in 2027", "2028", est("$2,199,290", "$166"), area=CENTRAL_AREA, src=I)
    # Same levies as pickaway.py's (same ids). Range splits 2-4 include Midway Village; Stokes splits 5-6 include South Solon Village.
    STERLING = P("RANGE TOWNSHIP", "MIDWAY VILLAGE", "STOKES TOWNSHIP", "SOUTH SOLON VILLAGE", "PLEASANT TOWNSHIP", "MT. STERLING VILLAGE")
    c.levy("sterling-ambulance-renewal", "Sterling Joint Ambulance District", STERLING, "Renewal", "Current expenses.", "1.8 mills",
           "5 years, commencing in 2027", "2028", est("$489,825", "$36", "the county auditor's appraised"),
           area="Range, Stokes and Pleasant townships, Mt. Sterling, Midway and South Solon (Paint/Range/Stokes splits 2-6, Mt. Sterling, Pleasant 1-3)", src=I)
    c.levy("tri-county-fire-additional", "Tri-County Joint Fire District", P("PLEASANT TOWNSHIP", "MT. STERLING VILLAGE"), "Additional",
           "Current expenses; fire apparatus, mechanical resuscitators, underwater rescue and recovery equipment, buildings and sites, water supply, fire-alarm "
           "communications, firefighting, emergency medical, administrative and communications personnel, ambulance equipment, and ambulance, paramedic or other "
           "emergency medical services.", "2.5 mills", "5 years, commencing in 2027", "2028", est("$710,410", "$88"),
           area="Pleasant Township and Mt. Sterling (precincts Mt. Sterling and Pleasant 1-3)", src=I)

    # --- School districts ---
    # Precincts West Jefferson A 1-2, West Jefferson B 1-2, Jefferson Twp A split 1 and Jefferson Township B.
    c.levy("jefferson-lsd-pi", "Jefferson Local School District", SD("JEFFERSON LOCAL SD (MADISON)"), "Additional", "Permanent improvements.", "2.55 mills",
           "5 years, commencing in 2026", "2027", est("$859,370", "$89"), area="West Jefferson A and B, Jefferson Twp A (split 1), Jefferson Township B", src=I)
    # Same question as pickaway.py's, clinton.py's and ross.py's miami-trace-renewal; the 46-day notice omits it, the issues list and ballots have it
    # (Paint/Range/Stokes split 4 and Pleasant split 2).
    c.levy("miami-trace-renewal", "Miami Trace Local School District (Fayette, Clinton, Highland, Pickaway and Ross)", SD("MIAMI TRACE LOCAL SD (FAYETTE)"), "Renewal",
           "Current operating expenses (fixed-sum levy of $1,900,000 a year).", "2.2 mills (estimated average)", "5 years, commencing in 2027", "2028",
           "$1,900,000 a year; $77 for each $100,000 of market value", area="Parts of Range and Pleasant townships (Paint/Range/Stokes split 4, Pleasant split 2)",
           note="A fixed-sum levy renewing an existing levy. The county auditor certified the district's carry-over balance in excess of the preceding year's general fund expenditures as $0 (0%).",
           src=["madison-issues", "madison-ballots"])

    # --- Townships ---
    # Listed on the issues list and ballots (Paint/Range/Stokes splits 2-4, which include Midway Village) but not in the 46-day notice.
    c.levy("range-twp-fire", "Range Township", P("RANGE TOWNSHIP", "MIDWAY VILLAGE"), "Renewal", "Fire protection.", "1.7 mills", "5 years, commencing in 2027", "2028",
           est("$45,940", "$12"), area="Range Township, including Midway (Paint/Range/Stokes splits 2-4)", src=["madison-issues", "madison-ballots"])
    c.issue("darby-twp-zoning", "question", "Darby Township (unincorporated area)", "Township zoning plan (replacing the Madison County Zoning Resolution)",
            P("DARBY TOWNSHIP"), area="Darby 1 and 2",
            text="A zoning plan regulating the buildings and structures and use of lots and land in the unincorporated area of Darby Township, Madison County, Ohio, "
                 "as a replacement for the Madison County Zoning Resolution. Shall the zoning plan for the unincorporated area of Darby Township as adopted by the "
                 "board of township trustees be approved?", src=I)

    # --- City of London ---
    LON = P("LONDON CITY"); LON_AREA = "London 1-A, 1-B, 2, 3 and 4"
    c.levy("london-current", "City of London", LON, "Renewal", "Current expenses.", "2.1 mills", "5 years, commencing in 2027", "2028",
           est("$439,585", "$43", "the county auditor's appraised"), area=LON_AREA, src=I)
    c.issue("london-gas-aggregation", "question", "City of London", "Natural gas aggregation (opt-out)", LON, area=LON_AREA,
            text="Shall the City of London have the authority to aggregate the retail natural gas loads located in the City of London, and for that purpose, enter "
                 "into service agreements to facilitate for those loads the sale and purchase of natural gas, such aggregation to occur automatically except where "
                 "any person elects to opt out?", src=I)
    c.issue("liquor-london-4-one-stop", "liquor", "City of London", "Local liquor option: London One Stop (Sunday sales)", LON, area="London precinct 4",
            text="Shall the sale of wine and mixed beverages be permitted for sale on Sunday by London Gas & Food, Inc., dba London One Stop, an applicant for a D-6 "
                 "liquor permit who is engaged in the business of operating a carryout/grocery store at 157 S Main St, London, Ohio 43140 in this precinct?", src=I)

    # --- Village of West Jefferson: seven charter amendments proposed by the charter commission (labelled #1-#7 on the ballot) ---
    WJ = P("WEST JEFFERSON VILLAGE"); WJ_AREA = "West Jefferson A and B"
    for n, name, sections in [
        (1, "Office of the Mayor", "3.01 Election and Term, 3.02 Qualifications, 3.04 Executive and Administrative Powers, 3.05 Veto Power, 3.06 Acting Mayor, "
                                   "3.07 Vacancy, and 3.09 Training and Continuing Education."),
        (2, "The Council", "4.02 Composition and Term, 4.03 Qualifications, 4.04 President and Vice President of Council, 4.06 Removal, 4.07 Vacancies, and 4.16 Compensation."),
        (3, "The Clerk of Council", "4.08 Clerk of Council."),
        (4, "Meetings, Notice, Legislation and Executive Session", "4.09 Regular Meetings, 4.10 Special Meetings, 4.11 Legislative Procedure, 4.12 Public Notice, "
                                                                   "4.14 Emergency Ordinances, 4.19 Emergency Meetings, and 4.21 Executive Session."),
        (5, "Executive Directors and Administration", "5.01 Appointment and Vacancy of Director of Finance, 5.02 Powers and Duties of Director of Finance, "
                                                      "6.02 Qualifications, 6.03 Duties in General, 7.01 Appointment, 7.03 Police Department, 7.06 Qualifications for "
                                                      "Police Chief, 8.02 Powers and Duties, 9.01 Director of Law, 9.02 Qualifications, 9.03 General Powers and Duties, "
                                                      "9.04 Taxpayer Standing to Bring Suit on Behalf of Municipality, 9.05 Conflict of Interest, and 11.02 Classified and "
                                                      "Unclassified Service."),
        (6, "Planning and Zoning Commission", "10.01 Planning and Zoning Commission - Composition and Procedure, 10.02 Planning and Zoning Commission - Organization, "
                                              "10.03 Planning and Zoning Commission - Powers and Duties; Appeals, 10.04 Mandatory Referral to the Planning and Zoning "
                                              "Commission, 10.05 Public Hearings by Council, and 10.06 Action by Council."),
        (7, "General Powers, Nominations of Candidates, Conflict of Interest, Anti-Nepotism, and Technical and Formatting of Charter",
            "2.01 Municipal Powers, 13.01 Nominations, 18.01 Personal Interest, 18.02 Hiring and/or Appointment Procedures, 18.07 Effect of the Charter Upon "
            "Existing Laws and Rights, and 19.01 Corrections to the Charter."),
    ]:
        c.issue(f"west-jefferson-charter-{n}", "question", "Village of West Jefferson", f"Charter amendment #{n}: {name}", WJ, area=WJ_AREA,
                text=f"{sections} Shall the proposed charter amendment, as reported by the charter commission of the Village of West Jefferson be adopted?", src=I)
    return c
