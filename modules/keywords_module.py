
def create_keywords_naam_tegenrekening_dict():
    keywords_naam_tegenrekening = {}

    names = ['odekerken', 'keizer', 'mineur', 'h g poorthuis', 'j berends', 'mw kz lieverse', 'fj sloos']

    keywords_naam_tegenrekening['Totaal'] = []
    keywords_naam_tegenrekening['Eigen rekeningen'] = ['wa poorthuis', 'w.a. poorthuis', 'w a poorthuis', 'poorthuis w a', 'Ideaalsparen', 'ideaalsparen']
    keywords_naam_tegenrekening['DUO'] = ['DUO', 'duo']
    keywords_naam_tegenrekening['Boodschappen'] = ['albert heijn', 'jumbo', 'AH', 'McD', 'MCD']
    keywords_naam_tegenrekening['Kleding'] = ['veganwear']
    keywords_naam_tegenrekening['Media'] = ['steampowered', 'boekenroute', 'games']
    keywords_naam_tegenrekening['Reiskosten'] = ['ns groep', 'chipkaart', 'NS Utrecht', 'NS Reizigers', 'NS Rotterdam']
    keywords_naam_tegenrekening['Woning'] = ['donker', 'ssh']
    keywords_naam_tegenrekening['Drugs'] = []
    keywords_naam_tegenrekening['Cadeaus'] = ['foodelicious']
    keywords_naam_tegenrekening['Terugbetalingen'] = ['betaalverzoek', 'tikkie', 'abn amro bank nv'] + names
    keywords_naam_tegenrekening['Loon'] = ['driessen']
    keywords_naam_tegenrekening['Bijdrage familie'] = ['k mol', 'f.p.m. poorthuis', 'rooseboom']
    keywords_naam_tegenrekening['Belastingen'] = ['belastingdienst']
    keywords_naam_tegenrekening['Horeca'] = ['louis hartlooper', 'takeaway', 'thuisbezorgd']
    keywords_naam_tegenrekening['Feesten'] = {'ticketing',  'ticketswap'}
    keywords_naam_tegenrekening['Goede doelen'] = ['milieudefensie', 'wwf', 'hersenstichting']
    keywords_naam_tegenrekening['Vaste lasten'] = ['youfone', 'orca', 'paypal', 'Gemeente']
    keywords_naam_tegenrekening['Online bestellingen'] = ['bol', 'coolblue', 'allekabels', 'alloverpiercings', 'amazon', 'marktplaats']
    keywords_naam_tegenrekening['Zorg'] = ['unive', 'infomedics', 'fysiotherapie']
    keywords_naam_tegenrekening['Hobbies'] = []
    keywords_naam_tegenrekening['Vakanties'] = ['SUPERSTORE']
    keywords_naam_tegenrekening['Geen categorie'] = []

    return keywords_naam_tegenrekening

def create_keywords_omschrijving_dict():
    keywords_omschrijving = {}

    keywords_omschrijving['Totaal'] = []
    keywords_omschrijving['Eigen rekeningen'] = ['Eerste inleg']
    keywords_omschrijving['DUO'] = []
    keywords_omschrijving['Boodschappen'] = ['Jumbo', 'ALBERT HEIJN', 'AH', 'Albert Heijn', 'Lidl', 'Ekoplaza', 'PLUS', 'Natuurwinkel', 'ALBERTHEIJN', 'ALDI', 'Aldi', 'Coop', 'Netto', 'DIRK', 'SweetGreen', 'Spar', 'Boon\'s', 'Odin', 'McD', 'MCD', 'BOONS']
    keywords_omschrijving['Kleding'] = ['Vintage Island', 'De ARM', 'dump', 'DUMP', 'Episode', 'Book Center']
    keywords_omschrijving['Media'] = ['AKO', 'Broese', 'ROBBEDOES', 'BOEKHANDEL', 'LantarenVenster']
    keywords_omschrijving['Reiskosten'] = [ 'Fietsen', 'Fiets', 'BIKE', 'Bike', 'Centraal', 'Giant', 'NS-', 'NS Utrecht', 'NS Reizigers', 'NS Rotterdam']
    keywords_omschrijving['Woning'] = ['Huisgeld', 'Airbnb']
    keywords_omschrijving['Drugs'] = ['Pleasure', 'PLEASURE', 'CULTURE', 'ANDERSOM', 'State of Mind']
    keywords_omschrijving['Cadeaus'] = ['CASA', 'Kinderwin.Westerkade']
    keywords_omschrijving['Terugbetalingen'] = ['OVERBOEKING VIA INTERNET']
    keywords_omschrijving['Loon'] = ['SALARIS']
    keywords_omschrijving['Bijdrage familie'] = []
    keywords_omschrijving['Belastingen'] = ['RENTE']
    keywords_omschrijving['Horeca'] = ['Ledig Erf', 'Orca', 'Ekko', 'EKKO', 'GROTE ZAAL', 'Falafel City', 'Filmcafe', 'Orloff', 'Cafe', 'cafe', 'CAFE', 'Vegan', 'Dikke Dries', 'Smullers', 'Lunchroom', 'Manneken Pis', 'Eethuis', 'Ladage', 'eten', 'DONER', 'Una Mas', 'Poema', 'SLA', 'LaPlace', 'Pandje', 'Snackbar', 'Food Village', 'Barlow']
    keywords_omschrijving['Feesten'] = {'Festival', 'TIVOLI', 'TivoliVredenburg'}
    keywords_omschrijving['Goede doelen'] = []
    keywords_omschrijving['Vaste lasten'] = []
    keywords_omschrijving['Online bestellingen'] = []
    keywords_omschrijving['Zorg'] = ['fysiotherapie']
    keywords_omschrijving['Hobbies'] = ['Pipoos', 'Kathmandu']
    keywords_omschrijving['Vakanties'] = []
    keywords_omschrijving['Geen categorie'] = []


    return keywords_omschrijving
