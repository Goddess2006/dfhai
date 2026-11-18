/* Foaia „NMC Parteneri”: importă lista de prețuri (ex. NMC05.10.26) și clienții din exportul programului de gestiune
   (Excel .xlsx/.xls, CSV sau tabele .dbf), îi păstrează doar în acest browser și oferă căutare de clienți.
   Inserat de build.py în pagină; folosește store, norm, num, fmt, conv, S, B, renderAll, fillForm, toast. */
const NP_FIELDS = {
  price: [
    ["c","Cod articol",1,/^cod$|^cod ?art|^cod ?produs|^cod ?intern|^simbol|^sku|^model|^cod/],
    ["n","Denumire",1,/denumire|^den |^den$|^nume|articol|produs/],
    ["u","UM",0,/^u ?m$|^um$|unitate|^u m /],
    ["p","Preț",1,/pret|price|valoare|^pu$/],
    ["list","Coloana cu numele listei de preț (dacă tabelul are mai multe liste)",0,/lista|tip ?pret|nume ?list|cod ?list/],
    ["k","Grupă / categorie",0,/grupa|categ|clasa|familie|gestiune/]
  ],
  client: [
    ["c_nume","Denumire client",1,/denumire|^nume|client|partener|firma/],
    ["c_cui","CUI / CNP",0,/^cui|cod ?fisc|^cif|cnp|cod ?unic/],
    ["c_reg","Nr. Reg. Com.",0,/reg ?com|registr|nr ?ord|onrc|^j$/],
    ["adr","Adresă",0,/adresa|sediu|strada/],
    ["loc","Localitate",0,/localit|oras/],
    ["jud","Județ",0,/judet/],
    ["c_tel","Telefon",0,/telefon|^tel|phone|mobil/],
    ["c_email","E-mail",0,/mail/],
    ["c_pers","Persoană de contact",0,/persoan|contact|delegat|reprezentant/]
  ]
};
const LIST_HINT = /nmc\s*0?5[.\-_ ]?10[.\-_ ]?(20)?26/i;
const SVC_RX = /montaj|manopera|manoperă|serviciu|servicii|prestar|transport|livrare|randare|consultan|proiectare/i;
const normH = s => norm(String(s)).replace(/[^a-z0-9]+/g," ").trim();
const npCache = {};
function npData(kind){ if(!(kind in npCache)) npCache[kind]=store.get("np_"+kind); return npCache[kind] }
function npSave(kind,v){ npCache[kind]=v; try{ localStorage.setItem("np_"+kind, JSON.stringify(v)); return true }catch(e){ return false } }
function pnum(v){
  if(typeof v==="number") return v;
  let s=String(v??"").trim().replace(/\s|lei|ron/gi,"");
  if(/,\d{1,4}$/.test(s)) s=s.replace(/\./g,"").replace(",","."); else s=s.replace(/,/g,"");
  const x=parseFloat(s); return isFinite(x)?x:NaN;
}
const dRo = iso => iso ? new Date(iso).toLocaleDateString("ro-RO") : "";
function npLoadCatalog(){
  const d=npData("price"); B.catalog = d ? d.items : []; B.listName = d ? d.name : "";
  B.catalog.forEach(p=>{ if(!p._t){ p._c=norm(p.c).replace(/[\s.]/g,""); p._t=norm(p.c+" "+p.n+" "+p.k) } });
}
function npStatus(){
  const p=npData("price"), c=npData("client");
  $("gsPrice").textContent = p ? `Listă de prețuri: ${p.name} · ${p.items.length.toLocaleString("ro-RO")} articole` : "Nicio listă de prețuri importată";
  $("gsPriceInfo").innerHTML = p ? `importată la ${dRo(p.date)} din ${esc(p.file)} · prețuri ${p.inclTva?"cu":"fără"} TVA în fișier` : `<span class="warn">Exportă din gestiune lista NMC05.10.26 (Excel, CSV sau DBF) și importă fișierul aici.</span>`;
  $("gsCli").textContent = c ? `Clienți: ${c.items.length.toLocaleString("ro-RO")}` : "Niciun client importat";
  $("gsCliInfo").textContent = c ? `importați la ${dRo(c.date)} din ${c.file}` : "Exportă lista de clienți din gestiune și importă fișierul aici.";
  $("impPrice").textContent = p ? "Actualizează lista de prețuri" : "Importă lista de prețuri";
  $("impCli").textContent = c ? "Actualizează clienții" : "Importă clienții";
}

