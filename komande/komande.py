from os import system
from time import sleep

from izuzeci import izuzeci
from common import konstante
from interfejsi import interfejsi

from datetime import datetime, timedelta
from korisnici import korisnici
from letovi import letovi
from karte import karte
from izvestaji import izvestaji

svi_korisnici = dict()
sve_karte = dict()
svi_letovi = dict()
svi_konkretni_letovi = dict()

korisnik = dict()

# TODO: Svi printovi u ispisi_let()

# -------------------- LETOVI -------------------- #


def pretraga_letova():
    global svi_letovi, svi_konkretni_letovi

    polaziste = input("Polaziste: ")
    odrediste = input("Odredište: ")
    datum_polaska = input("Datum polaska: ")
    datum_dolaska = input("Datum dolaska: ")
    vreme_poletanja = input("Vreme poletanja: ")
    vreme_sletanja = input("Vreme sletanja: ")
    prevoznik = input("Prevoznik: ")

    filtrirani_letovi = letovi.pretraga_letova(svi_letovi, svi_konkretni_letovi, polaziste,
                                               odrediste, datum_polaska, datum_dolaska, vreme_poletanja, vreme_sletanja, prevoznik)
    print(filtrirani_letovi)

    while True:
        unos = input("Pritisnite enter da biste nastavili. ")
        if unos == "":
            return

# -------------------- CHECKIN -------------------- #

def prijava_na_let():
    pass

# -------------------- KARTE -------------------- #

# TODO: pretraga_karata(): Datume treba pretvoriti u datetime (ili to raditi u pretraga_karata)

def pretraga_karata():
    global svi_letovi, svi_konkretni_letovi, karte

    polaziste = input("Unesite polazište: ")
    odrediste = input("Unesite odredište: ")
    datum_polaska = input("Unesite datum polaska: ")
    datum_dolaska = input("Unesite datum dolaska: ")
    putnici = list()
    while True:
        ime = input("Unesite ime putnika: ")
        prezime = input("Unesite prezime putnika: ")
        putnici.append({'ime': ime, 'prezime': prezime})
        unos = input("Pritisnite enter ukoliko želite da nastavite dalje.")
        if unos == "":
            break

    karte.pretraga_karata(sve_karte, svi_konkretni_letovi, svi_letovi,
                          polaziste, odrediste, datum_polaska, datum_dolaska, putnici)


def kupovina_karte():
    global korisnik, sve_karte, svi_konkretni_letovi, svi_letovi

    def odabir_putnika(sifra_konkretnog_leta: int):
        putnici = list()

        def potrvda_kupovine(putnici: list) -> bool:
            print(f"Putnici: \n{putnici}")
            unos = input(">> ")
            if unos == "1":
                slobodna_mesta = list()
                try:
                    slobodna_mesta = svi_konkretni_letovi[sifra_konkretnog_leta]['zauzetost']
                except:
                    slobodna_mesta = letovi.podesi_matricu_zauzetosti(
                        svi_letovi, svi_konkretni_letovi[sifra_konkretnog_leta])
                karta = karte.kupovina_karte(
                    sve_karte, svi_konkretni_letovi, sifra_konkretnog_leta, putnici, slobodna_mesta, korisnik)
                return True
            elif unos == "X":
                return False
            else:
                print("Nepostojeća komanda")

        def kupovina_sledece(sifra_konkretnog_leta: int):
            print("Karte je uspešno kupljena!")
            print("Da li želite da kupite sledeću kartu?")
            print("1: Da")
            print("2: Ne")
            unos = input(">> ")
            if unos == "1":
                datum_sletanja = svi_konkretni_letovi[sifra_konkretnog_leta]['datum_i_vreme_dolaska']
                poslednji_termin = datum_sletanja + timedelta(minutes=120)
                odrediste = svi_letovi[svi_konkretni_letovi[sifra_konkretnog_leta]
                                       ['broj_leta']]['sifra_odredisnog_aerodorma']

                filtrirani = letovi.pretraga_letova(
                    svi_letovi, svi_konkretni_letovi, odrediste, "", datum_sletanja, "", "", "", "")
                moguci_letovi = list()
                for let in filtrirani:
                    if let['datum_i_vreme_polaska'] >= datum_sletanja and let['datum_i_vreme_polaska'] <= poslednji_termin:
                        moguci_letovi.append(let)
                print(moguci_letovi)

                if moguci_letovi == []:
                    print("Ne postoje sledeći letovi!")
                    sleep(3)
                    return

                while True:
                    sifra_narednog_leta = input(
                        "Unesite šifru narednog leta: ")
                    if sifra_narednog_leta in moguci_letovi:
                        interfejsi.odabir_putnika()
                        odabir_putnika(sifra_narednog_leta)
                    if sifra_narednog_leta == "":
                        return
            elif unos == "2":
                return

        while True:
            unos = input(">> ")
            if unos == "1":
                if korisnik not in putnici:
                    putnici.append(korisnik)

                interfejsi.potrvda_kupovine()
                potvda = potrvda_kupovine(putnici)
                if potvda:
                    interfejsi.nastavak_kupovine_sledece_karte()
                    kupovina_sledece(sifra_konkretnog_leta)
                    return
            elif unos == "2":
                ime = input("Ime putnika: ")
                prezime = input("Prezime putnika: ")
                if {'ime': ime, 'prezime': prezime} not in putnici:
                    putnici.append({'ime': ime, 'prezime': prezime})

                interfejsi.potrvda_kupovine()
                potvrda = potrvda_kupovine(putnici)
                if potvrda:
                    interfejsi.nastavak_kupovine_sledece_karte()
                    kupovina_sledece(sifra_konkretnog_leta)
                    return

            elif unos == "X":
                return
            else:
                print("Nepostojeća komanda!")
                sleep(0.5)
            interfejsi.odabir_putnika()

    while True:
        unos = input(">> ")
        if unos == "1":
            konkretan_let = int(input("Unesite šifru leta: "))
            if konkretan_let not in svi_konkretni_letovi:
                print("Let ne postoji")
            else:
                interfejsi.odabir_putnika()
                odabir_putnika(konkretan_let)
        elif unos == "2":
            interfejsi.filteri_za_pretragu_letova()
            pretraga_letova()
        elif unos == "X":
            return
        else:
            print("Nepostojeća komanda!")
            sleep(0.5)

        interfejsi.kupovina_karata()

