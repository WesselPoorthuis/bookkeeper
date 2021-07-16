from datetime import datetime
from classes import Transaction, Category

def categorize_transaction(transaction, category):

    naam_tegenrekening = transaction.attributes['naam_tegenrekening'].lower()
    omschrijving = transaction.attributes['omschrijving'].lower()

    #Holidays
    zomervakantie_2020_start = datetime.strptime('2020-07-08', '%Y-%m-%d')
    zomervakantie_2020_end = datetime.strptime('2020-08-01', '%Y-%m-%d')
    chillberen_keulen_2019_start = datetime.strptime('2019-12-27', '%Y-%m-%d')
    chillberen_keulen_2019_end = datetime.strptime('2019-12-30', '%Y-%m-%d')

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
    zomervakantie_2020_start = datetime.strptime('2020-07-08', '%Y-%m-%d')
    zomervakantie_2020_end = datetime.strptime('2020-08-01', '%Y-%m-%d')
    chillberen_keulen_2019_start = datetime.strptime('2019-12-27', '%Y-%m-%d')
    chillberen_keulen_2019_end = datetime.strptime('2019-12-30', '%Y-%m-%d')

    # Categorisation based on date
    if transaction.category is None:
        if transaction.attributes['boekingsdatum'] >= zomervakantie_2020_start and transaction.attributes['boekingsdatum'] <= zomervakantie_2020_end:
            category['Vakanties'].transactions.append(transaction)
            transaction.category = 'Vakanties'
    if transaction.category is None:
        if transaction.attributes['boekingsdatum'] >= chillberen_keulen_2019_start and transaction.attributes['boekingsdatum'] <= chillberen_keulen_2019_end:
            category['Vakanties'].transactions.append(transaction)
            transaction.category = 'Vakanties'

    # Categorisation based on keywords
    if transaction.category is None:
        for cat in category:
            if any(x.lower() in naam_tegenrekening for x in category[cat].keywords_naam_tegenrekening):
                category[cat].transactions.append(transaction)
                transaction.category = cat
                break
            if any(x.lower() in omschrijving for x in category[cat].keywords_omschrijving):
                category[cat].transactions.append(transaction)
                transaction.category = cat
                break

    # If none of the above methods yielded categorisation, add to category 'Geen categorie'
    if transaction.category is None:
        category['Geen categorie'].transactions.append(transaction)
