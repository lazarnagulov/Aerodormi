from os import system
from time import sleep

from izuzeci import izuzeci
from common import konstante
from interfejsi import interfejsi

from korisnici import korisnici
from letovi import letovi
from karte import karte
from izvestaji import izvestaji

svi_korisnici = dict()
sve_karte = dict()
svi_letovi = dict()
svi_konkretni_letovi = dict()

korisnik = dict()

def komande_pretraga_letova():
    global svi_letovi, svi_konkretni_letovi
    
    polaziste = input("Polaziste: ")
    odrediste = input("Odredište: ")
    datum_polaska = input("Datum polaska: ")
    datum_dolaska = input("Datum dolaska: ")
    vreme_poletanja = input("Vreme poletanja: ")
    vreme_sletanja = input("Vreme sletanja: ")
    prevoznik = input("Prevoznik: ")
    
    filtrirani_letovi = letovi.pretraga_letova(svi_letovi, svi_konkretni_letovi, polaziste, odrediste, datum_polaska, datum_dolaska, vreme_poletanja, vreme_sletanja, prevoznik)
    for let in filtrirani_letovi:
        letovi.ispis_leta(let)


def komande_prijavljeni_korisnik():
    global svi_letovi, korisnik
    
    while True:
        unos = int(input(">> "))
        if unos == 1:
            letovi.pregled_nerealizovanih_letova(svi_letovi)
            sleep(0.5)
        elif unos == 2:
            interfejsi.filteri_za_pretragu_letova()
            komande_pretraga_letova()
        elif unos == 3:
            print("Kopovina karata trenutno nije dostupno!")
            sleep(0.5)
        elif unos == 4:
            print("Prijava na let trenutno nije dostpuno!")
            sleep(0.5)
        elif unos == 5:
            if korisnik['uloga'] == konstante.ULOGA_ADMIN:
                interfejsi.adminski_pocetni_interfejs(korisnik)
                komande_prijavljeni_admin()
                return
            elif korisnik['uloga'] == konstante.ULOGA_KORISNIK:
                return
        else:
            print("Nepostojeća komanda!")
            sleep(0.5)

        interfejsi.prijavljeni_interfejs(korisnik)

def komande_prijavljeni_admin():
    global korisnik
    
    while True:
        unos = input(">> ")
        if unos == "A":
            pass
        elif unos == "K":
            interfejsi.korisnicki_interfejs(korisnik)
            komande_prijavljeni_korisnik()
        elif unos == "X":
            korisnik = {}
            return
        

def komande_pocetna_strana():
    global svi_korisnici, korisnik
    
    while True:
        unos = int(input(">> "))
        if unos == 1:
            interfejsi.registracija(svi_korisnici)
        elif unos == 2:
            korisnik = korisnici.prijava(svi_korisnici)
            if korisnik['uloga'] == konstante.ULOGA_KORISNIK:
                interfejsi.korisnicki_interfejs(korisnik)
                komande_prijavljeni_korisnik()
            elif korisnik['uloga'] == konstante.ULOGA_ADMIN:
                interfejsi.adminski_pocetni_interfejs(korisnik)
                komande_prijavljeni_admin()
            elif korisnik['uloga'] == konstante.ULOGA_PRODAVAC:
                pass
            else:
                izuzeci.NepostojecaUloga()
        elif unos == 3:
            letovi.pregled_nerealizovanih_letova(svi_letovi)
            sleep(3)
        elif unos == 4:
            interfejsi.filteri_za_pretragu_letova()
            komande_pretraga_letova()
        elif unos == 5:
            print("Izlazak iz aplikacije...")
            return
        else:
            korisnici.sacuvaj_korisnike(konstante.PUTANJA_KORSINICI, ",", svi_korisnici)
            print("Nepostojeća komanda")
            sleep(0.5)

        interfejsi.pocetna_strana()


def inicializacija():
    global svi_korisnici, sve_karte, svi_letovi, svi_konkretani_letovi
    
    svi_korisnici = korisnici.ucitaj_korisnike_iz_fajla(konstante.PUTANJA_KORSINICI, ",")
    sve_karte = karte.ucitaj_karte_iz_fajla(konstante.PUTANJA_KARTE, ",")
    svi_letovi = letovi.ucitaj_letove_iz_fajla(konstante.PUTANJA_LETOVI, ",")    
    
    interfejsi.pocetna_strana()
    komande_pocetna_strana()
