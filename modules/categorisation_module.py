from datetime import datetime
from classes import Transaction, Category

def categorize_transaction(transaction, category):

    naam_tegenrekening = transaction.attributes['naam_tegenrekening'].lower()
    omschrijving = transaction.attributes['omschrijving'].lower()
    omschrijving_short = omschrijving.split(">")[0].strip()
    vakantie_2020_start = datetime.strptime('2020-07-08', '%Y-%m-%d')
    vakantie_2020_end = datetime.strptime('2020-08-01', '%Y-%m-%d')

    # Categorisation based on IBAN
    # These transactions are between current account and savings account
    if transaction.attributes['tegenrekening'] == 'NL63ASNB8820283166':
        category['Spaar'].transactions.append(transaction)
        transaction.category = 'Spaar'
        transaction.attributes['bedrag'] = - transaction.attributes['bedrag']

    # Every non savings account transaction gets added to the Totaal category
    if transaction.category is None:
        category['Totaal'].transactions.append(transaction)

    # Categorisation based on date
    if transaction.category is None:
        if transaction.attributes['boekingsdatum'] > vakantie_2020_start and transaction.attributes['boekingsdatum'] < vakantie_2020_end:
            category['Vakanties'].transactions.append(transaction)
            transaction.category = 'Vakanties'

    # Categorisation based on keywords
    if transaction.category is None:
        for cat in category:
            if any(x.lower() in naam_tegenrekening for x in category[cat].keywords_naam_tegenrekening):
                category[cat].transactions.append(transaction)
                transaction.category = cat
                break
            if any(x.lower() in omschrijving_short for x in category[cat].keywords_omschrijving):
                category[cat].transactions.append(transaction)
                transaction.category = cat
                break

    # If none of the above methods yielded categorisation, add to category 'Geen categorie'
    if transaction.category is None:
        category['Geen categorie'].transactions.append(transaction)
