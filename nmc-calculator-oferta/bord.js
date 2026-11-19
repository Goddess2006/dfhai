/* Foaia „Borderou livrări”: documente (facturi / avize) preluate din aceeași bază a gestiunii ca foaia de parteneri,
   cu antet NMC, transportator / șofer / nr. auto memorate (listă derulantă), anexă opțională cu produsele documentelor,
   export PDF / Word / print și arhivă de borderouri. Inserat de build.py; folosește DBX, listTables, readTable, dbUse,
   idbGet, fx, tbase, store, toast, download, esc, norm, num, todayISO, zipStore, b64bytes, BRANDS. */
const BD_ISSUER=[["NMC Stil Distribution SRL",""],["","CUI RO16109528 · Reg. Com. J40/1507/2004"],["","Autostrada București–Pitești km 13, clădirea A, Chiajna, Ilfov"],["","Tel. 021 319 35 35 · www.nmcromania.ro"]];
const BDRX = {
  nr:/^(NRDOC|NR_DOC|NRFACT|NR_FACT|NRAVIZ|NR_AVIZ|NUMAR|NRDOCUM|NR_DOCUM|NRFACTURA|NRAV)$/, data:/^(DATA|DATADOC|DATA_DOC|DATAFACT|DATA_FACT|DATAEMIT|DATAAVIZ|DATAF)$/,
  cli:/^(CODCLI|COD_CLI|CODPART|COD_PART|CODTERT|CODBEN|CODCLIENT)$/, val:/^(VALCUTVA|VAL_CU_TVA|TOTCUTVA|TOTALTVA|TOTAL|VALTOT|VAL_TOT|TOTALFACT|VALFACT|VALOARE|VALOARETVA|SUMA|VAL)$/,
  tip:/^(TIPDOC|TIP_DOC|TIP|FELDOC|TIPFACT)$/, cod:/^(CODPR|COD_PR|CODART|CODPROD)$/, cant:/^(CANTIT|CANT|CANTITATE|CANTIT_)$/,
  lval:/^(VALCUTVA|VALOARE|VAL|VALVANZ|VALTOT|VAL_TOT)$/, lpret:/^(PRETVANZ|PRET|PU|PRET_V|PRETV)$/, um:/^(UM|U_M|UNIT)$/, den:/^(DENUMIRE|DENPR|DEN)$/ };
const BDX = { cfg:store.get("bd_cfg"), cache:{}, results:[] };
const isoD = s => s&&s.length===8 ? `${s.slice(0,4)}-${s.slice(4,6)}-${s.slice(6)}` : (s||"");
const roD = s => s ? s.split("-").reverse().join(".") : "";
const fmtL = v => v==null||v==="" ? "" : new Intl.NumberFormat("ro-RO",{minimumFractionDigits:2,maximumFractionDigits:2}).format(v);
const dfield = t => (t.fields.find(f=>BDRX.data.test(f.name)&&(f.type==="D"||f.type==="T"))||t.fields.find(f=>f.type==="D"||f.type==="T")||{}).name||"";

/* ---------- starea borderoului ---------- */
let BD;
function bdNextNr(){ const y=new Date().getFullYear(); let c=store.get("bd_counter")||{y,n:0}; if(c.y!==y)c={y,n:0}; c.n++; store.set("bd_counter",c); return "BL-"+y+"-"+String(c.n).padStart(4,"0") }
function bdBlank(){ return {id:"", nr:bdNextNr(), data:todayISO(), firma:"", sofer:"", auto:"", tel:"", info:"", showVal:true, anexaVal:false, docs:[]} }
function bdSave(){ store.set("bd_draft",BD); clearTimeout(bdSave.t); bdSave.t=setTimeout(bdArhSave,400) }
const bdLists = () => store.get("bd_lists") || {firma:[],sofer:[],auto:[]};
function bdRemember(){ // transportator / șofer / nr. auto rămân în listele derulante după prima introducere
  const L=bdLists(); let ch=false;
  const add=(k,v,extra)=>{ v=(v||"").trim(); if(!v) return; let e=L[k].find(x=>(x.name||x).toLowerCase()===v.toLowerCase());
    if(!e){ e={name:v}; L[k].push(e); ch=true } if(extra){ for(const [kk,vv] of Object.entries(extra)) if(vv&&e[kk]!==vv){ e[kk]=vv; ch=true } } };
  add("firma",BD.firma); add("sofer",BD.sofer,{tel:BD.tel,firma:BD.firma,auto:BD.auto}); add("auto",BD.auto,{firma:BD.firma});
  if(ch){ store.set("bd_lists",L); bdFillLists() }
}
function bdFillLists(){
  const L=bdLists(), o=a=>a.map(x=>`<option value="${esc(x.name||x)}"></option>`).join("");
  $("dlFirma").innerHTML=o(L.firma); $("dlSofer").innerHTML=o(L.sofer); $("dlAuto").innerHTML=o(L.auto);
}

