/* Export ofertă: PDF (jsPDF + autotable, font Roboto cu diacritice), Word (.docx generat local) și e-mail.
   Inserat de build.py în index.html; folosește S, calc(), conv(), fmt(), fmtN(), SHIP, TVA din pagină. */
const C_INK=[34,37,42], C_MU=[108,111,118], C_LINE=[222,219,214], C_SOFT=[246,244,241];
const CLIENT_FIELDS=[["c_nume","Nume / Denumire firmă"],["c_cui","CUI / CNP"],["c_reg","Nr. Reg. Com."],["c_pers","Persoană de contact"],["c_tel","Telefon"],["c_email","E-mail"],["c_adr","Adresă facturare"],["c_livr","Adresă livrare"]];
const issuerLines=()=>B.issuer.map(([b,t])=>b+t);

function offer(){
  const t=calc();
  const dateRo=S.data?S.data.split("-").reverse().join("."):"";
  const lines=S.lines.map((l,i)=>[String(i+1),l.c||"",l.n||"",l.u||"",fmtN(l.q).replace(/,00$/,""),fmtN(conv(l.p/(1+TVA))),fmtN(conv(l.p)),fmtN(conv(l.q*l.p))]);
  const totals=[["Valoare produse (cu TVA)",fmt(conv(t.gross))]];
  if(t.disc>0){totals.push([S.dType==="pct"?`Discount ${String(S.disc).replace(".",",")}%`:"Discount","− "+fmt(conv(t.disc))]);totals.push(["Produse după discount",fmt(conv(t.prod))])}
  totals.push([shipName(S.ship),fmt(conv(t.ship))],["Total fără TVA",fmt(conv(t.net))],["TVA 21%",fmt(conv(t.tva))]);
  const other=S.cur==="RON"?"EUR":"RON", otherVal=other==="EUR"?t.total/(S.rate||1):t.total;
  return {t,dateRo,lines,totals,grand:fmt(conv(t.total)),
    alt:`Echivalent ${other} (1 EUR = ${String(S.rate).replace(".",",")} lei): ${fmt(otherVal,other)}`,
    client:CLIENT_FIELDS.map(([k,l])=>[l,(S.client[k]||"").trim()]).filter(x=>x[1]),
    meta:[["Nr. comandă",S.nr||""],["Data",dateRo],["Moneda",S.cur==="EUR"?`EUR (curs ${String(S.rate).replace(".",",")} lei)`:"RON (lei)"]],
    info:(S.info||"").trim(),
    note:`Prețurile și codurile produselor sunt preluate de pe ${B.domain}. Toate prețurile includ TVA 21%.`};
}
function fileBase(){
  const c=(S.client.c_nume||"").normalize("NFD").replace(/[̀-ͯ]/g,"").replace(/[^\w]+/g,"-").replace(/^-|-$/g,"").slice(0,40);
  return "Oferta-"+(S.nr||B.prefix).replace(/[^\w-]+/g,"-")+(c?"-"+c:"");
}
function download(blob,name){
  const a=document.createElement("a"); a.href=URL.createObjectURL(blob); a.download=name; document.body.append(a); a.click(); a.remove();
  setTimeout(()=>URL.revokeObjectURL(a.href),4000);
}
function b64bytes(b64){const s=atob(b64),u=new Uint8Array(s.length);for(let i=0;i<s.length;i++)u[i]=s.charCodeAt(i);return u}

