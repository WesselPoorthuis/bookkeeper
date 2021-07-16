import os
import sys
import csv
from datetime import datetime
import argparse

from modules.output_module import print_results
from modules.categorisation_module import categorize_transaction
from modules.keywords_module import add_tegenrekening_keywords, add_omschrijving_keywords
from classes import Transaction, Category

# Required for relative imports to also work when called
# from project root directory.
sys.path.append(os.path.dirname(__file__))

def check_date():
        while True:
            try:
                requested_date = input('Enter desired date in dd-mm-yyyy format\n')
                requested_date = datetime.strptime(requested_date, '%d-%m-%Y')
                return requested_date
                break
            except:
                print(f'{requested_date} is not the right format, please try again\n')

def check_dates():
        while True:
            try:
                start_date = input('Enter starting date in dd-mm-yyyy format\n')
                start_date = datetime.strptime(start_date, '%d-%m-%Y')
                break
            except:
                print(f'{start_date} is not the right format, please try again\n')
        while True:
            try:
                end_date = input('Enter final date in dd-mm-yyyy format\n')
                end_date = datetime.strptime(end_date, '%d-%m-%Y')
                return (start_date, end_date)
                break
            except:
                print(f'{end_date} is not the right format, please try again\n')

def initialize_categories(category_list, category):
    # Create categories
    for cat in category_list:
        category[cat] = Category(cat)

    # Add keywords to categories
    add_tegenrekening_keywords(category)
    add_omschrijving_keywords(category)

def main():
    # Create help
    parser = argparse.ArgumentParser(description='Goes through .csv file with banking details and categorizes transactions.')
    parser.add_argument('--category', action='store_true', help='get more detailed information about a category')
    parser.add_argument('--csv', action='store_true', help='generate .csv file with transaction history of the category specified with --category')
    parser.add_argument('--transactions', action='store_true', help='prints every transaction in the category specified with --category')
    parser.add_argument('--date', action='store_true', help='only considers transactions on a given date')
    parser.add_argument('--dates', action='store_true', help='only considers transactions between two given dates (inclusive)')
    args = parser.parse_args()

    # Create category instances based on category list
    category = {}
    category_list = [
    'Totaal',
    'Eigen rekeningen',
    'Bijdrage familie',
    'DUO',
    'Boodschappen',
    'Kleding',
    'Media',
    'Reiskosten',
    'Woning',
    'Drugs',
    'Cadeaus',
    'Terugbetalingen',
    'Loon',
    'Belastingen',
    'Horeca',
    'Goede doelen',
    'Vaste lasten',
    'Online bestellingen',
    'Zorg',
    'Feesten',
    'Hobbies',
    'Vakanties',
    'Spaar',
    'Geen categorie']

    initialize_categories(category_list, category)

    #Check for date modifiers
    requested_date = None
    start_date = None
    end_date = None

    if '--date' in sys.argv:
        requested_date = check_date()

    if '--dates' in sys.argv:
        (start_date, end_date) = check_dates()

    # Declare variables
    transaction_number = 0
    saldo_start = 0

    # Read in .csv file
    FILE_NAME_IN = 'inputs/betaal_2.csv'
    current_dir = os.path.dirname(os.path.realpath(__file__))
    path_in = os.path.join(current_dir, FILE_NAME_IN)

    with open(path_in) as infile:
        reader = csv.reader(infile, delimiter = ';')

        # Create transaction object
        for row in reader:

            attributes = {
                'transaction_number' : transaction_number,
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

            if (requested_date is None and start_date is None) or (requested_date is not None and attributes['boekingsdatum'] == requested_date) or (start_date is not None and attributes['boekingsdatum'] >= start_date and attributes['boekingsdatum'] <= end_date):
                transaction = Transaction(attributes)
                if transaction.attributes['transaction_number'] == 0:
                    saldo_start = transaction.attributes['saldo_voor']
                categorize_transaction(transaction, category)
                transaction_number += 1

    #Print results
    print_results(category, saldo_start)

if __name__ == "__main__":
	main()
