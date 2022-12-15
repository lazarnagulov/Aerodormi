from csv import DictReader, DictWriter
from common import konstante
from izuzeci import izuzeci
from operator import itemgetter
from datetime import datetime, timedelta


sifra_konkretnog_leta = 1000


def podesi_let(broj_leta: str, sifra_polazisnog_aerodroma: str, sifra_odredisnog_aerodorma: str,
               vreme_poletanja: str, vreme_sletanja: str, datum_pocetka_operativnosti: datetime, datum_kraja_operativnosti: datetime, sletanje_sutra: bool, prevoznik: str,
               dani: list, model: dict, cena: int) -> dict:
    svi_letovi = dict()
    svi_letovi.update(
        {
            broj_leta:
            {
                'broj_leta': broj_leta,
                'sifra_polazisnog_aerodroma': sifra_polazisnog_aerodroma,
                'sifra_odredisnog_aerodorma': sifra_odredisnog_aerodorma,
                'vreme_poletanja': vreme_poletanja,
                'vreme_sletanja': vreme_sletanja,
                'sletanje_sutra': sletanje_sutra,
                'datum_pocetka_operativnosti': datum_pocetka_operativnosti,
                'datum_kraja_operativnosti': datum_kraja_operativnosti,
                'prevoznik': prevoznik,
                'dani': dani,
                'model':
                {
                    'id': model['id'],
                    'naziv': model['naziv'],
                    'broj_redova': model['broj_redova'],
                    'pozicije_sedista': model['pozicije_sedista']
                },
                'cena': cena
            }
        }
    )

    return svi_letovi


def validacija_leta(broj_leta: str, sifra_polazisnog_aerodroma: str, sifra_odredisnog_aerodorma: str,
                    vreme_poletanja: str, vreme_sletanja: str,  sletanje_sutra: bool, prevoznik: str,
                    dani: list, model: dict, cena: int):
    if not broj_leta or not sifra_odredisnog_aerodorma or not sifra_polazisnog_aerodroma or not vreme_poletanja or not vreme_sletanja or sletanje_sutra == "" or not prevoznik or not dani or not model or not cena:
        raise izuzeci.NepostojeciPodaci(
            "Greška - Obavezni podaci nisu pravilno uneti!")
    if len(sifra_odredisnog_aerodorma) != 3 or len(sifra_polazisnog_aerodroma) != 3:
        raise izuzeci.NeispravnoUnetiPodaci(
            "Greška - Šifre aerodroma ne poštuju IATA.")
    if not (str(broj_leta[0:2]).isalpha() and str(broj_leta[2:4]).isnumeric()) and len(broj_leta) > 4:
        raise izuzeci.NeispravanBrojLeta(
            f"Greška - Broj leta mora biti oblika <slovo><slovo><broj><broj>. ({broj_leta})")
    try:
        sletanje_sati, sletanje_minuti = vreme_sletanja.split(":")
        poletanje_sati, poletanje_minuti = vreme_poletanja.split(":")
        if int(sletanje_minuti) >= 60 or int(poletanje_minuti) >= 60:
            raise izuzeci.NeispravnoVreme(
                f"Greška - Minuti ne mogu biti veći od 59. ({poletanje_minuti} | {sletanje_minuti})")
        if int(sletanje_sati) >= 24 or int(poletanje_sati) >= 24:
            raise izuzeci.NeispravnoVreme(
                f"Greška - Sati ne mogu biti veći od 23. ({poletanje_sati} | {sletanje_sati})")
    except:
        raise izuzeci.NeispravnoVreme(
            f"Greška - Vreme se unosi u formati hh:mm. ({vreme_poletanja} | {vreme_sletanja})")

    if type(sletanje_sutra) != bool:
        raise izuzeci.NeispravnoUnetiPodaci(
            f"Greška - sletanje_sutra mora biti True ili False. ({sletanje_sutra})")

    if cena < 0:
        raise izuzeci.NeispravnoUnetiPodaci(
            f"Greška - cena mora biti broj veći od 0. ({cena})")