/* ---------- afișare ---------- */
function bdRenderHead(){
  $("bdLogo").src=BRANDS.nmc.logo; $("bdIssuer").innerHTML=BD_ISSUER.map(([b,t])=>(b?`<b>${esc(b)}</b>`:"")+esc(t)).join("<br>");
  $("bdNr").value=BD.nr; $("bdData").value=BD.data; $("bdFirma").value=BD.firma; $("bdSofer").value=BD.sofer; $("bdAuto").value=BD.auto; $("bdTel").value=BD.tel;
  $("bdInfo").value=BD.info; $("bdShowVal").checked=BD.showVal; $("bdAnexaVal").checked=BD.anexaVal;
}
function bdRender(){
  const tb=$("bdRows");
  tb.innerHTML = BD.docs.length ? BD.docs.map((d,i)=>`<tr>
      <td class="um">${i+1}</td>
      <td class="cl"><input data-i="${i}" data-k="client" value="${esc(d.client)}" aria-label="Client document ${i+1}">${d.cui?`<small>${esc(d.cui)}</small>`:""}</td>
      <td><select data-i="${i}" data-k="tip" aria-label="Tip document ${i+1}"><option ${d.tip==="Factură"?"selected":""}>Factură</option><option ${d.tip==="Aviz"?"selected":""}>Aviz</option></select></td>
      <td><input data-i="${i}" data-k="nr" value="${esc(d.nr)}" style="width:110px" aria-label="Nr. document ${i+1}"></td>
      <td><input type="date" data-i="${i}" data-k="data" value="${esc(d.data)}" aria-label="Data document ${i+1}"></td>
      <td class="n">${BD.showVal?`<input data-i="${i}" data-k="val" inputmode="decimal" value="${d.val==null?"":fmtL(d.val).replace(/\./g,"")}" style="width:110px;text-align:right" aria-label="Valoare document ${i+1}">`:'<span class="um">—</span>'}</td>
      <td class="noprint" style="text-align:center"><input type="checkbox" data-i="${i}" data-k="anexa" ${d.anexa?"checked":""} aria-label="Include în anexă documentul ${i+1}" style="width:16px;height:16px;accent-color:var(--accent)"></td>
      <td class="sig"></td>
      <td class="noprint"><button class="x" data-del="${i}" aria-label="Scoate documentul ${i+1}">×</button></td></tr>`).join("")
    : `<tr class="emptyrow"><td colspan="9">Niciun document încă. Caută facturile / avizele de livrat mai sus sau adaugă un document manual.</td></tr>`;
  const tot=BD.docs.reduce((a,d)=>a+(+d.val||0),0);
  $("bdTot").innerHTML = `<span>${BD.docs.length} ${BD.docs.length===1?"document":"documente"}</span>${BD.showVal?`<span>Valoare totală: <b>${fmtL(tot)} lei</b></span>`:""}`;
  bdRenderAnexa();
  $("bdState").textContent = BD.id ? `${BD.nr} · salvat automat` : BD.nr;
}
function bdRenderAnexa(){
  const A=BD.docs.map((d,i)=>[d,i]).filter(([d])=>d.anexa);
  $("bdAnexa").classList.toggle("empty",!A.length);
  $("bdAnexaBody").innerHTML = A.length ? A.map(([d,i],k)=>`<div class="anx">
      <div class="ah"><b>Anexa ${k+1} – ${esc(d.tip)} nr. ${esc(d.nr)} din ${roD(d.data)}</b><span>${esc(d.client)}</span></div>
      <div class="tbl" style="border:0;border-radius:0"><table><thead><tr><th>Cod</th><th>Denumire</th><th>UM</th><th class="n">Cantitate</th>${BD.anexaVal?'<th class="n">Valoare (lei)</th>':""}<th class="noprint"></th></tr></thead><tbody>
      ${(d.lines||[]).map((l,j)=>`<tr><td><input data-d="${i}" data-j="${j}" data-k="c" value="${esc(l.c)}" style="width:90px"></td><td><input data-d="${i}" data-j="${j}" data-k="n" value="${esc(l.n)}" style="width:100%;text-align:left"></td>
        <td><input data-d="${i}" data-j="${j}" data-k="u" value="${esc(l.u)}" style="width:56px"></td><td class="n"><input data-d="${i}" data-j="${j}" data-k="q" inputmode="decimal" value="${String(l.q??"").replace(".",",")}" style="width:80px;text-align:right"></td>
        ${BD.anexaVal?`<td class="n"><input data-d="${i}" data-j="${j}" data-k="v" inputmode="decimal" value="${l.v==null?"":fmtL(l.v).replace(/\./g,"")}" style="width:100px;text-align:right"></td>`:""}
        <td class="noprint"><button class="x" data-ldel="${i}:${j}" aria-label="Șterge produsul">×</button></td></tr>`).join("")
        || `<tr class="emptyrow"><td colspan="6">${d.manual?"Adaugă produsele documentului.":"Nu am găsit produsele acestui document în bază — le poți adăuga manual."}</td></tr>`}
      </tbody></table></div>
      <div class="confirm noprint" style="padding:6px 10px"><button type="button" class="btn sm" data-ladd="${i}">+ Produs</button></div></div>`).join("")
    : `<p class="um noprint">Bifează „Anexă” la documentele pentru care vrei lista de produse.</p>`;
  $("bdAnexa").querySelectorAll("input").forEach(x=>x.classList.add("pu"));
}

/* ---------- editare ---------- */
const bdIn=(id,k,fn)=>$(id).addEventListener("input",e=>{ BD[k]=fn?fn(e.target):e.target.value; bdSave(); if(k==="nr"||k==="data") $("bdState").textContent=BD.nr });
bdIn("bdNr","nr"); bdIn("bdData","data"); bdIn("bdInfo","info"); bdIn("bdFirma","firma"); bdIn("bdAuto","auto"); bdIn("bdTel","tel");
$("bdSofer").addEventListener("input",e=>{ BD.sofer=e.target.value; const s=bdLists().sofer.find(x=>x.name===BD.sofer);
  if(s){ if(s.tel&&!BD.tel){BD.tel=s.tel;$("bdTel").value=s.tel} if(s.auto&&!BD.auto){BD.auto=s.auto;$("bdAuto").value=s.auto} if(s.firma&&!BD.firma){BD.firma=s.firma;$("bdFirma").value=s.firma} } bdSave() });
["bdFirma","bdSofer","bdAuto","bdTel"].forEach(id=>$(id).addEventListener("change",bdRemember));
$("bdShowVal").onchange=e=>{ BD.showVal=e.target.checked; bdRender(); bdSave() };
$("bdAnexaVal").onchange=e=>{ BD.anexaVal=e.target.checked; bdRenderAnexa(); bdSave() };
$("bdRows").addEventListener("input",e=>{ const i=e.target.dataset.i,k=e.target.dataset.k; if(i==null||k==="anexa") return; const d=BD.docs[i];
  d[k] = k==="val" ? (e.target.value.trim()===""?null:num(e.target.value)) : e.target.value; bdSave();
  if(k==="val"){ const tot=BD.docs.reduce((a,x)=>a+(+x.val||0),0); $("bdTot").innerHTML=`<span>${BD.docs.length} documente</span>${BD.showVal?`<span>Valoare totală: <b>${fmtL(tot)} lei</b></span>`:""}` } });
