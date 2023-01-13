from letovi import letovi
from karte import karte
from datetime import datetime, timedelta, date
from izuzeci import izuzeci
from common import konstante

def izvestaj_prodatih_karata_za_dan_prodaje(sve_karte: dict, dan: date) -> list:
    prodate_karte = list()
    for karta in sve_karte:
        datum_prodaje = sve_karte[karta]['datum_prodaje'] 
        if type(datum_prodaje) == str:
            datum_prodaje = datetime.strptime(datum_prodaje, konstante.FORMAT_DATETIME).date()
        if datum_prodaje == dan:
            prodate_karte.append(sve_karte[karta])
    return prodate_karte


def izvestaj_prodatih_karata_za_dan_polaska(sve_karte: dict, svi_konkretni_letovi: dict, dan: date) -> list:
    prodate_karte = list()
    for karta in sve_karte:
        sifra_konkretnog_leta = sve_karte[karta]['sifra_konkretnog_leta']
        datum_polaska = svi_konkretni_letovi[sifra_konkretnog_leta]['datum_i_vreme_polaska']
        if dan == datum_polaska.date():
            prodate_karte.append(sve_karte[karta])
    return prodate_karte


def izvestaj_prodatih_karata_za_dan_prodaje_i_prodavca(sve_karte: dict, dan: date, prodavac: str) -> list:
    prodate_karte = list()
    for karta in sve_karte:
        prodavac_karte = sve_karte[karta]['prodavac']
        if prodavac_karte == "":
            continue
        if type(prodavac_karte) != str:
            prodavac_karte = prodavac_karte['korisnicko_ime']
        datum_prodaje = sve_karte[karta]['datum_prodaje']
        if type(datum_prodaje) == str:
            datum_prodaje = datetime.strptime(datum_prodaje, konstante.FORMAT_DATETIME).date()
        if prodavac == prodavac_karte and dan == datum_prodaje:
            prodate_karte.append(sve_karte[karta])
    return prodate_karte


# ubc znaci ukupan broj i cena vraca neki tapl
def izvestaj_ubc_prodatih_karata_za_dan_prodaje(sve_karte: dict, svi_konkretni_letovi: dict, svi_letovi: dict,  dan: date) -> (int, float):
    broj_prodatih_karata = 0
    ukupna_cena = 0
    for karta in sve_karte:
        datum_prodaje = sve_karte[karta]['datum_prodaje']
        if type(datum_prodaje) == str:
            datum_prodaje = datetime.strptime(datum_prodaje, konstante.FORMAT_DATETIME).date()
        if datum_prodaje == dan:
            broj_prodatih_karata += 1
            ukupna_cena += svi_letovi[svi_konkretni_letovi[sve_karte[karta]['sifra_konkretnog_leta']]['broj_leta']]['cena']
    return (broj_prodatih_karata, ukupna_cena)


# ubc znaci ukupan broj i cena
def izvestaj_ubc_prodatih_karata_za_dan_polaska(sve_karte: dict, svi_konkretni_letovi: dict, svi_letovi: dict, dan: date):
    broj_prodatih_karata = 0
    ukupna_cena = 0
    try:
        dan = dan.date()
    except:
        pass
    for karta in sve_karte:
        konkretan_let = svi_konkretni_letovi[sve_karte[karta]['sifra_konkretnog_leta']]
        datum_polaska = konkretan_let['datum_i_vreme_polaska']
        
        if datum_polaska.date() == dan:
            broj_prodatih_karata += 1
            sifra_konkretnog_leta = sve_karte[karta]['sifra_konkretnog_leta']
            ukupna_cena += svi_letovi[svi_konkretni_letovi[sifra_konkretnog_leta]['broj_leta']]['cena']
    return (broj_prodatih_karata, ukupna_cena)


# ubc znaci ukupan broj i cena
def izvestaj_ubc_prodatih_karata_za_dan_prodaje_i_prodavca(sve_karte: dict, svi_konkretni_letovi: dict, svi_letovi: dict, dan: date, prodavac: str):
    broj_prodatih_karata = 0
    ukupna_cena = 0
    for karta in sve_karte:
        datum_prodaje = sve_karte[karta]['datum_prodaje']
        if type(datum_prodaje) == str:
            datum_prodaje = datetime.strptime(datum_prodaje, konstante.FORMAT_DATETIME).date()
        prodavac_karte = sve_karte[karta]['prodavac']
        if prodavac_karte == "":
            continue
        if type(prodavac_karte) != str:
            prodavac_karte = prodavac_karte['korisnicko_ime']
        if datum_prodaje == dan and prodavac_karte == prodavac:
            broj_prodatih_karata += 1
            sifra_konkretnog_leta = sve_karte[karta]['sifra_konkretnog_leta']
            ukupna_cena += svi_letovi[svi_konkretni_letovi[sifra_konkretnog_leta]['broj_leta']]['cena']
    return (broj_prodatih_karata, ukupna_cena)


# ubc znaci ukupan broj i cena
def izvestaj_ubc_prodatih_karata_30_dana_po_prodavcima(sve_karte: dict, svi_konkretni_letovi: dict, svi_letovi: dict) -> dict:
    danasnji_dan = datetime.now().date()
    pocetak_izvestaja = danasnji_dan - timedelta(days = 30)
    
    izvestaji = dict()
    prodavci = list()
    ukupna_cena = 0

    for karta in sve_karte:
        datum_prodaje = sve_karte[karta]['datum_prodaje']
        if type(datum_prodaje) == str:
            try:
                datum_prodaje = datetime.strptime(datum_prodaje, konstante.FORMAT_DATETIME).date()
            except:
                datum_prodaje = datetime.strptime(datum_prodaje, "%d.%m.%Y.").date()
        if danasnji_dan >= datum_prodaje >= pocetak_izvestaja:
            cena = svi_letovi[svi_konkretni_letovi[sve_karte[karta]['sifra_konkretnog_leta']]['broj_leta']]['cena']
            if sve_karte[karta].get('prodavac'):
                prodavac = sve_karte[karta]['prodavac']
                if type(prodavac) == dict:
                    prodavac = sve_karte[karta]['prodavac']['korisnicko_ime']
                if prodavac == "":
                    continue
                if prodavci == [] or prodavac not in list(zip(*prodavci))[2]:
                    prodavci.append([1, cena, prodavac])
                else:
                    i = 0
                    while i < len(prodavci):
                        if prodavci[i][2] == prodavac:
                            prodavci[i][1] += cena
                            prodavci[i][0] += 1
                            break
                        i += 1
    if prodavci != []:
        for broj_karte, cena, prodavac in prodavci:
            izvestaji.update({
                prodavac:(broj_karte,cena,prodavac)
            })
    return izvestaji