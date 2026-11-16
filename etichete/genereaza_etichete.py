import re, csv
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
rows=[l.rstrip('\n').split('\t') for l in open('all.tsv')]
order={'Ancadramente':0,'Solbanc':1,'Cornisa':2}
items=set()
for pid,brand,cat,name in rows:
    k=next((v for c,v in order.items() if c in cat),None)
    if k is None: continue
    m=re.search(r'\b([A-Z]+\d+)\s+(\d+)[xX](\d+)[xX](2000)\s*$',name.strip())
    if not m: continue
    items.add((k,m.group(1),f"{m.group(2)}X{m.group(3)}X2000"))
def nat(s): return [int(t) if t.isdigit() else t for t in re.split(r'(\d+)',s)]
items=sorted(items,key=lambda x:(x[0],nat(x[1])))
print(len(items))
with open('/home/user/dfhai/etichete/lista_etichete_adro_2000.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['categorie','cod','dimensiuni'])
    for k,c,d in items: w.writerow([['Ancadrament','Solbanc','Cornisa'][k],c,d])
# fonts
reg='/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'
bold='/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'
pdfmetrics.registerFont(TTFont('R',reg)); pdfmetrics.registerFont(TTFont('B',bold))
W,H=A4; LW,LH=65*mm,28*mm; COLS,ROWS=3,10
mx=(W-COLS*LW)/2; my=(H-ROWS*LH)/2
c=canvas.Canvas('/home/user/dfhai/etichete/etichete_adro_2000mm_A4.pdf',pagesize=A4)
c.setTitle('Etichete ADRo 2000 mm')
per=COLS*ROWS

def fit(texts,font,start,maxw):
    fs=start
    while max(pdfmetrics.stringWidth(t,font,fs) for t in texts)>maxw: fs-=0.25
    return fs
FS1=fit([a for _,a,_ in items],'B',27,LW-8*mm)
FS2=fit([b+' mm' for _,_,b in items],'R',FS1*0.56,LW-8*mm)
print('font',FS1,FS2)
for i,(k,code,dim) in enumerate(items):
    if i and i%per==0: c.showPage()
    j=i%per; col=j%COLS; row=j//COLS
    x=mx+col*LW; y=H-my-(row+1)*LH
    c.setStrokeColorRGB(.75,.75,.75); c.setLineWidth(.3); c.setDash(2,2)
    c.rect(x,y,LW,LH)
    c.setDash(); c.setFillColorRGB(0,0,0)
    cap1=FS1*0.72; cap2=FS2*0.72; gap=3.2*mm
    block=cap1+gap+cap2
    base2=y+(LH-block)/2
    base1=base2+cap2+gap
    c.setFont('B',FS1); c.drawCentredString(x+LW/2,base1,code)
    c.setFont('R',FS2); c.drawCentredString(x+LW/2,base2,dim+' mm')
c.save()
