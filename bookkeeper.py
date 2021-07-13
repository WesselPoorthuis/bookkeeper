import os
import sys
import csv
import collections

from keyword_dicts import create_keywords_naam_tegenrekening_dict, create_keywords_omschrijving_dict
from classes import Transaction

# Required for relative imports to also work when called
# from project root directory.
sys.path.append(os.path.dirname(__file__))

def categorize_transaction(transaction):
    naam_tegenrekening = transaction.attributes['naam_tegenrekening']
    omschrijving = transaction.attributes['omschrijving']
    omschrijving_short = omschrijving.split(">")[0].strip()

    # Make transactions easily searchable
    if naam_tegenrekening != '':
        tegenrekeningen_dict[naam_tegenrekening].append(transaction)
    else:
        omschrijvingen_dict[omschrijving_short].append(transaction)

    # Categorize based on keywords
    for cat in categories:
        if any(x in naam_tegenrekening for x in keywords_naam_tegenrekening[cat]):
            categories_dict[cat].append(transaction)
            tegenrekeningen_dict.pop(naam_tegenrekening, None)
            transaction.category = cat
        elif any(x in omschrijving_short for x in keywords_omschrijving[cat]):
            categories_dict[cat].append(transaction)
            omschrijvingen_dict.pop(omschrijving_short, None)
            transaction.category = cat

    return (tegenrekeningen_dict, omschrijvingen_dict)

categories = ['Overschrijving eigen rekeningen', 'DUO', 'Boodschappen', 'Kleding', 'Media', 'Reiskosten', 'Woning', 'Drugs', 'Cadeaus', 'Terugbetalingen', 'Loon', 'Bijdrage familie', 'Belastingen', 'Horeca', 'Goede doelen','Vaste lasten', 'Online bestellingen']

column_names = ['Boekingsdatum', 'Opdrachtgeversrekening', 'Tegenrekeningnummer', 'Naam tegenrekening', 'Adres', 'Postcode', 'Plaats', 'Valutasoort rekening', 'Saldo rekening voor mutatie', 'Valutasoort bedrag', 'Transactiebedrag', 'Journaaldatum', 'Valutadatum', 'Interne transactiecode', 'Globale transactiecode', 'Volgnummer transactie', 'Betalingskenmerk', 'Omschrijving', 'Afschriftnummer']

FILE_NAME_IN = 'betaal.csv'
current_dir = os.path.dirname(os.path.realpath(__file__))
path_in = os.path.join(current_dir, FILE_NAME_IN)

saldo_start = 282.04
flow_in = []
flow_out = []
tegenrekeningen_dict = collections.defaultdict(list)
omschrijvingen_dict = collections.defaultdict(list)
categories_dict = collections.defaultdict(list)
keywords_naam_tegenrekening = {}
keywords_omschrijving = {}

with open(path_in) as infile:

    # Create keywords
    keywords_naam_tegenrekening = create_keywords_naam_tegenrekening_dict()
    keywords_omschrijving = create_keywords_omschrijving_dict()

    # Read in .csv file
    reader = csv.reader(infile, delimiter = ';')
    for row in reader:
        # Assign attributes to transaction object
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

        # Categorisation
        (tegenrekeningen_dict, omschrijvingen_dict) = categorize_transaction(transaction)

        # Total in/out
        if transaction.attributes['bedrag'].startswith('-'):
            flow_out.append(transaction.attributes['bedrag'])
        else:
            flow_in.append(transaction.attributes['bedrag'])

total_in = sum(map(float, flow_in))
total_out = sum(map(float, flow_out))
balance_change = total_in + total_out
saldo_end = saldo_start + balance_change

print(f'Starting money: {round(saldo_start,2)}')
print(f'Total money in: {round(total_in,2)}')
print(f'Total money out: {round(total_out,2)}')
print(f'Balance change is: {round(balance_change,2)}')
print(f'Ending money: {round(saldo_end,2)}')