$("bdRows").addEventListener("change",async e=>{ const i=e.target.dataset.i,k=e.target.dataset.k; if(k==="tip"){ bdRenderAnexa() }
  if(k==="anexa"){ const d=BD.docs[i]; d.anexa=e.target.checked; if(d.anexa&&!d.lines&&d.src!=null){ try{ d.lines=await bdLinesFor(d) }catch(err){ d.lines=[] } } if(d.anexa&&!d.lines) d.lines=[]; bdRenderAnexa(); bdSave() } });
$("bdRows").addEventListener("click",e=>{ if(e.target.dataset.del!=null){ BD.docs.splice(+e.target.dataset.del,1); bdRender(); bdSave() } });
$("bdAnexaBody").addEventListener("input",e=>{ const t=e.target; if(t.dataset.d==null) return; const l=BD.docs[t.dataset.d].lines[t.dataset.j], k=t.dataset.k;
  l[k] = k==="q"||k==="v" ? (t.value.trim()===""?null:num(t.value)) : t.value; bdSave() });
$("bdAnexaBody").addEventListener("click",e=>{ const t=e.target;
  if(t.dataset.ladd!=null){ const d=BD.docs[t.dataset.ladd]; (d.lines=d.lines||[]).push({c:"",n:"",u:"buc",q:1,v:null}); bdRenderAnexa(); bdSave() }
  if(t.dataset.ldel){ const [i,j]=t.dataset.ldel.split(":"); BD.docs[i].lines.splice(+j,1); bdRenderAnexa(); bdSave() } });
$("bdAddManual").onclick=()=>{ BD.docs.push({key:"m"+Date.now(),manual:true,tip:"Factură",nr:"",data:todayISO(),client:"",val:null,anexa:false,lines:null}); bdRender(); bdSave(); const ins=$("bdRows").querySelectorAll('input[data-k="client"]'); ins[ins.length-1]?.focus() };
$("bdNew").onclick=()=>{ $("bdConfirmNew").hidden=false }; $("bdNewNo").onclick=()=>{ $("bdConfirmNew").hidden=true };
$("bdNewYes").onclick=async()=>{ await bdArhSave(); const keep={firma:BD.firma,sofer:BD.sofer,auto:BD.auto,tel:BD.tel}; BD=bdBlank(); Object.assign(BD,keep); $("bdConfirmNew").hidden=true; bdRenderHead(); bdRender(); bdSave(); toast("Borderou nou: "+BD.nr) };
$("bdLists").onclick=()=>{ const b=$("bdListsBox"); b.hidden=!b.hidden; if(!b.hidden) bdDrawLists() };
function bdDrawLists(){
  const L=bdLists(), sec=(k,t)=>`<div><b style="font-size:13px">${t}</b><div style="display:flex;flex-wrap:wrap;gap:6px;margin-top:6px">${L[k].length?L[k].map((x,i)=>`<span class="chipx">${esc(x.name)}${x.tel?` · ${esc(x.tel)}`:""} <button class="x" data-lk="${k}" data-li="${i}" aria-label="Șterge ${esc(x.name)}">×</button></span>`).join(""):'<span class="um">— gol —</span>'}</div></div>`;
  $("bdListsBox").innerHTML=sec("firma","Firme transportatoare")+sec("sofer","Șoferi")+sec("auto","Numere auto")+`<span class="um" style="font-size:12px">Valorile noi se adaugă automat în liste când le scrii în borderou.</span>`;
}
$("bdListsBox").addEventListener("click",e=>{ const b=e.target.closest("[data-lk]"); if(!b) return; const L=bdLists(); L[b.dataset.lk].splice(+b.dataset.li,1); store.set("bd_lists",L); bdFillLists(); bdDrawLists() });

