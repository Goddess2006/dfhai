# Pagina Contact — decoflair.ro/contact

Pagina Contact nu este o pagină de informații: este compusă din 4 locuri din admin. Mai jos, exact ce se pune în fiecare. Textul din blocurile de cod se copiază ca atare.

---

## 1. Blocurile de sus (Journal → Modules → Info Blocks → „Page / Contact / Vertical”, ID 194)

### Blocul 1 — Date firmă

**Title:**
```
DECO & FLAIR HUB S.R.L.
```

**Text** (în editor, modul cod sursă `</>`):
```html
Sediu social: Str. Renului nr. 3, Sector 2, București<br>
Depozit și punct de ridicare: Str. Comerțului f.n., Domnești, jud. Ilfov, 077040<br>
Nr. Reg. Com.: J2026031505008<br>
CIF: RO54681700<br>
Capital social: 500 lei<br>
IBAN: RO95 INGB 0000 9999 1984 0357<br>
Banca: ING Bank
```

### Blocul 2 — E-mail (neschimbat)

**Title:** `Adresa de email` → recomandat: `E-mail`
**Text:** `office@decoflair.ro` · Link: `mailto:office@decoflair.ro`

### Blocul 3 — Telefon

**Title:**
```
Telefon și consultanță
```
**Text:**
```
0765 740 280
```
**Link:**
```
tel:+40765740280
```
(Acum linkul este `tel:0723.300.603`; punctele din număr pot face apelul să nu funcționeze pe unele telefoane.)

### Blocul 4 — Program

**Title:** `Program de lucru`
**Text:**
```html
Luni – Vineri: 07:30 – 16:00<br>
Sâmbătă, duminică și sărbători legale: închis
```

---

## 2. Formularul (Journal → Modules → Form → „Formular contact - Contact”, ID 20)

**Titlu formular:**
```
Aveți o întrebare? Scrieți-ne și vă răspundem în cel mai scurt timp.
```

**Etichete câmpuri:** `Nume` · `E-mail` · `Telefon` · `Mesajul dumneavoastră`
**Placeholder mesaj:** `Spuneți-ne cu ce vă putem ajuta (produs, dimensiuni, cantitate, localitate de livrare)`
**Eticheta captcha:** `Confirmați că nu sunteți robot`

Bifa de acord: legătura către Politica de confidențialitate este corectă (information_id=3). Recomandat ca textul bifei să fie:
```
Am citit Politica de confidențialitate și sunt de acord cu prelucrarea datelor pentru a primi un răspuns.
```

---

## 3. Setările magazinului (System → Settings → Edit store → tab „Store”)

Secțiunea „Locația noastră” este ascunsă de temă pe pagina Contact, dar aceste câmpuri apar în e-mailurile de comandă, în facturi/proforme, în datele structurate pentru Google și în alte module. De aceea trebuie actualizate.

| Câmp | Valoare |
|---|---|
| Store Name | `DECO & FLAIR HUB S.R.L.` |
| Store Owner | `DECO & FLAIR HUB S.R.L.` |
| Address | `Str. Renului nr. 3, Sector 2, București` *(sediul social)* |
| Geocode | lăsat gol sau coordonatele depozitului, dacă vreți hartă către depozit |
| E-Mail | `office@decoflair.ro` |
| Telephone | `0765 740 280` |
| Fax | **gol** (acum conține 0765740280; după golire, rândul „Fax” dispare de pe pagină) |
| Opening Times | `Luni – Vineri: 07:30 – 16:00` |
| Comment | gol |

> Dacă vreți ca în „Locația noastră” să apară depozitul (unde vin clienții), nu sediul, puneți la Address `Str. Comerțului f.n., Domnești, jud. Ilfov, 077040` și lăsați sediul social în Blocul 1. Recomandarea mea: depozitul, pentru că acolo se ridică marfa.

---

## 4. Locații (System → Localisation → Store Locations → „Punct ridicare”)

| Câmp | Valoare |
|---|---|
| Store Name | `Depozit și punct de ridicare Deco & Flair` |
| Address | `Str. Comerțului f.n., Domnești, jud. Ilfov, 077040` |
| Telephone | `0765 740 280` |
| Fax | gol |
| Opening Times | `Luni – Vineri: 07:30 – 16:00` |

---

## 5. Alte locuri cu datele vechi (Făurei nr. 1 / 0723 300 603)

- Subsolul site-ului (Journal → Footer) — dacă afișează adresă sau telefon.
- Șabloanele de e-mail ale comenzilor și antetul proformei/facturii.
- Profilul Google Business, Facebook/Instagram, semnăturile de e-mail.

După salvare: Journal → System → Clear cache.
