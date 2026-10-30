from lib import County, NOTE_ORDER, NOTE_PLACES

NOTE_TWP = ("Township levies are shown for the township's own voters; if you live in a city or village inside a township, "
            "check your sample ballot for whether the township levy is on it.")

def build():
    c = County("columbiana", "Columbiana", "39029")
    c.src("columbiana-zero", "Columbiana County Board of Elections: 2026 General Election zero report (every contest and issue on Columbiana's ballots)",
          "https://columbiana.boe.ohio.gov/wp-content/uploads/2026/09/2026-General-Election-Zero-Report.pdf")
    c.src("mahoning-filings", "Mahoning County Board of Elections: filings for the November 3, 2026 General Election (millage for issues shared with Mahoning)",
          "https://vote.mahoningcountyoh.gov/DocumentCenter/View/2640/Filings-for-November-3-2026-General-Election")
    Z = ["columbiana-zero"]; ZM = ["columbiana-zero", "mahoning-filings"]
    c.links = [
        {"label": "Board of Elections", "url": "https://columbiana.boe.ohio.gov/"},
        {"label": "Sample ballots", "url": "https://columbiana.boe.ohio.gov/elections/sample-ballots/"},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://columbiana.boe.ohio.gov/elections/election-results/"}]
    c.notes = ["Taken from the Board of Elections' pre-election zero report, which lists every contest and issue on the county's ballots. "
               "The report names issues but not their millage; millage is shown where the Mahoning County Board's list gives it for a shared issue. "
               "See your sample ballot for the full wording.", NOTE_ORDER, NOTE_PLACES, NOTE_TWP]

    c.contest("congress-6", "U.S. House", "Representative to Congress", [("Elizabeth Kirtley", "DEM"), ("Michael A. Rulli", "REP")], detail="6th District", src=Z)
    c.contest("senate-33", "Ohio General Assembly", "State Senator", [("Al Cutrona", "REP"), ("Michael L. Kripchak", "DEM")], detail="33rd District", src=Z)
    c.contest("rep-59", "Ohio General Assembly", "State Representative", [("Tex Fischer", "REP"), ("Wayne Penny Jr.", "DEM")], detail="59th District", places=c.district("rep", 59), src=Z)
    c.contest("rep-79", "Ohio General Assembly", "State Representative", [("Monica Robb Blasdel", "REP"), ("Bob Guy", "DEM")], detail="79th District", places=c.district("rep", 79), src=Z)
    c.contest("appeals-7-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Molly K. Johnson", "REP")], detail="7th District · full term commencing February 9, 2027", src=Z)
    c.contest("appeals-7-0210", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Mark Anthony Hanni", "REP"), ("Katherine Rudzik", "DEM")], detail="7th District · full term commencing February 10, 2027", src=Z)
    c.contest("commissioner", "County offices", "County Commissioner", [("Mike Halleck", "REP")], detail="Full term commencing January 1, 2027", src=Z)
    c.contest("auditor", "County offices", "County Auditor", [("Nancy Gause Milliken", "REP")], src=Z)
    c.contest("cp-probate-juv", "Court of Common Pleas", "Judge of the Court of Common Pleas, Probate/Juvenile Division", ["Thomas M. Baronzzi"], detail="Full term commencing February 9, 2027 · no party label on the ballot", src=Z)

    T = lambda *raws: c.p(*raws)
    c.issue("alliance-csd", "levy", "Alliance City School District", "Tax levy: buildings", c.sd("ALLIANCE CITY SD"), src=Z)
    c.issue("east-palestine-sd-income", "question", "East Palestine City School District", "School district income tax", c.sd("EAST PALESTINE CITY SD"), src=Z)
    c.levy("west-branch-lsd", "West Branch Local School District", c.sd("WEST BRANCH LOCAL SD (MAHONING)"), "Additional", "General permanent improvement.", "1 mill", "5 years",
           estimate="$441,471 a year; $35 for each $100,000 of market value", src=ZM)
    c.issue("east-palestine-police", "levy", "Village of East Palestine", "Tax levy: police", T("EAST PALESTINE VILLAGE"), src=Z)
    c.issue("east-palestine-charter-303", "question", "Village of East Palestine", "Charter amendment: Section 3.03", T("EAST PALESTINE VILLAGE"), src=Z)
    c.issue("east-palestine-charter-multi", "question", "Village of East Palestine", "Charter amendment: Sections 4.13, 4.15, 4.16, 8.05 and 10.05", T("EAST PALESTINE VILLAGE"), src=Z)
    c.levy("salem-parks", "City of Salem", T("SALEM CITY"), "Renewal", "Recreational purposes (parks).", "1 mill", "5 years",
           estimate="$166,794 a year; $12 for each $100,000 of market value", src=ZM)
    c.issue("butler-roads", "levy", "Butler Township", "Tax levy: roads", T("BUTLER TWP"), src=Z)
    c.issue("center-fire", "levy", "Center Township", "Tax levy: fire", T("CENTER TWP"), src=Z)
    c.levy("fairfield-roads", "Fairfield Township", T("FAIRFIELD TWP", "COLUMBIANA CITY"), "Renewal", "Roads and bridges.", "1.6 mills", "5 years",
           estimate="$388,340 a year; $25 for each $100,000 of market value", src=ZM,
           note="Shown for the City of Columbiana too: the Mahoning Board lists it for the part of the city in Mahoning County.")
    c.issue("knox-roads", "levy", "Knox Township", "Tax levy: roads", T("KNOX TWP"), src=Z)
    c.issue("liverpool-fire", "levy", "Liverpool Township", "Tax levy: fire", T("LIVERPOOL TWP"), src=Z)
    c.issue("middleton-fire", "levy", "Middleton Township", "Tax levy: fire", T("MIDDLETOWN TWP"), src=Z)
    c.levy("perry-police", "Perry Township", T("PERRY TWP"), "Not stated", "Police department.", "1.5 mills", "5 years",
           estimate="$222,295 a year; $53 for each $100,000 of market value", src=ZM)
    c.issue("wayne-fire", "levy", "Wayne Township", "Tax levy: fire", T("WAYNE TWP"), src=Z)
    c.issue("west-roads", "levy", "West Township", "Tax levy: roads", T("WEST TWP"), src=Z)
    c.issue("liquor-salem-genes", "liquor", "City of Salem", "Local liquor option: Gene's Drive Thru", T("SALEM CITY"), area="Salem City precinct 2-A", src=Z)
    c.issue("liquor-salineville-legion", "liquor", "Village of Salineville", "Local liquor option: American Legion", T("SALINEVILLE VILLAGE"), area="Salineville Village", src=Z)
    return c
