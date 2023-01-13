from common import konstante
from csv import DictReader, DictWriter
from izuzeci import izuzeci
from interfejsi import interfejsi

def podesi_korisnika(korisnik: str, lozinka: str, ime: str, prezime: str,
                      uloga: str, pasos: str = "", drzavljanstvo: str = "",
                      telefon: str = "", email: str = "", pol: str = "") -> dict:
    
    svi_korisnici = dict()
    svi_korisnici.update({korisnik : {
        'korisnicko_ime': korisnik,
        'lozinka': lozinka,
        'ime': ime,
        'prezime': prezime,
        'uloga' : uloga,
        'pasos' : pasos,
        'drzavljanstvo' : drzavljanstvo,
        'telefon' : telefon,
        'email' : email,
        'pol' : pol
    }})

    return svi_korisnici

def validacija_korisnika(korisnik: str, lozinka: str, ime: str, prezime: str,
                      uloga: str, pasos: str = "",
                      telefon: str = "", email: str = ""):
    if  not (telefon and email and ime and prezime and korisnik and lozinka and uloga):
        raise izuzeci.NepostojeciPodaci("Greška - Obavezni podaci nisu pravilno uneti!")
    if email:
        if "@" not in email:
            raise izuzeci.NeispravanEmail(f"Greška - Email ({email}) ne sadrži @!")
        else:
            _, domen = str(email).split("@")
            if domen.count(".") != 1:
                raise izuzeci.NeispravanEmail(f"Greška - Email ({email}) sadrži više od jednog domena!")
    if uloga not in [konstante.ULOGA_ADMIN, konstante.ULOGA_KORISNIK, konstante.ULOGA_PRODAVAC]:
        raise izuzeci.NepostojecaUloga(f"Greška - Uloga {uloga} ne postoji!")
    if pasos:
        if not str(pasos).isnumeric():
            raise izuzeci.NeispravanPasos(f"Greška - Pasoš ({pasos}) nije numerički string!")
        if len(str(pasos)) != 9:
            raise izuzeci.NeispravanPasos(f"Greška - Pasoš ({pasos}) ne sadrži 9 cifara!")
    if telefon and not str(telefon).isnumeric():
        raise izuzeci.NeispravanTelefon(f"Greška - Telefon ({telefon}) nije numerički string!")
"""
Funkcija koja kreira novi rečnik koji predstavlja korisnika sa prosleđenim vrednostima. Kao rezultat vraća kolekciju
svih korisnika proširenu novim korisnikom. Može se ponašati kao dodavanje ili ažuriranje, u zavisnosti od vrednosti
parametra azuriraj:
- azuriraj == False: kreira se novi korisnik. staro_korisnicko_ime ne mora biti prosleđeno.
Vraća grešku ako korisničko ime već postoji.
- azuriraj == True: ažurira se postojeći korisnik. Staro korisnicko ime mora biti prosleđeno. 
Vraća grešku ako korisničko ime ne postoji.

Ova funkcija proverava i validnost podataka o korisniku, koji su tipa string.

CHECKPOINT 1: Vraća string sa greškom ako podaci nisu validni (ne važi za konverziju brojeva).
ODBRANA: Baca grešku sa porukom ako podaci nisu validni.
"""

def kreiraj_korisnika(svi_korisnici: dict, azuriraj: bool, uloga: str, staro_korisnicko_ime: str, korisnicko_ime: str,
                      lozinka: str, ime: str, prezime: str, email: str = "",
                      pasos: str = "", drzavljanstvo: str = "", 
                      telefon: str = "", pol: str = "") -> dict:
    validacija_korisnika(korisnicko_ime, lozinka, ime, prezime, uloga, pasos, telefon, email)
    if azuriraj:
        if staro_korisnicko_ime not in svi_korisnici:
            raise izuzeci.NepostojeceKorisnickoIme(f"Greška - Korisnik {staro_korisnicko_ime} ne postoji!")
        if staro_korisnicko_ime != korisnicko_ime:
            raise izuzeci.ZauzetoKorisnickoIme(f"Greška - Korisnik ({korisnicko_ime}) je zauzeto!")
        else:
            svi_korisnici.update(podesi_korisnika(korisnicko_ime, lozinka, ime, prezime, uloga, pasos,drzavljanstvo,telefon,email,pol))
            return svi_korisnici
        del svi_korisnici[staro_korisnicko_ime]
        svi_korisnici.update(podesi_korisnika(korisnicko_ime, lozinka, ime, prezime, uloga, pasos,drzavljanstvo,telefon,email,pol))
        return svi_korisnici
    else:
        if korisnicko_ime in svi_korisnici:
            raise izuzeci.ZauzetoKorisnickoIme(f"Greška - Korisnik ({korisnicko_ime}) je zauzeto!")
        svi_korisnici.update(podesi_korisnika(korisnicko_ime, lozinka, ime, prezime, uloga, pasos,drzavljanstvo,telefon,email,pol))
        return svi_korisnici
