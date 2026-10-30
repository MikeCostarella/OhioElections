from lib import County, NOTE_ORDER, NOTE_PLACES

SITE = "https://henrycountyohio.gov/231/Board-of-Elections"
NOTICE = "https://henrycountyohio.gov/DocumentCenter/View/1059/46-Day-Notice-PDF"


def build():
    # Default display names are right ("MCCLURE VILLAGE" -> "McClure Village", "NAPOLEON CITY" -> "Napoleon City"); no renames needed.
    c = County("henry", "Henry", "39069")
    c.src("henry-46day", "Henry County Board of Elections: 46-day election notice (FWAB, updated notification), November 3, 2026 General Election", NOTICE)
    C = I = ["henry-46day"]
    c.links = [
        {"label": "Board of Elections", "url": SITE},
        {"label": "46-day election notice", "url": NOTICE},
        {"label": "Voter registration, polling place and absentee ballot lookup", "url": "https://henry-voterview.boe.ohio.gov/VoterView/Home.do"},
        {"label": "Precinct map", "url": "https://henrycountyohio.gov/DocumentCenter/View/452/Henry-County-Precinct-Map-PDF"},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://henrycountyohio.gov/241/Election-Results"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it. "
               "The Board does not post precinct sample ballots or full ballot wording online, so issues are summarised from the notice "
               "and the county auditor's estimates are not shown.",
               NOTE_ORDER, NOTE_PLACES,
               "The Board's notice gives no local issue numbers; Issue 3 is the statewide question."]
    P = c.p; D = c.district; SD = c.sd

    # --- Federal, state legislative, appeals (all 23 precincts of Henry County are in each district) ---
    # Kathy McKinstry is a certified write-in for Congress (not listed).
    c.contest("congress-9", "U.S. House", "Representative to Congress", [("Marcy Kaptur", "DEM"), ("Derek Merrin", "REP")], detail="9th District", src=C)
    c.contest("senate-1", "Ohio General Assembly", "State Senator", [("Craig S. Riedel", "REP")], detail="1st District", src=C)
    c.contest("rep-81", "Ohio General Assembly", "State Representative", [("Patti Rockey", "REP"), ("David Swanson", "DEM")], detail="81st District", src=C)
    c.contest("appeals-3-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Mark C. Miller", "REP")], detail="3rd District · full term commencing February 9, 2027", src=C)

    # --- County offices (the notice lists no Common Pleas, Probate or Juvenile judge contests) ---
    c.contest("commissioner", "County offices", "County Commissioner", [("Joel Miller", "REP")], detail="Full term commencing January 1, 2027", src=C)
    c.contest("auditor", "County offices", "County Auditor", [("Elizabeth A. Fruchey", "REP")], detail="Full term commencing March 8, 2027", src=C)

    # --- Issues (unnumbered in the notice; listed in its order) ---
    c.levy("henry-hope-services", "Henry County HOPE Services", "county", "Additional",
           "Community developmental disabilities programs and services.", "2.5 mills", "5 years, commencing in 2026", "2027", src=I)
    c.levy("henry-health-district", "Henry County General Health District", "county", "Renewal",
           "Current expenses.", "1.2 mills", "5 years, commencing in 2027", "2028", src=I)
    # Same id, jurisdiction and purpose as defiance.py / fulton.py / williams.py; figures from those Boards' ballot wording (one countywide district levy).
    c.levy("four-county-adamhs", "Four County ADAMhs Board (Defiance, Fulton, Henry and Williams)", "county", "Renewal",
           "Current expenses of the Four County Board of Alcohol, Drug Addiction and Mental Health Services District.", "0.7 mill",
           "5 years, commencing in 2027", "2028", "$2,293,020 a year; $13 for each $100,000 of market value", area="Henry County", src=I)
    c.levy("deshler-current", "Village of Deshler", P("DESHLER VILLAGE"), "Renewal", "Current expenses.", "1.4 mills",
           "5 years, commencing in 2027", "2028", area="Deshler Village (precinct 7.0)", src=I)
    c.levy("ridgeville-twp-roads", "Ridgeville Township", P("RIDGEVILLE TOWNSHIP"), "Additional",
           "General construction, reconstruction, resurfacing and repair of streets, roads and bridges.", "2 mills",
           "5 years, commencing in 2026", "2028", area="Ridgeville Township (precincts 22.1, 22.2)", src=I,
           note="The Board's notice prints \"Commencing 2026, First due 2028\"; a levy commencing in 2026 is normally first due in 2027 "
                "(the Northwest Signal's filing report says 2027). Shown as the notice gives it.")
    c.levy("napoleon-twp-fire", "Napoleon Township", P("NAPOLEON TOWNSHIP"), "Additional",
           "Providing and maintaining fire apparatus and buildings of Napoleon Township and related matters.", "4 mills",
           "Continuing, commencing in 2026", "2027", area="Napoleon Township (Napoleon East and West, precincts 17.0, 18.0)", src=I)
    # Precinct 1.2 is the Liberty Township part of Napoleon City 01 (128 voters in the voter file) and 13.1 the Liberty Township part of
    # Liberty Center; 4.2 is presumably a Liberty Township split of Napoleon City 04 (no voters there in the voter file).
    c.levy("liberty-twp-current", "Liberty Township (including the Liberty Township parts of Napoleon and Liberty Center)",
           P("LIBERTY TOWNSHIP", "NAPOLEON CITY", "LIBERTY CENTER VILLAGE"), "Renewal", "Current expenses.", "0.75 mill",
           "5 years, commencing in 2026", "2027", area="Liberty Township (precincts 1.2, 4.2, 13.1, 14.0)", src=I)
    c.levy("harrison-twp-fire", "Harrison Township", P("HARRISON TOWNSHIP"), "Additional",
           "Providing and maintaining fire apparatus of Harrison Township and related matters.", "4 mills",
           "5 years, commencing in 2027", "2028", area="Harrison Township (precincts 12.1, 12.2, 12.3)", src=I)
    # Only precinct 20.1 (not New Bavaria Village or the Pleasant Township part of Holgate) votes on this levy.
    c.levy("pleasant-twp-roads", "Pleasant Township", P("PLEASANT TOWNSHIP"), "Renewal",
           "General construction, reconstruction, resurfacing and repair of streets, roads and bridges.", "2 mills",
           None, "2027", area="Pleasant Township (precinct 20.1)", src=I,
           note="The Board's notice gives \"Commencing 2026, First Due 2027\" but no number of years (the Northwest Signal's filing report says five years).")
    # Same id, jurisdiction and purpose as fulton.py (which numbers it Issue 3 on Fulton ballots); the Henry notice gives it no number.
    # The notice lists Freedom Township split 11.4, where the voter file puts no Pettisville voters, so Freedom Township is added by hand.
    c.levy("pettisville-lsd", "Pettisville Local School District (Fulton and Henry)", SD("PETTISVILLE LOCAL SD (FULTON)") + P("FREEDOM TOWNSHIP"), "Renewal",
           "General permanent improvements.", "2.5 mills", "5 years, commencing in 2026", "2027",
           area="Pettisville Local School District (Henry County part: precincts 11.4, 22.2)", src=I)
    return c
