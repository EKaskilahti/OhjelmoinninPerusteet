"""
Ohjelma joka lukee tiedostossa olevat varaustiedot
ja tulostaa ne konsoliin. Alla esimerkkitulostus:

Varausnumero: 123
Varaaja: Anna Virtanen
Päivämäärä: 2025-10-31
Aloitusaika: 10:00
Tuntimäärä: 2
Tuntihinta: 19.95 €
Kokonaishinta: 39.9 €
Maksettu: Kyllä
Kohde: Kokoustila A
Puhelin: 0401234567
Sähköposti: anna.virtanen@example.com

"""

def main():
    # Määritellään tiedoston nimi suoraan koodissa
    varaukset = "varaukset.txt"

    # Avataan tiedosto ja luetaan sisältö
    with open(varaukset, "r", encoding="utf-8") as f:
        varaus = f.read().strip()

    # Jaetaan tiedot osiin
    osat = varaus.split('|')
    
    from datetime import datetime

    # Tehdään muuttujat
    varausId = int(osat[0])
    varaaja = str(osat[1])
    paiva = datetime.strptime(osat[2], "%Y-%m-%d").date()
    aika = datetime.strptime(osat[3], "%H:%M").time()
    tuntimaara = int(osat[4])
    tuntihinta = float(osat[5])
    maksettu = bool(osat[6].strip() == "True")
    kohde = str(osat[7])
    puhelin = str(osat[8])
    sahkoposti = str(osat[9])

    # Lasketaan kokonaishinta
    kokonaishinta = tuntimaara * tuntihinta


    # Tulostetaan tiedot
    print("Varausnumero:", varausId)
    print("Varaaja:", varaaja)
    print("Päivämäärä:", paiva)
    print("Aloitusaika:", aika.strftime("%H:%M"))
    print("Tuntimäärä:", tuntimaara)
    print("Tuntihinta:", tuntihinta, "€")
    print("Kokonaishinta:", round(kokonaishinta, 2), "€")
    print(f"Maksettu: {'Kyllä' if maksettu else 'Ei'}")
    print("Kohde:", kohde)
    print("Puhelin:", puhelin)
    print("Sähköposti:", sahkoposti)


if __name__ == "__main__":
    main()