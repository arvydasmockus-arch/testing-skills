# Arvydo Mockaus ISC statistinės peržiūros darbinė metodika

## Modelio pagrindas
Pagal \`Analize ISC.xlsx\` 58 lapų analizę Δ yra pasirodymo ir pradinio reitingo skirtumas; Z – to skirtumo standartizacija **to paties turnyro viduje**, o ne iš anksto išoriniu modeliu prognozuoto rezultato Z.

\`delta = performance_rating - initial_rating\`
\`mean = AVERAGE(delta_range)\`
\`sd = STDEV.P(delta_range)\`
\`z = (delta - mean) / sd\`
\`p = 1 - NORM.S.DIST(z, TRUE)\`
\`one_in = 1 / p\`.

Šis p yra **modelinė, vienpusė** normaliojo skirstinio uodegos tikimybė; vien tik pagal empirinį Z nederėtų teigti, kad tikras įvykio šansas yra „vienas iš X“ arba kad tai įrodo neteisėtą pagalbą. Didžiausios atrankos reikšmės iš tos pačios imties, normalumo prielaida, reitingo ir grupės istorija bei daugybiniai palyginimai riboja interpretaciją.

## Nepriklausomi vizualiniai ir procedūriniai slenksčiai
**Istorinis Excel kodavimas**:
- Δ <200 – žalia; nuo 200 iki 300 – geltona; nuo 300 iki 400 – rožinė / raudona; >400 – ryškesnė violetinė.
- Z<2 – žalia; Z nuo 2 iki 3 – rožinė / raudona; Z>3 – violetinė; ribose Excel taisyklės gali persidengti.
- p<1 % – stiprus signalas; 1–2 % – papildomas žymėjimas; naujuose ISC lapuose formulė paprastai tikrinama ir Δ>0.
- Lapų vardų atrinkimo formulėse matyti skirtingi seni slenksčiai: ISC 2022 \`>300\`, ISC 2025/2026 \`>400\`. Tai nereiškia, kad Δ≥450 yra istorinis Excel filtravimo slenkstis.

**Tekstinė Excel legenda**:
- Maždaug 200 Elo – galima gera forma / talentas.
- 300+ Elo – reta, verta dėmesio.
- 400 / 450+ Elo – neįprasta, reikia konteksto.
- Z<2 – įprasta; Z nuo 2 iki 3 – padidėjęs nuokrypis; Z≥3 – anomalijos patikra; Z≥3,5 – aukšto prioriteto peržiūra.

**Atskira vartotojo siūloma griežta ISC patikra**:
1. Z≥3,5;
2. Δ≥450 Elo;
3. vieta≤20;
4. palyginamos grupės dydis N≥14.

Visi keturi kriterijai pažymimi atskirai; bendras stiprus peržiūros signalas tik kai jie **visi** patenkinti. Z≥3,0 galima išankstinė patikra, net kai griežtas derinys netenkinamas. Kai tai ISC, vietinio turnyro dydžio nesupainiok su bendra visos kategorijos imtimi. Nežinoma vieta / kategorija → „grupės N nepatikrintas“, ne automatinė atitiktis.

## Dvigubas skaičiavimas
1. **Excel-legacy**: išsaugok faktinį puslapio diapazoną, įskaitant trūkstamo reitingo atveju priskirtą Δ=0, jeigu taip elgiasi lapo formulė.
2. **Rated-only**: skaičiuok tik su įvestu reitingu; trūkstamas pradinis reitingas = NA, o ne 0.
3. Pateik modelių N, μ, σ, Z, atrankos klasės ir skirtumus. Paaiškink, ką reiškia jų neatitikimai.
4. Jei reitingo prielaida keičiama, parodyk ir fiksuotus μ/σ (tik iliustracijai), ir pilnai perskaičiuotus μ/σ (sprendimams labiau tinkama), jeigu įmanoma.
5. Jei paaiškėja Excel diapazono klaida, parodyk „Excel originalas“ ir „taisytas diapazonas“, o ne tyliai užtaisyk šaltinį.

## Priežiūra ir sprendimas
Pateiki tik analitinį signalą. Papildoma sprendimo lapų, teisėjų bei organizavimo aplinkybių patikra yra atskira. Kiekvieną procedūrinę išvadą pagrįsk tuo metu galiojančia WFCC/ISC taisyklių redakcija; šiame dokumente įrašyti kriterijai yra vartotojo darbinis projektas, ne oficialiai įsigaliojusi taisyklė.
