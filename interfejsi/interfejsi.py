from os import system
from time import sleep
from izuzeci import izuzeci
from korisnici import korisnici
from common import konstante
from letovi import letovi

def pocetna_strana():   
    system('cls')
    print("-------------------------------" )
    print("PRODAJA AVIONSKIH KARATA")
    print("-------------------------------")
    print("1. Registruj se")
    print("2. Prijavi se")
    print("3. Pregled letova")
    print("4. Pretraga letova")
    print("5. Izlazak")

def prijava_interfejs():
    system("cls")
    print("-------------------------------")
    print("Unesite korisničko ime i lozinku.")
    print("Pritisnite enter za povratak na početnu stranu.")
    print("-------------------------------")            

def filteri_za_pretragu_letova():
    system("cls")
    print("-------------------------------")
    print("Unesite filtere za pretragu.")
    print("-------------------------------")            

def adminski_pocetni_interfejs(korisnik: dict):
    system('cls')
    print("-------------------------------")
    print(f"Dobrodošao, {korisnik['korisnicko_ime']}!")
    print("-------------------------------")
    print(f"ULOGA: {korisnik['uloga'].capitalize()}")
    print("-------------------------------")
    print("A: Adminske komande")
    print("K: Korisničke komande")
    print("X: Odjava")
    
def prodavacki_interfejs(korisnik: dict):
    pass

def korisnicki_interfejs(korisnik: dict):
    system('cls')
    print("-------------------------------")
    print(f"Dobrodošao, {korisnik['korisnicko_ime']}!")
    print("-------------------------------")
    print(f"ULOGA: {korisnik['uloga'].capitalize()}")
    print("-------------------------------")
    print("1. Pregled letova")
    print("2. Pretraga letova")
    print("3. Kupovina karata")
    print("4. Prijava na let")
    print("5. Nazad")