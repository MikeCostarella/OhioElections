from lib import County, NOTE_ORDER, NOTE_PLACES

NOTICE = "https://www.boe.ohio.gov/muskingum/c/upload/FWAB_11November46Day.pdf"


def build():
    # The SoS file spells the village "FRAZEYBURG"; the Board's notice has Frazeysburg.
    c = County("muskingum", "Muskingum", "39119", rename={"FRAZEYBURG VILLAGE": "Frazeysburg Village"})
    c.src("muskingum-46day", "Muskingum County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election (revised 9/18/2026)", NOTICE)
    S = ["muskingum-46day"]
    c.links = [
        {"label": "Board of Elections", "url": "https://www.boe.ohio.gov/muskingum/"},
        {"label": "Election information", "url": "https://www.boe.ohio.gov/muskingum/election-information/"},
        {"label": "Sample ballots by precinct", "url": "https://lookup.boe.ohio.gov/vtrapp/muskingum/ballotlist.aspx"},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://www.boe.ohio.gov/muskingum/election-information/election-results/"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it. "
               "Issue wording is the Board's summary; the full wording is on the sample ballot.",
               NOTE_ORDER, NOTE_PLACES,
               "The Board's notice does not give local issue numbers; see your sample ballot for them."]
    P = c.p

    # --- Federal, state legislative, appeals (the whole county is in each district) ---
    c.contest("congress-12", "U.S. House", "Representative to Congress", [("Troy Balderson", "REP"), ("Jerrad Christian", "DEM")], detail="12th District · full 2-year term commencing January 3, 2027", src=S)
    c.contest("senate-31", "Ohio General Assembly", "State Senator", [("Al Landis", "REP"), ("Laura Sirot", "DEM")], detail="31st District · full 4-year term commencing January 1, 2027", src=S)
    c.contest("rep-97", "Ohio General Assembly", "State Representative", [("Kris Geis", "Nonparty"), ("Tim Godwin", "LIB"), ("Adam P. Holmes", "REP")],
              detail="97th District · full 2-year term commencing January 1, 2027", src=S)
    c.contest("appeals-5", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Matthew George", "REP")], detail="5th District · term commencing February 9, 2027", src=S)

    # --- County offices ---
    c.contest("commissioner", "County offices", "County Commissioner", [("Melissa Bell", "REP")], detail="Full 4-year term commencing January 1, 2027", src=S)
    c.contest("auditor", "County offices", "County Auditor", [("Tina M. Huebner", "REP")], detail="Full 4-year term commencing March 8, 2027", src=S)
    NP = " · no party label on the ballot"
    for id, office, date, cs in [
        ("cp-gen", "Judge of the Court of Common Pleas", "Full 6-year term commencing January 1, 2027", ["Gerald Anderson"]),
        ("cp-dr", "Judge of the Court of Common Pleas, Domestic Relations Division", "Full 6-year term commencing January 2, 2027", ["Maria N. Kalis"]),
        ("cp-probate-juvenile", "Judge of the Court of Common Pleas, Probate and Juvenile Division", "Full 6-year term commencing February 9, 2027", ["Eric D. Martin"]),
    ]:
        c.contest(id, "Court of Common Pleas", office, cs, detail=date + NP, src=S)

    # --- Issues (unnumbered in the Board's notice; listed in the notice's order) ---
    L = [
        ("frazeysburg-police", "Village of Frazeysburg", ["FRAZEYBURG VILLAGE"], "Additional", "Providing and maintaining police department, equipment and personnel.", "3 mills",
         "5 years, commencing in 2026", "2027", "Frazeysburg precinct 33/1"),
        ("norwich-current", "Village of Norwich", ["NORWICH VILLAGE"], "Additional", "Current expenses.", "4 mills", "5 years, commencing in 2026", "2027", "Norwich precinct 60/2"),
        ("philo-roads", "Village of Philo", ["PHILO VILLAGE"], "Additional", "General construction, reconstruction, resurfacing and repair of streets, roads and bridges.", "7.25 mills",
         "5 years, commencing in 2026", "2027", "Philo precinct 28/2"),
        ("roseville-current", "Village of Roseville (Muskingum and Perry counties)", ["ROSEVILLE VILLAGE"], "Renewal", "Current expenses.", "4 mills",
         "5 years, commencing in 2027", "2028", "Roseville precinct 19/2"),
        ("south-zanesville-fire", "Village of South Zanesville", ["SOUTH ZANESVILLE VILLAGE"], "Additional", "Providing fire protection and ambulance or emergency medical services.", "3 mills",
         "5 years, commencing in 2026", "2027", "South Zanesville precincts 47/2, 55/1"),
        ("blue-rock-cemeteries", "Blue Rock Township", ["BLUE ROCK TOWNSHIP"], "Renewal", "Maintaining and operating cemeteries.", "0.4 mill",
         "5 years, commencing in 2027", "2028", "Blue Rock Township precinct 16/1"),
        ("brush-creek-fire", "Brush Creek Township", ["BRUSH CREEK TOWNSHIP"], "Additional",
         "Providing fire protection, ambulance or emergency medical services, and underwater rescue and recovery equipment.", "0.5 mill",
         "5 years, commencing in 2026", "2027", "Brush Creek Township precinct 17/1"),
        ("licking-twp-roads", "Licking Township", ["LICKING TOWNSHIP"], "Renewal", "General construction, reconstruction, resurfacing and repair of streets, roads and bridges.", "1 mill",
         "5 years, commencing in 2026", "2027", "Licking Township precincts 37/1, 37/2, 38/1"),
        ("rich-hill-cemeteries", "Rich Hill Township", ["RICH HILL TOWNSHIP"], "Renewal", "Maintaining and operating cemeteries.", "0.25 mill",
         "5 years, commencing in 2026", "2027", "Rich Hill Township precincts 52/1, 52/2"),
        ("washington-twp-fire", "Washington Township", ["WASHINGTON TOWNSHIP"], "Renewal",
         "Providing fire protection, ambulance or emergency medical services, and underwater rescue and recovery equipment.", "2.5 mills",
         "5 years, commencing in 2027", "2028", "Washington Township precincts 62/1, 63/1, 63/2, 64/1"),
        ("springfield-twp-fire", "Springfield Township (unincorporated area)", ["SPRINGFIELD TOWNSHIP"], "Renewal",
         "Providing fire protection, ambulance or emergency medical services, and underwater rescue and recovery equipment.", "0.7 mill",
         "5 years, commencing in 2026", "2027", "Springfield Township precincts 56/1, 56/2, 57/1, 58/1 (unincorporated area)"),
    ]
    for id, jur, raws, t, purpose, mills, term, fd, area in L:
        c.levy(id, jur, P(*raws), t, purpose, mills, term, fd, area=area, src=S)

    # --- Local liquor options ---
    for id, jur, raw, prec, title, text in [
        ("liquor-crystal-springs-d6", "Hopewell Township", "HOPEWELL TOWNSHIP", "Hopewell A precinct (30, all splits)",
         "Local liquor option: The Golf Club at Crystal Springs (D-6 permit, Sunday)",
         "Local option (D-6 permit): The Golf Club at Crystal Springs, L.L.C., 745 N. Hopewell Road, Hopewell."),
        ("liquor-crystal-springs-d2-d3", "Hopewell Township", "HOPEWELL TOWNSHIP", "Hopewell A precinct (30, all splits)",
         "Local liquor option: The Golf Club at Crystal Springs (D-2 and D-3 permits)",
         "Local option (D-2 and D-3 permits): on/off-premise sales of wine and mixed beverages, and on-premise sales of spirituous liquor, by The Golf Club at Crystal Springs, L.L.C., "
         "745 N. Hopewell Road, Hopewell."),
        # The notice names no permit holder for this one, only the address.
        ("liquor-dresden-705-main", "Village of Dresden", "DRESDEN VILLAGE", "Dresden North precinct (35, all splits)",
         "Local liquor option: 705 Main Street, Dresden (wine and mixed beverages)",
         "Local option (D-2 and D-2X permits): sale of wine and mixed beverages, on/off-premise sales, at 705 Main Street, Dresden. The Board's notice does not name the permit holder."),
        ("liquor-dillon-duchess", "Muskingum Township", "MUSKINGUM TOWNSHIP", "Muskingum A precinct (42, all splits)", "Local liquor option: Dillon Duchess (Sunday)",
         "Local option: Sunday sale of wine and mixed beverages, or spirituous liquor, on-premise, off-premise or on/off-premise sales, by Englefield, Inc., dba Dillon Duchess, "
         "5955 Newark Rd., Nashport."),
        ("liquor-lp-nashport-shell", "Muskingum Township", "MUSKINGUM TOWNSHIP", "Muskingum B precinct (43, all splits)", "Local liquor option: LP Nashport Shell (Sunday)",
         "Local option: Sunday sale of beer, or wine and mixed beverages, or spirituous liquor, on-premise, off-premise or on/off-premise sales, by LP Ohio LLC, dba LP Nashport Shell, "
         "6220 Frazeysburg Rd., Nashport."),
        ("liquor-norwich-shell", "Perry Township", "PERRY TOWNSHIP", "Perry North precinct (50, all splits)", "Local liquor option: Norwich Shell (Sunday)",
         "Local option: Sunday sale of wine and mixed beverages, and spirituous liquor, on/off-premise sales, by MW Retail, L.L.C., dba Norwich Shell, 8490 E. Pike, Norwich (Perry Township)."),
        ("liquor-south-60-marathon", "Wayne Township", "WAYNE TOWNSHIP", "Wayne A precinct (65, all splits)", "Local liquor option: South 60 Marathon (Sunday)",
         "Local option: Sunday sale of beer, or wine and mixed beverages, or spirituous liquor, on-premise, off-premise or on/off-premise sales, by LP South 60 Market LLC, "
         "aka South 60 Marathon, 2040 S. River Rd., Zanesville."),
    ]:
        c.issue(id, "liquor", jur, title, P(raw), area=prec, text=text, src=S)
    return c
