/* Arhiva de oferte: fiecare ofertă se salvează automat (IndexedDB „oferte_arhiva”) cât lucrezi la ea;
   „Oferte salvate” le listează pe foi, cu căutare, și permite redeschiderea pentru editare, duplicarea, ștergerea
   și backup-ul într-un fișier .json (de păstrat pe server / de mutat pe alt calculator).
   Inserat de build.py; folosește S, B, BRANDS, calc, fmt, nextNr, todayISO, fillForm, renderAll, applyBrand, store, toast, download. */
const ARH = { db:null, cache:null };
function arhOpen(){ return ARH.db || (ARH.db = new Promise((res,rej)=>{ const r=indexedDB.open("oferte_arhiva",1);
  r.onupgradeneeded=()=>{ const st=r.result.createObjectStore("oferte",{keyPath:"id"}); st.createIndex("brand","brand") };
  r.onsuccess=()=>res(r.result); r.onerror=()=>rej(r.error) })) }
async function arhAll(){ try{ const d=await arhOpen(); return await new Promise(r=>{ const q=d.transaction("oferte").objectStore("oferte").getAll(); q.onsuccess=()=>r(q.result||[]); q.onerror=()=>r([]) }) }catch(e){ return [] } }
async function arhPut(o){ try{ const d=await arhOpen(); await new Promise(r=>{ const t=d.transaction("oferte","readwrite"); t.objectStore("oferte").put(o); t.oncomplete=r; t.onerror=r }) }catch(e){} }
async function arhDel(id){ try{ const d=await arhOpen(); await new Promise(r=>{ const t=d.transaction("oferte","readwrite"); t.objectStore("oferte").delete(id); t.oncomplete=r; t.onerror=r }) }catch(e){} }
const uid = () => Date.now().toString(36)+Math.random().toString(36).slice(2,8);

/* salvarea automată: la fiecare save() al ofertei curente (cu întârziere mică) */
let arhTimer=null;
function arhSchedule(){ clearTimeout(arhTimer); arhTimer=setTimeout(arhSaveNow,400) }
async function arhSaveNow(){
  if(!S || S.example) return;
  const empty = !S.lines.length && !(S.client.c_nume||"").trim();
  if(empty) return;
  if(!S.id){ S.id=uid(); S.created=new Date().toISOString(); store.set(B.id+"_oferta_draft",S) }
  const t=calc();
  await arhPut({ id:S.id, brand:B.id, nr:S.nr, data:S.data, client:(S.client.c_nume||"").trim(), cui:(S.client.c_cui||"").trim(),
    total:t.total, cur:S.cur, rate:S.rate, items:S.lines.length, created:S.created, updated:new Date().toISOString(), state:JSON.parse(JSON.stringify(S)) });
  $("histState").textContent = "Salvată automat · "+new Date().toLocaleTimeString("ro-RO",{hour:"2-digit",minute:"2-digit"});
  if(!$("hist").hidden) histDraw();
}

