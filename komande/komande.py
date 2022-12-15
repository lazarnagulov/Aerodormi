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

#TODO: Posebni moduli za letove, karte, admine, korisnike...
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
    
    filtrirani_letovi = letovi.pretraga_letova(svi_letovi, svi_konkretni_letovi, polaziste, odrediste, datum_polaska, datum_dolaska, vreme_poletanja, vreme_sletanja, prevoznik)
    print(filtrirani_letovi)
        
    while True:
        unos = input("Pritisnite enter da biste nastavili. ")
        if unos == "":
            return


def prijava_na_let():
    pass

# -------------------- KARTE -------------------- #

def odabir_putnika(sifra_konkretnog_leta: int):
    global sve_karte, svi_konkretni_letovi, korisnik
    
    for karta in sve_karte:
        if sifra_konkretnog_leta == sve_karte[karta]['sifra']:
            karta_za_kupovinu = sve_karte[karta]
    
    slobodna_mesta = []
    try:
        matrica_zauzetosti = letovi.matrica_zauzetosti(svi_konkretni_letovi[sifra_konkretnog_leta])
    except:
        matrica_zauzetosti = letovi.podesi_matricu_zauzetosti(svi_letovi, svi_konkretni_letovi[sifra_konkretnog_leta])
    
    red = list()        
    for i in range(len(matrica_zauzetosti)):
        for j in range(len(matrica_zauzetosti[i])):
            if matrica_zauzetosti[i][j] == 'X':
                red.append(False)
            else:
                red.append(True)
        slobodna_mesta.append(red)
        red = list()
    while True:
        unos = input(">> ")
        if unos == "1":
            if len(slobodna_mesta) < 1:
                print("Nema slobodnih mesta")
            else:
                interfejsi.potrvda_kupovine()
                potrvda_kupovine(slobodna_mesta, sifra_konkretnog_leta)
                return
                
        elif unos == "2":
            ime = input("Unesite ime putnika: ")
            prezime = input("Unesite prezime putnika: ")
            if len(slobodna_mesta) < 1:
                print("Nema slobodnih mesta")
            else:
                interfejsi.potrvda_kupovine()
                potrvda_kupovine(slobodna_mesta, sifra_konkretnog_leta, ime = ime, prezime = prezime)
                return
        elif unos == "X":
            return
        else:
            print("Nepsotojeca komanda")
        
        interfejsi.odabir_putnika()


def kupovina_karte():
    global svi_konkretni_letovi, svi_letovi
    
    while True:
        unos = input(">> ")
        if unos == "1":
            konkretan_let = int(input("Unesite šifru leta: "))
            if konkretan_let not in svi_konkretni_letovi:
                print("Let ne postoji")
            else:                
                interfejsi.odabir_putnika()
                odabir_putnika(konkretan_let)
                return
        elif unos == "2":
            interfejsi.filteri_za_pretragu_letova()
            pretraga_letova()
        elif unos == "X":
            return
        else:
            print("Nepostojeća komanda!")
            sleep(0.5)
    
        interfejsi.kupovina_karata()

def nastavak_kupovine_sledece_karte():
    pass


def nastavak_kupovine():
    while True:
        unos = input(">> ")
        if unos == "1":
            pass
        elif unos == "2":
            pass
        elif unos == "X":
            return
        else:
            print("Nepostojeća komanda!")
            sleep(0.5)
        
        interfejsi.nastavak_kupovine()
        
def dodatne_korisnicke_informacije():
    pass

def potrvda_kupovine(slobodna_mesta: list, sifra_konkretnog_leta: int,**kwargs):
    global korisnik, sve_karte, svi_konkretni_letovi
    
    while True:
        unos = input(">> ")
        if unos == "1":
            if kwargs != {}:
                karte.kupovina_karte(sve_karte, svi_konkretni_letovi, sifra_konkretnog_leta, [{'ime': kwargs['ime'], 'prezime': kwargs['prezime']}], slobodna_mesta, korisnik)
                print("Uspešno ste kupili kartu!")
                sleep(3)
                interfejsi.nastavak_kupovine()
                nastavak_kupovine()
                return
            else:
                karte.kupovina_karte(sve_karte, svi_konkretni_letovi, sifra_konkretnog_leta, korisnik, slobodna_mesta, korisnik)
                print("Uspešno ste kupili kartu!")
                sleep(3)
                interfejsi.nastavak_kupovine()
                nastavak_kupovine()
                return
        elif unos == "X":
            return
        else:
            print("Nepostojeća komanda!")
            sleep(0.5)
        
        interfejsi.potrvda_kupovine()

