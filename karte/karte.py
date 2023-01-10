from common import konstante
from functools import reduce
from datetime import datetime, timedelta, date
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
            if not sediste:
                return
    raise izuzeci.ZauzetoMesto("Greška - Sva mesta su zauzeta!")


"""
Funkcija vraća listu konkretnih letova koji će se dogoditi 120 minuta nakon sletanja na odredišni aerodrom
"""


def kupovina_sledece_karte(svi_letovi: dict, svi_konkretni_letovi: dict, konkretan_let: dict) -> list:
    letovi = list()

    vreme_sletanja: datetime = svi_konkretni_letovi[konkretan_let]['datum_i_vreme_dolaska']
    vreme_sledeceg_leta: datetime = vreme_sletanja + timedelta(minutes=120)

    odredisni_aerodrom = svi_letovi[svi_konkretni_letovi[konkretan_let]
                                    ['broj_leta']]['sifra_odredisnog_aerodorma']

    for konkretan_let in svi_konkretni_letovi:
        datum_i_vreme = svi_konkretni_letovi[konkretan_let]['datum_i_vreme_polaska']
        aerodrom = svi_letovi[svi_konkretni_letovi[konkretan_let]['broj_leta']]['sifra_polazisnog_aerodroma']
        if datum_i_vreme <= vreme_sledeceg_leta and datum_i_vreme >= vreme_sletanja and odredisni_aerodrom == aerodrom:
            letovi.append(svi_konkretni_letovi[konkretan_let])

    return letovi


"""
Kupovina karte proverava da li prosleđeni konkretni let postoji i da li ima slobodnih mesta. U tom slučaju se karta 
dodaje  u kolekciju svih karata. Slobodna mesta se prosleđuju posebno iako su deo konkretnog leta, zbog lakšeg 
testiranja. Baca grešku ako podaci nisu validni.
kwargs moze da prihvati prodavca kao recnik, i datum_prodaje kao datetime
recnik prodavac moze imati id i ulogu
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
    **kwargs
) -> (dict, dict):
    global sledeci_broj_karte
    
    karta = dict()
    validacija_karte(svi_konkretni_letovi, sifra_konkretnog_leta, slobodna_mesta, kupac, **kwargs)
    karta.update(
            {
                'broj_karte': sledeci_broj_karte,
                'sifra_konkretnog_leta': sifra_konkretnog_leta,
                'putnici': putnici,
                'obrisana': False,
                'kupac': kupac,
                'status': konstante.STATUS_NEREALIZOVANA_KARTA
            }
    )
    if kwargs != {}:
        for naziv, vrednost in kwargs.items():
            karta[naziv] = vrednost
    sve_karte[sledeci_broj_karte] = karta
    sledeci_broj_karte += 1
    
    return (karta, sve_karte)


def pretraga_karata(sve_karte: dict, svi_konkretni_letovi: dict, svi_letovi: dict, polaziste: str = "", odrediste: str = "", datum_polaska: datetime = None, 
                    datum_dolaska: datetime = None, putnici: list = None) -> list:

    filtrirano = list()
    for karta in sve_karte:
        konkretan_let = svi_konkretni_letovi[sve_karte[karta]['sifra_konkretnog_leta']]
        let = svi_letovi[konkretan_let['broj_leta']]
        if polaziste == let['sifra_polazisnog_aerodroma'] or polaziste == "":
            if odrediste == let['sifra_odredisnog_aerodorma'] or odrediste == "":
                if not datum_polaska or datum_polaska == konkretan_let['datum_i_vreme_polaska'].date():
                    if not datum_dolaska or datum_dolaska == konkretan_let['datum_i_vreme_dolaska'].date():
                        if putnici != []:
                            u_listi = True
                            for putnik in putnici:
                                if putnik not in sve_karte[karta]['putnici']:
                                    u_listi = False
                                    break
                            if u_listi:
                                filtrirano.append(sve_karte[karta])
                        else:
                            filtrirano.append(sve_karte[karta])
    return filtrirano


"""
Funkcija menja sve vrednosti karte novim vrednostima. Kao rezultat vraća rečnik sa svim kartama, 
koji sada sadrži izmenu.
"""
def izmena_karte(
    sve_karte: iter,
    svi_konkretni_letovi: iter,
    broj_karte: int,
    nova_sifra_konkretnog_leta: int=None,
    nov_datum_polaska: datetime=None,
    sediste=None
) -> dict:
    karta = sve_karte[broj_karte]
    nova_karta = {
        karta['broj_karte']:
        {
            'broj_karte': broj_karte,
            'sifra_konkretnog_leta': nova_sifra_konkretnog_leta if nova_sifra_konkretnog_leta != None else karta['sifra_konkretnog_leta'],
            'kupac': karta['kupac'],
            'prodavac': karta['prodavac'],
            'obrisana': karta['obrisana'],
            'sediste': sediste if sediste != None else karta['sediste']
        }
    }
    
    if karta.get('prodavac') != None:
        nova_karta['prodavac'] = karta['prodavac']
    if karta.get('datum_prodaje') != None:
        nova_karta['datum_prodaje'] = karta['datum_prodaje']
    if karta.get('putnici') != None:
        nova_karta['putnici'] = karta['putnici']
    if karta.get('status') != None:
        nova_karta['status'] = karta['status']
    if sediste != None:
        konkretan_let = svi_konkretni_letovi[nova_karta['sifra_konkretnog_leta']]
        try:
            pozicija = sediste[len(sediste)-1]
            red = ""
            for karakter in range(len(sediste) - 1):
                red += karakter
            red = int(red)

            konkretan_let['zauzetost'][red][pozicija] = True

            pozicija = karta['sediste'][len(karta['sediste'] - 1)]
            red = ""
            for karakter in range(len(karta['sediste']) - 1):
                red += karakter
            red = int(red)
            
            konkretan_let['zauzetost'][red][pozicija] = False        
        except:
            sve_karte.update(nova_karta)
            return sve_karte
          
        
    sve_karte.update(nova_karta)
    return sve_karte
    



"""
Vraća sve nerealizovane karte za korisnika u listi.
"""

def pregled_nerealizovanaih_karata(korisnik: dict, sve_karte: dict) -> list:
    nerealizovane_karte = list()
    for karta in sve_karte:
        putnici = karta['putnici']
        if korisnik in putnici and karta['status'] == konstante.STATUS_NEREALIZOVANA_KARTA:
            nerealizovane_karte.append(karta)            
    return nerealizovane_karte

"""
 Funkcija brisanja karte se ponaša drugačije u zavisnosti od korisnika:
