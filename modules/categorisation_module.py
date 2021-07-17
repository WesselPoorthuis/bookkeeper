from datetime import datetime
from classes import Transaction, Category, DatetimeRange

def categorize_transaction(transaction, category):

    naam_tegenrekening = transaction.attributes['naam_tegenrekening'].lower()
    omschrijving = transaction.attributes['omschrijving'].lower()

    # Categorisation based on IBAN
    # These transactions are between current account and savings account
    if transaction.attributes['tegenrekening'] == 'NL63ASNB8820283166':
        category['Spaar'].transactions.append(transaction)
        transaction.category = 'Spaar'
        transaction.attributes['bedrag'] = -transaction.attributes['bedrag']

    # Every non savings account transaction gets added to the Totaal category
    if transaction.category is None:
        category['Totaal'].transactions.append(transaction)

    # Holiday dates
    zomervakantie_2020 = DatetimeRange(datetime(2020,7,8), datetime(2020,8,1))
    chillberen_keulen_2019 = DatetimeRange(datetime(2019,12,27), datetime(2019,12,30))

    # Categorisation based on date
    if transaction.category is None:
        if zomervakantie_2020.__contains__(transaction.attributes['boekingsdatum']) or chillberen_keulen_2019.__contains__(transaction.attributes['boekingsdatum']):
            category['Vakanties'].transactions.append(transaction)
            transaction.category = 'Vakanties'

    # Categorisation based on keywords
    if transaction.category is None:
        for cat in category:
            if any(substring.lower() in naam_tegenrekening for substring in category[cat].keywords_naam_tegenrekening):
                category[cat].transactions.append(transaction)
                transaction.category = cat
                break
            if any(substring.lower() in omschrijving for substring in category[cat].keywords_omschrijving):
                category[cat].transactions.append(transaction)
                transaction.category = cat
                break

    # If none of the above methods yielded categorisation, add to category 'Geen categorie'
    if transaction.category is None:
        category['Geen categorie'].transactions.append(transaction)
