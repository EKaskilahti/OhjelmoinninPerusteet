from datetime import datetime


def hae_varausnumero(varaus):
    varausnumero = varaus[0]
    print(f"Varausnumero: {varausnumero}")

def hae_varaaja(varaus):
    nimi = varaus[1]
    print(f"Varaaja: {nimi}")

def hae_paiva(varaus):
    paiva_str = varaus[2]
    paiva = datetime.strptime(paiva_str, "%Y-%m-%d").strftime("%d.%m.%Y")
    print(f"Päivämäärä: {paiva}")

def hae_aloitusaika(varaus):
    aloitusaika = varaus[3]
    print(f"Aloitusaika: {aloitusaika}")

def hae_tuntimaara(varaus):
    tuntimäärä = varaus[4]
    print(f"Tuntimäärä: {tuntimäärä}")

def hae_tuntihinta(varaus):
    tuntihinta = float(varaus[5])
    print(f"Tuntihinta: {tuntihinta:.2f}€")

def hae_maksettu(varaus):
    maksettu = varaus[6]
    if maksettu.lower() == "true":
        print("Maksettu: Kyllä")
    else:
        print("Maksettu: Ei")

def hae_kohde(varaus):
    kohde = varaus[7]
    print(f"Kohde: {kohde}")

def hae_puhelin(varaus):
    puhelin = varaus[8]
    print(f"Puhelin: {puhelin}")

def hae_sahkoposti(varaus):
    sahkoposti = varaus[9]
    print(f"Sähköposti: {sahkoposti}")

def laske_kokonaishinta(varaus):
    tuntimaara = float(varaus[4])
    tuntihinta = float(varaus[5])
    kokonaishinta = tuntimaara * tuntihinta
    print(f"Kokonaishinta: {kokonaishinta:.2f}€")


def main():
    # Maaritellaan tiedoston nimi suoraan koodissa
    varaukset = "varaukset.txt"

    # Avataan tiedosto, luetaan ja splitataan sisalto
    with open(varaukset, "r", encoding="utf-8") as f:
        varaus = f.read().strip()
        varaus = varaus.split('|')

    hae_varausnumero(varaus)
    hae_varaaja(varaus)
    hae_paiva(varaus)
    hae_aloitusaika(varaus)
    hae_tuntimaara(varaus)
    hae_tuntihinta(varaus)
    laske_kokonaishinta(varaus)
    hae_maksettu(varaus)
    hae_kohde(varaus)
    hae_puhelin(varaus)
    hae_sahkoposti(varaus)


if __name__ == "__main__":
    main()