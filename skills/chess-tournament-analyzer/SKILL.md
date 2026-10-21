---
name: chess-tournament-analyzer
description: Analizuoja šachmatų kompozicijų sprendimo varžybų (įskaitant ISC) rezultatus, apskaičiuoja statistiką ir reitingu pagrįstą Z rodiklį, pažymi neįprastus pasirodymus ir rengia audituojamą ataskaitą pagal Arvydo Mockaus nustatytus peržiūros kriterijus. Naudoti gavus rezultatų lenteles ir, Z vertinimui, tinkamus istorinius arba modelio duomenis.
---

# Chess Tournament Analyzer

## Užduotis
Analizuok šachmatų kompozicijų sprendimo varžybas. Atskirk faktinius rezultatus, statistines anomalijas ir procedūrinius sprendimus. Nekaltink dalyvio nesąžiningumu vien iš statistikos.

## 1. Duomenų gavimas
- Priimk XLSX, CSV, PDF, HTML, nuotraukas ar lenteles; naudok prieinamus failų skaitymo įrankius. Niekada nespėliok neįskaitomų reikšmių.
- Išskirk renginį, datą, vietą, kategoriją, rangą, dalyvį, federaciją, pradinį reitingą (ir jo datą), turų ir uždavinių balus, galimą maksimumą, bendrą balų sumą, laiką, sprendimo lapus, vietinius teisėjus ir rezultato statusą (kai yra).
- Patikrink balų sudėtį, pasikartojimus, neatitikimus, trūkstamas reikšmes, skirtingas kategorijas ir maksimalių balų skirtumus. Neišvesk reitingo, jei jo nėra.
- Jei keli vietiniai ISC turnyrai: aiškiai nurodyk, kuri palyginamoji grupė naudota, ir ar taisyklės bei uždaviniai tikrai vienodi.

## 2. Aprašomoji statistika
- Kiekvienai palyginamai grupei pateik N, vidurkį, medianą, minimumą, maksimumą, standartinį nuokrypį (nurodant populiacijos ar imties apibrėžimą), kvartilius ir balų pasiskirstymą; prireikus procentą nuo maksimalių balų ir vietą.
- Dalyviui pateik balus, procentą nuo maksimumo, reitingą, vietą, nuokrypį nuo grupės vidurkio; reitingo pokytį pateik tik kai jis apskaičiuojamas pagal pagrįstą oficialią formulę ir turimus duomenis.
- Netapatink žalių balų Z rodiklio su reitingu pagrįstu rezultatų netikėtumo Z rodikliu.

## 3. Statistinis sąžiningumo vertinimas
- Prieš skaičiuodamas Z perskaityk `references/statistical-review.md`.
- PIRMINIS modelis: Z=(stebimas pasirodymas − tikėtinas pasirodymas)/modelio prognozės standartinis nuokrypis. Palyginamasis vienetas gali būti pasirodymo reitingas arba balai, bet tik jei tikėtina reikšmė ir dispersija pagrįstos tam pačiam vienetui; nemaišyk jų.
- Nepakanka turėti vien dalyvių reitingus ir galutinius balus patikimam Z. Modelio prognozę ir dispersiją reikia pagrįsti kalibraciniais istoriniais rezultatais, patikimu oficialiu modeliu arba aiškiai nurodyta vartotojo metodika. Jei jų nėra, rašyk „Z neapskaičiuojamas patikimai“ ir, tik kaip alternatyvą, pateik grupės balų standartizaciją kitu pavadinimu.
- Kartu pateik metodą, kontrolinę imtį, N, laikotarpį, panaudotus parametrus, šaltinius, trūkstamus duomenis, jautrumo analizę. Nekonstruok statistinio tikslumo iš prielaidų.
- Peržiūros atrankai naudok vartotojo darbo kriterijus iš nuorodos; jie **nėra automatinis kaltės, diskvalifikacijos ar oficialios WFCC sankcijos pagrindas**.

## 4. Papildoma ekspertinė patikra
Kai turimi sprendimo lapai, uždavinių tekstai, atsakymai ar vietinės varžybų aplinkybės, įvertink jų patikrinamumą: gynybų pilnumą, grėsmes, variantus, neįprastus praleidimus, vertinimo taisymus, laiką, lapų kilmę. Atskirai žymėk patvirtintą faktą, indikaciją ir nežinomybę. Neprimetinėk atsakymo iš sprendimų teisingumo be tikrinimo.

## 5. Ataskaita
Pateik lietuviškai (ar vartotojo prašyta kalba):
1. Renginio, šaltinių ir duomenų kokybės santrauką.
2. Dalyvių ir grupių statistiką.
3. Anomalijų suvestinę su modelio formule, įverčiais, slenksčiais ir priežastimis, kodėl pažymėta arba nepažymėta.
4. Alternatyvių prielaidų / jautrumo analizę.
5. Papildomų įrodymų ir procedūrinių neaiškumų sąrašą.
6. Aiškią išvadą: „nepažymėta“, „reikia papildomos peržiūros“, „rekomenduojama perduoti centriniam kontrolieriui“ arba „nepakanka duomenų“. Nenaudok statistikos kaip galutinio nuosprendžio.
7. Jei prašoma, pateik atskirą struktūruotą CSV/XLSX priedą su skaičiavimų audito stulpeliais.

## 6. Kokybės kontrolė
Perskaičiuok sumas ir ribinius atvejus; patikrink Z ženklą bei vienetus; pažymėk mažą N, atrankos šališkumą, nevienodas sąlygas, neaiškią reitingo istoriją ir daugybinių palyginimų riziką. Nedaryk išvadų iš nesamų duomenų. Neperrašyk kitų įgūdžių ar repo šaknies.