/* ---------- documente din baza gestiunii ---------- */
function bdDetect(T){
  const cfg={srcs:[]}, has=(t,rx)=>fx(t,rx);
  const heads=T.filter(t=>has(t,BDRX.nr)&&dfield(t)&&has(t,BDRX.cli)&&!has(t,BDRX.cod))
    .map(t=>({t,s:(has(t,BDRX.val)?2:0)+(/FACT|AVIZ|IES|VANZ|DOC/.test(tbase(t))?3:0)+(has(t,BDRX.tip)?1:0)+Math.min(3,Math.log10(t.n+1))}))
    .sort((a,b)=>b.s-a.s).slice(0,2);
  for(const {t} of heads){
    const nrF=fx(t,BDRX.nr), stem=tbase(t).slice(0,3);
    const lines=T.filter(x=>x!==t&&x.fields.some(f=>f.name===nrF)&&has(x,BDRX.cod)&&has(x,BDRX.cant))
      .map(x=>({x,s:(tbase(x).startsWith(stem)?3:0)+(/LIN|POZ|DET|CONT|ART/.test(tbase(x))?2:0)+Math.log10(x.n+1)})).sort((a,b)=>b.s-a.s)[0];
    const L=lines&&lines.x;
    cfg.srcs.push({label:/AVIZ/.test(tbase(t))?"Aviz":"Factură", t:t.name, nr:nrF, data:dfield(t), cli:fx(t,BDRX.cli), val:fx(t,BDRX.val), tip:fx(t,BDRX.tip),
      lt:L?L.name:"", lnr:L?nrF:"", ldata:L?(L.fields.find(f=>f.name===dfield(t))?.name||""):"", lcod:L?fx(L,BDRX.cod):"", lcant:L?fx(L,BDRX.cant):"", lval:L?fx(L,BDRX.lval):"", lpret:L?fx(L,BDRX.lpret):"", lum:L?fx(L,BDRX.um):"", lden:L?fx(L,BDRX.den):""});
  }
  const ct=T.find(t=>/^CLIENT$/.test(tbase(t))&&t.fields.some(f=>f.name==="NUMECLI")) || T.find(t=>fx(t,/^(CODCLI|COD_CLI)$/)&&fx(t,RX.cname)&&!fx(t,BDRX.nr));
  if(ct) cfg.cli={t:ct.name, code:fx(ct,/^(CODCLI|COD_CLI|CODPART)$/), name:fx(ct,RX.cname), cui:fx(ct,RX.cui)};
  return cfg;
}
async function bdTable(name, only){ const k=name+"|"+(only||[]).join(","); if(!BDX.cache[k]){ const t=DBX.tables.find(x=>x.name===name); if(!t) return []; BDX.cache[k]=await readTable(t,only) } return BDX.cache[k] }
async function bdClients(){
  const c=BDX.cfg&&BDX.cfg.cli; if(!c||!c.code) return {};
  if(!BDX.cliMap){ BDX.cliMap={}; for(const r of await bdTable(c.t,[c.code,c.name,c.cui].filter(Boolean))) BDX.cliMap[String(r[c.code]).trim()]={n:String(r[c.name]||"").trim(),cui:c.cui?String(r[c.cui]||"").trim():""} }
  return BDX.cliMap;
}
async function bdProducts(){
  if(BDX.prodMap) return BDX.prodMap; BDX.prodMap={};
  const P=DBX.cfg&&DBX.cfg.prod; if(P&&DBX.tables.some(t=>t.name===P.t)) for(const r of await bdTable(P.t,[P.code,P.name,P.um].filter(Boolean))) BDX.prodMap[String(r[P.code]).trim()]={n:String(r[P.name]||"").trim(),u:P.um?String(r[P.um]||"").trim().toLowerCase():""};
  return BDX.prodMap;
}
async function bdEnsureDb(interactive){
  if(!DBX.dir){ const d=await idbGet("dir"); if(d) DBX.dir=d }
  if(!DBX.dir) return false;
  let perm=await DBX.dir.queryPermission({mode:"read"}); if(perm!=="granted"&&interactive) perm=await DBX.dir.requestPermission({mode:"read"});
  if(perm!=="granted") return false;
  if(!DBX.tables) DBX.tables=await listTables(DBX.dir);
  if(!DBX.cfg){ try{ DBX.cfg=await autoDetect(DBX.tables); store.set("np_dbcfg2",DBX.cfg) }catch(e){} }
  if(!BDX.cfg||!BDX.cfg.srcs||!BDX.cfg.srcs.length){ BDX.cfg=bdDetect(DBX.tables); store.set("bd_cfg",BDX.cfg) }
  return true;
}
function bdDbState(){
  const ok=!!(DBX.dir&&DBX.tables), n=BDX.cfg&&BDX.cfg.srcs?BDX.cfg.srcs.filter(s=>s.t).length:0;
  $("bdDbState").innerHTML = ok ? `Baza de date a gestiunii: <span class="ok">conectată</span> (${esc(DBX.dir.name)})` : "Baza de date a gestiunii: neconectată";
  $("bdDbInfo").textContent = !window.showDirectoryPicker ? "Legătura directă cu baza merge în Google Chrome sau Microsoft Edge. Documentele se pot adăuga și manual."
    : ok ? (n ? `Documente din: ${BDX.cfg.srcs.filter(s=>s.t).map(s=>`${s.label.toLowerCase()} → ${s.t}${s.lt?` (produse: ${s.lt})`:""}`).join(" · ")}` : "Nu am găsit tabelele cu facturi / avize — deschide „Setări documente” sau trimite structura bazei.")
    : (DBX.dir ? "Apasă „Reîncarcă documentele” ca să dai acces la folder." : "Conectează folderul bazei (ex. \\\\rds.nmc.local\\Backup\\baze), la fel ca în foaia NMC Parteneri.");
  $("bdConnect").hidden=!window.showDirectoryPicker; $("bdConnect").textContent=DBX.dir?"Schimbă folderul":"Conectează folderul bazei";
  $("bdReload").hidden=!DBX.dir; $("bdSetup").hidden=!ok;
}
$("bdConnect").onclick=async()=>{ try{ const dir=await window.showDirectoryPicker({id:"baze-gestiune",mode:"read"}); BDX.cache={}; BDX.cliMap=null; BDX.prodMap=null;
  if(DBX.dir&&DBX.dir.name!==dir.name){ DBX.cfg=null; store.set("np_dbcfg2",null); BDX.cfg=null; store.set("bd_cfg",null) }
  await dbUse(dir); DBX.tables=null; await bdEnsureDb(true); bdDbState(); bdSearch() }catch(e){ if(e.name!=="AbortError") toast("Nu am putut deschide folderul: "+e.message) } };
