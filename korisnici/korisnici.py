from common import konstante
from csv import DictReader, DictWriter
from izuzeci import izuzeci

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

def validacija(korisnik: str, lozinka: str, ime: str, prezime: str,
                      uloga: str, pasos: str = "",
                      telefon: str = "", email: str = "") -> bool:
    if telefon == "" or telefon == None or email == "" or email == None or ime == "" or ime == None or prezime == "" or prezime == None or korisnik == None or korisnik == "" or lozinka == None or lozinka == "" or uloga == None or uloga == "":
        # raise izuzeci.NepostojeciPodaci("Greška - Obavezni podaci nisu pravilno uneti!")
        return False
        
    if email != "" and email != None:
        if "@" not in email:
            # raise izuzeci.NeispravanEmail(f"Greška - Email ({email}) ne sadrži @!")
            return False
        else:
            _, domen = str(email).split("@")
            if domen.count(".") != 1:
                # raise izuzeci.NeispravanEmail(f"Greška - Email ({email}) sadrži više od jednog domena!")
                return False
    if uloga not in [konstante.ULOGA_ADMIN, konstante.ULOGA_KORISNIK, konstante.ULOGA_PRODAVAC]:
        # raise izuzeci.NepostojecaUloga(f"Greška - Uloga {uloga} ne postoji!")
        return False
    if pasos != "" and pasos != None:
        if not str(pasos).isnumeric():
            # raise izuzeci.NeispravanPasos(f"Greška - Pasoš ({pasos}) nije numerički string!")
            return False
        if len(str(pasos)) != 9 or not str(pasos).isnumeric():
            # raise izuzeci.NeispravanPasos(f"Greška - Pasoš ({pasos}) ne sadrži 9 cifara!")
            return False
            
    if telefon != "" and telefon != None and not str(telefon).isnumeric():
            # raise izuzeci.NeispravanTelefon(f"Greška - Telefon ({telefon}) nije numerički string!")
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
        if staro_korisnicko_ime not in svi_korisnici:
            # raise izuzeci.NepostojeceKorisnickoIme(f"Greška - Korisnik {staro_korisnicko_ime} ne postoji!")
            return "Korisnik ne postoji"
        if staro_korisnicko_ime != korisnicko_ime:
            # raise izuzeci.ZauzetoKorisnickoIme(f"Greška - Korisnik ({korisnicko_ime}) je zauzeto!")
            return "Korisničko ime je zauzeto"
        else:
            svi_korisnici.update(podesi_korisnika(korisnicko_ime, lozinka, ime, prezime, uloga, pasos,drzavljanstvo,telefon,email,pol))
            return svi_korisnici
        del svi_korisnici[staro_korisnicko_ime]
        svi_korisnici.update(podesi_korisnika(korisnicko_ime, lozinka, ime, prezime, uloga, pasos,drzavljanstvo,telefon,email,pol))
        return svi_korisnici
    else:
        if korisnicko_ime in svi_korisnici:
            # raise izuzeci.ZauzetoKorisnickoIme(f"Greška - Korisnik ({korisnicko_ime}) je zauzeto!")
            return "Korisničko ime je zauzeto"

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
    if korisnik not in svi_korisnici.keys():
        # raise izuzeci.NeuspesnoPrijavljivanje(f"Greška - Korisničko ime {korisnik} ne postoji!")
        return "Korisničko ime ne postoji!"
    if svi_korisnici[korisnik]['lozinka'] != lozinka:
        # raise izuzeci.NeuspesnoPrijavljivanje(f"Greška - Neispravna lozinka!")
        return "Pogrešna sifra!"
    return svi_korisnici[korisnik]

