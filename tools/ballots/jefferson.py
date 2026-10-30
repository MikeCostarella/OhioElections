from lib import County, NOTE_ORDER, NOTE_PLACES

NOTICE = "https://www.boe.ohio.gov/jefferson/c/upload/FWAB_11November46Day.pdf"
CAND = "https://www.boe.ohio.gov/jefferson/c/upload/ELECTION_Candidates.pdf"
ISSUES = "https://www.boe.ohio.gov/jefferson/c/upload/ELECTION_Issues.pdf"
BALLOTS = "https://lookup.boe.ohio.gov/vtrapp/jefferson/ballotlist.aspx"


def build():
    # The voter file abbreviates "MT PLEASANT TWP"; the Board's issue list and ballots spell it Mount Pleasant.
    c = County("jefferson", "Jefferson", "39081", rename={"MT PLEASANT TWP": "Mount Pleasant Township"})
    c.src("jefferson-46day", "Jefferson County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election", NOTICE)
    c.src("jefferson-cand", "Jefferson County Board of Elections: candidate list, November 3, 2026 General Election (10/15/2026)", CAND)
    c.src("jefferson-ballots", "Jefferson County Board of Elections: sample ballots for every precinct, November 3, 2026 General Election", BALLOTS)
    c.src("jefferson-issues", "Jefferson County Board of Elections: issue list report, November 3, 2026 General Election (8/5/2026)", ISSUES)
    C = ["jefferson-46day", "jefferson-cand", "jefferson-ballots"]; I = ["jefferson-46day", "jefferson-issues", "jefferson-ballots"]
    c.links = [
        {"label": "Board of Elections", "url": "https://www.boe.ohio.gov/jefferson/"},
        {"label": "Election info", "url": "https://www.boe.ohio.gov/jefferson/election-info/"},
        {"label": "Sample ballots by precinct", "url": BALLOTS},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://www.boe.ohio.gov/jefferson/election-info/election-results/"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it, "
               "checked against the Board's candidate list, issue list and precinct sample ballots. Levy figures are from the sample ballots; "
               "the full wording is on your sample ballot.",
               NOTE_ORDER, NOTE_PLACES]
    P = c.p; SD = c.sd
    NP = " · no party label on the ballot"
    N = lambda n: f"Issue {n}"
    est = lambda total, per: f"{total} a year; {per} for each $100,000 of market value"

    # One congressional (6th), state House (96th) and appeals (7th) district covers the whole county; the 30th Senate seat is not up.
    c.contest("congress-6", "U.S. House", "Representative to Congress", [("Elizabeth Kirtley", "DEM"), ("Michael A. Rulli", "REP")], detail="6th District", src=C)
    c.contest("rep-96", "Ohio General Assembly", "State Representative", [("Ron Ferguson", "REP"), ("Charrie L. Foglio", "DEM")], detail="96th District", src=C)
    c.contest("appeals-7-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Molly K. Johnson", "REP")], detail="7th District · full term commencing February 9, 2027", src=C)
    c.contest("appeals-7-0210", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Mark Anthony Hanni", "REP"), ("Katherine Rudzik", "DEM")], detail="7th District · full term commencing February 10, 2027", src=C)
    c.contest("commissioner", "County offices", "County Commissioner", [("Brent G. Nemeth", "DEM"), ("Eric Timmons", "REP")], detail="Full term commencing January 1, 2027", src=C)
    c.contest("auditor", "County offices", "County Auditor", [("E. J. Conn", "REP")], detail="Term commencing March 8, 2027", src=C)
    c.contest("cp-0101", "Court of Common Pleas", "Judge of the Court of Common Pleas", ["Michelle Garcia Miller"], detail="Full term commencing January 1, 2027" + NP, src=C)
    c.contest("cp-0209", "Court of Common Pleas", "Judge of the Court of Common Pleas", ["Michael C. Bednar"], detail="Full term commencing February 9, 2027" + NP, src=C)
    c.contest("cp-probate-juvenile", "Court of Common Pleas", "Judge of the Court of Common Pleas, Probate/Juvenile Division", ["Frank W. Noble, Jr."],
              detail="Full term commencing February 9, 2027" + NP, src=C)

    # --- School districts ---
    c.levy("issue-4", "Edison Local School District (Jefferson, Carroll and Harrison)", SD("EDISON LOCAL SD (JEFFERSON)"), "Renewal (fixed sum)", "Current expenses ($1,049,150 a year).",
           "1.85 mills (estimated average)", "5 years, commencing in 2027", "2028", est("$1,049,150", "$65"), number=N(4),
           area="Edison Local School District (Brush Creek, Island Creek, Mt. Tabor, Pleasant Hill 1–2, Two Ridge, Welsmar, Wintringer, Stratton, Grant, New Somerset, Ross, Richmond, Salem, Shelley, Saline, Amsterdam and Elk; some precincts in part)", src=I)
    JVS = "Jefferson County Joint Vocational School District (Jefferson, Belmont, Carroll and Harrison)"
    c.levy("issue-5", JVS, "county", "Renewal",
           "0.67 mill for current expenses and 0.33 mill for reconditioning or acquiring tools, equipment or furnishings and for repairing, improving, renovating, expanding or reconstructing buildings and sites.",
           "1 mill", "10 years, commencing in 2027", "2028", est("$1,999,864", "$32"), number=N(5),
           note="One of two separate 1-mill JVS renewals on the ballot (see Issue 6).", src=I)
    c.levy("issue-6", JVS, "county", "Renewal",
           "0.67 mill for current expenses and 0.33 mill for purchasing equipment for buildings and improving buildings.",
           "1 mill", "10 years, commencing in 2027", "2028", est("$1,934,109", "$30"), number=N(6),
           note="One of two separate 1-mill JVS renewals on the ballot (see Issue 5).", src=I)

    # --- Park district (Jefferson part: Tiltonsville, Yorkville and Glen Robbins precincts) ---
    # Tiltonsville precinct (both splits, so Rayland too) votes on it, as do Yorkville and Glen Robbins (Warren Township).
    c.levy("issue-7", "Warren Township Park District (Jefferson and Belmont)", P("WARREN TWP", "TILTONSVILLE VILLAGE", "YORKVILLE VILLAGE", "RAYLAND VILLAGE"), "Additional",
           "Parks and recreational purposes.", "1 mill", "5 years, commencing in 2026", "2027", est("$123,905", "$35"), number=N(7),
           area="Tiltonsville (including Rayland), Yorkville and Glen Robbins precincts; also part of Belmont County", src=I)

    # --- County ---
    c.levy("issue-8", "Jefferson County", "county", "Renewal",
           "Community programs and services of the county Board of Developmental Disabilities, and acquiring, building, renovating, financing, maintaining and operating developmental disabilities facilities.",
           "1.7 mills", "10 years, commencing in 2027", "2028", est("$2,141,041", "$19"), number=N(8), src=I)
    c.levy("issue-9", "Jefferson County", "county", "Renewal", "Operation of the county 9-1-1 system.",
           "1.5 mills", "5 years, commencing in 2027", "2028", est("$2,482,785", "$35"), number=N(9),
           note="The 46-day notice says commencing in 2028, first due in 2029; the Board's issue list and sample ballots say commencing in 2027, first due in 2028, which is shown here.", src=I)

    # --- Villages ---
    c.levy("issue-10", "Village of Amsterdam", P("AMSTERDAM VILLAGE"), "Renewal", "Recreation, operation and maintenance.", "3 mills", "5 years, commencing in 2027", "2028",
           est("$12,206", "$86"), number=N(10), src=I)
    c.levy("issue-11", "Village of Irondale", P("IRONDALE VILLAGE"), "Renewal", "Current expenses.", "4 mills", "5 years, commencing in 2027", "2028",
           est("$11,648", "$102"), number=N(11), area="Village of Irondale (Saline precinct, part)", src=I)
    MP = P("MOUNT PLEASANT VILLAGE")
    c.levy("issue-12", "Village of Mount Pleasant", MP, "Renewal", "Current expenses.", "8 mills", "5 years, commencing in 2026", "2027",
           est("$23,527", "$115"), number=N(12), area="Village of Mount Pleasant (Emerson precinct, part)", src=I)
    c.levy("issue-13", "Village of Mount Pleasant", MP, "Renewal", "Maintaining and operating the village's cemeteries.", "1 mill", "5 years, commencing in 2026", "2027",
           est("$4,902", "$26"), number=N(13), area="Village of Mount Pleasant (Emerson precinct, part)", src=I)
    c.levy("issue-14", "Village of Rayland", P("RAYLAND VILLAGE"), "Renewal", "Current police protection.", "4 mills", "5 years, commencing in 2026", "2027",
           est("$20,609", "$104"), number=N(14), area="Village of Rayland (Tiltonsville precinct, part)", src=I)
    c.levy("issue-15", "Village of Richmond", P("RICHMOND VILLAGE"), "Renewal", "Current expenses.", "2 mills", "5 years, commencing in 2027", "2028",
           est("$12,004", "$45"), number=N(15), src=I)
    c.levy("issue-16", "Village of Stratton", P("STRATTON VILLAGE"), "Renewal", "Police and fire expenses.", "5 mills", "5 years, commencing in 2027", "2028",
           est("$205,862", "$139"), number=N(16), src=I)

    # --- Liquor option ---
    # On the ballot only in Piney Fork precinct split 068-2. The voter file has no split numbers; the post is at 75 Hanna Ave., Adena,
    # so the split is taken to be the Adena Village part of the precinct (the rest is unincorporated Smithfield Township).
    c.issue("issue-17", "liquor", "Smithfield Township (Piney Fork precinct)", "Local liquor option: Adena American Legion Post 525 (Sunday)", P("ADENA VILLAGE"), number=N(17),
            area="Piney Fork precinct, split 068-2",
            text="Sunday sale of wine and mixed beverages and spirituous liquor by AL Post 525 Gilbert Koontz dba Adena American Legion Post 525 (D-6 permit applicant, on-premise sales), a veterans service organization at 75 Hanna Ave., Adena.", src=I)

    # --- Townships ---
    c.levy("issue-18", "Salem Township", P("SALEM TWP", "RICHMOND VILLAGE"), "Renewal", "Fire protection.", "1.5 mills", "5 years, commencing in 2027", "2028",
           est("$195,021", "$43"), number=N(18), area="Salem Township (Richmond, Salem and Shelley precincts)", src=I)
    c.levy("issue-19", "Mount Pleasant Township (unincorporated)", P("MT PLEASANT TWP"), "Additional", "Fire and emergency medical services.", "4 mills",
           "Continuing period of time, commencing in 2026", "2027", est("$275,811", "$140"), number=N(19),
           area="Mount Pleasant Township outside the villages of Dillonvale and Mount Pleasant (Emerson precinct, part)", src=I)
    # Saline precinct (both splits, so Irondale too) and the Saline Township part of Stratton (split 050-2) vote on both Saline Township levies.
    SAL = P("SALINE TWP", "IRONDALE VILLAGE", "STRATTON VILLAGE")
    c.levy("issue-20", "Saline Township", SAL, "Renewal", "Ambulance and emergency medical services.", "2.5 mills", "5 years, commencing in 2027", "2028",
           est("$163,497", "$38"), number=N(20), area="Saline Township (Saline precinct, including Irondale, and Stratton precinct, part)", src=I)
    c.levy("issue-21", "Saline Township", SAL, "Additional", "Current operating expenses of the Saline Township Police Department.", "3 mills", "5 years, commencing in 2026", "2027",
           est("$212,349", "$105"), number=N(21), area="Saline Township (Saline precinct, including Irondale, and Stratton precinct, part)", src=I)
    return c
