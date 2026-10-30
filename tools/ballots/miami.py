from lib import County, NOTE_ORDER, NOTE_PLACES

NOTICE = "https://www.boe.ohio.gov/miami/c/upload/FWAB_11November46Day.pdf"
PIQUA = "https://www.boe.ohio.gov/miami/c/upload/FWAB__PiquaSpecialNovember3,2026.pdf"

def build():
    # Raw names display correctly ("TIPP CITY" -> "Tipp City", "UNION CITY" -> "Union City", "LOSTCREEK TOWNSHIP"); no renames needed.
    c = County("miami", "Miami", "39109")
    c.src("miami-46day", "Miami County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election", NOTICE)
    c.src("miami-piqua-special", "Miami County Board of Elections: 46-day election notice (FWAB), November 3, 2026 Piqua Special Election", PIQUA)
    S = ["miami-46day"]; PS = ["miami-piqua-special"]
    c.links = [
        {"label": "Board of Elections", "url": "https://www.boe.ohio.gov/miami/"},
        {"label": "Election info", "url": "https://www.boe.ohio.gov/miami/election-info/"},
        {"label": "Sample ballots by precinct", "url": "https://lookup.boe.ohio.gov/vtrapp/miami/ballotlist.aspx"},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://www.boe.ohio.gov/miami/election-info/"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it. "
               "Issue wording is the Board's summary; the full wording is on the sample ballot.",
               NOTE_ORDER, NOTE_PLACES,
               "The Board's notice does not give local issue numbers; see your sample ballot for them.",
               "Piqua also holds a city special election on November 3, 2026 (three recall questions and a charter amendment), on its own ballot. "
               "The Board's special-election notice says the ward candidates' names would be published after October 16; they are not listed here."]
    P = c.p; D = c.district; SD = c.sd

    # 8th and 15th Congressional districts; the 5th Senate and 80th House districts cover the whole county.
    # Write-ins Gary Josephson and Samuel Ronan (15th) are not listed.
    c.contest("congress-8", "U.S. House", "Representative to Congress", [("Warren Davidson", "REP"), ("Vanessa Enoch", "DEM")],
              detail="8th District (Hamilton, Butler (part), Preble, Darke and Miami (part) counties)", places=D("cong", 8), src=S)
    c.contest("congress-15", "U.S. House", "Representative to Congress", [("Brennan Barrington", "LIB"), ("Mike Carey", "REP"), ("Don Leonard", "DEM")],
              detail="15th District", places=D("cong", 15), src=S)
    c.contest("senate-5", "Ohio General Assembly", "State Senator", [("Jeffrey Harris", "DEM"), ("Phil Plummer", "REP")], detail="5th District", src=S)
    c.contest("rep-80", "Ohio General Assembly", "State Representative", [("Johnathan Newman", "REP"), ("Katie Koehler Wagner", "DEM")], detail="80th District", src=S)
    c.contest("appeals-2-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Chris Epley", "REP")], detail="2nd District · term commencing February 9, 2027", src=S)
    c.contest("commissioner", "County offices", "County Commissioner", [("Ted Mercer", "REP"), ("Bill Whitten", "DEM")], detail="Term commencing January 1, 2027", src=S)
    c.contest("auditor", "County offices", "County Auditor", [("Matthew W. Gearhardt", "REP")], detail="Term commencing March 8, 2027", src=S)
    NP = " · no party label on the ballot"
    # The notice prints "(Republican)" for both judges; Common Pleas judges carry no party label on the general-election ballot.
    c.contest("cp-0209", "Court of Common Pleas", "Judge of the Court of Common Pleas", ["Jeannine N. Pratt"], detail="Term commencing February 9, 2027" + NP, src=S)
    c.contest("cp-juvenile-probate", "Court of Common Pleas", "Judge of the Court of Common Pleas, Juvenile/Probate Division", ["Katherine Kemp Severt"],
              detail="Term commencing February 9, 2027" + NP, src=S)

    # --- Countywide issues ---
    est = lambda total, per: f"{total} a year; {per} for each $100,000 of the county auditor's market value"
    c.levy("tri-county-mental-health", "Tri-County Board of Recovery and Mental Health Services (Darke, Miami and Shelby counties)", "county", "Renewal",
           "Counseling and supportive services to children and adults through alcohol and drug addiction programs and mental health programs.", "0.6 mill",
           "5 years, commencing in 2027", "2028", est("$2,596,848", "$10"), area="All of Miami County", src=S)
    c.levy("park-district", "Miami County Park District", "county", "Additional",
           "Maintenance and improvement of the Park District's nature reserves, preserves and facilities, and its programs.", "1.4 mills",
           "10 years, commencing in 2026", "2027", est("$5,966,102", "$49"), area="All of Miami County",
           note="Replaces the operations now funded by the District's existing 1.5-mill levy: the Board of Park Commissioners has resolved not to collect that levy if this one passes.", src=S)

    # --- Local issues ---
    c.levy("casstown-operating", "Village of Casstown", P("CASSTOWN VILLAGE"), "Renewal", "General operating expenses.", "0.3 mill",
           "5 years, commencing in 2027", "2028", est("$10,478", "$56"), area="Casstown Village (precinct 057/1)", src=S)
    # Precincts 038-045 are Tipp City and 058-062 Monroe Township.
    c.levy("monroe-twp-community-services", "Monroe Township (incorporated and unincorporated areas)", P("MONROE TOWNSHIP", "TIPP CITY"), "Renewal",
           "Current expenses of Tipp Monroe Community Services and its recreational and enrichment programs and activities.", "0.5 mill",
           "5 years, commencing in 2027", "2028", est("$248,022", "$10"), area="Monroe Township and Tipp City", src=S)
    # The notice adds Concord, Monroe, Tipp City, Newton, Staunton, Union and Washington precincts to Troy's own; SD() matches them.
    c.levy("troy-csd-operating", "Troy City School District", SD("TROY CITY SD"), "Renewal", "Current expenses.", "5.8 mills",
           "5 years, commencing in 2026", "2027", est("$4,630,513", "$111"), area="Troy City School District", src=S)
    # Precincts 046-049 are Bethel Township's own; the Huber Heights piece of Bethel West (048/2) is not in the fire district.
    c.levy("bethel-fire-district", "Bethel Township Fire District One", P("BETHEL TOWNSHIP"), "Renewal", "Fire and emergency medical services.", "4.9 mills",
           "5 years, commencing in 2027", "2028", est("$795,046", "$103"), area="Bethel Township Fire District One (precincts 046–049)", src=S)
    c.levy("concord-twp-fire-ems", "Concord Township (unincorporated area)", P("CONCORD TOWNSHIP"), "Renewal", "Fire protection, ambulance and emergency medical services.",
           "3.7 mills", "5 years, commencing in 2027", "2028", est("$668,475", "$70"), area="Concord Township unincorporated area (precincts 051–055)", src=S)
    c.levy("monroe-fire-district", "Monroe Township Fire District One", P("MONROE TOWNSHIP"), "Renewal and increase", "Fire protection and emergency medical services (renewal of 4 mills and increase of 2 mills).",
           "6 mills", "5 years, commencing in 2027", "2028", est("$1,332,732", "$160"),
           area="Monroe Township Fire District One (precincts 058–062)", src=S)
    c.issue("liquor-phill-exchange", "liquor", "Village of Pleasant Hill", "Local liquor option: The PHill Exchange (beer)", P("PLEASANT HILL VILLAGE"),
            area="Pleasant Hill precinct 068/1",
            text="Sale of beer by The PHill Exchange LLC, a D-1 permit holder (restaurant/stationary food truck), 210 W. High St., Pleasant Hill.", src=S)

    # --- Piqua special election (separate ballot, same day) ---
    PQ = P("PIQUA CITY")
    c.issue("piqua-charter-data-center", "question", "City of Piqua", "Charter amendment: prohibit construction of a data center", PQ, area="All Piqua precincts (001–016)",
            text="Add Section 138 to the Piqua City Charter prohibiting construction of a data center: one or more buildings or facilities on a single or aggregated parcel used "
                 "primarily for digital information services, with an aggregate monthly demand or peak load over 25 megawatts. The section is self-executing.",
            note="Listed in the general-election notice under \"Special Election\".", src=S + PS)
    for who, seat in [("James D. Vetter", "Ward One Commissioner and Mayor"), ("William Frederick Walker", "Ward Three Commissioner"),
                      ("Frank DeBrosse", "Ward Five Commissioner and Vice Mayor")]:
        c.issue("piqua-recall-" + who.split()[-1].lower(), "question", "City of Piqua", f"Recall: {who}, {seat}", PQ, area="All Piqua precincts (001–016)",
                text=f"Shall {seat} {who} be removed from the Piqua City Commission by recall?", src=PS)
    return c