$("bdReload").onclick=async()=>{ BDX.cache={}; BDX.cliMap=null; BDX.prodMap=null; DBX.tables=null; try{ if(await bdEnsureDb(true)){ bdDbState(); await bdSearch(); toast("Documente reîncărcate") } else toast("Fără permisiune de citire pentru folder") }catch(e){ toast("Nu am putut citi baza: "+e.message) } };
async function bdSearch(){
  if(!(DBX.dir&&DBX.tables)||!BDX.cfg||!BDX.cfg.srcs){ $("bdResWrap").hidden=true; $("bdAddSel").hidden=true; return }
  const from=($("bdFrom").value||"0000-00-00").replace(/-/g,""), to=($("bdTo").value||"9999-99-99").replace(/-/g,""), q=norm($("bdQ").value.trim()), tipF=$("bdTip").value;
  const cl=await bdClients(), out=[];
  for(const [si,s] of BDX.cfg.srcs.entries()){ if(!s.t||!s.nr||!s.data) continue;
    const rows=await bdTable(s.t,[s.nr,s.data,s.cli,s.val,s.tip].filter(Boolean));
    for(const r of rows){ const d=String(r[s.data]||""); if(!d||d<from||d>to) continue;
      const tip = s.tip&&r[s.tip]!=null&&String(r[s.tip]).trim() ? (/AV/i.test(String(r[s.tip]))?"Aviz":/FA|FC/i.test(String(r[s.tip]))?"Factură":s.label) : s.label;
      if(tipF&&tip!==tipF) continue;
      const c=cl[String(r[s.cli]).trim()]||{n:s.cli?`Client cod ${String(r[s.cli]).trim()}`:"",cui:""};
      const nr=String(r[s.nr]).trim(); if(q&&!norm(nr+" "+c.n+" "+c.cui).includes(q)) continue;
      out.push({key:`${s.t}|${nr}|${d}`,src:si,tip,nr,data:isoD(d),client:c.n,cui:c.cui,val:s.val&&+r[s.val]?Math.round(+r[s.val]*100)/100:null});
    } }
  out.sort((a,b)=>b.data.localeCompare(a.data)||b.nr.localeCompare(a.nr,"ro",{numeric:true}));
  BDX.results=out.slice(0,400); const inB=new Set(BD.docs.map(d=>d.key));
  $("bdResWrap").hidden=false; $("bdAddSel").hidden=!BDX.results.length;
  $("bdRes").innerHTML = BDX.results.length ? BDX.results.map((r,i)=>`<tr><td><input type="checkbox" data-r="${i}" ${inB.has(r.key)?"disabled checked":""} aria-label="Selectează ${esc(r.nr)}" style="width:16px;height:16px;accent-color:var(--accent)"></td>
      <td class="um">${r.tip}</td><td class="code">${esc(r.nr)}</td><td class="um">${roD(r.data)}</td><td>${esc(r.client)}${r.cui?`<small style="display:block;color:var(--muted);font-size:11.5px">${esc(r.cui)}</small>`:""}</td>
      <td class="n val">${r.val==null?"—":fmtL(r.val)}</td><td class="n um">${inB.has(r.key)?"în borderou":""}</td></tr>`).join("")
    : `<tr class="emptyrow"><td colspan="7">Niciun document în intervalul ales.</td></tr>`;
  $("bdResInfo").textContent = `${out.length} ${out.length===1?"document":"documente"} găsite${out.length>400?" (primele 400)":""}`;
}
["bdFrom","bdTo","bdTip"].forEach(id=>$(id).addEventListener("change",bdSearch));
$("bdQ").addEventListener("input",()=>{ clearTimeout(bdSearch.t); bdSearch.t=setTimeout(bdSearch,250) });
$("bdAddSel").onclick=()=>{ const sel=[...$("bdRes").querySelectorAll("input[data-r]:checked:not(:disabled)")].map(c=>BDX.results[+c.dataset.r]);
  if(!sel.length){ toast("Bifează documentele de adăugat"); return }
  sel.forEach(r=>BD.docs.push({...r,anexa:false,lines:null})); bdRender(); bdSave(); bdSearch(); toast(`${sel.length} documente adăugate`) };
