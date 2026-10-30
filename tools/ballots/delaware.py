from lib import County, NOTE_ORDER, NOTE_PLACES

NOTICE = "https://vote.delawarecountyohio.gov/wp-content/uploads/2026/10/46-DAY-NOV-2026-FWAB-PDF1.pdf"


def build():
    # Raw names "COLUMBUS CITY ", "DUBLIN CITY ", "WESTERVILLE CITY " (trailing space) and "... TWP" display correctly
    # without renames. The notice numbers precincts 001-180 in alphabetical order of precinct name (001 Ashley,
    # 015-021 Columbus City A-G, 035-069 Delaware City 1-A to 4-I, 118-140 Orange A-W, 161-166 Sunbury City A-F, ...);
    # "/n" after a number is a split of that precinct.
    c = County("delaware", "Delaware", "39041")
    c.src("delaware-46day", "Delaware County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election (revised October 2, 2026)", NOTICE)
    C = I = ["delaware-46day"]
    c.links = [
        {"label": "Board of Elections", "url": "https://vote.delawarecountyohio.gov/"},
        {"label": "Sample ballots by precinct", "url": "https://lookup.boe.ohio.gov/vtrapp/delaware/ballotlist.aspx"},
        {"label": "Who are my elected officials?", "url": "https://lookup.boe.ohio.gov/vtrapp/delaware/cnm.aspx"},
    ]
    c.results_links = [{"label": "Board of Elections", "url": "https://vote.delawarecountyohio.gov/"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it. "
               "Issue wording is condensed from the notice; the full wording is on the sample ballot.",
               NOTE_ORDER, NOTE_PLACES,
               "The Board's notice does not give local issue numbers; see your sample ballot for them."]
    P = c.p; D = c.district; SD = c.sd

    # --- Federal, state legislative, appeals ---
    c.contest("congress-4", "U.S. House", "Representative to Congress", [("Jim Jordan", "REP"), ("Joshua D. Kolasinski", "DEM"), ("Tracey L. Tackett", "Nonparty")],
              detail="4th District", places=D("cong", 4), src=C)
    c.contest("congress-12", "U.S. House", "Representative to Congress", [("Troy Balderson", "REP"), ("Jerrad Christian", "DEM")], detail="12th District", places=D("cong", 12), src=C)
    c.contest("senate-19", "Ohio General Assembly", "State Senator", [("Scott Charland", "DEM"), ("Ryan Rivers", "REP")], detail="19th District", src=C)
    c.contest("rep-60", "Ohio General Assembly", "State Representative", [("Shelby Kimball", "DEM"), ("Brian Lorenz", "REP")], detail="60th District", places=D("rep", 60), src=C)
    c.contest("rep-61", "Ohio General Assembly", "State Representative", [("Vince McGrail", "DEM"), ("Shawn Stevens", "REP")], detail="61st District", places=D("rep", 61), src=C)
    c.contest("appeals-5", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Matthew George", "REP")], detail="5th District · term commencing February 9, 2027", src=C)

    # --- County offices ---
    c.contest("commissioner", "County offices", "County Commissioner", [("Ryan Grissinger", "DEM"), ("Renee Vaughan", "REP")], detail="Term commencing January 1, 2027", src=C)
    c.contest("auditor", "County offices", "County Auditor", [("George Kaitsa", "REP")], detail="Term commencing March 8, 2027", src=C)
    NP = " · no party label on the ballot"
    for id, office, date, cs in [
        ("cp-gen-0209", "General Division", "Term commencing February 9, 2027", ["Marianne T. Hemmeter"]),
        ("cp-gen-unexpired", "General Division", "Unexpired term ending December 31, 2030", ["Nickolas K. McCoy", "Emma Mirles-Jones"]),
        ("cp-probate-juvenile", "Probate/Juvenile Division", "Term commencing February 9, 2027", ["David Hejmanowski"]),
    ]:
        c.contest(id, "Court of Common Pleas", f"Judge of the Court of Common Pleas, {office}", cs, detail=date + NP, src=C)

    # --- Issues (unnumbered in the Board's notice; listed in the notice's order) ---
    est = lambda per: f"{per} for each $100,000 of market value"
    c.levy("delaware-dd", "Delaware County Board of Developmental Disabilities", "county", "Additional", "Community developmental disabilities programs and services.",
           "1.8 mills", "5 years, commencing in 2026", "2027", f"$25,448,490 a year; {est('$63')}", src=I)
    c.levy("delaware-morrow-mhrs", "Delaware-Morrow Mental Health & Recovery Services Board (Delaware and Morrow counties)", "county", "Renewal and increase",
           "Current expenses (renewal of 1.5 mills and an increase of 0.5 mill).", "2 mills", "5 years, commencing in 2027", "2028", f"$23,005,505 a year; {est('$50')}", src=I)

    COL = P("COLUMBUS CITY ")
    c.issue("columbus-charter-petition", "question", "City of Columbus (Delaware, Fairfield and Franklin counties)",
            "Charter amendment (by petition): council members elected only by voters in their district", COL, area="Columbus City A–G",
            text="This proposed charter amendment would limit the ability to vote for candidates for Columbus City Council to only those electors living within the districts that those "
                 "candidates seek to represent. Ballots within council districts would include both citywide races and the district race, and a recall election of a district council "
                 "member could be started by a petition signed by district electors equal to at least 15% of the votes cast in the district in the preceding mayoral election. "
                 "Shall the proposed charter amendment be approved?", src=I)
    c.issue("columbus-charter-council", "question", "City of Columbus (Delaware, Fairfield and Franklin counties)",
            "Charter amendment (by Council): district-only voting for district seats, at-large seats added, 13-member Council", COL, area="Columbus City A–G",
            text="This proposed charter amendment would limit the ability to vote for candidates for Columbus City Council to only those electors living within the districts that those "
                 "candidates seek to represent. It adds two at-large council members elected in 2027 and two more elected in 2029 (four-year terms), moving from a nine-member to an "
                 "eleven- and then a thirteen-member Council; redraws the council district map in 2027 and raises the allowed population variance between districts from 1% to 7.5%; "
                 "requires district candidates to have lived in their district for a year before the primary; updates expulsion, quorum and vote requirements; sets petition signature "
                 "requirements (150 district / 250 at-large); and allows recall of district and at-large members by petition. Shall the proposed charter amendment be approved?", src=I)
    c.issue("sunbury-data-center", "question", "City of Sunbury", "Charter amendment: new Section 11.05 prohibiting construction of a data center", P("SUNBURY CITY"),
            area="Sunbury City A–F",
            text="Shall Article XI, Section 11.05 of the Charter of the City of Sunbury be adopted? It would prohibit the construction of a data center, defined as one or more buildings, "
                 "facilities or infrastructure on a single parcel or on contiguous, adjacent or otherwise aggregated parcels used primarily or exclusively for digital information services "
                 "(managing, storing, processing and disseminating electronic data with computer systems, servers, networking and related equipment, including cooling) with an aggregate "
                 "monthly demand or peak load greater than 25 megawatts from any energy source. The section is self-executing.", src=I)
    c.levy("galena-current", "Village of Galena", P("GALENA VILLAGE"), "Additional", "Current expenses.", "2 mills", "4 years, commencing in 2026", "2027",
           f"$192,942 a year; {est('$70')}", area="Galena", src=I)
    # Berlin Township's fire levy also covers precincts in Delaware City (3-A splits 2-3, 3-F, 3-I split 3) and Sunbury City A split 4.
    c.levy("berlin-fire", "Berlin Township", P("BERLIN TWP", "DELAWARE CITY", "SUNBURY CITY"), "Renewal",
           "Fire protection, firefighting and emergency medical services: fire apparatus and equipment, buildings and sites, water supply, fire-alarm communications, "
           "firefighting and EMS personnel, ambulance equipment and services.", "2.95 mills", "5 years, commencing in 2027", "2028", f"$1,409,427 a year; {est('$103')}",
           area="Berlin Township A–G, Delaware City 3-A (splits 2–3), 3-F and 3-I (split 3), Sunbury City A (split 4)", src=I)
    c.levy("concord-roads", "Concord Township", P("CONCORD TWP", "POWELL CITY", "SHAWNEE HILLS VILLAGE"), "Renewal",
           "General construction, reconstruction, resurfacing and repair of roads and bridges.", "1 mill", "5 years, commencing in 2027", "2028", f"$325,427 a year; {est('$11')}",
           area="Concord Township A–K, Powell City J (split 2), Shawnee Hills (split 2)", src=I)
    c.levy("harlem-fire", "Harlem Township", P("HARLEM TWP"), "Renewal",
           "Fire protection, firefighting and emergency medical services: fire apparatus and buildings, water supply, fire alarm telegraph, firefighters, ambulance equipment and services.",
           "4 mills", "4 years, commencing in 2026", "2027", f"$956,658 a year; {est('$97')}", area="Harlem Township A–D", src=I)
    ORA = P("ORANGE TWP", "COLUMBUS CITY ", "WESTERVILLE CITY ")
    ORA_AREA = "Orange Township A–W, the Orange Township parts of Columbus City A–G, Westerville City A (split 3) and I (split 3)"
    c.levy("orange-roads", "Orange Township", ORA, "Additional", "General construction, reconstruction, resurfacing and repair of streets, roads and bridges.",
           "1 mill", "5 years, commencing in 2027", "2028", f"$2,279,352 a year; {est('$35')}", area=ORA_AREA, src=I)
    c.levy("orange-parks", "Orange Township", ORA, "Renewal", "Parks and recreational purposes.",
           "1 mill", "5 years, commencing in 2027", "2028", f"$1,372,814 a year; {est('$20')}", area=ORA_AREA, src=I)
    c.levy("oxford-roads", "Oxford Township", P("OXFORD TWP"), "Renewal", "General construction, reconstruction, resurfacing and repair of roads and bridges.",
           "1.2 mills", "5 years, commencing in 2026", "2027", f"$44,807 a year; {est('$30')}", area="Oxford Township", src=I)
    c.levy("elgin-lsd", "Elgin Local School District (Marion, Delaware and Hardin counties)", SD("ELGIN LOCAL SD (MARION)"), "Renewal",
           "Current expenses (fixed-sum levy of $850,000 a year).", "2.88 mills (estimated average)", "5 years, commencing in 2027", "2028", f"$850,000 a year; {est('$101')}",
           area="Thompson Township (split 2)", src=I)
    # DACC: every precinct except Dublin City A-D, Shawnee Hills, and splits of Concord, Genoa, Harlem, Porter, Scioto, Thompson and Westerville.
    DACC = P("ASHLEY VILLAGE", "BERKSHIRE TWP", "BERLIN TWP", "BROWN TWP", "COLUMBUS CITY ", "CONCORD TWP", "DELAWARE TWP", "DELAWARE CITY",
             "GALENA VILLAGE", "GENOA TWP", "HARLEM TWP", "KINGSTON TWP", "LIBERTY TWP", "MARLBORO TWP", "ORANGE TWP", "OSTRANDER VILLAGE", "OXFORD TWP",
             "PORTER TWP", "POWELL CITY", "RADNOR TWP", "SCIOTO TWP", "SUNBURY CITY", "THOMPSON TWP", "TRENTON TWP", "TROY TWP", "WESTERVILLE CITY ")
    c.levy("dacc-levy", "Delaware Area Career Center (joint vocational school district; Delaware, Franklin, Marion, Morrow and Union counties)", DACC, "Renewal and decrease",
           "Improving, renovating, remodeling, enlarging, furnishing and equipping school buildings and facilities (0.40 mill) and current expenses (0.35 mill); renewal of part of an existing levy, a reduction of 0.95 mill.",
           "0.75 mill", "10 years, commencing in 2026", "2027", f"$5,773,576 a year; {est('$18')}",
           area="Most of the county; not Dublin City, Shawnee Hills, or parts of Concord, Genoa, Harlem, Porter, Scioto and Thompson townships and Westerville City", src=I)
    c.levy("bstg-fire", "B.S.T. & G. Joint Fire District (Berkshire, Sunbury, Trenton and Galena)", P("BERKSHIRE TWP", "GALENA VILLAGE", "SUNBURY CITY", "TRENTON TWP"),
           "Renewal and increase", "Fire protection: fire apparatus, appliances, buildings, water supply, fire alarm telegraph and firefighters (renewal of 4.85 mills and an increase of 2.5 mills).",
           "7.35 mills", "5 years, commencing in 2026", "2027", f"$6,071,628 a year; {est('$176')}", area="Berkshire A–E, Galena, Sunbury City A–F, Trenton A–B", src=I)
    c.issue("transit-sales-tax", "question", "Delaware County Regional Transit Authority", "Sales and use tax: 0.2%, continuing, for transit",
            sorted(set(c.places) - set(COL)), area="All of Delaware County except the City of Columbus",
            text="Shall a sales and use tax be levied by the Delaware County Regional Transit Authority for the purpose of providing additional general revenues for a transit authority, "
                 "funding a regional transportation improvement project under section 5595.06 of the Revised Code, or funding public infrastructure projects as described in section "
                 "306.353 of the Revised Code, and to pay the expenses of administering such levy at a rate not exceeding 0.2 per cent for a continuing period of time?", src=I)

    # --- Local liquor options ---
    for id, jur, raw, prec, title, text in [
        ("liquor-born-on-third", "City of Columbus", "COLUMBUS CITY ", "Columbus City E (precinct 019)", "Local liquor option: Born on Third (Sunday)",
         "Sunday sale of beer and wine and mixed beverages by Born on Third Limited Partnership, applicant for a D-6 permit, restaurant at 40 Lazelle Rd, Columbus."),
        ("liquor-yokai-ramen", "City of Delaware", "DELAWARE CITY", "Delaware City 4-B (precinct 062)", "Local liquor option: Yokai Ramen Bistro (Sunday)",
         "Sunday sale of wine and mixed beverages, and spirituous liquor by Tony's Italian Bistro, L.L.C., dba Yokai Ramen Bistro, applicant for a D-6 permit, restaurant at 48 N. Sandusky Street, Delaware."),
        ("liquor-hacienda-taqueria", "City of Delaware", "DELAWARE CITY", "Delaware City 4-B (precinct 062)", "Local liquor option: Hacienda Taqueria & Bar (Sunday)",
         "Sunday sale of wine and mixed beverages, and spirituous liquor by Hot Spot Delaware, L.L.C., dba Hacienda Taqueria & Bar, applicant for a D-6 permit, restaurant/bar at 26 N. Sandusky Street, Delaware."),
        ("liquor-rosebuds", "City of Delaware", "DELAWARE CITY", "Delaware City 4-B (precinct 062)", "Local liquor option: Rosebud's (Sunday)",
         "Sunday sale of wine and mixed beverages, and spirituous liquor by FHDR, L.L.C., dba Rosebud's, applicant for a D-6 permit, restaurant at 3 W. Winter Street, Delaware."),
        ("liquor-restoration-brew-worx", "City of Delaware", "DELAWARE CITY", "Delaware City 4-B (precinct 062)", "Local liquor option: Restoration Brew Worx (Sunday)",
         "Sunday sale of wine and mixed beverages and spirituous liquor by Four Fat Bs LLC (dba Restoration Brew Worx), applicant for a D-6 permit, restaurant, craft brewery and taproom at 25 N. Sandusky St, Delaware."),
        ("liquor-chateau-wine", "Orange Township", "ORANGE TWP", "Orange A (precinct 118)", "Local liquor option: Chateau Wine & Spirits (Sunday)",
         "Sunday sale of wine and mixed beverages by Orange Point 117 LLC, dba Chateau Wine & Spirits, applicant for a D-6 permit, specialty wine shop and liquor agency store at the "
         "southeast corner of US 23 and Gooding Blvd./Orangepoint Drive, Orange Township, Lewis Center."),
        ("liquor-skybox-sunday", "Orange Township", "ORANGE TWP", "Orange U (precinct 138)", "Local liquor option: The Skybox Sports Bar (Sunday)",
         "Sunday sale of wine and mixed beverages and spirituous liquor by Skybox Sports Bar Inc., known as The Skybox Sports Bar, applicant for a D-6 permit, sports bar at 1317 Cameron Ave., Orange Township, Lewis Center."),
        ("liquor-skybox", "Orange Township", "ORANGE TWP", "Orange U (precinct 138)", "Local liquor option: The Skybox Sports Bar",
         "Sale of wine and mixed beverages by Skybox Sports Bar Inc., known as The Skybox Sports Bar, applicant for a D-5 permit, sports bar at 1317 Cameron Ave., Orange Township, Lewis Center."),
        ("liquor-ostrander-brewing", "Scioto Township", "SCIOTO TWP", "Scioto B (precinct 159)", "Local liquor option: Ostrander Brewing Company",
         "Sale of beer, wine and mixed beverages, and spirituous liquor by Ostrander Brewing Company, L.L.C., applicant for an A-1A permit, brewery/community gathering venue at 3794 Ostrander Road, Ostrander (Scioto Township)."),
        ("liquor-ostrander-brewing-sunday", "Scioto Township", "SCIOTO TWP", "Scioto B (precinct 159)", "Local liquor option: Ostrander Brewing Company (Sunday)",
         "Sunday sale of wine and mixed beverages, and spirituous liquor by Ostrander Brewing Company, L.L.C., applicant for a D-6 permit, brewery/community gathering venue at 3794 Ostrander Road, Ostrander (Scioto Township)."),
        ("liquor-sticks-table-tap", "City of Sunbury", "SUNBURY CITY", "Sunbury City A (precinct 161)", "Local liquor option: Sticks Table & Tap",
         "Sale of spirituous liquor by JPN Restaurants, L.L.C., dba Sticks Table & Tap, applicant for an A-1-A permit, brewery/restaurant at 571 W. Cherry Street, Sunbury."),
        ("liquor-sticks-table-tap-sunday", "City of Sunbury", "SUNBURY CITY", "Sunbury City A (precinct 161)", "Local liquor option: Sticks Table & Tap (Sunday)",
         "Sunday sale of wine and mixed beverages, and spirituous liquor by JPN Restaurants, L.L.C., dba Sticks Table & Tap, applicant for a D-6 permit, brewery/restaurant at 571 W. Cherry Street, Sunbury."),
    ]:
        c.issue(id, "liquor", jur, title, P(raw), area=prec, text=text, src=I)
    return c
