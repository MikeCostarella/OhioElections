from lib import County, NOTE_ORDER, NOTE_PLACES

NOTICE = "https://www.portagecounty-oh.gov/sites/g/files/vyhlif3706/f/uploads/november_3_2026_46_day_notice_update.pdf"

def build():
    c = County("portage", "Portage", "39133", rename={"SHALERSVILLE TOWNSHP": "Shalersville Township"})
    c.src("portage-46day", "Portage County Board of Elections: updated 46-day election notice, November 3, 2026 General Election", NOTICE)
    S = ["portage-46day"]
    c.links = [
        {"label": "Board of Elections", "url": "https://www.portagecounty-oh.gov/board-elections"},
        {"label": "Sample ballots by precinct", "url": "https://lookup.boe.ohio.gov/vtrapp/portage/ballotlist.aspx"},
    ]
    c.results_links = [{"label": "Board of Elections", "url": "https://www.portagecounty-oh.gov/board-elections"}]
    c.notes = ["Taken from the Board of Elections' updated 46-day election notice, which lists every contest and issue with the precincts that vote on it. "
               "Issue wording is the notice's summary; the full wording is on the sample ballot.", NOTE_ORDER, NOTE_PLACES]
    P = c.p; D = c.district

    c.contest("congress-13", "U.S. House", "Representative to Congress", [("Emilia Sykes", "DEM"), ("Carey Coleman", "REP"), ("Sandeep Dixit", "Non-party")], detail="13th District", places=D("cong", 13), src=S)
    c.contest("congress-14", "U.S. House", "Representative to Congress", [("Maria Jukic", "DEM"), ("David P. Joyce", "REP")], detail="14th District", places=D("cong", 14), src=S)
    c.contest("senate-27", "Ohio General Assembly", "State Senator", [("Mike Roberto", "DEM"), ("Steve Demetriou", "REP")], detail="27th District", src=S)
    c.contest("rep-35", "Ohio General Assembly", "State Representative", [("Samantha Salamon", "DEM"), ("Vik Sandhu", "REP")], detail="35th District", places=D("rep", 35), src=S)
    c.contest("rep-72", "Ohio General Assembly", "State Representative", [("Jeff Clapper", "DEM"), ("Michael Fricke", "LIB"), ("Heidi Workman", "REP")], detail="72nd District", places=D("rep", 72), src=S)
    c.contest("appeals-11-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Marisa L. Cornachio", "REP")], detail="11th District · term commencing February 9, 2027", src=S)
    c.contest("appeals-11-0210", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Robert J. Patton", "REP")], detail="11th District · term commencing February 10, 2027", src=S)
    c.contest("commissioner", "County offices", "County Commissioner", [("Jenny D. Adams", "DEM"), ("Mike Tinlin", "REP")], src=S)
    c.contest("auditor", "County offices", "County Auditor", [("Matt Kelly", "REP")], src=S)
    NP = " · no party label on the ballot"
    c.contest("cp-gen", "Court of Common Pleas", "Judge of the Court of Common Pleas, General Division", ["Becky L. Doherty"], detail=NP.strip(" ·"), src=S)
    c.contest("cp-juv-probate", "Court of Common Pleas", "Judge of the Court of Common Pleas, Juvenile/Probate Division", ["Patricia J. Smith"], detail=NP.strip(" ·"), src=S)

    N = lambda n: f"Issue {n}"
    e = lambda per: f"{per} for each $100,000 of the Auditor's market value"
    c.issue("issue-4", "levy", "Aurora City School District (Portage and Summit)", "Bond issue: $96,200,000 for an elementary school and other building improvements", P("AURORA CITY"), number=N(4),
            levy={"type": "Bond issue", "purpose": "Elementary school building and other building improvements.", "mills": "4.26 mills", "term": "37 years, commencing in 2026", "estimate": "$96,200,000 bond"}, src=S)
    L = [
        (5, "Ravenna City School District", ["RAVENNA CITY", "RAVENNA TOWNSHIP", "CHARLESTOWN TOWNSHIP", "SHALERSVILLE TOWNSHP"], "Renewal", "General permanent improvements.", "2.9 mills", "Continuing period of time, commencing in 2027", "$60", "Ravenna City, Ravenna Township, Charlestown Township A split 2, Shalersville Township D split 2"),
        (6, "Stow-Munroe Falls City School District (Summit and Portage)", ["FRANKLIN TOWNSHIP"], "Renewal", "Current expenses.", "3.17 mills", "5 years, commencing in 2026", "$97", "Franklin Township A, split 2"),
        (7, "Streetsboro City School District", ["STREETSBORO CITY"], "Renewal", "Current expenses (3.6 mills) and general permanent improvements (1.5 mills).", "5.1 mills", "5 years, commencing in 2026", "$96", "Streetsboro City except Streetsboro City 4B, split 2"),
        (9, "Crestwood Local School District", ["HIRAM VILLAGE", "HIRAM TOWNSHIP", "MANTUA TOWNSHIP", "MANTUA VILLAGE", "SHALERSVILLE TOWNSHP"], "Renewal", "General permanent improvements.", "3.5 mills", "5 years, commencing in 2027", "$26", "Hiram Village, Hiram Township A and B split 1, Mantua Township, Mantua Village, Shalersville Township A–D split 1"),
        (10, "West Branch Local School District (Mahoning and Portage)", ["DEERFIELD TOWNSHIP"], "Additional", "General permanent improvements.", "1 mill", "5 years, commencing in 2026", "$35", "Deerfield Township B, split 2"),
        (11, "Garrettsville, Freedom, Nelson Joint Fire District", ["GARRETTSVILLE VILLAGE", "FREEDOM TOWNSHIP", "NELSON TOWNSHIP"], "Renewal", "Fire and emergency medical services.", "3.2 mills", "5 years, commencing in 2027", "$85", None),
        (12, "Stark County District Library", ["SUFFIELD TOWNSHIP"], "Renewal and increase", "Current expenses.", "2.3 mills", "8 years, commencing in 2027", "$55", "Suffield Township C, split 2"),
        (13, "Portage County Job and Family Services", "county", "Additional", "Public assistance and human services.", "0.4 mill", "5 years, commencing in 2026", "$14", "All of Portage County"),
        (14, "Portage County Mental Health and Recovery Board", "county", "Renewal", "Current expenses.", "0.3 mill", "10 years, commencing in 2027", "$6", "All of Portage County"),
        (17, "City of Aurora", ["AURORA CITY"], "Renewal", "Roads and bridges.", "0.9 mill", "5 years, commencing in 2026", "$16", None),
        (19, "Village of Hiram", ["HIRAM VILLAGE"], "Renewal", "Current expenses.", "4.4 mills", "5 years, commencing in 2026", "$99", None),
        (20, "Village of Mogadore (Portage and Summit)", ["MOGADORE VILLAGE"], "Renewal and increase", "Fire and emergency medical services.", "4.73 mills", "5 years, commencing in 2027", "$135", None),
        (27, "Brimfield Township", ["BRIMFIELD TOWNSHIP"], "Additional", "Fire and emergency medical services.", "1.95 mills", "5 years, commencing in 2026", "$68", None),
        (28, "Deerfield Township", ["DEERFIELD TOWNSHIP"], "Renewal and increase", "Fire and emergency medical services.", "2.75 mills", "5 years, commencing in 2027", "$66", None),
        (29, "Franklin Township", ["FRANKLIN TOWNSHIP"], "Renewal", "Roads and bridges.", "2 mills", "5 years, commencing in 2026", "$17", None),
        (30, "Paris Township", ["PARIS TOWNSHIP"], "Renewal", "Fire and emergency medical services.", "2 mills", "5 years, commencing in 2027", "$22", None),
        (32, "Ravenna Township", ["RAVENNA TOWNSHIP"], "Additional", "Emergency medical services.", "4.5 mills", "5 years, commencing in 2027", "$158", None),
    ]
    for n, jur, raws, t, purpose, mills, term, per, area in L:
        places = "county" if raws == "county" else P(*raws)
        c.levy(f"issue-{n}", jur, places, t, purpose, mills, term, None, e(per), number=N(n), area=area, src=S)
    c.issue("issue-8", "question", "Tallmadge City School District (Summit and Portage)", "School district income tax: 1% on earned income for current expenses", P("BRIMFIELD TOWNSHIP"), number=N(8),
            area="Brimfield Township E, split 2", text="Earned income tax of 1%, for current expenses, for a continuing period of time, commencing January 1, 2027.", src=S)
    c.issue("issue-15", "question", "City of Ravenna", "Additional 0.25% income tax for fire, police and city hall facilities", P("RAVENNA CITY"), number=N(15),
            text="Additional income tax of 0.25%, for facilities for fire, police and city hall, for 30 years, commencing January 1, 2027.", src=S)
    c.issue("issue-16", "question", "City of Kent", "Income tax: reallocate the 0.25% income tax and extend it for a continuing period", P("KENT CITY"), number=N(16),
            text="Reallocation of the 0.25% income tax and extension of its term to a continuing period of time.", src=S)
    for n, art, what in [(21, "Article III, Section 3.12", "Posting of ordinances or resolutions."), (22, "Article IV, Section 4.03", "Mayoral absence."),
                         (23, "Article V", "Change the Clerk-Treasurer position to separate Clerk and Fiscal Officer positions."), (24, "Article X", "Change Board of Zoning Appeals membership from 7 to 5.")]:
        c.issue(f"issue-{n}", "question", "Village of Mogadore (Portage and Summit)", f"Charter amendment: {art}", P("MOGADORE VILLAGE"), number=N(n), text=what, src=S)
    c.issue("issue-31", "question", "Paris Township", "Repeal of zoning in the township", P("PARIS TOWNSHIP"), number=N(31), text="Shall zoning in Paris Township be repealed? (summary)", src=S)
    LQ = [
        (18, "Village of Garrettsville", "GARRETTSVILLE VILLAGE", "Garrettsville Village A", "Silver Crik Saloon (Sunday)", "Sunday sales of wine and mixed beverages and spirituous liquor; Stan Leigh Corp., dba Silver Crik Saloon."),
        (25, "Atwater Township", "ATWATER TOWNSHIP", "Atwater Township B", "The Watering Hole", "Sale of wine and mixed beverages at a particular location; K.J.'s Watering Hole, L.L.C., dba The Watering Hole."),
        (26, "Atwater Township", "ATWATER TOWNSHIP", "Atwater Township B", "The Watering Hole (Sunday)", "Sunday sales of wine and mixed beverages; K.J.'s Watering Hole, L.L.C., dba The Watering Hole."),
    ]
    for n, jur, raw, pct, biz, text in LQ:
        c.issue(f"issue-{n}", "liquor", jur, f"Local liquor option: {biz}", P(raw), number=N(n), area=f"Precinct {pct}", text=text, src=S)
    return c
