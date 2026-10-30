from lib import County, NOTE_ORDER, NOTE_PLACES

SITE = "https://www.boe.ohio.gov/champaign/"
NOTICE = "https://www.boe.ohio.gov/champaign/c/upload/FWAB_11November46Day.pdf"
BALLOTS = "https://lookup.boe.ohio.gov/vtrapp/champaign/ballotlist.aspx"


def build():
    # Raw names are clean ("ST. PARIS VILLAGE" -> "St. Paris Village", "NORTH LEWISBURG VILLAGE"); no renames needed.
    c = County("champaign", "Champaign", "39021")
    c.src("champaign-46day", "Champaign County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election (revised 9/14/2026)", NOTICE)
    c.src("champaign-ballots", "Champaign County Board of Elections: official sample ballots for all 51 precinct splits, November 3, 2026 (state ballot lookup)", BALLOTS)
    C = I = ["champaign-46day", "champaign-ballots"]
    c.links = [
        {"label": "Board of Elections", "url": SITE},
        {"label": "Election info", "url": "https://www.boe.ohio.gov/champaign/election-info/"},
        {"label": "Sample ballots by precinct", "url": BALLOTS},
        {"label": "Who are my elected officials?", "url": "https://lookup.boe.ohio.gov/vtrapp/champaign/cnm.aspx"},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://www.boe.ohio.gov/champaign/election-info/election-results/"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it "
               "and gives the full ballot wording of each issue, checked against the Board's sample ballots for all 51 precinct splits. "
               "Where the two differ, the sample ballot's wording is used.",
               NOTE_ORDER, NOTE_PLACES,
               "The Board's ballots do not give local issue numbers."]
    P = c.p; SD = c.sd

    # --- Federal, state legislative, appeals (all of Champaign County is in each district; the 12th Senate seat is not on the ballot) ---
    # The notice and ballots print no party for Tackett (an independent candidate), as in logan.py, clark.py and union.py.
    c.contest("congress-4", "U.S. House", "Representative to Congress", [("Jim Jordan", "REP"), ("Joshua D. Kolasinski", "DEM"), ("Tracey L. Tackett", "Nonparty")],
              detail="4th District", src=C)
    c.contest("rep-85", "Ohio General Assembly", "State Representative", [("Tim Barhorst", "REP"), ("Victoria Maddox", "DEM")], detail="85th District", src=C)
    # Same race as clark.py and miami.py.
    c.contest("appeals-2-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Chris Epley", "REP")], detail="2nd District · term commencing February 9, 2027", src=C)

    # --- County offices ---
    # Woodruff and Ritchie are printed with no party on the notice and the ballots (independent candidates).
    c.contest("commissioner", "County offices", "County Commissioner", [("Karen T. Bailey", "REP"), ("Jacob McKee", "DEM"), ("Todd Woodruff", "Nonparty")],
              detail="Full 4-year term commencing January 1, 2027", src=C)
    c.contest("auditor", "County offices", "County Auditor", [("John Patrick Ritchie", "Nonparty"), ("Nino Vitale", "REP")],
              detail="Full 4-year term commencing March 8, 2027", src=C)
    NP = " · no party label on the ballot"
    # The notice heads both seats "Juvenile Probate Division Judge"; the ballots say "Juvenile/Domestic/Probate Division".
    office = "Judge of the Court of Common Pleas, Juvenile/Domestic/Probate Division"
    c.contest("cp-juv-dr-probate-0209", "Court of Common Pleas", office, ["Lori L. Reisinger"], detail="Full 6-year term commencing February 9, 2027" + NP, src=C)
    c.contest("cp-juv-dr-probate-0210", "Court of Common Pleas", office, ["Brett A. Gilbert"], detail="Full 6-year term commencing February 10, 2027" + NP, src=C)

    # --- City of Urbana: mayor (successor if the recall passes) ---
    URB = P("URBANA CITY")
    URBA = "Urbana 1-A to 4-B (all city precincts)"
    c.contest("mayor-urbana", "Municipal offices", "Mayor, City of Urbana", ["Eugene E. Fields, Jr."],
              detail="Unexpired term ending December 31, 2027 · printed with the recall question and filled only if Mayor Bill Bean is recalled" + NP,
              places=URB, area=URBA, src=C)

    # --- Issues (unnumbered on the ballots; listed in the notice's order) ---
    est = lambda total, per: f"{total} a year; {per} for each $100,000 of market value"
    # The 46-day notice says $14 per $100,000; every sample ballot says $6. The ballot wording is used.
    c.levy("health-district", "Champaign County (Champaign Health District)", "county", "Renewal", "Operation of the Champaign Health District.",
           "0.4 mill", "5 years, commencing in 2027", "2028", est("$303,400", "$6"),
           note="The sample ballots give $6 for each $100,000 of market value; the Board's 46-day notice gives $14.", src=I)
    c.levy("dd-levy", "Champaign County", "county", "Additional",
           "Community developmental disabilities programs and services, and developmental disabilities facilities (Champaign County Board of Developmental Disabilities).",
           "1.5 mills", "5 years, commencing in 2027", "2028", est("$2,412,660", "$53"), src=I)
    c.issue("urbana-charter-data-center", "question", "City of Urbana", "Charter amendment: prohibit the construction of data centers (new Section 8.07)", URB, area=URBA,
            text="Shall Article VIII of the Charter of the City of Urbana be amended to add Section 8.07, to read as follows? "
                 "Article VIII, Section 8.07. Prohibition of a Data Center. (A) the construction of a data center is hereby prohibited. "
                 "(B) as used in this Section, \"construction\" shall mean the erection of one or more buildings, infrastructure, facilities and related activities, "
                 "which include preparations and modifications for same, for a common purpose. (C) as used in this Section, \"data center\" shall mean one or more "
                 "buildings or physical facilities or infrastructure, located on a single real property parcel or on contiguous, adjacent, or otherwise aggregated "
                 "real property parcels that are used primarily or exclusively for digital information services such as the management, storage, processing and "
                 "dissemination of electronic data and information, including but not limited to the implementation of artificial intelligence, through the use of "
                 "computer systems, servers, networking equipment, and related components, including equipment cooling systems, or virtual currency mining. "
                 "(D) this Section shall not apply to data centers, as defined in this section, whose sole purpose is to serve as a dedicated facility that supports "
                 "the computing needs of a single organization or enterprise not otherwise engaged in the business of management, storage, processing, and/or "
                 "dissemination of electronic data and information and which is wholly owned by that enterprise, and which has an aggregate monthly demand or peak "
                 "load of less than seven-point-five (7.5) megawatts, however derived from any energy source, or a combination thereof. (E) this Section is self-executing.",
            src=I)
    c.issue("urbana-mayor-recall", "question", "City of Urbana", "Recall of Mayor Bill Bean (by petition)", URB, area=URBA,
            text="Shall BILL BEAN be removed from the office of MAYOR of the CITY OF URBANA BY RECALL?",
            note="The same ballot box elects a successor for the unexpired term ending December 31, 2027 (Eugene E. Fields, Jr. is the only candidate); see the Mayor contest.",
            src=I)
    c.levy("goshen-memorial-park", "Goshen Township (Goshen Township Memorial Park)", P("GOSHEN TOWNSHIP", "MECHANICSBURG VILLAGE"), "Renewal",
           "Township memorial park district: purchasing, appropriating, operating, maintaining and improving land for park and recreational purposes.",
           "1 mill", "5 years, commencing in 2027", "2028", est("$55,500", "$13"), area="Mechanicsburg, Goshen North, Goshen South", src=I)
    c.levy("rush-roads", "Rush Township (excluding the villages of Woodstock and North Lewisburg)", P("RUSH TOWNSHIP"), "Renewal",
           "General construction, reconstruction, resurfacing and repair of roads and bridges.", "1 mill", "5 years, commencing in 2027", "2028",
           est("$11,000", "$6"), area="Rush (split 1)", src=I)
    # The notice adds Urbana 4-A and 4-B split 2 (the part of the city in Salem Township) to Salem North and South.
    c.levy("salem-fire-ems", "Salem Township", P("SALEM TOWNSHIP", "URBANA CITY"), "Renewal", "Fire and EMS services.", "3 mills",
           "5 years, commencing in 2027", "2028", est("$210,500", "$64"), area="Salem North, Salem South, plus Urbana 4-A and 4-B (split 2)", src=I)
    c.levy("wayne-roads", "Wayne Township", P("WAYNE TOWNSHIP"), "Renewal", "General construction, reconstruction, resurfacing and repair of roads.", "2.5 mills",
           "5 years, commencing in 2027", "2028", est("$68,500", "$24"), area="Wayne North, Wayne South", src=I)
    # Same two levies as clark.py (northwestern-lsd-pi, northwestern-lsd-current).
    NW = SD("NORTHWESTERN LOCAL SD (CLARK)")
    NWJ = "Northwestern Local School District (Clark and Champaign)"
    NWA = "Northwestern Local School District, Champaign County part (Mad River A split 3, Urbana South split 2)"
    c.levy("northwestern-lsd-pi", NWJ, NW, "Renewal", "Permanent improvements.", "1 mill", "5 years, commencing in 2026", "2027",
           est("$225,394", "$35"), area=NWA, src=I)
    # The notice omits "renewing an existing levy"; the ballots have it (and clark.py has it as a renewal).
    c.levy("northwestern-lsd-current", NWJ, NW, "Renewal", "Current operating expenses (fixed sum of $1,756,160).", "4.32 mills (estimated average)",
           "5 years, commencing in 2026", "2027", "$151 for each $100,000 of market value", area=NWA, src=I)
    c.levy("johnson-st-paris-fire", "Johnson St. Paris Fire District", P("ST. PARIS VILLAGE", "JOHNSON TOWNSHIP"), "Renewal",
           "Providing and maintaining fire apparatus, appliances, buildings or sites.", "2.25 mills", "5 years, commencing in 2027", "2028",
           est("$153,000", "$35"), area="St Paris (splits 1 and 2), Johnson", src=I)
    # The notice lists "0028/1 Urbana North, 0028/1 Urbana South, 0028/2 Urbana South"; the ballots put the levy on 0028/1 Urbana North and 0029/1-2 Urbana South.
    c.levy("urbana-twp-fire-ems", "Urbana Township (unincorporated, excluding the City of Urbana)", P("URBANA TOWNSHIP"), "Additional",
           "Fire and emergency medical (ambulance) services, including payment of firefighting companies or permanent, part-time or volunteer firefighters and EMS.",
           "4 mills", "Continuing, commencing in 2026", "2027", est("$525,000", "$140"), area="Urbana North, Urbana South (splits 1 and 2)", src=I)
    return c
