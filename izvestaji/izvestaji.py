from letovi import letovi
from karte import karte
from datetime import datetime, timedelta, date
from izuzeci import izuzeci


def izvestaj_prodatih_karata_za_dan_prodaje(sve_karte: dict, dan: date) -> list:
    prodate_karte = list()
    for karta in sve_karte:
        if sve_karte[karta]['datum_prodaje'] == dan:
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
        datum_prodaje = sve_karte[karta]['datum_prodaje']
        if prodavac == prodavac_karte and dan == datum_prodaje:
            prodate_karte.append(sve_karte[karta])
    return prodate_karte


# ubc znaci ukupan broj i cena vraca neki tapl
def izvestaj_ubc_prodatih_karata_za_dan_prodaje(sve_karte: dict, svi_konkretni_letovi: dict, svi_letovi: dict,  dan: date):
    broj_prodatih_karata = 0
    ukupna_cena = 0
    for karta in sve_karte:
        if sve_karte[karta]['datum_prodaje'] == dan:
            broj_prodatih_karata += 1
            ukupna_cena += svi_letovi[svi_konkretni_letovi[sve_karte[karta]
                                                           ['sifra_konkretnog_leta']]['broj_leta']]['cena']
    return (broj_prodatih_karata, ukupna_cena)


# ubc znaci ukupan broj i cena
def izvestaj_ubc_prodatih_karata_za_dan_polaska(sve_karte: dict, svi_konkretni_letovi: dict, svi_letovi: dict, dan: date):
    broj_prodatih_karata = 0
    ukupna_cena = 0
    for karta in sve_karte:
        konkretan_let = svi_konkretni_letovi[sve_karte[karta]
                                             ['sifra_konkretnog_leta']]
        datum_polaska = konkretan_let['datum_i_vreme_polaska']
        if datum_polaska.date() == dan.date():
            broj_prodatih_karata += 1
            ukupna_cena += svi_letovi[svi_konkretni_letovi[konkretan_let['sifra_konkretnog_leta']]
                                      ['broj_leta']]['cena']
    return (broj_prodatih_karata, ukupna_cena)


# ubc znaci ukupan broj i cena
def izvestaj_ubc_prodatih_karata_za_dan_prodaje_i_prodavca(sve_karte: dict, svi_konkretni_letovi: dict, svi_letovi: dict, dan: date, prodavac: str):
    broj_prodatih_karata = 0
    ukupna_cena = 0
    for karta in sve_karte:
        datum_prodaje = sve_karte[karta]['datum_prodaje']
        prodavac_karte = sve_karte[karta]['prodavac']
        if datum_prodaje == dan and prodavac_karte == prodavac:
            broj_prodatih_karata += 1
            ukupna_cena += svi_letovi[svi_konkretni_letovi[sve_karte[karta]
                                                           ['sifra_konkretnog_leta']]['broj_leta']]['cena']
    return (broj_prodatih_karata, ukupna_cena)


# ubc znaci ukupan broj i cena
def izvestaj_ubc_prodatih_karata_30_dana_po_prodavcima(sve_karte: dict, svi_konkretni_letovi: dict, svi_letovi: dict) -> dict:
    # trenutno_vreme = datetime.now()
    # vreme_vazenja = trenutno_vreme + timedelta(days=30)

    broj_prodatih_karata = dict()
    for karta in sve_karte:
        prodavac = sve_karte[karta]['prodavac']
        if prodavac in broj_prodatih_karata:
            broj_prodatih_karata[prodavac] += 1
        else:
            broj_prodatih_karata[prodavac] = 1
    return broj_prodatih_karata
