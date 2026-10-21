---
name: chess-tournament-analyzer
description: Perskaito šachmatų kompozicijų sprendimo varžybų rezultatus (XLSX/CSV), atkuria Arvydo Mockaus Excel empirinį Δ=Rperf−Rinitial ir Z=(Δ−μΔ)/σΔ modelį, lygina su jautrumo analize, spalviniais žymėjimais, ISC atrankos kriterijais ir rengia audituojamą išvadų ataskaitą. Naudoti ISC, WCSC, ECSC, WCCC Open, ECSC Open bei nacionalinių varžybų statistinei peržiūrai.
---

# Chess Tournament Analyzer

## Paskirtis ir statusas
Tai **vartotojo „Analize ISC.xlsx“ (58 lapų) empirinio statistinės atrankos modelio** įgūdis, ne savarankiška kaltės nustatymo sistema ar oficialios WFCC procedūros patvirtinimas. Visada atskirk **istorinį Excel rezultatą**, **pataisytą / jautrumo rezultatą**, **kitus įrodymus** ir **įgalioto asmens procedūrinį sprendimą**.

Prieš analizuodamas:
1. Perskaityk \`references/workbook-model.md\` – tikslūs lapų tipai, stulpeliai, formulės ir spalvos.
2. Perskaityk \`references/statistical-review.md\` – interpretavimas, Z/Δ slenksčiai, ISC darbinė atranka.
3. Jei vartotojas pateikia Excel, naudok \`scripts/analyze.py\` su originaliu failu; rezultatus tikrink pagal originalias langelių formules ir cache.
4. Rengdamas galutinę ataskaitą vadovaukis \`references/report-template.md\`.

## Darbo tvarka

### 1. Pradinių rezultatų patikra
- Atpažink varžybų seriją, metus, datą, varžybų tipą (2 raundai / 6 raundai / Open), kategoriją, vietą ir grupę; atskirk ISC vietinį turnyrą nuo visos kategorijos.
- Perskaityk vietą, dalyvio vardą, federaciją, oficialų prieš turnyrą turėtą reitingą, pasirodymo reitingą, taškus, laiko duomenis, kai jie pateikti, ir uždavinių balus. Duomenis iš nuotraukų/PDF patikrink ne spėliodamas.
- Patikrink perskaičiavimus, balų sumas, skirtingus maksimumus, pasikartojimus, neišsamius įrašus, lietuviškus / europinius dešimtainius skirtukus ir išsaugotas Excel formulių rezultatų reikšmes.
- **Pasirodymo reitingas paprastai jau įrašytas šaltinyje.** Jo nespėliok iš taškų be oficialios reitingavimo formulės ir atitinkamų duomenų.
- Atskirai pažymėk trūkstamą pradinį reitingą, laiko duomenis, pirmą reitingą, naujus / nepilnamečius žaidėjus.

### 2. Atkurk originalų Excel metodą
Pagal šaltinį kiekvienam i apskaičiuok:
- \`Δ_i = Rperf_i − Rinitial_i\` (originaliuose Excel lapuose kartais neradus pradinio reitingo formulė įrašo **0**, ne realų skirtumą).
- \`μΔ = AVERAGE(Δ)\` per **tiksliame lape nurodytą diapazoną**.
- \`σΔ = STDEV.P(Δ)\`, naudok populiacijos SD (ne STDEV.S).
- \`Z_i = (Δ_i − μΔ) / σΔ\`.
- \`p_i = 1 − NORM.S.DIST(Z_i, TRUE)\` – vienpusės standartinio normaliojo skirstinio uodegos modelinis dydis.
- \`trials_i = 1 / p_i\`; nevadink jo patikimu realių turnyrų skaičiumi iki anomalijos.
- Išsaugok abiejų diapazonų ribas; **jų netaisyk nepastebimai**, jei Excel turi klaidą ar neatitikimą.

### 3. Lygiagreti jautrumo analizė
- Pakartok μΔ, σΔ ir Z **tik turintiems pradinį reitingą** (trūkstamas ≠ 0). Pateik abiejų variantų N, parametrus ir pasikeitusius atrankos lygius.
- Palygink originalų Excel cache su naujai apskaičiuotais rezultatais; pažymėk nesutampančias formules / istorines suvestines.
- Jei pagrįsta, atskirai analizuok alternatyvias pradinio reitingo prielaidas, pvz., 1700 ar 2000, bet **niekada neduok sugalvoto tikslumo**. Pakeitus vieno dalyvio reitingą parodyk, ar perskaičiuotas visas grupės μΔ ir σΔ.
- Maža imtis, labai nevienalytė grupė, išskirtys, trūkstami reitingai, priklausomi dalyviai ir daugybiniai testai riboja normaliojo skirstinio tikimybių interpretaciją.

### 4. Spalvinis žymėjimas ir įtartinų atvejų atranka
- Pritaikyk faktinę darbo knygos legendą ir conditional formatting iš \`references/workbook-model.md\`.
- Atskirai atvaizduok **Δ kategoriją**, **Z kategoriją**, **p kategoriją** ir **darbinės ISC peržiūros** keturių kriterijų atitiktį.
- Kriterijai pagal vartotojo projektą: preliminarus Z≥3; reikšmingas Z≥3,5; Δ≥450 Elo; vieta≤20; palyginama grupė N≥14. Griežta atranka: paskutiniai **keturi** vienu metu; nenurodyto grupės dydžio nelaikyk tenkinamu.
- Istoriniai Excel filtrai \`>300\` ar \`>400\` **nėra tas pats**, kas naujasis Δ≥450 slenkstis.
- Atmintinai neperrašinėk ar nenormalizuok rankinio suvestinio lapo, jeigu jis skiriasi nuo šaltinio metų lapo: prioritetas – patikrinta šaltinio formulė / naujas skaičiavimas su nurodyta versija.

### 5. Papildomi įrodymai ir kontekstas
- Jei pateikti originalūs sprendimo lapai, vertink sprendinių pilnumą, variantų / grėsmių nurodymą, laiko apribojimą, teisėjų pataisas, rezultato kilmę ir teisėjavimo sąlygas.
- Statistinis išskirtinumas nesuteikia pagrindo tvirtinti sukčiavimą ar diskvalifikuoti. Visada atskirk faktą, požymį, paaiškinimą, nepatikrintą teiginį ir siūlomą patikrą.
- Jei aktualu, peržiūrėk galiojančias oficialias ISC/WFCC taisykles atskirai nuo vartotojo siūlomų slenksčių.

### 6. Ataskaita
Pateik: (a) renginio identifikavimą, datą ir šaltinio statusą, (b) imtį ir trūkstamus reitingus, (c) tikslią Excel formulę, μΔ, σΔ ir palyginimo vienetus, (d) pažymėtus dalyvius su Δ/Z/p/1/p, (e) visų keturių atrankos požymių lentelę, (f) Excel-vs-rated-only palyginimą, (g) sprendimo lapų ir priežiūros kontekstą, (h) išvados kategoriją: „statistiškai įprastas“, „preliminari patikra“, „papildoma išsami peržiūra“ arba „nepakanka duomenų“.

Ataskaitos statusas **nėra oficialus sprendimas**. Pridėk formulių ir šaltinių atsekamumą (lapas, diapazonas, modelio variantas).

## Paleidimas

\`\`\`bash
python scripts/analyze.py "Analize ISC.xlsx" --sheet "ISC 2025" --output-dir reports
python scripts/analyze.py "Analize ISC.xlsx" --all --output-dir reports
python scripts/analyze.py results.csv --output-dir reports
python -m unittest discover -s evals -v
\`\`\`

CSV alternatyva: \`name,rank,prior_rating,performance_rating,country,location,category\`.
Rezultatas: kiekvieno lapo \`*-analysis.csv\` su dalyvių rodikliais ir \`*-summary.json\` su metodika bei įspėjimais. Skriptas skaito XLSX **išsaugotas reikšmes**, pats Excel formulių neperskaičiuoja; jei jos pasenusios, pirmiausia atnaujink darbaknygės skaičiavimą. Kiekvienos analizės pradžioje patikrink, ar visi įėjimo stulpeliai atpažinti.

Neperkelk viso vartotojo turnyrų duomenų failo į viešą GitHub repozitoriją be aiškaus leidimo. Kitų įgūdžių nekeisk.
