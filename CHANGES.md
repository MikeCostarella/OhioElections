# Changes

# OhioElections — first build (Oct 30, 2026)

- New fleet app: React 18 + TypeScript + Vite PWA, hamburger menu (View / County / Links), build stamp, GitHub Pages deploy.
- One statewide app with county-scoped hash routes (`#/<county>/<election>/<view>/<place>`) so OhioCounties, CurrentElectionStatistics and the Voters apps can deep-link.
- 2026 General Election (Nov 3): the statewide ballot for all 88 counties — Governor/Lt. Governor, Attorney General, Auditor, Secretary of State, Treasurer, U.S. Senate, two Ohio Supreme Court seats, and State Issue 3 (voter photo ID).
- Trumbull County full ballot from the Board's candidate list, issues running list and 46-day notice: 9 county/district contests and 35 local questions and issues (22 tax levies, 8 questions, 5 liquor options), each linked to its source PDF.
- "Where you live" filter for Trumbull's 35 cities, villages and townships; kind filter (levies / questions / liquor options) and search over the local issues.
- Results view links to the Board's results page and the Secretary of State's 2026 results; outcomes get loaded after the canvass.
- `npm run check:data` validates the ballot files (sources, places, unique ids, index) and runs before every deploy.
- Other counties show the statewide ballot and a link to their Board until their local data is added.

Data notes (Trumbull):
- The Newton Falls Village photo-traffic-enforcement referendum is on the Board's issues list but not its 46-day notice; it is included and marked.
- Casa Angel's liquor options: the issues list gives Cortland precinct F, the notice gives H; shown as F with a note.
- The candidate list prints the commissioner term as "1/1/25"; the 46-day notice's "FTC 1/1/2027" is used.

# Oct 30, 2026 (later)

- "Related apps" row under the county picker: the county's Voters app, Election Statistics and the Ohio Counties hub as labelled buttons, so the way back to the rest of the fleet is obvious. The Board of Elections links (View your ballot, Where do I vote?) stay as plain links beside the view tabs. The menu keeps its links too.

# Oct 30, 2026 (six more counties)

- Full ballots for Mahoning, Columbiana, Ashtabula, Lake, Cuyahoga and Geauga, each from that county Board of Elections' own documents: Mahoning's filings list, Columbiana's pre-election zero report, Ashtabula's candidate list and issues sheet, Lake's candidate list and certified issues, Cuyahoga's candidate list and issues list (105 issues, ballot wording verbatim).
- "Where you live" for those counties is computed from each county's SoS voter file (in its *CountyVoters repo): a congressional, state rep or state senate district, or a school levy, shows for a city, village or township when any of its voters are in it. New `tools/ballots/` holds the generator (`place_summary.py`, one spec per county, `run.py`).
- Special districts whose boundaries aren't in the voter file (Ashtabula's park and ambulance districts, Cuyahoga County Council districts) stay listed for every place, marked "boundaries not mapped".
- Levy cards show the Board's collection estimate ("$X a year; $Y for each $100,000"); levy fields the Board doesn't give are left out.
- Statewide: Greg Levy (other-party) added to the U.S. Senate race. He is on the Columbiana, Lake, Ashtabula and Cuyahoga Boards' lists; the Trumbull 46-day notice and the Mahoning filings list leave him out.
- Source links are shortened to the county and document ("Lake candidate list"); the full title is in the tooltip.
- Geauga from all 91 of the Board's official precinct sample ballots (downloaded with a one-off script). Its "Where you live" comes from the ballots themselves. Geauga reuses issue numbers across school districts (Issue 4 is Berkshire's income tax in 13 precincts and Kirtland's levy in one; Issue 5 is Cardinal's levy in 9 and Mentor's in one), so each is listed separately.

# Oct 30, 2026 (Summit, Stark, Portage, Medina, Lorain)