# -------------------- KORISNIK -------------------- #

def prijavljeni_korisnik():
    global svi_letovi, korisnik, sve_karte

    while True:
        unos = input(">> ")
        if unos == "1":
            karte.pregled_nerealizovanaih_karata(korisnik, sve_karte)
            while True:
                kraj = input("Pritisnite enter.")
                if kraj == "":
                    break
        elif unos == "2":
            interfejsi.filteri_za_pretragu_letova()
            pretraga_letova()
        elif unos == "3":
            interfejsi.kupovina_karata()
            kupovina_karte()
        elif unos == "4":
            print("Prijava na let trenutno nije dostpuno!")
            sleep(0.5)
        elif unos == "5":
            pass
        elif unos == "6":
            print(polasci())
            while True:
                kraj = input("Pritisnite enter.")
                if kraj == "":
                    break
        elif unos == "X":
            return
        else:
            print("Nepostojeća komanda!")
            sleep(0.5)

        interfejsi.korisnicki(korisnik)

# -------------------- PRODAVAC -------------------- #


def izmena_letova():
    pass


def brisanje_karata():
    pass


def prijavljeni_prodavac():
    global korisnik

    while True:
        unos = input(">> ")
        if unos == "1":
            pass  # prodaja karata
        elif unos == "2":
            pass  # prijava_na_let
        elif unos == "3":
            pass  # izmena karte
        elif unos == "4":
            pass  # brisanje karte
        elif unos == "5":
            pass  # pretraga prodatih karata
        elif unos == "X":
            return
        else:
            print("Nepostojeća komanda!")
            sleep(0.5)
        interfejsi.prodavacki(korisnik)


# def prijavljeni_prodavac():
#     global korisnik

#     while True:
#         unos = input(">> ")
#         if unos == "P":
#             interfejsi.prodavacki(korisnik)
#             prijavljeni_prodavac_glavni()
#         elif unos == "K":
#             interfejsi.korisnicki(korisnik)
#             prijavljeni_korisnik()
#         elif unos == "X":
#             korisnici.logout(korisnik)
#             return
#         interfejsi.prodavacki_pocetni(korisnik)


# -------------------- ADMIN -------------------- #

def registracija_novog_prodavca():
    pass


def kreiranje_letova():
    pass


def izvestaji():
    pass


def prijavljeni_admin_glavni():
    global korisnik

    while True:
        unos = input(">> ")
        if unos == "1":
            pretraga_karata()
        elif unos == "2":
            registracija_novog_prodavca()
        elif unos == "3":
            kreiranje_letova()
        elif unos == "4":
            izmena_letova()
        elif unos == "5":
            brisanje_karata()
        elif unos == "X":
            return

        interfejsi.adminski(korisnik)


def prijavljeni_admin():
    global korisnik

    while True:
        unos = input(">> ")
        if unos == "A":
            interfejsi.adminski(korisnik)
            prijavljeni_admin_glavni()
        elif unos == "K":
            interfejsi.korisnicki(korisnik)
            prijavljeni_korisnik()
        elif unos == "X":
            korisnici.logout(korisnik)
            return
        interfejsi.adminski_pocetni(korisnik)


