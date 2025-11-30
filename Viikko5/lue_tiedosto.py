# Copyright (c) 2025 Elina Kaskilahti
# License: MIT

from datetime import datetime
from typing import List, Dict
import csv
from collections import defaultdict

FI_WEEKDAYS = ['maanantai', 'tiistai', 'keskiviikko', 'torstai', 'perjantai', 'lauantai', 'sunnuntai']

def muunna_aika(aika_str: str) -> datetime:
    return datetime.fromisoformat(aika_str)

def lue_data(viikko42: str) -> List[Dict]:
    data = []
    with open(viikko42, encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            rivi = {'Aika': muunna_aika(row['Aika'])}
            for key in row.keys():
                if key != 'Aika' and row[key] != '':
                    rivi[key] = int(row[key])
                elif key != 'Aika':
                    rivi[key] = 0  # jos puuttuva arvo, käsitellään nollana
            data.append(rivi)
    return data

#Muuntaa listan sanakirjojen arvot Wh-yksiköistä kWh-yksiköihin.
#Muutos tehdään suoraan listan sisällä.
def muunna_kwh(data: List[Dict]) -> None:
    for rivi in data:
        for key in list(rivi.keys()):
            if key != 'Aika':
                rivi[key] = rivi[key] / 1000.0


#Laskee päivittäiset summat kulutuksesta ja tuotannosta vaiheittain.
#Palauttaa sanakirjan, jossa avaimena on suomenkielinen viikonpäivä ja arvona summat.
def laske_yhteenveto(data: List[Dict]) -> Dict[str, Dict]:

    yhteenveto = defaultdict(lambda: {
        'date': '',
        'Kulutus vaihe 1 Wh': 0.0,
        'Kulutus vaihe 2 Wh': 0.0,
        'Kulutus vaihe 3 Wh': 0.0,
        'Tuotanto vaihe 1 Wh': 0.0,
        'Tuotanto vaihe 2 Wh': 0.0,
        'Tuotanto vaihe 3 Wh': 0.0
    })
    
    # Suomeksi: 0=maanantai, ..., 6=sunnuntai   
    for rivi in data: 
        viikko= FI_WEEKDAYS[rivi['Aika'].weekday()]
        date_str = f"{rivi['Aika'].day:02d}.{rivi['Aika'].month:02d}.{rivi['Aika'].year}"
        yhteenveto[viikko]['date'] = date_str

        for key in ('Kulutus vaihe 1 Wh', 'Kulutus vaihe 2 Wh', 'Kulutus vaihe 3 Wh',
                    'Tuotanto vaihe 1 Wh', 'Tuotanto vaihe 2 Wh', 'Tuotanto vaihe 3 Wh'):
            yhteenveto[viikko][key] += rivi.get(key, 0.0)

    # Pyöristä arvot kahteen desimaaliin
    for viikko in list(yhteenveto.keys()):
        for key in ('Kulutus vaihe 1 Wh', 'Kulutus vaihe 2 Wh', 'Kulutus vaihe 3 Wh',
                    'Tuotanto vaihe 1 Wh', 'Tuotanto vaihe 2 Wh', 'Tuotanto vaihe 3 Wh'):
            yhteenveto[viikko][key] = round(yhteenveto[viikko][key], 2)

    return yhteenveto

def muotoile_luku(arvo: float) -> str:
    return f"{arvo:.2f}".replace(".", ",")


#Tulostaa taulukkona: Päivä, päivämäärä, kulutus (vaiheittain) ja tuotanto (vaiheittain).
def tulosta_taulukko(yhteenveto: Dict[str, Dict]) -> None:
    print("\nViikon 42 sähkönkulutus ja -tuotanto (kWh, vaiheittain)\n")
    print("Päivä         Pvm         Kulutus [kWh]                 Tuotanto [kWh]")
    print("             (pv.kk.vvvv)  v1      v2      v3            v1       v2     v3")
    print("-------------------------------------------------------------------------------")

    for viikko in FI_WEEKDAYS:
        if viikko in yhteenveto:
            row = yhteenveto[viikko]
            print(
                f"{viikko:<12} {row['date']}   "
                f"{muotoile_luku(row['Kulutus vaihe 1 Wh']):>6}  "
                f"{muotoile_luku(row['Kulutus vaihe 2 Wh']):>6}  "
                f"{muotoile_luku(row['Kulutus vaihe 3 Wh']):>6}       "
                f"{muotoile_luku(row['Tuotanto vaihe 1 Wh']):>6}  "
                f"{muotoile_luku(row['Tuotanto vaihe 2 Wh']):>6}  "
                f"{muotoile_luku(row['Tuotanto vaihe 3 Wh']):>6}"
            )

#Pääohjelma,Lukee datan, muuntaa arvot, laskee yhteenvendon ja tulostaa taulukon.
def main() -> None:

    tiedosto = "viikko42.csv"
    data = lue_data(tiedosto)
    muunna_kwh(data)
    yhteenveto = laske_yhteenveto(data)
    tulosta_taulukko(yhteenveto)

if __name__ == "__main__":
    main()
