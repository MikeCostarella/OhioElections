from lib import County, NOTE_ORDER, NOTE_PLACES

SITE = "https://www.boe.ohio.gov/marion/"
NOTICE = "https://www.boe.ohio.gov/marion/c/upload/FWAB_11November46Day.pdf"

TWPS = ["BIG ISLAND", "BOWLING GREEN", "CLARIDON", "GRAND PRAIRIE", "GRAND", "GREEN CAMP", "MARION", "MONTGOMERY", "PLEASANT",
        "PROSPECT", "RICHLAND", "SALT ROCK", "SCOTT", "TULLY", "WALDO"]


def build():
    # Raw township names end in "TWP." with a period, which display() would turn into "... Twp. Township".
    rename = {f"{t} TWP.": f"{t.title()} Township" for t in TWPS}
    rename["LARUE VILLAGE"] = "LaRue Village"  # the Board's spelling
    c = County("marion", "Marion", "39101", rename=rename)
    # The notice names precincts 001-045: 001-021 Marion 1-A to 6-F (city), 022 Big Island, 023 Bowling Green, 024-025 Claridon A-B,
    # 026 "Grand Salt" (Grand and Salt Rock townships, Morral), 027 Grand Prairie, 028 Green Camp, 029-034 Marion Township A-F,
    # 035 Montgomery (with LaRue and New Bloomington), 036-039 Pleasant A-D, 040 Prospect Village, 041 Prospect Township,
    # 042-043 Richland A-B, 044 "Scott Tully", 045 Waldo; "/n" after a number is a split of that precinct.
    c.src("marion-46day", "Marion County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election (revised September 14, 2026)", NOTICE)
    C = I = ["marion-46day"]
    c.links = [
        {"label": "Board of Elections", "url": SITE},
        {"label": "Election info", "url": "https://www.boe.ohio.gov/marion/election-info/"},
        {"label": "Sample ballots by precinct", "url": "https://lookup.boe.ohio.gov/vtrapp/marion/ballotlist.aspx"},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://www.boe.ohio.gov/marion/election-info/election-results/"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it. "
               "Issue wording is condensed from the notice; the full wording is on the sample ballot.",
               NOTE_ORDER, NOTE_PLACES,
               "The Board's notice does not give local issue numbers; see your sample ballot for them."]
    P = c.p; D = c.district; SD = c.sd

    # --- Federal, state legislative, appeals (no State Senate seat for Marion County on this ballot) ---
    c.contest("congress-4", "U.S. House", "Representative to Congress", [("Jim Jordan", "REP"), ("Joshua D. Kolasinski", "DEM"), ("Tracey L. Tackett", "Nonparty")],
              detail="4th District", places=D("cong", 4), src=C)
    c.contest("rep-86", "Ohio General Assembly", "State Representative", [("Kent Halloran", "DEM"), ("Ben Weber", "REP")], detail="86th District", places=D("rep", 86), src=C)
    c.contest("rep-87", "Ohio General Assembly", "State Representative", [("Lora Covrett", "DEM"), ("Jeffrey A. McClain", "REP"), ("Craig Swartz", "Nonparty")],
              detail="87th District", places=D("rep", 87), src=C)
    c.contest("appeals-3-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Mark C. Miller", "REP")], detail="3rd District · term commencing February 9, 2027", src=C)

    # --- County offices ---
    c.contest("commissioner", "County offices", "County Commissioner", [("Kenneth H. Stiverson", "REP")], detail="Term commencing January 1, 2027", src=C)
    c.contest("auditor", "County offices", "County Auditor", [("Joan Kasotis", "DEM")], detail="Term commencing March 8, 2027", src=C)
    c.contest("coroner", "County offices", "County Coroner", [("Timothy F. Garner", "REP")], detail="Unexpired term ending December 31, 2028", src=C)
    NP = " · no party label on the ballot"
    c.contest("cp-family", "Court of Common Pleas", "Judge of the Court of Common Pleas, Family Division", ["Rhonda Burggraf"],
              detail="Term commencing February 9, 2027" + NP, src=C)

    # --- Issues (unnumbered in the Board's notice; listed in the notice's order) ---
    c.levy("elgin-lsd", "Elgin Local School District (Marion, Delaware and Hardin counties)", SD("ELGIN LOCAL SD (MARION)"), "Renewal",
           "Current expenses.", "2.88 mills", "5 years, commencing in 2027", "2028",
           area="Elgin Local School District (Marion 3-C, Big Island, Bowling Green, Grand Salt, Green Camp, Marion Township D and F, Montgomery, Prospect)", src=I)
    # The notice puts Marion 1-B (split 3) and 2-B (split 2) in Ridgedale; the voter file has no Marion City voters there.
    c.levy("ridgedale-lsd", "Ridgedale Local School District (Marion, Crawford and Wyandot counties)", SD("RIDGEDALE LOCAL SD (MARION)") + P("MARION CITY"), "Renewal",
           "Current expenses.", "2.44 mills", "5 years, commencing in 2027", "2028",
           area="Ridgedale Local School District (Marion 1-B and 2-B splits, Big Island, Grand Salt, Grand Prairie, Marion Township F, Montgomery, Scott Tully)", src=I)
    c.levy("dacc-levy", "Delaware Area Career Center (joint vocational school district; Delaware, Franklin, Marion, Morrow and Union counties)", P("WALDO TWP."),
           "Renewal and decrease", "Improving, renovating, remodeling, enlarging, furnishing and equipping school buildings and facilities.",
           "0.75 mill", "10 years, commencing in 2026", "2027", area="Waldo Township (split 3)", src=I)
    c.levy("battle-run-fire", "Battle Run Joint Fire District", P("PROSPECT VILLAGE", "PROSPECT TWP."), "Additional",
           "Fire apparatus, appliances, buildings or sites, sources of water supply and materials, and payment of permanent, part-time or volunteer firefighters "
           "or firefighting companies, including employer contributions under R.C. 742.34.", "2 mills", "Continuing period of time, commencing in 2026", "2027",
           area="Prospect Village and Prospect Township", src=I)
    c.levy("adamh", "Marion County (ADAMH Board)", "county", "Renewal", "Operation of alcohol and drug addiction programs and mental health programs.",
           "1 mill", "5 years, commencing in 2026", "2027", src=I)
    c.levy("mcbdd", "Marion County (Board of Developmental Disabilities)", "county", "Renewal",
           "Programs and services of the Marion County Board of Developmental Disabilities, and acquiring, constructing, renovating, financing, maintaining and operating developmental disabilities facilities.",
           "3 mills", "5 years, commencing in 2026", "2027", src=I)
    c.issue("marion-council-terms", "question", "City of Marion", "Four-year staggered terms for City Council and Council President", P("MARION CITY"),
            area="Marion 1-A to 6-F",
            text="Shall the City of Marion change the terms of office for members of City Council and the President of Council from two-year terms to four-year terms, "
                 "with council seats elected in staggered elections so that a portion of Council is elected every two years?", src=I)
    c.levy("green-camp-current", "Village of Green Camp", P("GREEN CAMP VILLAGE"), "Renewal and increase",
           "Current operating and maintenance expenses (renewal of 9 mills and an increase of 2 mills).", "11 mills", "5 years, commencing in 2027", "2028",
           area="Green Camp Village (Green Camp Township precinct, split 1)", src=I)
    c.levy("prospect-current", "Village of Prospect", P("PROSPECT VILLAGE"), "Renewal", "Current expenses.", "3.1 mills", "5 years, commencing in 2027", "2028",
           area="Prospect Village", src=I)
    c.levy("pleasant-fire-ems", "Pleasant Township", P("PLEASANT TWP."), "Additional",
           "Payment of permanent firefighting, emergency medical service, administrative or communications personnel, including employer contributions under R.C. 145.48 or 742.34, "
           "and ambulance, paramedic or other emergency medical services operated by a fire department (R.C. 5705.19(I)).",
           "4 mills", "5 years, commencing in 2026", "2027", area="Pleasant Township A–D", src=I)
    c.levy("prospect-twp-current", "Prospect Township", P("PROSPECT TWP.", "PROSPECT VILLAGE"), "Renewal", "Current expenses.", "1 mill", "5 years, commencing in 2026", "2027",
           area="Prospect Township, including the Village of Prospect", src=I)
    # Grand Salt splits 4 and 5 are the Salt Rock Township part of the combined precinct (Salt Rock Township and Morral, all in Ridgedale LSD).
    c.levy("salt-rock-fire", "Salt Rock Township", P("SALT ROCK TWP.", "MORRAL VILLAGE"), "Renewal",
           "Providing and maintaining fire apparatus, appliances, buildings or sites (R.C. 5705.19(A)).", "2 mills", "5 years, commencing in 2027", "2028",
           area="Grand Salt precinct, splits 4 and 5 (Salt Rock Township, including the Village of Morral)", src=I)
    return c
