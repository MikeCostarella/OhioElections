from lib import County, NOTE_ORDER, NOTE_PLACES

NOTICE = "https://www.boe.ohio.gov/perry/c/upload/FWAB_11November46Day.pdf"

# Precinct numbers in the notice (from the Board's primary candidate list, which names each precinct):
# 1-4 New Lexington, 5 Bearfield, 6 Clayton, 7 Coal (incl. New Straitsville), 8-9 Crooksville, 10 Roseville,
# 11 Harrison South, 12 Harrison North, 13 Hopewell E/Glenford, 14 Hopewell W, 15 Junction City, 16-17 Jackson,
# 18 Madison, 19 Monday Creek, 20 Monroe (incl. Corning, Rendville), 21-22 Pike, 23 Pleasant, 24 Somerset,
# 25-27 Reading, 28 Saltlick (incl. Shawnee, Hemlock), 29 Thornville, 30-32 Thorn, 33 Buckeye Lake (Thorn Township).


def build():
    # The SoS file spells the township "MONDAY CREEK TOWNSHP".
    c = County("perry", "Perry", "39127", rename={"MONDAY CREEK TOWNSHP": "Monday Creek Township"})
    c.src("perry-46day", "Perry County Board of Elections: election notice (FWAB), November 3, 2026 General Election (revised 9/18/2026)", NOTICE)
    S = ["perry-46day"]
    c.links = [
        {"label": "Board of Elections", "url": "https://www.boe.ohio.gov/perry/"},
        {"label": "Election information", "url": "https://www.boe.ohio.gov/perry/election-info/"},
        {"label": "Sample ballots by precinct", "url": "https://lookup.boe.ohio.gov/vtrapp/perry/ballotlist.aspx"},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://www.boe.ohio.gov/perry/election-info/election-results/"}]
    c.notes = ["Taken from the Board of Elections' election notice for the federal write-in absentee ballot (revised September 18, 2026), which lists every contest and issue "
               "with the precincts that vote on it. Issue wording is the Board's ballot wording, condensed; the full wording is on the sample ballot.",
               NOTE_ORDER, NOTE_PLACES,
               "The Board's notice does not give local issue numbers; see your sample ballot for them."]
    P = c.p; D = c.district

    # --- Federal, state legislative, appeals (the notice's precinct lists match the voter file's districts) ---
    c.contest("congress-2", "U.S. House", "Representative to Congress", [("Jen Mazzuckelli", "DEM"), ("David J. Taylor", "REP")],
              detail="2nd District", places=D("cong", 2), src=S)
    c.contest("congress-12", "U.S. House", "Representative to Congress", [("Troy Balderson", "REP"), ("Jerrad Christian", "DEM")],
              detail="12th District", places=D("cong", 12), src=S)
    c.contest("senate-17", "Ohio General Assembly", "State Senator", [("Brian A. Deer", "DEM"), ("Shane Wilkin", "REP")],
              detail="17th District", places=D("sen", 17), src=S)
    c.contest("rep-69", "Ohio General Assembly", "State Representative", [("Kevin D. Miller", "REP"), ("Amy Rigsby", "DEM")],
              detail="69th District (also in Fairfield and Licking counties)", places=D("rep", 69), src=S)
    c.contest("rep-92", "Ohio General Assembly", "State Representative", [("Mark Johnson", "REP"), ("Sarah Senff", "DEM")],
              detail="92nd District", places=D("rep", 92), src=S)
    c.contest("appeals-5", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Matthew George", "REP")], detail="5th District · term commencing February 9, 2027", src=S)

    # --- County offices ---
    c.contest("commissioner", "County offices", "County Commissioner", [("Scott Owen", "REP")], detail="Full term commencing January 1, 2027", src=S)
    c.contest("auditor", "County offices", "County Auditor", [("Derek Householder", "REP")], detail="Full 4-year term commencing March 8, 2027", src=S)
    c.contest("recorder", "County offices", "County Recorder", [("Ben Stenson", "REP")], detail="Unexpired term ending December 31, 2028", src=S)
    c.contest("coroner", "County offices", "County Coroner", [("Jeffrey P. VanMeter", "REP")], detail="Unexpired term ending December 31, 2028", src=S)
    NP = " · no party label on the ballot"
    for id, office, date, cs in [
        # The notice (and the Board's primary candidate list) give this term's start as 7-6-2028.
        ("cp-gen", "General Division", "Full term commencing July 6, 2028", ["Tina Boyer", "Steve Carr"]),
        ("cp-probate-juvenile", "Probate-Juvenile Division", "Full term commencing February 9, 2027", ["Carolyn J. Carnes"]),
    ]:
        c.contest(id, "Court of Common Pleas", f"Judge of the Court of Common Pleas, {office}", cs, detail=date + NP, src=S)

    # --- Issues (unnumbered in the Board's notice; listed in the notice's order) ---
    est = lambda a, per: f"${a} a year; ${per} for each $100,000 of market value"
    c.levy("county-home", "Perry County", "county", "Renewal", "Maintenance and operation of the Perry County Home (Fairview Assisted Living).", "1 mill",
           "5 years, commencing in 2026", "2027", est("690,629", 14), area="Perry County (all precincts)", src=S)
    L = [
        ("corning-police", "Village of Corning", ["CORNING VILLAGE"], "Renewal", "Providing and maintaining a police department, equipment and personnel.", "5 mills",
         "5 years, commencing in 2026", "2027", est("21,512", 155), "Corning (Monroe precinct 0020/2)"),
        ("crooksville-park-pool", "Village of Crooksville", ["CROOKSVILLE VILLAGE"], "Renewal", "Operation of the municipal park and swimming pool.", "2 mills",
         "5 years, commencing in 2027", "2028", est("55,905", 50), "Crooksville precincts 0008/1, 0009/1"),
        ("crooksville-park-recreation", "Village of Crooksville", ["CROOKSVILLE VILLAGE"], "Renewal", "Municipal park and recreational purposes.", "3 mills",
         "5 years, commencing in 2027", "2028", est("69,600", 52), "Crooksville precincts 0008/1, 0009/1"),
        ("junction-city-current", "Village of Junction City", ["JUNCTION CITY VILLAGE"], "Renewal", "Current expenses.", "5 mills",
         "5 years, commencing in 2027", "2028", est("15,888", 60), "Junction City precinct 0015/1"),
        ("new-lexington-parks", "Village of New Lexington", ["NEW LEXINGTON VILLAGE"], "Renewal", "Maintaining and operating the New Lexington Parks and Recreation.", "1 mill",
         "Continuing period of time, commencing in 2027", "2028", est("53,546", 23), "New Lexington precincts 0001/1–0004/1"),
    ]
    for id, jur, raws, t, purpose, mills, term, fd, e, area in L:
        c.levy(id, jur, P(*raws), t, purpose, mills, term, fd, e, area=area, src=S)
    # Same levy as muskingum.py's roseville-current (the village is in both counties).
    c.levy("roseville-current", "Village of Roseville (Muskingum and Perry counties)", P("ROSEVILLE VILLAGE"), "Renewal", "Current expenses.", "4 mills",
           "5 years, commencing in 2027", "2028", est("38,422", 65), area="Roseville precinct 0010/1", src=S)
    L = [
        ("shawnee-current-2", "Village of Shawnee", ["SHAWNEE VILLAGE"], "Renewal", "Current expenses.", "2 mills",
         "5 years, commencing in 2026", "2027", est("13,991", 49), "Shawnee (Saltlick precinct 0028/1)",
         "Shawnee has two current-expense renewals on this ballot (2 mills and 3 mills)."),
        ("shawnee-current-3", "Village of Shawnee", ["SHAWNEE VILLAGE"], "Renewal", "Current expenses.", "3 mills",
         "5 years, commencing in 2026", "2027", est("18,514", 55), "Shawnee (Saltlick precinct 0028/1)",
         "Shawnee has two current-expense renewals on this ballot (2 mills and 3 mills)."),
        ("shawnee-cemeteries", "Village of Shawnee", ["SHAWNEE VILLAGE"], "Renewal", "Maintaining and operating cemeteries.", "2 mills",
         "5 years, commencing in 2026", "2027", est("14,193", 51), "Shawnee (Saltlick precinct 0028/1)", None),
        ("somerset-current", "Village of Somerset", ["SOMERSET VILLAGE"], "Additional", "Current expenses.", "2.1 mills",
         "5 years, commencing in 2026", "2027", est("61,173", 74), "Somerset precinct 0024/1", None),
        ("somerset-police", "Village of Somerset", ["SOMERSET VILLAGE"], "Renewal", "Police protection.", "6.5 mills",
         "5 years, commencing in 2026", "2027", est("150,772", 169), "Somerset precinct 0024/1", None),
        ("bearfield-cemetery", "Bearfield Township", ["BEARFIELD TOWNSHIP"], "Renewal", "Maintaining and operating a cemetery.", "1 mill",
         "5 years, commencing in 2027", "2028", est("56,732", 9), "Bearfield Township precincts 0005/1, 0005/2", None),
        # Coal precincts 0007/1 and 0007/2 take in New Straitsville, which is in Coal Township.
        ("coal-current", "Coal Township", ["COAL TOWNSHIP", "NEW STRAITSVILLE VILLAGE"], "Renewal", "Current expenses.", "1 mill",
         "5 years, commencing in 2026", "2027", est("8,473", 25), "Coal Township precincts 0007/1, 0007/2 (incl. New Straitsville)", None),
        ("coal-cemetery", "Coal Township", ["COAL TOWNSHIP", "NEW STRAITSVILLE VILLAGE"], "Renewal", "Maintaining and operating a cemetery.", "2 mills",
         "5 years, commencing in 2026", "2027", est("15,183", 42), "Coal Township precincts 0007/1, 0007/2 (incl. New Straitsville)", None),
        ("coal-roads", "Coal Township", ["COAL TOWNSHIP", "NEW STRAITSVILLE VILLAGE"], "Renewal", "Maintaining roads and bridges.", "2 mills",
         "5 years, commencing in 2026", "2027", est("16,945", 50), "Coal Township precincts 0007/1, 0007/2 (incl. New Straitsville)", None),
        ("madison-roads", "Madison Township", ["MADISON TOWNSHIP"], "Additional", "General construction, reconstruction, resurfacing and repair of streets, roads and bridges.", "1 mill",
         "5 years, commencing in 2026", "2027", est("36,638", 35), "Madison Township precinct 0018/1", None),
        ("madison-fire", "Madison Township", ["MADISON TOWNSHIP"], "Renewal",
         "Providing and maintaining firefighting facilities, equipment and personnel, including paramedics and other emergency medical services.", "2 mills",
         "5 years, commencing in 2027", "2028", est("54,740", 50), "Madison Township precinct 0018/1", None),
        # Saltlick precincts 0028/1-4 take in Shawnee and Hemlock, both in Saltlick Township.
        ("saltlick-current", "Saltlick Township", ["SALTLICK TOWNSHIP", "SHAWNEE VILLAGE", "HEMLOCK VILLAGE"], "Additional", "Current expenses.", "0.5 mill",
         "5 years, commencing in 2027", "2028", est("13,446", 18), "Saltlick Township precincts 0028/1–0028/4 (incl. Shawnee and Hemlock)", None),
        # Thorn precincts 0029-0033 include Thornville (0029).
        ("thorn-fire-ems", "Thorn Township", ["THORN TOWNSHIP", "THORNVILLE VILLAGE"], "Renewal",
         "Payment of permanent, part-time or volunteer firefighting and emergency medical services.", "3 mills",
         "5 years, commencing in 2027", "2028", est("506,348", 64), "Thorn Township precincts 0029/1–0033/1 (incl. Thornville)", None),
    ]
    for id, jur, raws, t, purpose, mills, term, fd, e, area, note in L:
        c.levy(id, jur, P(*raws), t, purpose, mills, term, fd, e, area=area, note=note, src=S)

    # --- Local liquor option ---
    c.issue("liquor-quick-stop-93", "liquor", "Harrison Township", "Local liquor option: Quick Stop 93 (D-6 permit, Sunday)", P("HARRISON TOWNSHIP"),
            area="Harrison South precinct (0011/1, 0011/2)",
            text="Shall the sale of beer, wine and mixed beverages be permitted for sale on Sunday by Quick Stop 93 LLC, an applicant for a D-6 liquor permit who is engaged in the business "
                 "of convenience store and drive thru at 3905 State Route 93 NE, Crooksville, in this precinct?", src=S)
    return c
