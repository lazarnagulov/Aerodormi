from common import konstante
from csv import DictReader, DictWriter

def podesi_korisnika(korisnik: str, lozinka: str, ime: str, prezime: str,
                      uloga: str, pasos: str = "", drzavljanstvo: str = "",
                      telefon: str = "", email: str = "", pol: str = "") -> dict:
    
    svi_korisnici = dict()
    svi_korisnici.update({korisnik : {}})
    svi_korisnici[korisnik]['korisnicko_ime'] = korisnik
    svi_korisnici[korisnik]['lozinka'] = lozinka
    svi_korisnici[korisnik]['ime'] = ime
    svi_korisnici[korisnik]['prezime'] = prezime
    svi_korisnici[korisnik]['uloga'] = uloga
    svi_korisnici[korisnik]['pasos'] = pasos 
    svi_korisnici[korisnik]['drzavljanstvo'] = drzavljanstvo
    svi_korisnici[korisnik]['telefon'] = telefon 
    svi_korisnici[korisnik]['email'] = email
    svi_korisnici[korisnik]['pol'] = pol

    return svi_korisnici

def validacija(korisnik: str, lozinka: str, ime: str, prezime: str,
                      uloga: str, pasos: str = "",
                      telefon: str = "", email: str = "") -> bool:
    if email == "" or email == None or ime == "" or ime == None or prezime == "" or prezime == None or korisnik == None or korisnik == "" or lozinka == None or lozinka == "" or uloga == None or uloga == "":
        print("Fali nešto!")
        return False
    if email != "" and email != None:
        if "@" not in email:
            print(f"Neispravan email:{email}")
            return False
        else:
            _, domen = str(email).split("@")
            if domen.count(".") != 1:
                print(f"Neispravan email:{email}")
                return False
    if uloga != konstante.ULOGA_ADMIN and uloga != konstante.ULOGA_KORISNIK and uloga != konstante.ULOGA_PRODAVAC:
        print("Nepostojeća uloga")
        return False
    if pasos != "" and pasos != None:
        if len(str(pasos)) != 9 or not str(pasos).isnumeric():
            print(f"Neispravan pasoš:{pasos}")
            return False
    if telefon != "" and pasos != None:
        if not str(telefon).isnumeric():
            print(f"Neispravan broj telefona:{telefon}")
            return False
    
    return True

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
    if not validacija(korisnicko_ime, lozinka, ime, prezime, uloga, pasos, telefon, email):
        return "Neuspešna validacija podataka!"
    if azuriraj:
        if staro_korisnicko_ime != None:
            if korisnicko_ime in svi_korisnici.keys():
                return "Neuspešno ažuriranje! Korisničko ime već postoji!"
            if staro_korisnicko_ime not in svi_korisnici.keys():
                return "Korisničko ime ne postoji!"
            del svi_korisnici[staro_korisnicko_ime]
            svi_korisnici.update(podesi_korisnika(korisnicko_ime, lozinka, ime, prezime, uloga, pasos, drzavljanstvo, telefon, email, pol))
        else:
            if korisnicko_ime not in svi_korisnici.keys():
                return "Korisničko ime ne postoji!"
            svi_korisnici.update(podesi_korisnika(korisnicko_ime, lozinka, ime, prezime, uloga, pasos, drzavljanstvo, telefon, email, pol))
        return svi_korisnici
    else:
        if korisnicko_ime in svi_korisnici.keys():
            return "Korisničko ime već postoji!"
        svi_korisnici.update(podesi_korisnika(korisnicko_ime, lozinka, ime, prezime, uloga, pasos,drzavljanstvo,telefon,email,pol))
        return svi_korisnici
"""
Funkcija koja čuva podatke o svim korisnicima u fajl na zadatoj putanji sa zadatim separatorom.
"""
def sacuvaj_korisnike(putanja: str, separator: str, svi_korisnici: dict):
    with open(putanja, 'w') as f:
        csv_pisac = DictWriter(f, ['korisnicko_ime','lozinka','ime','prezime','uloga','pasos','drzavljanstvo','telefon','email','pol'], delimiter = separator)
        for korisnik in svi_korisnici:
            csv_pisac.writerow(svi_korisnici[korisnik])
"""
Funkcija koja učitava sve korisnika iz fajla na putanji sa zadatim separatorom. Kao rezultat vraća učitane korisnike.
"""
def ucitaj_korisnike_iz_fajla(putanja: str, separator: str) -> dict:
    with open(putanja, "r") as f:
        svi_korisnici = dict()
        csv_citac = DictReader(f,['korisnicko_ime','lozinka','ime','prezime','uloga','pasos','drzavljanstvo','telefon','email','pol'], delimiter=separator)
        for korisnik in csv_citac:
            svi_korisnici.update({korisnik['korisnicko_ime']: korisnik})
        return svi_korisnici       
"""
Funkcija koja vraća korisnika sa zadatim korisničkim imenom i šifrom.
CHECKPOINT 1: Vraća string sa greškom ako korisnik nije pronađen.
ODBRANA: Baca grešku sa porukom ako korisnik nije pronađen.
"""
def login(svi_korisnici, korisnik, lozinka) -> dict:
    if korisnik not in svi_korisnici.keys():
        return "Korisničko ime nije pronađeno!"
    if svi_korisnici[korisnik]['lozinka'] != lozinka:
        return "Pogrešna lozinka!"
    return svi_korisnici[korisnik]

def registruj(svi_korisnici: dict):
    while True:
        korisnicko_ime = str(input("Korisničko ime: "))
        lozinka = str(input("Lozinka: "))
        telefon = str(input("Kontakt telefon: "))
        email = str(input("Email: "))
        ime = str(input("Ime: "))
        prezime = str(input("Prezime: "))
        pasos = 111111111
        drzavljanstvo = "< drzavljanstvo >"
        pol = "< pol >"
        povratna_informacija = kreiraj_korisnika(svi_korisnici, False, "korisnik", None, korisnicko_ime, lozinka, ime, prezime, email, pasos, drzavljanstvo, telefon, pol)
        if type(povratna_informacija) == dict:
            print("-------------------------------")
            print("Uspešna registracija")
            print("-------------------------------")
            sacuvaj_korisnike("../korisnici.csv", ',', svi_korisnici)
            return povratna_informacija
        else:
            print(povratna_informacija)