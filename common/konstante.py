zaglavlja_konkretni_letovi = ['Sifra', 'Let', 'Polazak', 'Dolazak', 'Polazište', 'Odredište', 'Cena']
zaglavlja_letovi = ['Sifra', 'Polazište', 'Odredište', "Vreme poletanja", "Vreme sletanja", "Prevoznik", "Cena"]
zaglavlja_karte = ['Broj karte', 'Let', 'Polazište', 'Odredište', 'Polazak', 'Dolazak']

ZAGLAVLJE_KONKRETNI_LETOVI = lambda: print(f"{zaglavlja_konkretni_letovi[0]: <10}{zaglavlja_konkretni_letovi[1]: <10}{zaglavlja_konkretni_letovi[2]: <20}{zaglavlja_konkretni_letovi[3]: <20}{zaglavlja_konkretni_letovi[4]: <10}{zaglavlja_konkretni_letovi[5]: <10}{zaglavlja_konkretni_letovi[6]: <10}")
ZAGLAVLJE_LETOVI = lambda: print(f"{zaglavlja_letovi[0]: <10}{zaglavlja_letovi[1]: <10}{zaglavlja_letovi[2]: <10}{zaglavlja_letovi[3]: <20}{zaglavlja_letovi[4]: <20}{zaglavlja_letovi[5]: <30}{zaglavlja_letovi[6]: <5}")
ZAGLAVLJE_KARTE = lambda: print(f"{zaglavlja_karte[0]: <20}{zaglavlja_karte[1]: <10}{zaglavlja_karte[2]: <20}{zaglavlja_karte[3]: <20}{zaglavlja_karte[4]: <30}{zaglavlja_karte[5]: <30}")

ULOGA_KORISNIK = "korisnik"
ULOGA_PRODAVAC = "prodavac"
ULOGA_ADMIN = "admin"

PUTANJA_KORISNICI = "./podaci/korisnici.csv"
PUTANJA_LETOVI = "./podaci/letovi.csv"
PUTANJA_KARTE = "./podaci/karte.csv"
PUTANJA_KONKRETNI_LETOVI = "./podaci/konkretni_letovi.csv"
PUTANJA_MODELI_AVIONA = "./podaci/modeli_aviona.csv"
PUTANJA_AERODROMI = "./podaci/aerodromi.csv"

MAX_SEC = 86399

FORMAT_DATETIME = "%Y-%m-%d %H:%M:%S"
FORMAT_DATETIME_BEZ_SEKUNDI = "%Y-%m-%d %H:%M"
FORMAT_DATE = "%Y-%m-%d"

STATUS_NEREALIZOVANA_KARTA = "nerealizovana"
STATUS_REALIZOVANA_KARTA = "realizovana"

PONEDELJAK = 0
UTORAK = 1
SREDA = 2
CETVRTAK = 3
PETAK = 4
SUBOTA = 5
NEDELJA = 6

