/* Foaia „Borderou livrări” (model: Raport zilnic activitate șoferi din gestiunea NMC).
   Document = DL (dispoziție de livrare): nr. DL, firma, adresa de livrare, nr. factură (FACTOUT / NRFACTURA), nr. aviz (NRAVIZ),
   data, de încasat (cu TVA), încasat, nr. chitanță, greutate; produse: cod (CODPR), model (CODMARE), denumire (DENPROD),
   cantitate (CANTIT), preț fără TVA (PVANZFTVA), greutate unitară (GREUTATE).
   Surse: (1) baza gestiunii (aceeași legătură ca foaia Parteneri) — tabelele se recunosc după aceste câmpuri;
          (2) import de rapoarte Excel exportate din gestiune (ex. avize Dedeman/Altex, „facturi_nmc” = DL-urile cursei).
   Inserat de build.py; folosește DBX, listTables, readTable, dbUse, idbGet, tbase, store, toast, download, esc, norm, num,
   todayISO, zipStore, b64bytes, table, tr, cell, cp, para, BRANDS, framed, XLSX, TVA. */
const BD_ISSUER=[["NMC Stil Distribution SRL",""],["","CUI RO16109528 · Reg. Com. J40/1507/2004"],["","Autostrada București–Pitești km 13, clădirea A, Chiajna, Ilfov"],["","Tel. 021 319 35 35 · www.nmcromania.ro"]];
/* denumirile de câmpuri (în bază și în rapoartele exportate) pentru fiecare informație */
const BF = {
  dl:["NRDL","NRDLINIT","NR_DL","NRDISPL","NRDISP"], cli:["CODCLI","COD_CLI","CODPART","CODTERT"], client:["NUMECLI","FIRMA","DENCLI","CLIENT","DENPART","NUMEPART"],
  adresa:["DENLOCM","ADRESA","ADRESALIVR","ADR_LIVR","PUNCTLUCRU","LOCATIE"], loc:["LOCALITATE","ORAS","LOCALIT"],
  factura:["FACTOUT","NRFACTURA","NRFACT","NR_FACT","NRFACTOUT"], aviz:["NRAVIZ","NR_AVIZ","NRAV"], doc:["NRDOC"],
  data:["DATA","DATADL","DATA_DL","DATADOC","DATAAVIZ"], val:["SUMDEINCAS","DEINCASAT","SUMA_INCAS","VALCUTVA","VALOARE","TOTAL"],
  incasat:["INCASAT"], chitanta:["NRCHITANTA","NRCHIT","CHITANTA"], grdl:["GR_DL","GREUTDL","GREUT_DL","GRDL"],
  cod:["CODPR","COD_PR","CODART"], q:["CANTIT","CANT","CANTITATE"], pv:["PVANZFTVA","PRETFTVA","PVFTVA","PRETVANZ","PRET","PU"],
  den:["DENPROD","DENUMIRE","DENPR"], codm:["CODMARE","CODPRMARE","MODEL"], gr:["GREUTATE","GREUT"], sofer:["NUMESOF","SOFER"], anul:["FACT_ANUL"] };
const BDX = { cfg:store.get("bd_cfg3"), cache:{}, pool:[], dbDocs:null };
const pick = (names,list) => { const L=list.map(x=>String(x).toUpperCase()); for(const n of names){ const i=L.indexOf(n); if(i>=0) return list[i] } return "" };
function mapFor(fields){ const m={}; for(const k in BF) m[k]=pick(BF[k],fields); return m }
const roD = s => s ? s.split("-").reverse().join(".") : "";
const fmtL = v => v==null||v==="" ? "" : new Intl.NumberFormat("ro-RO",{minimumFractionDigits:2,maximumFractionDigits:2}).format(v);
function toISO(v){ // AAAALLZZ (DBF) · număr serial Excel · zz.ll.aaaa · Date
  if(v==null||v==="") return ""; if(v instanceof Date) return new Date(v-v.getTimezoneOffset()*6e4).toISOString().slice(0,10);
  if(typeof v==="number") return v>20000&&v<80000 ? new Date(Math.round((v-25569)*864e5)).toISOString().slice(0,10) : "";
  const s=String(v).trim(); let m;
  if(m=s.match(/^(\d{4})(\d{2})(\d{2})$/)) return `${m[1]}-${m[2]}-${m[3]}`;
  if(m=s.match(/^(\d{1,2})[./-](\d{1,2})[./-](\d{4})/)) return `${m[3]}-${m[2].padStart(2,"0")}-${m[1].padStart(2,"0")}`;
  if(m=s.match(/^(\d{4})-(\d{2})-(\d{2})/)) return m[0];
  return "";
}
const S2 = v => v==null ? "" : String(v).trim();
const dlKey = v => S2(v).replace(/\s*\(\d+\)\s*$/,""); // „131126011 (1)” → 131126011

/* rânduri (din bază sau din raport) → documente DL, cu produse dacă rândurile au cod + cantitate */
function rowsToDocs(rows, m, cliMap, srcTag){
  const by=new Map();
  for(const r of rows){
    const key = dlKey(r[m.dl]) || S2(r[m.factura]) || S2(r[m.aviz]) || S2(r[m.doc]); if(!key) continue;
    let d=by.get(key);
    if(!d){ const c=cliMap&&m.cli?cliMap[S2(r[m.cli])]:null;
      d={key:srcTag+"|"+key, src:srcTag, dl:m.dl?dlKey(r[m.dl]):"", dlLabel:m.dl?S2(r[m.dl]):"",
        client:S2(r[m.client])||(c&&c.n)||(m.cli&&S2(r[m.cli])?`Client cod ${S2(r[m.cli])}`:""), cui:c?c.cui:"",
        adresa:[S2(r[m.adresa]),S2(r[m.loc])].filter((x,i,a)=>x&&!(i&&a[0].toUpperCase().includes(x.toUpperCase()))).join(", ")||(c&&c.adr)||"",
        factura:S2(r[m.factura]), aviz:S2(r[m.aviz])||(m.aviz?"":S2(r[m.doc])), data:toISO(r[m.data]),
        val:m.val&&r[m.val]!==""&&r[m.val]!=null?+r[m.val]:null, incasat:m.incasat&&+r[m.incasat]?+r[m.incasat]:null, chitanta:S2(r[m.chitanta]),
        gr:m.grdl&&+r[m.grdl]?+r[m.grdl]:null, sofer:S2(r[m.sofer]), lines:m.cod&&m.q?[]:null };
      by.set(key,d) }
    if(d.lines){ const q=+r[m.q]||0, pv=m.pv?+r[m.pv]||0:null, cod=S2(r[m.cod]);
      if(cod&&q) d.lines.push({c:S2(r[m.codm])||cod, cp:cod, n:S2(r[m.den]), u:"buc", q, v:pv==null?null:Math.round(q*pv*(1+TVA)*100)/100, w:m.gr?q*(+r[m.gr]||0):0}) }
  }
  for(const d of by.values()){ if(d.lines){
      if(d.val==null&&d.lines.some(l=>l.v!=null)) d.val=Math.round(d.lines.reduce((a,l)=>a+(l.v||0),0)*100)/100;
      if(d.gr==null) d.gr=Math.round(d.lines.reduce((a,l)=>a+l.w,0)*100)/100;
      d.lines=mergeLines(d.lines) }
    d._t=norm([d.dlLabel,d.dl,d.client,d.cui,d.adresa,d.factura,d.aviz,roD(d.data)].join(" ")) }
  return [...by.values()];
}
function mergeLines(L){ const m=new Map(); for(const l of L){ const k=l.cp+"|"+l.n; const e=m.get(k); if(e){ e.q+=l.q; if(e.v!=null&&l.v!=null) e.v=Math.round((e.v+l.v)*100)/100; e.w+=l.w } else m.set(k,{...l}) } return [...m.values()] }
function mergeDocs(a,b){ // același DL din două surse (ex. DL-urile cursei + avizele cu produse)
  const idx=new Map(a.map(d=>[d.dl||d.factura||d.aviz,d]));
  for(const d of b){ const k=d.dl||d.factura||d.aviz, e=idx.get(k);
    if(e){ for(const f of ["client","adresa","factura","aviz","data","chitanta","sofer"]) if(!e[f]&&d[f]) e[f]=d[f];
      if(e.val==null) e.val=d.val; if(e.gr==null) e.gr=d.gr; if(!e.lines&&d.lines) e.lines=d.lines; e._t=norm([e._t,d._t].join(" ")) }
    else { a.push(d); idx.set(k,d) } }
  return a;
}

