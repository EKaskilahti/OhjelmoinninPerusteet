# Copyright (c) 2025 Elina Kaskilahti
# License: MIT

from datetime import datetime
from typing import List, Dict
import csv
from collections import defaultdict

FI_WEEKDAYS = ['maanantai', 'tiistai', 'keskiviikko', 'torstai', 'perjantai', 'lauantai', 'sunnuntai']

def muunna_aika(aika_str: str) -> datetime:
    """Muuntaa ISO-muotoisen aikaleiman datetime-olioksi."""
    return datetime.fromisoformat(aika_str)

def lue_data(tiedoston_nimi: str) -> List[Dict]:
    """Lukee CSV-tiedoston ja palauttaa listan sanakirjoja (Wh-yksiköissä)."""
    data = []
    with open(tiedoston_nimi, encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            rivi = {'Aika': muunna_aika(row['Aika'])}
            for key in row.keys():
                if key != 'Aika':
                    val = row[key].strip()
                    rivi[key] = int(val) if val else 0
            data.append(rivi)
    return data

def muunna_kwh(data: List[Dict]) -> None:
    """Muuntaa Wh-arvot kWh-arvoiksi (in-place)."""
    for rivi in data:
        for key in rivi.keys():
            if key != 'Aika':
                rivi[key] = rivi[key] / 1000.0

def laske_yhteenveto(data: List[Dict]) -> Dict[str, Dict]:
    """Laskee päiväkohtaiset summat kulutuksesta ja tuotannosta vaiheittain."""
    yhteenveto = defaultdict(lambda: {
        'date': '',
        'Kulutus vaihe 1 Wh': 0.0,
        'Kulutus vaihe 2 Wh': 0.0,
        'Kulutus vaihe 3 Wh': 0.0,
        'Tuotanto vaihe 1 Wh': 0.0,
        'Tuotanto vaihe 2 Wh': 0.0,
        'Tuotanto vaihe 3 Wh': 0.0
    })
    for rivi in data:
        wk_name = FI_WEEKDAYS[rivi['Aika'].weekday()]
        date_str = f"{rivi['Aika'].day:02d}.{rivi['Aika'].month:02d}.{rivi['Aika'].year}"
        if not yhteenveto[wk_name]['date']:
            yhteenveto[wk_name]['date'] = date_str
        for key in yhteenveto[wk_name].keys():
            if key != 'date':
                yhteenveto[wk_name][key] += rivi[key]
    for wk_name in yhteenveto:
        for key in yhteenveto[wk_name]:
            if key != 'date':
                yhteenveto[wk_name][key] = round(yhteenveto[wk_name][key], 2)
    return yhteenveto

def muotoile_luku(arvo: float) -> str:
    """Muotoilee luvun kahteen desimaaliin ja vaihtaa pisteen pilkuksi."""
    return f"{arvo:.2f}".replace(".", ",")

def pienin_nettokulutus_paiva(yhteenveto: Dict[str, Dict]) -> str:
    """Palauttaa viikonpäivän, jolla nettokulutus (kulutus - tuotanto) on pienin."""
    pienin_paiva = None
    pienin_arvo = None
    for wk_name, row in yhteenveto.items():
        kulutus = row['Kulutus vaihe 1 Wh'] + row['Kulutus vaihe 2 Wh'] + row['Kulutus vaihe 3 Wh']
        tuotanto = row['Tuotanto vaihe 1 Wh'] + row['Tuotanto vaihe 2 Wh'] + row['Tuotanto vaihe 3 Wh']
        netto = kulutus - tuotanto
        if pienin_arvo is None or netto < pienin_arvo:
            pienin_arvo = netto
            pienin_paiva = wk_name
    return pienin_paiva

def muodosta_viikkoraportti(viikko_label: str, yhteenveto: Dict[str, Dict]) -> str:
    """Muodostaa viikkoraportin selkeänä tekstinä."""
    korosta = pienin_nettokulutus_paiva(yhteenveto)
    lines = [
        f"{viikko_label} sähkönkulutus ja -tuotanto (kWh, vaiheittain)",
        "",
        "Päivä         Pvm         Kulutus [kWh]                 Tuotanto [kWh]",
        "             (pv.kk.vvvv)  v1      v2      v3            v1     v2     v3",
        "---------------------------------------------------------------------------"
    ]
    for wk_name in FI_WEEKDAYS:
        if wk_name in yhteenveto:
            row = yhteenveto[wk_name]
            merkki = "*" if wk_name == korosta else " "
            lines.append(
                f"{merkki}{wk_name:<11} {row['date']}   "
                f"{muotoile_luku(row['Kulutus vaihe 1 Wh']):>6}  "
                f"{muotoile_luku(row['Kulutus vaihe 2 Wh']):>6}  "
                f"{muotoile_luku(row['Kulutus vaihe 3 Wh']):>6}    "
                f"{muotoile_luku(row['Tuotanto vaihe 1 Wh']):>6}  "
                f"{muotoile_luku(row['Tuotanto vaihe 2 Wh']):>6}  "
                f"{muotoile_luku(row['Tuotanto vaihe 3 Wh']):>6}"
            )
    lines.append("")
    return "\n".join(lines)

def tallenna_raportti(tiedoston_nimi: str, sisältö: str) -> None:
    """Kirjoittaa raportin tiedostoon with-rakenteella."""
    with open(tiedoston_nimi, "w", encoding="utf-8") as f:
        f.write(sisältö)

def main() -> None:
    """Lukee viikot, laskee yhteenvedot ja tallentaa raportin tiedostoon."""
    raportti_osat = []
    for viikko, tiedosto in [("Viikko 41", "viikko41.csv"), ("Viikko 42", "viikko42.csv"), ("Viikko 43", "viikko43.csv")]:
        data = lue_data(tiedosto)
        muunna_kwh(data)
        yhteenveto = laske_yhteenveto(data)
        raportti_osat.append(muodosta_viikkoraportti(viikko, yhteenveto))
    koko_raportti = "\n".join(raportti_osat)
    tallenna_raportti("yhteenveto.txt", koko_raportti)
    print("Raportti tallennettu tiedostoon yhteenveto.txt")

if __name__ == "__main__":
    main()
