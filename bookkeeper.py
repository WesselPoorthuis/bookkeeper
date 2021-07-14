import os
import sys
import csv
from datetime import datetime
import argparse

from modules.printing_module import print_results
from modules.categorisation_module import categorize_transaction
from classes import Transaction, Category

# Required for relative imports to also work when called
# from project root directory.
sys.path.append(os.path.dirname(__file__))

def initialize_categories(category_list, category):
    for cat in category_list:
        category[cat] = Category(cat)

def main():
    # Create help
    parser = argparse.ArgumentParser(description='Goes through .csv file with banking details and categorizes transactions.')
    parser.add_argument('--category', action='store_true', help='get more detailed niformation about a category')
    parser.add_argument('--timeline', action='store_true', help='generate .csv file with transaction history of category')
    parser.add_argument('--transactions', action='store_true', help='prints every transaction in the category')
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
    'Geen categorie']

    initialize_categories(category_list, category)

    saldo_start = 282.04

    # Read in .csv file
    FILE_NAME_IN = 'inputs/betaal_2.csv'
    current_dir = os.path.dirname(os.path.realpath(__file__))
    path_in = os.path.join(current_dir, FILE_NAME_IN)

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
            categorize_transaction(transaction, category)

    #Print results
    print_results(category_list, category, saldo_start)

if __name__ == "__main__":
	main()