def ispis_leta(let: dict):
    for podatak in let:
        vrednost_podatka = let[podatak]
        if podatak == 'cena':
            print(f"| {vrednost_podatka} |")
            return
        if podatak == 'prevoznik' or podatak == 'model':
            continue
        if podatak == 'sletanje_sutra':
            print("|  Da   ", end="") if vrednost_podatka else print(
                "|  Ne   ", end="")
            continue
        print(f"| {vrednost_podatka} ", end="")


def matrica_zauzetosti(konkretan_let: dict) -> list:
    return konkretan_let['matrica_zauzetosti']


def podesi_matricu_zauzetosti(svi_letovi: dict, konkretan_let: dict) -> list:
    matrica_zauzetosti = list()
    let = svi_letovi[konkretan_let['broj_leta']]
    broj_redova = let['model']['broj_redova']
    pozicije_sedista = let['model']['pozicije_sedista']
    for _ in range(broj_redova):
        matrica_zauzetosti.append(pozicije_sedista)
    konkretan_let['matrica_zauzetosti'] = matrica_zauzetosti
    return matrica_zauzetosti


def checkin(svi_letovi: dict, konkretan_let: dict, red: int, pozicija: list):
    zauzetost = list()

    vreme_vazenja = datetime.now() + timedelta(hours=48)
    if vreme_vazenja > konkretan_let['datum_i_vreme_polaska']:
        raise izuzeci.NeispravnoUnetiPodaci("Greška - Checkin je već prošao")

    if konkretan_let.get(matrica_zauzetosti) == None:
        zauzetost = podesi_matricu_zauzetosti(svi_letovi, konkretan_let)
    else:
        zauzetost = matrica_zauzetosti(konkretan_let)

    ukupan_br_redova = svi_letovi[konkretan_let['broj_leta']
                                  ]['model']['broj_redova']
    if red < 0 or red > ukupan_br_redova:
        raise izuzeci.NeispravnoUnetiPodaci("Greška - Red ne postoji!")

    pozicije_sedista = svi_letovi[konkretan_let['broj_leta']
                                  ]['model']['pozicije_sedista']
    for konkretna_pozicija in pozicija:
        if konkretna_pozicija not in pozicije_sedista:
            raise izuzeci.NeispravnoUnetiPodaci(
                f"Greška - Pozicija ne postoji! ({konkretna_pozicija} -> {pozicije_sedista})")

    for i in range(len(pozicije_sedista)):
        for konkretna_pozicija in pozicija:
            if konkretna_pozicija == zauzetost[red][i]:
                if zauzetost[red][i] != 'X':
                    zauzetost[red][i] = 'X'
                else:
                    raise izuzeci.ZauzetoMesto("Greška - mesto je zauzeto!")


"""
Funkcija koja omogucuje korisniku da pregleda informacije o letovima
Ova funkcija sluzi samo za prikaz
"""


def pregled_nerealizovanih_letova(svi_letovi: dict):
    konstante.ZAGLAVLJE_LET()
    for let in svi_letovi:
        ispis_leta(svi_letovi[let])


"""
Funkcija koja omogucava pretragu leta po zadatim kriterijumima. Korisnik moze da zada jedan ili vise kriterijuma.
Povratna vrednost je lista konkretnih letova.
"""


def pretraga_letova(svi_letovi: dict, konkretni_letovi: dict, polaziste: str = "", odrediste: str = "", datum_polaska: str = "", datum_dolaska: str = "",
                    vreme_poletanja: str = "", vreme_sletanja: str = "", prevoznik: str = "") -> list:
    filtrirano = list()
    for konkretan_let in konkretni_letovi:
        let = svi_letovi[konkretni_letovi[konkretan_let]['broj_leta']]
        if datum_polaska == konkretni_letovi[konkretan_let]['datum_i_vreme_polaska'] or datum_polaska == "":
            if datum_dolaska == konkretni_letovi[konkretan_let]['datum_i_vreme_dolaska'] or datum_dolaska == "":
                if let['sifra_odredisnog_aerodorma'] == odrediste or odrediste == "":
                    if let['sifra_polazisnog_aerodroma'] == polaziste or polaziste == "":
                        if let['vreme_poletanja'] == vreme_poletanja or vreme_poletanja == "":
                            if let['vreme_sletanja'] == vreme_sletanja or vreme_sletanja == "":
                                if let['prevoznik'] == prevoznik or prevoznik == "":
                                    filtrirano.append(
                                        konkretni_letovi[konkretan_let])
    return filtrirano


