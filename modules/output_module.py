import sys

from modules.modifiers_module import process_modifiers

def calculate_percentage_uncategorized(category):
    '''
    Checks the percentage of money in and out that is uncategorized.
    '''
    (percentage_ungategorized_in, transactions_uncategorized_in, percentage_ungategorized_out, transactions_uncategorized_out) = (0,0,0,0)

    if category['Totaal'].calculate_flows()[0] != 0:
        percentage_ungategorized_in = abs(category['Geen categorie'].calculate_flows()[0]/category['Totaal'].calculate_flows()[0] * 100)
        transactions_uncategorized_in = len([transaction for transaction in category['Geen categorie'].transactions if transaction.attributes['bedrag'] > 0])

    if category['Totaal'].calculate_flows()[1] != 0:
        percentage_ungategorized_out = abs(category['Geen categorie'].calculate_flows()[1]/category['Totaal'].calculate_flows()[1] * 100)
        transactions_uncategorized_out = len([transaction for transaction in category['Geen categorie'].transactions if transaction.attributes['bedrag'] < 0])

    return (percentage_ungategorized_in, transactions_uncategorized_in, percentage_ungategorized_out, transactions_uncategorized_out)

def print_results(category, saldo_start, acceptable_uncategorized_percentage):

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
    print('Overview'.center(32,' '))
    print(''.center(32,'~'))
    for flow, amount in zip(total_flows_text, total_flow_amounts):
        print(f'{flow:20}:{amount:11.2f}')
    print(''.center(32,'~'))

    # Count flows per category
    money_per_category = {}
    for cat in category:
        (inflow, outflow) = category[cat].calculate_flows()
        money_per_category[cat] = inflow + outflow

    # Print net change per category
    print('\n')
    print('Balance change per category'.center(32,' '))
    print(''.center(32,'~'))
    for cat in category:
        print(f'{cat:20}: {money_per_category[cat]:10.2f}')
    print(''.center(32,'~'))

    # Uncategorized elaboration
    (percentage_ungategorized_in, transactions_uncategorized_in, percentage_ungategorized_out, transactions_uncategorized_out) = calculate_percentage_uncategorized(category)
    if percentage_ungategorized_in > acceptable_uncategorized_percentage:
        print(f'Warning: more than the max of {"{:.0f}".format(acceptable_uncategorized_percentage)}%, namely {round(percentage_ungategorized_in, 2)}%, of income has not been categorized. This entails {transactions_uncategorized_in} transactions.')
    if percentage_ungategorized_out > acceptable_uncategorized_percentage:
            print(f'Warning: more than the max of {"{:.0f}".format(acceptable_uncategorized_percentage)}%, namely {round(percentage_ungategorized_out, 2)}%, of spending has not been categorized. This entails {transactions_uncategorized_out} transactions.')

    process_modifiers(category, saldo_start)
