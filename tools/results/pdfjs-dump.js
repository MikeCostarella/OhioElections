// Paste into the Chrome console (or run with Claude in Chrome's javascript tool) on a page of the
// Board's own site, with PDF_PATH set to the report. It writes the PDF's text into the page as
// <main id="pdftext"><pre>, one line per row with cells joined by " | ", for tools/results/*.py --text.
const PDF_PATH = "/pdfs/Election%20Summary.pdf";
const pdfjs = await import("https://cdnjs.cloudflare.com/ajax/libs/pdf.js/4.4.168/pdf.min.mjs");
pdfjs.GlobalWorkerOptions.workerSrc = "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/4.4.168/pdf.worker.min.mjs";
const buf = await (await fetch(PDF_PATH, { cache: "no-store" })).arrayBuffer();
const doc = await pdfjs.getDocument({ data: buf }).promise;
const pages = [];
for (let i = 1; i <= doc.numPages; i++) {
  const tc = await (await doc.getPage(i)).getTextContent();
  const rows = new Map();
  for (const it of tc.items) {
    if (!it.str.trim()) continue;
    const y = Math.round(it.transform[5]);
    const key = [...rows.keys()].find((k) => Math.abs(k - y) <= 2) ?? y;
    if (!rows.has(key)) rows.set(key, []);
    rows.get(key).push({ x: it.transform[4], s: it.str });
  }
  const lines = [...rows.entries()].sort((a, b) => b[0] - a[0]).map(([, items]) => items.sort((a, b) => a.x - b.x).map((i) => i.s).join(" | "));
  pages.push("=== PAGE " + i + " ===\n" + lines.join("\n"));
}
const main = document.createElement("main"); main.id = "pdftext";
const pre = document.createElement("pre"); pre.textContent = pages.join("\n");
main.appendChild(pre); document.body.prepend(main);
doc.numPages + " pages";
