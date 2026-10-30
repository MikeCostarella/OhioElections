from lib import County, NOTE_ORDER, NOTE_PLACES

NOTICE = "https://www.boe.ohio.gov/darke/c/upload/FWAB_11November46Day.pdf"

def build():
    # Raw names display correctly ("TWIN  TWP" -> "Twin Township", "UNION CITY VILLAGE" -> "Union City Village"); no renames needed.
    # Bradford Village is shared with Miami County (miami.py); nothing on Darke's ballot is Bradford-only.
    c = County("darke", "Darke", "39037")
    c.src("darke-46day", "Darke County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election", NOTICE)
    S = ["darke-46day"]
    c.links = [
        {"label": "Board of Elections", "url": "https://www.boe.ohio.gov/darke/"},
        {"label": "Election info", "url": "https://www.boe.ohio.gov/darke/election-info/"},
        {"label": "Sample ballots by precinct", "url": "https://lookup.boe.ohio.gov/vtrapp/darke/ballotlist.aspx"},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://www.boe.ohio.gov/darke/election-info/"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it. "
               "Issue wording is the Board's summary; the full wording is on the sample ballot.",
               NOTE_ORDER, NOTE_PLACES,
               "The Board's notice does not give local issue numbers; see your sample ballot for them.",
               "County Coroner (unexpired term ending December 31, 2028) is also on the ballot, but the Board's notice says no valid candidate filed."]
    P = c.p; D = c.district; SD = c.sd

    # 8th Congressional district covers the whole county. The notice's 5th Senate / 80th House precincts (17-18, 23-24, 27, 29-31, 34-37)
    # and 84th House precincts match the voter file. The 12th Senate seat is not up this year.
    c.contest("congress-8", "U.S. House", "Representative to Congress", [("Warren Davidson", "REP"), ("Vanessa Enoch", "DEM")],
              detail="8th District (Hamilton, Butler (part), Preble, Darke and Miami (part) counties)", src=S)
    c.contest("senate-5", "Ohio General Assembly", "State Senator", [("Jeffrey Harris", "DEM"), ("Phil Plummer", "REP")], detail="5th District", places=D("sen", 5), src=S)
    c.contest("rep-80", "Ohio General Assembly", "State Representative", [("Johnathan Newman", "REP"), ("Katie Koehler Wagner", "DEM")], detail="80th District", places=D("rep", 80), src=S)
    c.contest("rep-84", "Ohio General Assembly", "State Representative", [("Arienne C. Childrey", "DEM"), ("Angie King", "REP")], detail="84th District", places=D("rep", 84), src=S)
    c.contest("appeals-2-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Chris Epley", "REP")], detail="2nd District · term commencing February 9, 2027", src=S)
    # The notice prints no party for Eddie Anjos.
    c.contest("commissioner", "County offices", "County Commissioner", [("Eddie Anjos", "Nonparty"), ("David J. Coons", "REP")], detail="Term commencing January 1, 2027", src=S)
    c.contest("auditor", "County offices", "County Auditor", [("Brian L. Holsapple", "REP")], detail="Term commencing March 8, 2027", src=S)
    NP = " · no party label on the ballot"
    c.contest("cp-juvenile-probate", "Court of Common Pleas", "Judge of the Court of Common Pleas, Juvenile/Probate Division", ["Jason Aslinger"],
              detail="Term commencing February 9, 2027" + NP, src=S)

    # --- Countywide issues ---
    est = lambda total, per: f"{total} a year; {per} for each $100,000 of the county auditor's market value"
    # Same levy as miami.py's tri-county-mental-health (and Shelby's).
    c.levy("tri-county-mental-health", "Tri-County Board of Recovery and Mental Health Services (Darke, Miami and Shelby counties)", "county", "Renewal",
           "Counseling and supportive services to children and adults through alcohol and drug addiction programs and mental health programs.", "0.6 mill",
           "5 years, commencing in 2027", "2028", est("$2,596,848", "$10"), area="All of Darke County", src=S)

    # --- Local issues ---
    # Precinct numbers matched to names via the PRSID/PRECNAME columns of the Board's absentee file, joined to the voter file.
    c.levy("ansonia-operating", "Village of Ansonia", P("ANSONIA VILLAGE"), "Renewal", "Current expenses.", "3 mills",
           "5 years, commencing in 2027", "2028", est("$36,812", "$65"), area="Ansonia Village (precinct 16/3)", src=S)
    c.issue("arcanum-income-tax", "question", "Village of Arcanum", "Municipal income tax: 0.5% increase for municipal operations, services and capital improvements",
            P("ARCANUM VILLAGE"), area="Arcanum Village (precincts 34/1, 35/1)",
            text="Ordinance providing for a 0.5% levy increase on income for general municipal operations, maintenance, new equipment, extension and enlargement "
                 "of municipal services and facilities, and capital improvements.", src=S)
    c.levy("palestine-operating", "Village of Palestine", P("PALESTINE VILLAGE"), "Renewal", "Current expenses.", "2.3 mills",
           "5 years, commencing in 2027", "2028", est("$3,971", "$55"), area="Palestine Village (precinct 27/1)", src=S)
    # Notice precincts 18/1, 18/5 (Franklin Twp), 20/2 (Greenville Twp), 29/1 (Monroe Twp), 29/5 (Pitsburg), 36/3 (Twin Twp), 37/2 (Van Buren Twp); SD() matches them.
    c.issue("franklin-monroe-lsd-tax", "question", "Franklin Monroe Local School District", "School district income tax: 1.25% for 5 years, for current expenses",
            SD("FRANKLIN-MONROE LOCAL SD (DARKE)"), area="Franklin Monroe Local School District",
            text="Annual income tax of 1.25% on the school district income of individuals, for 5 years, beginning January 1, 2027, for current expenses.", src=S)
    # Placed from the notice's precinct list: 17/1, 17/3 (Butler Twp; not Castine, 17/2), 23/1-3 (Hollansburg, Harrison Twp), 24/1-4 (Harrison Twp, New Madison),
    # 27/1-3 (Palestine, Liberty Twp), 30/1 (Wayne Lakes), 31/1, 31/4 (Neave Twp).
    c.levy("tri-village-ambulance", "Tri-Village Joint Ambulance District",
           P("BUTLER TWP", "HARRISON TWP", "HOLLANSBURG VILLAGE", "NEW MADISON VILLAGE", "LIBERTY TWP", "PALESTINE VILLAGE", "WAYNE LAKES VILLAGE", "NEAVE TWP"),
           "Additional", "Current expenses.", "1.5 mills", "Continuing period of time, commencing in 2026", "2027", est("$343,778", "$53"),
           area="Tri-Village Joint Ambulance District (precincts 17/1, 17/3, 23/1–3, 24/1–4, 27/1–3, 30/1, 31/1, 31/4)", src=S)
    return c
