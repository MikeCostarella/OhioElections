from lib import County, NOTE_ORDER, NOTE_PLACES

CAND = "https://www.boe.ohio.gov/summit/c/upload/Election_CandidateList.pdf"
SYN = "https://www.boe.ohio.gov/summit/c/upload/Election_60IssueSynopsis.pdf"

def build():
    c = County("summit", "Summit", "39153", rename={"NORTHFIELD CTR TP": "Northfield Center Township", "SAGAMORE HLS TWP": "Sagamore Hills Township"})
    c.src("summit-cand", "Summit County Board of Elections: official candidate list, November 3, 2026 General Election", CAND)
    c.src("summit-issues", "Summit County Board of Elections: issue synopsis, November 3, 2026 General Election", SYN)
    C = ["summit-cand"]; I = ["summit-issues"]
    c.links = [
        {"label": "Board of Elections", "url": "https://www.boe.ohio.gov/summit/"},
        {"label": "What's on my ballot?", "url": "https://lookup.boe.ohio.gov/vtrapp/summit/pollfinder.aspx"},
    ]
    c.results_links = [{"label": "Board of Elections: election results", "url": "https://www.boe.ohio.gov/summit/elections"}]
    c.notes = ["Taken from the Board of Elections' official candidate list and issue synopsis. Long charter amendments are condensed; "
               "the full wording is in the Board's issue synopsis and on the sample ballot.", NOTE_ORDER, NOTE_PLACES,
               "County Council at-large is a vote for up to three of the six candidates."]
    D = c.district; P = c.p; SD = c.sd

    c.contest("congress-13", "U.S. House", "Representative to Congress", [("Carey Coleman", "REP"), ("Sandeep Dixit", "Nonparty"), ("Emilia Sykes", "DEM")], detail="13th District", src=C)
    c.contest("senate-27", "Ohio General Assembly", "State Senator", [("Steve Demetriou", "REP"), ("Mike Roberto", "DEM")], detail="27th District", places=D("sen", 27), src=C)
    for n, cs in {31: [("Mike Kahoe", "REP"), ("J. Noah Spinner", "DEM")], 32: [("Jack K. Daniels", "REP"), ("Djordjije Popovic", "DEM")],
                  33: [("Napoleon Rodgers, Jr.", "REP"), ("Veronica Sims", "DEM")], 34: [("Derrick Hall", "DEM"), ("Craig A. Shubert", "REP")],
                  35: [("Samantha Salamon", "DEM"), ("Vik Sandhu", "REP")]}.items():
        c.contest(f"rep-{n}", "Ohio General Assembly", "State Representative", cs, detail=f"{n}{'st' if n == 31 else 'nd' if n == 32 else 'rd' if n == 33 else 'th'} District", places=D("rep", n), src=C)
    c.contest("appeals-9-0209", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Cynthia Curtin", "REP"), ("Betty Sutton", "DEM")], detail="9th District · term commencing February 9, 2027", src=C)
    c.contest("appeals-9-ute", "Ohio Court of Appeals", "Judge of the Court of Appeals", [("Tavia Galonski", "DEM"), ("Nathan Manning", "REP")], detail="9th District · unexpired term ending February 9, 2029", src=C)
    c.contest("council-at-large", "County offices", "Summit County Council at Large (vote for up to 3)",
              [("Shane R. Barker", "REP"), ("Jonathon D. Bollas", "REP"), ("John Chapman", "REP"), ("Erin Dickinson", "DEM"), ("John A. Donofrio", "DEM"), ("Elizabeth Walters", "DEM")],
              detail="Term commencing January 1, 2027", src=C)
    NP = " · no party label on the ballot"
    for i, (div, date, cs) in enumerate([
        ("Common Pleas Court Judge", "January 2, 2027", ["Tania Nemer", "Tammy O'Brien"]),
        ("Common Pleas Court Judge", "January 3, 2027", ["Kelly L. McLaughlin"]),
        ("Common Pleas Court Judge", "January 5, 2027", ["Alison McCarty", "Job Esau Perry"]),
        ("Common Pleas Court Judge", "January 6, 2027", ["Kate A. Makra", "Mary Margaret Rowlands"]),
        ("Common Pleas Court Judge", "February 9, 2027", ["Christine L. Croce", "John Galonski"]),
        ("Common Pleas Court Judge", "May 1, 2027", ["Joe Darwal", "Joy Malek Oldfield"]),
        ("Juvenile Court Judge", "January 1, 2027", ["Amy Corrigall Jones", "David Lombardi"]),
        ("Domestic Relations Judge", "January 4, 2027", ["Katarina Cook", "Lisa Dean"]),
        ("Probate Court Judge", "February 9, 2027", ["Steve Elliott", "Diana Stevenson"]),
    ]):
        c.contest(f"cp-{i}", "Court of Common Pleas", div, cs, detail=f"Term commencing {date}" + NP, src=C)
    c.contest("hudson-w2", "Municipal offices", "Hudson City Council, Ward 2", ["Phil Trendell", "Dan White"], detail="Unexpired term ending December 1, 2026 · Ward 2 voters only",
              places=P("HUDSON CITY"), area="Hudson Ward 2", src=C)

    est = lambda total, per: f"{total} a year; {per} for each $100,000 of market value"
    N = lambda n: f"Issue {n}"
    c.issue("issue-4", "levy", "Aurora City School District (Portage and Summit)", "Bond issue: $96,200,000 for a new elementary school, transportation facility and building improvements", SD("AURORA CITY SD"), number=N(4),
            levy={"type": "Bond issue", "purpose": "Constructing, furnishing and equipping a new elementary school and transportation facility, and renovating and improving school buildings and sites.", "mills": "4.26 mills (estimated average)", "term": "Up to 37 years", "estimate": "$96,200,000 principal; $149 for each $100,000 of market value"}, src=I)
    c.issue("issue-5", "question", "Barberton City School District", "School district income tax: 1% for 5 years", SD("BARBERTON CITY SD"), number=N(5),
            text="Shall an annual income tax of one percent (1.00%) on the earned income of individuals residing in the school district be imposed by the Barberton City School District, for 5 years, beginning January 1, 2027, for the purpose of current expenses?", src=I)
    c.levy("issue-6", "Cuyahoga Falls City School District", SD("CUYAHOGA FALLS CITY SD"), "Additional", "Current expenses.", "5.5 mills", "5 years, commencing in 2026", "2027", est("$6,148,893", "$193"), number=N(6), src=I)
    c.issue("issue-7", "question", "Norton City School District", "School district income tax: 0.75%, continuing", SD("NORTON CITY SD"), number=N(7),
            text="Shall an annual income tax of point seven five percent (0.75%) on the earned income of individuals residing in the school district be imposed by the Norton City School District, for a continuing period of time, beginning January 1, 2027, for the purpose of current operating expenses?", src=I)
    c.levy("issue-8", "Stow-Munroe Falls City School District (Summit and Portage)", SD("STOW-MUNROE FALLS CITY SD"), "Renewal", "Current operating expenses of the district.", "3.17 mills (estimated average)", "5 years, commencing in 2026", "2027",
           "$4,631,284 a year (fixed sum); $97 for each $100,000 of market value", number=N(8), src=I)
    c.issue("issue-9", "question", "Tallmadge City School District (Summit and Portage)", "School district income tax: 1%, continuing", SD("TALLMADGE CITY SD"), number=N(9),
            text="Shall an annual income tax of one percent (1.00%) on the earned income of individuals residing in the school district be imposed by the Tallmadge City School District, for a continuing period of time, beginning January 1, 2027, for the purpose of current expenses?", src=I)
    c.levy("issue-10", "Stark County District Library (Stark and Summit)", None, "Renewal and increase", "Current expenses (renewal of 2 mills and increase of 0.3 mill).", "2.3 mills", "8 years, commencing in 2027", "2028", est("$14,949,218", "$55"), number=N(10), src=I)
    AK = P("AKRON CITY")
    c.issue("issue-11", "question", "City of Akron", "Charter amendment: Section 101b (rental security deposits and application fees)", AK, number=N(11),
            text="Enact Section 101b to require property owners or operators to permit security deposits for residential rentals to be paid over three or six month periods; require operators to inform tenants of that right, criminalizing failure to notify; ban fees, charges, deposits or other payments before executing rental agreements; and criminalize collecting an application fee for residential rentals.", src=I)
    c.issue("issue-12", "question", "City of Akron", "Charter amendment: Section 100a (anti-discrimination protections; criminal history in housing)", AK, number=N(12),
            text="Enact Section 100a to add the City's existing codified anti-discrimination protections to the Charter; with exceptions for sex offenders and arson offenders, prohibit declining to rent to, or engage in real estate transactions with, an individual on the basis of criminal history, making individuals with criminal histories a protected class for renting, home sales and other real estate transactions; give the Akron Civil Rights Commission jurisdiction over real estate discrimination claims in Akron; and require City Council to enact implementing legislation within 90 days.", src=I)
    c.issue("issue-13", "question", "City of Akron", "Charter amendment: Section 68a (police oversight board and Independent Police Auditor)", AK, number=N(13),
            text="Amend Section 68a to change the composition and appointment process of the citizens' police oversight board (fewer Council appointees; one-third of members selected by the Board from a list provided by a committee of members of qualifying civil rights organizations); set procedures and deadlines for the Mayor, Police Chief and Council to respond to the Independent Police Auditor's recommendations; and authorize the Auditor's office to subpoena records and compel attendance and testimony.", src=I)
    c.issue("issue-14", "liquor", "City of Akron", "Local liquor option: Sunday sales, Akron 4-F (off-premises)", AK, number=N(14), area="Akron precinct 4-F",
            text="Shall the sale of wine and mixed beverages, of the same types as may be legally sold in this precinct on other days of the week, be permitted in this Akron 4-F for consumption off the premises where sold on Sunday?", src=I)
    c.issue("issue-15", "liquor", "City of Akron", "Local liquor option: Oakhill Foodmart", AK, number=N(15), area="Akron precinct 6-C",
            text="Shall the sale of wine and mixed beverages be permitted by Sunrise Petroleum, Inc. doing business as Oakhill Foodmart an applicant for a C2 liquor permit, who is engaged in the business of operating a full-service convenience store and foodmart at 2514 Mogadore Rd., Akron, Ohio 44312, in this precinct?", src=I)
    c.issue("issue-16", "liquor", "City of Akron", "Local liquor option: Oakhill Foodmart (Sunday)", AK, number=N(16), area="Akron precinct 6-C",
            text="Shall the sale of wine and mixed beverages be permitted for sale on Sunday by Sunrise Petroleum, Inc. doing business as Oakhill Foodmart an applicant for a D6 liquor permit who is engaged in the business of operating a full-service convenience store and foodmart at 2514 Mogadore Rd., Akron, Ohio 44312, in this precinct?", src=I)
    BB = P("BARBERTON CITY")
    c.issue("issue-17", "question", "City of Barberton", "Charter amendment: Sections 4.02 and 6.03 (Division of Parks and Recreation)", BB, number=N(17),
            text="Shall Section 4.02 be amended to establish a Division of Parks and Recreation under the direct reporting of the Director of Public Service and shall Section 6.03 be amended to require the Parks and Recreation Commission to serve in an advisory capacity?", src=I)
    c.issue("issue-18", "question", "City of Barberton", "Charter amendment: Section 5.11 (public posting places)", BB, number=N(18),
            text="Shall Section 5.11 be amended to remove the requirement that six (6) public places in the municipality be established if public posting is selected as the medium?", src=I)
    c.issue("issue-19", "question", "City of Barberton", "Charter amendment: Article 7 (non-partisan municipal elections)", BB, number=N(19), text="Shall Article 7 be amended to require non-partisan municipal elections?", src=I)
    c.issue("issue-20", "liquor", "City of Cuyahoga Falls", "Local liquor option: Club 2209 on the Riverfront / Barro di Mario (Sunday)", P("CUYAHOGA FALLS CITY"), number=N(20), area="Cuyahoga Falls precinct 4-C",
            text="Shall the sale of wine and mixed beverages, and spirituous liquor be permitted for sale on Sunday by Calabria, Inc., dba Club 2209 on the Riverfront/Barro di Mario an applicant for a D-6 liquor permit who is engaged in the business of operating a bar at 2209 Front Street, Cuyahoga Falls, Ohio 44221, in this precinct?", src=I)
    GR = P("GREEN CITY")
    for n, sec, text in [
        (21, "Section 4.8 (notice of special Council meetings)", "Shall Section 4.8 of the Charter of the City of Green be amended to replace the option of leaving a copy of the notice at the usual place of residence of the Mayor and Council members and substitute email with read receipt as a form of notification for special Council meetings?"),
        (22, "Section 4.11 (publishing ordinances and notices)", "Shall Section 4.11 of the Charter of the City of Green be amended to eliminate the requirement of the posting of ordinances and resolutions and other public notices in at least five public places within the City and add the Central Administration Building, and electronic/online equivalent of a newspaper of general circulation in the City, or the City's website for 30 days as a method of publication for ordinances, resolutions, and other public notices?"),
        (23, "Section 7.4 (Parks and Recreation Board)", "Shall Section 7.4 of the Charter of the City of Green be amended to clarify the powers and duties of the Parks and Recreation Board?"),
        (24, "Section 8.2 (income tax allocation to parks and recreation)", "Shall Section 8.2 of the Charter of the City of Green be amended to modify the allocation of annual income tax revenue funds to the City Parks and Recreation Program?"),
        (25, "Section 9.2 (publishing Charter Review recommendations)", "Shall Section 9.2 of the Charter of the City of Green be amended to allow Council to use the electronic/online equivalent of a newspaper of general circulation in the City as a method of publication for Charter Review Commission recommendations?"),
        (26, "Section 9.2 (charter review every five years)", "Shall Section 9.2 of the Charter of the City of Green be amended to require the City Charter be reviewed every five (5) years?"),
    ]:
        c.issue(f"issue-{n}", "question", "City of Green", f"Charter amendment: {sec}", GR, number=N(n), text=text, src=I)
    c.issue("issue-27", "question", "City of Hudson", "Natural gas aggregation", P("HUDSON CITY"), number=N(27),
            text="Shall the City of Hudson, Ohio have the authority to aggregate the retail natural gas loads located in the City, and for that purpose, enter into service agreements to facilitate for those loads the sale and purchase of natural gas, such aggregation to occur automatically for eligible local utility customers except where any person is under contract or elects to opt out, all in accordance with Section 4929.26 of the Ohio Revised Code?", src=I)
    c.levy("issue-28", "City of Munroe Falls", P("MUNROE FALLS CITY"), "Additional (replacing an expiring 2 mills)", "General construction, reconstruction, resurfacing, and repair of streets, roads, and bridges.", "2 mills", "10 years, commencing in 2026", "2027", est("$342,816", "$70"), number=N(28), src=I)
    NO = P("NORTON CITY")
    for n, sec, text in [
        (29, "Article II, Section 2.09 (Mayor's salary)", "Change the Mayor's salary rate in the Charter from $11,250 to $15,000, unless otherwise approved by the voters for the next term of office."),
        (30, "Article III, Section 3.08 (Council salaries)", "Change Council members' salary rate from $7,500 to $10,000 and the President of Council's from $8,500 to $11,000, unless otherwise approved by the voters for the next term of office."),
        (31, "Article IV, Section 4.03 (Administrative Officer supervision of Finance and Law)", "Place the Department of Finance and Department of Law under the direct administrative supervision of the Administrative Officer, while preserving the existing appointment and removal provisions and the legally vested fiscal and professional legal duties of those offices."),
        (32, "Article V, Section 5.03.B (Board of Control contract approval)", "Raise the contract amount requiring Board of Control approval from five thousand dollars to ten thousand dollars."),
        (33, "Title of the chief legal officer", "Change the title of the City's chief legal officer from Solicitor to Director of Law, without changing the appointment, qualifications, powers, duties, suspension or removal provisions applicable to that office."),
    ]:
        c.issue(f"issue-{n}", "question", "City of Norton (Summit and Wayne)", f"Charter amendment: {sec}", NO, number=N(n), text=text, src=I)
    ST = P("STOW CITY")
    c.issue("issue-34", "question", "City of Stow", "Ordinance: compensation of the Mayor, Law Director and Finance Director", ST, number=N(34),
            text="Set the base annual salary of the Mayor, Law Director and Finance Director at $100,000 each effective January 2, 2028 (increases of 24%, 23% and 23% over the salaries set in 2011 and 2013), and from January 2, 2029 increase each year by no less than the aggregate of the City's collective bargaining units' annual percentage increase.", src=I)
    c.issue("issue-35", "question", "City of Stow", "Charter amendment: Section 3.06 (Acting Mayor)", ST, number=N(35),
            text="Amend Section 3.06 so that the President of Council, or a member of Council designated by majority vote, becomes Acting Mayor when the Mayor is temporarily absent, inaccessible or unable to serve, or until Council elects a Mayor after a vacancy; if the President of Council cannot serve as Acting Mayor, Council chooses a designee by majority vote; a Council member acting as Mayor gives up Council voting power while doing so.", src=I)
    c.issue("issue-36", "question", "City of Stow", "Charter amendment: new Section 6.08 (Acting Finance Director)", ST, number=N(36),
            text="Add Section 6.08 so that the Assistant Director of the General Division becomes Acting Finance Director when the Finance Director is temporarily absent, inaccessible or unable to serve; if that position is vacant, the Mayor appoints an Acting Finance Director from within the Finance Department.", src=I)
    c.issue("issue-37", "question", "City of Stow", "Charter amendment: new Section 9.07 (Acting Law Director)", ST, number=N(37),
            text="Add Section 9.07 so that the Deputy Law Director becomes Acting Law Director when the Law Director is temporarily absent, inaccessible or unable to serve; if that position is vacant, the Mayor appoints an Acting Law Director from within the Law Department.", src=I)
    c.issue("issue-38", "question", "City of Twinsburg", "Zoning amendment: 2570 Post Road", P("TWINSBURG CITY"), number=N(38),
            text="Shall Ordinance 2026-093 rezoning 3.2 acres of land located at 2570 Post Road (and further identified as Parcel No. 64-02608) from PF (Public Facilities Zone) to R-3 Single Unit Residential Zone Use be approved?", src=I)
    BH = P("BOSTON HEIGHTS VILLAGE")
    c.issue("issue-39", "question", "Village of Boston Heights", "Municipal income tax: 0.25% increase for safety services", BH, number=N(39),
            text="A 0.25% increase in the income tax, effective January 1, 2027, for safety services, including a Safety Service Center for the police department and village offices, updating the fire station, fire and EMS personnel and equipment, and police department operations and personnel.", src=I)
    c.levy("issue-40", "Village of Boston Heights", BH, "Renewal", "General construction, reconstruction, resurfacing and repair of streets, roads, and bridges.", "2.75 mills", "5 years, commencing in 2027", "2028", est("$237,772", "$61"), number=N(40), src=I)
    c.levy("issue-41", "Village of Boston Heights", BH, "Renewal", "Providing and maintaining fire operations.", "0.75 mill", "3 years, commencing in 2027", "2028", est("$64,847", "$17"), number=N(41), src=I)
    MO = P("MOGADORE VILLAGE")
    for n, sec, text in [
        (42, "Article V (Fiscal Officer and Clerk)", "Shall Article V of the Charter of the Village of Mogadore, Ohio be changed and amended to eliminate the appointed office of Clerk-Treasurer and to create the appointed offices of Fiscal Officer to perform the fiscal functions of the Village and Clerk to perform the municipal clerk functions of the Village?"),
        (43, "Article IV, Section 4.03 (Acting Mayor)", "Shall Article IV Section 4.03 of the Charter of the Village of Mogadore, Ohio be changed and amended to clarify the circumstances where the incapacity or absence of the Mayor, or vacancy in the Office of Mayor, require the Council President or other member of Council to serve as the Acting Mayor and/or to preside over Council meetings?"),
        (44, "Article III, Section 3.12 (publishing ordinances online)", "Shall Article III Section 3.12 of the Charter of the Village of Mogadore, Ohio be changed and amended to require that every ordinance or resolution adopted by the Village Council be published by posting a copy of the same on the Village's website, which shall be accessible to the general public, within five (5) days of the effective date of the same, and remain on the Village's website for no less than five (5) years thereafter?"),
        (45, "Article X (Board of Zoning Appeals)", "Shall Article X of the Charter of the Village of Mogadore, Ohio be changed and amended to reduce the number of members of the Village of Mogadore's Board of Zoning Appeals from seven (7) to five (5) members?"),
    ]:
        c.issue(f"issue-{n}", "question", "Village of Mogadore (Summit and Portage)", f"Charter amendment: {sec}", MO, number=N(n), text=text, src=I)
    c.levy("issue-46", "Village of Mogadore (Summit and Portage)", MO, "Renewal and increase", "Fire and emergency medical service personnel and related costs (renewal of 3.5 mills and increase of 1.23 mills).", "4.73 mills", "5 years, commencing in 2027", "2028", est("$500,686", "$135"), number=N(46), src=I)
    c.issue("issue-47", "question", "Village of Peninsula", "Advisory election: short-term home rentals", P("PENINSULA VILLAGE"), number=N(47),
            text="Shall the Village of Peninsula prohibit all short-term home rentals, except when the owner is residing on site at the time of the rental? (Short-term home rentals are defined as home rentals for less than 30 consecutive days.)", src=I)
    TW = [
        (48, "Bath Township", "BATH TWP", "Renewal and increase", "General construction, reconstruction, resurfacing and repair of streets, roads and bridges (renewal of 2 mills and increase of 1.4 mills).", "3.4 mills", "5 years, commencing in 2027", "2028", est("$2,294,616", "$94")),
        (49, "Copley Township", "COPLEY TWP", "Additional", "Fire apparatus, equipment, buildings, firefighting and emergency medical service personnel, and related costs.", "1.7 mills", "3 years, commencing in 2026", "2027", est("$1,378,825", "$60")),
        (50, "Coventry Township", "COVENTRY TWP", "Renewal and decrease", "Township operations under its police contract with the Summit County Sheriff (renewal with a reduction of 0.25 mill).", "4.75 mills", "5 years, commencing in 2027", "2028", est("$1,353,006", "$115")),
        (51, "Coventry Township", "COVENTRY TWP", "Renewal", "Fire apparatus, buildings, firefighters, and ambulance and emergency medical services.", "3.25 mills", "5 years, commencing in 2027", "2028", est("$942,573", "$80")),
        (52, "Coventry Township", "COVENTRY TWP", "Renewal", "Road improvement.", "2.5 mills", "5 years, commencing in 2027", "2028", est("$725,056", "$62")),
        (53, "Coventry Township", "COVENTRY TWP", "Renewal", "Current expenses.", "0.95 mill", "5 years, commencing in 2026", "2027", est("$275,521", "$23")),
        (54, "Northfield Center Township", "NORTHFIELD CTR TP", "Additional", "General construction, reconstruction, resurfacing, and repair of streets, roads, and bridges.", "2 mills", "5 years, commencing in 2026", "2027", est("$485,312", "$70")),
        (55, "Springfield Township", "SPRINGFIELD TWP", "Additional (replacing an expiring 2 mills)", "Fire apparatus, equipment, buildings, firefighting and emergency medical service personnel, and related costs of the Springfield Township Fire Department.", "1.9 mills", "Continuing period of time, commencing in 2026", "2027", est("$786,001", "$67")),
        (56, "Twinsburg Township", "TWINSBURG TWP", "Additional", "General construction, reconstruction, resurfacing, and repair of streets, roads, and bridges.", "1.69 mills", "Continuing period of time, commencing in 2026", "2027", est("$412,593", "$59")),
    ]
    for n, jur, raw, t, purpose, mills, term, fd, e in TW:
        c.levy(f"issue-{n}", jur, P(raw), t, purpose, mills, term, fd, e, number=N(n), src=I)
    return c