/* ---------- PDF ---------- */
function makePDF(){
  const O=offer(); const {jsPDF}=window.jspdf; const d=new jsPDF({unit:"mm",format:"a4"});
  d.addFileToVFS("Roboto-Regular.ttf",FONT_R); d.addFont("Roboto-Regular.ttf","Roboto","normal");
  d.addFileToVFS("Roboto-Bold.ttf",FONT_B); d.addFont("Roboto-Bold.ttf","Roboto","bold");
  const W=210,M=14,R=W-M; let y;
  const txt=(s,x,yy,o={})=>{d.setFont("Roboto",o.b?"bold":"normal");d.setFontSize(o.s||9);d.setTextColor(...(o.c||C_INK));d.text(String(s),x,yy,o.a?{align:o.a}:undefined)};
  const head=(label,yy)=>{txt(label.toUpperCase(),M,yy,{b:1,s:8.5,c:B.rgbInk});const w=d.getTextWidth(label.toUpperCase());d.setDrawColor(...C_LINE);d.setLineWidth(.2);d.line(M+w+3,yy-1.1,R,yy-1.1)};
  const [lw,lh]=B.logoMM; d.addImage(B.logo,"PNG",M,12+(16.6-lh)/2,lw,lh);
  issuerLines().forEach((l,i,a)=>{const k=a.length>3, yy=(k?13.6:16)+i*(k?3.75:4.4); d.setFont("Roboto",i?"normal":"bold");d.setFontSize(k?7.3:8);d.setTextColor(...(i?C_MU:C_INK));d.text(l,M+lw+4,yy)});
  txt("OFERTĂ DE PREȚ",R,18,{b:1,s:17,a:"right"});
  O.meta.forEach(([k,v],i)=>{txt(k,R-46,25+i*4.8,{s:8.5,c:C_MU,a:"right"});txt(v,R,25+i*4.8,{b:1,s:8.5,a:"right"})});
  d.setFillColor(...B.rgb); d.rect(M,38,W-2*M,.9,"F");
  y=46;
  if(O.client.length){
    head("Date client",y); y+=5.5;
    const colW=(W-2*M)/2;
    O.client.forEach(([k,v],i)=>{const x=M+(i%2)*colW, yy=y+Math.floor(i/2)*9;
      txt(k.toUpperCase(),x,yy,{s:6.8,c:C_MU});
      d.setFont("Roboto","normal");d.setFontSize(9.5);d.setTextColor(...C_INK);d.text(d.splitTextToSize(v,colW-4)[0],x,yy+4)});
    y+=Math.ceil(O.client.length/2)*9+3;
  }
  head("Produse",y); y+=3;
  d.autoTable({startY:y,margin:{left:M,right:M,bottom:18},
    head:[["#","Cod","Produs","UM","Cant.","Preț unitar\nfără TVA","Preț unitar\ncu TVA","Valoare\ncu TVA"]],
    body:O.lines.length?O.lines:[["","","Niciun produs","","","","",""]],
    styles:{font:"Roboto",fontSize:8.3,textColor:C_INK,cellPadding:{top:1.8,bottom:1.8,left:1.6,right:1.6},lineColor:C_LINE,lineWidth:{bottom:.2}},
    headStyles:{fillColor:C_SOFT,textColor:C_MU,fontStyle:"normal",fontSize:7,valign:"middle"},
    columnStyles:{0:{cellWidth:7,textColor:C_MU},1:{cellWidth:22,textColor:B.rgbInk,fontStyle:"bold"},3:{cellWidth:17,textColor:C_MU},4:{cellWidth:12,halign:"right"},5:{cellWidth:20,halign:"right"},6:{cellWidth:20,halign:"right"},7:{cellWidth:23,halign:"right",fontStyle:"bold"}},
    didParseCell:c=>{if(c.section==="head"&&c.column.index>=4)c.cell.styles.halign="right"},
    theme:"plain"});
  y=d.lastAutoTable.finalY+7;
  const boxW=88, bx=R-boxW, rowH=6.4, need=(O.totals.length+2)*rowH+4;
  if(y+need>277){d.addPage();y=20}
  O.totals.forEach(([k,v],i)=>{const yy=y+i*rowH; d.setDrawColor(...C_LINE);d.setLineWidth(.2);d.line(bx,yy+rowH,R,yy+rowH);
    txt(k,bx+2.5,yy+4.3,{s:8.8}); txt(v.replace("−","-"),R-2.5,yy+4.3,{s:8.8,b:1,a:"right",c:k.startsWith("Discount")?[30,142,78]:C_INK})});
  let gy=y+O.totals.length*rowH;
  d.setFillColor(...B.rgb); d.rect(bx,gy,boxW,rowH+2.4,"F");
  txt("TOTAL DE PLATĂ",bx+2.5,gy+5.6,{b:1,s:10,c:[255,255,255]}); txt(O.grand,R-2.5,gy+5.8,{b:1,s:12.5,c:[255,255,255],a:"right"});
  txt(O.alt,R-2.5,gy+rowH+7,{s:7.5,c:C_MU,a:"right"});
  y=gy+rowH+15;
  if(O.info){
    d.setFont("Roboto","normal");d.setFontSize(9);const L=d.splitTextToSize(O.info,W-2*M);
    if(y+8+L.length*4.2>277){d.addPage();y=20}
    head("Informații / date suplimentare",y); y+=5.5; d.setFont("Roboto","normal");d.setFontSize(9);d.setTextColor(...C_INK); d.text(L,M,y,{lineHeightFactor:1.4}); y+=L.length*4.4+4;
  }
  if(y+16>277){d.addPage();y=20}
  y+=10; d.setDrawColor(...C_LINE); d.line(M,y,M+70,y); d.line(R-70,y,R,y);
  txt("Întocmit,",M,y+4,{s:8,c:C_MU}); txt("Client,",R-70,y+4,{s:8,c:C_MU});
  const n=d.getNumberOfPages();
  for(let i=1;i<=n;i++){d.setPage(i);d.setDrawColor(...C_LINE);d.line(M,284,R,284);
    txt(O.note,M,288.5,{s:7,c:C_MU}); txt(`${S.nr||""} · pagina ${i}/${n}`,R,288.5,{s:7,c:C_MU,a:"right"})}
  return d.output("blob");
}

