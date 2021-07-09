import os
import sys
import csv
import collections

# Required for relative imports to also work when called
# from project root directory.
sys.path.append(os.path.dirname(__file__))


class Transaction:

    def __init__(self, attributes):
        self.attributes = attributes









categories = ['Voeding', 'Reiskosten', 'Woning', 'Drank', 'Wiet', 'Cadeaus', 'Tikkies', 'Loon', 'Bijdrage papa en mama', 'Belastingen']




column_names = ['Boekingsdatum', 'Opdrachtgeversrekening', 'Tegenrekeningnummer', 'Naam tegenrekening', 'Adres', 'Postcode', 'Plaats', 'Valutasoort rekening', 'Saldo rekening voor mutatie', 'Valutasoort bedrag', 'Transactiebedrag', 'Journaaldatum', 'Valutadatum', 'Interne transactiecode', 'Globale transactiecode', 'Volgnummer transactie', 'Betalingskenmerk', 'Omschrijving', 'Afschriftnummer']

FILE_NAME_IN = 'betaal.csv'
current_dir = os.path.dirname(os.path.realpath(__file__))
path_in = os.path.join(current_dir, FILE_NAME_IN)

saldo_start = 282.04
flow_in = []
flow_out = []

with open(path_in) as infile:
    reader = csv.reader(infile, delimiter = ';')

    for row in reader:
        attributes = {
            'boekingsdatum': row[0],
            'opdrachtgeversrekening': row[1],
            'tegenrekening': row[2],
            'naam_tegenrekening': row[3],
            'adres': row[4],
            'postcode': row[5],
            'plaats': row[6],
            'valuta': row[7],
            'saldo_voor': row[8],
            'valuta_bedrag': row[9],
            'bedrag': row[10],
            'journaaldatum': row[11],
            'valutadatum': row[12],
            'code_intern': row[13],
            'code_globaal': row[14],
            'volgnummer': row[15],
            'kenmerk': row[16],
            'omschrijving': row[17],
            'afschriftnummer': row[18]
        }

        transaction = Transaction(attributes)

        # Total in/out
        if transaction.attributes['bedrag'].startswith('-'):
            flow_out.append(row[10])
        else:
            flow_in.append(row[10])

total_in = sum(map(float, flow_in))
total_out = sum(map(float, flow_out))
balance_change = total_in + total_out
saldo_end = saldo_start + balance_change

print(f'Starting money: {round(saldo_start,2)}')
print(f'Total money in: {round(total_in,2)}')
print(f'Total money out: {round(total_out,2)}')
print(f'Balance change is: {round(balance_change,2)}')
print(f'Ending money: {round(saldo_end,2)}')