/* ---------- import ---------- */
let IMP = null;
$("impPrice").onclick=()=>{ $("impFile").dataset.kind="price"; $("impFile").value=""; $("impFile").click() };
$("impCli").onclick=()=>{ $("impFile").dataset.kind="client"; $("impFile").value=""; $("impFile").click() };
$("impFile").addEventListener("change", async e=>{
  const f=e.target.files[0]; if(!f) return;
  try{
    const buf=await f.arrayBuffer();
    const isText=/\.(csv|txt)$/i.test(f.name); // CSV: citim textul brut, ca „36,50” să nu devină 3650
    const wb=isText ? XLSX.read(new TextDecoder(/\uFFFD/.test(new TextDecoder().decode(buf))?"windows-1250":"utf-8").decode(buf),{type:"string",raw:true})
                    : XLSX.read(buf,{type:"array",cellDates:true,codepage:1250});
    IMP={kind:e.target.dataset.kind, file:f.name, wb, sheet:null};
    const names=wb.SheetNames, kind=IMP.kind;
    IMP.sheet = names.find(n=>kind==="price"?LIST_HINT.test(n)||/pret|articol|stoc|nomencl/i.test(n):/client|partener|tert/i.test(n))
      || names.slice().sort((a,b)=>rowsOf(wb.Sheets[b]).length-rowsOf(wb.Sheets[a]).length)[0];
    drawMap();
  }catch(err){ toast("Fișierul nu a putut fi citit: "+err.message) }
});
function rowsOf(ws){ return XLSX.utils.sheet_to_json(ws,{defval:"",raw:true}) }
function guess(headers,rx,taken){ return headers.find(h=>!taken.has(h)&&rx.test(normH(h))) || "" }
function drawMap(){
  const ws=IMP.wb.Sheets[IMP.sheet]; IMP.rows=rowsOf(ws);
  IMP.headers=[...new Set(IMP.rows.slice(0,50).flatMap(r=>Object.keys(r)))].filter(h=>!/^__EMPTY/.test(h)||IMP.rows.some(r=>r[h]!==""));
  const F=NP_FIELDS[IMP.kind], taken=new Set();
  IMP.map={}; [...F].sort((x,y)=>(y[0]==="list")-(x[0]==="list")).forEach(([k,,,rx])=>{ const g=guess(IMP.headers,rx,taken); if(g){taken.add(g)} IMP.map[k]=g });
  if(IMP.kind==="price"){ // preferă coloana de preț de vânzare / cu numele listei
    const pc=IMP.headers.filter(h=>h!==IMP.map.list&&/pret|price/.test(normH(h)));
    IMP.map.p = pc.find(h=>LIST_HINT.test(h)) || pc.find(h=>/vanz|lista|partener/.test(normH(h))) || IMP.map.p;
    IMP.inclTva = /tva|cu tva/.test(normH(IMP.map.p||"")) && !/fara/.test(normH(IMP.map.p||""));
  }
  const opt=(sel)=>`<option value="">— nu există —</option>`+IMP.headers.map(h=>`<option ${h===sel?"selected":""}>${esc(h)}</option>`).join("");
  const sheets=IMP.wb.SheetNames.length>1?`<label>Foaie / tabel<select id="impSheet">${IMP.wb.SheetNames.map(n=>`<option ${n===IMP.sheet?"selected":""}>${esc(n)}</option>`).join("")}</select></label>`:"";
  $("impMap").innerHTML=`
    <b>${IMP.kind==="price"?"Import listă de prețuri":"Import clienți"} din ${esc(IMP.file)} · ${IMP.rows.length.toLocaleString("ro-RO")} rânduri</b>
    <span style="color:var(--muted);font-size:12.5px">Verifică ce coloană corespunde fiecărui câmp. Câmpurile marcate cu * sunt obligatorii.</span>
    <div class="grid">${sheets}${F.map(([k,l,req])=>`<label>${esc(l)}${req?" *":""}<select data-f="${k}">${opt(IMP.map[k])}</select></label>`).join("")}
      ${IMP.kind==="price"?`<label id="listValBox" ${IMP.map.list?"":"hidden"}>Lista de preț folosită<select id="listVal"></select></label>
      <label class="chk"><input type="checkbox" id="inclTva" ${IMP.inclTva?"checked":""}> Prețurile din fișier includ TVA</label>`:""}
    </div>
    <div class="prev" id="impPrev"></div>
    <div class="confirm"><button type="button" class="btn primary" id="impGo">Încarcă</button><button type="button" class="btn" id="impCancel">Renunț</button><span id="impMsg" style="color:var(--muted);font-size:12.5px"></span></div>`;
  $("impMap").hidden=false;
  $("impMap").querySelectorAll("select[data-f]").forEach(s=>s.onchange=()=>{ IMP.map[s.dataset.f]=s.value; if(s.dataset.f==="list"){fillListVals();} preview() });
  if($("impSheet")) $("impSheet").onchange=e=>{ IMP.sheet=e.target.value; drawMap() };
  if($("inclTva")) $("inclTva").onchange=e=>{ IMP.inclTva=e.target.checked; preview() };
  $("impCancel").onclick=()=>{ $("impMap").hidden=true; IMP=null };
  $("impGo").onclick=doImport;
  if(IMP.kind==="price") fillListVals();
  preview();
}
function fillListVals(){
  const box=$("listValBox"), col=IMP.map.list; box.hidden=!col; if(!col) return;
  const vals=[...new Set(IMP.rows.map(r=>String(r[col]).trim()).filter(Boolean))];
  const pick=vals.find(v=>LIST_HINT.test(v))||vals[0];
  $("listVal").innerHTML=vals.map(v=>`<option ${v===pick?"selected":""}>${esc(v)}</option>`).join("");
  $("listVal").onchange=preview;
}
function mapped(){
  const M=IMP.map, K=IMP.kind; let rows=IMP.rows;
  if(K==="price"){
    if(M.list && $("listVal")) rows=rows.filter(r=>String(r[M.list]).trim()===$("listVal").value);
    return rows.map(r=>{
      const raw=pnum(r[M.p]), n=String(r[M.n]??"").trim(), c=String(r[M.c]??"").trim();
      if(!n && !c || !(raw>0)) return null;
      const gross = IMP.inclTva ? raw : raw*(1+TVA);
      const u=String(M.u?r[M.u]:"").trim().toLowerCase()||"buc";
      return {c, n:n||c, u, p:Math.round(gross*100)/100, f:Math.round(gross/(1+TVA)*100)/100, o:null, k:String(M.k?r[M.k]:"").trim(), s:null, l:"", svc:SVC_RX.test(n)||/^(ora|ore|h|serv)/.test(u)};
    }).filter(Boolean);
  }
  return rows.map(r=>{
    const g=k=>String(M[k]?r[M[k]]:"").trim();
    const o={c_nume:g("c_nume"),c_cui:g("c_cui"),c_reg:g("c_reg"),c_tel:g("c_tel"),c_email:g("c_email"),c_pers:g("c_pers"),loc:g("loc")};
    o.c_adr=[g("adr"),g("loc"),g("jud")].filter(Boolean).join(", ");
    return o.c_nume?o:null;
  }).filter(Boolean);
}
function preview(){
  const data=mapped(), K=IMP.kind;
  const cols = K==="price" ? [["c","Cod"],["n","Denumire"],["u","UM"],["f","Preț fără TVA"],["p","Preț cu TVA"],["svc","Serviciu"]] : [["c_nume","Denumire"],["c_cui","CUI"],["c_reg","Reg. Com."],["c_adr","Adresă"],["c_tel","Telefon"],["c_email","E-mail"]];
  $("impPrev").innerHTML=`<table><thead><tr>${cols.map(c=>`<th>${c[1]}</th>`).join("")}</tr></thead><tbody>${data.slice(0,6).map(r=>`<tr>${cols.map(([k])=>`<td>${k==="svc"?(r[k]?"da":""):typeof r[k]==="number"?fmtN(r[k]):esc(r[k])}</td>`).join("")}</tr>`).join("")||`<tr><td colspan="${cols.length}">Niciun rând valid cu aceste coloane.</td></tr>`}</tbody></table>`;
  $("impMsg").textContent = `${data.length.toLocaleString("ro-RO")} ${K==="price"?"articole":"clienți"} vor fi importați`;
}
function doImport(){
  const K=IMP.kind, need=NP_FIELDS[K].filter(f=>f[2]&&!IMP.map[f[0]]);
  if(need.length){ toast("Alege coloana pentru: "+need.map(f=>f[1]).join(", ")); return }
  const items=mapped(); if(!items.length){ toast("Niciun rând valid de importat"); return }
  const name = K==="price" ? (IMP.map.list&&$("listVal")?$("listVal").value:(IMP.file.match(LIST_HINT)||[IMP.file.replace(/\.[^.]+$/,"")])[0]) : "";
  const ok=npSave(K,{name,file:IMP.file,date:new Date().toISOString(),inclTva:!!IMP.inclTva,items});
  if(!ok){ toast("Lista e prea mare pentru memoria browserului"); return }
  $("impMap").hidden=true; IMP=null;
  if(K==="price"){ npLoadCatalog(); fillCats(); B.noteText=`Prețuri conform listei de parteneri ${B.listName}. Toate prețurile includ TVA 21%.`; $("footNote").textContent=B.noteText }
  npStatus(); renderAll(); toast(`${items.length.toLocaleString("ro-RO")} ${K==="price"?"articole":"clienți"} importați`);
}

