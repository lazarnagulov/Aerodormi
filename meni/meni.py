from os import system
from time import sleep

from izuzeci import izuzeci
from common import konstante
from interfejsi import interfejsi

from datetime import datetime, timedelta
from korisnici import korisnici
from letovi import letovi
from aerodromi import aerodromi
from model_aviona import model_aviona
from konkretni_letovi import konkretni_letovi
from karte import karte
from izvestaji import izvestaji

svi_korisnici = dict()
sve_karte = dict()
svi_letovi = dict()
svi_konkretni_letovi = dict()
svi_aerodromi = dict()
svi_modeli_aviona = dict()

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
    for let in filtrirani_letovi:
        letovi.ispis_leta(let)

    while True:
        unos = input("Pritisnite enter da biste nastavili. ")
        if unos == "":
            return

# -------------------- CHECKIN -------------------- #

def prijava_na_let():
    global korisnik, svi_konkretni_letovi, sve_karte, svi_korisnici
    
    putnici = list()
    
    def odabir_sedista(putnici: list, sifra_karte: int):
        konkretan_let = svi_konkretni_letovi[sve_karte[sifra_karte]['sifra_konkretnog_leta']]
        zauzetost = konkretan_let['zauzetost']
        
        print(zauzetost)
                
        red = int(input("Unesite red sedišta: "))
        pozicija = input("Unesite poziciju sedišta: ")
        letovi.checkin(sve_karte[sifra_karte], svi_letovi, konkretan_let, red, pozicija)
        
    while True:
        unos = input(">> ")
        if unos == "1":
            broj_karte = int(input("Unesite broj karte: "))
            
            if broj_karte not in sve_karte:
                print("Karta ne postoji")
                continue
            
            if korisnik not in sve_karte[broj_karte]['putnici']:
                print("Korisnik nema kartu")
            else:      
                if not korisnik.get('pasos'):
                    pasos = input("Unesite broj pasoša: ")
                    korisnik['pasos'] = pasos
                if not korisnik.get('drzavljanstvo'):
                    drzavljanstvo = input("Unesite državljanstvo: ")
                    korisnik['drzavljanstvo'] = drzavljanstvo
                if not korisnik.get('pol'):
                    pol = input("Unesite pol: ")
                    korisnik['pol'] = pol 
                
                if korisnik not in putnici:
                    putnici.append(korisnik)
                
                odabir_sedista(putnici, broj_karte)
        elif unos == "2":
            print(karte.pregled_nerealizovanaih_karata(korisnik, [sve_karte[karta] for karta in sve_karte]))
            while True:
                kraj = input("Pritisnite enter.")
                if kraj == "":
                    break
        elif unos == "X":
            return
        else:
            print("Nepostojeća komanda")

        interfejsi.prijava_na_let()
        

# -------------------- KARTE -------------------- #

# TODO: pretraga_karata(): Datume treba pretvoriti u datetime (ili to raditi u pretraga_karata)

def izmena_karte():
    global izmena_karte, sve_karte
    
    while True:
        unos = input(">> ")
        
        if unos == "1":
            broj_karte = int(input("Unestite broj karte: "))
            karte.izmena_karte(sve_karte, svi_konkretni_letovi, broj_karte)
        elif unos == "2":
            interfejsi.pretraga_karata()
            pretraga_karata()
        elif unos == "X":
            return
        else:
            print("Nepostojeća komanda")
            sleep(0.5)

    interfejsi.izmena_karte()

def brisanje_karata():
    global korisnik, sve_karte
    
    while True:
        unos = input(">> ")
        
        if unos == "1":
            broj_karte = int(input("Unestite broj karte: "))
            karte.brisanje_karte(korisnik, sve_karte, broj_karte)
        elif unos == "2":
            interfejsi.pretraga_karata()
            pretraga_karata()
        elif unos == "X":
            return
        else:
            print("Nepostojeća komanda")
            sleep(0.5)
        interfejsi.brisanje_karte()

def pretraga_karata():
    global svi_letovi, svi_konkretni_letovi, karte

    polaziste = input("Unesite polazište: ")
    odrediste = input("Unesite odredište: ")
    datum_polaska = input("Unesite datum polaska: ")
    datum_dolaska = input("Unesite datum dolaska: ")
    datum_polaska = datetime.strptime(datum_polaska, konstante.FORMAT_DATETIME)
    datum_dolaska = datetime.strptime(datum_dolaska, konstante.FORMAT_DATETIME)
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


def prodaja_karte():
       
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

        interfejsi.prodaja_karte()


