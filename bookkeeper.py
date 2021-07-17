import os
import sys
import csv
from datetime import datetime
import argparse

from modules.output_module import print_results
from modules.categorisation_module import categorize_transaction
from modules.keywords_module import add_tegenrekening_keywords, add_omschrijving_keywords
from classes import Transaction, Category, DatetimeRange

# Required for relative imports to also work when called
# from project root directory.
sys.path.append(os.path.dirname(__file__))

def get_dates():
    requested_dates = []

    print('Enter desired dates in dd-mm-yyyy format.\nWhen finished, type "done".\n')
    while True:
        try:
            requested_date = input()
            if requested_date == 'done':
                break
            requested_date = datetime.strptime(requested_date, '%d-%m-%Y')
            requested_date = (requested_date, requested_date)
            requested_dates.append(requested_date)
        except:
            print(f'{requested_date} is not the right format, please try again.')
    return requested_dates

def get_intervals():
    requested_intervals = []

    print('Enter desired intervals in dd-mm-yyyy/dd-mm-yyyy format.\nWhen finished, type "done".\nOverlapping will double count.')
    while True:
        try:
            requested_interval = input()
            if requested_interval == 'done':
                break
            (start_date, end_date) = (requested_interval[:10], requested_interval[-9:])
            start_date = datetime.strptime(start_date, '%d-%m-%Y')
            end_date = datetime.strptime(end_date, '%d-%m-%Y')
            requested_interval = DatetimeRange(start_date, end_date)
            requested_intervals.append(requested_interval)
        except:
            print(f'{requested_interval} is not the right format, please try again.')
    return requested_intervals

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

    #Check for date modifiers
    requested_dates = [DatetimeRange(datetime(1,1,1), datetime(9999,1,1))]
    start_date = None
    end_date = None

    if '--dates' in sys.argv:
        requested_dates = get_dates()

    if '--intervals' in sys.argv:
        requested_dates = get_intervals()

    # Declare variables
    transaction_number = 0
    saldo_start = 0

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
    print_results(category, saldo_start)

if __name__ == "__main__":
	main()
