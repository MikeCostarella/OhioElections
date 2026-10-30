from lib import County, NOTE_ORDER, NOTE_PLACES

SITE = "https://www.boe.ohio.gov/adams/"
NOTICE = "https://www.boe.ohio.gov/adams/c/upload/FWAB_11November46Day.pdf"
BALLOTS = "https://lookup.boe.ohio.gov/vtrapp/adams/ballotlist.aspx"

APPEALS_4 = "4th District"


def build():
    # Raw SoS names ("BRATTON TOWNSHIP", "WEST UNION VILLAGE") already display correctly; no renames needed.
    # Board precincts: Locust Grove (02) is in Franklin Township; Manchester United Township (07) covers Manchester Village and Township;
    # West Union A/B (18, 19) are West Union Village; Tiffin East/West (20, 21) are Tiffin Township; Seaman Village is precinct 10 (in Scott Township);
    # Winchester Village is precinct 13 (in Winchester Township).
    c = County("adams", "Adams", "39001")
    c.src("adams-46day", "Adams County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election (revised October 6, 2026)", NOTICE)
    c.src("adams-ballots", "Adams County Board of Elections: precinct sample ballots, November 3, 2026 General Election (election data updated October 12, 2026)", BALLOTS)
    S = ["adams-46day", "adams-ballots"]
    B = ["adams-ballots", "adams-46day"]
    c.links = [
        {"label": "Board of Elections", "url": SITE},
        {"label": "Federal write-in absentee ballot notices", "url": "https://www.boe.ohio.gov/adams/election-info/federal-write-in-absentee-ballots/"},
        {"label": "Sample ballots by precinct", "url": BALLOTS},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://www.boe.ohio.gov/adams/election-info/election-results/"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it, "
               "checked against the Board's precinct sample ballots (which give the full ballot wording; where the two differ, the ballots are followed).",
               NOTE_ORDER, NOTE_PLACES,
               "The Board's notice and sample ballots do not give local issue numbers; see your sample ballot for the order.",
               "Court of Appeals: Peter B. Abele (Republican) is still printed on the main ballot for the 4th District seat; the Board's notice marks him "
               "deceased (no longer valid), and a supplemental 4th District Court of Appeals ballot lists Jayme Hartley Fountain (Republican) and "
               "Todd L. Grace (Democratic). The supplemental ballot is shown here."]
    P = c.p; D = c.district
    est = lambda a, b: f"{a} a year; {b} for each $100,000 of market value"

    # --- Federal, state legislative, appeals (every precinct is in the 2nd Congressional, 90th House and 4th Appeals districts; Senate District 14 is not up) ---
    c.contest("congress-2", "U.S. House", "Representative to Congress", [("Jen Mazzuckelli", "DEM"), ("David J. Taylor", "REP")],
              detail="2nd District", places=D("cong", 2), src=S)
    c.contest("rep-90", "Ohio General Assembly", "State Representative", [("Collin Docterman", "DEM"), ("Justin Pizzulli", "REP")],
              detail="90th District", places=D("rep", 90), src=S)
    # The notice (revised 10/6/2026) lists "Peter B. Abele (Deceased - No longer valid)", Grace (Dem) and Fountain (Rep); the main sample ballot
    # still prints Abele and a supplemental ballot lists Fountain and Grace, as in Ross, Scioto, Highland and Pike.
    c.contest("appeals-4-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Jayme Hartley Fountain", "REP"), ("Todd L. Grace", "DEM")],
              detail=APPEALS_4 + " · full term commencing February 9, 2027", src=B)

    # --- County ---
    c.contest("commissioner", "County offices", "County Commissioner",
              [("Kelly Jones", "REP"), ("Helen L. Newman", "Nonparty"), ("Troy D. Thatcher", "Nonparty"), ("Travis Wilson", "Nonparty")],
              detail="Full term commencing January 1, 2027", src=S)
    c.contest("auditor", "County offices", "County Auditor", [("David Gifford", "REP"), ("Clayton Osborne", "Nonparty")],
              detail="Full term commencing March 8, 2027", src=S)
    c.contest("prosecutor", "County offices", "Prosecuting Attorney", [("Ariana D. Norris", "REP"), ("David Osborne, Jr.", "Nonparty")],
              detail="Unexpired term ending December 31, 2028", src=S)
    NP = " · no party label on the ballot"
    # The notice says "Full 2 Year Term Commencing 02/09/2027"; the sample ballots say only "Full term commencing 2-9-2027".
    c.contest("cp-general", "Court of Common Pleas", "Judge of the Court of Common Pleas", ["Barbara Moore Holt", "Lisa Ann Rothwell"],
              detail="Full term commencing February 9, 2027" + NP, src=B)

    # --- Countywide issues ---
    c.levy("adams-ems", "Adams County", "county", "Additional", "Continued operation of Adams County Emergency Medical Services.", "3.5 mills",
           "5 years, commencing in 2026", "2027", est("$2,874,966", "$123"), src=S)
    c.levy("adams-children-services", "Adams County", "county", "Additional",
           "Continued operation of Adams County Children Services and the care and placement of children including Wilson Children's Home.", "1.5 mills",
           "5 years, commencing in 2026", "2027", est("$1,232,128", "$53"), src=S)

    # --- Village and township issues (in the notice's order) ---
    c.levy("peebles-police", "Village of Peebles", P("PEEBLES VILLAGE"), "Renewal", "Police operating expenses.", "2.8 mills",
           "5 years, commencing in 2027", "2028", est("$52,603", "$49"), area="Peebles Village (precinct 03)", src=S)
    c.levy("seaman-streets", "Village of Seaman", P("SEAMAN VILLAGE"), "Renewal", "Street improvements.", "2 mills",
           "5 years, commencing in 2026", "2027", est("$44,384", "$39"), area="Seaman Village (precinct 10)", src=S)
    c.levy("winchester-police", "Village of Winchester", P("WINCHESTER VILLAGE"), "Additional", "Police protection.", "3.5 mills",
           "5 years, commencing in 2026", "2027", est("$74,835", "$123"), area="Winchester Village (precinct 13)", src=S)
    c.levy("bratton-twp-current", "Township of Bratton", P("BRATTON TOWNSHIP"), "Additional", "Current expenses.", "1 mill",
           "5 years, commencing in 2026", "2027", est("$37,489", "$35"), area="Bratton Township (precincts 01/1 and 01/2)", src=S)
    c.levy("liberty-twp-cemeteries", "Township of Liberty", P("LIBERTY TOWNSHIP"), "Renewal", "Maintaining and operating cemeteries.", "0.9 mill",
           "5 years, commencing in 2027", "2028", est("$29,375", "$17"), area="Liberty Township (precincts 17/1 and 17/2)", src=S)
    ZONING = ("Shall the zoning plan for the unincorporated area of the Township of {t} as adopted by the Township of {t} be approved? "
              "(A resolution enacted under Section 519 of the Ohio Revised Code, titled \"{t} Township Zoning Resolution\", governing the unincorporated area of "
              "{t} Township, Adams County, Ohio, to preserve the rural and agricultural character of the Township, protect public health, safety, and general welfare, "
              "allow reasonable use of property with minimal unnecessary regulation, provide a predictable process for review of higher-impact development, "
              "ensure that uses with potentially significant impacts are evaluated and reasonably mitigated, and to promote orderly and compatible land use "
              "consistent with Township infrastructure and services; for the purpose of protecting agricultural, residential, and small-scale uses; preventing "
              "unreasonable burdens on roads, infrastructure, and public services; providing uniform and objective standards for land use review; and to carry out "
              "zoning authority in a manner consistent with Ohio law.)")
    c.issue("monroe-twp-zoning", "question", "Township of Monroe", "Proposed zoning plan for the unincorporated area of Monroe Township", P("MONROE TOWNSHIP"),
            area="Monroe Township unincorporated area (precincts 08/1 and 08/2)", text=ZONING.format(t="Monroe"),
            note="Voting FOR approves the township's zoning resolution; voting AGAINST rejects it.", src=S)
    c.levy("oliver-twp-roads", "Township of Oliver", P("OLIVER TOWNSHIP"), "Additional", "Road repairs and maintenance.", "2 mills",
           "5 years, commencing in 2026", "2027", est("$84,115", "$70"), area="Oliver Township (precinct 05)", src=S)
    # Precincts 10/1 (Seaman Village), 11/1 and 11/2 (Scott Township).
    SCOTT = P("SCOTT TOWNSHIP", "SEAMAN VILLAGE")
    SCOTT_AREA = "Scott Township, including Seaman Village (precincts 10, 11/1 and 11/2)"
    # The notice says "1 YEAR"; every Scott and Seaman sample ballot says 5 years, commencing in 2026.
    c.levy("scott-twp-ems", "Township of Scott", SCOTT, "Additional",
           "Providing and maintaining emergency medical services, including ambulance service, emergency service, or both, and to maintain EMS apparatus, "
           "appliances, buildings, sites for apparatus, EMS vehicles, and related equipment, whether by contract or otherwise.", "3.5 mills",
           "5 years, commencing in 2026", "2027", est("$259,477", "$123"), area=SCOTT_AREA, src=B)
    c.levy("scott-twp-fire", "Township of Scott", SCOTT, "Renewal",
           "Providing and maintaining fire apparatus and appliances of the volunteer fire department.", "1.5 mills",
           "5 years, commencing in 2026", "2027", est("$54,225", "$13"), area=SCOTT_AREA, src=S)
    c.issue("sprigg-twp-zoning", "question", "Township of Sprigg", "Proposed zoning plan for the unincorporated area of Sprigg Township", P("SPRIGG TOWNSHIP"),
            area="Sprigg Township unincorporated area (precinct 09)", text=ZONING.format(t="Sprigg"),
            note="Voting FOR approves the township's zoning resolution; voting AGAINST rejects it.", src=S)
    c.levy("wayne-twp-fire", "Township of Wayne", P("WAYNE TOWNSHIP"), "Renewal",
           "Maintaining and operating fire apparatus, appliances, buildings, or sites therefore.", "0.8 mill",
           "5 years, commencing in 2027", "2028", est("$15,618", "$12"), area="Wayne Township (precinct 12)", src=S)
    # Precincts 13/1 (Winchester Village) and 14/1 (Winchester Township).
    WIN = P("WINCHESTER TOWNSHIP", "WINCHESTER VILLAGE")
    WIN_AREA = "Winchester Township, including Winchester Village (precincts 13 and 14)"
    c.levy("winchester-twp-cemeteries", "Township of Winchester", WIN, "Renewal",
           "Care, supervision, repair and improvement of township cemeteries.", "0.4 mill",
           "5 years, commencing in 2027", "2028", est("$12,356", "$6"), area=WIN_AREA, src=S)
    # The notice says "the Winchester Union Cemetery District"; the sample ballots say "the Winchester Union Cemetery".
    c.levy("winchester-union-cemetery", "Township of Winchester", WIN, "Renewal",
           "Maintaining and operating the Winchester Union Cemetery.", "1 mill",
           "5 years, commencing in 2027", "2028", est("$29,887", "$14"), area=WIN_AREA, src=B)
    # The notice's precinct cell reads "PEEBLES VILLAGE 09 - All Splits" (09 is Sprigg Township); only the Peebles Village (03) sample ballot carries it.
    c.issue("peebles-liquor-local-jacks", "liquor", "Peebles Village", "Local liquor option: Local Jacks (Sunday)", P("PEEBLES VILLAGE"),
            area="Precinct Peebles Village (03)",
            text="Shall the sale of beer, wine, mixed beverages and spirituous liquor be permitted for sale on Sunday by Local Jacks LLC dba Local Jacks "
                 "an applicant for a D-6 liquor permit and holder of a D-1, D-2, D-3 liquor permits who is engaged in the business of operating a restaurant "
                 "at 122 S. Main St, Peebles, OH 45660 in this precinct?", src=B)
    return c
