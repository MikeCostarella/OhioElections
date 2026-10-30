from lib import County, NOTE_ORDER, NOTE_PLACES

SITE = "https://boe.clermontcountyohio.gov/"
NOTICE_PAGE = "https://boe.clermontcountyohio.gov/news_detail_T9_R39.php"
NOTICE = "https://boe.clermontcountyohio.gov/FWAB%2046%20day%20-%20November%203,%202026%20General%20r5.pdf"
WITHDRAWAL = "https://boe.clermontcountyohio.gov/Candidate%20Withdrawal-Byrne-12th%20District%20Court%20of%20Appeals.pdf"


def build():
    # "UNION  TWP" (double space) already displays as "Union Township". "WASHINGTON TOWNSHIP A" is the part of
    # Washington Township precinct A in the Bethel-Tate school district (the notice: "Part of Washington Township A").
    c = County("clermont", "Clermont", "39025", rename={"WASHINGTON TOWNSHIP A": "Washington Township"})
    c.src("clermont-46day", "Clermont County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election (updated, posted September 15, 2026)", NOTICE)
    c.src("clermont-withdrawal", "Clermont County Board of Elections: notice to Ohio voters of candidate withdrawal (Matthew Byrne, 12th District Court of Appeals)", WITHDRAWAL)
    S = ["clermont-46day"]
    c.links = [
        {"label": "Board of Elections", "url": SITE},
        {"label": "46-day election notice (FWAB)", "url": NOTICE_PAGE},
        {"label": "Find your sample ballot", "url": "https://clermont-voterview.boe.ohio.gov/VoterView/RegistrantSearch.do"},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://boe.clermontcountyohio.gov/election_results/index.php"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it. "
               "Issue wording is the notice's summary; the full wording is on the sample ballot.",
               NOTE_ORDER, NOTE_PLACES,
               "The Board's notice does not give local issue numbers; see your sample ballot for them."]
    P = c.p; D = c.district; SD = c.sd

    # --- Federal, state legislative, appeals ---
    c.contest("congress-2", "U.S. House", "Representative to Congress", [("Jen Mazzuckelli", "DEM"), ("David J. Taylor", "REP")],
              detail="2nd District",
              places=D("cong", 2), src=S)
    c.contest("rep-62", "Ohio General Assembly", "State Representative", [("Ron Grethel", "LIB"), ("Jean Schmidt", "REP"), ("Ian Schwartz", "DEM")],
              detail="62nd District", places=D("rep", 62), src=S)
    c.contest("rep-63", "Ohio General Assembly", "State Representative", [("Adam C. Bird", "REP"), ("Debbie Davidson", "DEM")],
              detail="63rd District (Clermont and part of Brown)", places=D("rep", 63), src=S)
    c.contest("appeals-12-0101", "Ohio Court of Appeals", "Judge of the Court of Appeals",
              [("Matthew Byrne", "REP", "Withdrew September 16, 2026; his name may still appear on the ballot, but votes for him will not count"),
               ("Willa Concannon", "Write-in")],
              detail="12th District (Butler, Brown, Clermont, Clinton, Fayette, Madison, Preble and Warren counties) · full term commencing January 1, 2027",
              src=S + ["clermont-withdrawal"])
    c.contest("appeals-12-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Robert A. Hendrickson", "REP")],
              detail="12th District (Butler, Brown, Clermont, Clinton, Fayette, Madison, Preble and Warren counties) · full term commencing February 9, 2027", src=S)

    # --- County ---
    c.contest("commissioner", "County offices", "County Commissioner", [("Claire B. Corcoran", "REP"), ("Joe Wessels", "DEM")], detail="Full term commencing January 1, 2027", src=S)
    c.contest("auditor", "County offices", "County Auditor", [("John Becker", "REP")], detail="Full term commencing March 13, 2027", src=S)
    NP = " · no party label on the ballot"
    c.contest("cp-probate-juvenile", "Court of Common Pleas", "Judge of the Court of Common Pleas, Probate/Juvenile Division", ["Nathan M. Little"],
              detail="Full term commencing February 9, 2027" + NP, src=S)

    # --- Issues (unnumbered in the Board's notice; listed in the notice's order) ---
    c.levy("bethel-tate-current", "Bethel-Tate Local School District (Clermont and Brown)", SD("BETHEL-TATE LOCAL SD (CLERMONT)"), "Renewal",
           "Current operating expenses.", "5.48 mills", "5 years",
           area="Bethel Village A and B; Tate Township A and H; part of Franklin Township A and D, Tate Township B, D and F, and Washington Township A", src=S)

    # U.S. Grant Joint Vocational School District: not in the voter file's school-district columns; placed from the notice's precinct list.
    USG = P("BATAVIA TWP", "FELICITY VILLAGE", "FRANKLIN TWP", "JACKSON TWP", "MONROE TWP", "NEW RICHMOND VILLAGE", "OHIO TWP", "PIERCE TWP",
            "BETHEL VILLAGE", "TATE TWP", "WASHINGTON TWP", "WILLIAMSBURG VILLAGE", "WILLIAMSBURG TWP")
    USG_AREA = ("Felicity Village; Franklin Township A, B and D; Jackson Township B; Monroe Township B–E; New Richmond Village A and B; Ohio Township A and B; "
                "Pierce Township B, E and M; Bethel Village A and B; Tate Township A, D, F and H; Washington Township A–C; Williamsburg Village A and C; "
                "Williamsburg Township A and B; parts of Batavia Township C, Ohio Township C, Pierce Township A and D, Tate Township B and Williamsburg Township C")
    c.issue("us-grant-bond", "levy", "U.S. Grant Joint Vocational School District", "Bond issue: new construction, improvements and renovations to school facilities", USG,
            area=USG_AREA,
            text="Bond issue, estimated 1.15 mills, 37 years, for paying the costs of new construction, improvements, renovations and other additions to school facilities, "
                 "as well as equipment, furnishings, site development, safety and security measures, and all necessary appurtenances for the foregoing, "
                 "as well as land acquisition and capitalized interest.", src=S)
    c.levy("us-grant-pi", "U.S. Grant Joint Vocational School District", USG, "Additional",
           "Acquisition, construction, enlargement, renovation, and financing of permanent improvements.", "0.84 mill", "Continuing period of time", area=USG_AREA, src=S)

    c.levy("county-children", "Clermont County", "county", "Renewal", "Support of children services and the care and placement of children.", "0.8 mill", "5 years", src=S)

    FIRE = "Fire and emergency medical services: fire apparatus and equipment, buildings and sites, firefighting and EMS personnel, and ambulance, paramedic or other emergency medical service."
    c.levy("batavia-twp-fire", "Batavia Township", P("BATAVIA TWP", "BATAVIA VILLAGE"), "Additional", FIRE, "8.4 mills", "Continuing period of time",
           area="Batavia Township A–P and Batavia Village A", src=S)
    c.levy("union-twp-fire", "Union Township", P("UNION  TWP"), "Additional", FIRE, "1.99 mills", "Continuing period of time",
           area="Union Township A–R, T, U, W–Z, B1B, C1C, D1D, E1E, F1F, J1J, K1K, L1L, M1M, P1P, R1R, S1S, U1U and V1V", src=S)
    c.levy("washington-twp-fire", "Washington Township", P("WASHINGTON TWP", "WASHINGTON TOWNSHIP A"), "Additional", FIRE, "5.5 mills", "5 years",
           area="Washington Township A, B and C", src=S)

    c.issue("liquor-scramblers", "liquor", "Union Township", "Local liquor option: Scramblers (Sunday)", P("UNION  TWP"), area="Union Township precinct G",
            text="Sunday sales of wine and mixed beverages, and spirituous liquor, at a particular business location (by petition): Amy's F & B L.L.C. dba Scramblers.", src=S)
    return c
