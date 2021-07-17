from datetime import datetime, timedelta
from functools import reduce
import operator

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

"""
:authors: python273
:license: Apache License, Version 2.0
:copyright: (c) 2018 python273
"""

class DatetimeRange:
    def __init__(self, start_date, end_date):
        if end_date < start_date:
            raise ValueError('{!r} < {!r}'.format(end_date, start_date))

        self.start_date = start_date
        self.end_date = end_date

    def __contains__(self, date):
        """ (start_date, end_date] """
        return self.start_date <= date < self.end_date

    def __eq__(self, other):
        return (
            (self.start_date == other.start_date) and
            (self.end_date == other.end_date)
        )

    def __and__(self, other):
        """ Return overlapping range for dr1 & dr2. """

        dates = sorted([
            self.start_date,
            self.end_date,
            other.start_date,
            other.end_date
        ])

        if self.end_date < other.start_date or self.start_date > other.end_date:
            return

        return DatetimeRange(dates[1], dates[2])

    def __sub__(self, other):
        """ Return list with ranges """
        intersection = self & other

        if intersection is None:
            return [self]

        result = []

        if intersection.start_date != self.start_date:
            result.append(DatetimeRange(self.start_date, intersection.start_date))

        if intersection.end_date != self.end_date:
            result.append(DatetimeRange(intersection.end_date, self.end_date))

        return result

    @property
    def delta(self):
        return self.end_date - self.start_date

    def __repr__(self):
        return '<DatetimeRange({!r}, {!r}>'.format(
            self.start_date, self.end_date
        )


def coverage(primary_range, sub_ranges):
    left = [primary_range]

    for sub_range in sub_ranges:
        new_left = []

        for left_range in left:
            new_left.extend(left_range - sub_range)

        left = new_left

        if not left:
            break

    delta_left = reduce(
        operator.add,
        (i.delta for i in left),
        timedelta()
    )

    return primary_range.delta - delta_left
