
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