def trazenje_10_najjeftinijih_letova(svi_letovi: dict, polaziste: str = "", odrediste: str = ""):
    filtrirano = list()
    for let in svi_letovi:
        if polaziste == svi_letovi[let]['sifra_polazisnog_aerodroma'] or polaziste == "":
            if odrediste == svi_letovi[let]['sifra_odredisnog_aerodorma'] or odrediste == "":
                filtrirano.append(svi_letovi[let])
    sortirano = sorted(filtrirano, key=lambda l: l['cena'])
    konstante.ZAGLAVLJE_LET()
    if len(sortirano) < 10:
        for let in sortirano:
            ispis_leta(let)
    else:
        i = 0
        while i < 10:
            ispis_leta(let[i])
            i += 1


def kreiranje_konkretnih_letova(svi_letovi: dict,
                                broj_leta: str, datum_pocetka_operativnosti: datetime, datum_kraja_operativnosti: datetime) -> dict:
    global sifra_konkretnog_leta

    datum_dolaska = datum_pocetka_operativnosti
    konkretni_letovi = dict()

    if svi_letovi[broj_leta]['sletanje_sutra']:
        datum_dolaska += timedelta(days=1)

    while datum_kraja_operativnosti >= datum_pocetka_operativnosti:
        konkretni_letovi.update({
            sifra_konkretnog_leta:
                {
                    'sifra': sifra_konkretnog_leta,
                    'broj_leta': broj_leta,
                    'datum_i_vreme_polaska': datum_pocetka_operativnosti,
                    'datum_i_vreme_dolaska': datum_dolaska,
                }
        })
        sifra_konkretnog_leta += 1
        datum_pocetka_operativnosti += timedelta(days=7)
        datum_dolaska += timedelta(days=7)

    return konkretni_letovi


"""
Funkcija koja kreira novi rečnik koji predstavlja let sa prosleđenim vrednostima. Kao rezultat vraća kolekciju
svih letova proširenu novim letom. 
Ova funkcija proverava i validnost podataka o letu. Paziti da kada se kreira let, da se kreiraju i njegovi konkretni letovi.

CHECKPOINT2: Baca grešku sa porukom ako podaci nisu validni.
"""


def kreiranje_letova(svi_letovi: dict, broj_leta: str, sifra_polazisnog_aerodroma: str, sifra_odredisnog_aerodorma: str,
                     vreme_poletanja: str, vreme_sletanja: str, sletanje_sutra: bool, prevoznik: str,
                     dani: list, model: dict, cena: float, datum_pocetka_operativnosti: datetime = None,
                     datum_kraja_operativnosti: datetime = None
                     ) -> dict:
    validacija_leta(broj_leta, sifra_polazisnog_aerodroma, sifra_odredisnog_aerodorma,
                    vreme_poletanja, vreme_sletanja, sletanje_sutra, prevoznik, dani, model, cena)
    svi_letovi.update(podesi_let(broj_leta, sifra_polazisnog_aerodroma, sifra_odredisnog_aerodorma,
                      vreme_poletanja, vreme_sletanja, datum_pocetka_operativnosti, datum_kraja_operativnosti,  sletanje_sutra, prevoznik, dani, model, cena))
    if datum_kraja_operativnosti != None and datum_kraja_operativnosti != None:
        kreiranje_konkretnih_letova(
            svi_letovi, broj_leta, datum_pocetka_operativnosti, datum_kraja_operativnosti)
    return svi_letovi


"""
Funkcija koja menja let sa prosleđenim vrednostima. Kao rezultat vraća kolekciju
svih letova sa promenjenim letom. 
Ova funkcija proverava i validnost podataka o letu.

CHECKPOINT2: Baca grešku sa porukom ako podaci nisu validni.
"""