def odabir_putnika(sifra_konkretnog_leta: int):
    global korisnik, svi_korisnici
    
    putnici = list()
    kupac = dict()
    potvrda = False
    

    while True:
        unos = input(">> ")
        if unos == "1":
            if korisnik['uloga'] == konstante.ULOGA_KORISNIK:
                if korisnik not in putnici:
                    putnici.append(korisnik)

                interfejsi.potvrda_kupovine()
                potvda = potvrda_kupovine(sifra_konkretnog_leta, putnici)
            elif korisnik['uloga'] == konstante.ULOGA_PRODAVAC:
                korisnicko_ime = input("Korisničko ime putnika: ")
                if korisnicko_ime in svi_korisnici:
                    putnici.append(svi_korisnici[korisnicko_ime])
                    kupac = korisnicko_ime
                    interfejsi.potvrda_prodaje()
                    potvrda = potvrda_prodaje(sifra_konkretnog_leta, putnici, svi_korisnici[kupac])
                else:
                    print("Korisničko ime ne postoji!")
                    sleep(3)
            if potvrda:
                if korisnik['uloga'] == konstante.ULOGA_KORISNIK:
                    interfejsi.npotvrda_kupovine_sledece_karte()
                    kupovina_sledece(sifra_konkretnog_leta)
                elif korisnik['uloga'] == konstante.ULOGA_PRODAVAC:
                    pass
                return
        elif unos == "2":
            ime = input("Ime putnika: ")
            prezime = input("Prezime putnika: ")
            if {'ime': ime, 'prezime': prezime} not in putnici:
                putnici.append({'ime': ime, 'prezime': prezime})

            if korisnik['uloga'] == konstante.ULOGA_KORISNIK:            
                interfejsi.potvrda_kupovine()
                potvrda = potvrda_kupovine(sifra_konkretnog_leta, putnici)
            elif korisnik['uloga'] == konstante.ULOGA_PRODAVAC:
                interfejsi.potvrda_prodaje()
                potvrda = potvrda_prodaje(sifra_konkretnog_leta, putnici, svi_korisnici[kupac])
            if potvrda:
                interfejsi.npotvrda_kupovine_sledece_karte()
                kupovina_sledece(sifra_konkretnog_leta)
                return

        elif unos == "X":
            return
        else:
            print("Nepostojeća komanda!")
            sleep(0.5)
        interfejsi.odabir_putnika()

def kupovina_sledece(sifra_konkretnog_leta: int):
    global svi_letovi, svi_konkretni_letovi
    
    interfejsi.kupovina_sledece()
    unos = input(">> ")
    if unos == "1":
        moguci_letovi = karte.kupovina_sledece_karte(svi_letovi, svi_konkretni_letovi, sifra_konkretnog_leta)
        print(moguci_letovi)

        if moguci_letovi == []:
            print("Ne postoje sledeći letovi!")
            sleep(3)
            return

        while True:
            sifra_narednog_leta = input("Unesite šifru narednog leta: ")
            if sifra_narednog_leta in moguci_letovi:
                interfejsi.odabir_putnika()
                odabir_putnika(sifra_narednog_leta)
            if sifra_narednog_leta == "":
                return
    elif unos == "2":
        return

def potvrda_kupovine(sifra_konkretnog_leta: int, putnici: list) -> bool:
        print(f"Putnici: \n{putnici}")
        unos = input(">> ")
        if unos == "1":
            slobodna_mesta = list()
            try:
                slobodna_mesta = svi_konkretni_letovi[sifra_konkretnog_leta]['zauzetost']
            except:
                slobodna_mesta = letovi.podesi_matricu_zauzetosti(
                    svi_letovi, svi_konkretni_letovi[sifra_konkretnog_leta])
            karta = karte.kupovina_karte(sve_karte, svi_konkretni_letovi, sifra_konkretnog_leta, putnici, slobodna_mesta, korisnik)
            return True
        elif unos == "X":
            return False
        else:
            print("Nepostojeća komanda")

def potvrda_prodaje(sifra_konkretnog_leta: int, putnici: list, kupac: dict) -> bool:
        global korisnik
        print(f"Putnici: \n{putnici}")
        unos = input(">> ")
        if unos == "1":
            slobodna_mesta = list()
            try:
                slobodna_mesta = svi_konkretni_letovi[sifra_konkretnog_leta]['zauzetost']
            except:
                slobodna_mesta = letovi.podesi_matricu_zauzetosti(
                    svi_letovi, svi_konkretni_letovi[sifra_konkretnog_leta])
            karta = karte.kupovina_karte(sve_karte, svi_konkretni_letovi, sifra_konkretnog_leta, putnici, slobodna_mesta, kupac, prodavac = korisnik)
            return True
        elif unos == "X":
            return False
        else:
            print("Nepostojeća komanda")