# -------------------- KORISNIK -------------------- #

def prijavljeni_korisnik():
    global svi_letovi, korisnik
    
    while True:
        unos = input(">> ")
        if unos == "1":
            print("Pregled karata trenutno nije dostupno!")
            sleep(0.5)
        elif unos == "2":
            interfejsi.filteri_za_pretragu_letova()
            pretraga_letova()
        elif unos == "3":
            interfejsi.kupovina_karata()
            kupovina_karte()
        elif unos == "4":
            print("Prijava na let trenutno nije dostpuno!")
            sleep(0.5)
        elif unos == "X":
            return
        else:
            print("Nepostojeća komanda!")
            sleep(0.5)

        interfejsi.korisnicki(korisnik)

# -------------------- PRODAVAC -------------------- #

def prijavljeni_prodavac_glavni():
    global korisnik
    
    while True:
        unos = input(">> ")
        
        
        interfejsi.prodavacki(korisnik)


def prijavljeni_prodavac():
    global korisnik
    
    while True:
        unos = input(">> ")
        if unos == "P":
            interfejsi.prodavacki(korisnik)
            prijavljeni_prodavac_glavni()
        elif unos == "K":
            interfejsi.korisnicki(korisnik)
            prijavljeni_korisnik()
        elif unos == "X":
            korisnici.logout(korisnik)
            return
        interfejsi.adminski_pocetni(korisnik)
        

# -------------------- ADMIN -------------------- #

def prijavljeni_admin_glavni():
    global korisnik
    
    while True:
        unos = input(">> ")
        
        
        
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

def pocetna_strana():
    global svi_korisnici, korisnik
    
    while True:
        unos = input(">> ")
        if unos == "1":
            interfejsi.registracija()
            korisnici.registracija(svi_korisnici)
        elif unos == "2":
            korisnik = korisnici.prijava(svi_korisnici)
            if korisnik['uloga'] == konstante.ULOGA_KORISNIK:
                interfejsi.korisnicki(korisnik)
                prijavljeni_korisnik()
            elif korisnik['uloga'] == konstante.ULOGA_ADMIN:
                interfejsi.adminski_pocetni(korisnik)
                prijavljeni_admin()
            elif korisnik['uloga'] == konstante.ULOGA_PRODAVAC:
                interfejsi.prodavacki_pocetni(korisnik)
                prijavljeni_prodavac()
            else:
                izuzeci.NepostojecaUloga()
        elif unos == "3":
            letovi.pregled_nerealizovanih_letova(svi_letovi)
            sleep(3)
        elif unos == "4":
            interfejsi.filteri_za_pretragu_letova()
            pretraga_letova()
        elif unos == "X":
            print("Izlazak iz aplikacije...")
            return
        else:
            korisnici.sacuvaj_korisnike(konstante.PUTANJA_KORSINICI, ",", svi_korisnici)
            print("Nepostojeća komanda")
            sleep(0.5)

        interfejsi.pocetna_strana()

def kreiranje_konkretnih_letova():
    global svi_konkretni_letovi, svi_letovi, sifra_konkretnog_leta
    
    danas = datetime.now()
    
    trenutan_dan = datetime.now()
    poslednji_dan = trenutan_dan + timedelta(days = 7)

    while poslednji_dan >= trenutan_dan:
        for let in svi_letovi:
            if trenutan_dan.weekday() in svi_letovi[let]['dani']:
                svi_konkretni_letovi.update(letovi.kreiranje_konkretnih_letova(svi_letovi, let, trenutan_dan , trenutan_dan + timedelta(days=30)))
        trenutan_dan += timedelta(days = 1)

            
def inicializacija():
    global svi_korisnici, sve_karte, svi_letovi
    
    svi_korisnici = korisnici.ucitaj_korisnike_iz_fajla(konstante.PUTANJA_KORSINICI, ",")
    # sve_karte = karte.ucitaj_karte_iz_fajla(konstante.PUTANJA_KARTE, ",")
    # svi_letovi = letovi.ucitaj_letove_iz_fajla(konstante.PUTANJA_LETOVI, ",")    
    # svi_konkretni_letovi = kreiranje_konkretnih_letova()
    
    interfejsi.pocetna_strana()
    pocetna_strana()
