
class Transaction:

    def __init__(self, attributes):
        self.attributes = attributes
        self.category = None

class Category:

    def __init__(self, name):
        self.name = name
        self.transactions = []
        self.keywords_naam_tegenrekening = []
        self.keywords_omschrijving = []

    def calculate_flows(self):
        flow_in = 0
        flow_out = 0
        for transaction in self.transactions:
            if transaction.attributes['bedrag'] < 0:
                flow_out += transaction.attributes['bedrag']
            else:
                flow_in += transaction.attributes['bedrag']
        return (flow_in,flow_out)

    def get_transactions_by_date(date):
        for i in range(0,100):
            while True:
                try:
                    datetime.strptime(date, '%d-%m-%Y')
                except NameError:
                    print('Please enter date in dd-mm-yyyy format')
                    continue
                break

    # can define a function to retrieve transactions between certain dates
