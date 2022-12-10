from os import system
from time import sleep
from izuzeci import izuzeci
from korisnici import korisnici
from common import konstante
from letovi import letovi

def zaglavlje(korisnik: dict):
    print("-------------------------------")
    print(f"Dobrodošao, {korisnik['korisnicko_ime']}!")
    print("-------------------------------")
    print(f"ULOGA: {korisnik['uloga'].capitalize()}")
    print("-------------------------------")
    print("1. Pregled letova")
    print("2. Pretraga letova")
    print("3. Kupovina karata")
    print("4. Prijava na let")
    print("5. Odjava")


def pocetna_strana():
    prijavljeni_korisnici = dict()
    svi_korisnici = korisnici.ucitaj_korisnike_iz_fajla(konstante.PUTANJA_KORSINICI, ",")
    svi_letovi = letovi.ucitaj_letove_iz_fajla(konstante.PUTANJA_LETOVI, ",")
    letovi.pregled_nerealizovanih_letova(svi_letovi)
    return
    while True:    
        system('cls')
        print("-------------------------------" )
        print("PRODAJA AVIONSKIH KARATA")
        print("-------------------------------")
        print("1. Registruj se")
        print("2. Prijavi se")
        print("3. Pregled letova")
        print("4. Pretraga letova")
        print("5. Izlazak")
        unos = int(input(">> "))
        if unos == 1:
            novi_korisnik = registracija(svi_korisnici)
        elif unos == 2:
            prijava(svi_korisnici, prijavljeni_korisnici)
        elif unos == 3:
            print("Pregled nerealizovanih letova trenutno nije dostupan!")
            sleep(0.5)
        elif unos == 4:
            print("Pretraga letova trenutno nije dostupna!")
            sleep(0.5)
        elif unos == 5:
            print("Izlazak iz aplikacije...")
            return
        else:
            korisnici.sacuvaj_korisnike(konstante.PUTANJA_KORSINICI, ",", svi_korisnici)
            print("Nepostojeća komanda")
            sleep(0.5)

def prijava(svi_korisnici: dict, prijavljeni_korisnici: dict):
    while True:
        system("cls")
        print("-------------------------------")
        print("Unesite korisničko ime i lozinku.")
        print("Pritisnite enter za povratak na početnu stranu.")
        print("-------------------------------")
        korisnicko_ime = str(input("Korisničko ime: "))
        if korisnicko_ime == "":
            return        
        lozinka = str(input("Lozinka: "))
        login = korisnici.login(svi_korisnici, korisnicko_ime, lozinka)
        if type(login) == dict:
            prijavljeni_korisnici.update({korisnicko_ime:login})
            print("Uspešna prijava!")
            prijavljeni_interfejs(login)
            return
        else:
            print(login)
            sleep(0.5)

def registracija(svi_korisnici: dict):
    while True:
        system("cls")
        print("-------------------------------")
        print("Unesite Vaše podatke.")
        print("Pritisnite enter za povratak na početnu stranu.")
        print("-------------------------------")
        korisnicko_ime = str(input("Korisničko ime: "))
        if korisnicko_ime == "":
            break
        lozinka = str(input("Lozinka: "))
        telefon = str(input("Kontakt telefon: "))
        email = str(input("Email: "))
        ime = str(input("Ime: "))
        prezime = str(input("Prezime: "))
        pasos = ""
        drzavljanstvo = ""
        pol = ""
        povratna_informacija = korisnici.kreiraj_korisnika(svi_korisnici, False, "korisnik", None, korisnicko_ime, lozinka, ime, prezime, email, pasos, drzavljanstvo, telefon, pol)
        if type(povratna_informacija) == dict:
            print("Uspešna registracija")
            korisnici.sacuvaj_korisnike("../korisnici.csv", ',', svi_korisnici)
            return povratna_informacija
        else:
            print(povratna_informacija)
            sleep(0.5)

def korisnicki_interfejs(korisnik: dict):
    while True:
        unos = int(input(">> "))
        if unos == 1:
            print("Pregled letova trenutno nije dostupno!")
            sleep(0.5)
        elif unos == 2:
            print("Pretraga letova trenutno nije dostupno!")
            sleep(0.5)
        elif unos == 3:
            print("Kopovina karata trenutno nije dostupno!")
            sleep(0.5)
        elif unos == 4:
            print("Prijava na let trenutno nije dostpuno!")
            sleep(0.5)
        elif unos == 5:
            return
        else:
            print("Nepostojeća komanda!")
            sleep(0.5)

def adminski_interfejs(korisnik: dict):
    pass

def prodavacki_interfejs(korisnik: dict):
    pass

def prijavljeni_interfejs(korisnik: dict):
    system('cls')
    zaglavlje(korisnik)
    if korisnik['uloga'] == konstante.ULOGA_KORISNIK:
        korisnicki_interfejs(korisnik)
    elif korisnik['uloga'] == konstante.ULOGA_ADMIN:
        adminski_interfejs(korisnik)
    elif korisnik['uloga'] == konstante.ULOGA_PRODAVAC:
        prodavacki_interfejs(korisnik)
    else:
        raise izuzeci.NepostojecaUloga("Fatalna greška - U bazi se nalazi korisnik sa nepostojećom ulogom!")