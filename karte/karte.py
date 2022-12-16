from common import konstante
from functools import reduce
from datetime import datetime, timedelta
from izuzeci import izuzeci
from csv import DictReader, DictWriter

sledeci_broj_karte = 1


def validacija_karte(svi_konkretni_letovi: dict, sifra_konkretnog_leta: int, slobodna_mesta: list, kupac: dict, **kwargs):
    if sifra_konkretnog_leta not in svi_konkretni_letovi:
        raise izuzeci.NeispravnoUnetiPodaci(
            "Greška - Konkretan let ne postoji")
    if kupac['uloga'] == konstante.ULOGA_PRODAVAC:
        raise izuzeci.NedostatakDozvole("Greška - Prodavac ne može da kupi kartu")
    if kupac['uloga'] == konstante.ULOGA_ADMIN:
        raise izuzeci.NedostatakDozvole("Greška - Admin ne može da kupi kartu.")
    for kwarg in kwargs:
        if kwarg == "prodavac":
            if kwargs[kwarg]['uloga'] != konstante.ULOGA_PRODAVAC:
                raise izuzeci.NedostatakDozvole("Greška - Samo podavac može da proda kartu.")
    for mesta in slobodna_mesta:
        for sediste in mesta:
            if sediste.isalpha():
                return
    raise izuzeci.ZauzetoMesto("Greška - Sva mesta su zauzeta!")


"""
Funkcija vraća listu konkretnih letova koji će se dogoditi 120 minuta nakon sletanja na odredišni aerodrom
"""


def kupovina_sledece_karte(svi_letovi: dict, svi_konkretni_letovi: dict, konkretan_let: dict) -> list:
    letovi = list()

    vreme_sletanja: datetime = konkretan_let['datum_i_vreme_dolaska']
    vreme_sledeceg_leta: datetime = vreme_sletanja + timedelta(minutes=120)

    odredisni_aerodrom = svi_letovi[svi_konkretni_letovi[konkretan_let]
                                    ['broj_leta']]['sifra_odredisnog_aerodroma']

    for konkretan_let in svi_konkretni_letovi:
        datum_i_vreme = svi_konkretni_letovi[konkretan_let]['datum_i_vreme_polaska']
        aerodrom = svi_letovi[svi_konkretni_letovi[konkretan_let]
                              ]['sifra_odredisnog_aerodroma']
        if datum_i_vreme <= vreme_sledeceg_leta and datum_i_vreme >= vreme_sletanja and odredisni_aerodrom == aerodrom:
            letovi.append(svi_konkretni_letovi[konkretan_let])

    return letovi


"""
Kupovina karte proverava da li prosleđeni konkretni let postoji i da li ima slobodnih mesta. U tom slučaju se karta 
dodaje  u kolekciju svih karata. Slobodna mesta se prosleđuju posebno iako su deo konkretnog leta, zbog lakšeg 
testiranja. Baca grešku ako podaci nisu validni.
CHECKPOINT 2: kupuje se samo za ulogovanog korisnika i bez povezanih letova.
ODBRANA: moguće je dodati saputnike i odabrati povezane letove. 
"""


def kupovina_karte(
    sve_karte: dict,
    svi_konkretni_letovi: dict,
    sifra_konkretnog_leta: int,
    putnici: list,
    slobodna_mesta: list,
    kupac: dict,
    **kwargs  # prodavac, datum prodaje
) -> dict:
    global sledeci_broj_karte
    
    validacija_karte(svi_konkretni_letovi, sifra_konkretnog_leta, slobodna_mesta, kupac, **kwargs)
    sve_karte.update(
        {
            'broj_karte': sledeci_broj_karte,
            'sifra_konkretnog_leta': sifra_konkretnog_leta,
            'putnici': putnici,
            'kupac': kupac,
            'status': konstante.STATUS_NEREALIZOVANA_KARTA
        }
    )
    if kwargs != {}:
        for naziv, vrednost in kwargs.items():
            sve_karte[naziv] = vrednost
    sledeci_broj_karte += 1
    return sve_karte