- Full ballots for Summit, Stark, Portage, Medina and Lorain (11 counties with local data now, plus Trumbull's original):
  - Summit: the Board's candidate list and 60-day issue synopsis (20 contests, 53 issues).
  - Stark: the Board's candidate list and numbered issues list (15 contests, 29 issues).
  - Portage: the Board's updated 46-day notice (11 contests, 29 issues, including four Mogadore charter amendments).
  - Medina: the Board's 46-day notice (10 contests, 35 issues, including Rittman's 15 charter amendments).
  - Lorain: the Board's certified candidate and issues lists plus its 46-day notice for precincts (10 contests, 35 issues).
- "Where you live" comes from each county's SoS voter file, as before. Stark's file lists townships by bare name ("JACKSON"); the generator adds "Township" (`County(bare=...)`). Odd SoS names are renamed: Summit's NORTHFIELD CTR TP and SAGAMORE HLS TWP, Portage's SHALERSVILLE TOWNSHP, Lorain's ROCHESTER TWP & VIL.
- Stark's fire and road districts are shown for their township. The Wayne County JVSD levy (on Stark's list with no issue number) is marked "boundaries not mapped".

# Oct 30, 2026 (Franklin, Hamilton, Montgomery, Lucas, Butler)

- Full ballots for Franklin, Hamilton, Montgomery, Lucas and Butler (16 counties with local data now, plus Trumbull's original), each from the Board's 46-day FWAB notice, checked against its candidate and issues lists:
  - Franklin: 28 contests, 50 issues (19 liquor options; three unnumbered items: Delaware Area Career Center levy, Pickerington LSD income tax, Pickerington Library levy). The notices of election for individual issues supplied ballot wording and collection estimates.
  - Hamilton: 28 contests, 30 issues. The Board's ballot-issues document supplied the full wording and estimates.
  - Montgomery: 18 contests, 22 issues.
  - Lucas: 15 contests, 27 issues. The Board's documents are Google Drive files linked from lucascountyohiovotes.gov.
  - Butler: 16 contests, 16 issues.
- `lib.py`: precinct-split places renamed to one display name (Hamilton's Silverton A/B/C and St. Bernard 1-A..4-A, Lucas's Washington 1/2 and Waterville A/B) are listed once.

Data notes:
- Franklin's SoS voter file has empty school-district columns, so Franklin's school and special-district issues are placed by matching the 46-day notice's precincts to the voter file's precincts (typed in the spec). Small slices of Lithopolis, Pickerington and Brice that sit in Madison and Truro township precincts are included in those townships' levies.
- Where the 46-day notice lists precincts the voter file doesn't place in a district, the place is added by hand (Montgomery: West Carrollton in Miamisburg CSD Issue 5, New Lebanon in Jackson Twp Issue 24, Dayton in Jefferson Twp Issue 25; Butler: St. Clair Twp in Senate 5 / House 40; Lucas: Harding Twp in Evergreen LSD Issue 4, Harding Twp and Ottawa Hills in Toledo CSD Issue 9).
- Hamilton: Silverton and St. Bernard are shown as villages, as every Board document calls them. Issue 17 (Madeira D Sunday sales) was withdrawn on Sep 24 and is left out. Where the 46-day notice and the later ballot wording differ (Forest Park Issue 14 additional, Issue 10 renewal and increase, Fairfax 0.96 mill), the ballot wording is used.
- Butler: in the Court of Appeals seat starting 1/1/2027, Republican Matthew Byrne withdrew on 9/16 (his votes won't count); write-in Willa Concannon is the only active candidate. Butler's documents give only type, rate and term for issues, so its charter amendments have no ballot text and its levies no estimates.
- Lucas: the Swanton Public Library levy (Fulton and Lucas) is "boundaries not mapped". QuikTrip's liquor option (Issue 11) is "wine and mixed beverages" on the notice and "Sunday sales" on the issue list; the notice's wording is used.
- Franklin has no Issue 39 in any Board document.

# Oct 30, 2026 (fresh ballot data)

- Ballot data (`data/**`) is no longer precached by the service worker. It is fetched network-first (cached copy used offline), so newly added counties show right after a deploy instead of after the old service worker is replaced. Previously a browser that had opened the app earlier kept showing "Only the statewide races..." for counties added since.

# Oct 30, 2026 (Warren, Delaware, Clermont, Licking, Greene)

- Full ballots for Warren, Delaware, Clermont, Licking and Greene (21 counties with local data now, plus Trumbull's original), each from the Board's 46-day FWAB notice:
  - Warren: 10 contests, 6 issues. The Board's per-issue ballot-language PDFs gave wording, estimates and first-due years.
  - Delaware: 11 contests, 28 issues (12 liquor options). The 46-day notice (revised Oct 2) is the Board's only posted ballot document.
  - Clermont: 8 contests, 8 issues. The 46-day notice (revised Sep 15) is the Board's only posted ballot document, plus its withdrawal notice for Matthew Byrne.
  - Licking: 9 contests, 28 issues, checked against the certified candidate list and filed-issues list.
  - Greene: 10 contests, 27 issues, checked against the candidate list and questions-and-issues list.

Data notes:
- Delaware, Clermont and Licking don't number their local issues in any posted Board document; those issues have descriptive ids and a note pointing to the sample ballot for the numbers. Greene leaves eight items unnumbered (two Sunday liquor options, Kettering's five charter amendments, Southeastern Local's income tax); they are marked "Unnumbered in Greene County".
- 12th District Court of Appeals (Warren, Clermont, as in Butler): Republican Matthew Byrne withdrew; write-in Willa Concannon is the only active candidate.
- Warren Issue 4 (Franklin City Schools income tax) is on the Board's issues list but not its 46-day notice; it is sourced to the issues list. The voter file's "BUTLER VILLAGE" is Butlerville.
- Greene: the SoS voter file labels Southeastern Local (Clark) voters "SOUTHEAST LOCAL SD (PORTAGE)"; the spec uses that label. Issue 20 (Miami Township fire/EMS, 0.8 mill) is "5 years" and "CPT" on the Board's list; it is shown as continuing.
- Clermont: the U.S. Grant career center issues are placed from the notice's precinct list (career center districts aren't in the voter file). Clermont and Delaware levies give rate and term only (no estimates).
- Delaware: the notice names precincts by number; they match the Board's precinct names in alphabetical order (checked against the voter file). Township levies that reach into a city or village (Berlin, Concord, Orange) include that place, with the exact precincts in the area text.
- Licking: Heath is added to House 68 by hand (the notice lists a Heath precinct the voter file puts elsewhere). Obvious typos in the Board's issue wording are corrected.

# Oct 30, 2026 (Fairfield, Clark, Wood, Richland, Wayne)

- Full ballots for Fairfield, Clark, Wood, Richland and Wayne (26 counties with local data now, plus Trumbull's original), each from the Board's 46-day FWAB notice:
  - Fairfield: 8 contests, 14 issues, checked against the certified candidates and issues list.
  - Clark: 11 contests, 36 issues (12 New Carlisle liquor options). The notice is the Board's only posted ballot document.
  - Wood: 10 contests, 24 issues, checked against the certified candidate list and Q&I list. The notice is a scanned PDF (read with OCR); its numeric precinct codes were matched to names using the Board's May 2026 precinct results.
  - Richland: 9 contests, 30 issues. The notice is the only Board document readable without the lookup search form.
  - Wayne: 11 contests, 42 issues, checked against the Board's 256-page all-precinct sample ballots. Includes the Doylestown and Chippewa Township merger questions and their merger-commission elections (vote for up to 5; new "Township offices" group).

Data notes:
- None of the five print local issue numbers (Wayne numbers only State Issue 3); issues have descriptive ids and the sample-ballot note.
- Shared issues reuse the neighbouring county's ids and wording: Fairfield's Pickerington LSD/library and Columbus Issues 8–9 (Franklin) and Southwest Licking/Pataskala library/Buckeye Lake (Licking); Clark's Southeastern LSD income tax (Greene); Wayne's Rittman charter amendments (Medina), Norton charter amendments (Summit), Wayne JVSD (Stark) and Canaan fire (Medina).
- Rittman amendment #8 (Section 6.05): Medina's notice says the Law Director must be an "attorney-in-fact", Wayne's says "attorney-at-law"; each county's file follows its own Board.
- Wood's voter file splits townships into precinct pieces (Lake Twp East/Latcha/North/Union, Perrysburg Twp Belmont/…/PRBG Fallen Timbers, Portage West, …); each is renamed to its township. Where the notice's congressional and House precinct lists disagree with the voter file, the voter file is used. Herringshaw withdrew from the commissioner race (Ryan E. Lee is the Republican).
- Wayne: the SoS file's "FREDERICKTOWN VILLAGE" is Fredericksburg. Burbank has two identical 3-mill current-expense renewals; both are on the ballot.
- Clark: Harmony Township's two 1-mill EMS renewals and Bethel Township's three 2-mill fire renewals differ only in the amount collected; each is noted. The probate judge's term start isn't in the notice and is left off.
- Richland: Galion's two council-term questions apply to its small Richland piece (precinct Sandusky split 3) and are shown under Sandusky Township. The Village of Lucas income tax prints "commencing 1/1/2026", kept as printed.

# Oct 30, 2026 (Miami, Allen, Tuscarawas, Muskingum, Ross, Erie, Hancock, Scioto, Belmont, Jefferson)

- Full ballots for ten more counties (36 with local data now, plus Trumbull's original), each from the Board's 46-day FWAB notice:
  - Miami: 9 contests, 13 issues, plus the Board's separate notice for the Piqua special election held the same day (data-center charter amendment and three recall questions).
  - Allen: 6 contests, 10 issues (notice posted as a Dropbox file linked from the Board's election page).
  - Tuscarawas: 9 contests, 27 issues, checked against the certified candidates and issues list.
  - Muskingum: 9 contests, 18 issues.
  - Ross: 8 contests, 9 issues, checked against the candidate list (scanned, read with OCR) and issues list; Waverly CSD and Miami Trace LSD details from the Pike and Fayette Boards' notices.
  - Erie: 7 contests, 22 issues, checked against the candidate and issue filings.
  - Hancock: 8 contests, 7 issues, checked against the Board's candidate and issues lists (Google Docs).
  - Scioto: 9 contests, 13 issues, with wording and estimates from the Board's precinct sample ballots.
  - Belmont: 10 contests, 17 issues.
  - Jefferson: 9 contests, 18 issues, checked against the candidate list, issue list and all 92 precinct sample ballots.

Data notes:
- Only Tuscarawas, Erie and Jefferson number their local issues; the others use descriptive ids and the sample-ballot note.
- 5th District Court of Appeals (Matthew George): on the other 5th District counties' ballots but in neither Tuscarawas document, so it is not listed for Tuscarawas.
- 4th District Court of Appeals: Scioto's 46-day notice lists Peter B. Abele, but its sample ballots (updated Oct 12) and Ross's Oct 8 candidate list have Jayme Hartley Fountain (REP) vs Todd L. Grace (DEM); both counties use the latter.
- Miami: Piqua's Ward 1, 3 and 5 successor candidates weren't named in the special-election notice and aren't listed. Montgomery's City of Union income tax (Issue 21) is not on Miami's notice although 21 Union voters live in Miami County; not added.
- Ross: Dan D. Cryder (commissioner) is on the Oct 5 notice but not the Oct 8 candidate list; left out.
- North Baltimore LSD income tax: Hancock's full ballot wording says it renews a tax expiring at the end of 2027; Wood's entry follows Wood's shorter issues list.
- Erie's Vermilion items reuse Lorain's titles and wording under Erie's own issue numbers.
- Barnhill (Tuscarawas) and Rarden (Scioto) vote on surrendering their village corporate powers. Tuscarawas Issue 4 is a Claymont CSD levy decrease by petition.
- Renames: Allen's reversed township names ("Township Sugar Creek"), Muskingum's "FRAZEYBURG" (Frazeysburg), Jefferson's "MT PLEASANT TWP".
- Misprints kept out: Belmont's Holloway levy "$42,000 for each $100,000" (only the annual figure is shown); Jefferson's 9-1-1 levy years follow the issue list and ballots, not the notice.

# Oct 30, 2026 (Marion, Union, Knox, Athens, Washington, Pickaway, Sandusky, Huron, Lawrence, Seneca)

- Full ballots for ten more counties (46 with local data now, plus Trumbull's original), each from the Board's 46-day FWAB notice, cross-checked against precinct sample ballots wherever lookup.boe.ohio.gov opened (Union 87, Pickaway 65, Washington 64, Lawrence 99 ballot styles; Huron, Knox, Seneca by sample):
  - Marion: 8 contests, 12 issues (notice only).
  - Union: 7 contests, 15 issues (notice at unioncountyohio.gov; wording and estimates from the ballots).
  - Knox: 8 contests, 16 issues.
  - Athens: 8 contests, 28 issues (Issues 1, 2, 4–29), wording from the Board's notices of election.
  - Washington: 9 contests, 7 issues.
  - Pickaway: 8 contests, 16 issues (incl. Ashville's EdgeConneX data-center referendum).
  - Sandusky: 10 contests, 22 issues (the Board publishes a .docx notice, .xlsx candidate list, .txt issues list and all 61 sample ballots on sanduskycountyoh.gov).
  - Huron: 10 contests, 22 issues.
  - Lawrence: 8 contests, 15 issues (8 liquor options).
  - Seneca: 6 contests, 6 issues.

Data notes:
- Only Athens numbers its local issues; the rest use descriptive ids and the sample-ballot note.
- 4th District Court of Appeals: the Washington and Pickaway notices (like Scioto's) list Peter B. Abele, but every sample ballot has Jayme Hartley Fountain (REP) vs Todd L. Grace (DEM); all 4th District counties use the ballots.
- Ross: the Miami Trace LSD renewal is a fixed sum of $1,900,000 a year (about 2.2 mills, per the Pickaway ballot), not "1.9 mills"; corrected.
- Shared items reuse ids and wording: South-Western CSD bond (Franklin Issue 6, Pickaway), DACC (Delaware, Union, Marion), Miami Trace (Ross, Pickaway), Fostoria (Wood, Hancock, Seneca), Green Springs fire and Old Fort LSD (Seneca, Sandusky), Bellevue parks (Erie, Sandusky, Huron), Plymouth cemetery and South Central LSD (Richland, Huron), Loudonville-Perrysville and its library (Richland, Knox).
- Where the ballots and the notice differ, the ballots are used: Huron's Norwalk fire levy is 0.9 mill (notice ".09"); Pickaway's Deercreek road levy amounts and years; Union's Northern Union fire levy also covers Jackson and York townships; Lawrence's Fayette Twp fire levy also covers South Point; Knox's 0.8-mill renewal is the Loudonville library's.
- Voter-file names: Sandusky's Fremont, Clyde and Bellevue precinct pieces are merged; Riley Township's voters are coded as Rice Township (Riley has no place of its own; neither has a local issue). Knox's "GANN VILLAGE" is Brinkhaven. Marion's and Lawrence's "TWP." names and Marion's LaRue are renamed. Lawrence's file calls Fairland Local "FAIRLAWN LOCAL SD (SHELBY)".