/* ---------- starea borderoului ---------- */
let BD;
function bdNextNr(){ const y=new Date().getFullYear(); let c=store.get("bd_counter")||{y,n:0}; if(c.y!==y)c={y,n:0}; c.n++; store.set("bd_counter",c); return "BL-"+y+"-"+String(c.n).padStart(4,"0") }
const BD_DEF = () => ({id:"",nr:"",data:todayISO(),firma:"",sofer:"",auto:"",tel:"",cursa:"1",gestiune:"NMC SD",kmP:"",kmS:"",statie:"",litri:"",valComb:"",info:"",showVal:true,marfa:true,anexaVal:false,docs:[]});
function bdBlank(){ return Object.assign(BD_DEF(),{nr:bdNextNr()}) }
function bdMigrate(b){ for(const d of b.docs||[]) if(d.nr!=null&&d.dl==null){ d.dl=""; d.dlLabel=""; if(d.tip==="Aviz") d.aviz=d.nr; else d.factura=d.nr; delete d.nr; delete d.tip }
  return Object.assign(BD_DEF(),b) }
function bdSave(){ store.set("bd_draft",BD); clearTimeout(bdSave.t); bdSave.t=setTimeout(bdArhSave,400) }
const bdLists = () => store.get("bd_lists") || {firma:[],sofer:[],auto:[]};
function bdRemember(){ // șofer / mașină / transportator rămân în listele derulante după prima introducere
  const L=bdLists(); let ch=false;
  const add=(k,v,extra)=>{ v=(v||"").trim(); if(!v) return; let e=L[k].find(x=>(x.name||x).toLowerCase()===v.toLowerCase());
    if(!e){ e={name:v}; L[k].push(e); ch=true } if(extra) for(const [kk,vv] of Object.entries(extra)) if(vv&&e[kk]!==vv){ e[kk]=vv; ch=true } };
  add("firma",BD.firma); add("sofer",BD.sofer,{tel:BD.tel,firma:BD.firma,auto:BD.auto}); add("auto",BD.auto,{firma:BD.firma});
  if(ch){ store.set("bd_lists",L); bdFillLists() }
}
function bdFillLists(){ const L=bdLists(), o=a=>a.map(x=>`<option value="${esc(x.name||x)}"></option>`).join(""); $("dlFirma").innerHTML=o(L.firma); $("dlSofer").innerHTML=o(L.sofer); $("dlAuto").innerHTML=o(L.auto) }

/* ---------- afișare ---------- */
const HEADF=[["bdNr","nr"],["bdData","data"],["bdFirma","firma"],["bdSofer","sofer"],["bdAuto","auto"],["bdTel","tel"],["bdCursa","cursa"],["bdGestiune","gestiune"],["bdKmP","kmP"],["bdKmS","kmS"],["bdStatie","statie"],["bdLitri","litri"],["bdValComb","valComb"],["bdInfo","info"]];
function bdRenderHead(){
  $("bdLogo").src=BRANDS.nmc.logo; $("bdIssuer").innerHTML=BD_ISSUER.map(([b,t])=>(b?`<b>${esc(b)}</b>`:"")+esc(t)).join("<br>");
  HEADF.forEach(([id,k])=>$(id).value=BD[k]??""); $("bdShowVal").checked=BD.showVal; $("bdAnexaVal").checked=BD.anexaVal; $("bdMarfa").checked=BD.marfa; bdCalcHead();
}
function bdCalcHead(){
  const e=num(BD.kmS)-num(BD.kmP); $("bdKmE").value = BD.kmS&&BD.kmP ? String(e) : "";
  const g=BD.docs.reduce((a,d)=>a+(+d.gr||0),0); $("bdGr").value = g ? fmtL(g) : "";
}
const totInc = () => BD.docs.reduce((a,d)=>a+(+d.val||0),0), totIncasat = () => BD.docs.reduce((a,d)=>a+(+d.incasat||0),0);
function bdTotHtml(){ return `<span>${BD.docs.length} ${BD.docs.length===1?"document":"documente"}</span>${BD.showVal?`<span>Total de încasat: <b>${fmtL(totInc())} lei</b></span><span>Total încasat: <b>${fmtL(totIncasat())} lei</b></span>`:""}` }
function bdRender(){
  const inp=(i,k,v,w,al)=>`<input data-i="${i}" data-k="${k}" value="${esc(v??"")}" style="${w?`width:${w}px;`:""}${al?`text-align:${al}`:""}" aria-label="${k} ${i+1}">`;
  $("bdRows").innerHTML = BD.docs.length ? BD.docs.map((d,i)=>`<tr>
      <td class="um">${i+1}</td><td>${inp(i,"dlLabel",d.dlLabel||d.dl,120)}</td>
      <td class="cl">${inp(i,"client",d.client)}${d.cui?`<small>${esc(d.cui)}</small>`:""}</td><td class="ad">${inp(i,"adresa",d.adresa)}</td>
      <td>${inp(i,"factura",d.factura,120)}</td><td>${inp(i,"aviz",d.aviz,90)}</td>
      <td class="n">${BD.showVal?inp(i,"val",d.val==null?"":fmtL(d.val).replace(/\./g,""),100,"right"):'<span class="um">—</span>'}</td>
      <td class="n">${BD.showVal?inp(i,"incasat",d.incasat==null?"":fmtL(d.incasat).replace(/\./g,""),90,"right"):'<span class="um">—</span>'}</td>
      <td>${inp(i,"chitanta",d.chitanta,90)}</td>
      <td class="noprint" style="text-align:center"><input type="checkbox" data-i="${i}" data-k="anexa" ${d.anexa?"checked":""} aria-label="Anexă document ${i+1}" style="width:16px;height:16px;accent-color:var(--accent)"></td>
      <td class="noprint"><button class="x" data-del="${i}" aria-label="Scoate documentul ${i+1}">×</button></td></tr>`).join("")
    : `<tr class="emptyrow"><td colspan="11">Niciun document încă. Caută DL-urile / facturile / avizele mai sus sau adaugă un document manual.</td></tr>`;
  $("bdTot").innerHTML=bdTotHtml(); bdCalcHead(); bdRenderMarfa(); bdRenderAnexa();
  $("bdState").textContent = BD.id ? `${BD.nr} · salvat automat` : BD.nr;
}
function bdMarfaRows(){ // centralizator: toate produsele din documentele borderoului, însumate pe cod
  const m=new Map(); for(const d of BD.docs) for(const l of d.lines||[]){ const k=l.c+"|"+l.n; const e=m.get(k); if(e){ e.q+=+l.q||0; e.v=(e.v||0)+(+l.v||0) } else m.set(k,{c:l.c,n:l.n,u:l.u,q:+l.q||0,v:+l.v||0}) }
  return [...m.values()].sort((a,b)=>a.c.localeCompare(b.c,"ro",{numeric:true}));
}
function bdRenderMarfa(){
  $("bdMarfaSec").classList.toggle("off",!BD.marfa);
  const R=bdMarfaRows(), fq=q=>String(Math.round(q*1000)/1000).replace(".",",");
  $("bdMarfaBody").innerHTML = R.length ? `<div class="marfa">${R.map(r=>`<div><span>${esc(r.c)}${r.n?" – "+esc(r.n):""}</span><b>= ${fq(r.q)}${BD.anexaVal&&r.v?` · ${fmtL(r.v)} lei`:""}</b></div>`).join("")}</div>`
    : `<p class="um">Produsele apar aici după ce adaugi documente care au produse (din bază sau din raportul cu produse).</p>`;
}
function bdRenderAnexa(){
  const A=BD.docs.map((d,i)=>[d,i]).filter(([d])=>d.anexa);
  $("bdAnexa").classList.toggle("empty",!A.length);
  $("bdAnexaBody").innerHTML = A.length ? A.map(([d,i],k)=>`<div class="anx">
      <div class="ah"><b>Anexa ${k+1} – DL ${esc(d.dlLabel||d.dl||"—")}${d.factura?` · factura ${esc(d.factura)}`:""}${d.aviz?` · aviz ${esc(d.aviz)}`:""}${d.data?` · ${roD(d.data)}`:""}</b><span>${esc(d.client)}${d.adresa?" · "+esc(d.adresa):""}</span></div>
      <div class="tbl" style="border:0;border-radius:0"><table><thead><tr><th>Cod</th><th>Denumire</th><th>UM</th><th class="n">Cantitate</th>${BD.anexaVal?'<th class="n">Valoare cu TVA</th>':""}<th class="noprint"></th></tr></thead><tbody>
      ${(d.lines||[]).map((l,j)=>`<tr><td><input data-d="${i}" data-j="${j}" data-k="c" value="${esc(l.c)}" style="width:100px"></td><td><input data-d="${i}" data-j="${j}" data-k="n" value="${esc(l.n)}" style="width:100%;text-align:left"></td>
        <td><input data-d="${i}" data-j="${j}" data-k="u" value="${esc(l.u)}" style="width:56px"></td><td class="n"><input data-d="${i}" data-j="${j}" data-k="q" inputmode="decimal" value="${String(l.q??"").replace(".",",")}" style="width:80px;text-align:right"></td>
        ${BD.anexaVal?`<td class="n"><input data-d="${i}" data-j="${j}" data-k="v" inputmode="decimal" value="${l.v==null?"":fmtL(l.v).replace(/\./g,"")}" style="width:100px;text-align:right"></td>`:""}
        <td class="noprint"><button class="x" data-ldel="${i}:${j}" aria-label="Șterge produsul">×</button></td></tr>`).join("")
        || `<tr class="emptyrow"><td colspan="6">Nu am găsit produsele acestui document — le poți adăuga manual.</td></tr>`}
      </tbody></table></div>
      <div class="confirm noprint" style="padding:6px 10px"><button type="button" class="btn sm" data-ladd="${i}">+ Produs</button></div></div>`).join("")
    : `<p class="um noprint">Bifează „Anexă” la documentele pentru care vrei lista de produse pe pagină separată.</p>`;
}

