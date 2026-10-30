from lib import County, NOTE_ORDER, NOTE_PLACES

SITE = "https://www.boe.ohio.gov/wyandot/"
NOTICE = "https://www.boe.ohio.gov/wyandot/c/upload/FWAB_11November46Day.pdf"
BALLOTS = "https://www.boe.ohio.gov/wyandot/election-info/ballots-general-election/"

# The SoS file's place columns are mostly empty in Wyandot: townships are known only by precinct name ("ANTRIM TS", "TS" = township),
# Carey Village by its precincts Carey A/B/C, Upper Sandusky City by Upper A to Upper F, and Nevada Village by its one precinct, whose
# TOWNSHIP column splits it into "NEVADA ANTRIM" and "NEVADA EDEN". Harpster, Kirby, Marseilles and Wharton villages do have VILLAGE
# values (Kirby spans the Jackson and Mifflin township precincts). Sycamore Village has its own precinct and sample ballot at the Board,
# but the voter file has no Sycamore Village precinct or VILLAGE value: its voters are inside "SYCAMORE TS".
TWPS = ["ANTRIM", "CRANE", "CRAWFORD", "EDEN", "JACKSON", "MARSEILLES", "MIFFLIN", "PITT", "RICHLAND", "RIDGE", "SALEM", "SYCAMORE", "TYMOCHTEE"]
RENAME = {f"{t} TS": f"{t.capitalize()} Township" for t in TWPS}
RENAME.update({f"CAREY {x}": "Carey Village" for x in "ABC"})
RENAME.update({f"UPPER {x}": "Upper Sandusky City" for x in "ABCDEF"})
RENAME.update({"NEVADA ANTRIM": "Nevada Village", "NEVADA EDEN": "Nevada Village"})