/* ---------- căutare clienți ---------- */
let chits=[], csel=0;
function csearch(){
  const q=norm($("cq").value.trim()), d=npData("client");
  if(!q){ $("cres").hidden=true; $("cq").setAttribute("aria-expanded","false"); return }
  const items=d?d.items:[], words=q.split(" ").filter(Boolean);
  chits=items.filter(c=>{ const t=c._t||(c._t=norm([c.c_nume,c.c_cui,c.c_adr,c.c_pers].join(" ")).replace(/\s+/g," ")); return words.every(w=>t.includes(w)) }).slice(0,50);
  csel=0; cdraw();
}
function cdraw(){
  const r=$("cres"); r.hidden=false; $("cq").setAttribute("aria-expanded","true");
  r.innerHTML = !npData("client") ? '<div class="empty">Importă mai întâi clienții din gestiune.</div>'
    : chits.length ? chits.map((c,i)=>`<div role="option" data-c="${i}" aria-selected="${i===csel}"><span>${esc(c.c_nume)}<small>${esc([c.c_cui,c.c_adr].filter(Boolean).join(" · "))}</small></span><span class="pr" style="font-weight:400;color:var(--muted)">${esc(c.c_tel||"")}</span></div>`).join("")
    : '<div class="empty">Niciun client găsit. Completează datele manual mai jos.</div>';
  const a=r.querySelector('[aria-selected="true"]'); a&&a.scrollIntoView({block:"nearest"});
}
function cpick(i){
  const c=chits[i]; if(!c) return;
  ["c_nume","c_cui","c_reg","c_pers","c_tel","c_email","c_adr"].forEach(k=>S.client[k]=c[k]||"");
  $("cq").value=""; $("cres").hidden=true; $("cq").setAttribute("aria-expanded","false");
  fillForm(); renderAll(); toast("Client selectat: "+c.c_nume);
}
$("cq").addEventListener("input",csearch);
$("cq").addEventListener("keydown",e=>{
  if($("cres").hidden) return;
  if(e.key==="ArrowDown"){csel=Math.min(csel+1,chits.length-1);cdraw();e.preventDefault()}
  else if(e.key==="ArrowUp"){csel=Math.max(csel-1,0);cdraw();e.preventDefault()}
  else if(e.key==="Enter"){cpick(csel);e.preventDefault()}
  else if(e.key==="Escape"){$("cres").hidden=true}
});
$("cres").addEventListener("mousedown",e=>{const d=e.target.closest("[data-c]"); if(d){e.preventDefault();cpick(+d.dataset.c)}});
document.addEventListener("click",e=>{ if(!e.target.closest(".cpick")) $("cres").hidden=true });

