from izuzeci import izuzeci
from csv import DictReader, DictWriter

"""
Funkcija kreira rečnik za novi aerodrom i dodaje ga u rečnik svih aerodroma.
Kao rezultat vraća rečnik svih aerodroma sa novim aerodromom.
"""
def kreiranje_aerodroma(
    svi_aerodromi: dict,
    skracenica: str ="",
    pun_naziv: str ="",
    grad: str ="",
    drzava: str =""
) -> dict:
    if not skracenica or not pun_naziv or not grad or not drzava:
        raise izuzeci.NepostojeciPodaci("Greška - Obavezni podaci nisu pravilno uneti!")
    svi_aerodromi.update(
    {
        skracenica:
        {
            'skracenica': skracenica,
            'pun_naziv': pun_naziv,
            'grad': grad,
            'drzava': drzava
        }
    })

    return svi_aerodromi        
        
"""
Funkcija koja čuva aerodrome u fajl.
"""
def sacuvaj_aerodrome(putanja: str, separator: str, svi_aerodromi: dict):
     with open(putanja, 'w', newline='') as f:
        csv_pisac = DictWriter(f, ['skracenica', 'pun_naziv', 'grad', 'drzava'], delimiter = separator)
        for aerodrom in svi_aerodromi:
            csv_pisac.writerow(svi_aerodromi[aerodrom])

"""
Funkcija koja učitava aerodrome iz fajla.
"""
def ucitaj_aerodrom(putanja: str, separator: str) -> dict:
    svi_aerodromi = dict()
    with open(putanja) as f:
        csv_citac = DictReader(f, ['skracenica', 'pun_naziv', 'grad', 'drzava'], delimiter = separator)
        for aerodrom in csv_citac:
            svi_aerodromi.update({
                aerodrom['skracenica']:
                {
                    'skracenica': aerodrom['skracenica'],
                    'pun_naziv': aerodrom['pun_naziv'],
                    'grad': aerodrom['grad'],
                    'drzava': aerodrom['drzava']        
                }
            })
    return svi_aerodromi