from lib import County, NOTE_ORDER, NOTE_PLACES

SITE = "https://www.boe.ohio.gov/lawrence/"
NOTICE = "https://www.boe.ohio.gov/lawrence/c/upload/FWAB_11November46Day.pdf"
BALLOTS = "https://lookup.boe.ohio.gov/vtrapp/lawrence/ballotlist.aspx"

TWPS = ["AID", "DECATUR", "ELIZABETH", "FAYETTE", "HAMILTON", "LAWRENCE", "MASON", "PERRY", "ROME", "SYMMES", "UNION", "UPPER", "WASHINGTON", "WINDSOR"]


def build():
    # The SoS file spells townships "AID TWP." with a period; villages and Ironton City already display correctly.
    rename = {f"{t} TWP.": f"{t.title()} Township" for t in TWPS}
    c = County("lawrence", "Lawrence", "39087", rename=rename)
    c.src("lawrence-46day", "Lawrence County Board of Elections: 46-day election notice (FWAB), November 3, 2026 General Election (posted October 15, 2026)", NOTICE)
    c.src("lawrence-ballots", "Lawrence County Board of Elections: precinct sample ballots, November 3, 2026 General Election (election data updated October 5, 2026)", BALLOTS)
    S = ["lawrence-46day", "lawrence-ballots"]
    B = ["lawrence-ballots", "lawrence-46day"]
    c.links = [
        {"label": "Board of Elections", "url": SITE},
        {"label": "Federal write-in absentee ballot notices", "url": "https://www.boe.ohio.gov/lawrence/election-info/federal-write-in-absentee-ballots/"},
        {"label": "Sample ballots by precinct", "url": BALLOTS},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://www.boe.ohio.gov/lawrence/election-info/election-results/"}]
    c.notes = ["Taken from the Board of Elections' 46-day election notice, which lists every contest and issue with the precincts that vote on it, "
               "checked against the Board's precinct sample ballots. Terms of office and issue wording are from the sample ballots.",
               NOTE_ORDER, NOTE_PLACES,
               "The Board's notice and sample ballots do not give local issue numbers.",
               "The 46-day notice lists the Fayette Township fire levy for Fayette 1–3 and Burlington 1–3; the sample ballots also carry it in "
               "South Point 1–3 (the part of South Point Village in Fayette Township), as shown here."]
    P = c.p; D = c.district

    # --- Federal, state legislative, appeals (every precinct is in the 2nd Congressional, 17th Senate, 93rd House and 4th Appeals districts) ---
    c.contest("congress-2", "U.S. House", "Representative to Congress", [("Jen Mazzuckelli", "DEM"), ("David J. Taylor", "REP")],
              detail="2nd District", places=D("cong", 2), src=S)
    c.contest("senate-17", "Ohio General Assembly", "State Senator", [("Brian A. Deer", "DEM"), ("Shane Wilkin", "REP")],
              detail="17th District", places=D("sen", 17), src=S)
    c.contest("rep-93", "Ohio General Assembly", "State Representative", [("Jessica Harper", "DEM"), ("Jason Stephens", "REP")],
              detail="93rd District", places=D("rep", 93), src=S)
    c.contest("appeals-4-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Jayme Hartley Fountain", "REP"), ("Todd L. Grace", "DEM")],
              detail="4th District · full term commencing February 9, 2027", src=B)

    # --- County ---
    c.contest("commissioner", "County offices", "County Commissioner", [("Mike Finley", "REP")],
              detail="Full term commencing January 1, 2027", src=B)
    # Neither the notice nor the sample ballot gives the auditor's term.
    c.contest("auditor", "County offices", "County Auditor", [("Paul David Knipp", "REP")], src=S)
    NP = " · no party label on the ballot"
    # The notice lists Ballard as DEM and Sanders as REP; the sample ballots print no party for these judges.
    for id, office, cs in [
        ("cp-0209", "Judge of the Court of Common Pleas", ["Andy Ballard"]),
        ("cp-probate-juvenile", "Judge of the Court of Common Pleas, Probate/Juvenile Division", ["Patricia Sanders"]),
    ]:
        c.contest(id, "Court of Common Pleas", office, cs, detail="Full term commencing February 9, 2027" + NP, src=B)

    # --- Issues (unnumbered; listed in the notice's order) ---
    est = lambda total, per: f"{total} a year; {per} for each $100,000 of market value"
    CH = P("CHESAPEAKE VILLAGE")
    c.levy("chesapeake-police", "Village of Chesapeake", CH, "Renewal", "Providing and maintaining police protection.", "1.5 mills",
           "5 years, commencing in 2027", "2028", est("$22,512", "$35"), area="Chesapeake A and B", src=B)
    PR = P("PROCTORVILLE VILLAGE")
    c.levy("proctorville-current", "Village of Proctorville", PR, "Renewal", "Current expenses.", "2.5 mills",
           "5 years, commencing in 2027", "2028", est("$12,907", "$45"), area="Proctorville precinct", src=B)
    c.levy("proctorville-fire", "Village of Proctorville", PR, "Renewal", "Fire protection.", "1.5 mills",
           "5 years, commencing in 2027", "2028", est("$14,998", "$53"), area="Proctorville precinct", src=B)
    c.levy("ironton-recreation", "City of Ironton", P("IRONTON CITY"), "Renewal", "Recreation.", "0.5 mill",
           "5 years, commencing in 2027", "2028", est("$75,000", "$11"), area="Ironton 1A through 5A", src=B)
    # Lawrence County JVSD: not in the voter file's school-district columns; the notice lists all precincts except Washington
    # (Washington Township, whose voters are all in the Oak Hill Union Local School District).
    JVS = [x for x in c.places if x != "Washington Township"]
    c.levy("lawrence-jvsd-pi", "Lawrence County Joint Vocational School District", JVS, "Renewal", "Permanent improvements.", "0.5 mill",
           "5 years, commencing in 2027", "2028", est("$744,260", "$11"), area="All precincts except Washington", src=B)
    c.levy("fayette-twp-fire", "Fayette Township", P("FAYETTE TWP.", "SOUTH POINT VILLAGE"), "Renewal", "Fire protection.", "2 mills",
           "5 years, commencing in 2026", "2027", est("$266,530", "$46"),
           area="Fayette 1–3, Burlington 1–3 and South Point 1–3", src=B)
    c.levy("rome-twp-fire", "Rome Township", P("ROME TWP."), "Renewal", "Fire protection.", "1 mill",
           "5 years, commencing in 2027", "2028", est("$93,000", "$12"), area="Labelle 1–7 and Miller", src=B)

    # Local options (by petition)
    PE = P("PERRY TWP.")
    KASH_PERRY = "Kaival Property, Inc., dba Kash Stop, operating a carryout/grocery store at 3302 State Route 243, Ironton (Perry Township)"
    for id, title, text in [
        ("liquor-kash-stop-perry-beer", "Local liquor option: Kash Stop (beer)",
         f"Sale of beer by {KASH_PERRY}, an applicant for a C1 liquor permit."),
        ("liquor-kash-stop-perry-sunday", "Local liquor option: Kash Stop (Sunday sales)",
         f"Sunday sale of beer, wine and mixed beverages by {KASH_PERRY}, an applicant for a D-6 liquor permit."),
        ("liquor-kash-stop-perry-wine", "Local liquor option: Kash Stop (wine and mixed beverages)",
         f"Sale of wine and mixed beverages by {KASH_PERRY}, an applicant for a C2 liquor permit."),
    ]:
        c.issue(id, "liquor", "Perry Township", title, PE, area="Perry Township precinct Perry 2", text=text, src=B)
    for id, title, text in [
        ("liquor-chesapeake-a-sunday-on", "Local liquor option: Sunday sales for on-premises consumption",
         "Sunday sale of intoxicating liquor, of the same types as may be legally sold in the precinct on other days, for consumption on the premises where sold."),
        ("liquor-chesapeake-a-sunday-food", "Local liquor option: Sunday sales on premises where food and other sales exceed 50 percent",
         "Sunday sale of intoxicating liquor, of the same types as may be legally sold in the precinct on other days, for consumption on the premises where sold, "
         "at licensed premises where the sale of food and other goods and services exceeds fifty percent of the permit holder's total gross receipts there."),
        ("liquor-chesapeake-a-sunday-off", "Local liquor option: Sunday sales of wine and mixed beverages for off-premises consumption",
         "Sunday sale of wine and mixed beverages, of the same types as may be legally sold in the precinct on other days, for consumption off the premises where sold."),
    ]:
        c.issue(id, "liquor", "Village of Chesapeake", title, CH, area="Chesapeake precinct Chesapeake A", text=text, src=B)
    KASH_CH = "Radha Kash Stop, Inc., operating a carryout/grocery store at 531 3rd Avenue, Chesapeake"
    c.issue("liquor-kash-stop-chesapeake", "liquor", "Village of Chesapeake", "Local liquor option: Kash Stop (beer, wine and mixed beverages)", CH,
            area="Chesapeake precinct Chesapeake B",
            text=f"Sale of beer, wine and mixed beverages by {KASH_CH}, an applicant for a C1, C2 liquor permit.", src=B)
    c.issue("liquor-kash-stop-chesapeake-sunday", "liquor", "Village of Chesapeake", "Local liquor option: Kash Stop (Sunday wine and mixed beverages)", CH,
            area="Chesapeake precinct Chesapeake B",
            text=f"Sunday sale of wine and mixed beverages by {KASH_CH}, an applicant for a D-6 liquor permit.", src=B)
    return c