def izmena_letova(svi_letovi: dict, broj_leta: str, sifra_polazisnog_aerodroma: str, sifra_odredisnog_aerodorma: str,
                  vreme_poletanja: str, vreme_sletanja: str, sletanje_sutra:   bool, prevoznik: str,
                  dani: list, model: dict, cena: float) -> dict:
    if broj_leta not in svi_letovi:
        raise izuzeci.NepostojeciLet("Greška - Broj leta ne postoji.")
    validacija_leta(broj_leta, sifra_polazisnog_aerodroma, sifra_odredisnog_aerodorma,
                    vreme_poletanja, vreme_sletanja, sletanje_sutra, prevoznik, dani, model, cena)
    svi_letovi.update({
        broj_leta:
        {
            'broj_leta': broj_leta,
            'sifra_polazisnog_aerodroma': sifra_polazisnog_aerodroma,
            'sifra_odredisnog_aerodorma': sifra_odredisnog_aerodorma,
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
                    'pozicije_sedista': model['pozicije_sedista']
                },
            'cena': cena
        }
    })
    return svi_letovi


"""
Funkcija koja cuva sve letove na zadatoj putanji
"""


def sacuvaj_letove(putanja: str, separator: str, svi_letovi: dict):
    with open(putanja, 'w', newline='') as f:
        csv_pisac = DictWriter(f, ['broj_leta', 'sifra_polazisnog_aerodroma', 'sifra_odredisnog_aerodorma', 'vreme_poletanja', 'vreme_sletanja', 'datum_pocetka_operativnosti', 'datum_kraja_operativnosti', 'sletanje_sutra', 'prevoznik',
                                   'dani', 'model', 'naziv', 'broj_redova', 'pozicije_sedista', 'cena'], delimiter=separator)
        for let in svi_letovi:
            csv_pisac.writerow({
                'broj_leta': svi_letovi[let]['broj_leta'],
                'sifra_polazisnog_aerodroma': svi_letovi[let]['sifra_polazisnog_aerodroma'],
                'sifra_odredisnog_aerodorma': svi_letovi[let]['sifra_odredisnog_aerodorma'],
                'vreme_poletanja': svi_letovi[let]['vreme_poletanja'],
                'vreme_sletanja': svi_letovi[let]['vreme_sletanja'],
                'datum_pocetka_operativnosti': svi_letovi[let]['datum_pocetka_operativnosti'],
                'datum_kraja_operativnosti': svi_letovi[let]['datum_kraja_operativnosti'],
                'sletanje_sutra': svi_letovi[let]['sletanje_sutra'],
                'prevoznik': svi_letovi[let]['prevoznik'],
                'dani': ",".join(str(dan) for dan in svi_letovi[let]['dani']),
                'model': svi_letovi[let]['model']['id'],
                'naziv': svi_letovi[let]['model']['naziv'],
                'broj_redova': int(svi_letovi[let]['model']['broj_redova']),
                'pozicije_sedista': ",".join(str(pozicija) for pozicija in svi_letovi[let]['model']['pozicije_sedista']),
                'cena': float(svi_letovi[let]['cena'])
            })


"""
Funkcija koja učitava sve letove iz fajla i vraća ih u rečniku.
"""


def ucitaj_letove_iz_fajla(putanja: str, separator: str) -> dict:
    with open(putanja, "r") as f:
        svi_letovi = dict()
        csv_citac = DictReader(f, ['broj_leta', 'sifra_polazisnog_aerodroma', 'sifra_odredisnog_aerodorma', 'vreme_poletanja', 'vreme_sletanja', 'datum_pocetka_operativnosti', 'datum_kraja_operativnosti', 'sletanje_sutra',
                                   'prevoznik', 'dani', 'model', 'naziv', 'broj_redova', 'pozicije_sedista', 'cena'], delimiter=separator)
        for let in csv_citac:
            dani = [int(dan) for dan in let['dani'].split(",")]
            model = {
                'id': int(let['model']),
                'naziv': let['naziv'],
                'broj_redova': int(let['broj_redova']),
                'pozicije_sedista': [str(pozicija) for pozicija in let['pozicije_sedista'].split(",")]
            }
            svi_letovi.update(podesi_let
                              (
                                  let['broj_leta'],
                                  let['sifra_polazisnog_aerodroma'],
                                  let['sifra_odredisnog_aerodorma'],
                                  let['vreme_poletanja'],
                                  let['vreme_sletanja'],
                                  let['datum_pocetka_operativnosti'],
                                  let['datum_kraja_operativnosti'],
                                  let['sletanje_sutra'] == 'True',
                                  let['prevoznik'],
                                  dani,
                                  model,
                                  float(let['cena'])
                              )
                              )

        return svi_letovi
