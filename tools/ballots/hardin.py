from lib import County, NOTE_ORDER, NOTE_PLACES

SITE = "https://www.boe.ohio.gov/hardin/"
NOTICE = "https://www.boe.ohio.gov/hardin/c/upload/FWAB_11November46Day.pdf"


def build():
    # The SoS file misspells Taylor Creek ("TAYLOR CREEK TOWNSHP"); the other names display correctly
    # ("MT. VICTORY VILLAGE" -> "Mt. Victory Village", "MCGUFFEY VILLAGE" -> "McGuffey Village").
    c = County("hardin", "Hardin", "39065", rename={"TAYLOR CREEK TOWNSHP": "Taylor Creek Township"})
    c.src("hardin-46day", "Hardin County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election (revised 9/17/2026)", NOTICE)
    S = ["hardin-46day"]
    c.links = [
        {"label": "Board of Elections", "url": SITE},
        {"label": "Election info", "url": "https://www.boe.ohio.gov/hardin/election-info/"},
        {"label": "Sample ballots by precinct", "url": "https://lookup.boe.ohio.gov/vtrapp/hardin/ballotlist.aspx"},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://www.boe.ohio.gov/hardin/election-info/election-results/"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it "
               "and gives the full ballot wording of each issue.",
               NOTE_ORDER, NOTE_PLACES,
               "The Board's notice does not give local issue numbers; see your sample ballot for them."]
    P = c.p; SD = c.sd

    # The notice lists precincts by number only. Numbers match the absentee file's PRSID/PRECNAME: 01-04 Kenton 1-4, 05 Dunkirk/Blanchard,
    # 08 Dudley, 10 Mt Victory/Ridgeway/Hale, 12 Ada North, 13 Ada South, 14 Liberty, 21 Washington.

    # --- Federal, state legislative, appeals: all of Hardin County is in the 4th Congressional, 83rd House and 1st Senate districts ---
    # The notice prints no party for Tackett (an independent candidate), as in allen.py and logan.py.
    c.contest("congress-4", "U.S. House", "Representative to Congress", [("Jim Jordan", "REP"), ("Joshua D. Kolasinski", "DEM"), ("Tracey L. Tackett", "Nonparty")],
              detail="4th District", src=S)
    # The notice prints no district number; the voter file puts all of Hardin in the 1st (same candidate as hancock.py and logan.py).
    c.contest("senate-1", "Ohio General Assembly", "State Senator", [("Craig S. Riedel", "REP")], detail="1st District · full term commencing January 1, 2027", src=S)
    c.contest("rep-83", "Ohio General Assembly", "State Representative", [("Sheila Coressel", "DEM"), ("Ty Mathews", "REP")], detail="83rd District", src=S)
    # The notice prints no party for Miller; party as in allen.py and logan.py.
    c.contest("appeals-3-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Mark C. Miller", "REP")],
              detail="3rd District · full term commencing February 9, 2027", src=S)

    # --- County offices ---
    c.contest("commissioner", "County offices", "County Commissioner", [("Daryl G. Flowers", "DEM"), ("Michael P. Kasler", "REP")],
              detail="Term commencing January 1, 2027", src=S)
    c.contest("auditor", "County offices", "County Auditor", [("Mark Schwemer", "REP")], detail="Term commencing March 8, 2027", src=S)
    NP = " · no party label on the ballot"
    c.contest("cp-general-probate", "Court of Common Pleas", "Judge of the Court of Common Pleas, General Division and Probate Division", ["Steve Christopher"],
              detail="Full 6-year term commencing February 9, 2027" + NP, src=S)

    # --- Issues (unnumbered in the Board's notice; listed in the notice's order) ---
    c.issue("kenton-charter-commission", "question", "City of Kenton", "Charter commission: shall a commission be chosen to frame a charter?", P("KENTON CITY"),
            area="Kenton (precincts 01/1, 01/2, 02/1, 03/1, 04/1, 04/2)",
            text="Shall a commission be chosen to frame a charter?", src=S)
    # Precinct 10 (all four splits) is Mt Victory/Ridgeway/Hale; the store is in Ridgeway.
    HALE = P("HALE TOWNSHIP", "RIDGEWAY VILLAGE", "MT. VICTORY VILLAGE")
    SK = "Tresha Corporation, dba S. & K. Minimart, {what}, who is engaged in the business of operating a carryout/grocery store at 110 N. Main Street, Ridgeway"
    for id, title, text in [
        ("liquor-sk-minimart", "Local liquor option: S. & K. Minimart (wine and mixed beverages)",
         "Sale of wine and mixed beverages by " + SK.format(what="an applicant for a C2 liquor permit") + "."),
        ("liquor-sk-minimart-sunday", "Local liquor option: S. & K. Minimart (Sunday, wine and mixed beverages)",
         "Sunday sale of wine and mixed beverages by " + SK.format(what="an applicant for a D6 liquor permit") + "."),
    ]:
        c.issue(id, "liquor", "Hale Township", title, HALE, area="Precinct Mt Victory/Ridgeway/Hale (10/1–10/4)", text=text, src=S)
    ADA = P("LIBERTY TOWNSHIP", "ADA VILLAGE")
    ADA_AREA = "Precincts Ada North, Ada South and Liberty (12/1, 13/1, 14/1)"
    PARK = "Defraying the expense and improving and maintaining the free public park."
    c.levy("liberty-park-1", "Park District of Liberty Township", ADA, "Renewal", PARK, "1 mill", "5 years, commencing in 2027", "2028",
           "$107,817 a year; $26 for each $100,000 of market value", area=ADA_AREA, src=S)
    c.levy("liberty-park-1-5", "Park District of Liberty Township", ADA, "Renewal", PARK, "1.5 mills", "5 years, commencing in 2027", "2028",
           "$161,726 a year; $39 for each $100,000 of market value", area=ADA_AREA, src=S)
    c.levy("ada-library", "Ada Public Library (Hardin and Hancock counties)", ADA, "Renewal", "Current expenses of the Library.", "1 mill",
           "5 years, commencing in 2027", "2028", "$102,209 a year; $20 for each $100,000 of market value", area=ADA_AREA, src=S)
    # Dudley 08/3 and Mt Victory/Ridgeway/Hale 10/2; the voter file's Elgin voters are in Dudley and Hale townships.
    c.levy("elgin-lsd", "Elgin Local School District (Marion, Delaware and Hardin counties)", SD("ELGIN LOCAL SD (MARION)"), "Renewal",
           "Current expenses.", "2.88 mills", "5 years, commencing in 2027", "2028", "$850,000 a year (fixed sum); $101 for each $100,000 of market value",
           area="Elgin Local School District (precincts Dudley 08/3, Mt Victory/Ridgeway/Hale 10/2)", src=S,
           note="A fixed-sum levy of $850,000; 2.88 mills is the county auditor's estimated average rate.")
    c.levy("northern-hardin-fire", "Northern Hardin County Fire District", P("DUNKIRK VILLAGE", "BLANCHARD TOWNSHIP", "WASHINGTON TOWNSHIP"), "Additional",
           "Fire apparatus, equipment, buildings and personnel, and ambulance, paramedic or other emergency medical services.", "0.9 mill",
           "5 years, commencing in 2026", "2027", "$82,220 a year; $32 for each $100,000 of market value",
           area="Precincts Dunkirk/Blanchard (05/1–05/3) and Washington (21/1)", src=S)
    c.levy("ada-liberty-ambulance", "Ada-Liberty Joint Ambulance District", ADA, "Renewal", "Ambulance service, emergency service, or both.", "2 mills",
           "5 years, commencing in 2027", "2028", "$218,316 a year; $53 for each $100,000 of market value", area=ADA_AREA, src=S)
    return c