/* ---------- editare ---------- */
HEADF.forEach(([id,k])=>$(id).addEventListener("input",e=>{ BD[k]=e.target.value; if(k==="kmP"||k==="kmS") bdCalcHead(); if(k==="nr") $("bdState").textContent=BD.nr; bdSave() }));
$("bdSofer").addEventListener("input",()=>{ const s=bdLists().sofer.find(x=>x.name===BD.sofer); if(!s) return;
  for(const [k,id] of [["tel","bdTel"],["auto","bdAuto"],["firma","bdFirma"]]) if(s[k]&&!BD[k]){ BD[k]=s[k]; $(id).value=s[k] } bdSave() });
["bdFirma","bdSofer","bdAuto","bdTel"].forEach(id=>$(id).addEventListener("change",bdRemember));
$("bdShowVal").onchange=e=>{ BD.showVal=e.target.checked; bdRender(); bdSave() };
$("bdAnexaVal").onchange=e=>{ BD.anexaVal=e.target.checked; bdRenderMarfa(); bdRenderAnexa(); bdSave() };
$("bdMarfa").onchange=e=>{ BD.marfa=e.target.checked; bdRenderMarfa(); bdSave() };
$("bdRows").addEventListener("input",e=>{ const i=e.target.dataset.i,k=e.target.dataset.k; if(i==null||k==="anexa") return; const d=BD.docs[i];
  d[k] = k==="val"||k==="incasat" ? (e.target.value.trim()===""?null:num(e.target.value)) : e.target.value; if(k==="dlLabel") d.dl=dlKey(e.target.value);
  bdSave(); if(k==="val"||k==="incasat") $("bdTot").innerHTML=bdTotHtml() });
$("bdRows").addEventListener("change",async e=>{ const i=e.target.dataset.i; if(e.target.dataset.k!=="anexa") return; const d=BD.docs[i]; d.anexa=e.target.checked;
  if(d.anexa&&!d.lines) d.lines=await bdLinesFor(d).catch(()=>[]); bdRenderMarfa(); bdRenderAnexa(); bdSave() });
$("bdRows").addEventListener("click",e=>{ if(e.target.dataset.del!=null){ BD.docs.splice(+e.target.dataset.del,1); bdRender(); bdSave() } });
$("bdAnexaBody").addEventListener("input",e=>{ const t=e.target; if(t.dataset.d==null) return; const l=BD.docs[t.dataset.d].lines[t.dataset.j], k=t.dataset.k;
  l[k] = k==="q"||k==="v" ? (t.value.trim()===""?null:num(t.value)) : t.value; bdSave(); bdRenderMarfa() });
$("bdAnexaBody").addEventListener("click",e=>{ const t=e.target;
  if(t.dataset.ladd!=null){ const d=BD.docs[t.dataset.ladd]; (d.lines=d.lines||[]).push({c:"",n:"",u:"buc",q:1,v:null}); bdRenderAnexa(); bdSave() }
  if(t.dataset.ldel){ const [i,j]=t.dataset.ldel.split(":"); BD.docs[i].lines.splice(+j,1); bdRenderAnexa(); bdRenderMarfa(); bdSave() } });
$("bdAddManual").onclick=()=>{ BD.docs.push({key:"m"+Date.now(),src:"manual",dl:"",dlLabel:"",client:"",adresa:"",factura:"",aviz:"",data:BD.data,val:null,incasat:null,chitanta:"",gr:null,anexa:false,lines:null}); bdRender(); bdSave(); $("bdRows").querySelectorAll('input[data-k="dlLabel"]')[BD.docs.length-1]?.focus() };
$("bdNew").onclick=()=>{ $("bdConfirmNew").hidden=false }; $("bdNewNo").onclick=()=>{ $("bdConfirmNew").hidden=true };
$("bdNewYes").onclick=async()=>{ await bdArhSave(); const keep={firma:BD.firma,sofer:BD.sofer,auto:BD.auto,tel:BD.tel,gestiune:BD.gestiune,kmP:BD.kmS}; BD=bdBlank(); Object.assign(BD,keep); $("bdConfirmNew").hidden=true; bdRenderHead(); bdRender(); bdSave(); toast("Borderou nou: "+BD.nr) };
$("bdLists").onclick=()=>{ const b=$("bdListsBox"); b.hidden=!b.hidden; if(!b.hidden) bdDrawLists() };
function bdDrawLists(){
  const L=bdLists(), sec=(k,t)=>`<div><b style="font-size:13px">${t}</b><div style="display:flex;flex-wrap:wrap;gap:6px;margin-top:6px">${L[k].length?L[k].map((x,i)=>`<span class="chipx">${esc(x.name)}${x.tel?` · ${esc(x.tel)}`:""} <button class="x" data-lk="${k}" data-li="${i}" aria-label="Șterge ${esc(x.name)}">×</button></span>`).join(""):'<span class="um">— gol —</span>'}</div></div>`;
  $("bdListsBox").innerHTML=sec("sofer","Șoferi")+sec("auto","Mașini")+sec("firma","Firme transportatoare")+`<span class="um" style="font-size:12px">Valorile noi se adaugă automat în liste când le scrii în borderou.</span>`;
}
$("bdListsBox").addEventListener("click",e=>{ const b=e.target.closest("[data-lk]"); if(!b) return; const L=bdLists(); L[b.dataset.lk].splice(+b.dataset.li,1); store.set("bd_lists",L); bdFillLists(); bdDrawLists() });

