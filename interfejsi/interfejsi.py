from os import system

def pocetna_strana():   
    system('cls')
    print("-------------------------------" )
    print("PRODAJA AVIONSKIH KARATA")
    print("-------------------------------")
    print("1: Registruj se")
    print("2: Prijavi se")
    print("3: Pregled letova")
    print("4: Pretraga letova")
    print("5: 10 najjeftinijih letova")
    print("6: Polasci")
    print("X: Izlazak")

def odabir_putnika():
    system("cls")
    print("-------------------------------" )
    print("Kupujem kartu za:")
    print("-------------------------------" )
    print("1: Sebe")
    print("2: Drugu osobu")
    print("X: Nazad")

def nastavak_kupovine():
    system('cls')
    print("-------------------------------" )
    print("Nastavak kupovine za:")
    print("-------------------------------" )
    print("1: Sledeću kartu")
    print("2: Saputnika")
    print("X: Nazad")
    
    
def nastavak_kupovine_sledece_karte():
    system('cls')
    print("-------------------------------" )
    print("KUPOVINA SLEDEĆE KARTE")
    print("-------------------------------" )
    print("1: Unesite šifru leta")
    print("2: Pretraga letova")
    print("X: Nazad")
    

def potrvda_kupovine():
    system('cls')
    print("-------------------------------" )
    print("Potvrda kupovine:")
    print("-------------------------------" )
    print("1: Kupi kartu")
    print("X: Nazad")
    
def prijava_na_let():
    system('cls')
    print("-------------------------------" )
    print("Prijava na let")
    print("-------------------------------" )
    print("1: Unesite broj karte")
    print("2: Prikažu kopljene karte")
    print("3: Pretraga karata")
    print("X: Nazad")

def prijava():
    system("cls")
    print("-------------------------------")
    print("Unesite korisničko ime i lozinku.")
    print("Pritisnite enter za povratak na početnu stranu.")
    print("-------------------------------")            

def kupovina_karata():
    system("cls")
    print("-------------------------------")
    print("KUPOVINA KARATA")
    print("-------------------------------")
    print("1: Unesite šifru leta")
    print("2: Pretraga konkretnih letova")    
    print("X: Nazad")

def registracija():
    system("cls")
    print("-------------------------------")
    print("Unesite Vaše podatke.")
    print("Pritisnite enter za povratak na početnu stranu.")
    print("-------------------------------")

def filteri_za_pretragu_letova():
    system("cls")
    print("-------------------------------")
    print("Unesite filtere za pretragu.")
    print("-------------------------------")            

def adminski_pocetni(korisnik: dict):
    system('cls')
    print("-------------------------------")
    print(f"Dobrodošao, {korisnik['korisnicko_ime']}!")
    print("-------------------------------")
    print(f"ULOGA: {korisnik['uloga'].capitalize()}")
    print("-------------------------------")
    print("A: Adminske komande")
    print("K: Korisničke komande")
    print("X: Odjava")

def pretraga_karata():
    pass

def registracija_novog_prodavca():
    pass

def kreiranje_letova():
    pass

def izvestaji():
    pass


def adminski(korisnik: dict):
    system('cls')
    print("-------------------------------")
    print(f"Dobrodošao, {korisnik['korisnicko_ime']}!")
    print("-------------------------------")
    print(f"ULOGA: {korisnik['uloga'].capitalize()}")
    print("-------------------------------")
    print("1: Pretraga prodatih karata")
    print("2: Registracija novih prodavaca")
    print("3: Kreiranje letova")
    print("4: Izmena letova")
    print("5: Brisanje karata")
    print("6: Izveštaji")
    print("X: Nazad")
    
def prodavacki(korisnik: dict):
    system('cls')
    print("-------------------------------")
    print(f"Dobrodošao, {korisnik['korisnicko_ime']}!")
    print("-------------------------------")
    print(f"ULOGA: {korisnik['uloga'].capitalize()}")
    print("-------------------------------")
    print("1: Prodaj kartu")
    print("2: Prijava na let")
    print("3: Izmeni kartu")
    print("4: Obriši kartu")
    print("5: Pretraga prodatih karata")
    print("X: Nazad")
    
    
    
def korisnicki(korisnik: dict):
    system('cls')
    print("-------------------------------")
    print(f"Dobrodošao, {korisnik['korisnicko_ime']}!")
    print("-------------------------------")
    print(f"ULOGA: {korisnik['uloga'].capitalize()}")
    print("-------------------------------")
    print("1: Pregled letova")
    print("2: Pretraga letova")
    print("3: Kupovina karata")
    print("4: Prijava na let")
    print("5: 10 najjeftinijih letova")
    print("6: Polasci")
    print("7: Prikaži kupljene karte")
    print("X: Nazad")