def kupovina_karte():
    global korisnik, sve_karte, svi_konkretni_letovi, svi_letovi

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
            print(karte.pregled_nerealizovanaih_karata(korisnik, sve_karte))            
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
            interfejsi.prijava_na_let()
            prijava_na_let()
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
            polaziste = input("Unesite polazište: ")
            odrediste = input("Unesite odredište: ")
            datum = input("Unesite datum: ")
            datum = datetime.strptime(datum, "%Y-%m-%d")
            broj_fleksibilnih_dana = int(input("Unesite broj fleksibilnih dana: "))
                        
            print(letovi.fleksibilni_polasci(svi_letovi, svi_konkretni_letovi, polaziste, odrediste, datum, broj_fleksibilnih_dana, None))
            while True:
                kraj = input("Pritisnite enter.")
                if kraj == "":
                    break
        elif unos == "7":
            print(karte.pregled_nerealizovanaih_karata(korisnik, [sve_karte[karta] for karta in sve_karte]))
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

def prijavljeni_prodavac():
    global korisnik

    while True:
        unos = input(">> ")
        if unos == "1":
            interfejsi.prodaja_karte()
            prodaja_karte()
        elif unos == "2":
            interfejsi.prijava_na_let()
            prijava_na_let()
        elif unos == "3":
            interfejsi.izmena_karte()
            izmena_karte()
        elif unos == "4":
            interfejsi.brisanje_karte()
            brisanje_karata()
        elif unos == "5":
            pass  # pretraga prodatih karata
        elif unos == "X":
            return
        else:
            print("Nepostojeća komanda!")
            sleep(0.5)
        interfejsi.prodavacki(korisnik)

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
            interfejsi.brisanje_karte()
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

def pocetna_strana():
    global svi_korisnici, korisnik, svi_konkretni_letovi, svi_letovi, svi_aerodromi, svi_modeli_aviona

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
            print(letovi.pregled_nerealizovanih_letova(svi_letovi))
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
            print(letovi.trazenje_10_najjeftinijih_letova(svi_letovi, polaziste, odrediste))
            while True:
                kraj = input("Pritisnite enter.")
                if kraj == "":
                    break
        elif unos == "6":
            polaziste = input("Unesite polazište: ")
            odrediste = input("Unesite odredište: ")
            datum = input("Unesite datum: ")
            datum = datetime.strptime(datum, "%Y-%m-%d")
            broj_fleksibilnih_dana = int(input("Unesite broj fleksibilnih dana: "))
                        
            print(letovi.fleksibilni_polasci(svi_letovi, svi_konkretni_letovi, polaziste, odrediste, datum, broj_fleksibilnih_dana, None))
            while True:
                kraj = input("Pritisnite enter.")
                if kraj == "":
                    break
        elif unos == "X":
            print("Izlazak iz aplikacije...")
            korisnici.sacuvaj_korisnike(konstante.PUTANJA_KORSINICI, ",", svi_korisnici)
            karte.sacuvaj_karte(sve_karte, konstante.PUTANJA_KARTE, ",")
            letovi.sacuvaj_letove(konstante.PUTANJA_LETOVI, ",", svi_letovi)
            konkretni_letovi.sacuvaj_kokretan_let(konstante.PUTANJA_KONKRETNI_LETOVI, ",", svi_konkretni_letovi)
            aerodromi.sacuvaj_aerodrome(konstante.PUTANJA_AERODROMI, ",", svi_aerodromi)
            model_aviona.sacuvaj_modele_aviona(konstante.PUTANJA_MODELI_AVIONA, ",", svi_modeli_aviona)
            return
        else:
            print("Nepostojeća komanda")
            sleep(0.5)

        interfejsi.pocetna_strana()

def inicializacija():
    global svi_konkretni_letovi, svi_korisnici, sve_karte, svi_letovi

    svi_korisnici = korisnici.ucitaj_korisnike_iz_fajla(konstante.PUTANJA_KORSINICI, ",")
    sve_karte = karte.ucitaj_karte_iz_fajla(konstante.PUTANJA_KARTE, ",")
    svi_letovi = letovi.ucitaj_letove_iz_fajla(konstante.PUTANJA_LETOVI, ",")
    svi_konkretni_letovi = konkretni_letovi.ucitaj_konkretan_let(konstante.PUTANJA_KONKRETNI_LETOVI, ",")
    svi_aerodromi = aerodromi.ucitaj_aerodrom(konstante.PUTANJA_AERODROMI, ",")
    svi_modeli_aviona = model_aviona.ucitaj_modele_aviona(konstante.PUTANJA_MODELI_AVIONA, ",")

    interfejsi.pocetna_strana()
    pocetna_strana()
