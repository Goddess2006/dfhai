
(function(){
// Cornice profile: (a = distance out from wall, b = distance down from ceiling)
const P=[[0,13],[1.1,13],[1.1,12],[1.8,11.6]];
for(let i=1;i<=14;i++){const t=i/14;const s=t*t*(3-2*t);const w=Math.sin(t*Math.PI)*1.6;
  P.push([1.8+s*6.4 - w*0.6, 11.6-t*9.0 + w*0.9]);}
P.push([8.2,2.6],[9.2,2.6],[9.2,1.4],[10.2,1.4],[10.2,0]);
// room
const W=165,H=75,D=330,ZN=40,f=190,cx=150,cy=128;
const pr=(x,y,z)=>[cx+f*x/z, cy-f*y/z];
const pts=a=>a.map(p=>pr(...p).map(v=>v.toFixed(2)).join(',')).join(' ');
const L=[-0.35,-0.55,-0.75];{const n=Math.hypot(...L);L.forEach((v,i)=>L[i]=v/n);}
function shade(n){const d=Math.max(0,n[0]*L[0]+n[1]*L[1]+n[2]*L[2]);const k=0.64+0.38*d;
  return `rgb(${Math.min(255,Math.round(252*k))},${Math.min(255,Math.round(249*k))},${Math.min(255,Math.round(242*k))})`;}
const S=2.9; // scale cornice
let g='';
g+=`<defs>
<linearGradient id="wb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e9dcc8"/><stop offset="1" stop-color="#cdb796"/></linearGradient>
<linearGradient id="wl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#cdb898"/><stop offset="1" stop-color="#e2d4bf"/></linearGradient>
<linearGradient id="wr" x1="1" y1="0" x2="0" y2="0"><stop offset="0" stop-color="#c2ab88"/><stop offset="1" stop-color="#dccbb2"/></linearGradient>
<linearGradient id="ce" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fbf8f2"/><stop offset="1" stop-color="#f1ebe1"/></linearGradient>
<radialGradient id="glow" cx="0.5" cy="0.15" r="0.6"><stop offset="0" stop-color="#fff6e0" stop-opacity=".9"/><stop offset="1" stop-color="#fff6e0" stop-opacity="0"/></radialGradient>
</defs>`;
const Y0=-200;
g+=`<polygon fill="url(#ce)" points="${pts([[-W,H,ZN],[W,H,ZN],[W,H,D],[-W,H,D]])}"/>`;
g+=`<polygon fill="url(#wb)" points="${pts([[-W,H,D],[W,H,D],[W,Y0,D],[-W,Y0,D]])}"/>`;
g+=`<polygon fill="url(#wl)" points="${pts([[-W,H,ZN],[-W,H,D],[-W,Y0,D],[-W,Y0,ZN]])}"/>`;
g+=`<polygon fill="url(#wr)" points="${pts([[W,H,ZN],[W,H,D],[W,Y0,D],[W,Y0,ZN]])}"/>`;
// ceiling rose
const rc=[0,H,D*0.72];g+=(()=>{let s='';for(const [r,c] of [[34,'#f3ede3'],[26,'#fdfbf7'],[18,'#efe7da'],[11,'#fffdf9']]){
 const ring=[];for(let i=0;i<48;i++){const t=i/48*2*Math.PI;ring.push([rc[0]+r*Math.cos(t),H,rc[2]+r*Math.sin(t)]);}
 s+=`<polygon fill="${c}" stroke="#d8ccb8" stroke-width=".25" points="${pts(ring)}"/>`;}return s;})();
// pendant
const top=pr(0,H,D*0.72),bot=pr(0,H-30,D*0.72);
g+=`<line x1="${top[0]}" y1="${top[1]}" x2="${bot[0]}" y2="${bot[1]}" stroke="#8a7350" stroke-width=".5"/>`;
g+=`<circle cx="${bot[0]}" cy="${bot[1]+4}" r="22" fill="url(#glow)"/>`;
g+=`<path d="M${bot[0]-6} ${bot[1]+5} Q${bot[0]} ${bot[1]-3} ${bot[0]+6} ${bot[1]+5} Z" fill="#B8914F"/>`;
g+=`<ellipse cx="${bot[0]}" cy="${bot[1]+5}" rx="6" ry="1.2" fill="#fff3d6"/>`;
// cornice bands, three segments, mitered
for(let i=0;i<P.length-1;i++){
  const [a1,b1]=P[i].map(v=>v*S),[a2,b2]=P[i+1].map(v=>v*S);
  // profile tangent (da,db) -> normal pointing away from wall/ceiling corner: (db, -da) in (a,b) space flipped
  let na=(b1-b2), nb=(a2-a1); const nl=Math.hypot(na,nb)||1; na/=nl; nb/=nl; // na: out from wall, nb: down from ceiling
  const seg=[
    {q:[[-W+a1,H-b1,ZN],[-W+a1,H-b1,D-a1],[-W+a2,H-b2,D-a2],[-W+a2,H-b2,ZN]], n:[na,-nb,0]},
    {q:[[-W+a1,H-b1,D-a1],[W-a1,H-b1,D-a1],[W-a2,H-b2,D-a2],[-W+a2,H-b2,D-a2]], n:[0,-nb,-na]},
    {q:[[W-a1,H-b1,D-a1],[W-a1,H-b1,ZN],[W-a2,H-b2,ZN],[W-a2,H-b2,D-a2]], n:[-na,-nb,0]}];
  for(const s of seg){const c=shade(s.n);g+=`<polygon fill="${c}" stroke="${c}" stroke-width=".25" points="${pts(s.q)}"/>`;}
}
// soft shadow under cornice on back wall
const sb=P[0][1]*S;
g+=`<polygon fill="rgba(90,70,40,.10)" points="${pts([[-W,H-sb,D],[W,H-sb,D],[W,H-sb-7,D],[-W,H-sb-7,D]])}"/>`;
document.querySelectorAll('svg.room').forEach((s,i)=>{s.innerHTML=g.replace(/id="([^"]+)"/g,(_,id)=>`id="room${i}-${id}"`).replace(/url\(#([^\)]+)\)/g,(_,id)=>`url(#room${i}-${id})`);});

// clear cross-sections (a = out from wall, b = down from ceiling), all in 0..10 units
const PR=[
 (()=>{const r=[[0,10],[0.8,10],[0.8,9.2]];for(let i=0;i<=16;i++){const t=i/16*Math.PI/2;r.push([0.8+8.4*(1-Math.cos(t)),9.2-8.4*Math.sin(t)]);}r.push([10,0.8],[10,0]);return r;})(),
 P.map(([a,b])=>[a*10/10.2,b*10/13]),
 [[0,10],[1.5,10],[1.5,8],[3.5,8],[3.5,6],[5.5,6],[5.5,4],[7.5,4],[7.5,2],[10,2],[10,0]],
 [[0,10],[1,10],[1,9],[9,1],[10,1],[10,0]],
 (()=>{const r=[[0,10],[1.2,10],[1.2,9],[2,9],[2,8.2]];for(let i=1;i<=14;i++){const t=i/14*Math.PI/2;r.push([2+5.8*Math.sin(t),2+6.2*Math.cos(t)]);}r.push([9,2],[9,1],[10,1],[10,0]);return r;})()
];
document.querySelectorAll('svg.sec').forEach(sv=>{const pr=PR[+sv.dataset.p];const k=2.7,o=6;
 const X=a=>(34-a*k).toFixed(2),Y=b=>(o+b*k).toFixed(2);
 sv.innerHTML=`<path d="M3 ${o} H34 V37" fill="none" stroke="#c9b48c" stroke-width=".8"/>`+
 `<polygon points="34,${o} ${pr.map(([a,b])=>X(a)+','+Y(b)).join(' ')}" fill="#efe4cf" stroke="#2B2621" stroke-width=".7" stroke-linejoin="round"/>`;});
// profile cross-section icon
let d='M4 4 ';P.forEach(([a,b])=>{d+=`L${(4+a*3).toFixed(2)} ${(4+(13-b)*2.6+0).toFixed(2)} `;});
const pp=P.map(([a,b])=>`${(36-(b)*2.4).toFixed(2)},${(4+a*3.1).toFixed(2)}`);
const poly=`<path d="M4 4 H36 V36" fill="none" stroke="#B8914F" stroke-width="1"/>`+
 `<polygon points="36,4 ${P.map(([a,b])=>`${(36-a*3.1).toFixed(2)},${(4+b*2.4).toFixed(2)}`).join(' ')} 36,4" fill="#e9dcc2" stroke="#2B2621" stroke-width=".6" stroke-linejoin="round"/>`;
document.querySelectorAll('svg.profile').forEach(s=>s.innerHTML=poly);
})();
