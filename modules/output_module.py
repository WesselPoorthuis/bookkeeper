import sys
import csv
from datetime import datetime

def print_category_details(requested_category, category, saldo_start):
        (inflow, outflow) = category[requested_category].calculate_flows()
        print(f'\nIncome in category: {requested_category}: {round(inflow,2)}')
        print(f'Expenditures in category: {requested_category}: {round(outflow,2)}')

        if '--transactions' in sys.argv:
            for transaction in category[requested_category].transactions:
                print(datetime.strftime(transaction.attributes['boekingsdatum'], '%d-%m-%Y'))
                print(transaction.attributes['valuta_bedrag'] + ' ' + str(round(transaction.attributes['bedrag'],2)))
                print(transaction.attributes['naam_tegenrekening'] )
                print(transaction.attributes['omschrijving'])
                print('\n')

        if '--csv' in sys.argv:
            make_timeline_csv(requested_category, category, saldo_start)

def make_timeline_csv(requested_category, category, saldo_start):
    '''
    Writes .csv file with transaction data
    '''
    net_change = 0
    if requested_category == 'Totaal':
        net_change += saldo_start
    with open(f'outputs/{requested_category}_transactions.csv', 'w', newline='') as csvfile:
        transaction_writer = csv.writer(csvfile, delimiter =',', quotechar = '"')

        # Write header
        transaction_writer.writerow(['boekingsdatum', 'bedrag', 'net_change', 'saldo_voor', 'category', 'naam_tegenrekening', 'omschrijving'])

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

    print(f'\n{requested_category}_transactions.csv had been created in the outputs folder.')

def check_percentage_uncategorized(category):
    '''
    Checks the percentage of money in and out that is uncategorized
    '''
    acceptable_uncategorized_percentage = 5

    if category['Totaal'].calculate_flows()[0] != 0:
        percentage_ungategorized_in = abs(category['Geen categorie'].calculate_flows()[0]/category['Totaal'].calculate_flows()[0] * 100)
        transactions_uncategorized_in = len([transaction for transaction in category['Geen categorie'].transactions if transaction.attributes['bedrag'] > 0])
        if percentage_ungategorized_in > acceptable_uncategorized_percentage:
            print(f'Warning: {round(percentage_ungategorized_in, 2)}% of income has not been categorized. This entails {transactions_uncategorized_in} transactions.')

    if category['Totaal'].calculate_flows()[1] != 0:
        percentage_ungategorized_out = abs(category['Geen categorie'].calculate_flows()[1]/category['Totaal'].calculate_flows()[1] * 100)
        transactions_uncategorized_out = len([transaction for transaction in category['Geen categorie'].transactions if transaction.attributes['bedrag'] < 0])
        if percentage_ungategorized_out > acceptable_uncategorized_percentage:
            print(f'Warning: {round(percentage_ungategorized_out, 2)}% of spending has not been categorized. This entails {transactions_uncategorized_out} transactions.')

def print_results(category, saldo_start):
    money_per_category = {}

    # Count flows per category
    for cat in category:
        (inflow, outflow) = category[cat].calculate_flows()
        money_per_category[cat] = inflow + outflow

    # Calculate total flows
    (total_in,total_out) = category['Totaal'].calculate_flows()
    (savings_in, savings_out) = category['Spaar'].calculate_flows()
    balance_change = total_in + total_out
    saldo_end = saldo_start + balance_change
    savings_balance = savings_in + savings_out
    current_balance = saldo_end - savings_balance

    text = ('Initial amount', 'Total in', 'Total out', 'Balance change', 'On current account', 'On savings account','Final amount')
    amount = (saldo_start, total_in, total_out, balance_change, current_balance, savings_balance, saldo_end)

    #Printing
    print('\n')
    print('Overview'.center(31,' '))
    print(''.center(31,'~'))
    for x, y in zip(text, amount):
        print(f'{x:20}:{y:10.2f}')

    print('\n')
    print(f'Balance change per category'.center(32,' '))
    print(''.center(32,'~'))
    for cat in category:
        print(f'{cat:20}: {money_per_category[cat]:10.2f}')

    check_percentage_uncategorized(category)

    if '--category' in sys.argv:
        while True:
            try:
                print("\nAvailable categories are listed above.")
                requested_category = input('Which category would like details on?\n')
                print_category_details(requested_category, category, saldo_start)
                break
            except:
                print('\nSorry, the input did not match any category. Please try again.')
