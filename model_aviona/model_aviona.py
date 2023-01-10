from izuzeci import izuzeci
from csv import DictReader, DictWriter

sifra_modela = 0 

def ispis_modela_aviona(model_aviona: dict):
    print(f"{model_aviona['id']:<10}{model_aviona['naziv']:<30}{model_aviona['broj_redova']:<30}")

"""
Funkcija kreira novi rečnik za model aviona i dodaje ga u rečnik svih modela aviona.
Kao rezultat vraća rečnik svih modela aviona sa novim modelom.
"""
def kreiranje_modela_aviona(
    svi_modeli_aviona: dict,
    naziv: str ="",
    broj_redova: int = 0,
    pozicija_sedista: list = []
) -> dict:
    global sifra_modela
    if not naziv or not broj_redova or not pozicija_sedista:
        raise izuzeci.NepostojeciPodaci("Greška - Obavezni podaci nisu pravilno uneti!")
    svi_modeli_aviona.update(
    {
        sifra_modela:
        {
            'id': sifra_modela,
            'naziv': naziv,
            'broj_redova': broj_redova,
            'pozicije_sedista': pozicija_sedista
        }
    })
    sifra_modela += 1
    return svi_modeli_aviona

"""
Funkcija čuva sve modele aviona u fajl na zadatoj putanji sa zadatim operatorom.
"""
def sacuvaj_modele_aviona(putanja: str, separator: str, svi_aerodromi: dict):
    with open(putanja, 'w', newline='') as f:
        csv_pisac = DictWriter(f, ['id', 'naziv', 'broj_redova', 'pozicije_sedista'], delimiter = separator)
        for aerodrom in svi_aerodromi:
            csv_pisac.writerow({
                'id': svi_aerodromi[aerodrom]['id'],
                'naziv': svi_aerodromi[aerodrom]['naziv'],
                'broj_redova': int(svi_aerodromi[aerodrom]['broj_redova']),
                'pozicije_sedista': ",".join(str(pozicija) for pozicija in svi_aerodromi[aerodrom]['pozicije_sedista'])
            })

"""
Funkcija učitava sve modele aviona iz fajla na zadatoj putanji sa zadatim operatorom.
"""
def ucitaj_modele_aviona(putanja: str, separator: str) -> dict:
    svi_aerodromi = dict()
    with open(putanja) as f:
        csv_citac = DictReader(f, ['id', 'naziv', 'broj_redova', 'pozicije_sedista'], delimiter = separator)
        for aerodrom in csv_citac:
            svi_aerodromi.update({
                int(aerodrom['id']):
                    {
                        'id': int(aerodrom['id']),
                        'naziv': aerodrom['naziv'],
                        'broj_redova': int(aerodrom['broj_redova']),
                        'pozicije_sedista': [str(pozicija) for pozicija in aerodrom['pozicije_sedista'].split(",")]
                    }
                }
            )
    return svi_aerodromi