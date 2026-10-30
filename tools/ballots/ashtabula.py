from lib import County, NOTE_ORDER, NOTE_PLACES, NOTE_UNKNOWN

TYPES = {"REN": "Renewal", "ADD": "Additional", "REN+INC": "Renewal and increase", "REN+RED": "Renewal and reduction"}

def build():
    c = County("ashtabula", "Ashtabula", "39007")
    c.src("ashtabula-cand", "Ashtabula County Board of Elections: candidate list, November 3, 2026 General Election (revised 9-15-26)",
          "https://www.boe.ohio.gov/ashtabula/c/upload/Election_Candidates.pdf")
    c.src("ashtabula-issues", "Ashtabula County Board of Elections: issues sheet, November 3, 2026 General Election (revised 9/15/26)",
          "https://www.boe.ohio.gov/ashtabula/c/upload/Election_Issues.pdf")
    C = ["ashtabula-cand"]; I = ["ashtabula-issues"]
    c.links = [
        {"label": "Board of Elections", "url": "https://www.boe.ohio.gov/ashtabula/"},
        {"label": "Sample ballots", "url": "https://www.boe.ohio.gov/ashtabula/c/upload/Ballots_NonSampleBallots.pdf"},
    ]
    c.results_links = [{"label": "Board of Elections", "url": "https://www.boe.ohio.gov/ashtabula/"}]
    c.notes = ["Taken from the Board of Elections' candidate list and issues sheet. The issues sheet is the Board's abbreviated summary; "
               "the full wording is on the sample ballot.", NOTE_ORDER, NOTE_PLACES, NOTE_UNKNOWN]

    c.contest("congress-14", "U.S. House", "Representative to Congress", [("David P. Joyce", "REP"), ("Maria Jukic", "DEM")], detail="14th District", src=C)
    c.contest("rep-65", "Ohio General Assembly", "State Representative", [("John Barbo", "DEM"), ("David Thomas", "REP")], detail="65th District", places=c.district("rep", 65), src=C)
    c.contest("rep-99", "Ohio General Assembly", "State Representative", [("Sarah Fowler Arthur", "REP"), ("Louis Murphy", "DEM")], detail="99th District", places=c.district("rep", 99), src=C)
    c.contest("appeals-11-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Marisa L. Cornachio", "REP")], detail="11th District · full term commencing February 9, 2027", src=C)
    c.contest("appeals-11-0210", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Robert J. Patton", "REP")], detail="11th District · full term commencing February 10, 2027", src=C)
    NP = " · no party label on the ballot"
    c.contest("cp-0101", "Court of Common Pleas", "Judge of the Court of Common Pleas", ["Marianne Sezon"], detail="Full term commencing January 1, 2027" + NP, src=C)
    c.contest("cp-0102", "Court of Common Pleas", "Judge of the Court of Common Pleas", ["Albert S. Camplese", "Harold E. Specht Jr."], detail="Full term commencing January 2, 2027" + NP, src=C)
    c.contest("cp-0209", "Court of Common Pleas", "Judge of the Court of Common Pleas", ["Thomas E. Harris"], detail="Full term commencing February 9, 2027" + NP, src=C)
    c.contest("cp-probate-0209", "Court of Common Pleas", "Judge of the Court of Common Pleas, Probate Division", ["Edith M. Jonas"], detail="Full term commencing February 9, 2027" + NP, src=C)
    c.contest("commissioner", "County offices", "County Commissioner", [("Casey Kozlowski", "REP"), ("Jayson-Robert T. Noscal", "DEM")], detail="Full term commencing January 1, 2027", src=C)
    c.contest("auditor", "County offices", "County Auditor", [("Oakey L. Emery", "DEM"), ("Scott Yamamoto", "REP")], detail="Full term commencing March 11, 2027", src=C)
    c.contest("coroner", "County offices", "County Coroner", [("Catherine A. Bishop", "REP")], detail="Unexpired term ending December 31, 2028", src=C)

    # (issue no, jurisdiction, places (raw SoS names, "county", or None = special district), type, mills, purpose, years, span)
    L = [
        (4, "Ashtabula County Metroparks", "county", "ADD", "0.5 mill", "Parks and recreation.", "15 years", "2027–2041"),
        (5, "Conneaut Township Park District", None, "ADD", "1.25 mills", "Current operating expenses.", "5 years", "2027–2031"),
        (6, "Jefferson Emergency Rescue District", None, "REN", "2 mills", "Ambulance and EMS.", "5 years", "2027–2031"),
        (7, "Northwest Ambulance District", None, "REN", "2 mills", "Ambulance and EMS.", "5 years", "2027–2031"),
        (8, "Saybrook Township Park District", None, "REN", "0.5 mill", "Current operating expenses.", "3 years", "2027–2029"),
        (9, "Andover Village", ["ANDOVER VILLAGE"], "REN", "1.46 mills", "Current operating expenses.", "5 years", "2027–2031"),
        (11, "Geneva-on-the-Lake Village", ["GENEVA-ON-THE-LAKE VILLAGE"], "ADD", "1.99 mills", "Police.", "5 years", "2026–2030"),
        (12, "Jefferson Village", ["JEFFERSON VILLAGE"], "REN", "1 mill", "Parks and recreation.", "5 years", "2027–2031"),
        (13, "Jefferson Village", ["JEFFERSON VILLAGE"], "REN", "1.5 mills", "Fire.", "5 years", "2027–2031"),
        (14, "North Kingsville Village", ["NORTH KINGSVILLE VILLAGE"], "ADD", "1 mill", "Ambulance and EMS.", "5 years", "2027–2031"),
        (15, "North Kingsville Village", ["NORTH KINGSVILLE VILLAGE"], "REN+INC", "2 mills", "Police services.", "5 years", "2027–2031"),
        (16, "Andover Township (excluding Andover Village)", ["ANDOVER TWP"], "REN", "2 mills", "Ambulance.", "2 years", "2027–2028"),
        (17, "Andover Township (excluding Andover Village)", ["ANDOVER TWP"], "REN", "2 mills", "Roads and bridges.", "5 years", "2027–2031"),
        (18, "Ashtabula Township (excluding Ashtabula City)", ["ASHTABULA TWP"], "REN", "1 mill", "Cemeteries.", "5 years", "2027–2031"),
        (19, "Ashtabula Township (excluding Ashtabula City)", ["ASHTABULA TWP"], "REN", "1.25 mills", "Roads and bridges.", "5 years", "2027–2031"),
        (20, "Ashtabula Township (excluding Ashtabula City)", ["ASHTABULA TWP"], "REN", "1 mill", "Fire and EMS.", "5 years", "2027–2031"),
        (21, "Ashtabula Township (excluding Ashtabula City)", ["ASHTABULA TWP"], "REN", "1.5 mills", "Fire and EMS.", "5 years", "2027–2031"),
        (22, "Ashtabula Township (excluding Ashtabula City)", ["ASHTABULA TWP"], "REN", "2.5 mills", "Fire and EMS.", "5 years", "2027–2031"),
        (23, "Austinburg Township", ["AUSTINBURG TWP"], "REN", "1 mill", "Current operating expenses.", "5 years", "2027–2031"),
        (24, "Austinburg Township", ["AUSTINBURG TWP"], "REN+INC", "1.4 mills", "Fire.", "5 years", "2027–2031"),
        (25, "Cherry Valley Township", ["CHERRY VALLEY TWP"], "REN+RED", "1 mill", "Fire.", "5 years", "2027–2031"),
        (26, "Colebrook Township", ["COLEBROOK TWP"], "REN", "1.5 mills", "Fire protection.", "5 years", "2027–2031"),
        (27, "Colebrook Township", ["COLEBROOK TWP"], "ADD", "2 mills", "Roads and bridges.", "5 years", "2026–2030"),
        (28, "Denmark Township", ["DENMARK TWP"], "REN", "1 mill", "Fire and EMS.", "5 years", "2027–2031"),
        (29, "Geneva Township (excluding the city and village)", ["GENEVA TWP"], "REN", "1 mill", "Roads and bridges.", "5 years", "2027–2031"),
        (30, "Geneva Township (excluding the city and village)", ["GENEVA TWP"], "REN", "1.49 mills", "Fire.", "5 years", "2027–2031"),
        (31, "Harpersfield Township", ["HARPERSFIELD TWP"], "REN", "1.5 mills", "Roads and bridges.", "5 years", "2027–2031"),
        (32, "Kingsville Township", ["KINGSVILLE TWP"], "REN", "1 mill", "Cemeteries.", "5 years", "2027–2031"),
        (33, "Lenox Township", ["LENOX TWP"], "REN", "1.5 mills", "Fire and EMS.", "", "2027–2031"),
        (34, "Morgan Township (excluding Rock Creek and Roaming Shores villages)", ["MORGAN TWP"], "REN", "1.5 mills", "Roads and bridges.", "5 years", "2027–2031"),
        (35, "Orwell Township (excluding Orwell Village)", ["ORWELL TWP"], "REN", "1.5 mills", "Fire protection.", "5 years", "2027–2031"),
        (36, "Pierpont Township", ["PIERPONT TWP"], "REN", "2.5 mills", "Fire and ambulance service.", "5 years", "2027–2031"),
        (37, "Richmond Township", ["RICHMOND TWP"], "REN+INC", "2 mills", "Fire and EMS.", "2 years", "2027–2028"),
        (38, "Sheffield Township", ["SHEFFIELD TWP"], "REN", "0.5 mill", "Cemetery.", "5 years", "2027–2031"),
        (39, "Sheffield Township", ["SHEFFIELD TWP"], "ADD", "4.5 mills", "Fire and EMS.", "5 years", "2027–2031"),
        (40, "Windsor Township", ["WINDSOR TWP"], "ADD", "2.5 mills", "Fire and EMS.", "5 years", "2027–2031"),
    ]
    for n, jur, raws, t, mills, purpose, yrs, span in L:
        places = raws if raws in ("county", None) else c.p(*raws)
        term = f"{yrs}, {span}".strip(", ") if yrs else span
        c.levy(f"issue-{n}", jur, places, TYPES[t], purpose, mills, term, number=f"Issue {n}", src=I)
    c.issue("issue-10", "question", "Conneaut City", "Proposed charter amendment: data center", c.p("CONNEAUT CITY"), number="Issue 10", src=I)
    for n, raw, pct, biz in [(41, "ASHTABULA CITY", "Ashtabula City 3 B", "Convenient Food Mart"), (42, "TRUMBULL TWP", "Trumbull Township", "Hunters Tavern"), (43, "TRUMBULL TWP", "Trumbull Township", "Monarch Meadow Vineyard")]:
        c.issue(f"issue-{n}", "liquor", pct.rsplit(" ", 1)[0] if raw == "ASHTABULA CITY" else "Trumbull Township", f"Local liquor option: {biz}", c.p(raw), area=pct,
                number=f"Issue {n}", text="Listed by the Board as \"5R - SS\" (see the sample ballot for the question's wording).", src=I)
    return c
