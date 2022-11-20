from os import system
from korisnici import korisnici
from common import konstante

def pocetna_strana():
    prijavljeni_korisnici = dict()
    svi_korisnici = dict()
    
    if svi_korisnici == {}:
        svi_korisnici = korisnici.ucitaj_korisnike_iz_fajla(konstante.PUTANJA, ",")
    system('cls')
    print("PRODAJA AVIONSKIH KARATA")
    print("--------------------------")
    print("1. Registruj se")
    print("2. Prijavi se")
    print("3. Pregled letova")
    print("4. Pretraga letova")
    print("5. Izlazak")
    unos = int(input(">> "))
    if unos == 1:
        novi_korisnik = korisnici.registruj(svi_korisnici)
        korisnici.sacuvaj_korisnike(konstante.PUTANJA, ",", svi_korisnici)
        pocetna_strana()
        return
    elif unos == 2:
        while True:
            korisnicko_ime = str(input("Korisničko ime: "))
            lozinka = str(input("Lozinka: "))
            login = korisnici.login(svi_korisnici, korisnicko_ime, lozinka)
            if type(login) == dict:
                prijavljeni_korisnici.update({korisnicko_ime:login})
                print("Uspešna prijava!")
                prijavljeni_interfejs(login)
                break
            else:
                print(login)
    elif unos == 3:
        print("Pregled nerealizovanih letova trenutno nije dostupan!")
    elif unos == 4:
        print("Pretraga letova trenutno nije dostupna!") 
    elif unos == 5:
        print("Izlazak iz aplikacije...")
        return
    else:
        print("Nepostojeća komanda")

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

def korisnicki_interfejs(korisnik: dict):
    while True:
        unos = int(input(">> "))
        if unos == 1:
            print("Pregled letova trenutno nije dostupno!")
            pass
        elif unos == 2:
            print("Pretraga letova trenutno nije dostupno!")
            pass
        elif unos == 3:
            print("Kopovina karata trenutno nije dostupno!")
            pass
        elif unos == 4:
            print("Prijava na let trenutno nije dostpuno!")
            pass
        elif unos == 5:
            system('cls')
            pocetna_strana()
            return
        else:
            print("Nepostojeća komanda!")

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
        print("Ne postojeća uloga!")
        


