from letovi import letovi
from karte import karte
from datetime import datetime, timedelta
from izuzeci import izuzeci

def izvestaj_prodatih_karata_za_dan_prodaje(sve_karte: dict, dan: str) -> list:
    prodate_karte = list()
    for karta in sve_karte:
        if sve_karte[karta]['datum_prodaje'] == dan:
            prodate_karte.append(sve_karte[karta])
    return prodate_karte
    
def izvestaj_prodatih_karata_za_dan_polaska(sve_karte: dict, svi_konkretni_letovi: dict, dan: str) -> list:
    prodate_karte = list()
    for karta in sve_karte:
        sifra_konkretnog_leta = sve_karte[karta]['sifra_konkretnog_leta']
        datum_polaska = svi_konkretni_letovi[sifra_konkretnog_leta]['datum_polaska']
        if dan == datum_polaska:
            prodate_karte.append(sve_karte[karta])
    return prodate_karte

def izvestaj_prodatih_karata_za_dan_prodaje_i_prodavca(sve_karte: dict, dan: str, prodavac: str) -> list:
    prodate_karte = list()
    for karta in sve_karte:
        prodavac_karte = sve_karte[karta]['prodavac']
        datum_prodaje = sve_karte[karta]['datum_prodaje']
        if prodavac == prodavac_karte and dan == datum_prodaje:
            prodate_karte.append(sve_karte[karta])
    return prodate_karte

# Nemam pristup ceni, treba dodati svi_letovi, ili cenu kartu stavi u sve_karte
def izvestaj_ubc_prodatih_karata_za_dan_prodaje(sve_karte: dict, dan: str): #ubc znaci ukupan broj i cena vraca neki tapl
    broj_prodatih_karata = dict()
    for karta in sve_karte:
        if sve_karte[karta]['datum_prodaje'] == dan:
            if karta in broj_prodatih_karata:
                broj_prodatih_karata[karta] += 1
            else:
                broj_prodatih_karata[karta] = 1
    return (broj_prodatih_karata, 69)

def izvestaj_ubc_prodatih_karata_za_dan_polaska(sve_karte: dict, svi_konkretni_letovi: dict, dan: str): #ubc znaci ukupan broj i cena
    broj_prodatih_karata = dict()
    for karta in sve_karte:
        datum_polaska = svi_konkretni_letovi[sve_karte[karta]['sifra_konkretnog_leta']]
        if datum_polaska == dan:
            if karta in broj_prodatih_karata:
                broj_prodatih_karata[karta] += 1
            else:
                broj_prodatih_karata[karta] = 1
    return (broj_prodatih_karata, 420)

def izvestaj_ubc_prodatih_karata_za_dan_prodaje_i_prodavca(sve_karte: dict, dan: str, prodavac: str): #ubc znaci ukupan broj i cena
    broj_prodatih_karata = dict()
    for karta in sve_karte:
        datum_prodaje = sve_karte[karta]['datum_prodaje']
        prodavac_karte = sve_karte[karta]['prodavac']
        if datum_prodaje == dan and prodavac_karte == prodavac:
            if karta in broj_prodatih_karata:
                broj_prodatih_karata[karta] += 1
            else:
                broj_prodatih_karata[karta] = 1
    return (broj_prodatih_karata, 69420)

def izvestaj_ubc_prodatih_karata_30_dana_po_prodavcima(sve_karte: dict) -> dict: #ubc znaci ukupan broj i cena
    # trenutno_vreme = datetime.now()
    # vreme_vazenja = trenutno_vreme + timedelta(days=30)
    
    # trenutno_vreme = trenutno_vreme.strftime("%d.%m.%Y.")
    # vreme_vazenja = vreme_vazenja.strftime("%d.%m.%Y.")
    broj_prodatih_karata = dict()
    for karta in sve_karte:
        prodavac = sve_karte[karta]['prodavac']
        if prodavac in broj_prodatih_karata:
            broj_prodatih_karata[prodavac] += 1
        else:
            broj_prodatih_karata[prodavac] = 1
    return broj_prodatih_karata