/* panoul „Oferte salvate” */
const BR_NAME = {nmc:"NMC România", np:"NMC Parteneri", df:"Deco&Flair"};
async function histDraw(){
  const all=(await arhAll()).sort((a,b)=>b.updated.localeCompare(a.updated));
  const scope=$("histScope").value, q=norm($("histQ").value.trim());
  const list=all.filter(o=>(scope==="all"||o.brand===scope) && (!q || norm([o.nr,o.client,o.cui,o.data.split("-").reverse().join(".")].join(" ")).includes(q)));
  $("histCount").textContent = `${list.length} ${list.length===1?"ofertă":"oferte"}${scope==="all"?"":" în "+BR_NAME[scope]} · ${all.length} în total`;
  $("histRows").innerHTML = list.length ? list.slice(0,300).map(o=>`<tr data-id="${o.id}" class="${o.id===S.id?"cur":""}">
      <td class="code">${esc(o.nr)}</td><td class="um">${esc(o.data.split("-").reverse().join("."))}</td>
      <td>${esc(o.client||"—")}${o.cui?`<small>${esc(o.cui)}</small>`:""}</td>
      <td class="um">${esc(BR_NAME[o.brand]||o.brand)}</td><td class="n um">${o.items}</td>
      <td class="n val">${new Intl.NumberFormat("ro-RO",{minimumFractionDigits:2,maximumFractionDigits:2}).format(o.cur==="EUR"?o.total/(o.rate||1):o.total)} ${o.cur==="EUR"?"€":"lei"}</td>
      <td class="um">${new Date(o.updated).toLocaleString("ro-RO",{day:"2-digit",month:"2-digit",year:"numeric",hour:"2-digit",minute:"2-digit"})}</td>
      <td class="acts">${o.id===S.id?'<span class="um">deschisă acum</span>':`<button type="button" class="btn sm" data-a="open">Deschide</button>`}
        <button type="button" class="btn sm" data-a="dup">Duplică</button><button type="button" class="btn sm danger" data-a="del">Șterge</button></td></tr>`).join("")
    : `<tr class="emptyrow"><td colspan="8">${all.length?"Nicio ofertă nu se potrivește căutării.":"Încă nu există oferte salvate. Ofertele se salvează automat pe măsură ce le completezi."}</td></tr>`;
}
async function histOpen(id, dup){
  const o=(await arhAll()).find(x=>x.id===id); if(!o) return;
  await arhSaveNow();
  if(o.brand!==B.id){ save(); applyBrand(o.brand) }
  S=JSON.parse(JSON.stringify(o.state)); S.example=false;
  if(dup){ S.id=uid(); S.created=new Date().toISOString(); S.nr=nextNr(); S.data=todayISO() }
  fillForm(); renderAll(); if(dup) arhSaveNow();
  toast(dup?`Copie creată: ${S.nr}`:`Ofertă deschisă: ${S.nr}`);
  histDraw(); window.scrollTo({top:0,behavior:"smooth"});
}
$("histBtn").onclick=()=>{ const h=$("hist"); h.hidden=!h.hidden; $("histBtn").setAttribute("aria-expanded",!h.hidden); if(!h.hidden){ $("histScope").value=B.id; histDraw(); $("histQ").focus() } };
$("histClose").onclick=()=>{ $("hist").hidden=true; $("histBtn").setAttribute("aria-expanded","false") };
$("histQ").addEventListener("input",histDraw); $("histScope").addEventListener("change",histDraw);
$("histRows").addEventListener("click",async e=>{
  const btn=e.target.closest("button[data-a]"); if(!btn) return; const id=btn.closest("tr").dataset.id, a=btn.dataset.a;
  if(a==="open") histOpen(id,false);
  else if(a==="dup") histOpen(id,true);
  else if(a==="del"){
    if(btn.dataset.sure){ await arhDel(id); toast("Oferta a fost ștearsă"); histDraw() }
    else { btn.dataset.sure="1"; btn.textContent="Sigur? Șterge"; setTimeout(()=>{ if(btn.isConnected){ delete btn.dataset.sure; btn.textContent="Șterge" } },4000) }
  }
});
$("histExport").onclick=async()=>{
  const all=await arhAll(); if(!all.length){ toast("Nu există oferte de salvat"); return }
  download(new Blob([JSON.stringify({tip:"oferte-nmc-decoflair",versiune:1,exportat:new Date().toISOString(),oferte:all},null,1)],{type:"application/json"}),`Backup-oferte-${todayISO()}.json`);
  toast(`Backup cu ${all.length} oferte descărcat`);
};
$("histImport").onclick=()=>$("histFile").click();
$("histFile").addEventListener("change",async e=>{
  const f=e.target.files[0]; e.target.value=""; if(!f) return;
  try{
    const d=JSON.parse(await f.text()); const list=Array.isArray(d)?d:d.oferte; if(!Array.isArray(list)) throw new Error("fișierul nu este un backup de oferte");
    const have=new Map((await arhAll()).map(o=>[o.id,o])); let n=0;
    for(const o of list){ if(!o||!o.id||!o.state) continue; const ex=have.get(o.id); if(!ex||ex.updated<o.updated){ await arhPut(o); n++ } }
    toast(`${n} oferte restaurate din backup`); histDraw();
  }catch(err){ toast("Backup-ul nu a putut fi citit: "+err.message) }
});