def build():
    c = County("wyandot", "Wyandot", "39175", rename=RENAME)
    c.src("wyandot-46day", "Wyandot County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election", NOTICE)
    c.src("wyandot-ballots", "Wyandot County Board of Elections: precinct sample ballots, November 3, 2026 General Election", BALLOTS)
    C = ["wyandot-46day", "wyandot-ballots"]; I = ["wyandot-ballots", "wyandot-46day"]
    c.links = [
        {"label": "Board of Elections", "url": SITE},
        {"label": "Election information", "url": "https://www.boe.ohio.gov/wyandot/election-info/"},
        {"label": "Sample ballots by precinct", "url": BALLOTS},
    ]
    c.results_links = [{"label": "Board of Elections", "url": SITE}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it, "
               "checked against the Board's 35 precinct sample ballots. Issue wording is from the sample ballots.",
               NOTE_ORDER, NOTE_PLACES,
               "Wyandot County's ballots do not number local issues (only statewide Issue 3 is numbered); see your sample ballot for the order of the issues.",
               "The state voter file does not separate Sycamore Village from Sycamore Township; Sycamore Village voters should use Sycamore Township here, "
               "but do not vote on the electric aggregation question (unincorporated areas only)."]
    P = c.p; SD = c.sd
    est = lambda total, per: f"{total} a year; {per} for each $100,000 of the county auditor's market value"

    # --- Federal, state legislative, appeals (the 5th Congressional, 87th House and 3rd Appeals districts cover the whole county;
    #     no State Senate race: the 26th District is not up in 2026; no Common Pleas race on the ballot) ---
    c.contest("congress-5", "U.S. House", "Representative to Congress", [("Bob Latta", "REP"), ("Brian A. Shaver", "DEM"), ("Michael J. Veloff", "LIB")],
              detail="5th District", src=C)
    c.contest("rep-87", "Ohio General Assembly", "State Representative", [("Lora Covrett", "DEM"), ("Jeffrey A. McClain", "REP"), ("Craig Swartz", "Nonparty")],
              detail="87th District", src=C)
    c.contest("appeals-3-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Mark C. Miller", "REP")],
              detail="3rd District · full term commencing February 9, 2027", src=C)

    # --- County offices (the notice lists the commissioner's three independents as "Independent") ---
    c.contest("commissioner", "County offices", "County Commissioner",
              [("Kenneth Beamer", "Nonparty"), ("Jon Hathaway", "Nonparty"), ("Russell L. Smith", "REP"), ("Jason S. Yeater", "Nonparty")],
              detail="Full term commencing January 1, 2027", src=C)
    c.contest("auditor", "County offices", "County Auditor", [("George Kitzler", "REP")], src=C)

    # --- Issues, in the notice's order ---
    # Jackson Township precincts: Jackson Township and Jackson Kirby Village (Kirby's Mifflin Township part does not vote on it).
    c.levy("jackson-twp-current", "Jackson Township", P("JACKSON TS", "KIRBY VILLAGE"), "Renewal", "Current expenses.", "1.5 mills",
           "5 years, commencing in 2027", "2028", estimate=est("$22,735", "$24"),
           area="Jackson Township (precincts Jackson Township and Jackson Kirby Village)", src=I)
    c.levy("marseilles-twp-current", "Marseilles Township", P("MARSEILLES TS", "MARSEILLES VILLAGE"), "Renewal", "Current expenses.", "2 mills",
           "5 years, commencing in 2026", "2027", estimate=est("$19,124", "$26"),
           area="Marseilles Township (including Marseilles Village)", src=I)
    c.levy("richland-twp-current", "Richland Township", P("RICHLAND TS", "WHARTON VILLAGE"), "Renewal", "Current expenses.", "1 mill",
           "5 years, commencing in 2027", "2028", estimate=est("$22,088", "$19"),
           area="Richland Township (including Wharton Village)", src=I)
    US = P("UPPER C")
    c.issue("liquor-upper-c-elie", "liquor", "City of Upper Sandusky", "Local liquor option: Elie Wine & Spirits (Sunday)", US, area="Upper Sandusky precinct Upper C",
            text="Shall the sale of beer, wine, mixed beverages and spirituous liquor be permitted for sale on Sunday, by Elie Wine & Spirits a D-6 liquor permit applicant, "
                 "holder of C-1, C-2, D-8 permit, who is engaged in the business of operating a liquor store at 117 E. Walker St. Upper Sandusky, OH 43351 in this precinct?", src=I)
    c.issue("liquor-upper-c-ten-ducks", "liquor", "City of Upper Sandusky", "Local liquor option: Ten Ducks Holding, Ltd (Sunday)", US, area="Upper Sandusky precinct Upper C",
            text="Shall the sale of wine and mixed beverages, and spirituous liquor be permitted for sale on Sunday by Ten Ducks Holding, Ltd an applicant for a D-6 liquor permit "
                 "who is engaged in the business of operating a bar and full-service restaurant at 124-132 N Sandusky Ave. Upper Sandusky, OH 43351 in this precinct?", src=I)
    # Same Board as seneca.py's "mhrs" (a separate 0.6-mill Wyandot County levy). The sample ballots' wording is used: the notice instead says "for the benefit of
    # Wyandot County" and names the "Mental Health and Recovery Services Board of Seneca, Sandusky and Wyandot Counties".
    c.levy("mhrs", "Wyandot County", "county", "Renewal",
           "Mental Health and Recovery Services Board of Seneca, Ottawa, Sandusky and Wyandot Counties (and/or its intended successor, the North Central Behavioral Health Board): "
           "operation of community addiction and mental health services providers, and alcohol and drug addiction and mental health facilities in Wyandot County.",
           "0.6 mill", "10 years, commencing in 2027", "2028", estimate=est("$361,454", "$13"),
           note="The sample ballot's wording reads \"a renewal of a tax for the benefit of Seneca County\" for facilities in Wyandot County; the Board's 46-day notice "
                "says \"for the benefit of Wyandot County\" and names the board as that of Seneca, Sandusky and Wyandot Counties.", src=I)
    c.issue("sales-tax", "question", "Wyandot County", "Sales and use tax: 0.5% continuation, 5 years, for the Sheriff's Department and Emergency Medical Services", "county",
            text="The Board of County Commissioners of Wyandot County proposes a continuation of a sales and use tax in the amount of 0.5% for the purpose of providing "
                 "additional revenue for the County's general fund for the operation of the Wyandot County Sheriff's Department and Emergency Medical Services for a period "
                 "of 5 years. Shall the resolution of the Wyandot county commissioners proposing a 0.5% sales and use tax be approved?", src=I)
    c.issue("upper-sandusky-charter-data-center", "question", "City of Upper Sandusky",
            "Charter amendment (Ordinance 85-14): Article XVII, Section 17.13, prohibition of construction of a data center", P("UPPER A"),
            area="Upper Sandusky precincts Upper A to Upper F",
            text="Shall the proposed charter amendment, Article XVII, Section 17.13: Prohibition of Construction of a Data Center, as reported by the charter commission "
                 "of the city of Upper Sandusky be adopted?", src=I)
    # Ballots: all three Antrim precincts, Eden Wyandot East Fire (Upper Sandusky and Wynford parts) and Nevada. Same district as crawford.py's issue-9.
    c.levy("wyandot-east-fire", "Wyandot East Fire District", P("ANTRIM TS", "EDEN TS", "NEVADA ANTRIM"), "Renewal",
           "Providing and maintaining fire protection services.", "2.5 mills", "5 years, commencing in 2026", "2027", estimate=est("$76,990", "$32"),
           area="Wyandot East Fire District (Antrim Township, Eden Township's Wyandot East Fire precincts and Nevada Village; also Tod Township in Crawford County)", src=I)
    # Same question as crawford.py's issue-6. The notice prints 1.74 percent; the sample ballots (and Crawford's issue) say 1.75 percent.
    c.issue("wynford-lsd-income-tax", "question", "Wynford Local School District (Crawford and Wyandot counties)",
            "School district income tax: additional 1.75%, 10 years, for current expenses", SD("WYNFORD LOCAL SD (CRAWFORD)"),
            area="Wynford Local School District, Wyandot County part (Antrim Wynford, Crane Wynford, Eden Wyandot East Fire Wynford, Nevada, Pitt Wynford)",
            text="Shall an annual income tax of 1.75 percent on the earned income of individuals residing in the school district be imposed by the Wynford Local School "
                 "District for 10 years, beginning January 1, 2027, for the purpose of current expenses?",
            note="The Board's 46-day notice prints the rate as 1.74 percent; the sample ballots say 1.75 percent.", src=I)
    # Same levy as marion.py's ridgedale-lsd and crawford.py's issue-5.
    c.levy("ridgedale-lsd", "Ridgedale Local School District (Marion, Crawford and Wyandot counties)", SD("RIDGEDALE LOCAL SD (MARION)"), "Renewal",
           "Current expenses (fixed sum of $575,034).", "2.44 mills (estimated average)", "5 years, commencing in 2027", "2028",
           estimate=est("$575,034", "$85"), area="Ridgedale Local School District, Wyandot County part (Antrim Ridgedale)",
           note="The county auditor certified the district's carry-over balance above the prior year's general fund expenditures as $0 (0% of those expenditures).", src=I)
    # The notice's precincts: "All unincorporated portions of the county" (every township precinct; not the village and city precincts).
    c.issue("electric-aggregation", "question", "Wyandot County (unincorporated area)", "Electric aggregation for the unincorporated area (opt-out)",
            P(*[f"{t} TS" for t in TWPS]), area="Unincorporated Wyandot County (all township precincts)",
            text="Shall Wyandot County have the authority to aggregate the retail electric loads located in the unincorporated areas of Wyandot County, and for that "
                 "purpose, enter into service agreements to facilitate for those loads the sale and purchase of electricity, such aggregation to occur automatically "
                 "except where any person elects to opt out?", src=I)
    return c
