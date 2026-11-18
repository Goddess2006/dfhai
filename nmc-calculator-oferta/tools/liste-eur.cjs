/* Convertește listele de preț în EUR (fără TVA) pentru foaia NMC Parteneri -> data/parteneri-eur.json
   Rulare: node tools/liste-eur.cjs   (citește data/liste-eur/*.xls[x]) */
const X=require('../data/lib/xlsx.full.min.js'), fs=require('fs'), path=require('path');
const D=path.join(__dirname,'..','data'), dir=path.join(D,'liste-eur');
const rd=(f,s)=>{const wb=X.read(fs.readFileSync(path.join(dir,f)),{type:'buffer'});return X.utils.sheet_to_json(wb.Sheets[s||wb.SheetNames[0]],{header:1,defval:''})};
const T=s=>String(s??'').replace(/\s+/g,' ').trim();
const umN=u=>{u=T(u).toLowerCase();return u==='pacchet'?'pachet':u==='m'?'m':u||'buc'};
const lists=[], items=[];
for(const f of fs.readdirSync(dir).filter(f=>/\.xlsx?$/i.test(f)).sort()){
  const date=(f.match(/(\d{2})\.(\d{2})\.(\d{4})/)||[])[0]||'';
  if(/Interior_Premium/i.test(f)){
    const R=rd(f,'Lista NMC 2026'); let k='', n=0;
    for(const r of R.slice(2)){
      if(typeof r[0]==='string'&&T(r[0])&&r[1]===''){ if(!/^Preturile/i.test(T(r[0]))) k=T(r[0]); continue }
      const model=T(r[1]), p=+r[10]||+r[9]; if(!model||!(p>0)) continue;
      const len=+r[4]?` · ${String(r[4]).replace('.',',')} ml`:'';
      items.push({c:T(r[0]), m:model, n:`${model} – ${T(r[2])} ${T(r[3])}${len}`.replace(/\s+/g,' ').trim(), u:umN(r[8]), e:+p.toFixed(4), k, src:'Interior Premium'}); n++;
    }
    lists.push({name:'Interior Premium',date,n});
  } else if(/SELIT/i.test(f)){
    let n=0; for(const r of rd(f)){ const p=+r[3]; if(!T(r[0])||!(p>0)||/COD/i.test(r[0])) continue;
      items.push({c:T(r[0]), m:T(r[1]).split(' ')[0], n:`${T(r[1])} · ${String(r[2]).replace('.',',')} m²/pachet`, u:'pachet', e:+p.toFixed(4), k:'Selit – subparchet', src:'Selit'}); n++ }
    lists.push({name:'Selit',date,n});
  } else if(/IZOLATII/i.test(f)){
    let n=0; for(const r of rd(f)){ const p=+r[5]; if(!T(r[2])||!(p>0)||/COD/i.test(r[2])) continue;
      items.push({c:T(r[2]), m:T(r[2]), n:T(r[3]), u:umN(r[4]), e:+p.toFixed(4), k:'Izolații țeavă – '+T(r[1]), src:'Izolații țeavă'}); n++ }
    lists.push({name:'Izolații țeavă',date,n});
  }
}
fs.writeFileSync(path.join(D,'parteneri-eur.json'),JSON.stringify({lists,items}));
console.log(lists.map(l=>`${l.name} ${l.date}: ${l.n}`).join(' | '),'→',items.length,'articole');