def pretraga_karata(sve_karte: dict, svi_konkretni_letovi: dict, svi_letovi: dict, polaziste: str = "", odrediste: str = "", datum_polaska: datetime = None, 
                    datum_dolaska: datetime = None, putnik: list = None) -> list:
    filtrirano = list()
    for karta in sve_karte:
        konkretan_let = svi_konkretni_letovi[sve_karte['sifra_konkretnog_leta']]
        let = svi_letovi[konkretan_let['broj_leta']]
        if polaziste == let['sifra_polazisnog_aerodroma'] or polaziste == "":
            if odrediste == let['sifra_odredisnog_aerodorma'] or odrediste == "":
                if datum_polaska == konkretan_let['datum_i_vreme_polaska'] or datum_polaska == None:
                    if datum_dolaska == konkretan_let['datum_i_vreme_dolaska'] or datum_dolaska == None:
                        if putnik in sve_karte[karta]['putnici'] or putnik == None:
                            filtrirano.append(sve_karte[karta])
    return filtrirano

"""
Vraća sve nerealizovane karte za korisnika u listi.
"""


def pregled_nerealizovanaih_karata(korisnik: dict, sve_karte: dict) -> list:
    nerealizovane_karte = list()
    for karta in sve_karte:
        putnici = karta['putnici']
        if korisnik in putnici and karta.get('status') == konstante.STATUS_NEREALIZOVANA_KARTA:
            nerealizovane_karte.append(karta)
    return nerealizovane_karte


"""
 Funkcija brisanja karte se ponaša drugačije u zavisnosti od korisnika:
- Prodavac: karta se označava za brisanje
- Admin/menadžer: karta se trajno briše
Kao rezultat se vraća nova kolekcija svih karata. Baca grešku ako podaci nisu validni.
"""


def brisanje_karte(korisnik: dict, sve_karte: dict, broj_karte: int) -> dict:
    if korisnik['uloga'] == konstante.ULOGA_KORISNIK:
        raise izuzeci.NedostatakDozvole(
            "Greška - Korisnik ne može da briše karte!")
    elif korisnik['uloga'] == konstante.ULOGA_PRODAVAC:
        sve_karte[broj_karte]['obrisana'] = True
    elif korisnik['uloga'] == konstante.ULOGA_ADMIN:
        del sve_karte[broj_karte]
    else:
        raise Exception("Uloga ne postoji!")
    return sve_karte


"""
Funkcija koja čuva sve karte u fajl na zadatoj putanji.
"""


def sacuvaj_karte(sve_karte: dict, putanja: str, separator: str):
    with open(putanja, 'w', newline="") as f:
        csv_pisac = DictWriter(f, ['broj_karte', 'sifra_konkretnog_leta',
                                   'kupac', 'prodavac', 'sifra_sedista', 'datum_prodaje', 'obrisana'], delimiter=separator)
        for karta in sve_karte:
            csv_pisac.writerow(sve_karte[karta])


"""
Funkcija koja učitava sve karte iz fajla i vraća ih u rečniku.
"""


def ucitaj_karte_iz_fajla(putanja: str, separator: str) -> dict:
    with open(putanja) as f:
        karte = dict()
        csv_citac = DictReader(f, ['broj_karte', 'sifra_konkretnog_leta',
                                   'kupac', 'prodavac', 'sifra_sedista', 'datum_prodaje', 'obrisana'], delimiter=separator)
        for karta in csv_citac:
            karte.update({
                int(karta['broj_karte']):
                    {
                        'broj_karte': int(karta['broj_karte']),
                        'sifra_konkretnog_leta': int(karta['sifra_konkretnog_leta']),
                        'kupac': karta['kupac'],
                        'prodavac': karta['prodavac'],
                        'sifra_sedista': karta['sifra_sedista'],
                        'datum_prodaje': karta['datum_prodaje'],
                        'obrisana': karta['obrisana'] == 'True'
                }
            })
    return karte
