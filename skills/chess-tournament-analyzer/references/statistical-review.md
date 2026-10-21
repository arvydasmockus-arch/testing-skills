# ISC statistinės peržiūros darbiniai kriterijai

Šie kriterijai atspindi savininko siūlomą / darbinę procedūrą, **nepatvirtina**, kad tai galiojančios oficialios ISC/WFCC taisyklės. Prieš oficialų pritaikymą patikrink aktualią taisyklių redakciją ir teisinį / procedūrinį statusą.

## Atrankos kriterijai
- Z >= 3,0: preliminari papildoma patikra (tik tada, kai Z patikimai kalibruotas).
- Z >= 3,5: stiprus statistinis signalas.
- Pasirodymo ir išankstinio reitingo skirtumas (Δ) >= 450 Elo: papildomas signalas; nurodyk, kaip nustatytas pasirodymo reitingas.
- Galutinė vieta <= 20.
- Palyginamosios grupės dalyvių skaičius >= 14.

Atrankos į griežtesnę peržiūrą **darbinė kombinacija**: Z >= 3,5, Δ >= 450 Elo, vieta <= 20 ir grupė N >= 14; aiškiai parodyk, kurie kriterijai tenkinami. Nepriskirk mažo N tariamam patikimumui. Atskirai galima pažymėti vien Z >= 3,0 kaip preliminarų signalą, tačiau nereiškia patvirtintos anomalijos.

## Skaičiavimo ir jautrumo principai
1. Tiksliai aprašyk reitingą: oficialus, iki renginio galiojęs, jo data, ar preliminarus.
2. Naudok tik vienodai apibrėžtas imtis ir tikėtiną pasirodymą. Jei reitingui trūksta istorijos, neimituok patikimo Z.
3. Z matuoja nuokrypį nuo modelio, o ne įrodytą nesąžiningumą. Didelis Z savaime nėra priežastis atmesti rezultatą.
4. Išbandyk alternatyvias pradinio reitingo prielaidas, pvz., 1700 ir 2000 Elo, jei tam yra pagrindas, ir parodyk, kaip keičiasi Z / Δ; neskaičiuok fiktyvių verčių.
5. Atskirai nagrinėk sprendimo lapus, variantų pilnumą, priežiūrą, uždavinių prieinamumą, rezultatų taisymus ir teisėjų atsakymus.
6. Galutinį procedūrinį sprendimą priima atitinkamas įgaliotas asmuo pagal tuo metu galiojančias taisykles; šis įgūdis parengia analitinę medžiagą.

## Minimalios audito lentelės antraštės
event_id,category,venue,solver,prior_rating,rating_date,score,max_score,rank,group_n,expected_performance,observed_performance,prediction_sd,z,delta_elo,precheck_z3,flag_z35,flag_delta450,flag_top20,flag_n14,review_status,source,notes

Jei duomens nėra, palik tuščią ir paaiškink, o ne pakeisk jį nuliu.
