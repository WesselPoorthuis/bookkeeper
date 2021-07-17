import os
import sys
import csv
from datetime import datetime
import argparse

from modules.output_module import print_results
from modules.categorisation_module import categorize_transaction
from modules.keywords_module import add_tegenrekening_keywords, add_omschrijving_keywords
from modules.classes import Transaction, Category, DatetimeRange
from modules.timespan_module import get_timespan

# Required for relative imports to also work when called
# from project root directory.
sys.path.append(os.path.dirname(__file__))

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
    parser.add_argument('--category', action='store_true', help='Prints more detailed information about a category.')
    parser.add_argument('--csv', action='store_true', help='Generates .csv file with transaction history of the category specified with --category.')
    parser.add_argument('--transactions', action='store_true', help='Prints every transaction in the category specified with --category. Useful for a quick view.')
    parser.add_argument('--dates', action='store_true', help='Specify transactions per day.')
    parser.add_argument('--intervals', action='store_true', help='Specify transactions per time interval (inclusive).')
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
    'Gepind',
    'Geen categorie']

    initialize_categories(category_list, category)

    # Timespan that is considered
    requested_dates = get_timespan()

    # Declare variables
    transaction_number = 0
    saldo_start = 0
    acceptable_uncategorized_percentage = 5

    # Read in .csv file
    FILE_NAME_IN = 'betaal_2.csv'
    current_dir = os.path.dirname(os.path.realpath(__file__))
    path_in = os.path.join(current_dir + '/inputs', FILE_NAME_IN)

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

            for interval in requested_dates:
                if interval.__contains__(attributes['boekingsdatum']):
                    transaction = Transaction(attributes)
                    if transaction.attributes['transaction_number'] == 0:
                        saldo_start = transaction.attributes['saldo_voor']
                    categorize_transaction(transaction, category)
                    transaction_number += 1

    #Print results
    print_results(category, saldo_start,acceptable_uncategorized_percentage)

if __name__ == "__main__":
	main()