# -------------------- OSTALO -------------------- #
def polasci():
    global svi_konkretni_letovi, svi_letovi

    polaziste = input("Unesite polazište: ")
    odrediste = input("Unesite odredište: ")
    datum = input("Unesite datum: ")

    fleksibilni_dani = int(input("Unesite broj fleksibilnih dana: "))

    pocetni = (datetime.strptime(datum, "%Y-%m-%d") -
               timedelta(days=fleksibilni_dani)).date()
    krajnji = (datetime.strptime(datum, "%Y-%m-%d") +
               timedelta(days=fleksibilni_dani)).date()

    filtriranik_letovi = list()
    for konkretan_let in svi_konkretni_letovi:
        if polaziste == svi_letovi[svi_konkretni_letovi[konkretan_let]['broj_leta']] or polaziste == "":
            if odrediste == svi_letovi[svi_konkretni_letovi[konkretan_let]['broj_leta']] or odrediste == "":
                konkretan_datum = svi_konkretni_letovi[konkretan_let]['datum_i_vreme_polaska'].date(
                )
                if konkretan_datum <= krajnji and konkretan_datum >= pocetni:
                    filtriranik_letovi.append(
                        svi_konkretni_letovi[konkretan_let])
    return filtriranik_letovi


def pocetna_strana():
    global svi_korisnici, korisnik, svi_konkretni_letovi, svi_letovi

    while True:
        unos = input(">> ")
        if unos == "1":
            interfejsi.registracija()
            korisnici.registracija(svi_korisnici)
        elif unos == "2":
            korisnik = korisnici.prijava(svi_korisnici)
            if korisnik != None:
                if korisnik['uloga'] == konstante.ULOGA_KORISNIK:
                    interfejsi.korisnicki(korisnik)
                    prijavljeni_korisnik()
                elif korisnik['uloga'] == konstante.ULOGA_ADMIN:
                    interfejsi.adminski_pocetni(korisnik)
                    prijavljeni_admin()
                elif korisnik['uloga'] == konstante.ULOGA_PRODAVAC:
                    interfejsi.prodavacki(korisnik)
                    prijavljeni_prodavac()
                else:
                    izuzeci.NepostojecaUloga()
        elif unos == "3":
            letovi.pregled_nerealizovanih_letova(svi_letovi)
            while True:
                kraj = input("Pritisnite enter.")
                if kraj == "":
                    break
        elif unos == "4":
            interfejsi.filteri_za_pretragu_letova()
            pretraga_letova()
        elif unos == "5":
            polaziste = input("Unesite polazište: ")
            odrediste = input("Unesite odredište: ")
            letovi.trazenje_10_najjeftinijih_letova(
                svi_letovi, polaziste, odrediste)
            while True:
                kraj = input("Pritisnite enter.")
                if kraj == "":
                    break
        elif unos == "6":
            print(polasci())
            while True:
                kraj = input("Pritisnite enter.")
                if kraj == "":
                    break
        elif unos == "X":
            print("Izlazak iz aplikacije...")
            korisnici.sacuvaj_korisnike(
                konstante.PUTANJA_KORSINICI, ",", svi_korisnici)
            karte.sacuvaj_karte(sve_karte, konstante.PUTANJA_KARTE, ",")
            letovi.sacuvaj_letove(konstante.PUTANJA_LETOVI, ",", svi_letovi)
            return
        else:
            print("Nepostojeća komanda")
            sleep(0.5)

        interfejsi.pocetna_strana()

# def kreiranje_konkretnih_letova():
#     global svi_konkretni_letovi, svi_letovi, sifra_konkretnog_leta

#     danas = datetime.now()

#     trenutan_dan = datetime.now()
#     poslednji_dan = trenutan_dan + timedelta(days = 7)

#     while poslednji_dan >= trenutan_dan:
#         for let in svi_letovi:
#             if trenutan_dan.weekday() in svi_letovi[let]['dani']:
#                 svi_konkretni_letovi.update(letovi.kreiranje_konkretnih_letova(svi_letovi, let, trenutan_dan , trenutan_dan + timedelta(days=30)))
#         trenutan_dan += timedelta(days = 1)


def inicializacija():
    global svi_konkretni_letovi, svi_korisnici, sve_karte, svi_letovi

    svi_korisnici = korisnici.ucitaj_korisnike_iz_fajla(
        konstante.PUTANJA_KORSINICI, ",")
    sve_karte = karte.ucitaj_karte_iz_fajla(konstante.PUTANJA_KARTE, ",")
    svi_letovi = letovi.ucitaj_letove_iz_fajla(konstante.PUTANJA_LETOVI, ",")
    for let in svi_letovi:
        svi_konkretni_letovi.update(letovi.kreiranje_konkretnih_letova(
            svi_letovi, let, datetime.now(), datetime.now() + timedelta(days=30)))

    interfejsi.pocetna_strana()
    pocetna_strana()
