import sys
import csv
from datetime import datetime

def process_modifiers(category, saldo_start):
    # If no category is specified, assume all transactions are requested
    requested_category = 'Totaal'

    if '--category' in sys.argv:
        while True:
            print("\nAvailable categories are listed above.")
            requested_category = input('On which category would like details?\n')
            if requested_category in category:
                break
            print('Sorry, the input did not match any category. Please try again.')
        print_category_details(requested_category, category)

    if '--transactions' in sys.argv:
        print_transactions(requested_category, category)

    if '--csv' in sys.argv:
        write_transactions_csv(requested_category, category, saldo_start)

def print_category_details(requested_category, category):
    '''
    Prints extra information on category.
    '''
    (inflow, outflow) = category[requested_category].calculate_flows()
    print(f'\nIncome in category {requested_category}: {round(inflow,2)}')
    print(f'Expenditures in category {requested_category}: {round(outflow,2)}')
    # Visualisations here? net change over time?

def print_transactions(requested_category, category):
    '''
    Prints transactions to terminal.
    '''
    print('\nTransactions:')
    header = ['boekingsdatum', 'bedrag', 'category', 'naam_tegenrekening', 'omschrijving']
    print(', '.join(header))
    for transaction in category[requested_category].transactions:
        if transaction.category == None:
            transaction.category = 'Geen categorie'
        columns = [
        datetime.strftime(transaction.attributes['boekingsdatum'],'%d-%m-%Y'),
        str(transaction.attributes['bedrag']),
        transaction.category,
        transaction.attributes['naam_tegenrekening'],
        transaction.attributes['omschrijving']
        ]
        print(', '.join(columns))
        print('\n')

def write_transactions_csv(requested_category, category, saldo_start):
    '''
    Writes .csv file with transaction data.
    '''
    net_change = 0
    requested_category_string = requested_category.replace(' ', "_")

    if requested_category == 'Totaal':
        net_change += saldo_start

    # Create output file
    with open(f'outputs/{requested_category_string}_transactions.csv', 'w', newline='') as csvfile:
        transaction_writer = csv.writer(csvfile, delimiter =',', quotechar = '"')

        # Write header
        transaction_writer.writerow(['boekingsdatum', 'bedrag', 'net_change', 'saldo_voor', 'category', 'naam_tegenrekening', 'omschrijving'])

        # Write transaction data
        for transaction in category[requested_category].transactions:
            net_change += transaction.attributes['bedrag']
            columns = [
            datetime.strftime(transaction.attributes['boekingsdatum'],'%d-%m-%Y'),
            str(transaction.attributes['bedrag']),
            net_change,
            str(transaction.attributes['saldo_voor']),
            transaction.category,
            transaction.attributes['naam_tegenrekening'],
            transaction.attributes['omschrijving']
            ]
            transaction_writer.writerow(columns)

    print(f'\n{requested_category_string}_transactions.csv had been created in the outputs folder.')