/* ---------- surse: baza gestiunii ---------- */
function bdDetect(T){ // tabel cu produse pe DL (NRDL + CODPR + CANTIT) și/sau tabel cu DL-uri (NRDL + sumă / factură)
  const has=(t,k)=>pick(BF[k],t.fields.map(f=>f.name));
  const lines=T.filter(t=>has(t,"dl")&&has(t,"cod")&&has(t,"q")).sort((a,b)=>(has(b,"pv")?1:0)-(has(a,"pv")?1:0)||b.n-a.n)[0];
  const head=T.filter(t=>has(t,"dl")&&!has(t,"cod")&&(has(t,"val")||has(t,"factura")||has(t,"cli"))).sort((a,b)=>(has(b,"val")?1:0)-(has(a,"val")?1:0)||b.n-a.n)[0];
  const ct=T.find(t=>/^CLIENT$/.test(tbase(t))&&t.fields.some(f=>f.name==="NUMECLI"));
  return { lines:lines?{t:lines.name,map:mapFor(lines.fields.map(f=>f.name))}:null, head:head?{t:head.name,map:mapFor(head.fields.map(f=>f.name))}:null,
    cli:ct?{t:ct.name,code:"CODCLI",name:"NUMECLI",adr:ct.fields.some(f=>f.name==="ADRESA")?"ADRESA":""}:null };
}
async function bdTable(name){ if(!BDX.cache[name]){ const t=DBX.tables.find(x=>x.name===name); BDX.cache[name]=t?await readTable(t):[] } return BDX.cache[name] }
async function bdClients(){
  const c=BDX.cfg&&BDX.cfg.cli; if(!c) return {};
  if(!BDX.cliMap){ BDX.cliMap={}; for(const r of await bdTable(c.t)) BDX.cliMap[S2(r[c.code])]={n:S2(r[c.name]),cui:"",adr:c.adr?S2(r[c.adr]):""} }
  return BDX.cliMap;
}
async function bdEnsureDb(interactive){
  if(!DBX.dir){ const d=await idbGet("dir"); if(d) DBX.dir=d }
  if(!DBX.dir) return false;
  let perm=await DBX.dir.queryPermission({mode:"read"}); if(perm!=="granted"&&interactive) perm=await DBX.dir.requestPermission({mode:"read"});
  if(perm!=="granted") return false;
  if(!DBX.tables) DBX.tables=await listTables(DBX.dir);
  if(!BDX.cfg||(!BDX.cfg.lines&&!BDX.cfg.head)){ BDX.cfg=bdDetect(DBX.tables); store.set("bd_cfg3",BDX.cfg) }
  return true;
}
async function bdDbDocs(){
  if(BDX.dbDocs) return BDX.dbDocs;
  const C=BDX.cfg||{}, cl=await bdClients(); let docs=[];
  if(C.head&&C.head.t) docs=rowsToDocs(await bdTable(C.head.t),C.head.map,cl,"db");
  if(C.lines&&C.lines.t) docs=mergeDocs(docs,rowsToDocs(await bdTable(C.lines.t),C.lines.map,cl,"db"));
  return BDX.dbDocs=docs;
}
async function bdLinesFor(d){ // produse pentru un document adăugat fără produse
  const all=[...BDX.pool,...(BDX.dbDocs||[])]; const f=all.find(x=>x.lines&&((d.dl&&x.dl===d.dl)||(d.factura&&x.factura===d.factura)||(d.aviz&&x.aviz===d.aviz)));
  return f?JSON.parse(JSON.stringify(f.lines)):[];
}
function bdDbState(){
  const ok=!!(DBX.dir&&DBX.tables), C=BDX.cfg||{};
  $("bdDbState").innerHTML = (ok ? `Baza de date a gestiunii: <span class="ok">conectată</span> (${esc(DBX.dir.name)})` : "Baza de date a gestiunii: neconectată")
    + (BDX.pool.length?` · raport importat: ${BDX.pool.length.toLocaleString("ro-RO")} documente`:"");
  $("bdDbInfo").textContent = ok ? ((C.lines||C.head) ? `DL-uri din: ${[C.head&&C.head.t,C.lines&&C.lines.t+" (cu produse)"].filter(Boolean).join(" + ")}`
      : `Am citit ${DBX.tables.length} tabele, dar nu am găsit tabelul cu DL-uri (câmpuri NRDL, CODPR, CANTIT…). Folosește „Importă raport (Excel)” sau „Setări documente”.`)
    : (window.showDirectoryPicker ? (DBX.dir?"Apasă „Reîncarcă documentele” ca să dai acces la folder.":"Conectează folderul bazei (\\\\rds.nmc.local\\Backup\\baze) sau importă un raport Excel exportat din gestiune.") : "Importă un raport Excel exportat din gestiune (legătura directă cu baza merge în Chrome / Edge).");
  $("bdConnect").hidden=!window.showDirectoryPicker; $("bdConnect").textContent=DBX.dir?"Schimbă folderul":"Conectează folderul bazei";
  $("bdReload").hidden=!DBX.dir; $("bdSetup").hidden=!ok;
}
function bdResetDb(){ BDX.cache={}; BDX.cliMap=null; BDX.dbDocs=null }
$("bdConnect").onclick=async()=>{ try{ const dir=await window.showDirectoryPicker({id:"baze-gestiune",mode:"read"}); bdResetDb();
  if(DBX.dir&&DBX.dir.name!==dir.name){ DBX.cfg=null; store.set("np_dbcfg2",null); BDX.cfg=null; store.set("bd_cfg3",null) }
  await dbUse(dir); DBX.tables=null; await bdEnsureDb(true); bdDbState(); bdSearch() }catch(e){ if(e.name!=="AbortError") toast("Nu am putut deschide folderul: "+e.message) } };
$("bdReload").onclick=async()=>{ bdResetDb(); DBX.tables=null; try{ if(await bdEnsureDb(true)){ bdDbState(); await bdSearch(); toast("Documente reîncărcate") } else toast("Fără permisiune de citire pentru folder") }catch(e){ toast("Nu am putut citi baza: "+e.message) } };

/* ---------- surse: rapoarte Excel exportate din gestiune ---------- */
$("bdImp").onclick=()=>{ $("bdImpFile").value=""; $("bdImpFile").click() };
$("bdImpFile").addEventListener("change",async e=>{
  let n=0;
  for(const f of e.target.files){
    try{ const ce=console.error; console.error=()=>{}; let wb; try{ wb=XLSX.read(await f.arrayBuffer(),{type:"array",codepage:1250}) } finally { console.error=ce } // avertismente inofensive ale citirii .xls
      for(const sn of wb.SheetNames){ const rows=XLSX.utils.sheet_to_json(wb.Sheets[sn],{defval:"",raw:true}); if(!rows.length) continue;
        const m=mapFor(Object.keys(rows[0])); if(!m.dl&&!m.factura&&!m.aviz) continue;
        const docs=rowsToDocs(rows,m,null,"xls"); BDX.pool=mergeDocs(BDX.pool,docs); n+=docs.length } }
    catch(err){ toast(`${f.name}: ${err.message}`) } }
  BDX.pool.sort((a,b)=>b.data.localeCompare(a.data)||String(b.dl).localeCompare(String(a.dl),"ro",{numeric:true}));
  bdDbState(); toast(n?`${n} documente importate din raport — caută-le sau apasă „Adaugă toate rezultatele”`:"Nu am găsit DL-uri / facturi / avize în fișier"); $("bdQ").focus(); bdSearch();
});

/* ---------- căutare cu listă derulantă (potrivire parțială, toate datele) ---------- */
let bdHits=[], bdSel=0;
async function bdAllDocs(){ let db=[]; if(DBX.dir&&DBX.tables&&BDX.cfg&&(BDX.cfg.lines||BDX.cfg.head)){ try{ db=await bdDbDocs() }catch(e){ $("bdResInfo").textContent="Nu am putut citi documentele: "+e.message } }
  return mergeDocs(JSON.parse(JSON.stringify(db)),BDX.pool).sort((a,b)=>b.data.localeCompare(a.data)||String(b.dl).localeCompare(String(a.dl),"ro",{numeric:true})) }
