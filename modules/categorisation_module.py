from datetime import datetime
from classes import Transaction, Category

def categorize_transaction(transaction, category):

    naam_tegenrekening = transaction.attributes['naam_tegenrekening']
    omschrijving = transaction.attributes['omschrijving']
    omschrijving_short = omschrijving.split(">")[0].strip()
    vakantie_2020_start = datetime.strptime('2020-07-08', '%Y-%m-%d')
    vakantie_2020_end = datetime.strptime('2020-08-01', '%Y-%m-%d')

    # Every transaction gets added to the Totaal category
    category['Totaal'].transactions.append(transaction)

    # Categorisation based on keywords
    for cat in category:
        if any(x in naam_tegenrekening for x in category[cat].keywords_naam_tegenrekening):
            category[cat].transactions.append(transaction)
            transaction.category = cat
            break
        if any(x in omschrijving_short for x in category[cat].keywords_omschrijving):
            category[cat].transactions.append(transaction)
            transaction.category = cat
            break

    # Categorisation based on date
    if transaction.category is None:
        if transaction.attributes['boekingsdatum'] > vakantie_2020_start and transaction.attributes['boekingsdatum'] < vakantie_2020_end:
            category['Vakanties'].transactions.append(transaction)
            transaction.category = 'Vakanties'
    if transaction.category is None:
        category['Geen categorie'].transactions.append(transaction)