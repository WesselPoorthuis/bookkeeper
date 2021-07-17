import sys
import csv
from datetime import datetime

def process_modifiers(category, saldo_start):
    # If no category is specified, assume 'Totaal' is desired
    requested_category = 'Totaal'

    if '--category' in sys.argv:
        while True:
            try:
                print("\nAvailable categories are listed above.")
                requested_category = input('Which category would like details on?\n')
                if requested_category in category:
                    break
            except:
                print('\nSorry, the input did not match any category. Please try again.')

    if requested_category != 'Totaal':
        (inflow, outflow) = category[requested_category].calculate_flows()
        print(f'\nIncome in category: {requested_category}: {round(inflow,2)}')
        print(f'Expenditures in category: {requested_category}: {round(outflow,2)}')

    if '--transactions' in sys.argv:
        print('\nTransactions:')
        header = ['boekingsdatum', 'bedrag', 'category', 'naam_tegenrekening', 'omschrijving']
        print(', '.join(header))
        for transaction in category[requested_category].transactions:
            columns = [
            datetime.strftime(transaction.attributes['boekingsdatum'],'%d-%m-%Y'),
            str(transaction.attributes['bedrag']),
            transaction.category,
            transaction.attributes['naam_tegenrekening'],
            transaction.attributes['omschrijving']
            ]
            print(', '.join(columns))
            print('\n')

    if '--csv' in sys.argv:
        make_timeline_csv(requested_category, category, saldo_start)

def make_timeline_csv(requested_category, category, saldo_start):
    '''
    Writes .csv file with transaction data
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

        # Write transactions_uncategorized_in
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

def check_percentage_uncategorized(category):
    '''
    Checks the percentage of money in and out that is uncategorized
    '''
    (percentage_ungategorized_in, transactions_uncategorized_in, percentage_ungategorized_out, transactions_uncategorized_out) = (0,0,0,0)
    
    if category['Totaal'].calculate_flows()[0] != 0:
        percentage_ungategorized_in = abs(category['Geen categorie'].calculate_flows()[0]/category['Totaal'].calculate_flows()[0] * 100)
        transactions_uncategorized_in = len([transaction for transaction in category['Geen categorie'].transactions if transaction.attributes['bedrag'] > 0])

    if category['Totaal'].calculate_flows()[1] != 0:
        percentage_ungategorized_out = abs(category['Geen categorie'].calculate_flows()[1]/category['Totaal'].calculate_flows()[1] * 100)
        transactions_uncategorized_out = len([transaction for transaction in category['Geen categorie'].transactions if transaction.attributes['bedrag'] < 0])

    return (percentage_ungategorized_in, transactions_uncategorized_in, percentage_ungategorized_out, transactions_uncategorized_out)

def print_results(category, saldo_start):
    money_per_category = {}
    acceptable_uncategorized_percentage = 5

    # Calculate total flows
    (total_in,total_out) = category['Totaal'].calculate_flows()
    (savings_in, savings_out) = category['Spaar'].calculate_flows()
    balance_change = total_in + total_out
    saldo_end = saldo_start + balance_change
    savings_balance = savings_in + savings_out
    current_balance = saldo_end - savings_balance

    # Print overview
    total_flows_text = ('Initial amount', 'Total in', 'Total out', 'Balance change', 'On current account', 'On savings account','Final amount')
    total_flow_amounts = (saldo_start, total_in, total_out, balance_change, current_balance, savings_balance, saldo_end)
    print('\nOverview'.center(31,' '))
    print(''.center(31,'~'))
    for flow, amount in zip(total_flows_text, total_flow_amounts):
        print(f'{flow:20}:{amount:10.2f}')

    # Count flows per category
    for cat in category:
        (inflow, outflow) = category[cat].calculate_flows()
        money_per_category[cat] = inflow + outflow

    # Print net change per category
    print(f'\nBalance change per category'.center(32,' '))
    print(''.center(32,'~'))
    for cat in category:
        print(f'{cat:20}: {money_per_category[cat]:10.2f}')

    # Uncategorized elaboration
    (percentage_ungategorized_in, transactions_uncategorized_in, percentage_ungategorized_out, transactions_uncategorized_out) = check_percentage_uncategorized(category)
    if percentage_ungategorized_in > acceptable_uncategorized_percentage:
        print(f'Warning: more than the max of {"{:.0f}".format(acceptable_uncategorized_percentage)}%, namely {round(percentage_ungategorized_in, 2)}%, of income has not been categorized. This entails {transactions_uncategorized_in} transactions.')
    if percentage_ungategorized_out > acceptable_uncategorized_percentage:
            print(f'Warning: more than the max of {"{:.0f}".format(acceptable_uncategorized_percentage)}%, namely {round(percentage_ungategorized_out, 2)}%, of spending has not been categorized. This entails {transactions_uncategorized_out} transactions.')

    process_modifiers(category, saldo_start)