/* ---------- Word (.docx) ---------- */
const X=s=>String(s??"").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");
function run(t,o={}){const pr=`<w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Calibri"/>${o.b?"<w:b/>":""}<w:color w:val="${o.c||"22252A"}"/><w:sz w:val="${Math.round((o.s||10)*2)}"/></w:rPr>`;
  return String(t).split("\n").map((p,i)=>(i?"<w:r><w:br/></w:r>":"")+`<w:r>${pr}<w:t xml:space="preserve">${X(p)}</w:t></w:r>`).join("")}
function para(t,o={}){return `<w:p><w:pPr><w:spacing w:before="${o.before||0}" w:after="${o.after??0}"/>${o.a?`<w:jc w:val="${o.a}"/>`:""}${o.border?`<w:pBdr><w:bottom w:val="single" w:sz="${o.border}" w:space="4" w:color="${o.bc||B.hex}"/></w:pBdr>`:""}</w:pPr>${t?run(t,o):""}</w:p>`}
function cell(content,w,o={}){return `<w:tc><w:tcPr><w:tcW w:w="${w}" w:type="dxa"/>${o.fill?`<w:shd w:val="clear" w:color="auto" w:fill="${o.fill}"/>`:""}${o.span?`<w:gridSpan w:val="${o.span}"/>`:""}<w:vAlign w:val="center"/></w:tcPr>${content}</w:tc>`}
function cp(t,o={}){return para(t,{...o,after:0})}
function table(widths,rows,o={}){
  const b=o.noBorder?`<w:tblBorders><w:top w:val="nil"/><w:left w:val="nil"/><w:bottom w:val="nil"/><w:right w:val="nil"/><w:insideH w:val="nil"/><w:insideV w:val="nil"/></w:tblBorders>`
    :`<w:tblBorders><w:top w:val="single" w:sz="4" w:color="DEDBD6"/><w:left w:val="single" w:sz="4" w:color="DEDBD6"/><w:bottom w:val="single" w:sz="4" w:color="DEDBD6"/><w:right w:val="single" w:sz="4" w:color="DEDBD6"/><w:insideH w:val="single" w:sz="4" w:color="DEDBD6"/><w:insideV w:val="nil"/></w:tblBorders>`;
  return `<w:tbl><w:tblPr><w:tblW w:w="${widths.reduce((a,b)=>a+b,0)}" w:type="dxa"/>${o.jc?`<w:jc w:val="${o.jc}"/>`:""}${b}<w:tblLayout w:type="fixed"/><w:tblCellMar><w:top w:w="50" w:type="dxa"/><w:left w:w="80" w:type="dxa"/><w:bottom w:w="50" w:type="dxa"/><w:right w:w="80" w:type="dxa"/></w:tblCellMar></w:tblPr><w:tblGrid>${widths.map(w=>`<w:gridCol w:w="${w}"/>`).join("")}</w:tblGrid>${rows.join("")}</w:tbl>`;
}
const tr=(cells,head)=>`<w:tr>${head?'<w:trPr><w:tblHeader/></w:trPr>':'<w:trPr><w:cantSplit/></w:trPr>'}${cells}</w:tr>`;
function heading(t){return para(t.toUpperCase(),{b:1,s:9,c:B.hexInk,before:240,after:80,border:4,bc:"DEDBD6"})}
function makeDOCX(){
  const O=offer(), FULL=10466, cx=Math.round(B.logoMM[0]*36000), cy=Math.round(B.logoMM[1]*36000), lcol=B.id==="df"?2300:1500;
  const logo=`<w:p><w:r><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0"><wp:extent cx="${cx}" cy="${cy}"/><wp:docPr id="1" name="Logo NMC"/><a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:nvPicPr><pic:cNvPr id="1" name="logo.png"/><pic:cNvPicPr/></pic:nvPicPr><pic:blipFill><a:blip r:embed="rIdLogo"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill><pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="${cx}" cy="${cy}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>`;
  let body="";
  body+=table([lcol,5966-lcol,4500],[tr(
    cell(logo,lcol)+cell(issuerLines().map((l,i)=>cp(l,{s:B.issuer.length>3?7.5:8.5,c:i?"6C6F76":"22252A",b:!i})).join(""),5966-lcol)+
    cell(cp("OFERTĂ DE PREȚ",{b:1,s:18,a:"right"})+O.meta.map(([k,v])=>`<w:p><w:pPr><w:jc w:val="right"/></w:pPr>${run(k+":  ",{s:9,c:"6C6F76"})}${run(v,{s:9,b:1})}</w:p>`).join(""),4500))],{noBorder:1});
  body+=para("",{border:18,after:120});
  if(O.client.length){
    body+=heading("Date client");
    const rows=[];for(let i=0;i<O.client.length;i+=2){const a=O.client[i],b=O.client[i+1];
      rows.push(tr(cell(cp(a[0].toUpperCase(),{s:7,c:"6C6F76"})+cp(a[1],{s:10}),FULL/2)+cell(b?cp(b[0].toUpperCase(),{s:7,c:"6C6F76"})+cp(b[1],{s:10}):cp(""),FULL/2)))}
    body+=table([FULL/2,FULL/2],rows,{noBorder:1});
  }
  body+=heading("Produse");
  const W=[400,1250,3866,950,700,1100,1100,1100];
  const H=["#","Cod","Produs","UM","Cant.","Preț unitar fără TVA","Preț unitar cu TVA","Valoare cu TVA"];
  const rows=[tr(H.map((h,i)=>cell(cp(h,{s:7.5,c:"6C6F76",a:i>=4?"right":undefined}),W[i],{fill:"F6F4F1"})).join(""),1)];
  O.lines.forEach(r=>rows.push(tr(r.map((v,i)=>cell(cp(v,{s:8.5,a:i>=4?"right":undefined,b:i===1||i===7,c:i===1?B.hexInk:i===0||i===3?"6C6F76":undefined}),W[i])).join(""))));
  body+=table(W,rows);
  body+=para("",{after:160});
  const TW=[3000,1900], trs=O.totals.map(([k,v])=>tr(cell(cp(k,{s:9.5}),TW[0])+cell(cp(v,{s:9.5,b:1,a:"right",c:k.startsWith("Discount")?"1E8E4E":undefined}),TW[1])));
  trs.push(tr(cell(cp("TOTAL DE PLATĂ",{s:11,b:1,c:"FFFFFF"}),TW[0],{fill:B.hex})+cell(cp(O.grand,{s:13,b:1,c:"FFFFFF",a:"right"}),TW[1],{fill:B.hex})));
  trs.push(tr(cell(cp(O.alt,{s:8,c:"6C6F76",a:"right"}),TW[0]+TW[1],{span:2})));
  body+=table(TW,trs,{jc:"right"});
  if(O.info){body+=heading("Informații / date suplimentare");body+=para(O.info,{s:10})}
  body+=para("",{after:600});
  body+=table([4700,1066,4700],[tr(cell(para("Întocmit,",{s:9,c:"6C6F76",border:4,bc:"9A9A9A"}),4700)+cell(cp(""),1066)+cell(para("Client,",{s:9,c:"6C6F76",border:4,bc:"9A9A9A"}),4700))],{noBorder:1});
  body+=para(O.note,{s:7.5,c:"6C6F76",before:400});
  const doc=`<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"><w:body>${body}<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="680" w:right="720" w:bottom="680" w:left="720" w:header="360" w:footer="360" w:gutter="0"/></w:sectPr></w:body></w:document>`;
  const enc=new TextEncoder();
  const files=[
    ["[Content_Types].xml",`<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Default Extension="png" ContentType="image/png"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/></Types>`],
    ["_rels/.rels",`<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>`],
    ["word/_rels/document.xml.rels",`<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rIdLogo" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/logo.png"/></Relationships>`],
    ["word/document.xml",doc]
  ].map(([n,c])=>({name:n,data:enc.encode(c)}));
  files.push({name:"word/media/logo.png",data:b64bytes(B.logo.split(",")[1])});
  return zipStore(files,"application/vnd.openxmlformats-officedocument.wordprocessingml.document");
}
function crc32(u){let t=crc32.t;if(!t){t=crc32.t=new Uint32Array(256);for(let n=0;n<256;n++){let c=n;for(let k=0;k<8;k++)c=c&1?0xEDB88320^(c>>>1):c>>>1;t[n]=c>>>0}}
  let c=0xFFFFFFFF;for(let i=0;i<u.length;i++)c=t[(c^u[i])&255]^(c>>>8);return (c^0xFFFFFFFF)>>>0}