/* ---------- legătură directă cu baza de date a gestiunii (folder cu tabele .dbf FoxPro) ----------
   Folderul se alege o dată (File System Access API, Chrome/Edge); handle-ul se păstrează în IndexedDB.
   La deschiderea foii, dacă browserul a păstrat permisiunea, se sincronizează singur; altfel un clic pe „Sincronizează acum”. */
const DBX = { dir:null, tables:null, cfg:store.get("np_dbcfg") };
function idb(){ return new Promise((res,rej)=>{ const r=indexedDB.open("oferta_np",1); r.onupgradeneeded=()=>r.result.createObjectStore("h"); r.onsuccess=()=>res(r.result); r.onerror=()=>rej(r.error) }) }
async function idbGet(k){ try{ const d=await idb(); return await new Promise(r=>{ const q=d.transaction("h").objectStore("h").get(k); q.onsuccess=()=>r(q.result); q.onerror=()=>r(null) }) }catch(e){ return null } }
async function idbSet(k,v){ try{ const d=await idb(); return await new Promise(r=>{ const t=d.transaction("h","readwrite"); t.objectStore("h").put(v,k); t.oncomplete=()=>r(true); t.onerror=()=>r(false) }) }catch(e){ return false } }

const CP = {0x03:"windows-1252",0x57:"windows-1252",0xC8:"windows-1250",0x64:"windows-1250",0x65:"windows-1250",0x02:"windows-1250"};
function dbfHead(buf){
  const v=new DataView(buf), u8=new Uint8Array(buf);
  const n=v.getUint32(4,true), hl=v.getUint16(8,true), rl=v.getUint16(10,true), cp=v.getUint8(29);
  const fields=[]; let off=1;
  for(let o=32; o+32<=Math.min(hl,buf.byteLength) && u8[o]!==0x0D; o+=32){
    let name=""; for(let i=0;i<11&&u8[o+i];i++) name+=String.fromCharCode(u8[o+i]);
    const f={name:name.trim().toUpperCase(), type:String.fromCharCode(u8[o+11]), len:u8[o+16], dec:u8[o+17], off};
    off+=f.len; fields.push(f);
  }
  return {n,hl,rl,enc:CP[cp]||"windows-1250",fields};
}
function dbfRows(buf, only){
  const h=dbfHead(buf), u8=new Uint8Array(buf), v=new DataView(buf), dec=new TextDecoder(h.enc), out=[];
  const F=only?h.fields.filter(f=>only.includes(f.name)):h.fields;
  for(let r=0;r<h.n;r++){
    const b=h.hl+r*h.rl; if(b+h.rl>buf.byteLength) break; if(u8[b]===0x2A) continue; // șters
    const o={};
    for(const f of F){
      const p=b+f.off;
      switch(f.type){
        case "C": case "V": o[f.name]=dec.decode(u8.subarray(p,p+f.len)).replace(/\0/g,"").trim(); break;
        case "N": case "F": { const t=String.fromCharCode(...u8.subarray(p,p+f.len)).trim(); o[f.name]=t===""?null:parseFloat(t); break }
        case "I": o[f.name]=v.getInt32(p,true); break;
        case "Y": o[f.name]=Number(v.getBigInt64(p,true))/10000; break;
        case "B": o[f.name]=v.getFloat64(p,true); break;
        case "L": o[f.name]=/[TtYy]/.test(String.fromCharCode(u8[p])); break;
        case "D": o[f.name]=String.fromCharCode(...u8.subarray(p,p+8)).trim(); break;
        default: o[f.name]=null; // memo / binar: ignorat
      }
    }
    out.push(o);
  }
  return out;
}
async function listTables(dir){
  const T=[];
  for await (const [name,h] of dir.entries()){
    if(h.kind!=="file" || !/\.dbf$/i.test(name)) continue;
    const file=await h.getFile(); if(file.size<33) continue;
    try{ const head=dbfHead(await file.slice(0,Math.min(file.size,32+32*255+2)).arrayBuffer()); T.push({name, size:file.size, n:head.n, fields:head.fields, h}) }catch(e){}
  }
  return T.sort((a,b)=>a.name.localeCompare(b.name));
}
const fx=(t,rx)=>t.fields.find(f=>rx.test(f.name))?.name||"";
const tbase=t=>t.name.replace(/\.dbf$/i,"").toUpperCase();
async function readTable(t,only){ return dbfRows(await (await t.h.getFile()).arrayBuffer(), only) }
const RX = { code:/^(CODPR|COD_?PR|CODART|COD_?ART|CODPROD|COD_?PROD|CODMAT|COD_?MARFA|CODINTERN|CODP)$/, name:/^(DENUMIRE|DENPR|DEN_?PR|DENART|DEN_?ART|DENPROD|DENMAT|DENUM|NUME|DEN)$/,
  um:/^(UM|U_?M|UNIT|UNITATE|UM1)$/, price:/^(PRET|PRET_?V|PRETV|PRET_?VANZ|PRVANZ|PU|PRET_?LISTA|PRETLISTA|PRET1|VALOARE)$/, pricey:/PRET|PRT|^PU/,
  cname:/^(DENUMIRE|DENPART|DEN_?PART|DENCL|DEN_?CL|DENTERT|NUME|DENUM|DEN|DENFIRMA|FIRMA)$/, cui:/^(COD_?FISC(AL)?|CODFISC|CUI|CIF|CF|COD_?FISCAL|CNP|CODUNIC)$/,
  reg:/^(NR_?REG(_?COM)?|NRREGCOM|REGCOM|REG_?COM|NRORC|ONRC|NR_?ORC)$/, adr:/^(ADRESA|ADR|SEDIU|STRADA|ADRESA1)$/, loc:/^(LOCALITATE|LOCALIT|ORAS|LOCAL)$/, jud:/^(JUDET|JUD)$/,
  tel:/^(TELEFON|TEL|TEL1|TELEFON1|MOBIL|TELMOBIL)$/, email:/^(E_?MAIL|EMAIL|MAIL)$/, pers:/^(PERS_?CONTACT|PERSCONT|CONTACT|DELEGAT|REPREZ|PERSOANA)$/ };
