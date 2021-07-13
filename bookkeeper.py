import os
import sys
import csv
from datetime import datetime
# from datetime import date

from keyword_dicts import create_keywords_naam_tegenrekening_dict, create_keywords_omschrijving_dict
from classes import Transaction, Category

# Required for relative imports to also work when called
# from project root directory.
sys.path.append(os.path.dirname(__file__))

def initialize_categories():
    for cat in category_list:
        category[cat] = Category(cat)

def categorize_transaction(transaction):
    naam_tegenrekening = transaction.attributes['naam_tegenrekening']
    omschrijving = transaction.attributes['omschrijving']
    omschrijving_short = omschrijving.split(">")[0].strip()
    vakantie_2020_start = datetime.strptime('2020-07-08', '%Y-%m-%d')
    vakantie_2020_end = datetime.strptime('2020-08-01', '%Y-%m-%d')

    # Categorize based on keywords
    for cat in category_list:
        if any(x in naam_tegenrekening for x in keywords_naam_tegenrekening[cat]):
            category[cat].transactions.append(transaction)
            transaction.category = cat
            break
        if any(x in omschrijving_short for x in keywords_omschrijving[cat]):
            category[cat].transactions.append(transaction)
            transaction.category = cat
            break

    if transaction.category is None:
        if transaction.attributes['boekingsdatum'] > vakantie_2020_start and transaction.attributes['boekingsdatum'] < vakantie_2020_end:
            category['Vakanties'].transactions.append(transaction)
            transaction.category = 'Vakanties'
    if transaction.category is None:
        category['Geen categorie'].transactions.append(transaction)


'''Start of program'''

category_list = ['Overschrijving eigen rekeningen', 'Bijdrage familie', 'DUO', 'Boodschappen', 'Kleding', 'Media', 'Reiskosten', 'Woning', 'Drugs', 'Cadeaus', 'Terugbetalingen', 'Loon', 'Belastingen', 'Horeca', 'Goede doelen','Vaste lasten', 'Online bestellingen', 'Zorg', 'Feesten', 'Hobbies', 'Vakanties', 'Geen categorie']

FILE_NAME_IN = 'betaal_2.csv'
current_dir = os.path.dirname(os.path.realpath(__file__))
path_in = os.path.join(current_dir, FILE_NAME_IN)

saldo_start = 282.04
total_in = 0
total_out = 0
money_per_category = {}
category = {}

# Create keywords
keywords_naam_tegenrekening = create_keywords_naam_tegenrekening_dict()
keywords_omschrijving = create_keywords_omschrijving_dict()

initialize_categories()

# Read in .csv file
with open(path_in) as infile:
    reader = csv.reader(infile, delimiter = ';')

    # Create transaction object
    for row in reader:
        attributes = {
            'boekingsdatum': datetime.strptime(row[0], '%d-%m-%Y'),
            'opdrachtgeversrekening': row[1],
            'tegenrekening': row[2],
            'naam_tegenrekening': row[3],
            'adres': row[4],
            'postcode': row[5],
            'plaats': row[6],
            'valuta': row[7],
            'saldo_voor': float(row[8]),
            'valuta_bedrag': row[9],
            'bedrag': float(row[10]),
            'journaaldatum': datetime.strptime(row[11], '%d-%m-%Y'),
            'valutadatum': datetime.strptime(row[12], '%d-%m-%Y'),
            'code_intern': row[13],
            'code_globaal': row[14],
            'volgnummer': row[15],
            'kenmerk': row[16],
            'omschrijving': row[17],
            'afschriftnummer': row[18]
        }
        transaction = Transaction(attributes)
        # Categorize transaction
        categorize_transaction(transaction)

# Money counting per category
for cat in category_list:
    (inflow, outflow) = category[cat].calculate_flows()
    money_per_category[cat] = inflow + outflow
    total_in += inflow
    total_out += outflow

balance_change = total_in + total_out
saldo_end = saldo_start + balance_change
#
# for transactions in category['Vakanties'].transactions:
#     print(transactions.attributes['naam_tegenrekening'])
#     print(transactions.attributes['omschrijving'])
#     print(transactions.attributes['bedrag'])

# Print results
print(f'Starting money: {round(saldo_start,2)}')
print(f'Total money in: {round(total_in,2)}')
print(f'Total money out: {round(total_out,2)}')
print(f'Balance change is: {round(balance_change,2)}')
print(f'Ending money: {round(saldo_end,2)}\n')
print(f'Net money per category:')
for cat in category_list:
    print(f'{cat}: {round(money_per_category[cat],2)}')
