import os
import sys
import csv

# Required for relative imports to also work when called
# from project root directory.
sys.path.append(os.path.dirname(__file__))

column_names = ['Boekingsdatum', 'Opdrachtgeversrekening', 'Tegenrekeningnummer', 'Naam tegenrekening', 'Adres', 'Postcode', 'Plaats', 'Valutasoort rekening', 'Saldo rekening voor mutatie', 'Transactiebedrag', 'Journaaldatum', 'Valutadatum', 'Interne transactiecode', 'Globale transactiecode', 'Volgnummer transactie', 'Betalingskenmerk', 'Omschrijving', 'Afschriftnummer']


FILE_NAME_IN = '0772942609_09072021_155047.csv'
current_dir = os.path.dirname(os.path.realpath(__file__))
path_in = os.path.join(current_dir, FILE_NAME_IN)



saldo_start = 1994.58
flow_in = []
flow_out = []








with open(path_in) as infile:
    reader = csv.reader(infile, delimiter = ';')

    for row in reader:
        if row[10].startswith('-'):
            flow_out.append(row[10])
        else:
            flow_in.append(row[10])

total_in = sum(map(float, flow_in))
total_out = sum(map(float, flow_out))
balance_change = total_in + total_out
saldo_end = saldo_start + balance_change

print(f'Starting money: {saldo_start}')
print(f'Total money in: {total_in}')
print(f'Total money out: {round(total_out,2)}')
print(f'Balance change is: {round(balance_change,2)}')
print(f'Ending money: {round(saldo_end,2)}')