function zipStore(files,type){
  const enc=new TextEncoder(),parts=[],cen=[];let off=0;
  for(const f of files){const nm=enc.encode(f.name),d=f.data,crc=crc32(d);
    const h=new DataView(new ArrayBuffer(30));[[0,0x04034b50,4],[4,20,2],[6,0x0800,2],[8,0,2],[10,0,2],[12,0x21,2],[14,crc,4],[18,d.length,4],[22,d.length,4],[26,nm.length,2],[28,0,2]].forEach(([o,v,s])=>s===4?h.setUint32(o,v,true):h.setUint16(o,v,true));
    parts.push(new Uint8Array(h.buffer),nm,d);
    const c=new DataView(new ArrayBuffer(46));[[0,0x02014b50,4],[4,20,2],[6,20,2],[8,0x0800,2],[10,0,2],[12,0,2],[14,0x21,2],[16,crc,4],[20,d.length,4],[24,d.length,4],[28,nm.length,2],[30,0,2],[32,0,2],[34,0,2],[36,0,2],[38,0,4],[42,off,4]].forEach(([o,v,s])=>s===4?c.setUint32(o,v,true):c.setUint16(o,v,true));
    cen.push(new Uint8Array(c.buffer),nm); off+=30+nm.length+d.length}
  const cs=cen.reduce((a,b)=>a+b.length,0),e=new DataView(new ArrayBuffer(22));
  e.setUint32(0,0x06054b50,true);e.setUint16(8,files.length,true);e.setUint16(10,files.length,true);e.setUint32(12,cs,true);e.setUint32(16,off,true);
  return new Blob([...parts,...cen,new Uint8Array(e.buffer)],{type});
}