async function bdSearch(force){
  const all=await bdAllDocs();
  if(!all.length){ $("bdResInfo").textContent=""; $("bdDrop").hidden=true; return }
  // o singură dată aleasă (doar „De la”) = documentele din ziua respectivă
  const from=$("bdFrom").value, to=$("bdTo").value||$("bdFrom").value, q=norm($("bdQ").value.trim()), words=q.split(/\s+/).filter(Boolean);
  bdHits=all.filter(o=>(!from||o.data>=from)&&(!to||o.data<=to)&&words.every(w=>o._t.includes(w)))
    .map(o=>({o,s:!q?0:[o.dl,o.factura,o.aviz].some(x=>norm(x)===q)?0:[o.dl,o.factura,o.aviz].some(x=>norm(x).startsWith(q))?1:2})).sort((a,b)=>a.s-b.s).map(x=>x.o);
  bdSel=0;
  $("bdResInfo").textContent=`${all.length.toLocaleString("ro-RO")} documente disponibile · ${bdHits.length.toLocaleString("ro-RO")} corespund căutării`;
  if(force===true||document.activeElement===$("bdQ")) bdDrawDrop();
}
const bdK = o => o.dl||o.factura||o.aviz;
const bdLim = () => $("bdFrom").value||$("bdTo").value ? 2000 : 150; // pe o dată / interval se afișează toate documentele
function bdDrawDrop(){ // listă derulantă cu bife: bifat = documentul e în borderou (se adaugă / se scoate imediat)
  const inB=new Set(BD.docs.map(bdK)), r=$("bdDrop"); r.hidden=false; $("bdQ").setAttribute("aria-expanded","true");
  const H=bdHits.slice(0,bdLim()), allIn=H.length&&H.every(o=>inB.has(bdK(o)));
  r.innerHTML = H.length ? `<div class="dall" data-all="1" role="option" aria-selected="false"><input type="checkbox" tabindex="-1" ${allIn?"checked":""} aria-hidden="true"><span><b>${allIn?"Debifează toate":"Bifează toate"} (${H.length}${bdHits.length>H.length?` din ${bdHits.length}`:""})</b><small>${inB.size} documente în borderou</small></span><span></span></div>`+
    H.map((o,i)=>{ const inn=inB.has(bdK(o)); return `<div role="option" data-h="${i}" aria-selected="${i===bdSel}" aria-checked="${inn}" class="${inn?"on":""}">
      <input type="checkbox" tabindex="-1" ${inn?"checked":""} aria-hidden="true"><span><code>${esc(o.dlLabel||o.dl||o.factura||o.aviz)}</code> ${esc(o.client||"—")}${o.adresa?` · ${esc(o.adresa)}`:""}<small>${[o.factura&&"fact. "+o.factura,o.aviz&&"aviz "+o.aviz,roD(o.data),o.lines?`${o.lines.length} produse`:""].filter(Boolean).map(esc).join(" · ")}</small></span>
      <span class="pr">${o.val==null?"":fmtL(o.val)+" lei"}</span></div>` }).join("")
    : '<div class="empty">Niciun document găsit. Încearcă doar o parte din număr, client sau adresă.</div>';
  const a=r.querySelector('[data-h][aria-selected="true"]'); a&&a.scrollIntoView({block:"nearest"});
}
function bdAddDoc(o){ if(BD.docs.some(d=>bdK(d)===bdK(o))) return false; const {_t,...d}=o; BD.docs.push({...JSON.parse(JSON.stringify(d)),anexa:false,incasat:d.incasat??null}); return true }
function bdToggle(i){ // bifă → preluare automată în borderou; debifare → scoatere
  const o=bdHits[i]; if(!o) return; const k=bdK(o), at=BD.docs.findIndex(d=>bdK(d)===k);
  if(at>=0){ BD.docs.splice(at,1); toast(`Scos: ${o.dlLabel||k}`) } else { bdAddDoc(o); toast(`Adăugat: ${o.dlLabel||k}`) }
  bdRender(); bdSave(); const st=$("bdDrop").scrollTop; bdDrawDrop(); $("bdDrop").scrollTop=st;
}
function bdToggleAll(){
  const H=bdHits.slice(0,bdLim()), inB=new Set(BD.docs.map(bdK)), allIn=H.every(o=>inB.has(bdK(o)));
  if(allIn){ const ks=new Set(H.map(bdK)); BD.docs=BD.docs.filter(d=>!ks.has(bdK(d))); toast(`${H.length} documente scoase`) }
  else { const n=H.filter(bdAddDoc).length; toast(`${n} documente adăugate`) }
  bdRender(); bdSave(); bdDrawDrop();
}
$("bdAddAll").onclick=async()=>{ if(!bdHits.length) await bdSearch(); const n=bdHits.filter(bdAddDoc).length; bdRender(); bdSave(); bdSearch(); toast(n?`${n} documente adăugate`:"Niciun document nou de adăugat") };
["bdFrom","bdTo"].forEach(id=>$(id).addEventListener("change",()=>bdSearch(true))); // alegi data → lista se deschide cu toate documentele din acea zi
$("bdQ").addEventListener("input",()=>{ clearTimeout(bdSearch.t); bdSearch.t=setTimeout(bdSearch,150) });
$("bdQ").addEventListener("focus",()=>bdSearch());
$("bdQ").addEventListener("keydown",e=>{ if($("bdDrop").hidden) return;
  if(e.key==="ArrowDown"){bdSel=Math.min(bdSel+1,Math.min(bdHits.length,bdLim())-1);bdDrawDrop();e.preventDefault()}
  else if(e.key==="ArrowUp"){bdSel=Math.max(bdSel-1,0);bdDrawDrop();e.preventDefault()}
  else if(e.key==="Enter"||e.key===" "&&e.ctrlKey){bdToggle(bdSel);e.preventDefault()} else if(e.key==="Escape"){$("bdDrop").hidden=true} });
$("bdDrop").addEventListener("mousedown",e=>{ e.preventDefault(); if(e.target.closest("[data-all]")){ bdToggleAll(); return } const d=e.target.closest("[data-h]"); if(d) bdToggle(+d.dataset.h) });
document.addEventListener("click",e=>{ if(!e.target.closest(".bdsearch")){ $("bdDrop").hidden=true; $("bdQ").setAttribute("aria-expanded","false") } });

