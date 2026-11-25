# Etichete pe un rand (67x10 mm) pentru o selectie de coduri ADRo, varianta 2000 mm.
# Sursa: all2.tsv extras din nmcromania.ro/adro?page=N (trackProductClick).
import re, sys
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
CODES="na102 na103 na231 na106 na107 na118 na213 na236 na210 na212 na214 na121 rema16 na229 na230 na104 na210 na108 ns162 ns111 ns109 ns166 ns116 ns108 ns112 ns110 ns118 refa12 nc101 na105 nc174 nc103 nc160 nc111 nc104 nc173".upper().split()
tsv=sys.argv[1]; out=sys.argv[2]
dims={}
for l in open(tsv):
    pid,brand,cat,name=l.rstrip('\n').split('\t')
    if not any(k in cat for k in ('Ancadramente','Solbanc','Cornisa')): continue
    m=re.search(r'\b([A-Z]+\d+)\s+(\d+)[xX](\d+)[xX](2000)\s*$',name.strip())
    if m: dims[m.group(1)]=f"{m.group(2)}X{m.group(3)}X2000"
items=[]; missing=[]
for c in dict.fromkeys(CODES):
    (items.append((c,dims[c])) if c in dims else missing.append(c))
print(len(items),'etichete; lipsa pe site:',missing)
pdfmetrics.registerFont(TTFont('R','/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'))
pdfmetrics.registerFont(TTFont('B','/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'))
W,H=A4; LW,LH=67*mm,10*mm; COLS=3
ROWS=-(-len(items)//COLS)
mx=(W-COLS*LW)/2; my=(H-ROWS*LH)/2
def width(fs,c,d): return pdfmetrics.stringWidth(c+' ','B',fs)+pdfmetrics.stringWidth(d+' mm','R',fs)
FS=16
while max(width(FS,c,d) for c,d in items)>LW-5*mm or FS*0.72>LH-4*mm: FS-=0.25
print('font',FS)
cv=canvas.Canvas(out,pagesize=A4); cv.setTitle('Etichete ADRo selectie')
for i,(c,d) in enumerate(items):
    col=i%COLS; row=i//COLS
    x=mx+col*LW; y=H-my-(row+1)*LH
    cv.setStrokeColorRGB(.75,.75,.75); cv.setLineWidth(.3); cv.setDash(2,2); cv.rect(x,y,LW,LH); cv.setDash()
    cv.setFillColorRGB(0,0,0)
    tx=x+(LW-width(FS,c,d))/2; ty=y+(LH-FS*0.72)/2
    cv.setFont('B',FS); cv.drawString(tx,ty,c+' ')
    cv.setFont('R',FS); cv.drawString(tx+pdfmetrics.stringWidth(c+' ','B',FS),ty,d+' mm')
cv.save()