/* ---------- e-mail ---------- */
function mailBody(){
  const O=offer(), c=S.client;
  const L=[`Bună ziua${c.c_pers?" "+c.c_pers:c.c_nume?" "+c.c_nume:""},`,"",`Vă transmitem oferta ${B.name} nr. ${S.nr} din data de ${O.dateRo}.`,""];
  O.lines.forEach(r=>L.push(`• ${r[1]} – ${r[2]}: ${r[4]} ${r[3]} x ${r[6]} = ${r[7]} ${S.cur==="EUR"?"€":"lei"}`));
  if(O.lines.length)L.push("");
  O.totals.forEach(([k,v])=>L.push(`${k}: ${v}`)); L.push(`TOTAL DE PLATĂ: ${O.grand} (TVA inclus)`);
  if(O.info)L.push("",O.info);
  L.push("","Oferta completă este atașată în format PDF.","","Cu stimă,",...B.sign);
  let b=L.join("\n");
  if(b.length>1700){ // limita practică a link-urilor mailto
    const short=[L[0],"",L[2],"",`TOTAL DE PLATĂ: ${O.grand} (TVA inclus)`,"","Oferta completă (toate produsele) este atașată în format PDF.","","Cu stimă,",...B.sign];
    b=short.join("\n");
  }
  return b;
}
function pdfName(){return fileBase()+".pdf"}
function saveWarn(){ if(!S.lines.length){toast("Adaugă cel puțin un produs în ofertă");return false} return true }
$("pdfBtn").onclick=()=>{ if(!saveWarn())return; download(makePDF(),pdfName()); toast("PDF descărcat: "+pdfName()) };
$("docBtn").onclick=()=>{ if(!saveWarn())return; const n=fileBase()+".docx"; download(makeDOCX(),n); toast("Word descărcat: "+n) };
$("mailBtn").onclick=()=>{
  const box=$("mailBox"), open=box.hidden; box.hidden=!open; $("mailBtn").setAttribute("aria-expanded",open);
  if(open){ $("mailTo").value=S.client.c_email||$("mailTo").value; $("mailSubj").value=`Ofertă ${B.name} nr. ${S.nr}`+(S.client.c_nume?` – ${S.client.c_nume}`:""); $("mailTo").focus() }
};
$("mailClose").onclick=()=>{$("mailBox").hidden=true;$("mailBtn").setAttribute("aria-expanded","false")};
try{ const probe=new File([new Blob(["x"],{type:"application/pdf"})],"t.pdf",{type:"application/pdf"}); if(navigator.canShare&&navigator.canShare({files:[probe]})) $("mailShare").hidden=false }catch(e){}
function mailPrep(){ if(!saveWarn())return null; download(makePDF(),pdfName()); return {to:$("mailTo").value.trim(),su:$("mailSubj").value.trim(),body:mailBody()} }
$("mailDefault").onclick=()=>{ const m=mailPrep(); if(!m)return;
  setTimeout(()=>{ location.href=`mailto:${encodeURIComponent(m.to).replace(/%40/g,"@")}?subject=${encodeURIComponent(m.su)}&body=${encodeURIComponent(m.body)}` },400);
  toast("PDF descărcat. Atașează-l în e-mailul care se deschide.") };
$("mailGmail").onclick=()=>{ const m=mailPrep(); if(!m)return;
  window.open(`https://mail.google.com/mail/?view=cm&fs=1&to=${encodeURIComponent(m.to)}&su=${encodeURIComponent(m.su)}&body=${encodeURIComponent(m.body)}`,"_blank");
  toast("PDF descărcat. Atașează-l în fereastra Gmail.") };
$("mailShare").onclick=async()=>{ if(!saveWarn())return;
  const f=new File([makePDF()],pdfName(),{type:"application/pdf"});
  try{ await navigator.share({files:[f],title:$("mailSubj").value,text:mailBody()}) }catch(e){ if(e.name!=="AbortError") toast("Partajarea nu a mers; folosește Outlook / Mail") } };
