from lib import County, NOTE_ORDER, NOTE_PLACES, NOTE_UNKNOWN

SITE = "https://www.boe.ohio.gov/knox/"
NOTICE = "https://www.boe.ohio.gov/knox/c/upload/FWAB_11November46Day.pdf"
BALLOTS = "https://lookup.boe.ohio.gov/vtrapp/knox/ballotlist.aspx"


def build():
    # The SoS file names the Brinkhaven precinct's village "GANN VILLAGE" (its old name); the Board calls it Brinkhaven.
    c = County("knox", "Knox", "39083", rename={"GANN VILLAGE": "Brinkhaven Village"})
    c.src("knox-46day", "Knox County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election (revised 10/16/2026)", NOTICE)
    c.src("knox-ballots", "Knox County Board of Elections: precinct sample ballots, November 3, 2026 General Election", BALLOTS)
    C = ["knox-46day"]; I = ["knox-ballots", "knox-46day"]
    c.links = [
        {"label": "Board of Elections", "url": SITE},
        {"label": "Election information", "url": "https://www.boe.ohio.gov/knox/election-info/"},
        {"label": "Sample ballots by precinct", "url": BALLOTS},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://www.boe.ohio.gov/knox/election-info/election-results/"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it; "
               "issue wording is from the Board's precinct sample ballots.",
               NOTE_ORDER, NOTE_PLACES, NOTE_UNKNOWN,
               "The Board's notice and sample ballots do not print local issue numbers; see your sample ballot for the order of the issues."]
    P = c.p; D = c.district; SD = c.sd
    MV = P("MOUNT VERNON CITY")

    # --- Federal, state legislative, appeals (the 12th Congressional, 19th Senate and 5th Appeals districts cover the whole county) ---
    c.contest("congress-12", "U.S. House", "Representative to Congress", [("Troy Balderson", "REP"), ("Jerrad Christian", "DEM")], detail="12th District", src=C)
    c.contest("senate-19", "Ohio General Assembly", "State Senator", [("Scott Charland", "DEM"), ("Ryan Rivers", "REP")], detail="19th District", src=C)
    # The notice puts precinct Mount Vernon 1-B split 2 (Mount Vernon/Clinton Township) in the 61st District; the voter file has no Mount Vernon voters there.
    c.contest("rep-61", "Ohio General Assembly", "State Representative", [("Vince McGrail", "DEM"), ("Shawn Stevens", "REP")], detail="61st District",
              places=sorted(set(D("rep", 61) + MV)), src=C)
    c.contest("rep-98", "Ohio General Assembly", "State Representative", [("Scott Grund", "DEM"), ("Mark Hiner", "REP")], detail="98th District", places=D("rep", 98), src=C)
    c.contest("appeals-5", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Matthew George", "REP")], detail="5th District · term commencing February 9, 2027", src=C)

    # --- County offices ---
    c.contest("commissioner", "County offices", "County Commissioner", [("Bill Pursel", "REP"), ("Chuck Rogers", "DEM")], detail="4-year term commencing January 1, 2027", src=C)
    c.contest("auditor", "County offices", "County Auditor", [("Sarah Thorne", "REP")], detail="4-year term commencing March 7, 2027", src=C)
    NP = " · no party label on the ballot"
    c.contest("cp-probate-juvenile", "Court of Common Pleas", "Judge of the Court of Common Pleas, Probate/Juvenile Division", ["Jay Walter Nixon"],
              detail="6-year term commencing February 9, 2027" + NP, src=C)

    # --- Issues (unnumbered in the Board's documents; listed in the notice's order) ---
    c.levy("knox-senior-services", "Knox County", "county", "Renewal", "Providing or maintaining senior citizens services or facilities for Knox County senior citizens.",
           "0.79 mill", "5 years, commencing in 2027", "2028", estimate="$1,155,031 a year; $28 per $100,000 of market value", area="Knox County (all precincts)", src=I)

    c.issue("brinkhaven-council", "question", "Village of Brinkhaven", "Ordinance: reduce Village Council from six members to five", P("GANN VILLAGE"), area="Brinkhaven precinct",
            text="Shall the number of members of the Village Council of the Village of Brinkhaven, Ohio, be reduced from six (6) members to five (5) members?", src=I)

    CB = P("CENTERBURG VILLAGE")
    for kind, what in [("electric", "electric customers"), ("gas", "natural gas customers")]:
        noun = "electricity" if kind == "electric" else "natural gas"
        c.issue(f"centerburg-{kind}-aggregation", "question", "Village of Centerburg", f"{kind.capitalize()} aggregation", CB, area="Centerburg precinct, splits 1 and 2 (village part)",
                text=f"Shall the Village of Centerburg have the authority to aggregate the retail {what} located in the Village, and for that purpose, enter into services agreements "
                     f"to facilitate for those customers the sale and purchase of {noun}, conversion to the aggregation program will occur automatically unless the customers choose to opt out of the program?",
                src=I)

    # The notice says "parks and recreational purposes"; the ballot says "park maintenance".
    c.levy("danville-parks", "Village of Danville", P("DANVILLE VILLAGE"), "Renewal", "Park maintenance.", "1 mill", "5 years, commencing in 2027", "2028",
           estimate="$13,501 a year; $35 per $100,000 of market value", area="Danville precinct, splits 1 and 2 (village part)", src=I)

    L = [
        ("berlin-twp-roads", "Berlin Township", ["BERLIN TOWNSHIP"], "Renewal", "General construction, reconstruction, resurfacing and repair of streets, roads and bridges.", "2 mills",
         "4 years, commencing in 2027", "2028", "$95,026 a year; $70 per $100,000 of market value", "Berlin precinct"),
        ("liberty-twp-cemeteries", "Liberty Township", ["LIBERTY TOWNSHIP"], "Renewal", "Maintaining and operating cemeteries.", "0.6 mill",
         "5 years, commencing in 2027", "2028", "$27,519 a year; $21 per $100,000 of market value", "Liberty A, Liberty B (splits 1 and 2)"),
        # Monroe B and Mount Vernon 3-C split 2 (the Mount Vernon part in Monroe Township) vote on it.
        ("monroe-twp-fire", "Monroe Township", ["MONROE TOWNSHIP", "MOUNT VERNON CITY"], "Renewal and increase",
         "Fire protection and emergency medical services (renewal of 3 mills and an increase of 2 mills).", "5 mills",
         "5 years, commencing in 2026", "2027", "$398,243 a year; $175 per $100,000 of market value", "Monroe A and Monroe B (splits 1 and 2 each), Mount Vernon 3-C split 2"),
        ("pike-twp-roads", "Pike Township", ["PIKE TOWNSHIP"], "Renewal", "Construction, reconstruction, general repairs and maintenance of roads.", "2 mills",
         "5 years, commencing in 2027", "2028", "$90,771 a year; $70 per $100,000 of market value", "Pike precinct, splits 1–3"),
        # Mount Vernon 1-C split 3 is the Mount Vernon part in Pleasant Township; the voter file puts no Mount Vernon voters in Pleasant Township.
        ("pleasant-twp-roads", "Pleasant Township", ["PLEASANT TOWNSHIP", "MOUNT VERNON CITY"], "Renewal",
         "General construction, reconstruction, resurfacing, maintenance and repair of streets, roads and bridges.", "2 mills",
         "5 years, commencing in 2027", "2028", "$119,388 a year; $70 per $100,000 of market value", "Pleasant A, Pleasant B, Mount Vernon 1-C split 3"),
    ]
    for id, jur, raws, t, purpose, mills, term, fd, est, area in L:
        c.levy(id, jur, P(*raws), t, purpose, mills, term, fd, estimate=est, area=area, src=I)

    LP = SD("LOUDONVILLE-PERRYSVILLE EX VILL SD (ASHLAND)")
    LP_AREA = "Brown precinct split 4, Jefferson precinct split 2"
    c.issue("loudonville-perrysville-bond-income-tax", "levy", "Loudonville-Perrysville Exempted Village School District (Ashland, Knox and Richland counties)",
            "School district income tax (0.25%, 30 years) and bond issue ($16,400,000)", LP, area=LP_AREA,
            levy={"type": "Income tax and bond issue", "purpose": "Income tax for current expenses; bonds for constructing, renovating, repairing, expanding, furnishing and equipping school facilities and improving their sites.",
                  "mills": "2.85 mills (bond, estimated average)", "term": "Income tax 30 years from January 1, 2027; bonds up to 37 years",
                  "estimate": "$16,400,000 principal; $100 for each $100,000 of market value (bond)"},
            text="Shall Loudonville-Perrysville Exempted Village School District be authorized to do both of the following: (1) Impose an annual income tax of 0.25% on the school district "
                 "income of individuals, for a period of 30 years, beginning January 1, 2027, for the purpose of current expenses? (2) Issue bonds for the purpose of constructing school "
                 "facilities, renovating, repairing, expanding, improving, and constructing additions to school facilities; furnishing and equipping; and improving the sites thereof the same "
                 "in the principal amount of $16,400,000, to be repaid annually over a maximum period of 37 years, and levy a property tax outside the ten-mill limitation estimated by the "
                 "county auditor to average over the bond repayment period 2.85 mills for each $1 of taxable value, which amounts to $100 for each $100,000 of the county auditor's market "
                 "value, to pay the annual debt charges on the bonds, and to pay debt charges on any notes issued in anticipation of those bonds?", src=I)
    # The notice lists this levy under the school district ("current expenses"); the ballot says it is for the Loudonville Public Library (as in richland.py).
    c.levy("loudonville-library", "Loudonville Public Library (Ashland, Knox and Richland counties)", LP, "Renewal", "Current expenses.", "0.8 mill", "5 years, commencing in 2027", "2028",
           estimate="$178,719 a year; $19 per $100,000 of market value", area=LP_AREA, src=I)

    c.issue("mount-vernon-csd-income-tax", "question", "Mount Vernon City School District", "School district income tax: additional 1% on earned income, 30 years, for current expenses",
            SD("MOUNT VERNON CITY SD"), area="Mount Vernon City School District (all Mount Vernon precincts and parts of Brown, Clinton, College, Gambier, Harrison, Howard, Liberty, Miller, Monroe, Morgan, Morris, Pike and Pleasant)",
            text="Shall an annual income tax of one percent (1.00%) on the earned income of individuals residing in the school district be imposed by Mount Vernon City School District, "
                 "for 30 years, beginning January 1, 2027, for the purpose of current expenses?", src=I)

    # Precincts Clay-Martinsburg (all splits) and Jackson; the fire district is not in the voter file, so it is placed from the notice's precinct list.
    c.levy("bladensburg-fire", "Bladensburg Fire District", P("CLAY TOWNSHIP", "MARTINSBURG VILLAGE", "JACKSON TOWNSHIP"), "Additional",
           "Fire apparatus, equipment and buildings, firefighting and emergency medical service personnel, ambulance equipment and services, and related costs.",
           "6 mills", "Continuing period of time, commencing in 2026", "2027", estimate="$562,293 a year; $210 per $100,000 of market value",
           area="Clay-Martinsburg precinct (splits 1–3) and Jackson precinct", src=I)

    # --- Local liquor options ---
    c.issue("liquor-mt-vernon-duchess", "liquor", "City of Mount Vernon", "Local liquor option: Mt. Vernon Duchess (Sunday)", MV, area="Mount Vernon precinct 3-A",
            text="Sunday sale of wine and mixed beverages, off-premise sales, by Englefield, Inc. dba Mt. Vernon Duchess (D-6 permit applicant), a carryout / grocery store at 814 Coshocton Ave., Mount Vernon.", src=I)
    c.issue("liquor-centerburg-amvets", "liquor", "Village of Centerburg", "Local liquor option: Amvets Post 0059", CB, area="Centerburg precinct (all splits)",
            text="Sale of beer, wine and mixed beverages, and spirituous liquor by Amvets Post 0059, a D-4 permit holder engaged in serving food and beverages, at 3894 Columbus Rd., Centerburg.", src=I)
    return c
