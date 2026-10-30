from lib import County, NOTE_ORDER, NOTE_PLACES

BASE = "https://vote.franklincountyohio.gov/getmedia/"
NOTICE = BASE + "352b644d-b348-447e-b60d-aa9b9193a297/2026-General-Form-No-120-FWAB-Notice-46-Day"
CAND = BASE + "e0a4ca45-6893-45c1-8190-87696f8804b4/2026-General-Candidate-List-5"
QI = BASE + "4001b052-1b90-4f73-b030-2d981e6ec8fa/2026-General-Certified-Questions-and-Issues"


def ordinal(n):
    return f"{n}{'th' if 10 <= n % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')}"


def build():
    c = County("franklin", "Franklin", "39049", rename={
        "GROVE CITY-CITY": "Grove City",
        "COLUMBUS CITY ": "Columbus City", "DUBLIN CITY ": "Dublin City", "HARRISBURG VILLAGE ": "Harrisburg Village",
        "REYNOLDSBURG CITY ": "Reynoldsburg City", "WESTERVILLE CITY ": "Westerville City",
    })
    c.src("franklin-46day", "Franklin County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election", NOTICE)
    c.src("franklin-cand", "Franklin County Board of Elections: 2026 General Election candidates (revised October 16, 2026)", CAND)
    c.src("franklin-issues", "Franklin County Board of Elections: certified questions and issues, November 3, 2026 General Election (revised 9/4/2026)", QI)
    S = ["franklin-46day", "franklin-cand"]; I = ["franklin-issues", "franklin-46day"]
    c.links = [
        {"label": "Board of Elections", "url": "https://vote.franklincountyohio.gov/"},
        {"label": "2026 election information and notices", "url": "https://vote.franklincountyohio.gov/election-info/2026"},
        {"label": "Sample ballot", "url": "https://vote.franklincountyohio.gov/voters/sample-ballot"},
    ]
    c.results_links = [{"label": "Board of Elections: 2026 election information and results", "url": "https://vote.franklincountyohio.gov/election-info/2026"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it, "
               "with candidates' parties from the Board's candidate list and issue details from its certified questions and issues list and "
               "individual notices of election. Long charter amendments are condensed; the full wording is on the sample ballot and in the "
               "full-text documents on the Board's 2026 page.", NOTE_ORDER, NOTE_PLACES,
               "Franklin County's voter file has no school districts, so school and library issues are placed using the precincts the Board's "
               "46-day notice lists for each issue."]
    D = c.district; P = c.p

    # --- Federal and state legislative ---
    c.contest("congress-3", "U.S. House", "Representative to Congress", [("Joyce Beatty", "DEM"), ("Cleophus Dulaney", "REP")], detail="3rd District", places=D("cong", 3), src=S)
    c.contest("congress-15", "U.S. House", "Representative to Congress", [("Brennan Barrington", "LIB"), ("Mike Carey", "REP"), ("Don Leonard", "DEM")],
              detail="15th District", places=D("cong", 15), src=S)
    for n, cs in {3: [("Stacie A. Baker", "DEM"), ("Michele Reynolds", "REP")], 15: [("Joseph Healy", "REP"), ("Latyna M. Humphrey", "DEM")],
                  25: [("Bill DeMora", "DEM"), ("Don Roberts", "REP")]}.items():
        c.contest(f"senate-{n}", "Ohio General Assembly", "State Senator", cs, detail=f"{ordinal(n)} District", places=D("sen", n), src=S)
    REPS = {
        1: [("Joel A. Greff", "REP"), ("Dontavius Jarrells", "DEM")],
        2: [("Charity Martin King", "DEM")],
        3: [("Bernadine Kennedy Kent", "REP"), ("Ismail Mohamed", "DEM")],
        4: [("Beryl Brown Piccolantonio", "DEM")],
        5: [("Richard Cole", "REP"), ("Meredith R. Lawson-Rowe", "DEM")],
        6: [("Christine Cockley", "DEM"), ("Matthew Jackson", "REP")],
        7: [("Ukeme Awakessien Jeter", "DEM"), ("Cameron Koffel", "Nonparty"), ("William Mercier", "REP")],
        8: [("Kelly Hunter-Kalagidis", "REP"), ("Anita Somani", "DEM")],
        9: [("Munira Yasin Abdullahi", "DEM"), ("Bruce Euans", "REP")],
        10: [("Denise D'Angelo", "REP"), ("Mark Sigrist", "DEM")],
        11: [("Shawn Kaeser", "REP"), ("Crystal Lett", "DEM")],
        12: [("Brian Stewart", "REP"), ("Lee Yarsky", "DEM")],
    }
    for n, cs in REPS.items():
        c.contest(f"rep-{n}", "Ohio General Assembly", "State Representative", cs, detail=f"{ordinal(n)} District", places=D("rep", n), src=S)

    # --- Courts and county offices ---
    c.contest("appeals-10-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Michael C. Mentel", "DEM")], detail="10th District · full term commencing February 9, 2027", src=S)
    c.contest("appeals-10-0701", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Terri Jamison", "DEM")], detail="10th District · full term commencing July 1, 2027", src=S)
    c.contest("commissioner", "County offices", "County Commissioner", [("Erica C. Crawley", "DEM"), ("Eric Terford", "LIB")], detail="Full term commencing January 1, 2027", src=S)
    c.contest("auditor", "County offices", "County Auditor", [("Michael Stinziano", "DEM")], detail="Full term commencing March 8, 2027", src=S)
    NP = " · no party label on the ballot"
    for i, (div, date, cs) in enumerate([
        ("General Division", "January 1, 2027", ["Carl Aveni"]),
        ("General Division", "February 9, 2027", ["Andy Miller"]),
        ("General Division", "July 1, 2027", ["David Young"]),
        ("General Division", "July 2, 2027", ["Chris Brown"]),
        ("Domestic Relations Division", "January 2, 2027", ["Kelley Gabrielle Boller"]),
        ("Domestic Relations Division", "January 3, 2027", ["Lasheyl N. Stroud"]),
        ("Probate Division", "February 9, 2027", ["Kelly Green", "Chris Junga"]),
    ]):
        c.contest(f"cp-{i}", "Court of Common Pleas", f"Judge of the Court of Common Pleas, {div}", cs, detail=f"Full term commencing {date}" + NP, src=S)

    # --- Local questions and issues ---
    N = lambda n: f"Issue {n}"
    est = lambda per: f"{per} for each $100,000 of market value"
    COL = P("COLUMBUS CITY ")

    c.issue("issue-5", "levy", "Bexley City School District", "School district income tax (0.5%, continuing) and bond issue ($29,250,000)", P("BEXLEY CITY"), number=N(5),
            area="Bexley precincts 1-A to 4-C",
            levy={"type": "Income tax and bond issue", "purpose": "Income tax for current expenses; bonds for constructing, renovating, expanding, furnishing and equipping school facilities.",
                  "mills": "2.05 mills (bond, estimated average)", "term": "Income tax continuing from January 1, 2027; bonds up to 30 years",
                  "estimate": "$29,250,000 principal; $72 for each $100,000 of market value (bond)"},
            text="Shall the Bexley City School District be authorized to do both of the following: 1. Impose an annual income tax of 0.5 per cent on the school district income of individuals, for a continuing period of time, beginning January 1, 2027 for the purpose of current expenses? 2. Issue bonds for the purpose of constructing school facilities; renovating, repairing, expanding, improving, and constructing additions to school facilities; furnishing and equipping the same in the principal amount of $29,250,000, to be repaid annually over a maximum period of 30 years, and levy a property tax outside the ten-mill limitation estimated by the county auditor to average over the bond repayment period 2.05 mills, which amounts to $72 for each $100,000 of the county auditor's market value?",
            src=I)
    c.levy("dacc-levy", "Delaware Area Career Center (joint vocational school district; Delaware, Franklin and other counties)", COL, "Renewal and decrease",
           "School maintenance and current expenses (a reduction of 0.95 mill).", "0.75 mill", "10 years, commencing in 2026", None, est("$18"),
           area="Columbus precinct 71-C", note="Unnumbered in Franklin County.", src=I)
    PICK = sorted(set(COL + P("Madison Township", "PICKERINGTON CITY")))
    c.issue("pickerington-lsd-tax", "question", "Pickerington Local School District (Fairfield and Franklin)", "School district income tax increase: 0.75% for 10 years", PICK,
            area="Columbus precincts 45-E, 86-D, 86-E; Madison Township precinct E",
            text="Proposed income tax increase of 0.75% on the school district income of individuals, for 10 years, for current expenses.",
            note="Unnumbered in Franklin County.", src=I)
    c.levy("pickerington-library", "Pickerington Public Library (Fairfield and Franklin)", PICK, "Additional", "Current expenses.", "1.5 mills", "Continuing, commencing in 2026", None, est("$53"),
           area="Columbus precincts 45-E, 86-D, 86-E; Madison Township precinct E", note="Unnumbered in Franklin County.", src=I)
    SWCSD = sorted(set(COL + P("Franklin Township", "GROVE CITY-CITY", "Jackson Township", "Pleasant Township", "HARRISBURG VILLAGE ", "Prairie Township", "URBANCREST VILLAGE")))
    c.issue("issue-6", "levy", "South-Western City School District", "Bond issue: $220,000,000 for new Westland and Grove City high schools and other school facilities", SWCSD, number=N(6),
            area="Parts of Columbus and Prairie Township; Grove City; Franklin, Jackson and Pleasant townships; Harrisburg and Urbancrest villages",
            levy={"type": "Bond issue", "purpose": "Constructing, furnishing and equipping a new Westland High School and new Grove City High School, with related site improvements; constructing, renovating, repairing, expanding and improving other school facilities.",
                  "mills": "2.26 mills (estimated average)", "term": "Up to 38 years", "firstDue": "2027", "estimate": "$220,000,000 principal; $79 for each $100,000 of market value"}, src=I)
    UACSD = sorted(set(COL + P("Perry Township", "UPPER ARLINGTON CITY")))
    c.issue("issue-7", "levy", "Upper Arlington City School District", "Bond issue ($273,500,000) and additional operating levy (4.9 mills, continuing)", UACSD, number=N(7),
            area="Upper Arlington; Columbus precincts 10-E, 63-G, 63-H, 77-C; Perry Township precinct C",
            levy={"type": "Bond issue and additional levy", "purpose": "Bonds for Burbank Early Childhood School, Hastings and Jones middle schools and a high school addition; additional levy for current operating expenses.",
                  "mills": "4.84 mills (bond, estimated average) + 4.9 mills (operating)", "term": "Bonds up to 38 years; operating levy continuing",
                  "estimate": "$273,500,000 principal, $169 per $100,000 (bond); $14,396,791 a year, $172 per $100,000 (operating)"}, src=I)

    c.issue("issue-8", "question", "City of Columbus", "Charter amendment (by petition): council members elected only by voters in their district", COL, number=N(8),
            text="This proposed charter amendment would limit the ability to vote for candidates for Columbus City Council to only those electors living within the districts that those candidates seek to represent. Ballots within council districts would include both citywide races and the district race, and a recall election of a district council member could be started by a petition signed by district electors equal to at least 15% of the votes cast in the district in the preceding mayoral election. Shall the proposed charter amendment be approved?", src=I)
    c.issue("issue-9", "question", "City of Columbus", "Charter amendment (by Council): district-only voting for district seats, at-large seats added, 13-member Council", COL, number=N(9),
            text="This proposed charter amendment would limit the ability to vote for candidates for Columbus City Council to only those electors living within the districts that those candidates seek to represent. It adds two at-large council members elected in 2027 and two more elected in 2029 (four-year terms), moving from a nine-member to an eleven- and then a thirteen-member Council; redraws the council district map in 2027 and raises the allowed population variance between districts from 1% to 7.5%; requires district candidates to have lived in their district for a year before the primary; updates expulsion, quorum and vote requirements; sets petition signature requirements (150 district / 250 at-large); and allows recall of district and at-large members by petition. Shall the proposed charter amendment be approved?", src=I)

    LIQ = [
        ("10a", "Weekday sales (beer, wine and mixed beverages)", "Neubite, L.L.C. (dba Aveneu), 1017 Mt. Vernon Avenue", "COLUMBUS CITY ", "Columbus precinct 07-D"),
        ("10b", "Sunday sales (wine and mixed beverages)", "Neubite, L.L.C. (dba Aveneu), 1017 Mt. Vernon Avenue", "COLUMBUS CITY ", "Columbus precinct 07-D"),
        ("11b", "Sunday sales (wine and mixed beverages)", "Dublin & Grandview Duchess, 1090 Dublin Road", "COLUMBUS CITY ", "Columbus precinct 10-A"),
        ("12b", "Sunday sales (wine and mixed beverages and spirituous liquor)", "Born on Third, 3411 Trabue Rd", "COLUMBUS CITY ", "Columbus precinct 10-D"),
        ("13b", "Sunday sales (wine and mixed beverages)", "Englefield, Inc., dba Morse Rd. Duchess, 927 Morse Road", "COLUMBUS CITY ", "Columbus precinct 22-D"),
        ("14b", "Sunday sales (wine and mixed beverages, and spirituous liquor)", "Third Way Café LLC, 3059 W. Broad Street", "COLUMBUS CITY ", "Columbus precinct 32-A"),
        ("15b", "Sunday sales (wine and mixed beverages)", "RaceTrac, Inc., 30 Rathmell Road", "COLUMBUS CITY ", "Columbus precinct 49-F"),
        ("16a", "Weekday sales (beer, wine and mixed beverages)", "Englefield, Inc., dba E. Broad St. Duchess, 825 E. Broad Street", "COLUMBUS CITY ", "Columbus precinct 55-D"),
        ("16b", "Sunday sales (wine and mixed beverages)", "Englefield, Inc., dba E. Broad St. Duchess, 825 E. Broad Street", "COLUMBUS CITY ", "Columbus precinct 55-D"),
        ("17b", "Sunday sales (wine and mixed beverages)", "Convenient Plus Food Mart, 5435 E. Livingston Avenue", "COLUMBUS CITY ", "Columbus precinct 68-A"),
        ("29b", "Sunday sales (wine and mixed beverages, and spirituous liquor)", "Dapper Dog Tavern, 4057 Broadway", "GROVE CITY-CITY", "Grove City precinct 1-A"),
        ("30b", "Sunday sales (wine and mixed beverages, and spirituous liquor)", "Drunch, 3997 Truepointe Blvd.", "HILLIARD CITY", "Hilliard precinct 2-D"),
        ("31b", "Sunday sales (wine and mixed beverages, and spirituous liquor)", "Medley Kitchen, 3986 Truepointe Blvd. Suite 101", "HILLIARD CITY", "Hilliard precinct 2-D"),
        ("32b", "Sunday sales (wine and mixed beverages, and spirituous liquor)", "Old Scratch Pizza, 3998 Truepointe Blvd.", "HILLIARD CITY", "Hilliard precinct 2-D"),
        ("33b", "Sunday sales (wine and mixed beverages, and spirituous liquor)", "Smoked Lick BBQ Burgers and Booze, 3997 Truepointe Blvd., Suite 101", "HILLIARD CITY", "Hilliard precinct 2-D"),
        ("44a", "Weekday sales (wine and mixed beverages)", "RaceTrac, 2555 London Groveport Road (Madison Township)", "Madison Township", "Madison Township precinct A (includes the part of Lithopolis Village in it)"),
        ("44b", "Sunday sales (wine and mixed beverages)", "RaceTrac, 2555 London Groveport Road (Madison Township)", "Madison Township", "Madison Township precinct A (includes the part of Lithopolis Village in it)"),
        ("46a", "Weekday sales (beer, wine and mixed beverages, and spirituous liquor)", "The Golf Club Company, 4522 Kitzmiller Road (Plain Township)", "Plain Township", "Plain Township precinct A"),
        ("46b", "Sunday sales (wine and mixed beverages, and spirituous liquor)", "The Golf Club Company, 4522 Kitzmiller Road (Plain Township)", "Plain Township", "Plain Township precinct A"),
    ]
    JUR = {"COLUMBUS CITY ": "City of Columbus", "GROVE CITY-CITY": "City of Grove City", "HILLIARD CITY": "City of Hilliard", "Madison Township": "Madison Township", "Plain Township": "Plain Township"}
    for n, what, biz, raw, area in LIQ:
        name = biz.split(",")[0] if not biz.startswith(("Neubite", "Englefield")) else biz.rsplit(",", 1)[0]
        c.issue(f"issue-{n}", "liquor", JUR[raw], f"Local liquor option: {name} ({what.split(' (')[0].replace('Sunday', 'sunday').lower().replace('sunday', 'Sunday')})", P(raw) + (P("LITHOPOLIS VILLAGE") if n.startswith("44") else []), number=N(n.upper() if n.endswith("a") else n), area=area,
                text=f"Local option, particular location: {what}, {biz}.", src=I)

    GAH = P("GAHANNA CITY")
    for n, sec, text in [
        (18, "RES-0026 (mayoral primary)", "Shall Section 3.01, Election and Term, of Article III, Mayor, be amended to eliminate the mayoral primary election when no more than two candidates have filed for the office of Mayor?"),
        (19, "RES-0027 (qualifications of elected officials)", "Shall Section 3.02, Qualifications, of Article III, Mayor; Section 4.03, Qualifications, of Article IV, The Council; and Section 10.02, Qualifications, of Article X, Department of Law, be amended to establish a consistent standard regarding conflicts with other public offices and public employment for the Mayor, Council Members and the City Attorney?"),
        (20, "RES-0028 (ward boundary adjustment)", "Shall Section 4.02, Composition and Term, of Article IV, The Council, be amended to revise the process for adjusting ward boundaries to base it on federal decennial census population data and specified population disparity criteria?"),
        (21, "RES-0029 (legislative procedure: council abstentions)", "Shall Section 4.12, Legislative Procedure, of Article IV, The Council, be amended to require that an alleged improper voting abstention by a Council member be subject to the notice and hearing procedures for removal established in the Charter?"),
        (22, "RES-0030 (administrative departments)", "Shall Article V, Administrative Departments, be amended to remove department listings, preserving the Charter duties of the Director of Finance, and making related organizational changes?"),
        (23, "RES-0031 (City Attorney)", "Shall Sections 10.01, City Attorney, and 10.03, General Powers and Duties, of Article X, Department of Law, be amended to clarify the process for filling vacancies in the office of the City Attorney, update the powers and duties of the office, and make related grammatical revisions?"),
        (24, "RES-0032 (Planning Commission attendance)", "Shall Section 11.02, Planning Commission - Organization, of Article XI, Planning Commission, be amended to authorize the Planning Commission to establish attendance requirements for its members through its rules of operation?"),
        (25, "RES-0033 (zoning appeals)", "Shall Section 11.03, Planning Commission - Powers and Duties, of Article XI, Planning Commission, be amended and Article XII, Board of Zoning and Building Appeals, be repealed to transfer zoning, building, and landscaping appeal functions to the Planning Commission and to transfer Planning Commission appeals to Franklin County courts?"),
        (26, "RES-0034 (Charter Review Commission every ten years)", "Shall Section 22.01, Composition and Term, of Article XXII, Charter Review Commission, be amended to require that the Charter Review Commission be convened every ten years instead of every five years?"),
        (27, "RES-0035 (non-discrimination)", "Shall Section 23.07, Non Discrimination Clause, of Article XXIII, General Provisions, be amended to update the Charter's nondiscrimination provisions to align with the City's Codified Ordinances and applicable federal, state, and local law?"),
    ]:
        c.issue(f"issue-{n}", "question", "City of Gahanna", f"Charter amendment: {sec}", GAH, number=N(n), text=text, src=I)

    c.issue("issue-28", "question", "City of Grove City", "Charter amendment (by petition): Community Consent Amendment (referendum on large developments)", P("GROVE CITY-CITY"), number=N(28),
            text="Amends the city charter to include a new article, Article XI, to establish a mandatory public referendum process as a condition of approval for any proposed development, qualifiable business expansion, or transfer of property ownership that occupies 50 or more contiguous acres, draws or is designed to draw more than 20 megawatts of electrical power at peak capacity, or consumes or is projected to consume more than 500,000 gallons of water per day; and establishes enforceable community impact standards for any approved facility. Shall the charter amendment, as proposed by initiative, be adopted?", src=I)
    c.levy("issue-34", "City of Upper Arlington", P("UPPER ARLINGTON CITY"), "Renewal and increase", "Employer contributions to the Ohio Police and Fire Pension Fund (renewal of 0.89 mill and increase of 0.24 mill).",
           "1.13 mills", "5 years, commencing in 2027", None, f"$2,190,393 a year; {est('$26')}", number=N(34), src=I)
    WOR = P("WORTHINGTON CITY")
    for n, title, text in [
        (35, "Charter amendment: effective date of ordinances (recommended by Commission)", "Shall the Charter of the City of Worthington be amended to delete Section 1.04 REFERENDUM AND EFFECTIVE DATE ON ZONING ORDINANCES OR OTHER ZONING MEASURES in its entirety and to amend Sections 2.17 PROCEDURE IN THE PASSAGE OF ORDINANCES and 2.19 EFFECTIVE DATE OF ORDINANCES as set forth in Exhibit A of Ordinance No. 20-2026 of the City of Worthington?"),
        (36, "Charter amendment: referendum petition signature requirement (recommended by Commission)", "Shall the Charter of the City of Worthington be amended to add Section 1.05 to read as follows: SECTION 1.05 REFERENDUM PETITION SIGNATURE REQUIREMENT. Notwithstanding Section 731.29 of the Ohio Revised Code, the signature requirement for a referendum petition shall be ten percent of the number of electors who voted for governor at the most recent general election for the office of governor in the municipal corporation?"),
        (37, "Charter amendment: various amendments (recommended by Commission)", "Shall the various sections of the Charter of the City of Worthington be amended as set forth in Exhibit A of Ordinance No. 22-2026 of the City of Worthington?"),
        (38, "Charter amendment (by petition): referendum petition signature requirement", "Shall the Charter of the City of Worthington be amended to add Section 1.05 to read as follows: SECTION 1.05 REFERENDUM PETITION SIGNATURE REQUIREMENT. Notwithstanding any other provisions of this Charter, the power of referendum on any ordinance or other measure passed by the Council may be exercised in the manner provided by the laws of the State of Ohio except that the petition signature requirement shall be ten percent of the electors of the City, based on the total vote cast at the last preceding general municipal election?"),
    ]:
        c.issue(f"issue-{n}", "question", "City of Worthington", title, WOR, number=N(n), text=text, src=I)

    c.issue("issue-40", "question", "Brown Township (unincorporated area)", "Township zoning plan (unincorporated area)", P("Brown Township"), number=N(40),
            text="Shall the zoning plan for the unincorporated area of Brown Township as adopted by the board of township trustees be approved?", src=I)
    c.levy("issue-41", "Hamilton Township Road District (unincorporated areas)", P("Hamilton Township"), "Additional", "General construction, reconstruction, resurfacing and repair of streets, roads and bridges.",
           "0.8 mill", "Continuing, commencing in 2026", None, f"$100,131 a year; {est('$28')}", number=N(41), src=I)
    MAD = P("CANAL WINCHESTER CITY", "COLUMBUS CITY ", "GROVEPORT CITY", "Madison Township", "LITHOPOLIS VILLAGE", "PICKERINGTON CITY", "OBETZ CITY")
    MAD_AREA = "Madison Township, Canal Winchester, Groveport, Obetz precinct B, and Columbus precincts 49-E, 85-D, 85-E, 86-A, 86-B, 86-G to 86-J"
    c.levy("issue-42", "Madison Township", MAD, "Additional", "Fire protection, firefighting and emergency medical services.", "4.89 mills", "Continuing, commencing in 2026", None,
           f"$6,842,340 a year; {est('$171')}", number=N(42), area=MAD_AREA, src=I)
    c.levy("issue-43", "Madison Township", MAD, "Additional", "Police protection.", "1.99 mills", "Continuing, commencing in 2026", None,
           f"$2,784,510 a year; {est('$70')}", number=N(43), area=MAD_AREA, src=I)
    c.levy("issue-45", "Mifflin Township Police District (unincorporated area)", P("Mifflin Township"), "Additional", "Police protection.", "6.96 mills", "Continuing, commencing in 2026", None,
           f"$500,322 a year; {est('$244')}", number=N(45), src=I)
    c.levy("issue-47", "Sharon Township Road District (unincorporated area)", P("Sharon Township"), "Additional", "General construction, reconstruction, resurfacing and repair of streets, roads and bridges.",
           "2.46 mills", "Continuing, commencing in 2026", None, f"$285,000 a year; {est('$86')}", number=N(47), src=I)
    c.levy("issue-48", "Truro Township", P("COLUMBUS CITY ", "REYNOLDSBURG CITY ", "Truro Township", "BRICE VILLAGE"), "Renewal and decrease", "Current expenses (renewal of part of an existing 1.5-mill levy, a reduction of 0.5 mill).",
           "1 mill", "5 years, commencing in 2026", None, f"$472,902 a year; {est('$17')}", number=N(48),
           area="Truro Township, Reynoldsburg, and Columbus precincts 45-D and 84-H", src=I)
    return c
