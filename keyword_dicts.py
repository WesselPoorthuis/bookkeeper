import os
import sys
import csv
import collections

# Required for relative imports to also work when called
# from project root directory.
sys.path.append(os.path.dirname(__file__))

def create_keywords_naam_tegenrekening_dict():
    keywords_naam_tegenrekening = {}

    keywords_naam_tegenrekening['Overschrijving eigen rekeningen'] = ['wa poorthuis', 'w.a. poorthuis', 'w a poorthuis', 'poorthuis w a', 'Ideaalsparen', 'ideaalsparen']
    keywords_naam_tegenrekening['DUO'] = ['DUO', 'duo']
    keywords_naam_tegenrekening['Boodschappen'] = ['albert heijn', 'jumbo', 'AH', 'McD', 'MCD']
    keywords_naam_tegenrekening['Kleding'] = ['veganwear']
    keywords_naam_tegenrekening['Media'] = ['steampowered', 'boekenroute', 'games']
    keywords_naam_tegenrekening['Reiskosten'] = ['ns groep', 'chipkaart']
    keywords_naam_tegenrekening['Woning'] = ['donker', 'ssh']
    keywords_naam_tegenrekening['Drugs'] = []
    keywords_naam_tegenrekening['Cadeaus'] = ['foodelicious']
    keywords_naam_tegenrekening['Terugbetalingen'] = ['betaalverzoek', 'tikkie', 'abn amro bank nv', 'odekerken']
    keywords_naam_tegenrekening['Loon'] = ['driessen']
    keywords_naam_tegenrekening['Bijdrage familie'] = ['k mol', 'f.p.m. poorthuis', 'rooseboom']
    keywords_naam_tegenrekening['Belastingen'] = ['belastingdienst']
    keywords_naam_tegenrekening['Horeca'] = ['louis hartlooper', 'ticketing', 'takeaway', 'thuisbezorgd', 'ticketswap']
    keywords_naam_tegenrekening['Goede doelen'] = ['milieudefensie', 'wwf', 'hersenstichting']
    keywords_naam_tegenrekening['Vaste lasten'] = ['youfone', 'orca', 'paypal']
    keywords_naam_tegenrekening['Online bestellingen'] = ['bol', 'coolblue', 'allekabels', 'alloverpiercings']
    keywords_naam_tegenrekening['Geen categorie'] = []

    return keywords_naam_tegenrekening

def create_keywords_omschrijving_dict():
    keywords_omschrijving = {}

    keywords_omschrijving['Overschrijving eigen rekeningen'] = []
    keywords_omschrijving['DUO'] = []
    keywords_omschrijving['Boodschappen'] = ['Jumbo', 'ALBERT HEIJN', 'AH', 'Albert Heijn', 'Lidl', 'Ekoplaza', 'PLUS', 'Natuurwinkel', 'ALBERTHEIJN', 'ALDI', 'Aldi', 'Coop', 'Netto', 'DIRK', 'SweetGreen', 'Spar', 'Boon\'s', 'Odin', 'McD', 'MCD']
    keywords_omschrijving['Kleding'] = ['Vintage Island', 'De ARM', 'dump', 'DUMP', 'Episode']
    keywords_omschrijving['Media'] = ['AKO', 'Broese', 'ROBBEDOES', 'BOEKHANDEL']
    keywords_omschrijving['Reiskosten'] = [ 'Fietsen', 'Fiets', 'BIKE', 'Bike', 'Centraal', 'Giant']
    keywords_omschrijving['Woning'] = ['Huisgeld']
    keywords_omschrijving['Drugs'] = ['Pleasure', 'PLEASURE', 'CULTURE', 'ANDERSOM', 'State of Mind']
    keywords_omschrijving['Cadeaus'] = []
    keywords_omschrijving['Terugbetalingen'] = []
    keywords_omschrijving['Loon'] = ['SALARIS']
    keywords_omschrijving['Bijdrage familie'] = []
    keywords_omschrijving['Belastingen'] = ['RENTE']
    keywords_omschrijving['Horeca'] = ['Ledig Erf', 'Orca', 'Ekko', 'EKKO', 'GROTE ZAAL', 'Falafel City', 'Filmcafe', 'Orloff', 'Cafe', 'cafe', 'CAFE', 'LANTAREN', 'TIVOLI', 'Vegan', 'Dikke Dries', 'Smullers', 'Lunchroom', 'Manneken Pis', 'Eethuis', 'Ladage', 'eten', 'DONER', 'Una Mas', 'Poema', 'SLA', 'LaPlace', 'Pandje']
    keywords_omschrijving['Goede doelen'] = []
    keywords_omschrijving['Vaste lasten'] = []
    keywords_omschrijving['Online bestellingen'] = []
    keywords_omschrijving['Geen categorie'] = []


    return keywords_omschrijving