async function bdLinesFor(d){
  const s=BDX.cfg&&BDX.cfg.srcs[d.src]; if(!s||!s.lt||!await bdEnsureDb(true)) return [];
  const rows=await bdTable(s.lt,[s.lnr,s.ldata,s.lcod,s.lcant,s.lval,s.lpret,s.lum,s.lden].filter(Boolean)), P=await bdProducts(), dd=d.data.replace(/-/g,"");
  return rows.filter(r=>String(r[s.lnr]).trim()===d.nr && (!s.ldata||!r[s.ldata]||String(r[s.ldata])===dd)).map(r=>{
    const c=String(r[s.lcod]).trim(), p=P[c]||{}, q=+r[s.lcant]||0;
    const v = s.lval&&r[s.lval]!=null ? +r[s.lval] : (s.lpret&&r[s.lpret]!=null ? +r[s.lpret]*q : null);
    return {c, n:(s.lden&&String(r[s.lden]||"").trim())||p.n||`Articol cod ${c}`, u:(s.lum&&String(r[s.lum]||"").trim().toLowerCase())||p.u||"buc", q:Math.round(q*1000)/1000, v:v==null?null:Math.round(v*100)/100};
  });
}
/* setări: alegerea tabelelor de documente */
$("bdSetup").onclick=()=>{ const b=$("bdCfg"); b.hidden=!b.hidden; if(!b.hidden) bdSetupDraw() };
function bdSetupDraw(){
  const T=DBX.tables||[], C=BDX.cfg||(BDX.cfg={srcs:[]}); while(C.srcs.length<2) C.srcs.push({label:C.srcs.length?"Aviz":"Factură",t:"",lt:""});
  const tsel=(si,key,val)=>`<select data-s="${si}" data-k="${key}" data-tbl="1"><option value="">— nefolosit —</option>${T.map(t=>`<option ${t.name===val?"selected":""} value="${esc(t.name)}">${esc(t.name)} · ${t.n.toLocaleString("ro-RO")} rânduri</option>`).join("")}</select>`;
  const fsel=(si,key,label,tn)=>{ const t=T.find(x=>x.name===tn), v=C.srcs[si][key]||""; return `<label>${label}<select data-s="${si}" data-k="${key}"><option value="">—</option>${(t?t.fields:[]).map(f=>`<option ${f.name===v?"selected":""}>${f.name}</option>`).join("")}</select></label>` };
  $("bdCfg").innerHTML=`<b>Setări documente</b><span class="um" style="font-size:12.5px">Alege tabelul cu antetele documentelor (nr., dată, client, valoare) și tabelul cu produsele lor. Poți folosi două surse (ex. facturi și avize).</span>`+
    C.srcs.map((s,si)=>`<div class="grid"><label>Sursa ${si+1} – tip implicit<select data-s="${si}" data-k="label"><option ${s.label==="Factură"?"selected":""}>Factură</option><option ${s.label==="Aviz"?"selected":""}>Aviz</option></select></label>
      <label>Tabel documente${tsel(si,"t",s.t)}</label>${fsel(si,"nr","Nr. document",s.t)}${fsel(si,"data","Data",s.t)}${fsel(si,"cli","Cod client",s.t)}${fsel(si,"val","Valoare",s.t)}${fsel(si,"tip","Tip document (opțional)",s.t)}
      <label>Tabel produse pe document${tsel(si,"lt",s.lt)}</label>${fsel(si,"lnr","Nr. document",s.lt)}${fsel(si,"ldata","Data (opțional)",s.lt)}${fsel(si,"lcod","Cod articol",s.lt)}${fsel(si,"lcant","Cantitate",s.lt)}${fsel(si,"lval","Valoare (opțional)",s.lt)}${fsel(si,"lpret","Preț (opțional)",s.lt)}</div>`).join("")+
    `<div class="confirm"><button type="button" class="btn primary" id="bdCfgSave">Salvează</button><button type="button" class="btn" id="bdCfgAuto">Detectează din nou</button><button type="button" class="btn" id="bdCfgCopy">Copiază structura bazei</button><button type="button" class="btn" id="bdCfgClose">Închide</button></div>`;
  $("bdCfg").querySelectorAll("select[data-s]").forEach(x=>x.onchange=()=>{ C.srcs[x.dataset.s][x.dataset.k]=x.value; if(x.dataset.tbl) bdSetupDraw() });
  $("bdCfgSave").onclick=()=>{ C.srcs=C.srcs.filter(s=>s.t); store.set("bd_cfg",C); BDX.cache={}; $("bdCfg").hidden=true; bdDbState(); bdSearch() };
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
  if(!BD.docs.length && !BD.firma && !BD.sofer) return;
  if(!BD.id){ BD.id=Date.now().toString(36)+Math.random().toString(36).slice(2,7); store.set("bd_draft",BD) }
  await bdPut({id:BD.id,nr:BD.nr,data:BD.data,firma:BD.firma,sofer:BD.sofer,docs:BD.docs.length,val:BD.docs.reduce((a,d)=>a+(+d.val||0),0),
    text:BD.docs.map(d=>d.nr+" "+d.client).join(" "),updated:new Date().toISOString(),state:JSON.parse(JSON.stringify(BD))});
  $("bdState").textContent=`${BD.nr} · salvat automat ${new Date().toLocaleTimeString("ro-RO",{hour:"2-digit",minute:"2-digit"})}`;
  if(!$("bdHist").hidden) bdHistDraw();
}
async function bdHistDraw(){
  const q=norm($("bdHistQ").value.trim()), all=(await bdAll()).sort((a,b)=>b.updated.localeCompare(a.updated));
  const L=all.filter(o=>!q||norm([o.nr,o.firma,o.sofer,o.text,roD(o.data)].join(" ")).includes(q));
  $("bdHistCount").textContent=`${L.length} din ${all.length}`;
  $("bdHistRows").innerHTML = L.length ? L.map(o=>`<tr data-id="${o.id}" class="${o.id===BD.id?"cur":""}"><td class="code">${esc(o.nr)}</td><td class="um">${roD(o.data)}</td><td>${esc(o.firma||"—")}</td><td>${esc(o.sofer||"—")}</td>
      <td class="n um">${o.docs}</td><td class="n val">${fmtL(o.val)} lei</td><td class="um">${new Date(o.updated).toLocaleString("ro-RO",{day:"2-digit",month:"2-digit",year:"numeric",hour:"2-digit",minute:"2-digit"})}</td>
      <td class="acts">${o.id===BD.id?'<span class="um">deschis acum</span>':'<button type="button" class="btn sm" data-a="open">Deschide</button>'} <button type="button" class="btn sm" data-a="dup">Duplică</button> <button type="button" class="btn sm danger" data-a="del">Șterge</button></td></tr>`).join("")
    : `<tr class="emptyrow"><td colspan="8">${all.length?"Niciun borderou nu se potrivește căutării.":"Încă nu există borderouri salvate. Se salvează automat pe măsură ce le completezi."}</td></tr>`;
}
$("bdHistBtn").onclick=()=>{ const h=$("bdHist"); h.hidden=!h.hidden; if(!h.hidden){ bdHistDraw(); $("bdHistQ").focus() } };
$("bdHistClose").onclick=()=>{ $("bdHist").hidden=true }; $("bdHistQ").addEventListener("input",bdHistDraw);
$("bdHistRows").addEventListener("click",async e=>{ const b=e.target.closest("button[data-a]"); if(!b) return; const id=b.closest("tr").dataset.id, o=(await bdAll()).find(x=>x.id===id); if(!o) return;
  if(b.dataset.a==="del"){ if(b.dataset.sure){ await bdDel(id); bdHistDraw(); toast("Borderou șters") } else { b.dataset.sure="1"; b.textContent="Sigur? Șterge" } return }
  await bdArhSave(); BD=JSON.parse(JSON.stringify(o.state));
  if(b.dataset.a==="dup"){ BD.id=""; BD.nr=bdNextNr(); BD.data=todayISO() }
  bdRenderHead(); bdRender(); bdSave(); bdHistDraw(); toast(b.dataset.a==="dup"?`Copie: ${BD.nr}`:`Deschis: ${BD.nr}`) });

