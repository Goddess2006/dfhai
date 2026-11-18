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