/* ---------- setări: alegerea tabelelor din bază ---------- */
$("bdSetup").onclick=()=>{ const b=$("bdCfg"); b.hidden=!b.hidden; if(!b.hidden) bdSetupDraw() };
const BF_LBL={dl:"Nr. DL",cli:"Cod client",client:"Nume client",adresa:"Adresă / punct livrare",loc:"Localitate",factura:"Nr. factură",aviz:"Nr. aviz",doc:"Nr. document",data:"Data",val:"De încasat",incasat:"Încasat",chitanta:"Nr. chitanță",grdl:"Greutate DL",cod:"Cod articol",q:"Cantitate",pv:"Preț fără TVA",den:"Denumire produs",codm:"Cod / model afișat",gr:"Greutate unitară",sofer:"Șofer"};
function bdSetupDraw(){
  const T=DBX.tables||[], C=BDX.cfg||(BDX.cfg={});
  const block=(key,title)=>{ const s=C[key]||{t:"",map:{}}, t=T.find(x=>x.name===s.t);
    return `<div class="grid"><label>${title}<select data-b="${key}" data-tbl="1"><option value="">— nefolosit —</option>${T.map(x=>`<option ${x.name===s.t?"selected":""} value="${esc(x.name)}">${esc(x.name)} · ${x.n.toLocaleString("ro-RO")} rânduri</option>`).join("")}</select></label>
      ${t?Object.keys(BF_LBL).map(k=>`<label>${BF_LBL[k]}<select data-b="${key}" data-k="${k}"><option value="">—</option>${t.fields.map(f=>`<option ${f.name===s.map[k]?"selected":""}>${f.name}</option>`).join("")}</select></label>`).join(""):""}</div>` };
  $("bdCfg").innerHTML=`<b>Setări documente</b><span class="um" style="font-size:12.5px">Tabelul cu DL-uri (nr. DL, client, factură, sumă) și/sau tabelul cu produsele pe DL (nr. DL, cod articol, cantitate, preț fără TVA).</span>`+
    block("head","Tabel DL-uri")+block("lines","Tabel produse pe DL")+
    `<div class="confirm"><button type="button" class="btn primary" id="bdCfgSave">Salvează</button><button type="button" class="btn" id="bdCfgAuto">Detectează din nou</button><button type="button" class="btn" id="bdCfgCopy">Copiază structura bazei</button><button type="button" class="btn" id="bdCfgClose">Închide</button></div>`;
  $("bdCfg").querySelectorAll("select[data-b]").forEach(x=>x.onchange=()=>{ const b=x.dataset.b;
    if(x.dataset.tbl){ const t=T.find(y=>y.name===x.value); C[b]=x.value?{t:x.value,map:mapFor(t.fields.map(f=>f.name))}:null; bdSetupDraw() } else C[b].map[x.dataset.k]=x.value });
  $("bdCfgSave").onclick=()=>{ store.set("bd_cfg3",C); bdResetDb(); $("bdCfg").hidden=true; bdDbState(); bdSearch() };
  $("bdCfgAuto").onclick=()=>{ BDX.cfg=bdDetect(T); bdSetupDraw() };
  $("bdCfgClose").onclick=()=>{ $("bdCfg").hidden=true };
  $("bdCfgCopy").onclick=()=>{ const txt=T.map(t=>`${t.name} (${t.n} rânduri): ${t.fields.map(f=>f.name+":"+f.type+f.len).join(", ")}`).join("\n");
    (navigator.clipboard?navigator.clipboard.writeText(txt):Promise.reject()).then(()=>toast("Structura bazei a fost copiată"),()=>$("bdCfg").insertAdjacentHTML("beforeend",`<pre>${esc(txt)}</pre>`)) };
}

/* ---------- arhivă borderouri ---------- */
function bdDb(){ return BDX.db || (BDX.db=new Promise((res,rej)=>{ const r=indexedDB.open("borderouri_arhiva",1); r.onupgradeneeded=()=>r.result.createObjectStore("b",{keyPath:"id"}); r.onsuccess=()=>res(r.result); r.onerror=()=>rej(r.error) })) }
async function bdAll(){ try{ const d=await bdDb(); return await new Promise(r=>{ const q=d.transaction("b").objectStore("b").getAll(); q.onsuccess=()=>r(q.result||[]); q.onerror=()=>r([]) }) }catch(e){ return [] } }
async function bdPut(o){ try{ const d=await bdDb(); await new Promise(r=>{ const t=d.transaction("b","readwrite"); t.objectStore("b").put(o); t.oncomplete=r; t.onerror=r }) }catch(e){} }
async function bdDel(id){ try{ const d=await bdDb(); await new Promise(r=>{ const t=d.transaction("b","readwrite"); t.objectStore("b").delete(id); t.oncomplete=r; t.onerror=r }) }catch(e){} }
async function bdArhSave(){
  if(!BD.docs.length && !BD.sofer && !BD.firma) return;
  if(!BD.id){ BD.id=Date.now().toString(36)+Math.random().toString(36).slice(2,7); store.set("bd_draft",BD) }
  await bdPut({id:BD.id,nr:BD.nr,data:BD.data,firma:BD.firma,sofer:BD.sofer,auto:BD.auto,docs:BD.docs.length,val:totInc(),
    text:BD.docs.map(d=>[d.dlLabel,d.factura,d.aviz,d.client].join(" ")).join(" "),updated:new Date().toISOString(),state:JSON.parse(JSON.stringify(BD))});
  $("bdState").textContent=`${BD.nr} · salvat automat ${new Date().toLocaleTimeString("ro-RO",{hour:"2-digit",minute:"2-digit"})}`;
  if(!$("bdHist").hidden) bdHistDraw();
}
async function bdHistDraw(){
  const q=norm($("bdHistQ").value.trim()), all=(await bdAll()).sort((a,b)=>b.updated.localeCompare(a.updated));
  const L=all.filter(o=>!q||norm([o.nr,o.firma,o.sofer,o.auto,o.text,roD(o.data)].join(" ")).includes(q));
  $("bdHistCount").textContent=`${L.length} din ${all.length}`;
  $("bdHistRows").innerHTML = L.length ? L.map(o=>`<tr data-id="${o.id}" class="${o.id===BD.id?"cur":""}"><td class="code">${esc(o.nr)}</td><td class="um">${roD(o.data)}</td><td>${esc(o.sofer||"—")}</td><td>${esc(o.auto||"—")}</td>
      <td class="n um">${o.docs}</td><td class="n val">${fmtL(o.val)} lei</td><td class="um">${new Date(o.updated).toLocaleString("ro-RO",{day:"2-digit",month:"2-digit",year:"numeric",hour:"2-digit",minute:"2-digit"})}</td>
      <td class="acts">${o.id===BD.id?'<span class="um">deschis acum</span>':'<button type="button" class="btn sm" data-a="open">Deschide</button>'} <button type="button" class="btn sm" data-a="dup">Duplică</button> <button type="button" class="btn sm danger" data-a="del">Șterge</button></td></tr>`).join("")
    : `<tr class="emptyrow"><td colspan="8">${all.length?"Niciun borderou nu se potrivește căutării.":"Încă nu există borderouri salvate. Se salvează automat pe măsură ce le completezi."}</td></tr>`;
}
$("bdHistBtn").onclick=()=>{ const h=$("bdHist"); h.hidden=!h.hidden; if(!h.hidden){ bdHistDraw(); $("bdHistQ").focus() } };
$("bdHistClose").onclick=()=>{ $("bdHist").hidden=true }; $("bdHistQ").addEventListener("input",bdHistDraw);
$("bdHistRows").addEventListener("click",async e=>{ const b=e.target.closest("button[data-a]"); if(!b) return; const id=b.closest("tr").dataset.id, o=(await bdAll()).find(x=>x.id===id); if(!o) return;
  if(b.dataset.a==="del"){ if(b.dataset.sure){ await bdDel(id); bdHistDraw(); toast("Borderou șters") } else { b.dataset.sure="1"; b.textContent="Sigur? Șterge" } return }
  await bdArhSave(); BD=bdMigrate(JSON.parse(JSON.stringify(o.state)));
  if(b.dataset.a==="dup"){ BD.id=""; BD.nr=bdNextNr(); BD.data=todayISO() }
  bdRenderHead(); bdRender(); bdSave(); bdHistDraw(); toast(b.dataset.a==="dup"?`Copie: ${BD.nr}`:`Deschis: ${BD.nr}`) });

/* ---------- export (PDF / Word / print) ---------- */
function bdSaveWarn(){ if(!BD.docs.length){ toast("Adaugă cel puțin un document"); return false } bdRemember(); return true }
const bdFile = ext => `Borderou-${(BD.nr||"BL").replace(/[^\w-]+/g,"-")}${BD.data?"-"+BD.data:""}${BD.sofer?"-"+BD.sofer.normalize("NFD").replace(/[̀-ͯ]/g,"").replace(/[^\w]+/g,"-"):""}.${ext}`;
const kmE = () => BD.kmS&&BD.kmP ? String(num(BD.kmS)-num(BD.kmP)) : "";
const grT = () => { const g=BD.docs.reduce((a,d)=>a+(+d.gr||0),0); return g?fmtL(g)+" kg":"" };
function bdHeadPairs(){ return [["Data",roD(BD.data)],["Șofer",BD.sofer+(BD.tel?" · "+BD.tel:"")],["Nr. mașină",BD.auto],["Cursa nr.",BD.cursa],["Gestiune",BD.gestiune],["Firmă transportatoare",BD.firma],
  ["Km plecare",BD.kmP],["Km sosire",BD.kmS],["Km efectuați",kmE()],["Greutate totală",grT()]] }
