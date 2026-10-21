# „Analize ISC.xlsx“ rekonstrukcijos žinynas (2026-10-21)

## Inventorius: visi 58 lapai
- ISC 2017–2026: 10 lapų, dažniausiai 2 raundai, 240 min.
- Atskiri turnyrai (Ryga, Kaunas, Ukraina, Geelis, Vilnius, Sekocinas): 8 lapai.
- ECSC Open: 6 lapai (2016–2024 su pertraukomis).
- WCCC Open: 8 lapai (2016–2024 su pertraukomis).
- Šveicarija, Belgija, Lenkija: 3 lapai.
- WCSC: 8 lapai (2016–2024 be kiekvienų metų).
- ECSC: 15 lapų (2007–2024 su pertraukomis).

Skirtingos varžybų formos nėra viena palyginamoji imtis: ISC paprastai 2 raundai; WCSC/ECSC – 6; „Open“ – kitokie laiko ir uždavinių rinkiniai. Reitingo skirtumo Z kiekvieną kartą skaičiuojamas **atskiros lentelės / grupės kontekste**, ne iš bendros 58 lapų imties.

## Konkretūs langelių modeliai
- **ISC 2025/2026**: \`C\` vardas, \`E\` vieta, \`G\` pradinis reitingas, \`X\` taškai, \`Z\` pasirodymo reitingas; \`AC\` Δ, \`AF\` Z, \`AG5\` μ, \`AH5\` σ, \`AI\` p, \`AJ\` 1/p. Pavyzdys: ISC 2025 \`AC5=IF(G5<>"",Z5-G5,Z5-Z5)\`; \`AG5=AVERAGE(AC5:AC120)\`, \`AH5=STDEV.P(AC5:AC120)\`, \`AF5=(AC5-$AG$5)/$AH$5\`, \`AI5=1-NORM.S.DIST(AF5,TRUE)\`, \`AJ5=1/AI5\`.
- **ISC 2018–2024**: \`B\` vardas, \`E\` reitingas, \`X\` pasirodymo reitingas, \`AA\` Δ, \`AF\` Z, \`AG5\` μ, \`AH5\` σ, \`AI\` p, \`AJ\` 1/p. **ISC 2017** Z bei μ/σ/p stulpeliai paslinkti (\`AE/AF/AG/AH/AI\`).
- **ECSC Open / WCCC Open**: \`B\` vardas, \`E\` reitingas, \`X\` pasirodymo reitingas, \`AB\` Δ, \`AE\` Z, \`AF5\` μ, \`AG5\` σ, \`AH\` p, \`AI\` 1/p.
- **WCSC / ECSC**: \`B\` vardas, \`E\` reitingas, \`AH\` pasirodymo reitingas, \`AK\` Δ, \`AN\` Z, \`AO5\` μ, \`AP5\` σ, \`AQ\` p, \`AR\` 1/p.
- **Kiti turnyrai** – stulpelių poslinkiai skiriasi; atpažink \`Rank\`, \`Name\`, \`Rating\`, \`Perf. Rat.\`, \`Difference\`, \`Z-Score\`, \`μΔ\`, \`σΔ\`, \`Probability\`, \`Number of Trials\` iš 2 ir 4 eilučių antraščių; nemanyk, kad visi lapai vienodi.

Vietomis duomenys įrašyti su **kableliu** kaip dešimtainiu skirtuku (ypač ISC 2026), kitur su tašku. Tikrink, ar importuota kaip skaičius, ir neprarask tūkstantųjų / dešimtainių.

## Originalūs žymėjimai
Daugumoje lapų automatinė conditional formatting taisyklė:
- Δ < 200: žalias fonas; tarp 200 ir 300: geltonas; 300–400: rausvas; >400: violetinis.
- Z < 2: žalias; nuo 2 iki 3: rausvas; >3: violetinis.
- Tikimybė p<0,01: ryškesnis žymėjimas; p<0,02: silpnesnis žymėjimas, naujuose ISC tik jei Δ>0.
- Taisyklės \`between\` įtraukia ribas; ties 300 ir 3 sąlygos sutampa, todėl dvi spalvos gali konkuruoti pagal taisyklių prioritetą. Statistinių loginių slenksčių nereikia tapatinti su vien vizualiniais atspalviais.

Excel tekstinėse pastabose pabrėžiami Δ ≈200, ≥300 ir 400/450+, Z<2, 2–3, ≥3 ir ≥3,5. ISC 2025 bei ISC 2026 \`AD\` stulpelyje vardas automatiškai įrašomas, jei Δ>400. Ankstesniame ISC 2022 \`AB\` vardų atrankos slenkstis buvo >300. Taigi **istorinės legendos ir dabartinis siūlomas griežtas keturių kriterijų filtras skiriasi**.

## Rankinės palyginimų suvestinės
ISC 2025 lapo dešinėje yra papildomos rankinės istorinės suvestinės (\`AL20:AP29\`, \`AL43:AT79\`) su išskirtinių ankstesnių pasirodymų sąrašais, Z, p, Δ ir reitingais. Tai svarbi vartotojo darbo dalis – jis **lyginasi ne tik vieno turnyro viduje, bet ir su dešimtimis metų istorijos**.
- Tokias suvestines traktuok kaip hipotezių / precedento lenteles, **ne** automatiškai atsinaujinančią duomenų bazę.
- Viename senesniame ISC 2025 lapo rankiniame įraše 2026 m. aukščiausiam atvejui nurodytas Z≈4,246, bet pačiame ISC 2026 lape to atvejo išsaugotas Z≈5,087. Pateik atnaujintą šaltinio rodiklį ir nurodyk nesutapimą, ne pasirink patogesnį.
- Ataskaitoje naudok istorinės dažnumo analizės denominatorių (kiek turnyrų, kiek dalyvių / stebėjimų pagal laikotarpį) ir nuoseklų atrankos metodą.

## Užfiksuotos kokybės problemos (ne taisyti vartotojo XLSX be prašymo)
1. **WCSC 2024**: \`AO5=AVERAGE(AK5:AK56)\`, bet \`AP5=STDEV.P(AK5:AK86)\`. Tai skirtingos imtys: pakartok originalų rezultatą ir paraleliai parodyk vienodų diapazonų patikrą; jokio tylaus taisymo.
2. **ISC 2026**: \`AG5=AVERAGE(AC5:AC166)\` ir \`AH5=STDEV.P(AC5:AC166)\`, nors lapas tęsiasi iki 167 eilutės. Patikrink, ar paskutinė eilutė netyčia neįtraukta.
3. **ISC 2026**: langelyje \`A1\` tebėra senesnio „21st ISC 2025“ renginio pavadinimas; metams nustatyti naudok lapo pavadinimą ir patikimą varžybų metaduomenų šaltinį.
4. **Trūkstami reitingai**: dalyvio formulėse \`IF(E5="", X5-X5, X5-E5)\` ar analogiškai trūkstamo reitingo atveju gaunamas **nulinis Δ**, kuris patenka į \`AVERAGE\` ir \`STDEV.P\`. Pavyzdžiui, ISC 2025 yra 12 tokių dalyvių; skaičiuojant vien reitinguotus, pirmos eilutės Z keičiasi ~4,151 → ~3,934. Visada parodyk abu variantus ir imčių skirtumą.
5. **Tikimybių interpretacija**: \`1/p\` yra matematinė transformacija (Excel „Number of Trials“), bet ne įrodytas realaus sukčiavimo retumas; kalibracijai ir daugkartiniams palyginimams reikia atskiro tyrimo.

### Patikrinti orientyrai iš išsaugotų Excel reikšmių
- ISC 2025 eil. 5: Δ=890,97, μ≈−6,86707, σ≈216,28674, Z≈4,15114249, p≈0,000016541.
- ISC 2026 eil. 10: Δ≈1035,57, Z≈5,08675266.
- ISC 2024 eil. 5: Δ≈530,59, Z≈3,47284256.
- ISC 2022 eil. 6: Δ≈671,21, Z≈4,35052285.
- WCSC 2024 eil. 5: Δ≈100,72, μ≈35,58038, σ≈125,55364, Z≈0,518819.
Šie pavyzdžiai tėra skaitinė skaičiavimo kontrolė, **ne** išvada apie dalyvius.

## Skaitymo ir audito taisyklės
Nenaudok vien \`A1\` metų, nepasikliauk vien nudažytu langeliu ar rankiniu palyginimu. Išsaugok programoje lapo vardą, šaltinio eilutę, μ ir σ formulių diapazonus, Z metodo versiją, reitinguotų dalyvių N, trūkstamų reitingų skaičių, sąlygų atitiktį, šaltinių versiją. Darbaknygė nepakeista.