"""
Funkcija koja čuva podatke o svim korisnicima u fajl na zadatoj putanji sa zadatim separatorom.
"""
def sacuvaj_korisnike(putanja: str, separator: str, svi_korisnici: dict):
    with open(putanja, 'w', newline='') as f:
        csv_pisac = DictWriter(f, ['korisnicko_ime','lozinka','ime','prezime','uloga','pasos','drzavljanstvo','telefon','email','pol'], delimiter = separator)
        for korisnik in svi_korisnici:
            csv_pisac.writerow(svi_korisnici[korisnik])
"""
Funkcija koja učitava sve korisnika iz fajla na putanji sa zadatim separatorom. Kao rezultat vraća učitane korisnike.
"""
def ucitaj_korisnike_iz_fajla(putanja: str, separator: str) -> dict:
    with open(putanja, "r") as f:
        svi_korisnici = dict()
        csv_citac = DictReader(f,['korisnicko_ime','lozinka','ime','prezime','uloga','pasos','drzavljanstvo','telefon','email','pol'], delimiter = separator)
        for korisnik in csv_citac:
            svi_korisnici.update({korisnik['korisnicko_ime']: korisnik})
        return svi_korisnici       
"""
Funkcija koja vraća korisnika sa zadatim korisničkim imenom i šifrom.
CHECKPOINT 1: Vraća string sa greškom ako korisnik nije pronađen.
ODBRANA: Baca grešku sa porukom ako korisnik nije pronađen.
"""
def login(svi_korisnici, korisnik, lozinka) -> dict:
    if korisnik not in svi_korisnici:
        raise izuzeci.NeuspesnoPrijavljivanje(f"Greška - Korisničko ime {korisnik} ne postoji!")
    if svi_korisnici[korisnik]['lozinka'] != lozinka:
        raise izuzeci.NeuspesnoPrijavljivanje(f"Greška - Neispravna lozinka!")
    return svi_korisnici[korisnik]


"""
Funkcija koja vrsi log out
*
"""

def logout(korisnicko_ime: str):
    korisnicko_ime = {}


def registracija(svi_korisnici: dict) -> dict:
    korisnicko_ime = str(input("Korisničko ime: "))
    if korisnicko_ime == "":
        return
    lozinka = str(input("Lozinka: "))
    telefon = str(input("Kontakt telefon: "))
    email = str(input("Email: "))
    ime = str(input("Ime: "))
    prezime = str(input("Prezime: "))
    pasos = input("Pasoš (nije obavezno): ")
    drzavljanstvo = input("Državljanstvo (nije obavezno): ")
    pol = input("Pol (nije obavezno): ")
    povratna_informacija = kreiraj_korisnika(svi_korisnici, False, "korisnik", None, korisnicko_ime, lozinka, ime, prezime, email, pasos, drzavljanstvo, telefon, pol)

    print("Uspešna registracija")
    return povratna_informacija
    
def prijava(svi_korisnici: dict) -> dict:
    while True:
        interfejsi.prijava()
        korisnicko_ime = str(input("Korisničko ime: "))
        if korisnicko_ime == "":
            return        
        lozinka = str(input("Lozinka: "))
        prijavaljeni_korisnik = login(svi_korisnici, korisnicko_ime, lozinka)
        
            
        print("Uspešna prijava!")
        return prijavaljeni_korisnik
        


