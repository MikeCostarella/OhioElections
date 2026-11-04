// Fallback when the SoS API refuses scripted requests: run this in the Chrome console on
// https://liveresults.ohiosos.gov/ (or with Claude in Chrome's javascript tool). It fetches the
// county list, the contest list, the election summary CSV and every county's contests, and offers
// the bundle as a download; then: python sos.py --bundle "<path to the downloaded file>".
const ELECTION = "2026-11-03";
const j = async (p) => (await fetch(p)).json();
const counties = await j("/Api/v1/Contest/getCountyList");
const contests = await j("/Api/v1/Contest/getContestList");
const summaryCsv = await (await fetch("/Api/v1/Contest/GetElectionSummaryCsv")).text();
const byCounty = {};
for (const c of counties) byCounty[c.name] = await j("/Api/v1/Contest/GetContestsByCounty?countyId=" + c.value);
const bundle = { fetched: new Date().toISOString(), counties, contests, summaryCsv, byCounty };
const a = document.createElement("a");
a.href = URL.createObjectURL(new Blob([JSON.stringify(bundle)], { type: "application/json" }));
a.download = `sos-${ELECTION}.json`;
a.textContent = `Download sos-${ELECTION}.json (${Object.keys(byCounty).length} counties)`;
a.style.cssText = "position:fixed;top:10px;left:10px;z-index:99999;background:#ff0;padding:12px;font:16px sans-serif";
document.body.prepend(a);
a.textContent;
