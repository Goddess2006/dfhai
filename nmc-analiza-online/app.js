/* Analiză vânzări „Magazin online” — preț de listă vs. discount ipotetic (implicit 40%).
   Citește direct tabelele Visual FoxPro (.dbf) ale DistribNet dintr-un folder ales o dată (File System Access API, Chrome/Edge)
   și se resincronizează singur: verifică la câteva secunde dacă tabelele folosite s-au modificat (dată + mărime) și recalculează.
   Nimic nu pleacă din calculator: datele se citesc local, în browser. */
"use strict";
const $ = id => document.getElementById(id);
const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const S = v => v == null ? "" : String(v).trim();
const N = v => { const x = +v; return isFinite(x) ? x : 0 };
const norm = s => S(s).normalize("NFD").replace(/[̀-ͯ]/g, "").toUpperCase().replace(/[^A-Z0-9]/g, "");
const r2 = x => Math.round(x * 100) / 100;
const lei = v => v == null ? "—" : new Intl.NumberFormat("ro-RO", { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(v);
const pct = v => v == null || !isFinite(v) ? "—" : new Intl.NumberFormat("ro-RO", { minimumFractionDigits: 1, maximumFractionDigits: 1 }).format(v * 100) + "%";
const LUNI = ["", "ianuarie", "februarie", "martie", "aprilie", "mai", "iunie", "iulie", "august", "septembrie", "octombrie", "noiembrie", "decembrie"];
const store = { get(k, d) { try { const v = localStorage.getItem("mo_" + k); return v == null ? d : JSON.parse(v) } catch (e) { return d } },
  set(k, v) { try { localStorage.setItem("mo_" + k, JSON.stringify(v)) } catch (e) {} } };
function toast(t) { const el = $("toast"); el.textContent = t; el.classList.add("on"); clearTimeout(toast.t); toast.t = setTimeout(() => el.classList.remove("on"), 3800) }

/* ---------- IndexedDB: păstrează handle-ul folderului între sesiuni ---------- */
function idb() { return new Promise((res, rej) => { const r = indexedDB.open("analiza_online", 1); r.onupgradeneeded = () => r.result.createObjectStore("h"); r.onsuccess = () => res(r.result); r.onerror = () => rej(r.error) }) }
async function idbGet(k) { try { const d = await idb(); return await new Promise(r => { const q = d.transaction("h").objectStore("h").get(k); q.onsuccess = () => r(q.result); q.onerror = () => r(null) }) } catch (e) { return null } }
async function idbSet(k, v) { try { const d = await idb(); return await new Promise(r => { const t = d.transaction("h", "readwrite"); t.objectStore("h").put(v, k); t.oncomplete = () => r(true); t.onerror = () => r(false) }) } catch (e) { return false } }

/* ---------- cititor DBF (FoxPro / dBase), cu citire pe bucăți pentru tabelele mari ---------- */
const CP = { 0x03: "windows-1252", 0x57: "windows-1252", 0xC8: "windows-1250", 0x64: "windows-1250", 0x65: "windows-1250", 0x02: "windows-1250" };
function dbfHead(buf) {
  const v = new DataView(buf), u8 = new Uint8Array(buf);
  const n = v.getUint32(4, true), hl = v.getUint16(8, true), rl = v.getUint16(10, true), cp = v.getUint8(29);
  const fields = []; let off = 1;
  for (let o = 32; o + 32 <= Math.min(hl, buf.byteLength) && u8[o] !== 0x0D; o += 32) {
    let name = ""; for (let i = 0; i < 11 && u8[o + i]; i++) name += String.fromCharCode(u8[o + i]);
    const f = { name: name.trim().toUpperCase(), type: String.fromCharCode(u8[o + 11]), len: u8[o + 16], dec: u8[o + 17], off };
    off += f.len; fields.push(f);
  }
  return { n, hl, rl, enc: CP[cp] || "windows-1250", fields };
}
function readField(f, u8, v, p, dec) {
  switch (f.type) {
    case "C": case "V": return dec.decode(u8.subarray(p, p + f.len)).replace(/\0/g, "").trim();
    case "N": case "F": { const t = String.fromCharCode(...u8.subarray(p, p + f.len)).trim(); return t === "" ? null : parseFloat(t) }
    case "I": return v.getInt32(p, true);
    case "Y": return Number(v.getBigInt64(p, true)) / 10000;
    case "B": return v.getFloat64(p, true);
    case "L": return /[TtYy]/.test(String.fromCharCode(u8[p]));
    case "D": return String.fromCharCode(...u8.subarray(p, p + 8)).trim();
    case "T": { const jd = v.getInt32(p, true); return jd > 0 ? new Date((jd - 2440588) * 864e5).toISOString().slice(0, 10).replace(/-/g, "") : "" }
    default: return null;
  }
}
/* parcurge tabelul pe bucăți (~8 MB) și apelează fn(rând) doar cu câmpurile cerute */
async function dbfScan(file, only, fn) {
  const h = dbfHead(await file.slice(0, Math.min(file.size, 32 + 32 * 255 + 2)).arrayBuffer());
  const F = only ? h.fields.filter(f => only.includes(f.name)) : h.fields, dec = new TextDecoder(h.enc);
  const per = Math.max(1, Math.floor(8e6 / h.rl));
  for (let r0 = 0; r0 < h.n; r0 += per) {
    const a = h.hl + r0 * h.rl, b = Math.min(file.size, h.hl + Math.min(h.n, r0 + per) * h.rl);
    if (a >= file.size) break;
    const buf = await file.slice(a, b).arrayBuffer(), u8 = new Uint8Array(buf), v = new DataView(buf);
    for (let o = 0; o + h.rl <= buf.byteLength; o += h.rl) {
      if (u8[o] === 0x2A) continue; // rând șters
      const row = {}; for (const f of F) row[f.name] = readField(f, u8, v, o + f.off, dec);
      fn(row);
    }
  }
}
async function dbfAll(file, only) { const out = []; await dbfScan(file, only, r => out.push(r)); return out }

/* ---------- sursa: folder (Chrome/Edge, cu sincronizare) sau fișiere încărcate (orice browser) ---------- */
const DB = { dir: null, files: null, tables: null, cfg: store.get("cfg", null), stamp: "", live: true, busy: false };
async function listTables() {
  const T = [];
  async function walk(dir, prefix, depth) {
    for await (const [name, h] of dir.entries()) {
      if (h.kind === "directory") { if (depth < 3 && !/^\.|^(TEMP|TMP)$/i.test(name)) await walk(h, prefix + name + "/", depth + 1); continue }
      if (!/\.dbf$/i.test(name)) continue;
      const file = await h.getFile(); if (file.size < 33) continue;
      try { const hd = dbfHead(await file.slice(0, Math.min(file.size, 32 + 32 * 255 + 2)).arrayBuffer()); T.push({ name: prefix + name, size: file.size, mod: file.lastModified, n: hd.n, fields: hd.fields, get: () => h.getFile() }) } catch (e) {}
    }
  }
  if (DB.dir) await walk(DB.dir, "", 0);
  else if (DB.files) for (const file of DB.files) {
    if (!/\.dbf$/i.test(file.name) || file.size < 33) continue;
    try { const hd = dbfHead(await file.slice(0, Math.min(file.size, 32 + 32 * 255 + 2)).arrayBuffer()); T.push({ name: file.webkitRelativePath ? file.webkitRelativePath.replace(/^[^/]+\//, "") : file.name, size: file.size, mod: file.lastModified, n: hd.n, fields: hd.fields, get: async () => file }) } catch (e) {}
  }
  return T.sort((a, b) => a.name.localeCompare(b.name));
}
const tbase = t => t.name.replace(/^.*\//, "").replace(/\.dbf$/i, "").toUpperCase();
const tbl = n => (DB.tables || []).find(t => t.name === n);
const fieldsOf = n => (tbl(n) || { fields: [] }).fields.map(f => f.name);

/* ---------- detectarea automată a tabelelor și câmpurilor ---------- */
const RX = {
  nr: /^(NRFACT|NRFACTURA|NR_FACT|NR_FACTURA|FACTOUT|NRFACTOUT|NRFAC|NRFACTIES|NRDOC|NR_DOC|NUMAR|NRDOCUMENT)$/,
  id: /^(ID|IDFACT|ID_FACT|IDFACTURA|IDDOC|ID_DOC|IDANTET|NRINT|NRINTERN|NR_INT|CODDOC|NRCRT_FACT|NRUNIC)$/,
  data: /^(DATA|DATAFACT|DATA_FACT|DATAFACTURA|DATADOC|DATA_DOC|DATAF|DATAEM|DATAEMIT)$/,
  cli: /^(CODCLI|COD_CLI|CODPART|COD_PART|CODTERT|CODBENEF|CODCLIENT)$/,
  cname: /^(NUMECLI|NUME_CLI|DENCLI|DEN_CLI|FIRMA|CLIENT|DENPART|NUMEPART|DENUMIRE|NUMECLIENT)$/,
  agent: /^(CODAGENT|COD_AGENT|CODAG|COD_AG|AGENT|CODAGEN|CODVANZ|CODVANZATOR|VANZATOR|NUMEAGENT|DENAGENT|NUME_AGENT|CODREP|AGENTVANZ|CODDELEGAT|CODAGENTV|AG)$/,
  agname: /^(NUMEAGENT|NUME_AGENT|DENAGENT|DEN_AGENT|NUMEAG|DENAG|NUMEPREN|NUMEPRENUME|NUME|DENUMIRE|AGENT)$/,
  cat: /^(CATPRET|CAT_PRET|CATPR|CATEGPRET|LISTAPRET|LISTA_PRET|CODLISTA|NRLISTA|LISTA|TIPPRET|CATEGPR)$/,
  anul: /^(ANULAT|ANULATA|ANULARE|FACT_ANUL|STERS|ANULATAF)$/,
  cod: /^(CODPR|COD_PR|CODART|COD_ART|CODPROD|CODMAT|CODP)$/,
  q: /^(CANTIT|CANT|CANTITATE|CANTFACT|CANTITF)$/,
  pv: /^(PVANZFTVA|PRETFTVA|PVFTVA|PRETVFTVA|PUFTVA|PRET_FTVA|PRETFARATVA|PVANZ|PRETVANZ|PRET|PU|PRETUNIT)$/,
  val: /^(VALFTVA|VAL_FTVA|VALFARATVA|VALOAREFTVA|VALOARE|VALVANZ|VAL)$/,
  pname: /^(DENUMIRE|DENPR|DEN_PR|DENART|DENPROD|DENMAT|DENUM|DEN)$/,
  lname: /^(DENCAT|DENLISTA|DENUMIRE|NUMELISTA|DENCATPRET|NUME|DEN|DENUM|DESCRIERE)$/,
};
const fx = (t, rx) => t ? (t.fields.find(f => rx.test(f.name)) || {}).name || "" : "";
const fxs = (t, rx) => t ? t.fields.filter(f => rx.test(f.name)).map(f => f.name) : [];
const BAD = /MODIF|ISTOR|STERS|INTR|RECEP|NIR|COMAND|OFERT|PROF|TEMP|TMP|BAK|OLD|LOG|ARH/;
function autoDetect(T) {
  const C = { v: 2, defCat: "90" };
  const firstD = t => (t.fields.find(f => f.type === "D" || f.type === "T") || {}).name || "";
  // antete facturi: nr. + dată + client, fără cod articol
  const heads = T.filter(t => fx(t, RX.nr) && (fx(t, RX.data) || firstD(t)) && (fx(t, RX.cli) || fx(t, RX.cname)) && !fx(t, RX.cod) && !/^(CLIENT|CLIENTI|FURNIZ|PRETURI|AGENT|AGENTI)$/.test(tbase(t)))
    .map(t => ({ t, s: (/FACT|IES|VANZ/.test(tbase(t)) ? 4 : 0) - (BAD.test(tbase(t)) ? 6 : 0) - (/AVIZ|METRO|DL/.test(tbase(t)) ? 2 : 0) + (fx(t, RX.agent) ? 3 : 0) + (fx(t, RX.cat) ? 2 : 0) + (fx(t, RX.val) ? 1 : 0) }))
    .sort((a, b) => b.s - a.s || b.t.n - a.t.n);
  const H = heads[0] && heads[0].t;
  // linii: cod articol + cantitate + câmpul de legătură comun cu antetul
  const lineCands = T.filter(t => t !== H && fx(t, RX.cod) && fx(t, RX.q)).map(t => {
    let link = "";
    if (H) { const common = t.fields.map(f => f.name).filter(n => H.fields.some(g => g.name === n));
      link = common.find(n => RX.id.test(n)) || common.find(n => RX.nr.test(n)) || "" }
    const pre = H ? tbase(H).slice(0, 4) : "";
    return { t, link, s: (link ? 6 : 0) + (pre && tbase(t).startsWith(pre) ? 3 : 0) + (/LIN|POZ|DET|CONT|ART|FACT|IES|VANZ/.test(tbase(t)) ? 2 : 0) - (BAD.test(tbase(t)) ? 6 : 0) - (/AVIZ|METRO/.test(tbase(t)) ? 2 : 0) + (fx(t, RX.pv) || fx(t, RX.val) ? 2 : 0) - (/^PRETURI$/.test(tbase(t)) ? 20 : 0) };
  }).sort((a, b) => b.s - a.s || b.t.n - a.t.n);
  const L = lineCands[0];
  if (H) {
    const link = L && L.link ? L.link : fx(H, RX.id) || fx(H, RX.nr);
    C.head = { t: H.name, nr: fx(H, RX.nr), link, data: fx(H, RX.data) || firstD(H), cli: fx(H, RX.cli), cname: fx(H, RX.cname), agent: fx(H, RX.agent), cat: fx(H, RX.cat), anul: fx(H, RX.anul) };
  }
  if (L) { const t = L.t;
    C.lines = { t: t.name, link: L.link || fx(t, RX.id) || fx(t, RX.nr), cod: fx(t, RX.cod), q: fx(t, RX.q), pv: fx(t, RX.pv), val: fx(t, RX.val), cat: fx(t, RX.cat), pname: fx(t, RX.pname), inclTva: false };
    if (!H && (fx(t, RX.data) || firstD(t))) // un singur tabel cu tot (antet repetat pe fiecare linie)
      C.head = { t: t.name, nr: fx(t, RX.nr), link: C.lines.link, data: fx(t, RX.data) || firstD(t), cli: fx(t, RX.cli), cname: fx(t, RX.cname), agent: fx(t, RX.agent), cat: fx(t, RX.cat), anul: fx(t, RX.anul) };
  }
  // clienți
  const ct = T.filter(t => fx(t, RX.cli) && fx(t, RX.cname) && !fx(t, RX.cod) && !fx(t, RX.nr)).map(t => ({ t, s: (/^CLI|CLIENT|PARTEN|TERT/.test(tbase(t)) ? 5 : 0) - (/FURN/.test(tbase(t)) ? 6 : 0) - (BAD.test(tbase(t)) ? 4 : 0) })).sort((a, b) => b.s - a.s || b.t.n - a.t.n)[0];
  if (ct) { const t = ct.t; C.cli = { t: t.name, code: fx(t, RX.cli), name: t.fields.some(f => f.name === "NUMECLI") ? "NUMECLI" : fx(t, RX.cname), agent: fx(t, RX.agent), cat: fx(t, RX.cat) } }
  // agenți: cod + nume, tabel cu AGENT / VANZ în nume
  const at = T.filter(t => /AGENT|VANZATOR|DELEGAT|REPREZ/.test(tbase(t)) && t.fields.length <= 40 && !fx(t, RX.cod) && !fx(t, RX.nr)).sort((a, b) => (/^AGENT/.test(tbase(b)) ? 1 : 0) - (/^AGENT/.test(tbase(a)) ? 1 : 0))[0];
  if (at) { const code = fxs(at, RX.agent).find(n => !/NUME|DEN/.test(n)) || fx(at, /^(COD|ID|NR)$/) || at.fields[0].name;
    C.ag = { t: at.name, code, name: fxs(at, RX.agname).find(n => n !== code) || (at.fields.find(f => f.type === "C" && f.name !== code) || {}).name || "" } }
  // prețuri: schema cunoscută DistribNet — preturi.dbf (CODPR, CATPRET, PRETVANZ cu TVA, PRETVAL + CODVAL=1 → EUR)
  const pt = T.find(t => /^PRETURI$/.test(tbase(t)) && fx(t, RX.cod) && fx(t, RX.cat)) || T.filter(t => fx(t, RX.cod) && fx(t, RX.cat) && fx(t, /^(PRETVANZ|PRET|PRETLISTA|PRET_LISTA)$/) && !fx(t, RX.q)).sort((a, b) => b.n - a.n)[0];
  if (pt) C.price = { t: pt.name, cod: fx(pt, RX.cod), cat: fx(pt, RX.cat), p: fx(pt, /^PRETVANZ$/) || fx(pt, /^(PRET|PRETLISTA|PRET_LISTA)$/), pval: fx(pt, /^PRETVAL$/), cval: fx(pt, /^CODVAL$/), inclTva: true };
  // denumirile listelor de preț: tabel mic cu câmpul listei + o denumire
  if (C.price) { const cf = C.price.cat;
    const lt = T.filter(t => t.name !== C.price.t && t.n < 5000 && t.fields.some(f => f.name === cf) && !fx(t, RX.cod) && !fx(t, RX.nr) && !fx(t, RX.cli)).map(t => ({ t, nm: fx(t, RX.lname) || (t.fields.find(f => f.type === "C" && f.name !== cf) || {}).name })).filter(x => x.nm)
      .sort((a, b) => (/CAT|LIST|PRET/.test(tbase(b.t)) ? 1 : 0) - (/CAT|LIST|PRET/.test(tbase(a.t)) ? 1 : 0))[0];
    if (lt) C.lists = { t: lt.t.name, code: cf, name: lt.nm } }
  // articole (denumiri)
  const pr = T.filter(t => fx(t, RX.cod) && fx(t, RX.pname) && !fx(t, RX.q) && !fx(t, RX.cat)).map(t => ({ t, s: (/PROD|ARTIC|MARF|NOMEN|STOC|MATER/.test(tbase(t)) ? 3 : 0) - (BAD.test(tbase(t)) ? 4 : 0) })).sort((a, b) => b.s - a.s || b.t.n - a.t.n)[0];
  if (pr) C.prod = { t: pr.t.name, cod: fx(pr.t, RX.cod), name: fx(pr.t, RX.pname) };
  return C;
}

/* ---------- parametri de calcul (editabili în pagină) ---------- */
const P = Object.assign({ year: 2026, months: [9, 10, 11], agent: "MAGAZIN ONLINE", excl: "DECO & FLAIR", disc: 40, tva: 21, eur: 5.10, noList: "exclude", interval: 20 }, store.get("params", {}));
const saveP = () => store.set("params", P);

/* ---------- calcul ---------- */
const R = { inv: [], agents: [], excluded: [], stats: {} };
async function compute() {
  const C = DB.cfg, T = DB.tables;
  if (!C || !C.head || !C.lines) { R.inv = []; render(); diag(); return }
  const tv = 1 + P.tva / 100, D = P.disc / 100;
  const get = async n => { const t = tbl(n); return t ? await t.get() : null };
  // tabele mici
  const agMap = {}, cliMap = {}, listName = {}, prodName = {}, price = {};
  if (C.ag && tbl(C.ag.t)) for (const r of await dbfAll(await get(C.ag.t), [C.ag.code, C.ag.name])) agMap[S(r[C.ag.code])] = S(r[C.ag.name]);
  if (C.cli && tbl(C.cli.t)) for (const r of await dbfAll(await get(C.cli.t), [C.cli.code, C.cli.name, C.cli.agent, C.cli.cat].filter(Boolean)))
    cliMap[S(r[C.cli.code])] = { n: S(r[C.cli.name]), ag: C.cli.agent ? S(r[C.cli.agent]) : "", cat: C.cli.cat ? S(r[C.cli.cat]) : "" };
  if (C.lists && tbl(C.lists.t)) for (const r of await dbfAll(await get(C.lists.t), [C.lists.code, C.lists.name])) listName[S(r[C.lists.code])] = S(r[C.lists.name]);
  if (C.prod && tbl(C.prod.t)) await dbfScan(await get(C.prod.t), [C.prod.cod, C.prod.name], r => { prodName[S(r[C.prod.cod])] = S(r[C.prod.name]) });
  if (C.price && tbl(C.price.t)) { const pc = C.price;
    await dbfScan(await get(pc.t), [pc.cod, pc.cat, pc.p, pc.pval, pc.cval].filter(Boolean), r => {
      let v = N(r[pc.p]), eur = false;
      if (!(v > 0) && pc.pval && N(r[pc.pval]) > 0) { v = N(r[pc.pval]) * P.eur; eur = true } // articol cu preț doar în EUR
      if (v > 0) price[S(r[pc.cat]) + "|" + S(r[pc.cod])] = { f: pc.inclTva ? v / tv : v, eur };
    }) }
  // antete în perioadă
  const H = C.head, same = H.t === C.lines.t, mset = new Set(P.months.map(Number)), y = String(P.year);
  const agWant = norm(P.agent), exclWant = P.excl.split(/[;,\n]/).map(norm).filter(Boolean);
  const agName = raw => { const s = S(raw); return agMap[s] || s };
  const inv = new Map(), agents = new Map(), excluded = new Map();
  const onHead = r => {
    if (H.anul && (r[H.anul] === true || N(r[H.anul]) === 1)) return;
    const d = S(r[H.data]); if (d.slice(0, 4) !== y || !mset.has(+d.slice(4, 6))) return;
    const key = S(r[H.link]); if (!key) return;
    const cc = H.cli ? S(r[H.cli]) : "", c = cliMap[cc] || {};
    const client = (H.cname && S(r[H.cname])) || c.n || (cc ? "Client cod " + cc : "");
    const agRaw = H.agent ? S(r[H.agent]) : c.ag || "", ag = agName(agRaw) || "(fără agent)";
    const nrDoc = H.nr ? S(r[H.nr]) : key;
    const a = agents.get(ag) || { n: ag, docs: new Set() }; a.docs.add(nrDoc + "|" + d); agents.set(ag, a);
    if (norm(ag) !== agWant && norm(agRaw) !== agWant) return;
    if (exclWant.some(x => norm(client).includes(x))) { excluded.set(key, { nr: nrDoc, data: d, client }); return }
    if (!inv.has(key)) inv.set(key, { key, nr: nrDoc, data: d, client, cc, ag, cat: (H.cat && S(r[H.cat])) || "", catCli: c.cat || "", lines: [] });
    if (same) onLine(r);
  };
  const L = C.lines;
  const onLine = r => {
    const d = inv.get(S(r[L.link])); if (!d) return;
    const q = N(r[L.q]); const cod = S(r[L.cod]); if (!q && !N(r[L.val])) return;
    let vf = L.val && r[L.val] != null && r[L.val] !== "" ? N(r[L.val]) : q * N(r[L.pv]);
    if (L.inclTva) vf = vf / tv;
    d.lines.push({ cod, n: (L.pname && S(r[L.pname])) || prodName[cod] || "", q, vf, cat: L.cat ? S(r[L.cat]) : "" });
  };
  const hf = [...new Set([H.data, H.link, H.nr, H.cli, H.cname, H.agent, H.cat, H.anul].filter(Boolean))];
  const lf = [...new Set([L.link, L.cod, L.q, L.pv, L.val, L.cat, L.pname].filter(Boolean))];
  await dbfScan(await get(H.t), same ? [...new Set([...hf, ...lf])] : hf, onHead);
  if (!same) await dbfScan(await get(L.t), lf, onLine);
  // evaluare la prețul de listă
  for (const d of inv.values()) {
    let fact = 0, list = 0, fNo = 0, nNo = 0, eur = false, src = "";
    const catOf = l => { if (l.cat) { src = "linie"; return l.cat } if (d.cat) { src = "factură"; return d.cat } if (d.catCli) { src = "client"; return d.catCli } src = "implicită"; return S(C.defCat) };
    const cats = new Set();
    for (const l of d.lines) {
      const cat = catOf(l); cats.add(cat); l.catU = cat;
      const p = price[cat + "|" + l.cod];
      l.pf = l.q ? l.vf / l.q : null;
      if (p) { l.pl = p.f; l.vl = l.q * p.f; l.eur = p.eur; eur = eur || p.eur; fact += l.vf; list += l.vl }
      else { l.pl = null; l.vl = null; fNo += l.vf; nNo++; if (P.noList === "include") { fact += l.vf; list += l.vf } }
    }
    d.catSrc = src; d.cats = [...cats]; d.listN = d.cats.map(c => listName[c] ? `${listName[c]} (${c})` : `lista ${c}`).join(", ");
    d.fact = r2(fact); d.list = r2(list); d.l40 = r2(list * (1 - D)); d.diff = r2(fact - list * (1 - D));
    d.discReal = list ? 1 - fact / list : null; d.fNo = r2(fNo); d.nNo = nNo; d.eur = eur;
    d.factTot = r2(d.lines.reduce((a, l) => a + l.vf, 0));
    d._t = norm([d.nr, d.client, d.listN, d.data].join(" "));
  }
  R.inv = [...inv.values()].sort((a, b) => a.data.localeCompare(b.data) || a.nr.localeCompare(b.nr, "ro", { numeric: true }));
  R.agents = [...agents.values()].map(a => ({ n: a.n, c: a.docs.size })).sort((a, b) => b.c - a.c);
  R.excluded = [...excluded.values()];
  R.priceCount = Object.keys(price).length; R.listName = listName;
  DB.stamp = new Date().toLocaleString("ro-RO");
  render(); diag();
}

/* ---------- afișare ---------- */
const V = { q: "", sort: store.get("sort", { k: "data", d: 1 }), open: new Set(), month: 0 };
function filtered() { const q = norm(V.q); return R.inv.filter(d => (!q || d._t.includes(q)) && (!V.month || +d.data.slice(4, 6) === V.month)) }
function sum(list) { const s = { n: list.length, fact: 0, list: 0, l40: 0, diff: 0, fNo: 0, factTot: 0 }; for (const d of list) for (const k of ["fact", "list", "l40", "diff", "fNo", "factTot"]) s[k] += d[k]; for (const k in s) if (k !== "n") s[k] = r2(s[k]); return s }
function render() {
  const all = R.inv, s = sum(all), D = P.disc;
  $("kpis").innerHTML = all.length ? `
    <div class="kpi"><span>Facturat (fără TVA)</span><b>${lei(s.fact)}</b><small>${s.n.toLocaleString("ro-RO")} facturi · comparabil cu lista</small></div>
    <div class="kpi"><span>La preț de listă</span><b>${lei(s.list)}</b><small>discount real mediu ${pct(s.list ? 1 - s.fact / s.list : null)}</small></div>
    <div class="kpi"><span>Listă −${D}%</span><b>${lei(s.l40)}</b><small>dacă fiecare factură avea −${D}% din listă</small></div>
    <div class="kpi ${s.diff >= 0 ? "pos" : "neg"}"><span>Diferență (facturat − listă −${D}%)</span><b>${s.diff >= 0 ? "+" : ""}${lei(s.diff)}</b><small>${s.diff >= 0 ? `cu −${D}% s-ar fi încasat cu ${lei(s.diff)} lei mai puțin` : `cu −${D}% s-ar fi încasat cu ${lei(-s.diff)} lei mai mult`}</small></div>`
    : `<div class="empty">${DB.cfg && DB.cfg.head ? `Nicio factură pentru agentul „${esc(P.agent)}” în perioada aleasă. Verifică numele agentului (lista de mai jos) sau anul.` : "Conectează folderul bazei DistribNet ca să încep calculul."}</div>`;
  // pe luni
  const months = [...new Set(all.map(d => +d.data.slice(4, 6)))].sort((a, b) => a - b);
  $("months").innerHTML = all.length ? `<table class="t"><thead><tr><th>Luna</th><th class="n">Facturi</th><th class="n">Facturat</th><th class="n">La listă</th><th class="n">Disc. real</th><th class="n">Listă −${D}%</th><th class="n">Diferență</th><th class="n">Fără preț listă</th></tr></thead><tbody>
    ${months.map(m => { const x = sum(all.filter(d => +d.data.slice(4, 6) === m)); return `<tr class="${V.month === m ? "sel" : ""}" data-m="${m}"><td>${LUNI[m]} ${P.year}</td><td class="n">${x.n}</td><td class="n">${lei(x.fact)}</td><td class="n">${lei(x.list)}</td><td class="n">${pct(x.list ? 1 - x.fact / x.list : null)}</td><td class="n">${lei(x.l40)}</td><td class="n ${x.diff >= 0 ? "pos" : "neg"}">${lei(x.diff)}</td><td class="n mut">${lei(x.fNo)}</td></tr>` }).join("")}
    <tr class="tot" data-m="0"><td>Total</td><td class="n">${s.n}</td><td class="n">${lei(s.fact)}</td><td class="n">${lei(s.list)}</td><td class="n">${pct(s.list ? 1 - s.fact / s.list : null)}</td><td class="n">${lei(s.l40)}</td><td class="n ${s.diff >= 0 ? "pos" : "neg"}">${lei(s.diff)}</td><td class="n mut">${lei(s.fNo)}</td></tr></tbody></table>
    <p class="note">Clic pe o lună filtrează lista de facturi. „Fără preț listă” = linii (transport, servicii, articole lipsă din listă) ${P.noList === "include" ? "incluse la valoarea facturată și în coloana „La listă”" : "lăsate în afara comparației"}.</p>` : "";
  // facturi
  const rows = filtered(), k = V.sort.k, dir = V.sort.d;
  rows.sort((a, b) => { const x = a[k], y = b[k]; return (typeof x === "number" ? x - y : String(x).localeCompare(String(y), "ro", { numeric: true })) * dir });
  const th = (key, l, n) => `<th class="${n ? "n " : ""}s" data-k="${key}">${l}${k === key ? (dir > 0 ? " ▲" : " ▼") : ""}</th>`;
  $("invCount").textContent = rows.length ? `${rows.length.toLocaleString("ro-RO")} facturi${V.month ? " · " + LUNI[V.month] : ""}` : "";
  $("inv").innerHTML = rows.length ? `<table class="t inv"><thead><tr>${th("nr", "Factura")}${th("data", "Data")}${th("client", "Client")}${th("listN", "Listă de preț")}${th("fact", "Facturat", 1)}${th("list", "La listă", 1)}${th("discReal", "Disc. real", 1)}${th("l40", "Listă −" + D + "%", 1)}${th("diff", "Diferență", 1)}</tr></thead><tbody>
    ${rows.slice(0, 3000).map(d => `<tr class="row ${V.open.has(d.key) ? "op" : ""}" data-key="${esc(d.key)}"><td>${esc(d.nr)}${d.fact < 0 ? ' <i class="tag">storno</i>' : ""}</td><td>${d.data.slice(6, 8)}.${d.data.slice(4, 6)}.${d.data.slice(0, 4)}</td><td>${esc(d.client)}</td><td>${esc(d.listN)}<small class="mut"> · din ${d.catSrc}</small>${d.nNo ? ` <i class="tag warn" title="${d.nNo} linii fără preț în listă: ${lei(d.fNo)} lei">${d.nNo} fără preț</i>` : ""}${d.eur ? ' <i class="tag">EUR</i>' : ""}</td><td class="n">${lei(d.fact)}</td><td class="n">${lei(d.list)}</td><td class="n">${pct(d.discReal)}</td><td class="n">${lei(d.l40)}</td><td class="n ${d.diff >= 0 ? "pos" : "neg"}">${lei(d.diff)}</td></tr>
      ${V.open.has(d.key) ? `<tr class="det"><td colspan="9"><table class="t sub"><thead><tr><th>Cod</th><th>Denumire</th><th class="n">Cant.</th><th class="n">Preț facturat</th><th class="n">Preț listă</th><th class="n">Disc. real</th><th class="n">Val. facturată</th><th class="n">Val. listă</th><th class="n">Val. listă −${D}%</th></tr></thead><tbody>
        ${d.lines.map(l => `<tr class="${l.pl == null ? "mut" : ""}"><td>${esc(l.cod)}</td><td>${esc(l.n)}${l.pl == null ? ` <i class="tag warn">nu e în lista ${esc(l.catU)}</i>` : ""}${l.eur ? ' <i class="tag">EUR×' + P.eur + "</i>" : ""}</td><td class="n">${l.q.toLocaleString("ro-RO")}</td><td class="n">${lei(l.pf)}</td><td class="n">${lei(l.pl)}</td><td class="n">${l.pl ? pct(1 - l.pf / l.pl) : "—"}</td><td class="n">${lei(l.vf)}</td><td class="n">${lei(l.vl)}</td><td class="n">${l.vl == null ? "—" : lei(l.vl * (1 - D / 100))}</td></tr>`).join("")}
      </tbody></table></td></tr>` : ""}`).join("")}</tbody></table>${rows.length > 3000 ? `<p class="note">Afișez primele 3.000; exportul Excel le conține pe toate.</p>` : ""}` : "";
  // agenți găsiți
  $("agents").innerHTML = R.agents.length ? R.agents.slice(0, 40).map(a => `<button type="button" class="chip ${norm(a.n) === norm(P.agent) ? "on" : ""}" data-ag="${esc(a.n)}">${esc(a.n)} <small>${a.c}</small></button>`).join("") : "";
  $("exclInfo").textContent = R.excluded.length ? `${R.excluded.length} facturi ale agentului excluse (client: ${[...new Set(R.excluded.map(x => x.client))].slice(0, 3).join(", ")}).` : "";
  $("export").disabled = !all.length;
  syncState();
}
function syncState() {
  const on = !!(DB.dir && DB.tables);
  $("dbState").innerHTML = on ? `<span class="dot ${DB.live ? "live" : ""}"></span> Conectat la <b>${esc(DB.dir.name)}</b>${DB.live ? ` · sincronizare automată la ${P.interval} s` : " · sincronizare oprită"}`
    : DB.files ? `<span class="dot"></span> Fișiere încărcate (${DB.tables ? DB.tables.length : 0} tabele) · fără sincronizare automată — reîncarcă fișierele pentru date noi`
      : `<span class="dot off"></span> Neconectat`;
  $("stamp").textContent = DB.stamp ? `Calculat la ${DB.stamp}` : "";
  $("liveBtn").hidden = !on; $("liveBtn").textContent = DB.live ? "Oprește sincronizarea" : "Pornește sincronizarea";
  $("syncBtn").hidden = !(on || DB.files);
  $("connect").textContent = DB.dir ? "Schimbă folderul" : "Conectează folderul bazei";
  $("connect").hidden = !window.showDirectoryPicker;
  $("noFsa").hidden = !!window.showDirectoryPicker;
}

/* ---------- setări bază (tabele + câmpuri) ---------- */
const CFG_DEF = [
  ["head", "Facturi — antet", [["nr", "Nr. factură"], ["link", "Legătură cu liniile"], ["data", "Data"], ["cli", "Cod client"], ["cname", "Nume client"], ["agent", "Agent"], ["cat", "Listă de preț"], ["anul", "Anulată"]]],
  ["lines", "Facturi — linii", [["link", "Legătură cu antetul"], ["cod", "Cod articol"], ["q", "Cantitate"], ["pv", "Preț unitar facturat"], ["val", "Valoare linie (are prioritate)"], ["cat", "Listă de preț pe linie"], ["pname", "Denumire"]]],
  ["cli", "Clienți", [["code", "Cod client"], ["name", "Nume"], ["agent", "Agent"], ["cat", "Listă de preț"]]],
  ["ag", "Agenți", [["code", "Cod agent"], ["name", "Nume agent"]]],
  ["price", "Prețuri de listă", [["cod", "Cod articol"], ["cat", "Listă de preț"], ["p", "Preț (lei)"], ["pval", "Preț EUR"], ["cval", "Cod monedă"]]],
  ["lists", "Denumiri liste", [["code", "Cod listă"], ["name", "Denumire"]]],
  ["prod", "Articole", [["cod", "Cod articol"], ["name", "Denumire"]]],
];
function diag() {
  const C = DB.cfg || {}, T = DB.tables || [];
  if (!T.length) { $("cfg").innerHTML = ""; return }
  const tsel = (g, v) => `<select data-t="${g}"><option value="">— nefolosit —</option>${T.map(t => `<option ${t.name === v ? "selected" : ""} value="${esc(t.name)}">${esc(t.name)} · ${t.n.toLocaleString("ro-RO")} rânduri</option>`).join("")}</select>`;
  const fsel = (g, k, v) => `<select data-g="${g}" data-k="${k}"><option value="">—</option>${fieldsOf((C[g] || {}).t).map(f => `<option ${f === v ? "selected" : ""}>${f}</option>`).join("")}</select>`;
  $("cfg").innerHTML = `<div class="cfggrid">${CFG_DEF.map(([g, l, F]) => `<fieldset><legend>${l}</legend><label>Tabel ${tsel(g, (C[g] || {}).t)}</label>
    ${F.map(([k, fl]) => `<label>${fl} ${fsel(g, k, (C[g] || {})[k])}</label>`).join("")}
    ${g === "lines" ? `<label class="chk"><input type="checkbox" data-g="lines" data-k="inclTva" ${C.lines && C.lines.inclTva ? "checked" : ""}> prețul facturat include TVA</label>` : ""}
    ${g === "price" ? `<label class="chk"><input type="checkbox" data-g="price" data-k="inclTva" ${C.price && C.price.inclTva ? "checked" : ""}> prețul de listă include TVA</label>` : ""}</fieldset>`).join("")}
    <fieldset><legend>Listă implicită</legend><label>Cod listă când factura / clientul nu o au <input data-def value="${esc(C.defCat || "")}"></label>
    <p class="note">Liste găsite în prețuri: ${R.priceCount ? R.priceCount.toLocaleString("ro-RO") + " prețuri" : "—"}${Object.keys(R.listName || {}).length ? " · " + Object.entries(R.listName).slice(0, 12).map(([c, n]) => esc(n + " = " + c)).join(", ") : ""}</p></fieldset></div>
    <div class="row-btns"><button type="button" class="btn" id="cfgAuto">Detectează din nou</button><button type="button" class="btn" id="cfgCopy">Copiază structura bazei</button></div>`;
  $("cfg").querySelectorAll("select[data-t]").forEach(s => s.onchange = () => { const g = s.dataset.t; C[g] = Object.assign({}, C[g] || {}, { t: s.value }); if (!s.value) delete C[g]; saveCfg(true) });
  $("cfg").querySelectorAll("[data-g]").forEach(s => s.onchange = () => { const g = s.dataset.g; C[g] = Object.assign({}, C[g] || {}, { [s.dataset.k]: s.type === "checkbox" ? s.checked : s.value }); saveCfg(false) });
  $("cfg").querySelector("[data-def]").onchange = e => { C.defCat = e.target.value.trim(); saveCfg(false) };
  $("cfgAuto").onclick = () => { DB.cfg = autoDetect(T); saveCfg(true) };
  $("cfgCopy").onclick = () => { const txt = T.map(t => `${t.name} (${t.n} rânduri): ${t.fields.map(f => f.name + ":" + f.type + f.len).join(", ")}`).join("\n");
    (navigator.clipboard ? navigator.clipboard.writeText(txt) : Promise.reject()).then(() => toast("Structura bazei a fost copiată (doar nume de tabele și câmpuri, fără date)"), () => { $("cfg").insertAdjacentHTML("beforeend", `<pre>${esc(txt)}</pre>`) }) };
}
function saveCfg(redraw) { DB.cfg = DB.cfg || {}; store.set("cfg", DB.cfg); if (redraw) diag(); run() }

/* ---------- sincronizare în timp real ---------- */
const sig = () => { const C = DB.cfg || {}; return ["head", "lines", "cli", "ag", "price", "lists", "prod"].map(g => C[g] && C[g].t).filter(Boolean) };
let lastSig = "";
async function fileSig() {
  if (!DB.dir) return "";
  const parts = [];
  for (const n of [...new Set(sig())]) { const t = tbl(n); if (!t) continue; const f = await t.get(); parts.push(n + ":" + f.size + ":" + f.lastModified) }
  return parts.join("|");
}
async function run(force) {
  if (DB.busy) { DB.again = true; return } DB.busy = true; $("busy").hidden = false;
  try {
    if (!DB.tables) { DB.tables = await listTables(); if (!DB.cfg || DB.cfg.v !== 2 || !tbl((DB.cfg.head || {}).t)) { DB.cfg = autoDetect(DB.tables); store.set("cfg", DB.cfg) } }
    lastSig = await fileSig();
    await compute();
  } catch (e) { console.error(e); toast("Nu am putut citi baza: " + e.message) }
  DB.busy = false; $("busy").hidden = true;
  if (DB.again) { DB.again = false; run() }
}
async function tick() {
  if (!DB.live || !DB.dir || DB.busy || document.hidden) return;
  try { if (await DB.dir.queryPermission({ mode: "read" }) !== "granted") return; const s = await fileSig(); if (s && s !== lastSig) { toast("Baza s-a modificat — recalculez"); await run() } else { $("stamp").textContent = `Calculat la ${DB.stamp} · verificat ${new Date().toLocaleTimeString("ro-RO")}` } } catch (e) {}
}
let timer = null;
function startTimer() { clearInterval(timer); timer = setInterval(tick, Math.max(5, +P.interval || 20) * 1000) }
document.addEventListener("visibilitychange", () => { if (!document.hidden) tick() });

/* ---------- conectare ---------- */
async function useDir(dir) { DB.dir = dir; DB.files = null; DB.tables = null; await idbSet("dir", dir); syncState(); await run(); startTimer() }
$("connect").onclick = async () => {
  try { const dir = await window.showDirectoryPicker({ id: "baze-distribnet", mode: "read" }); if (DB.dir && DB.dir.name !== dir.name) { DB.cfg = null; store.set("cfg", null) } await useDir(dir) }
  catch (e) { if (e.name !== "AbortError") toast("Nu am putut deschide folderul: " + e.message) }
};
$("dirfiles").onchange = $("files").onchange = async e => { const fl = [...e.target.files]; if (!fl.length) return; DB.dir = null; DB.files = fl; DB.tables = null; DB.cfg = null; syncState(); await run() };
$("syncBtn").onclick = async () => {
  if (DB.dir) { try { if (await DB.dir.queryPermission({ mode: "read" }) !== "granted" && await DB.dir.requestPermission({ mode: "read" }) !== "granted") { toast("Fără permisiune de citire pentru folder"); return } } catch (e) {} }
  DB.tables = null; await run(); toast("Sincronizat");
};
$("liveBtn").onclick = () => { DB.live = !DB.live; syncState(); if (DB.live) tick() };

/* ---------- parametri ---------- */
function paramsUI() {
  $("pYear").value = P.year; $("pAgent").value = P.agent; $("pExcl").value = P.excl; $("pDisc").value = P.disc; $("pTva").value = P.tva; $("pEur").value = P.eur; $("pNoList").value = P.noList; $("pInt").value = P.interval;
  $("pMonths").innerHTML = LUNI.slice(1).map((m, i) => `<label class="mchk"><input type="checkbox" value="${i + 1}" ${P.months.includes(i + 1) ? "checked" : ""}>${m.slice(0, 3)}</label>`).join("");
}
let deb = null;
const onParam = recalc => { saveP(); clearTimeout(deb); deb = setTimeout(() => recalc ? run() : (R.inv.length ? recomputeLight() : null), 250) };
function recomputeLight() { run() }
$("pYear").oninput = e => { P.year = +e.target.value || P.year; onParam(true) };
$("pAgent").onchange = e => { P.agent = e.target.value.trim(); onParam(true) };
$("pExcl").onchange = e => { P.excl = e.target.value; onParam(true) };
$("pDisc").oninput = e => { P.disc = Math.min(100, Math.max(0, +e.target.value || 0)); onParam(true) };
$("pTva").oninput = e => { P.tva = +e.target.value || 0; onParam(true) };
$("pEur").oninput = e => { P.eur = +e.target.value || 0; onParam(true) };
$("pNoList").onchange = e => { P.noList = e.target.value; onParam(true) };
$("pInt").onchange = e => { P.interval = Math.max(5, +e.target.value || 20); saveP(); startTimer(); syncState() };
$("pMonths").onchange = () => { P.months = [...$("pMonths").querySelectorAll("input:checked")].map(i => +i.value); V.month = 0; onParam(true) };
$("agents").onclick = e => { const b = e.target.closest("[data-ag]"); if (!b) return; P.agent = b.dataset.ag; $("pAgent").value = P.agent; saveP(); run() };
$("q").oninput = e => { V.q = e.target.value; render() };
$("months").onclick = e => { const tr = e.target.closest("tr[data-m]"); if (!tr) return; const m = +tr.dataset.m; V.month = V.month === m ? 0 : m; render() };
$("inv").onclick = e => {
  const h = e.target.closest("th[data-k]"); if (h) { const k = h.dataset.k; V.sort = { k, d: V.sort.k === k ? -V.sort.d : 1 }; store.set("sort", V.sort); render(); return }
  const tr = e.target.closest("tr.row"); if (!tr) return; const k = tr.dataset.key; V.open.has(k) ? V.open.delete(k) : V.open.add(k); render();
};

/* ---------- export Excel ---------- */
$("export").onclick = () => {
  if (!window.XLSX) { toast("Biblioteca Excel nu s-a încărcat"); return }
  const D = P.disc, s = sum(R.inv), wb = XLSX.utils.book_new(), dt = d => `${d.slice(6, 8)}.${d.slice(4, 6)}.${d.slice(0, 4)}`;
  const sumar = [["Analiză vânzări agent", P.agent], ["Perioada", P.months.map(m => LUNI[m]).join(", ") + " " + P.year], ["Clienți excluși", P.excl], ["Discount ipotetic", D + "%"], ["Calculat la", DB.stamp], [],
    ["Luna", "Facturi", "Facturat fără TVA", "La listă fără TVA", "Discount real", `Listă −${D}%`, "Diferență", "Linii fără preț de listă"]];
  for (const m of [...new Set(R.inv.map(d => +d.data.slice(4, 6)))].sort((a, b) => a - b)) { const x = sum(R.inv.filter(d => +d.data.slice(4, 6) === m)); sumar.push([LUNI[m], x.n, x.fact, x.list, x.list ? r2((1 - x.fact / x.list) * 100) / 100 : null, x.l40, x.diff, x.fNo]) }
  sumar.push(["Total", s.n, s.fact, s.list, s.list ? r2((1 - s.fact / s.list) * 100) / 100 : null, s.l40, s.diff, s.fNo]);
  XLSX.utils.book_append_sheet(wb, XLSX.utils.aoa_to_sheet(sumar), "Sumar");
  XLSX.utils.book_append_sheet(wb, XLSX.utils.json_to_sheet(R.inv.map(d => ({ "Factura": d.nr, "Data": dt(d.data), "Client": d.client, "Listă de preț": d.listN, "Listă din": d.catSrc, "Facturat fără TVA": d.fact, "La listă fără TVA": d.list, "Discount real": d.discReal == null ? null : r2(d.discReal * 10000) / 10000, [`Listă −${D}%`]: d.l40, "Diferență": d.diff, "Linii fără preț listă": d.nNo, "Valoare fără preț listă": d.fNo, "Total factură fără TVA": d.factTot }))), "Facturi");
  const L = []; for (const d of R.inv) for (const l of d.lines) L.push({ "Factura": d.nr, "Data": dt(d.data), "Client": d.client, "Cod": l.cod, "Denumire": l.n, "Listă": l.catU, "Cantitate": l.q, "Preț facturat": l.pf == null ? null : r2(l.pf), "Preț listă": l.pl == null ? null : r2(l.pl), "Valoare facturată": r2(l.vf), "Valoare listă": l.vl == null ? null : r2(l.vl), [`Valoare listă −${D}%`]: l.vl == null ? null : r2(l.vl * (1 - D / 100)) });
  XLSX.utils.book_append_sheet(wb, XLSX.utils.json_to_sheet(L), "Linii");
  XLSX.writeFile(wb, `Analiza-${P.agent.replace(/\W+/g, "-")}-${P.year}-${P.months.join("-")}-discount-${D}.xlsx`);
};

/* ---------- pornire ---------- */
(async function boot() {
  paramsUI(); syncState(); render();
  if (!window.showDirectoryPicker) return;
  const dir = await idbGet("dir"); if (!dir) return;
  DB.dir = dir; syncState();
  try { if (await dir.queryPermission({ mode: "read" }) === "granted") { await run(); startTimer() } else $("dbState").innerHTML += ` · <b>apasă „Sincronizează acum” pentru a da din nou acces la folder</b>` } catch (e) {}
  startTimer();
})();