- Prodavac: karta se označava za brisanje
- Admin/menadžer: karta se trajno briše
Kao rezultat se vraća nova kolekcija svih karata. Baca grešku ako podaci nisu validni.
"""


def brisanje_karte(korisnik: dict, sve_karte: dict, broj_karte: int) -> dict:
    if broj_karte not in sve_karte:
        raise izuzeci.NeispravnoUnetiPodaci("Greška - Karta ne postoji!")
    if korisnik['uloga'] == konstante.ULOGA_KORISNIK:
        raise izuzeci.NedostatakDozvole(
            "Greška - Korisnik ne može da briše karte!")
    elif korisnik['uloga'] == konstante.ULOGA_PRODAVAC:
        sve_karte[broj_karte]['obrisana'] = True
    elif korisnik['uloga'] == konstante.ULOGA_ADMIN:
        del sve_karte[broj_karte]
    else:
        raise izuzeci.NepostojecaUloga("Greška - Uloga ne postoji!")
    return sve_karte

#TODO: Dodati aerodrome
def ispis_karte(karta: dict, svi_konkretni_letovi: dict, svi_letovi: dict, svi_aerodromi: dict):
    konkretan_let = svi_konkretni_letovi[karta['sifra_konkretnog_leta']]
    let = svi_letovi[konkretan_let['broj_leta']]
    datum_i_vreme_polaska = datetime.strftime(konkretan_let['datum_i_vreme_polaska'], konstante.FORMAT_DATETIME_BEZ_SEKUNDI)
    datum_i_vreme_dolaska = datetime.strftime(konkretan_let['datum_i_vreme_dolaska'], konstante.FORMAT_DATETIME_BEZ_SEKUNDI)
    print(f"{karta['broj_karte']: <20}{let['sifra_polazisnog_aerodroma']: <20}{let['sifra_odredisnog_aerodorma']: <20}{datum_i_vreme_polaska:<30}{datum_i_vreme_dolaska:<30}")



"""
Funkcija koja čuva sve karte u fajl na zadatoj putanji.
"""

def sacuvaj_karte(sve_karte: dict, putanja: str, separator: str):
    with open(putanja, 'w', newline="") as f:
        csv_pisac = DictWriter(f, ['broj_karte', 'sifra_konkretnog_leta', 'sediste', 'putnici', 'status',
                                   'kupac', 'prodavac', 'sifra_sedista', 'datum_prodaje', 'obrisana'], delimiter=separator)
        for karta in sve_karte:
            datum_prodaje = sve_karte[karta]['datum_prodaje']
            datum_prodaje = datetime.strftime(datum_prodaje, konstante.FORMAT_DATETIME)
            csv_pisac.writerow({
                'broj_karte': int(sve_karte[karta]['broj_karte']),
                'sifra_konkretnog_leta': int(sve_karte[karta]['sifra_konkretnog_leta']),
                'kupac': sve_karte[karta]['kupac'],
                'prodavac': sve_karte[karta]['prodavac'],
                'sediste': ""  if sve_karte[karta].get('sediste') == None else sve_karte[karta]['sediste'],
                'status': sve_karte[karta]['status'],
                'putnici': sve_karte[karta]['putnici'],
                'datum_prodaje': datum_prodaje,
                'obrisana': sve_karte[karta]['obrisana']
            })
"""
Funkcija koja učitava sve karte iz fajla i vraća ih u rečniku.
"""

def ucitaj_karte_iz_fajla(putanja: str, separator: str) -> dict:
    global sledeci_broj_karte
    with open(putanja) as f:
        karte = dict()
        csv_citac = DictReader(f, ['broj_karte', 'sifra_konkretnog_leta', 'sediste', 'putnici', 'status',
                                   'kupac', 'prodavac', 'sifra_sedista', 'datum_prodaje', 'obrisana'], delimiter = separator)
        for karta in csv_citac:
            try:
                datum_prodaje = datetime.strptime(karta['datum_prodaje'], konstante.FORMAT_DATETIME)
            except:
                datum_prodaje = ''
            karte.update({
                int(karta['broj_karte']):
                    {
                        'broj_karte': int(karta['broj_karte']),
                        'sifra_konkretnog_leta': int(karta['sifra_konkretnog_leta']),
                        'kupac': karta['kupac'],
                        'prodavac': karta['prodavac'],
                        'sediste': karta['sediste'],
                        'status': karta['status'],
                        'putnici': eval(karta['putnici']),
                        'datum_prodaje': datum_prodaje,
                        'obrisana': karta['obrisana'] == 'True'
                    }
            })
    if karte != {}:
        sledeci_broj_karte = max(karte) + 1
    return karte
