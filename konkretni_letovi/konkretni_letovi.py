from datetime import datetime, timedelta
from common import konstante
from letovi import letovi
from csv import DictReader, DictWriter

sifra_konkretnog_leta = 1000

def kreiranje_konkretnog_leta(svi_konkretni_letovi: dict, let: dict):
    global sifra_konkretnog_leta
    
    konkretni_letovi = dict()
    
    datum_pocetka: datetime = let['datum_pocetka_operativnosti']   
    datum_kraja: datetime = let['datum_kraja_operativnosti']
    
    sat_poletanja, minut_poletanja = let['vreme_poletanja'].split(":")
    sat_sletanja, minut_sletanja = let['vreme_sletanja'].split(":")    
    
    if type(datum_pocetka) == str:
        datum_pocetka = datetime.strptime(datum_pocetka, konstante.FORMAT_DATETIME)
    if type(datum_kraja) == str:
        datum_kraja = datetime.strptime(datum_kraja, konstante.FORMAT_DATETIME)
        
    datum_i_vreme_poletanja = datum_pocetka.replace(hour = int(sat_poletanja), minute = int(minut_poletanja))
    datum_i_vreme_sletanja = datum_pocetka.replace(hour = int(sat_sletanja), minute = int(minut_sletanja))
    
    period = datum_kraja - datum_pocetka
    for _ in range(period.days):
        if datum_i_vreme_poletanja.weekday() in let['dani']:
            konkretni_letovi.update({
                        sifra_konkretnog_leta:
                        {
                            'sifra': sifra_konkretnog_leta,
                            'broj_leta': let['broj_leta'],
                            'datum_i_vreme_polaska': datum_i_vreme_poletanja,
                            'datum_i_vreme_dolaska': datum_i_vreme_sletanja,
                        }
                    })
            sifra_konkretnog_leta += 1
        datum_i_vreme_poletanja += timedelta(days = 1)
        datum_i_vreme_sletanja += timedelta(days = 1)
        
    svi_konkretni_letovi.update(konkretni_letovi)
    return konkretni_letovi

def sacuvaj_kokretan_let(putanja: str, separator: str, svi_konkretni_letovi: dict):
    with open(putanja, 'w', newline='') as f:
        csv_pisac = DictWriter(f, ['sifra', 'broj_leta', 'datum_i_vreme_polaska', 'datum_i_vreme_dolaska', 'zauzetost'], delimiter = separator)
        
        for konkretan_let in svi_konkretni_letovi:
            matrica = ""
            for red in range(len(svi_konkretni_letovi[konkretan_let]['zauzetost'])):
                matrica += ",".join(str(sediste) for sediste in svi_konkretni_letovi[konkretan_let]['zauzetost'][red]) + ";"
                    
            csv_pisac.writerow({
                'sifra': int(svi_konkretni_letovi[konkretan_let]['sifra']),
                'broj_leta': svi_konkretni_letovi[konkretan_let]['broj_leta'],
                'datum_i_vreme_polaska': datetime.strftime(svi_konkretni_letovi[konkretan_let]['datum_i_vreme_polaska'], konstante.FORMAT_DATETIME),
                'datum_i_vreme_dolaska': datetime.strftime(svi_konkretni_letovi[konkretan_let]['datum_i_vreme_dolaska'], konstante.FORMAT_DATETIME),
                'zauzetost': matrica                
            })

def ucitaj_konkretan_let(putanja: str, separator: str) -> dict:
    global sifra_konkretnog_leta
    konkretni_letovi = dict()
    with open(putanja) as f:
        csv_citac = DictReader(f, ['sifra', 'broj_leta', 'datum_i_vreme_polaska', 'datum_i_vreme_dolaska', 'zauzetost'], delimiter = separator)
        for konkretan_let in csv_citac:
            matrica = list()
            redovi = konkretan_let['zauzetost'].split(';')[:-1]
            for sedista in redovi:
                matrica.append([zauzeto == 'True' for zauzeto in sedista.split(',')])
            
            konkretni_letovi.update({
                int(konkretan_let['sifra']): 
                {
                    'sifra': int(konkretan_let['sifra']),
                    'broj_leta': konkretan_let['broj_leta'],
                    'datum_i_vreme_polaska': datetime.strptime(konkretan_let['datum_i_vreme_polaska'], konstante.FORMAT_DATETIME),
                    'datum_i_vreme_dolaska': datetime.strptime(konkretan_let['datum_i_vreme_dolaska'], konstante.FORMAT_DATETIME),
                    'zauzetost': matrica
                }
            })
    if konkretni_letovi != {}:
       sifra_konkretnog_leta = max(konkretni_letovi) + 1
    return konkretni_letovi