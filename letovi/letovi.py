from csv import DictReader, DictWriter
from common import konstante
from izuzeci import izuzeci

"""
Validan let primer:
{
    "ab12":
    {
        'broj_leta': "ab12",
        'polazisni_aerodrom': "123"
        'odredisni_aerodrom': "456",
        'vreme_poletanja': "09:45",
        'vreme_sletanja': "15:45",
        'sletanje_sutra': False,
        'prevoznik': ""
        'dani': [1,2,3,4]
        "model": 
        {
            23345:
            {
                'id': 23345
                'broj_redova': 42
                'pozicija_sedista': ['A', 'B', 'C', 'D'] 
            }
        }
        
    }
}
"""

def podesi_let(broj_leta: str, sifra_polazisnog_aerodroma: str, sifra_odredisnog_aerodroma: str,
                     vreme_poletanja: str, vreme_sletanja: str, sletanje_sutra: bool, prevoznik: str,
                     dani: list, model: dict, cena: int)-> dict:
    
    svi_letovi = dict()
    svi_letovi.update(
        {
            broj_leta : 
            {
                'broj_leta': broj_leta,
                'sifra_polazisnog_aerodroma': sifra_polazisnog_aerodroma,
                'sifra_odredisnog_aerodroma': sifra_odredisnog_aerodroma,
                'vreme_poletanja': vreme_poletanja,
                'vreme_sletanja': vreme_sletanja,
                'sletanje_sutra': sletanje_sutra,
                'prevoznik': prevoznik,
                'dani': dani,
                'model': 
                {
                    'id': model['id'],
                    'naziv': model['naziv'],
                    'broj_redova': model['broj_redova'],
                    'pozicija_sedista': model['pozicija_sedista']       
                },
                'cena': cena
            }
        }
    )
    
    return svi_letovi

def validacija_leta(broj_leta: str, sifra_polazisnog_aerodroma: str, sifra_odredisnog_aerodroma: str,
                     vreme_poletanja: str, vreme_sletanja: str, sletanje_sutra: bool, prevoznik: str,
                     dani: list, model: dict, cena: int):
    if not broj_leta or not sifra_odredisnog_aerodroma or not sifra_polazisnog_aerodroma or not vreme_poletanja or not vreme_sletanja or not sletanje_sutra or not prevoznik or not dani or not model or not cena:
        raise izuzeci.NepostojeciPodaci("Greška - Obavezni podaci nisu pravilno uneti!")
    if not (str(broj_leta[0:2]).isalpha() and str(broj_leta[2:4]).isnumeric()):
        raise izuzeci.NeispravanBrojLeta("Greška - Broj leta mora biti oblika <slovo><slovo><broj><broj>")

def ispis_leta(let: dict):
    pass
"""
Funkcija koja omogucuje korisniku da pregleda informacije o letovima
*mislim da ne mora nista da vraca
todo
"""
def pregled_nerealizovanih_letova(svi_letovi: dict):
    pass

def pretraga_letova(svi_letovi: dict, konkretni_letovi:dict, polaziste: str = "", odrediste: str = "", datum_polaska: str = "",datum_dolaska: str = "",
                    vreme_poletanja: str = "", vreme_sletanja: str = "", prevoznik: str = "")->list:
    pass

def trazenje_10_najjeftinijih_letova(svi_letovi: dict, polaziste: str = "", odrediste: str =""):
    pass

# 7 zad nema sad???
def kreiranje_letova(svi_letovi : dict, broj_leta: str, sifra_polazisnog_aerodroma: str, sifra_odredisnog_aerodroma: str,
                     vreme_poletanja: str, vreme_sletanja: str, sletanje_sutra: bool, prevoznik: str,
                     dani: list, model: dict, cena: int):
    validacija_leta(broj_leta, sifra_polazisnog_aerodroma, sifra_odredisnog_aerodroma, vreme_poletanja, vreme_sletanja, sletanje_sutra, prevoznik, dani, model, cena)
    svi_letovi.update(podesi_let(broj_leta, sifra_polazisnog_aerodroma, sifra_odredisnog_aerodroma, vreme_poletanja, vreme_sletanja, sletanje_sutra, prevoznik, dani, model, cena))
    return svi_letovi

def izmena_letova(svi_letovi : dict, broj_leta: str, sifra_polazisnog_aerodroma: str, sifra_odredisnog_aerodroma: str,
                     vreme_poletanja: str, vreme_sletanja: str, sletanje_sutra: bool, prevoznik: str,
                     dani: list, model: dict, cena: float)-> dict:
    pass

def sacuvaj_letove(putanja: str, separator: str, svi_letovi: dict):
    with open(putanja, 'w', newline='') as f:
        csv_pisac = DictWriter(f, ['broj_leta','sifra_polazisnog_aerodroma','sifra_odredisnog_aerodroma','vreme_poletanja','vreme_sletanja','sletanje_sutra','prevoznik',
                                   'dani', 'model', 'naziv','broj_redova','pozicija_sedista','cena'], delimiter = separator)
        for let in svi_letovi:            
            csv_pisac.writerow({
                'broj_leta': svi_letovi[let]['broj_leta'],
                'sifra_polazisnog_aerodroma': svi_letovi[let]['sifra_polazisnog_aerodroma'],
                'sifra_odredisnog_aerodroma': svi_letovi[let]['sifra_odredisnog_aerodroma'],
                'vreme_poletanja': svi_letovi[let]['vreme_poletanja'],
                'vreme_sletanja': svi_letovi[let]['vreme_sletanja'],
                'sletanje_sutra': svi_letovi[let]['sletanje_sutra'],
                'prevoznik': svi_letovi[let]['prevoznik'],
                'dani': ",".join(str(dan) for dan in svi_letovi[let]['dani']),
                'model': svi_letovi[let]['model']['id'],
                'naziv': svi_letovi[let]['model']['naziv'],
                'broj_redova': int(svi_letovi[let]['model']['broj_redova']),
                'pozicija_sedista': ",".join(str(pozicija) for pozicija in svi_letovi[let]['model']['pozicija_sedista']),
                'cena': float(svi_letovi[let]['cena'])
            })
            
def ucitaj_letove_iz_fajla(putanja: str, separator: str) -> dict:
    with open(putanja, "r") as f:
        svi_letovi = dict()
        csv_citac = DictReader(f, ['broj_leta','sifra_polazisnog_aerodroma','sifra_odredisnog_aerodroma','vreme_poletanja','vreme_sletanja','sletanje_sutra',
                                   'prevoznik','dani','model', 'naziv', 'broj_redova', 'pozicija_sedista','cena'], delimiter = separator)        
        for let in csv_citac:
            dani = [int(dan) for dan in let['dani'].split(",")]
            model = {
                        'id': int(let['model']),
                        'naziv': let['naziv'],
                        'broj_redova': int(let['broj_redova']),
                        'pozicija_sedista': [str(pozicija) for pozicija in let['pozicija_sedista'].split(",")]
                    }
            svi_letovi.update(podesi_let
                (
                    let['broj_leta'], 
                    let['sifra_polazisnog_aerodroma'], 
                    let['sifra_odredisnog_aerodroma'], 
                    let['vreme_poletanja'], 
                    let['vreme_sletanja'], 
                    True if let['sletanje_sutra'] == 'True' else False, 
                    let['prevoznik'], 
                    dani, 
                    model, 
                    float(let['cena'])
                )
            )
        
        return svi_letovi      