function bdDocRows(){ const sv=BD.showVal; return BD.docs.map((d,i)=>[String(i+1),d.dlLabel||d.dl||"",d.client||"",d.adresa||"",d.factura||"",d.aviz||"",...(sv?[d.val==null?"":fmtL(d.val),d.incasat==null?"":fmtL(d.incasat)]:[]),d.chitanta||""]) }
const bdDocHead = () => ["Nr. crt","Nr. DL","Firma","Adresa","Nr. factură","Nr. aviz",...(BD.showVal?["De încasat","Încasat"]:[]),"Nr. chitanță"];
function bdPDF(){
  const {jsPDF}=window.jspdf, d=new jsPDF({unit:"mm",format:"a4",orientation:"landscape"}), OR=[255,103,31], INK=[34,37,42], MU=[108,111,118], LN=[200,198,194], SO=[246,244,241], CI=[194,71,11];
  d.addFileToVFS("Roboto-Regular.ttf",FONT_R); d.addFont("Roboto-Regular.ttf","Roboto","normal"); d.addFileToVFS("Roboto-Bold.ttf",FONT_B); d.addFont("Roboto-Bold.ttf","Roboto","bold");
  const W=297,M=12,R=W-M,H=210, txt=(s,x,y,o={})=>{d.setFont("Roboto",o.b?"bold":"normal");d.setFontSize(o.s||9);d.setTextColor(...(o.c||INK));d.text(String(s),x,y,o.a?{align:o.a}:undefined)};
  const head=(label,y)=>{txt(label.toUpperCase(),M,y,{b:1,s:8.5,c:CI});const w=d.getTextWidth(label.toUpperCase());d.setDrawColor(...LN);d.setLineWidth(.2);d.line(M+w+3,y-1.1,R,y-1.1)};
  const header=()=>{ d.addImage(BRANDS.nmc.logo,"PNG",M,9,24,14.8); BD_ISSUER.forEach(([b,t],i)=>txt(b||t,M+28,12+i*3.7,{s:7.4,b:!i,c:i?MU:INK}));
    txt("BORDEROU DE LIVRARE",R,15,{b:1,s:15,a:"right"}); txt(`Nr. ${BD.nr} · ${roD(BD.data)}`,R,21,{b:1,s:9,a:"right"}); d.setFillColor(...OR); d.rect(M,27,W-2*M,.8,"F") };
  header(); let y=33;
  const P=bdHeadPairs(), cw=(W-2*M)/5;
  P.forEach(([k,v],i)=>{ const x=M+(i%5)*cw, yy=y+Math.floor(i/5)*9.5; txt(k.toUpperCase(),x,yy,{s:6.6,c:MU}); txt(v||"—",x,yy+4.2,{s:9.6,b:k==="Greutate totală"}) });
  y+=21;
  const sv=BD.showVal;
  d.autoTable({startY:y,margin:{left:M,right:M,bottom:14},theme:"grid",head:[bdDocHead()],body:bdDocRows(),
    styles:{font:"Roboto",fontSize:8.4,textColor:INK,cellPadding:1.6,lineColor:LN,lineWidth:.2,valign:"middle"},
    headStyles:{fillColor:SO,textColor:INK,fontStyle:"bold",fontSize:7.6,halign:"center"},
    columnStyles:Object.assign({0:{cellWidth:12,halign:"center"},1:{cellWidth:28},4:{cellWidth:26},5:{cellWidth:20}},sv?{6:{cellWidth:24,halign:"right"},7:{cellWidth:22,halign:"right"},8:{cellWidth:24}}:{6:{cellWidth:26}})});
  y=d.lastAutoTable.finalY+5;
  txt(`${BD.docs.length} documente${sv?` · Total de încasat: ${fmtL(totInc())} lei · Total încasat: ${fmtL(totIncasat())} lei`:""}`,R,y,{b:1,s:9.5,a:"right"}); y+=6;
  const MR=BD.marfa?bdMarfaRows():[];
  if(MR.length){ if(y>H-30){d.addPage();header();y=33} head("Total marfă",y+2); y+=5;
    const av=BD.anexaVal;
    d.autoTable({startY:y,margin:{left:M,right:M,bottom:14},theme:"plain",head:[["Cod","Denumire","Cantitate",...(av?["Valoare cu TVA"]:[])]],
      body:MR.map(r=>[r.c,r.n,String(Math.round(r.q*1000)/1000).replace(".",","),...(av?[fmtL(r.v)]:[])]),
      styles:{font:"Roboto",fontSize:7.8,textColor:INK,cellPadding:{top:.7,bottom:.7,left:1.4,right:1.4},lineColor:LN,lineWidth:{bottom:.1}},headStyles:{fillColor:SO,textColor:MU,fontStyle:"normal",fontSize:7},
      columnStyles:Object.assign({0:{cellWidth:30,textColor:CI},2:{cellWidth:22,halign:"right",fontStyle:"bold"}},av?{3:{cellWidth:28,halign:"right"}}:{})});
    y=d.lastAutoTable.finalY+6 }
  if(y>H-34){d.addPage();header();y=33}
  txt(`Total încasat = ${fmtL(totIncasat())} lei`,W/2,y+2,{b:1,s:10,a:"center"}); y+=8;
  [["Alimentare stație",BD.statie],["Nr. litri",BD.litri],["Valoare",BD.valComb?BD.valComb+" lei":""]].forEach(([k,v],i)=>{ txt(k+":",M,y+i*5,{s:9,c:MU}); txt(v||"",M+32,y+i*5,{s:9.5}) });
  if(BD.info.trim()){ d.setFont("Roboto","normal");d.setFontSize(9);const L=d.splitTextToSize("Observații: "+BD.info.trim(),130); d.setTextColor(...INK); d.text(L,M+90,y) }
  y+=20; d.setDrawColor(...LN); d.line(M,y,M+70,y); d.line(R-70,y,R,y); txt("Predat (gestionar),",M,y+4,{s:8,c:MU}); txt("Semnătura șofer,",R-70,y+4,{s:8,c:MU});
  const A=BD.docs.filter(x=>x.anexa);
  if(A.length){ d.addPage(); header(); y=33; head("Anexă – produse pe documente",y); y+=4;
    A.forEach((x,k)=>{ if(y>H-30){d.addPage();header();y=33}
      txt(`Anexa ${k+1} – DL ${x.dlLabel||x.dl||"—"}${x.factura?" · factura "+x.factura:""}${x.aviz?" · aviz "+x.aviz:""} · ${x.client}${x.adresa?" · "+x.adresa:""}`,M,y+3,{b:1,s:9}); y+=5;
      const av=BD.anexaVal;
      d.autoTable({startY:y,margin:{left:M,right:M,bottom:14},theme:"plain",head:[["Cod","Denumire","UM","Cantitate",...(av?["Valoare cu TVA"]:[])]],
        body:(x.lines&&x.lines.length?x.lines:[{c:"",n:"(fără produse)",u:"",q:"",v:null}]).map(l=>[l.c,l.n,l.u,l.q===""||l.q==null?"":String(l.q).replace(".",","),...(av?[l.v==null?"":fmtL(l.v)]:[])]),
        styles:{font:"Roboto",fontSize:8.2,textColor:INK,cellPadding:1.4,lineColor:LN,lineWidth:{bottom:.15}},headStyles:{fillColor:SO,textColor:MU,fontStyle:"normal",fontSize:7},
        columnStyles:Object.assign({0:{cellWidth:30,textColor:CI},2:{cellWidth:14,textColor:MU},3:{cellWidth:22,halign:"right"}},av?{4:{cellWidth:28,halign:"right"}}:{})});
      y=d.lastAutoTable.finalY+7 }) }
  const n=d.getNumberOfPages(); for(let i=1;i<=n;i++){ d.setPage(i); d.setDrawColor(...LN); d.line(M,H-9,R,H-9); txt("NMC Stil Distribution SRL · Borderou de livrare",M,H-5,{s:7,c:MU}); txt(`${BD.nr} · pagina ${i}/${n}`,R,H-5,{s:7,c:MU,a:"right"}) }
  return d.output("blob");
}
function bdDOCX(){
  const NMCHEX="FF671F", INKC="C2470B", FULL=15398, sv=BD.showVal;
  const hd=t=>para(t.toUpperCase(),{b:1,s:9,c:INKC,before:200,after:60,border:4,bc:"DEDBD6"});
  const logo=`<w:p><w:r><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0"><wp:extent cx="864000" cy="532000"/><wp:docPr id="1" name="Logo NMC"/><a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:nvPicPr><pic:cNvPr id="1" name="logo.png"/><pic:cNvPicPr/></pic:nvPicPr><pic:blipFill><a:blip r:embed="rIdLogo"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill><pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="864000" cy="532000"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>`;
  let body=table([1500,8398,5500],[tr(cell(logo,1500)+cell(BD_ISSUER.map(([b,t],i)=>cp(b||t,{s:8,b:!i,c:i?"6C6F76":"22252A"})).join(""),8398)+
    cell(cp("BORDEROU DE LIVRARE",{b:1,s:15,a:"right"})+cp(`Nr. ${BD.nr} · ${roD(BD.data)}`,{b:1,s:10,a:"right"}),5500))],{noBorder:1});
  body+=para("",{border:18,bc:NMCHEX,after:100});
  const P=bdHeadPairs(), cw=Math.floor(FULL/5);
  body+=table(Array(5).fill(cw),[0,1].map(rw=>tr(P.slice(rw*5,rw*5+5).map(([k,v])=>cell(cp(k.toUpperCase(),{s:7,c:"6C6F76"})+cp(v||"—",{s:10,b:k==="Greutate totală"}),cw)).join(""))),{noBorder:1});
  body+=hd("Documente livrate");
  const HH=bdDocHead(), Wd=sv?[700,1700,2900,3000,1600,1200,1500,1300,1498]:[700,1800,3400,3800,1800,1400,2498];
  const rows=[tr(HH.map((h,i)=>cell(cp(h,{s:7.5,b:1,a:sv&&(i===6||i===7)?"right":undefined}),Wd[i],{fill:"F6F4F1"})).join(""),1)];
  bdDocRows().forEach(r=>rows.push(tr(r.map((v,j)=>cell(cp(v,{s:8.8,a:sv&&(j===6||j===7)?"right":undefined}),Wd[j])).join(""))));
  body+=table(Wd,rows);
  body+=para(`${BD.docs.length} documente${sv?` · Total de încasat: ${fmtL(totInc())} lei · Total încasat: ${fmtL(totIncasat())} lei`:""}`,{b:1,s:10,a:"right",before:100});
  const MR=BD.marfa?bdMarfaRows():[], av=BD.anexaVal;
  if(MR.length){ body+=hd("Total marfă"); const MW=av?[2400,8698,2000,2300]:[2600,10298,2500];
    body+=table(MW,[tr(["Cod","Denumire","Cantitate",...(av?["Valoare cu TVA"]:[])].map((h,i)=>cell(cp(h,{s:7.5,c:"6C6F76",a:i>=2?"right":undefined}),MW[i],{fill:"F6F4F1"})).join(""),1),
      ...MR.map(r=>tr([r.c,r.n,String(Math.round(r.q*1000)/1000).replace(".",","),...(av?[fmtL(r.v)]:[])].map((v,i)=>cell(cp(v,{s:8.5,b:i===2,c:i===0?INKC:undefined,a:i>=2?"right":undefined}),MW[i])).join("")))]) }
  body+=para(`Total încasat = ${fmtL(totIncasat())} lei`,{b:1,s:11,a:"center",before:200,after:120});
  body+=para(`Alimentare stație: ${BD.statie||""}`,{s:9.5})+para(`Nr. litri: ${BD.litri||""}`,{s:9.5})+para(`Valoare: ${BD.valComb?BD.valComb+" lei":""}`,{s:9.5});
  if(BD.info.trim()) body+=para("Observații: "+BD.info.trim(),{s:9.5,before:80});
  body+=para("",{after:400})+table([6000,3398,6000],[tr(cell(para("Predat (gestionar),",{s:9,c:"6C6F76",border:4,bc:"9A9A9A"}),6000)+cell(cp(""),3398)+cell(para("Semnătura șofer,",{s:9,c:"6C6F76",border:4,bc:"9A9A9A"}),6000))],{noBorder:1});
  const A=BD.docs.filter(x=>x.anexa);
  if(A.length){ body+=`<w:p><w:r><w:br w:type="page"/></w:r></w:p>`+hd("Anexă – produse pe documente");
    A.forEach((x,k)=>{ body+=para(`Anexa ${k+1} – DL ${x.dlLabel||x.dl||"—"}${x.factura?" · factura "+x.factura:""}${x.aviz?" · aviz "+x.aviz:""} · ${x.client}${x.adresa?" · "+x.adresa:""}`,{b:1,s:10,before:140,after:60});
      const AW=av?[2400,8398,1000,1600,2000]:[2400,9898,1200,1900], AH=["Cod","Denumire","UM","Cantitate",...(av?["Valoare cu TVA"]:[])];
      body+=table(AW,[tr(AH.map((h,i)=>cell(cp(h,{s:7.5,c:"6C6F76",a:i>=3?"right":undefined}),AW[i],{fill:"F6F4F1"})).join(""),1),
        ...(x.lines||[]).map(l=>tr([l.c,l.n,l.u,l.q==null?"":String(l.q).replace(".",","),...(av?[l.v==null?"":fmtL(l.v)]:[])].map((v,i)=>cell(cp(v,{s:8.8,a:i>=3?"right":undefined,c:i===0?INKC:undefined}),AW[i])).join("")))]) }) }
  const doc=`<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"><w:body>${body}<w:sectPr><w:pgSz w:w="16838" w:h="11906" w:orient="landscape"/><w:pgMar w:top="600" w:right="720" w:bottom="600" w:left="720" w:header="360" w:footer="360" w:gutter="0"/></w:sectPr></w:body></w:document>`;
  const enc=new TextEncoder(), files=[
    ["[Content_Types].xml",`<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Default Extension="png" ContentType="image/png"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/></Types>`],
    ["_rels/.rels",`<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>`],
    ["word/_rels/document.xml.rels",`<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rIdLogo" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/logo.png"/></Relationships>`],
    ["word/document.xml",doc]].map(([n,c])=>({name:n,data:enc.encode(c)}));
  files.push({name:"word/media/logo.png",data:b64bytes(BRANDS.nmc.logo.split(",")[1])});
  return zipStore(files,"application/vnd.openxmlformats-officedocument.wordprocessingml.document");
}
$("bdPdf").onclick=()=>{ if(!bdSaveWarn()) return; download(bdPDF(),bdFile("pdf")); toast("PDF descărcat: "+bdFile("pdf")) };
$("bdDoc").onclick=()=>{ if(!bdSaveWarn()) return; download(bdDOCX(),bdFile("docx")); toast("Word descărcat: "+bdFile("docx")) };
$("bdPrint").onclick=()=>{ if(!bdSaveWarn()) return; window.print() };

/* ---------- pornire foaie ---------- */
async function bdShow(){
  if(!BD){ BD=bdMigrate(store.get("bd_draft")||bdBlank()); bdFillLists(); bdRenderHead(); bdRender(); $("bdFrom").value=""; $("bdTo").value="" }
  if(framed){ $("bdPdf").hidden=$("bdDoc").hidden=$("bdPrint").hidden=true }
  bdDbState();
  try{ if(window.showDirectoryPicker && await bdEnsureDb(false)){ bdDbState(); await bdSearch() } }catch(e){}
}
