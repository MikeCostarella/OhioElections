from lib import County, NOTE_ORDER, NOTE_PLACES

NOTICE = "https://www.boe.ohio.gov/carroll/c/upload/FWAB_11November46Day.pdf"
CANDISS = "https://www.boe.ohio.gov/carroll/c/upload/Election_CandidateandIssuesList.pdf"
BALLOTS = "https://lookup.boe.ohio.gov/vtrapp/carroll/ballotlist.aspx"


def build():
    # The voter file abbreviates Washington Township as "WASH. TWP".
    c = County("carroll", "Carroll", "39019", rename={"WASH. TWP": "Washington Township"})
    c.src("carroll-46day", "Carroll County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election (revised 9/17/2026)", NOTICE)
    c.src("carroll-candiss", "Carroll County Board of Elections: list of candidates and issues, November 3, 2026 General Election (updated 9/18/2026)", CANDISS)
    S = ["carroll-46day", "carroll-candiss"]
    c.links = [
        {"label": "Board of Elections", "url": "https://www.boe.ohio.gov/carroll/"},
        {"label": "Election information", "url": "https://www.boe.ohio.gov/carroll/election-info/"},
        {"label": "Sample ballots by precinct", "url": BALLOTS},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://www.boe.ohio.gov/carroll/election-info/election-results/"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it, "
               "checked against the Board's list of candidates and issues (which names the precincts). Issue wording is the Board's summary; the full wording is on the sample ballot.",
               NOTE_ORDER, NOTE_PLACES,
               "The Board's notice and candidates and issues list do not give local issue numbers; see your sample ballot for them."]
    P = c.p; SD = c.sd
    NP = " · no party label on the ballot"
    est = lambda total, per: f"{total} a year; {per} for each $100,000 of market value"

    # --- Federal, state legislative, appeals (each covers the whole county) ---
    c.contest("congress-6", "U.S. House", "Representative to Congress", [("Elizabeth Kirtley", "DEM"), ("Michael A. Rulli", "REP")], detail="6th District", src=S)
    c.contest("senate-33", "Ohio General Assembly", "State Senator", [("Al Cutrona", "REP"), ("Michael L. Kripchak", "DEM")], detail="33rd District", src=S)
    c.contest("rep-79", "Ohio General Assembly", "State Representative", [("Monica Robb Blasdel", "REP"), ("Bob Guy", "DEM")], detail="79th District", src=S)
    c.contest("appeals-7-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Molly K. Johnson", "REP")], detail="7th District · full term commencing February 9, 2027", src=S)
    c.contest("appeals-7-0210", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Mark Anthony Hanni", "REP"), ("Katherine Rudzik", "DEM")], detail="7th District · full term commencing February 10, 2027", src=S)

    # --- County offices ---
    c.contest("commissioner", "County offices", "County Commissioner", [("Ron Eick", "REP")], detail="Full term commencing January 1, 2027", src=S)
    c.contest("auditor", "County offices", "County Auditor", [("Staci L. Brady", "REP")], detail="Full term commencing March 8, 2027", src=S)
    # Write-in Vincent L. Slabaugh is certified but not printed on the ballot.
    c.contest("cp-probate-juvenile", "Court of Common Pleas", "Judge of the Court of Common Pleas, Probate and Juvenile Division", ["Maureen E. Stoneman", "Jennifer L. Thomas"],
              detail="Full term commencing February 9, 2027" + NP, src=S)

    # --- Local issues (unnumbered in the Board's documents; listed in the notice's order) ---
    c.levy("county-home", "Carroll County", "county", "Renewal", "Maintenance and operation of the County Home.",
           "1.4 mills", "5 years, commencing in 2027", "2028", est("$1,761,950", "$30"), area="Carroll County (all precincts)", src=S)
    # Brown A split 3 and Rose splits 1 and 2 (precincts 004/3, 021/1, 021/2).
    c.levy("sandy-valley-lsd", "Sandy Valley Local School District (Stark, Carroll and Tuscarawas)", SD("SANDY VALLEY LOCAL SD (STARK)"), "Renewal", "Current operating expenses.",
           "2.3 mills", "5 years, commencing in 2027", "2028", est("$750,000", "$81"),
           area="Sandy Valley Local School District, Carroll County part (Brown A split 3, Rose splits 1 and 2)", src=S)
    # Only Brown A split 2 (precinct 004/2) of Carroll County is in the library district; the Board gives no cost per $100,000.
    c.levy("stark-library", "Stark County District Library", P("BROWN TWP"), "Renewal and increase",
           "Current expenses (renewal of 2 mills and increase of 0.3 mill).", "2.3 mills", "8 years, commencing in 2027", "2028", "$14,949,218 a year",
           area="Stark County District Library, Carroll County part (Brown A split 2)", src=S)
    c.levy("carrollton-fire", "Village of Carrollton", P("CARROLLTON VILLAGE"), "Renewal", "Providing and maintaining fire personnel, buildings and equipment.",
           "1 mill", "5 years, commencing in 2026", "2027", est("$69,960", "$35"), area="Village of Carrollton (Carrollton A and B)", src=S)
    c.levy("dellroy-current", "Village of Dellroy", P("DELLROY VILLAGE"), "Renewal", "Current expenses.",
           "5 mills", None, "2027", est("$12,000", "$53"), area="Village of Dellroy (Monroe split 2)", src=S,
           note="The Board's documents say commencing in 2026, first due in 2027, and do not state the number of years; see your sample ballot.")
    c.levy("fox-twp-fire", "Fox Township", P("FOX TWP"), "Additional", "Providing and maintaining fire personnel, buildings and equipment.",
           "1.5 mills", "5 years, commencing in 2027", "2028", est("$73,900", "$53"), area="Fox Township (Fox splits 1–3)", src=S)
    # Fox split 3, Lee split 2 and Loudon split 2 (precincts 012/3, 015/2, 016/2) vote on Edison and both Jefferson County JVS renewals.
    c.levy("edison-lsd", "Edison Local School District (Jefferson, Carroll and Harrison)", SD("EDISON LOCAL SD (JEFFERSON)"), "Renewal (fixed sum)", "Current expenses ($1,049,150 a year).",
           "1.85 mills (estimated average)", "5 years, commencing in 2027", "2028", est("$1,049,150", "$65"),
           area="Edison Local School District, Carroll County part (Fox split 3, Lee split 2, Loudon split 2)", src=S)
    JVS = "Jefferson County Joint Vocational School District (Jefferson, Belmont, Carroll and Harrison)"
    JVS_AREA = "Jefferson County JVSD, Carroll County part (Fox split 3, Lee split 2, Loudon split 2)"
    # The JVS precincts are the same as Edison's, so its places come from the Edison district.
    JP = SD("EDISON LOCAL SD (JEFFERSON)")
    c.levy("jefferson-jvsd-1", JVS, JP, "Renewal",
           "0.67 mill for current expenses and 0.33 mill for reconditioning or acquiring tools, equipment or furnishings and for repairing, improving, renovating, expanding or reconstructing buildings and sites.",
           "1 mill", "10 years, commencing in 2027", "2028", est("$1,999,864", "$32"), area=JVS_AREA,
           note="One of two separate 1-mill JVS renewals on the ballot (listed by the Board as Jefferson County Joint Vocational School (1) and (2)).", src=S)
    c.levy("jefferson-jvsd-2", JVS, JP, "Renewal",
           "0.67 mill for current expenses and 0.33 mill for purchasing equipment for buildings and improving buildings.",
           "1 mill", "10 years, commencing in 2027", "2028", est("$1,934,109", "$30"), area=JVS_AREA,
           note="One of two separate 1-mill JVS renewals on the ballot (listed by the Board as Jefferson County Joint Vocational School (1) and (2)).", src=S)
    c.levy("magnolia-police", "Village of Magnolia (Stark and Carroll)", P("MAGNOLIA VILLAGE"), "Renewal", "Police.",
           "4 mills", "5 years, commencing in 2027", "2028", est("$30,969", "$28"), area="Village of Magnolia, Carroll County part (Rose split 2)", src=S,
           text="Providing and maintaining equipment and personnel for operation of the police department.")
    RT = "Rose Township (excluding the Village of Magnolia)"
    c.levy("rose-twp-roads", RT, P("ROSE TWP"), "Renewal", "General construction, reconstruction, resurfacing and repair of streets, roads and bridges.",
           "2.69 mills", "5 years, commencing in 2027", "2028", est("$75,840", "$94"), area="Rose Township outside Magnolia (Rose splits 1 and 3)", src=S)
    c.levy("rose-twp-fire", RT, P("ROSE TWP"), "Renewal", "Providing and maintaining fire personnel, buildings and equipment.",
           "1 mill", "5 years, commencing in 2027", "2028", est("$41,630", "$35"), area="Rose Township outside Magnolia (Rose splits 1 and 3)", src=S)
    return c
