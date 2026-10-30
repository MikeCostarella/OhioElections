from lib import County, NOTE_ORDER, NOTE_PLACES

NOTICE = "https://www.boe.ohio.gov/medina/c/upload/FWAB_11November46Day.pdf"

def build():
    c = County("medina", "Medina", "39103")
    c.src("medina-46day", "Medina County Board of Elections: 46-day election notice, November 3, 2026 General Election (revised 9/18/2026)", NOTICE)
    S = ["medina-46day"]
    c.links = [
        {"label": "Board of Elections", "url": "https://www.boe.ohio.gov/medina/"},
        {"label": "Sample ballots by precinct", "url": "https://lookup.boe.ohio.gov/vtrapp/medina/ballotlist.aspx"},
    ]
    c.results_links = [{"label": "Board of Elections", "url": "https://www.boe.ohio.gov/medina/"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it. "
               "Issue wording is the notice's summary; the full wording is on the sample ballot.", NOTE_ORDER, NOTE_PLACES]
    P = c.p

    c.contest("congress-7", "U.S. House", "Representative to Congress", [("Brian Poindexter", "DEM"), ("Max Miller", "REP")], detail="7th District", src=S)
    c.contest("rep-66", "Ohio General Assembly", "State Representative", [("Chris Nardo", "DEM"), ("Justin P. Peroli", "LIB"), ("Sean M. Hutson", "REP")], detail="66th District", places=c.district("rep", 66), src=S)
    c.contest("rep-67", "Ohio General Assembly", "State Representative", [("Heather L. Sample", "DEM"), ("Melanie Miller", "REP")], detail="67th District", places=c.district("rep", 67), src=S)
    c.contest("appeals-9-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Betty Sutton", "DEM"), ("Cynthia Curtin", "REP")], detail="9th District · full term commencing February 9, 2027", src=S)
    c.contest("appeals-9-0210", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Tavia Galonski", "DEM"), ("Nathan Manning", "REP")], detail="9th District · unexpired term ending February 9, 2029", src=S)
    c.contest("commissioner", "County offices", "County Commissioner", [("Cheryl Minichiello", "DEM"), ("Julie A. McNabb", "REP")], detail="Full term commencing January 1, 2027", src=S)
    c.contest("recorder", "County offices", "County Recorder", [("Bradford Scott Quade", "DEM"), ("Sharon A. Ray", "REP")], detail="Unexpired term ending December 31, 2028", src=S)
    c.contest("auditor", "County offices", "County Auditor", [("Carol Brenstuhl", "DEM"), ("Rick Dumperth", "REP")], detail="Full term commencing March 8, 2027", src=S)
    NP = " · no party label on the ballot"
    c.contest("cp-gen", "Court of Common Pleas", "Judge of the Court of Common Pleas, General Division", ["Ben Fuchs", "Matthew K. Razavi"], detail="Full term commencing January 1, 2027" + NP, src=S)
    c.contest("cp-juv-probate", "Court of Common Pleas", "Judge of the Court of Common Pleas, Juvenile/Probate Division", ["Mike Conway", "Kevin W. Dunn"], detail="Full term commencing February 9, 2027" + NP, src=S)

    c.issue("medina-sidewalks", "question", "City of Medina", "Amendment to Sections 161.01, 161.03(A) and 162.013(A) of the Codified Ordinances: sidewalks in the 0.25% income tax allocation",
            P("MEDINA CITY"), area="Medina City wards 1–4, plus splits 080/2-LFTD and 118/2-YKTA",
            text="An amendment to Sections 161.01, 161.03(A), and 162.013(A) of the Codified Ordinances of the City of Medina to include the installation, maintenance, repair and/or replacement of sidewalks as a permitted expense within the 0.25% income tax allocation that is currently restricted for improvements for streets, storm water, and utility improvements?", src=S)
    RIT = [
        ("Section 9.05", "Eliminate outdated language regarding the civil service status of employees and add a new section allowing for the removal of a member of City Council by other members of City Council for bad behavior, criminal conduct, or absenteeism."),
        ("Articles III, IV, VII, XII and XIII", "Change the date of the organizational meeting, change the date that elected officials take office, and change the deadline that nominating petitions for elective offices in the municipality must be submitted to the Board of Elections."),
        ("Section 3.06", "Allow City Council to hold executive sessions for any reason allowable by Ohio Revised Code."),
        ("Section 4.03", "Clarify language that the Mayor, when invited, is only an attendee and does not preside over executive sessions of City Council."),
        ("Section 4.05", "Clarify the procedure by which a member of City Council is nominated to and can become Mayor in the event the office of Mayor becomes vacant."),
        ("Section 5.01", "Require an annual review of the Municipal Manager by City Council."),
        ("Articles VI and IX", "Change language to reflect that the Fire and EMS departments have merged into one department."),
        ("Section 6.05", "Require that the Law Director be an attorney-in-fact in good standing with the State Bar Association and oversee representation of the City in all cases as well as provide direct representation."),
        ("Section 9.01", "Update old language concerning the establishment of a Civil Service Commission if Rittman became a city, as Rittman is already a city."),
        ("Section 9.02", "Change the term an individual serves on the Civil Service Commission from six (6) years to three (3) years."),
        ("Section 11.01", "Add a member of City Council to serve on the Cemetery Board."),
        ("Section 12.02", "Change the deadline for submitting the budget to City Council from January 1st to December 31st and clarify language."),
        ("Section 12.06", "Require an annual review of the Finance Director by City Council."),
        ("Section 13.04", "Reduce the residency requirement to be eligible to be an elected officer of the municipality from two (2) years to one (1) year."),
        ("Section 16.01", "Amend the schedule in which the Charter Review Commission convenes to intentionally misalign it with the election of new members of City Council."),
    ]
    for i, (sec, text) in enumerate(RIT, 1):
        c.issue(f"rittman-charter-{i}", "question", "City of Rittman (Wayne and Medina counties)", f"Proposed charter amendment #{i}: {sec}", P("RITTMAN CITY"),
                area="Precinct splits 068/2-GUTA and 068/3-GUTA", text=text, src=S)

    WAD = P("WADSWORTH CITY")
    c.levy("wadsworth-ems", "City of Wadsworth", WAD, "Renewal and increase", "Ambulance and emergency medical services (renew 3 mills, increase 1 mill).", "4 mills", "5 years, commencing in 2027", "2028",
           area="Wadsworth City wards 1–4, plus splits 109/2-SHTD, 113/3-WDTB, 114/2-WDTC, 114/3-WDTC", src=S)
    c.levy("wadsworth-fire", "City of Wadsworth", WAD, "Renewal and decrease", "Fire apparatus, equipment, buildings, water supply and fire-alarm communications (renew 1.5 mills, reduce 1 mill).", "0.5 mill", "5 years, commencing in 2026", "2027",
           area="Wadsworth City wards 1–4, plus splits 109/2-SHTD, 113/3-WDTB, 114/2-WDTC, 114/3-WDTC", src=S)
    L = [
        ("lodi-current", "Village of Lodi", ["LODI VILLAGE"], "Renewal", "Current operating expenses.", "3 mills", "5 years, commencing in 2026", "2027", None),
        ("canaan-fire", "Canaan Township (Wayne and Medina counties)", ["Westfield TWP"], "Additional", "Fire and emergency medical services.", "2.5 mills", "3 years, commencing in 2026", "2027", "One precinct split in Medina County: 116/2-WSTA"),
        ("chatham-cemeteries", "Chatham Township", ["Chatham TWP"], "Renewal", "Maintaining and operating cemeteries.", "0.5 mill", "5 years, commencing in 2027", "2028", None),
        ("guilford-ems", "Guilford Township", ["Guilford TWP", "SEVILLE VILLAGE"], "Renewal", "Ambulance service and medical emergency service.", "2.5 mills", "5 years, commencing in 2026", "2027", "Guilford Township A and B, Seville Village A and B"),
        ("harrisville-cemeteries", "Harrisville Township", ["Harrisville TWP", "LODI VILLAGE"], "Additional", "Maintaining and operating cemeteries.", "0.75 mill", "5 years, commencing in 2026", "2027", "Harrisville Township A, Lodi Village A and B"),
        ("hinckley-police", "Hinckley Township", ["Hinckley TWP"], "Additional", "Police department vehicles, equipment, buildings and personnel, police protection contracts, and related costs.", "2 mills", "5 years, commencing in 2026", "2027", None),
        ("litchfield-roads", "Litchfield Township", ["Litchfield TWP"], "Renewal", "Road and bridge construction and the repair of township roads.", "1 mill", "5 years, commencing in 2026", "2027", None),
        ("litchfield-fire", "Litchfield Township", ["Litchfield TWP"], "Additional", "Fire and EMS.", "3 mills", "5 years, commencing in 2026", "2027", None),
        ("liverpool-fire-add", "Liverpool Township", ["Liverpool TWP"], "Additional", "Fire and EMS.", "1.5 mills", "5 years, commencing in 2026", "2027", None),
        ("liverpool-fire-ren", "Liverpool Township", ["Liverpool TWP"], "Renewal", "Fire and EMS.", "2 mills", "5 years, commencing in 2026", "2027", None),
        ("sharon-fire", "Sharon Township", ["Sharon TWP"], "Renewal", "Fire and EMS.", "1.1 mills", "5 years, commencing in 2026", "2027", None),
        ("westfield-jfd", "Westfield Joint Fire District", ["Westfield TWP", "WESTFIELD CENTER VILLAGE"], "Additional", "Fire and emergency medical services.", "3.1 mills", "5 years, commencing in 2026", "2027", "Westfield Center Village; Westfield Township A and B"),
        ("wayne-jvsd", "Wayne County Joint Vocational School District", ["Guilford TWP", "Harrisville TWP", "Wadsworth TWP", "Westfield TWP"], "Renewal", "General permanent improvements.", "0.5 mill", "5 years, commencing in 2027", "2028", "Precinct splits 068/3-GUTA, 070/2-HRTA, 113/1-WDTB, 116/2-WSTA, 116/3-WSTA"),
    ]
    for id, jur, raws, t, purpose, mills, term, fd, area in L:
        c.levy(id, jur, P(*raws), t, purpose, mills, term, fd, area=area, src=S)
    c.issue("york-bond", "levy", "York Township", "Bond issue: fire station addition", P("York TWP"),
            text="Bond issue, principal $5,050,000, estimated 1 mill, 29 years, commencing 2026, first due 2027, for constructing a fire station addition and related improvements; furnishing and equipping the same; and improving the sites thereof.", src=S)
    c.issue("wadsworth-csd-income", "question", "Wadsworth City School District", "School district income tax: 1% additional, 5 years, for current expenses", c.sd("WADSWORTH CITY SD"),
            area="Wadsworth City School District", text="Income tax (additional), 1%, 5 years, commencing January 1, 2027, for current expenses.", src=S)
    c.issue("liquor-meijer", "liquor", "City of Medina", "Local liquor option: Meijer Express #335 (Sunday)", P("MEDINA CITY"), area="Medina City precinct 1-C",
            text="Sunday sale of wine and mixed beverages, off-premise sales, by Meijer Stores Limited Partnership (dba Express #335), NW corner of Pearl Road and the Meijer store access drive, Medina.", src=S)
    c.issue("liquor-casa-conrique", "liquor", "City of Medina", "Local liquor option: Casa Conrique (Sunday)", P("MEDINA CITY"), area="Medina City precinct 2-A",
            text="Sunday sale of wine and mixed beverages and spirituous liquor, on/off-premise sales, by Conrique Valadez, LLC (dba Casa Conrique), 111 W. Liberty Street, Medina.", src=S)
    return c
