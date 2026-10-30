from lib import County, NOTE_ORDER, NOTE_PLACES

def build():
    c = County("mahoning", "Mahoning", "39099")
    c.src("mahoning-filings", "Mahoning County Board of Elections: filings for the November 3, 2026 General Election",
          "https://vote.mahoningcountyoh.gov/DocumentCenter/View/2640/Filings-for-November-3-2026-General-Election")
    c.src("columbiana-zero", "Columbiana County Board of Elections: 2026 General Election zero report (lists every contest on Columbiana's ballots)",
          "https://columbiana.boe.ohio.gov/wp-content/uploads/2026/09/2026-General-Election-Zero-Report.pdf")
    F = ["mahoning-filings"]
    c.links = [
        {"label": "Board of Elections", "url": "https://vote.mahoningcountyoh.gov/"},
        {"label": "Ohio sample ballot lookup", "url": "https://www.ohiosos.gov/elections/voters/toolkit/sample-ballot/"},
    ]
    c.results_links = [{"label": "Board of Elections: election information and results", "url": "https://vote.mahoningcountyoh.gov/"}]
    c.notes = ["Taken from the Board of Elections' list of filings for the general election.", NOTE_ORDER, NOTE_PLACES]

    c.contest("congress-6", "U.S. House", "Representative to Congress", [("Elizabeth Kirtley", "DEM"), ("Michael A. Rulli", "REP")], detail="6th District", places=c.district("cong", 6), src=F)
    c.contest("congress-14", "U.S. House", "Representative to Congress", [("David P. Joyce", "REP"), ("Maria Jukic", "DEM")], detail="14th District", places=c.district("cong", 14), src=F)
    c.contest("senate-33", "Ohio General Assembly", "State Senator", [("Al Cutrona", "REP"), ("Michael L. Kripchak", "DEM")], detail="33rd District", places=c.district("sen", 33), src=F)
    c.contest("rep-58", "Ohio General Assembly", "State Representative", [("John A. Boccieri", "DEM"), ("Heather Fronk", "REP")], detail="58th District", places=c.district("rep", 58), src=F)
    c.contest("rep-59", "Ohio General Assembly", "State Representative", [("Tex Fischer", "REP"), ("Wayne Penny, Jr.", "DEM")], detail="59th District", places=c.district("rep", 59), src=F)
    c.contest("appeals-7-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Molly K. Johnson", "REP")], detail="7th District · full term commencing February 9, 2027", src=F)
    c.contest("appeals-7-0210", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Mark Anthony Hanni", "REP"), ("Katherine Rudzik", "DEM")], detail="7th District · full term commencing February 10, 2027", src=F)
    c.contest("commissioner", "County offices", "County Commissioner", [("Lauren McNally", "DEM"), ("Christine Oliver", "REP")], src=F)
    c.contest("auditor", "County offices", "County Auditor", [("Ralph T. Meacham", "REP"), ("Dalton Bosze", "DEM")], src=F)
    NP = " · no party label on the ballot"
    c.contest("cp-gen-0102", "Court of Common Pleas", "Judge of the Court of Common Pleas, General Division", ["Maureen A. Sweeney"], detail="Term commencing January 2, 2027" + NP, src=F)
    c.contest("cp-gen-0209", "Court of Common Pleas", "Judge of the Court of Common Pleas, General Division", ["Ross T. Smith", "Mark P. D'Apolito"], detail="Term commencing February 9, 2027" + NP, src=F)
    c.contest("cp-gen-0701", "Court of Common Pleas", "Judge of the Court of Common Pleas, General Division", ["Ralph Rivera", "J. Michael Thompson", "Robert Andrews", "Jeff Limbian"], detail="Term commencing July 1, 2027" + NP, src=F)
    c.contest("cp-dr-0101", "Court of Common Pleas", "Judge of the Court of Common Pleas, Domestic Relations Division", ["Mark Anthony DeVicchio", "Terry A. Grenga"], detail="Term commencing January 1, 2027" + NP, src=F)
    c.contest("cp-probate-0209", "Court of Common Pleas", "Judge of the Court of Common Pleas, Probate Division", ["Robert N. Rusu, Jr."], detail="Term commencing February 9, 2027" + NP, src=F)

    def est(total, per):
        return f"{total} a year; {per} for each $100,000 of market value"
    Y5 = "5 years"
    c.levy("mcbdd", "Mahoning County Board of Developmental Disabilities", "county", "Additional", "Maintaining the Mahoning County Board of Developmental Disabilities.", "2.4 mills", Y5, estimate=est("$15,522,964", "$84"), area="All of Mahoning County", src=F)
    c.levy("canfield-police", "City of Canfield", c.p("CANFIELD CITY"), "Renewal", "Police department.", "3.9 mills", Y5, estimate=est("$812,524", "$82"), src=F)
    c.levy("austintown-parks", "Austintown Township", c.p("AUSTINTOWN TWP"), "Renewal", "Parks and recreational purposes.", "0.8 mill", Y5, estimate=est("$321,610", "$10"), src=F)
    c.levy("austintown-seniors", "Austintown Township", c.p("AUSTINTOWN TWP"), "Renewal", "Senior citizen services.", "0.5 mill", Y5, estimate=est("$327,568", "$11"), src=F)
    c.levy("boardman-safety", "Boardman Township", c.p("BOARDMAN TWP"), "Additional", "Police and fire.", "2.75 mills", Y5, estimate=est("$3,772,795", "$96"), src=F)
    c.levy("poland-twp-roads", "Poland Township", c.p("POLAND TWP"), "Renewal", "Repair of roads.", "2 mills", Y5, estimate=est("$227,666", "$13"), src=F)
    c.levy("springfield-fire", "Springfield Township", c.p("SPRINGFIELD TWP"), "Renewal", "Fire department.", "1.5 mills", Y5, estimate=est("$179,695", "$22"), src=F)
    c.levy("springfield-current", "Springfield Township", c.p("SPRINGFIELD TWP"), "Renewal", "Current expenses.", "1.5 mills", Y5, estimate=est("$135,515", "$15"), src=F)
    c.levy("new-middletown-roads", "Village of New Middletown", c.p("NEW MIDDLETOWN VILLAGE"), "Renewal", "Streets, roads and bridges.", "1.5 mills", Y5, estimate=est("$44,786", "$39"), src=F)
    c.levy("poland-village-police", "Village of Poland", c.p("POLAND VILLAGE"), "Renewal", "Police department.", "1 mill", Y5, estimate=est("$53,300", "$23"), src=F)
    sd = c.sd
    c.levy("boardman-lsd", "Boardman Local School District", sd("BOARDMAN LOCAL SD (MAHONING)"), "Renewal", "Providing for the emergency requirements.", "3.72 mills", "10 years", estimate=est("$4,646,975", "$130"), src=F)
    c.levy("canfield-lsd", "Canfield Local School District", sd("CANFIELD LOCAL SD (MAHONING)"), "Additional", "Current expenses.", "5.9 mills", Y5, estimate=est("$5,715,791", "$207"), src=F)
    c.levy("lowellville-lsd", "Lowellville Local School District", sd("LOWELLVILLE LOCAL SD (MAHONING)"), "Renewal", "General permanent improvements.", "4 mills", Y5, estimate=est("$224,058", "$107"), src=F)
    c.levy("poland-lsd-emergency", "Poland Local School District", sd("POLAND LOCAL SD (MAHONING)"), "Renewal", "Emergency requirements.", "3.57 mills", Y5, estimate=est("$2,181,867", "$125"), src=F)
    c.levy("poland-lsd-pi", "Poland Local School District", sd("POLAND LOCAL SD (MAHONING)"), "Renewal", "Permanent improvements.", "1 mill", Y5, estimate=est("$403,667", "$22"), src=F)
    c.levy("west-branch-lsd", "West Branch Local School District", sd("WEST BRANCH LOCAL SD (MAHONING)"), "Additional", "General permanent improvement.", "1 mill", Y5, estimate=est("$441,471", "$35"), src=F)
    c.levy("fairfield-twp-roads", "Fairfield Township (Columbiana County)", c.p("COLUMBIANA CITY"), "Renewal", "Roads and bridges.", "1.6 mills", Y5, estimate=est("$388,340", "$25"), src=F,
           note="Voted on in the part of the City of Columbiana that lies in Mahoning County (Fairfield Township).")
    c.levy("perry-twp-police", "Perry Township (Columbiana County)", [], "Not stated", "Police department.", "1.5 mills", Y5, estimate=est("$222,295", "$53"), src=F,
           note="On the Mahoning Board's list, but the state voter file shows no Mahoning County voters in Perry Township.")
    c.levy("salem-rec", "City of Salem (Columbiana County)", [], "Renewal", "Recreational purposes.", "1 mill", Y5, estimate=est("$166,794", "$12"), src=F,
           note="On the Mahoning Board's list, but the state voter file shows no Mahoning County voters in the City of Salem.")
    c.issue("alliance-csd", "levy", "Alliance City School District", "Tax levy: buildings", sd("ALLIANCE CITY SD"), src=["columbiana-zero"],
            note="Not on the Mahoning Board's list. It is on the Columbiana Board's report, and the state voter file puts some Smith Township and Alliance City voters in Mahoning County in this school district. Check your sample ballot.")

    LQ = [
        ("yo-2d-lorenzinos", "Youngstown City", "YOUNGSTOWN CITY", "Youngstown 2-D", "Lorenzino's Bocce Club, LLC, 128 Jacob's Rd.", "Sunday sales."),
        ("yo-6h-gateway-weekly", "Youngstown City", "YOUNGSTOWN CITY", "Youngstown 6-H", "Gateway Gas Mart, 2732 Glenwood Ave.", "Weekly beer, wine and mixed beverages."),
        ("yo-6h-gateway-sunday", "Youngstown City", "YOUNGSTOWN CITY", "Youngstown 6-H", "Gateway Gas Mart, 2732 Glenwood Ave. (Sunday)", "Sunday wine and mixed beverages."),
        ("campbell-3b-12th", "Campbell City", "CAMPBELL CITY", "Campbell 3-B", "12th Street Party Shop, 223 12th Street", "Sunday sales."),
        ("aust-17-rulli", "Austintown Township", "AUSTINTOWN TWP", "Austintown 17", "Rulli Brothers, 431 Kirk Rd.", "Sunday sales."),
        ("board-25-rulli", "Boardman Township", "BOARDMAN TWP", "Boardman 25", "Rulli Brothers, 8025 South Ave.", "Sunday sales."),
        ("board-9-tobacco", "Boardman Township", "BOARDMAN TWP", "Boardman 9", "Tobacco City LLC, 112 Boardman Poland Rd.", "Weekly and Sunday sales."),
        ("board-9-singh", "Boardman Township", "BOARDMAN TWP", "Boardman 9", "Singh & 3 Brothers, 6607 Market St.", "Weekly and Sunday sales."),
        ("board-15-millionaire", "Boardman Township", "BOARDMAN TWP", "Boardman 15", "Millionaire Express, 5955 South Ave.", "Sunday sales."),
    ]
    for id, jur, raw, pct, biz, text in LQ:
        c.issue("liquor-" + id, "liquor", jur, f"Local liquor option: {biz}", c.p(raw), area=f"Precinct {pct}", text=text, src=F)
    return c
