// Sanity checks for the ballot data in public/data before a commit:
//   every county in index.json has its file, every source id an entry cites
//   exists, every place an entry names is in the county's places list, and
//   ids are unique. Run: npm run check:data
import { readFileSync, existsSync } from "node:fs";
import { join } from "node:path";

const dir = new URL("../public/data/", import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, "$1");
const read = (p) => JSON.parse(readFileSync(join(dir, p), "utf8"));
const problems = [];
const check = (ok, msg) => { if (!ok) problems.push(msg); };

function checkBallot(path, b) {
  const ids = new Set();
  for (const e of [...b.contests, ...b.issues]) {
    check(!ids.has(e.id), `${path}: duplicate id ${e.id}`);
    ids.add(e.id);
    for (const s of e.sources) check(s in b.sources, `${path}: ${e.id} cites unknown source ${s}`);
    for (const p of e.places ?? []) check((b.places ?? []).includes(p), `${path}: ${e.id} names unknown place ${p}`);
  }
  for (const c of b.contests) check(c.candidates.length > 0, `${path}: ${c.id} has no candidates`);
  return b.contests.length + b.issues.length;
}

for (const e of read("elections.json")) {
  const sp = `state/${e.id}.json`;
  check(existsSync(join(dir, sp)), `missing ${sp}`);
  if (existsSync(join(dir, sp))) console.log(`${sp}: ${checkBallot(sp, read(sp))} entries`);
  for (const slug of read("county/index.json")[e.id] ?? []) {
    const cp = `county/${slug}/${e.id}.json`;
    check(existsSync(join(dir, cp)), `missing ${cp}`);
    if (existsSync(join(dir, cp))) console.log(`${cp}: ${checkBallot(cp, read(cp))} entries`);
  }
}
// Results files (data/results/<county>/<election>.json): every id and candidate name must be on the ballot,
// and nothing may be left unmatched by the parser.
function checkResults(path, r, state, local) {
  const contests = new Map([...state.contests, ...local.contests].map((c) => [c.id, c]));
  const issues = new Set([...state.issues, ...local.issues].map((i) => i.id));
  check(["unofficial", "official"].includes(r.status), `${path}: bad status ${r.status}`);
  check(!isNaN(Date.parse(r.asOf)), `${path}: bad asOf ${r.asOf}`);
  for (const [id, c] of Object.entries(r.contests)) {
    const b = contests.get(id);
    check(!!b, `${path}: contest ${id} not on the ballot`);
    if (!b) continue;
    const names = new Set(b.candidates.map((k) => k.name));
    for (const k of c.candidates) check(k.unmatched || names.has(k.name), `${path}: ${id}: candidate "${k.name}" not on the ballot`);
    check(c.candidates.reduce((s, k) => s + k.votes, 0) + (c.writeIn ?? 0) <= c.total + 1, `${path}: ${id}: votes exceed total`);
  }
  for (const id of Object.keys(r.issues)) check(issues.has(id), `${path}: issue ${id} not on the ballot`);
  check(!(r.unmatched?.length), `${path}: unmatched report titles: ${(r.unmatched ?? []).join("; ")}`);
  return Object.keys(r.contests).length + Object.keys(r.issues).length;
}

for (const e of read("elections.json")) {
  const state = read(`state/${e.id}.json`);
  for (const slug of read("county/index.json")[e.id] ?? []) {
    const rp = `results/${slug}/${e.id}.json`;
    if (!existsSync(join(dir, rp))) continue;
    console.log(`${rp}: ${checkResults(rp, read(rp), state, read(`county/${slug}/${e.id}.json`))} totals`);
  }
}

if (problems.length) { console.error(problems.join("\n")); process.exit(1); }
console.log("Ballot data OK");
