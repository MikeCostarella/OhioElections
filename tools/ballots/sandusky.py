from lib import County, NOTE_ORDER, NOTE_PLACES

SITE = "https://sanduskycountyoh.gov/index.php?page=board-of-elections"
UP = "https://sanduskycountyoh.gov/uploads/"
NOTICE = UP + "46%20day%20FWAB%20November%202026.docx"
CAND = UP + "Sandusky%20County%20Candidates%20November%20General%20Election%202026.xlsx"
ISSUES = UP + "Sandusky%20County%20Issues%20November%20General%20Election%202026.txt"
SAMPLE = UP + "2026%20General%20Election-Sample.pdf"


def build():
    # The voter file splits the three cities by precinct; each piece gets its city's name (lib lists it once).
    # Bellevue is shared with Erie, Huron and Seneca. Riley Township's voters are coded "RICE TOWNSHIP" in the SoS file
    # (precinct RILEY), so there is no Riley Township place; neither township has a local issue (see notes).
    rename = {f"BELLEVUE CITY {p}": "Bellevue City" for p in ("1-A", "1-B", "2-A", "2-B")}
    rename.update({f"CLYDE CITY {p}": "Clyde City" for p in "ABCDE"})
    rename.update({f"FREMONT CITY {w}-{p}": "Fremont City" for w in "1234" for p in "ABCD"})  # there is no 3-D; unused keys are harmless
    c = County("sandusky", "Sandusky", "39143", rename=rename)
    c.src("sandusky-46day", "Sandusky County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election", NOTICE)
    c.src("sandusky-cand", "Sandusky County Board of Elections: candidates, November 3, 2026 General Election", CAND)
    c.src("sandusky-issues", "Sandusky County Board of Elections: issues (ballot wording), November 3, 2026 General Election", ISSUES)
    c.src("sandusky-sample", "Sandusky County Board of Elections: 2026 General Election sample ballots (all precincts)", SAMPLE)
    C = ["sandusky-46day", "sandusky-cand"]; I = ["sandusky-46day", "sandusky-issues"]; IS = I + ["sandusky-sample"]
    c.links = [
        {"label": "Board of Elections", "url": SITE},
        {"label": "Sample ballots (all precincts)", "url": SAMPLE},
        {"label": "Early voting hours", "url": UP + "OFFICE%20HOURS%20NOV%202026.pdf"},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": SITE}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it, "
               "checked against the Board's candidate list, its issues list (which gives the full ballot wording) and its sample ballots.",
               NOTE_ORDER, NOTE_PLACES,
               "The Board's notice, issues list and sample ballots do not give local issue numbers.",
               "The state voter file lists Riley Township's voters under Rice Township, so Riley Township is not in the list of places: "
               "Riley Township voters can use Rice Township (neither township has a local issue on this ballot)."]
    P = c.p; SD = c.sd

    # --- Federal, state legislative, appeals (all of Sandusky County is in each district; the 26th Senate seat is not up) ---
    c.contest("congress-5", "U.S. House", "Representative to Congress", [("Bob Latta", "REP"), ("Brian A. Shaver", "DEM"), ("Michael J. Veloff", "LIB")],
              detail="5th District", src=C)
    c.contest("rep-88", "Ohio General Assembly", "State Representative", [("Gary Click", "REP"), ("Aaron W. Jones", "DEM")], detail="88th District", src=C)
    c.contest("appeals-6-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Michael R. Goulding", "REP")], detail="6th District · full term commencing February 9, 2027", src=C)
    c.contest("appeals-6-0210", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Myron C. Duhart", "DEM"), ("CJ Kamm", "REP")], detail="6th District · full term commencing February 10, 2027", src=C)

    # --- County offices ---
    c.contest("commissioner", "County offices", "County Commissioner", [("Richard J. Farmer II", "REP"), ("Kurtis A. Kuhl", "DEM")],
              detail="Full term commencing January 1, 2027", src=C)
    c.contest("commissioner-unexpired", "County offices", "County Commissioner", [("Jill A. Simpson", "DEM"), ("Justin C. Smith", "REP")],
              detail="Unexpired term ending January 2, 2029", src=C)
    c.contest("auditor", "County offices", "County Auditor", [("David W. Freitag", "REP")], src=C)
    # The notice gives Ickes "R" and Ontko "N/P"; judges carry no party label on the general-election ballot (as the sample ballots show).
    NP = " · no party label on the ballot"
    c.contest("cp-gen-0101", "Court of Common Pleas", "Judge of the Court of Common Pleas, General Division", ["Jon M. Ickes", "Kimberly Ontko"],
              detail="Full term commencing January 1, 2027" + NP, src=C)
    c.contest("cp-gen-0210", "Court of Common Pleas", "Judge of the Court of Common Pleas, General Division", ["Jeremiah Ray"],
              detail="Full term commencing February 10, 2027" + NP, src=C)
    c.contest("cp-probate-juvenile", "Court of Common Pleas", "Judge of the Court of Common Pleas, Probate/Juvenile Division", ["Brad Smith"],
              detail="Full term commencing February 9, 2027" + NP, src=C)

    est = lambda total, per: f"{total} a year; {per} for each $100,000 of the county auditor's market value"

    # --- Issues (unnumbered; in the notice's order) ---
    c.levy("ballville-fire", "Ballville Township", P("BALLVILLE TOWNSHIP"), "Renewal", "Fire protection.", "1.75 mills",
           "5 years, commencing in 2027", "2028", est("$279,953", "$36"), area="Ballville Township (Ballville A to G)", src=I)
    # Same question as erie.py's issue-8.
    c.levy("bellevue-parks", "City of Bellevue (Erie, Huron, Sandusky and Seneca)", P("BELLEVUE CITY 1-A"), "Renewal", "Parks and recreation.", "1 mill",
           "5 years, commencing in 2027", "2028", est("$181,373", "$19"), area="Bellevue City, Sandusky County part (Bellevue 1-A, 1-B, 2-A, 2-B)", src=I)
    c.issue("liquor-bellevue-1a-the-hut", "liquor", "City of Bellevue", "Local liquor option: The Hut AA (Sunday)", P("BELLEVUE CITY 1-A"), area="Bellevue precinct 1-A",
            text="Shall the sale of beer, wine and mixed beverages, and spirituous liquor be permitted for sale on Sunday by The Hut AA, LLC an applicant for a D-6 liquor permit "
                 "who is engaged in the business of operating bar and grill for purpose of serving food and drinks at 938 W Main St Bellevue, Ohio 44811 in this precinct?", src=I)

    CLY = P("CLYDE CITY A"); CA = "Clyde City (Clyde A to E)"
    CHARTER = [
        (1, "Compensation of Council members and the Mayor",
         "Shall the City of Clyde Charter be amended to (1) delete the existing Council member salary language from Section 3-1; (2) delete the Mayor salary sentence from Section 3-7 "
         "and enshrine a Vice Mayor meeting coverage stipend of $100.00 per meeting presided over in the Mayor's absence; and (3) replace Section 3-9 in its entirety to establish "
         "Council member base compensation at the OPERS Monthly Minimum multiplied by twelve, with an additional $2,400 annual premium for the Mayor, automatic annual adjustments, "
         "per-member delayed implementation for currently serving members, prohibitions on legislative modification of all Council compensation including the Vice Mayor meeting "
         "stipend, and codification of the City Manager's wage recommendation authority?"),
        (2, "Council meetings by electronic means during a state of emergency",
         "Shall the City of Clyde Charter be amended to add a paragraph to Section 3-5 authorizing Council to hold meetings by electronic means during any period in which a state of "
         "emergency has been declared by the President of the United States, the Governor of the State of Ohio, or the Mayor of the City of Clyde, subject to compliance with Ohio's "
         "Open Meetings Act and a thirty-day wind-down period following termination of the emergency?"),
        (3, "Modernizing publication and notice requirements",
         "Shall the City of Clyde Charter be amended to replace Section 4-8 in its entirety to eliminate the mandatory newspaper publication requirement for ordinances and resolutions "
         "in favor of digital-first publication methods including posting on the City's official website, physical City Hall posting, or electronic notification; to modernize "
         "codification and adoption-by-reference provisions; to add a savings clause preventing technical publication errors from invalidating an otherwise valid ordinance; and to "
         "delete the third paragraph of Section 7-2 eliminating the Planning Commission's Charter-level newspaper notice requirement for public hearings on zoning and rezoning matters?"),
        (4, "Eliminating the Civil Service Commission; personnel authority to the City Manager",
         "Shall the City of Clyde Charter be amended to delete Sections 7-6, 7-7, and 7-8 establishing the Civil Service Commission and its duties; to replace them with a new Section "
         "7-6 vesting full personnel authority in the City Manager, eliminating the application of ORC Chapter 124 civil service procedures except as required by the Ohio Constitution, "
         "providing that employee appeals shall be governed by the Employee Handbook as adopted and amended by Council, authorizing Council to establish an appeals authority by "
         "resolution, and protecting collective bargaining rights; to renumber Sections 7-9 through 7-13 as Sections 7-7 through 7-11, respectively, without substantive change, with a "
         "cross-reference savings clause; and to make a conforming update to Section 5-3?"),
    ]
    for n, what, text in CHARTER:
        c.issue(f"clyde-charter-{n}", "question", "City of Clyde", f"Charter amendment #{n}: {what}", CLY, area=CA, text=text, src=I)
    c.issue("clyde-income-tax", "question", "City of Clyde", "Municipal income tax: continuation of the existing 1.5% levy on income", CLY, area=CA,
            text="Shall the Ordinance providing for the continuation of an existing 1.5 per cent levy on income for the general operations, maintenance, new equipment, extension and "
                 "enlargement of municipal services and facilities, and capital improvements be passed?", src=I)

    c.issue("liquor-gibsonburg-a-gails", "liquor", "Village of Gibsonburg", "Local liquor option: Gail's Party Shoppe (Sunday)", P("GIBSONBURG VILLAGE"), area="Gibsonburg precinct A",
            text="Shall the sale of spirituous liquor be permitted for sale on Sunday by Gail's Party Shoppe a holder of a C-1, C-2 and D-6 liquor permit who is engaged in the "
                 "business of convenience store/liquor store at 201 S Main St Gibsonburg, Ohio 43431 in this precinct?", src=I)
    c.levy("green-creek-fire", "Green Creek Township", P("GREEN CREEK TOWNSHIP"), "Renewal", "Fire protection.", "1.65 mills",
           "5 years, commencing in 2027", "2028", est("$110,745", "$30"), area="Green Creek Township (Green Creek A to D; not Green Springs Village)", src=I)
    # Same question as seneca.py's green-springs-fire.
    c.levy("green-springs-fire", "Village of Green Springs (Sandusky and Seneca)", P("GREEN SPRINGS VILLAGE"), "Additional", "Fire protection.", "3 mills",
           "5 years, commencing in 2026", "2027", est("$69,080", "$105"), area="Green Springs Village, Sandusky County part", src=I)
    # The notice lists Jackson A, B and Helena (part); the sample ballots show Burgoon Village votes in precinct Jackson Twp B.
    c.levy("jackson-current", "Jackson Township (including Burgoon and part of Helena)", P("JACKSON TOWNSHIP", "BURGOON VILLAGE", "HELENA VILLAGE"), "Renewal", "Current expenses.", "1.5 mills",
           "5 years, commencing in 2027", "2028", est("$89,862", "$37"), area="Jackson Township (Jackson A, Jackson B with Burgoon, and the Jackson Township part of Helena)", src=IS)
    # Same question as erie.py's issue-1 (Erie numbers it 1).
    c.issue("margaretta-lsd-bond", "levy", "Margaretta Local School District (Erie and Sandusky)", "Bond issue: $11,000,000 for a natatorium and fitness/multipurpose center",
            SD("MARGARETTA LOCAL SD (ERIE)"), area="Margaretta Local School District, Sandusky County part (Townsend Township, part)",
            levy={"type": "Bond issue", "purpose": "Constructing a natatorium and fitness/multipurpose center; furnishing and equipping them; and improving their sites.",
                  "mills": "2.15 mills (estimated average)", "term": "Up to 20 years, commencing in 2026", "firstDue": "2027",
                  "estimate": "$11,000,000 principal; $76 for each $100,000 of the county auditor's market value"},
            text="Shall bonds be issued by the Margaretta Local School District for the purpose of constructing a natatorium and fitness/multipurpose center; furnishing and equipping the same as necessary; "
                 "and improving the sites thereof in the principal amount of $11,000,000, to be repaid annually over a maximum period of 20 years, and an annual levy of property taxes be made outside "
                 "the 10-mill limitation, estimated by the county auditor to average over the repayment period of the bond issue 2.15 mills for each $1 of taxable value, which amounts to $76 for each "
                 "$100,000 of the county auditor's market value, commencing in 2026, first due in calendar year 2027, to pay the annual debt charges on the bonds, and to pay debt charges on any notes "
                 "issued in anticipation of those bonds?", src=I)
    # Same question as seneca.py's old-fort-schools.
    c.levy("old-fort-schools", "Old Fort Local School District (Seneca and Sandusky)", SD("OLD FORT LOCAL SD (SENECA)"), "Renewal",
           "Current operating expenses and general permanent improvements.", "6.3 mills (4.30 mills current operating, 2.00 mills permanent improvements)",
           "5 years, commencing in 2027", "2028", est("$528,626", "$111"), area="Old Fort Local School District, Sandusky County part (Ballville A, part)",
           note="The county auditor certified the district's carry-over balance in excess of the preceding year's general fund expenditures as $0 (0%).", src=I)
    c.levy("park-district", "Sandusky County Park District", "county", "Renewal", "Parks and recreation.", "1 mill",
           "10 years, commencing in 2027", "2028", est("$1,461,911", "$20"), src=I)
    c.levy("criminal-justice", "Sandusky County", "county", "Renewal", "County criminal justice services.", "0.55 mill",
           "5 years, commencing in 2027", "2028", est("$857,563", "$14"), src=I)
    c.levy("sandusky-twp-fire", "Sandusky Township", P("SANDUSKY TWP"), "Renewal", "Fire protection.", "1 mill",
           "5 years, commencing in 2027", "2028", est("$124,069", "$21"), area="Sandusky Township (Sandusky A to D)", src=I)
    c.levy("scott-fire", "Scott Township", P("SCOTT TOWNSHIP"), "Renewal and increase", "Fire protection.", "2 mills (renewal of 1 mill and increase of 1 mill)",
           "5 years, commencing in 2026", "2027", est("$75,535", "$42"), src=I)
    c.levy("scott-refuse", "Scott Township", P("SCOTT TOWNSHIP"), "Renewal", "Refuse collection.", "0.5 mill",
           "5 years, commencing in 2026", "2027", est("$16,952", "$9"), src=I)
    c.levy("townsend-roads", "Townsend Township", P("TOWNSEND TOWNSHIP"), "Renewal", "General construction, reconstruction, resurfacing and repair of streets, roads and bridges.", "1.5 mills",
           "5 years, commencing in 2027", "2028", est("$140,362", "$37"), src=I)
    c.levy("woodville-twp-cemetery", "Woodville Township (including the Village of Woodville)", P("WOODVILLE TOWNSHIP", "WOODVILLE VILLAGE"), "Renewal", "Cemetery maintenance.", "0.5 mill",
           "5 years, commencing in 2026", "2027", est("$54,243", "$11"), area="Woodville Township and Woodville Village (Woodville Twp., Woodville Vlg. A and B)", src=I)
    c.levy("woodville-village-current", "Village of Woodville", P("WOODVILLE VILLAGE"), "Renewal", "Current expenses.", "9.4 mills",
           "5 years, commencing in 2026", "2027", est("$330,150", "$210"), area="Woodville Village (Woodville Vlg. A and B)", src=I)
    return c