async function autoDetect(T){
  const cfg={};
  // 1) clienți: denumire + cod fiscal (+ adresă)
  const cl=T.map(t=>({t,s:(fx(t,RX.cname)?2:0)+(fx(t,RX.cui)?3:0)+(fx(t,RX.adr)||fx(t,RX.loc)?1:0)+(/CLIENT|PARTEN|TERT|BENEF/.test(tbase(t))?2:0)-(/FURN/.test(tbase(t))?2:0)}))
    .filter(x=>x.s>=5).sort((a,b)=>b.s-a.s||b.t.n-a.t.n)[0];
  if(cl){ const t=cl.t; cfg.cli={t:t.name,name:fx(t,RX.cname),cui:fx(t,RX.cui),reg:fx(t,RX.reg),adr:fx(t,RX.adr),loc:fx(t,RX.loc),jud:fx(t,RX.jud),tel:fx(t,RX.tel),email:fx(t,RX.email),pers:fx(t,RX.pers)} }
  // 2) articole: cod + denumire
  const pr=T.map(t=>({t,s:(fx(t,RX.code)?3:0)+(fx(t,RX.name)?2:0)+(fx(t,RX.um)?1:0)+(/PROD|ARTIC|MARF|NOMEN|STOC|MATER/.test(tbase(t))?2:0)}))
    .filter(x=>x.s>=5).sort((a,b)=>b.s-a.s||b.t.n-a.t.n)[0];
  if(pr){ const t=pr.t; cfg.prod={t:t.name,code:fx(t,RX.code),name:fx(t,RX.name),um:fx(t,RX.um)} }
  // 3) lista NMC05.10.26: căutăm valoarea în tabelele mici, apoi tabelul de prețuri care o folosește
  for(const t of T.filter(t=>t.size<4e6 && t.fields.some(f=>f.type==="C"))){
    let rows; try{ rows=await readTable(t) }catch(e){ continue }
    for(const r of rows){
      const hitF=Object.keys(r).find(k=>typeof r[k]==="string"&&LIST_HINT.test(r[k])); if(!hitF) continue;
      const pc=fx(t,RX.code), pp=fx(t,RX.price)||fx(t,RX.pricey);
      if(pc&&pp){ cfg.price={t:t.name,code:pc,price:pp,lf:hitF,lv:String(r[hitF]),name:fx(t,RX.name),label:r[hitF]}; break }
      const idF=t.fields.find(f=>f.name!==hitF && /^(COD|ID|NR)/.test(f.name))?.name; if(!idF) continue;
      const pt=T.find(x=>x!==t && x.fields.some(f=>f.name===idF) && fx(x,RX.code) && (fx(x,RX.price)||fx(x,RX.pricey)));
      if(pt){ cfg.price={t:pt.name,code:fx(pt,RX.code),price:fx(pt,RX.price)||fx(pt,RX.pricey),lf:idF,lv:String(r[idF]),name:fx(pt,RX.name),label:`${r[hitF]} (${idF} = ${r[idF]})`}; break }
    }
    if(cfg.price) break;
  }
  if(!cfg.price && cfg.prod){ // fallback: preț din tabelul de articole
    const t=T.find(x=>x.name===cfg.prod.t), pp=t&&(fx(t,RX.price)||fx(t,RX.pricey));
    if(pp) cfg.price={t:t.name,code:cfg.prod.code,price:pp,lf:"",lv:"",name:cfg.prod.name,label:"(din tabelul de articole — nu am găsit lista NMC05.10.26)"};
  }
  cfg.inclTva=false;
  return cfg;
}
async function dbSync(silent){
  const T=DBX.tables||(DBX.tables=await listTables(DBX.dir));
  if(!DBX.cfg){ DBX.cfg=await autoDetect(T); store.set("np_dbcfg",DBX.cfg) }
  const C=DBX.cfg, byName=n=>T.find(t=>t.name===n), stamp=new Date().toISOString(), msg=[];
  if(C.price&&byName(C.price.t)){
    const pt=byName(C.price.t); let rows=await readTable(pt);
    if(C.price.lf) rows=rows.filter(r=>String(r[C.price.lf]).trim()===String(C.price.lv).trim());
    let names={};
    if(C.prod&&byName(C.prod.t)){ for(const r of await readTable(byName(C.prod.t),[C.prod.code,C.prod.name,C.prod.um].filter(Boolean))) names[String(r[C.prod.code]).trim()]=r }
    const items=[], seen=new Set();
    for(const r of rows){
      const c=String(r[C.price.code]??"").trim(), raw=+r[C.price.price]; if(!c||!(raw>0)||seen.has(c)) continue; seen.add(c);
      const pr=names[c]||{}, n=String((C.prod&&pr[C.prod.name])||(C.price.name&&r[C.price.name])||c).trim(), u=String((C.prod&&C.prod.um&&pr[C.prod.um])||"buc").trim().toLowerCase()||"buc";
      const gross=C.inclTva?raw:raw*(1+TVA);
      items.push({c,n,u,p:Math.round(gross*100)/100,f:Math.round(gross/(1+TVA)*100)/100,o:null,k:"",s:null,l:"",svc:SVC_RX.test(n)||/^(ora|ore|h|serv)/.test(u)});
    }
    items.sort((a,b)=>a.c.localeCompare(b.c,"ro",{numeric:true}));
    if(items.length){ npSave("price",{name:String(C.price.label||C.price.lv||"").split(" (")[0]||"gestiune",file:"baza "+C.price.t,date:stamp,inclTva:!!C.inclTva,items}); msg.push(items.length+" articole") }
  }
  if(C.cli&&byName(C.cli.t)){
    const k=C.cli, items=(await readTable(byName(C.cli.t))).map(r=>{ const g=f=>f?String(r[f]??"").trim():"";
      const o={c_nume:g(k.name),c_cui:g(k.cui),c_reg:g(k.reg),c_tel:g(k.tel),c_email:g(k.email),c_pers:g(k.pers),loc:g(k.loc)}; o.c_adr=[g(k.adr),g(k.loc),g(k.jud)].filter(Boolean).join(", "); return o.c_nume?o:null }).filter(Boolean);
    if(items.length){ npSave("client",{file:"baza "+C.cli.t,date:stamp,items}); msg.push(items.length+" clienți") }
  }
  store.set("np_dblast",stamp);
  if(B.partner){ npLoadCatalog(); fillCats(); B.noteText=`Prețuri conform listei de parteneri ${B.listName}. Toate prețurile includ TVA 21%.`; $("footNote").textContent=B.noteText; npStatus(); renderAll() }
  dbState(); if(!silent||msg.length) toast(msg.length?"Sincronizat din gestiune: "+msg.join(", "):"Nu am găsit tabelele — deschide „Setări bază”");
  if(!C.price||!C.cli) dbSetupOpen();
}
function dbState(){
  const last=store.get("np_dblast");
  $("dbState").innerHTML = DBX.dir ? `Baza de date a gestiunii: <span class="ok">conectată</span> (${esc(DBX.dir.name)})` : "Baza de date a gestiunii: neconectată";
  $("dbInfo").textContent = DBX.dir ? (last?`Ultima sincronizare: ${new Date(last).toLocaleString("ro-RO")}`:"Nesincronizată încă") : (window.showDirectoryPicker?"Conectează o dată folderul cu baza (ex. \\\\rds.nmc.local\\Backup\\baze) și prețurile și clienții se preiau automat.":"Legătura directă cu baza merge în Google Chrome sau Microsoft Edge. Aici folosește importul de fișiere de mai jos.");
  $("dbConnect").textContent = DBX.dir ? "Schimbă folderul" : "Conectează folderul bazei";
  $("dbConnect").hidden = !window.showDirectoryPicker; $("dbSync").hidden=!DBX.dir; $("dbSetup").hidden=!DBX.dir;
}
async function dbUse(dir){ DBX.dir=dir; DBX.tables=null; await idbSet("dir",dir); dbState(); }
$("dbConnect").onclick=async()=>{
  try{ const dir=await window.showDirectoryPicker({id:"baze-gestiune",mode:"read"}); if(DBX.dir&&DBX.dir.name!==dir.name){DBX.cfg=null;store.set("np_dbcfg",null)} await dbUse(dir); await dbSync() }
  catch(e){ if(e.name!=="AbortError") toast("Nu am putut deschide folderul: "+e.message) }
};
$("dbSync").onclick=async()=>{
  try{ if(await DBX.dir.queryPermission({mode:"read"})!=="granted" && await DBX.dir.requestPermission({mode:"read"})!=="granted"){ toast("Fără permisiune de citire pentru folder"); return }
    DBX.tables=null; await dbSync() }catch(e){ toast("Sincronizarea nu a mers: "+e.message) }
};
/* setări: alegerea tabelelor/câmpurilor + structura bazei (de trimis pentru configurare) */
function dbSetupOpen(){ dbSetupDraw(); $("dbCfg").hidden=false }
$("dbSetup").onclick=async()=>{ if(!$("dbCfg").hidden){ $("dbCfg").hidden=true; return } try{ if(!DBX.tables) DBX.tables=await listTables(DBX.dir) }catch(e){ toast(e.message); return } dbSetupOpen() };
function dbSetupDraw(){
  const T=DBX.tables||[], C=DBX.cfg||(DBX.cfg={}), tbl=n=>T.find(t=>t.name===n);
  const tsel=(id,val)=>`<select id="${id}"><option value="">— nefolosit —</option>${T.map(t=>`<option ${t.name===val?"selected":""} value="${esc(t.name)}">${esc(t.name)} · ${t.n.toLocaleString("ro-RO")} rânduri</option>`).join("")}</select>`;
  const fsel=(grp,key,label,tn)=>{ const t=tbl(tn), v=(C[grp]||{})[key]||""; return `<label>${label}<select data-g="${grp}" data-k="${key}"><option value="">—</option>${(t?t.fields:[]).map(f=>`<option ${f.name===v?"selected":""}>${f.name}</option>`).join("")}</select></label>` };
  const P=C.price||{}, D=C.prod||{}, L=C.cli||{};
  $("dbCfg").innerHTML=`
    <b>Setări bază de date</b><span style="color:var(--muted);font-size:12.5px">Am ales automat tabelele de mai jos. Dacă ceva nu e corect, schimbă și apasă „Salvează și sincronizează”.</span>
    <div class="grid">
      <label>Tabel prețuri (lista NMC05.10.26)${tsel("cfgPriceT",P.t)}</label>${fsel("price","code","Cod articol",P.t)}${fsel("price","price","Preț",P.t)}${fsel("price","lf","Câmp listă de preț",P.t)}
      <label>Valoare listă (ex. NMC05.10.26 sau codul ei)<input id="cfgLv" value="${esc(P.lv||"")}" style="font:13.5px var(--f-body);background:var(--soft);border:1px solid var(--line);border-radius:6px;padding:6px 8px;color:var(--ink)"></label>
      <label class="chk"><input type="checkbox" id="cfgTva" ${C.inclTva?"checked":""}> Prețurile din bază includ TVA</label>
      <label>Tabel articole (denumire, UM)${tsel("cfgProdT",D.t)}</label>${fsel("prod","code","Cod articol",D.t)}${fsel("prod","name","Denumire",D.t)}${fsel("prod","um","UM",D.t)}
      <label>Tabel clienți${tsel("cfgCliT",L.t)}</label>${["name:Denumire","cui:CUI","reg:Reg. Com.","adr:Adresă","loc:Localitate","jud:Județ","tel:Telefon","email:E-mail","pers:Persoană contact"].map(x=>{const[k,l]=x.split(":");return fsel("cli",k,l,L.t)}).join("")}
    </div>
    <div class="confirm"><button type="button" class="btn primary" id="cfgSave">Salvează și sincronizează</button><button type="button" class="btn" id="cfgAuto">Detectează din nou</button><button type="button" class="btn" id="cfgCopy">Copiază structura bazei</button><button type="button" class="btn" id="cfgClose">Închide</button></div>
    <span style="color:var(--muted);font-size:12px">„Copiază structura bazei” copiază doar numele tabelelor și ale câmpurilor (fără date) — o poți trimite pentru o configurare exactă.</span>`;
  const setT=(g,id)=>$(id).onchange=e=>{ C[g]=Object.assign({},C[g]||{},{t:e.target.value}); dbSetupDraw() };
  setT("price","cfgPriceT"); setT("prod","cfgProdT"); setT("cli","cfgCliT");
  $("dbCfg").querySelectorAll("select[data-g]").forEach(s=>s.onchange=()=>{ C[s.dataset.g]=Object.assign({},C[s.dataset.g]||{},{[s.dataset.k]:s.value}) });
  $("cfgSave").onclick=async()=>{ if(C.price){const nv=$("cfgLv").value.trim(); if(nv!==C.price.lv){C.price.lv=nv; C.price.label=nv}} C.inclTva=$("cfgTva").checked;
    for(const g of ["price","prod","cli"]) if(C[g]&&!C[g].t) delete C[g];
    store.set("np_dbcfg",C); $("dbCfg").hidden=true; await dbSync() };
  $("cfgAuto").onclick=async()=>{ DBX.cfg=await autoDetect(T); store.set("np_dbcfg",DBX.cfg); dbSetupDraw() };
  $("cfgClose").onclick=()=>{ $("dbCfg").hidden=true };
  $("cfgCopy").onclick=()=>{ const txt=T.map(t=>`${t.name} (${t.n} rânduri): ${t.fields.map(f=>f.name+":"+f.type+f.len).join(", ")}`).join("\n");
    (navigator.clipboard?navigator.clipboard.writeText(txt):Promise.reject()).then(()=>toast("Structura bazei a fost copiată"),()=>{ $("dbCfg").insertAdjacentHTML("beforeend",`<pre>${esc(txt)}</pre>`) }) };
}
/* la pornire: reia folderul salvat; sincronizează singur dacă permisiunea e încă valabilă */
async function dbBoot(){
  dbState(); if(!window.showDirectoryPicker) return;
  const dir=await idbGet("dir"); if(!dir) return;
  DBX.dir=dir; dbState();
  try{ if(await dir.queryPermission({mode:"read"})==="granted" && B.partner) await dbSync(true) }catch(e){}
}