/* ---------- export ---------- */
function bdSaveWarn(){ if(!BD.docs.length){ toast("Adaugă cel puțin un document"); return false } bdRemember(); return true }
const bdFile = ext => `Borderou-${(BD.nr||"BL").replace(/[^\w-]+/g,"-")}${BD.data?"-"+BD.data:""}.${ext}`;
function bdPDF(){
  const {jsPDF}=window.jspdf, d=new jsPDF({unit:"mm",format:"a4"}), OR=[255,103,31], INK=[34,37,42], MU=[108,111,118], LN=[222,219,214], SO=[246,244,241], CI=[194,71,11];
  d.addFileToVFS("Roboto-Regular.ttf",FONT_R); d.addFont("Roboto-Regular.ttf","Roboto","normal"); d.addFileToVFS("Roboto-Bold.ttf",FONT_B); d.addFont("Roboto-Bold.ttf","Roboto","bold");
  const W=210,M=14,R=W-M, txt=(s,x,y,o={})=>{d.setFont("Roboto",o.b?"bold":"normal");d.setFontSize(o.s||9);d.setTextColor(...(o.c||INK));d.text(String(s),x,y,o.a?{align:o.a}:undefined)};
  const head=(label,y)=>{txt(label.toUpperCase(),M,y,{b:1,s:8.5,c:CI});const w=d.getTextWidth(label.toUpperCase());d.setDrawColor(...LN);d.setLineWidth(.2);d.line(M+w+3,y-1.1,R,y-1.1)};
  const header=()=>{ d.addImage(BRANDS.nmc.logo,"PNG",M,12,27,16.6); BD_ISSUER.forEach(([b,t],i)=>txt(b||t,M+31,15+i*4,{s:7.6,b:!i,c:i?MU:INK}));
    txt("BORDEROU DE LIVRARE",R,18,{b:1,s:15,a:"right"}); txt("Nr. "+BD.nr,R,25,{b:1,s:9,a:"right"}); txt("Data: "+roD(BD.data),R,30,{s:9,a:"right",c:MU}); d.setFillColor(...OR); d.rect(M,36,W-2*M,.9,"F") };
  header(); let y=44;
  head("Transport",y); y+=5.5;
  [["Firmă transportatoare",BD.firma],["Șofer",BD.sofer+(BD.tel?" · "+BD.tel:"")],["Nr. auto",BD.auto]].forEach(([k,v],i)=>{ const x=M+i*((W-2*M)/3); txt(k.toUpperCase(),x,y,{s:6.8,c:MU}); txt(v||"—",x,y+4.5,{s:10}) });
  y+=12; head("Documente livrate",y); y+=3;
  const hv=BD.showVal;
  d.autoTable({startY:y,margin:{left:M,right:M,bottom:18},theme:"plain",
    head:[["#","Client","Tip","Nr. document","Data emiterii",...(hv?["Valoare (lei)"]:[]),"Semnătură primire"]],
    body:BD.docs.map((x,i)=>[String(i+1),x.client+(x.cui?"\n"+x.cui:""),x.tip,x.nr,roD(x.data),...(hv?[x.val==null?"":fmtL(x.val)]:[]),""]),
    styles:{font:"Roboto",fontSize:8.6,textColor:INK,cellPadding:{top:2.4,bottom:2.4,left:1.6,right:1.6},lineColor:LN,lineWidth:{bottom:.2},minCellHeight:9,valign:"middle"},
    headStyles:{fillColor:SO,textColor:MU,fontStyle:"normal",fontSize:7.2},
    columnStyles:Object.assign({0:{cellWidth:7,textColor:MU},2:{cellWidth:16},3:{cellWidth:24,fontStyle:"bold",textColor:CI},4:{cellWidth:22}},hv?{5:{cellWidth:24,halign:"right"},6:{cellWidth:36}}:{5:{cellWidth:40}})});
  y=d.lastAutoTable.finalY+6;
  const tot=BD.docs.reduce((a,x)=>a+(+x.val||0),0);
  txt(`${BD.docs.length} documente${hv?` · Valoare totală: ${fmtL(tot)} lei`:""}`,R,y,{b:1,s:9.5,a:"right"}); y+=8;
  if(BD.info.trim()){ d.setFont("Roboto","normal");d.setFontSize(9);const L=d.splitTextToSize(BD.info.trim(),W-2*M); if(y+10+L.length*4.4>270){d.addPage();y=20} head("Observații",y); y+=5.5; d.setTextColor(...INK); d.text(L,M,y); y+=L.length*4.4+4 }
  if(y+22>277){d.addPage();y=20} y+=14; d.setDrawColor(...LN); d.line(M,y,M+70,y); d.line(R-70,y,R,y); txt("Predat (gestionar),",M,y+4,{s:8,c:MU}); txt("Primit (șofer / transportator),",R-70,y+4,{s:8,c:MU});
  const A=BD.docs.filter(x=>x.anexa);
  if(A.length){ d.addPage(); header(); y=44; head("Anexă – produse pe documente",y); y+=4;
    A.forEach((x,k)=>{ if(y>255){d.addPage();y=20}
      txt(`Anexa ${k+1} – ${x.tip} nr. ${x.nr} din ${roD(x.data)} · ${x.client}`,M,y+3,{b:1,s:9}); y+=5;
      const av=BD.anexaVal;
      d.autoTable({startY:y,margin:{left:M,right:M,bottom:18},theme:"plain",head:[["Cod","Denumire","UM","Cantitate",...(av?["Valoare (lei)"]:[])]],
        body:(x.lines&&x.lines.length?x.lines:[{c:"",n:"(fără produse)",u:"",q:"",v:null}]).map(l=>[l.c,l.n,l.u,l.q===""||l.q==null?"":String(l.q).replace(".",","),...(av?[l.v==null?"":fmtL(l.v)]:[])]),
        styles:{font:"Roboto",fontSize:8.3,textColor:INK,cellPadding:1.6,lineColor:LN,lineWidth:{bottom:.2}},headStyles:{fillColor:SO,textColor:MU,fontStyle:"normal",fontSize:7},
        columnStyles:Object.assign({0:{cellWidth:24,textColor:CI},2:{cellWidth:14,textColor:MU},3:{cellWidth:22,halign:"right"}},av?{4:{cellWidth:26,halign:"right"}}:{})});
      y=d.lastAutoTable.finalY+7 }) }
  const n=d.getNumberOfPages(); for(let i=1;i<=n;i++){ d.setPage(i); d.setDrawColor(...LN); d.line(M,284,R,284); txt("NMC Stil Distribution SRL · Borderou de livrare",M,288.5,{s:7,c:MU}); txt(`${BD.nr} · pagina ${i}/${n}`,R,288.5,{s:7,c:MU,a:"right"}) }
  return d.output("blob");
}
function bdDOCX(){
  const FULL=10466, hv=BD.showVal, NMCHEX="FF671F", INKC="C2470B";
  const hd=t=>para(t.toUpperCase(),{b:1,s:9,c:INKC,before:240,after:80,border:4,bc:"DEDBD6"});
  const logo=`<w:p><w:r><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0"><wp:extent cx="972000" cy="598000"/><wp:docPr id="1" name="Logo NMC"/><a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:nvPicPr><pic:cNvPr id="1" name="logo.png"/><pic:cNvPicPr/></pic:nvPicPr><pic:blipFill><a:blip r:embed="rIdLogo"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill><pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="972000" cy="598000"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>`;
  let body=table([1500,5166,3800],[tr(cell(logo,1500)+cell(BD_ISSUER.map(([b,t],i)=>cp(b||t,{s:8,b:!i,c:i?"6C6F76":"22252A"})).join(""),5166)+
    cell(cp("BORDEROU DE LIVRARE",{b:1,s:15,a:"right"})+cp("Nr. "+BD.nr,{b:1,s:10,a:"right"})+cp("Data: "+roD(BD.data),{s:9,a:"right",c:"6C6F76"}),3800))],{noBorder:1});
  body+=para("",{border:18,bc:NMCHEX,after:120});
  body+=hd("Transport")+table([3488,3489,3489],[tr([["Firmă transportatoare",BD.firma],["Șofer",BD.sofer+(BD.tel?" · "+BD.tel:"")],["Nr. auto",BD.auto]].map(([k,v])=>cell(cp(k.toUpperCase(),{s:7,c:"6C6F76"})+cp(v||"—",{s:10.5}),3488)).join(""))],{noBorder:1});
  body+=hd("Documente livrate");
  const W=hv?[400,3266,1000,1500,1300,1400,1600]:[400,4166,1000,1500,1300,2100], H=["#","Client","Tip","Nr. document","Data emiterii",...(hv?["Valoare (lei)"]:[]),"Semnătură primire"];
  const rows=[tr(H.map((h,i)=>cell(cp(h,{s:7.5,c:"6C6F76",a:hv&&i===5?"right":undefined}),W[i],{fill:"F6F4F1"})).join(""),1)];
  BD.docs.forEach((x,i)=>rows.push(tr([String(i+1),x.client+(x.cui?"\n"+x.cui:""),x.tip,x.nr,roD(x.data),...(hv?[x.val==null?"":fmtL(x.val)]:[]),""].map((v,j)=>cell(cp(v,{s:9,b:j===3,c:j===3?INKC:j===0?"6C6F76":undefined,a:hv&&j===5?"right":undefined}),W[j])).join(""))));
  body+=table(W,rows);
  const tot=BD.docs.reduce((a,x)=>a+(+x.val||0),0);
  body+=para(`${BD.docs.length} documente${hv?` · Valoare totală: ${fmtL(tot)} lei`:""}`,{b:1,s:10,a:"right",before:120});
  if(BD.info.trim()) body+=hd("Observații")+para(BD.info.trim(),{s:10});
  body+=para("",{after:500})+table([4700,1066,4700],[tr(cell(para("Predat (gestionar),",{s:9,c:"6C6F76",border:4,bc:"9A9A9A"}),4700)+cell(cp(""),1066)+cell(para("Primit (șofer / transportator),",{s:9,c:"6C6F76",border:4,bc:"9A9A9A"}),4700))],{noBorder:1});
  const A=BD.docs.filter(x=>x.anexa), av=BD.anexaVal;
  if(A.length){ body+=`<w:p><w:r><w:br w:type="page"/></w:r></w:p>`+hd("Anexă – produse pe documente");
    A.forEach((x,k)=>{ body+=para(`Anexa ${k+1} – ${x.tip} nr. ${x.nr} din ${roD(x.data)} · ${x.client}`,{b:1,s:10,before:160,after:60});
      const AW=av?[1500,5266,800,1300,1600]:[1600,6566,900,1400], AH=["Cod","Denumire","UM","Cantitate",...(av?["Valoare (lei)"]:[])];
      const r=[tr(AH.map((h,i)=>cell(cp(h,{s:7.5,c:"6C6F76",a:i>=3?"right":undefined}),AW[i],{fill:"F6F4F1"})).join(""),1)];
      (x.lines||[]).forEach(l=>r.push(tr([l.c,l.n,l.u,l.q==null?"":String(l.q).replace(".",","),...(av?[l.v==null?"":fmtL(l.v)]:[])].map((v,i)=>cell(cp(v,{s:9,a:i>=3?"right":undefined,c:i===0?INKC:undefined}),AW[i])).join(""))));
      body+=table(AW,r) }) }
  const doc=`<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"><w:body>${body}<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="680" w:right="720" w:bottom="680" w:left="720" w:header="360" w:footer="360" w:gutter="0"/></w:sectPr></w:body></w:document>`;
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
  if(!BD){ BD=store.get("bd_draft")||bdBlank(); bdFillLists(); bdRenderHead(); bdRender();
    const t=new Date(), f=new Date(t-3*864e5), iso=x=>new Date(x-x.getTimezoneOffset()*6e4).toISOString().slice(0,10);
    $("bdFrom").value=iso(f); $("bdTo").value=iso(t) }
  if(framed){ $("bdPdf").hidden=$("bdDoc").hidden=$("bdPrint").hidden=true }
  bdDbState();
  try{ if(window.showDirectoryPicker && await bdEnsureDb(false)){ bdDbState(); await bdSearch() } }catch(e){}
}
