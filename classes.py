
class Transaction:

    def __init__(self, attributes):
        self.attributes = attributes
        self.category = None

class Category:

    def __init__(self):
        self.transactions = []
        self.keywords = []

    def calc_in_out(self):
        flow_in = 0
        flow_out = 0
        for transaction in self.transactions:
            if transaction.attributes['bedrag'].startswith('-'):
                flow_out += map(float, transaction.attributes['bedrag'])
            else:
                flow_in += map(float, transaction.attributes['bedrag'])
        return (flow_in,flow_out)
