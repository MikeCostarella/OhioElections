from lib import County, NOTE_ORDER, NOTE_PLACES

NOTICE = "https://www.waynecountyoh.gov/wp-content/uploads/2026/10/Form-120-46-Day-FWAB-Gen-26-10162026-0910.pdf"
SAMPLES = "https://www.waynecountyoh.gov/wp-content/uploads/2026/09/Sample-Ballots-ALL-WATERMARK-09192026-1352.pdf"


def build():
    # The voter file spells Fredericksburg (Salt Creek Township) as "FREDERICKTOWN VILLAGE"; the ballots say Fredericksburg.
    c = County("wayne", "Wayne", "39169", rename={"FREDERICKTOWN VILLAGE": "Fredericksburg Village"})
    c.src("wayne-46day", "Wayne County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election (revised 10/16/2026)", NOTICE)
    c.src("wayne-samples", "Wayne County Board of Elections: sample ballots for every precinct, November 3, 2026 General Election (9/19/2026)", SAMPLES)
    S = ["wayne-46day", "wayne-samples"]
    c.links = [
        {"label": "Board of Elections", "url": "https://www.waynecountyoh.gov/"},
        {"label": "Sample ballots", "url": "https://www.waynecountyoh.gov/sampleballots/"},
        {"label": "Sample ballots by precinct", "url": "https://lookup.boe.ohio.gov/vtrapp/wayne/ballotlist.aspx"},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://www.waynecountyoh.gov/election-results-past-election-results/"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it, "
               "checked against the Board's sample ballots. Issue wording is the Board's summary; the full wording is on the sample ballot.",
               NOTE_ORDER, NOTE_PLACES,
               "Wayne County's ballots do not number local issues (only State Issue 3 has a number); they are listed here in the Board's order."]
    P = c.p; D = c.district; SD = c.sd
    NP = " · no party label on the ballot"

    c.contest("congress-6", "U.S. House", "Representative to Congress", [("Elizabeth Kirtley", "DEM"), ("Michael A. Rulli", "REP")], detail="6th District", places=D("cong", 6), src=S)
    c.contest("congress-7", "U.S. House", "Representative to Congress", [("Brian Poindexter", "DEM"), ("Max Miller", "REP")], detail="7th District", places=D("cong", 7), src=S)
    c.contest("senate-31", "Ohio General Assembly", "State Senator", [("Laura Sirot", "DEM"), ("Al Landis", "REP")], detail="31st District", places=D("sen", 31), src=S)
    c.contest("rep-77", "Ohio General Assembly", "State Representative", [("Brooke Dillon", "DEM"), ("Meredith Craig", "REP")], detail="77th District", places=D("rep", 77), src=S)
    c.contest("appeals-9-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Betty Sutton", "DEM"), ("Cynthia Curtin", "REP")], detail="9th District · full term commencing February 9, 2027", src=S)
    c.contest("appeals-9-0210", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Tavia Galonski", "DEM"), ("Nathan Manning", "REP")], detail="9th District · unexpired term ending February 9, 2029", src=S)
    c.contest("commissioner", "County offices", "County Commissioner", [("Jonathan Hofstetter", "REP")], detail="Full term commencing January 1, 2027", src=S)
    c.contest("auditor", "County offices", "County Auditor", [("Russell Robertson", "REP")], detail="Full term commencing March 8, 2027", src=S)
    c.contest("cp-probate-juvenile", "Court of Common Pleas", "Judge of the Court of Common Pleas, Probate and Juvenile Division", ["Latecia Eileen Wiles"],
              detail="Full term commencing February 9, 2027" + NP, src=S)

    est = lambda total, per: f"{total} a year; {per} for each $100,000 of market value"

    # --- School districts ---
    c.issue("chippewa-lsd-income", "question", "Chippewa Local School District", "School district income tax: 1% renewal, 5 years, for current operating expenses", SD("CHIPPEWA LOCAL SD (WAYNE)"),
            area="Chippewa Local School District (precincts 10/2, 53/1, 54/1, 55/1, 55/2, 56/1, 57/1, 58/1, 80/4)",
            text="Shall an annual income tax of 1.00% on the earned income of individuals residing in the school district be imposed by the Chippewa Local School District to renew an income tax expiring at the end of 2027, for 5 years, beginning January 1, 2028, for the purpose of providing for the current operating expenses of the school district?", src=S)
    c.levy("dalton-lsd-pi", "Dalton Local School District", SD("DALTON LOCAL SD (WAYNE)"), "Renewal", "General, on-going permanent improvements.", "2 mills", "5 years, commencing in 2027", "2028", est("$244,127", "$28"),
           area="Dalton Local School District (precincts 43/2, 87/1, 87/3, 88/1, 88/3, 89/1)", src=S)
    c.levy("northwestern-lsd-current", "Northwestern Local School District (Wayne and Ashland)", SD("NORTHWESTERN LOCAL SD (WAYNE)"), "Renewal (fixed sum)", "Current operating expenses ($456,400 a year).", "1.8 mills (estimated average)", "5 years, commencing in 2026", "2027", "$456,400 a year; $63 for each $100,000 of market value",
           area="Northwestern Local School District (precincts 50/1, 51/1, 65/1, 66/1, 67/1, 67/2, 84/3, 85/3)", src=S)
    c.issue("orrville-csd-income", "question", "Orrville City School District", "School district income tax: 1% additional, 5 years, for current expenses", SD("ORRVILLE CITY SD"),
            area="Orrville City School District (precincts 1/1, 1/2, 2/1, 3/1, 5/1, 6/1, 43/1, 44/1, 68/2, 75/2, 88/2)",
            text="Shall an annual income tax of 1.00% on the earned income of individuals residing in the school district be imposed by the Orrville City School District, for 5 years, beginning January 1, 2027, for the purpose of current expenses?", src=S)
    c.issue("triway-lsd-income", "question", "Triway Local School District (Wayne and Holmes)", "School district income tax: 0.75% additional, 3 years, for current expenses", SD("TRIWAY LOCAL SD (WAYNE)"),
            area="Triway Local School District (precincts 15/2, 15/3, 15/5, 62/1, 63/1, 73/1, 74/1, 84/1, 85/1, 92/3, 97/1, 98/1, 99/1)",
            text="Shall an annual income tax of 0.75% on the earned income of individuals residing in the school district be imposed by the Triway Local School District, for 3 years, beginning January 1, 2027, for the purpose of current expenses?", src=S)
    # Every Wayne place has precincts in the JVSD; only seven precinct splits served by other counties' school districts are left out.
    c.levy("wayne-jvsd", "Wayne County Joint Vocational School District (Wayne, Ashland, Holmes, Medina and Stark)", list(c.places), "Renewal", "General permanent improvements.", "0.5 mill", "5 years, commencing in 2027", "2028", est("$1,480,860", "$11"),
           area="All precincts except 43/3, 44/4, 44/5, 53/3, 62/2, 83/3 and 84/2 (parts of Baughman, Chippewa, Clinton, Paint and Plain townships)", src=S)

    # --- City of Norton (Summit and Wayne): same five charter amendments as on Summit's ballot (Summit issues 29-33) ---
    NO = P("NORTON CITY")
    for i, (sec, text) in enumerate([
        ("Article II, Section 2.09 (Mayor's salary)", "Change the Mayor's salary rate in the Charter from $11,250 to $15,000, unless otherwise approved by the voters for the next term of office."),
        ("Article III, Section 3.08 (Council salaries)", "Change Council members' salary rate from $7,500 to $10,000 and the President of Council's from $8,500 to $11,000, unless otherwise approved by the voters for the next term of office."),
        ("Article IV, Section 4.03 (Administrative Officer supervision of Finance and Law)", "Place the Department of Finance and Department of Law under the direct administrative supervision of the Administrative Officer, while preserving the existing appointment and removal provisions and the legally vested fiscal and professional legal duties of those offices."),
        ("Article V, Section 5.03.B (Board of Control contract approval)", "Raise the contract amount requiring Board of Control approval from five thousand dollars to ten thousand dollars."),
        ("Title of the chief legal officer", "Change the title of the City's chief legal officer from Solicitor to Director of Law, without changing the appointment, qualifications, powers, duties, suspension or removal provisions applicable to that office."),
    ], 1):
        c.issue(f"norton-charter-{i}", "question", "City of Norton (Summit and Wayne)", f"Charter amendment: {sec}", NO, area="Norton City precinct 55/2 (Chippewa 3)", text=text, src=S)

    # --- City of Rittman (Wayne and Medina): same 15 charter amendments as in medina.py ---
    RIT = [
        ("Section 9.05", "Eliminate outdated language regarding the civil service status of employees and add a new section allowing for the removal of a member of City Council by other members of City Council for bad behavior, criminal conduct, or absenteeism."),
        ("Articles III, IV, VII, XII and XIII", "Change the date of the organizational meeting, change the date that elected officials take office, and change the deadline that nominating petitions for elective offices in the municipality must be submitted to the Board of Elections."),
        ("Section 3.06", "Allow City Council to hold executive sessions for any reason allowable by Ohio Revised Code."),
        ("Section 4.03", "Clarify language that the Mayor, when invited, is only an attendee and does not preside over executive sessions of City Council."),
        ("Section 4.05", "Clarify the procedure by which a member of City Council is nominated to and can become Mayor in the event the office of Mayor becomes vacant."),
        ("Section 5.01", "Require an annual review of the Municipal Manager by City Council."),
        ("Articles VI and IX", "Change language to reflect that the Fire and EMS departments have merged into one department."),
        ("Section 6.05", "Require that the Law Director be an attorney-at-law in good standing with the state bar association and oversee representation of the City in all cases as well as provide direct representation."),
        ("Section 9.01", "Update old language concerning the establishment of a Civil Service Commission if Rittman became a city, as Rittman is already a city."),
        ("Section 9.02", "Change the term an individual serves on the Civil Service Commission from six (6) years to three (3) years."),
        ("Section 11.01", "Add a member of City Council to serve on the Cemetery Board."),
        ("Section 12.02", "Change the deadline for submitting the budget to City Council from January 1st to December 31st and clarify language."),
        ("Section 12.06", "Require an annual review of the Finance Director by City Council."),
        ("Section 13.04", "Reduce the residency requirement to be eligible to be an elected officer of the municipality from two (2) years to one (1) year."),
        ("Section 16.01", "Amend the schedule in which the Charter Review Commission convenes to intentionally misalign it with the election of new members of City Council."),
    ]
    for i, (sec, text) in enumerate(RIT, 1):
        c.issue(f"rittman-charter-{i}", "question", "City of Rittman (Wayne and Medina counties)", f"Proposed charter amendment #{i}: {sec}", P("RITTMAN CITY"),
                area="Rittman City precincts 10/1, 10/2, 11/1, 12/1, 12/2, 13/1", text=text, src=S)

    # --- Villages ---
    BU = P("BURBANK VILLAGE")
    for i, (mills, total, per) in enumerate([("3 mills", "$9,156", "$42"), ("3 mills", "$9,156", "$42"), ("4 mills", "$12,951", "$63")], 1):
        c.levy(f"burbank-current-{i}", "Village of Burbank", BU, "Renewal", "Current expenses.", mills, "5 years, commencing in 2027", "2028", est(total, per), area="Burbank Village (precinct 45/2)",
               note="The ballot carries two separate 3-mill renewals with identical wording." if mills == "3 mills" else None, src=S)
    DT = P("DOYLESTOWN VILLAGE")
    c.issue("doylestown-advisory-rentals", "question", "Village of Doylestown", "Advisory question: zoning to permit and regulate short-term rental properties", DT, area="Doylestown Village (precincts 56/1, 57/1)",
            text="Should the Village Council consider adopting zoning regulations to permit and regulate short-term rental properties within the BD Downtown Business District and BG General Business District?", src=S)
    c.issue("doylestown-advisory-dispensaries", "question", "Village of Doylestown", "Advisory question: zoning to permit adult-use marijuana dispensaries", DT, area="Doylestown Village (precincts 56/1, 57/1)",
            text="Should the Village Council consider adopting zoning regulations to permit adult-use marijuana dispensaries within the BD Downtown Business District and BG General Business District?", src=S)
    c.issue("smithville-ordinance", "question", "Village of Smithville", "Initiative ordinance: repeal photo traffic enforcement (Ordinance 2025-4)", P("SMITHVILLE VILLAGE"), area="Smithville Village (precinct 77/1)",
            text="An ordinance proposed by initiative petition repealing Ordinance 2025-4, \"An ordinance providing for photo traffic enforcement within the Village of Smithville,\" enacted by the Village Council on March 18, 2025. Shall the proposed ordinance to repeal Ordinance 2025-4 be adopted?", src=S)

    # --- Doylestown / Chippewa Township merger: each votes on a merger commission and elects five commissioners ---
    MQ = "Shall a commission be chosen to draw up a statement of conditions for merger of the political subdivisions of the Village of Doylestown and Chippewa Township?"
    c.issue("doylestown-merger", "question", "Village of Doylestown", "Merger commission: merger with Chippewa Township", DT, area="Doylestown Village (precincts 56/1, 57/1)", text=MQ, src=S)
    c.contest("doylestown-merger-commission", "Municipal offices", "Member of Merger Commission (Village of Doylestown)", ["Misty Hray", "Madeline Rock", "Tony Lindeman", "Marie Lepley", "Dean Porr"],
              detail="Vote for not more than 5 · for the commission voted on in the merger question" + NP, places=DT, area="Doylestown Village (precincts 56/1, 57/1)", src=S)
    # The notice also puts precinct 55/2 (Norton City's Wayne County voters) in the Chippewa Township question.
    CH = P("CHIPPEWA TOWNSHIP", "NORTON CITY")
    CHA = "Chippewa Township (precincts 53/1, 53/2, 53/3, 54/1, 54/2, 55/1, 55/2, 58/1)"
    c.issue("chippewa-merger", "question", "Chippewa Township", "Merger commission: merger with the Village of Doylestown", CH, area=CHA, text=MQ, src=S)
    c.contest("chippewa-merger-commission", "Township offices", "Member of Merger Commission (Chippewa Township)", ["Lesa Miller", "Jeanien Frantz", "Mark Tetzel", "Megan Busson", "Nick Kukta"],
              detail="Vote for not more than 5 · for the commission voted on in the merger question" + NP, places=CH, area=CHA, src=S)

    # --- Townships ---
    c.levy("canaan-fire", "Canaan Township (Wayne and Medina counties)", P("CANAAN TOWNSHIP", "BURBANK VILLAGE", "CRESTON VILLAGE"), "Additional", "Fire and emergency medical services.", "2.5 mills", "3 years, commencing in 2026", "2027", est("$395,115", "$88"),
           area="Canaan Township precincts 45/1, 45/2, 46/1, 47/1, 47/2 (including Burbank and Creston)", src=S)
    c.levy("chester-roads", "Chester Township", P("CHESTER TOWNSHIP"), "Renewal", "General construction, reconstruction, resurfacing, and repair of streets, roads, and bridges.", "1.9 mills", "5 years, commencing in 2026", "2027", est("$70,956", "$20"),
           area="Chester Township (precincts 50/1, 50/2, 51/1)", src=S)
    c.levy("clinton-fire", "Clinton Township", P("CLINTON TOWNSHIP", "SHREVE VILLAGE"), "Renewal", "Fire and ambulance protection.", "1.5 mills", "4 years, commencing in 2027", "2028", est("$98,495", "$30"),
           area="Clinton Township precincts 62/1, 62/2, 63/1 (including Shreve)", src=S)
    # Precincts 15/3 and 33/2 are Wooster City splits in Wooster Township (ballot labels "Woo 1A ... Wst Twp", "Woo 4B Woo-Wst Twp").
    c.levy("wooster-twp-fire-building", "Wooster Township", P("WOOSTER TOWNSHIP", "WOOSTER CITY"), "Additional", "Construction, improvement or maintenance of a building for firefighting and emergency medical services.", "1.5 mills", "5 years, commencing in 2026", "2027", est("$343,342", "$53"),
           area="Wooster Township precincts 97/1, 97/2, 97/3, 98/1, 99/1, 99/2, 99/3, plus Wooster City splits 15/3 and 33/2", src=S)

    # --- Local liquor options ---
    c.issue("liquor-gigis-diner", "liquor", "Baughman Township", "Local liquor option: GiGi's Diner (Sunday)", P("BAUGHMAN TWP", "MARSHALLVILLE VILLAGE"), area="Baughman Township precinct 2 (44/1–44/5, including Marshallville)",
            text="Sunday sale of beer, wine and mixed beverages, and spirituous liquor by GiGi's Diner LLC (D-6 permit applicant), a diner at 1 North Main Street, Marshallville.", src=S)
    c.issue("liquor-lincoln-way-vineyards", "liquor", "Plain Township", "Local liquor option: Lincoln Way Vineyards (Sunday)", P("PLAIN TOWNSHIP"), area="Plain Township precinct 1 (84/1–84/3)",
            text="Sunday sale of beer, wine and mixed beverages by Lincoln Way Vineyards, Inc. (D-6 permit applicant; A-1C and A-2 permit holder), a winery and brewery at 9050 W. Old Lincoln Way, Wooster.", src=S)
    SC = P("SALT CREEK TOWNSHIP", "FREDERICKTOWN VILLAGE")
    c.issue("liquor-legion-651", "liquor", "Salt Creek Township", "Local liquor option: Fredericksburg American Legion Post 651", SC, area="Salt Creek Township precinct 1 (86/1, 86/2, including Fredericksburg)",
            text="Sale of beer, wine and mixed beverages, and spirituous liquor by Fredericksburg American Legion Post 651 (D-4 permit applicant), 6353 Harrison Rd., Fredericksburg.", src=S)
    c.issue("liquor-legion-651-sunday", "liquor", "Salt Creek Township", "Local liquor option: Fredericksburg American Legion Post 651 (Sunday)", SC, area="Salt Creek Township precinct 1 (86/1, 86/2, including Fredericksburg)",
            text="Sunday sale of beer, wine and mixed beverages, and spirituous liquor by Fredericksburg American Legion Post 651 (D-6 and D-4 permit applicant), 6353 Harrison Rd., Fredericksburg.", src=S)
    return c
