import os
import sys
import csv
from datetime import datetime
import argparse

from modules.output_module import print_results
from modules.categorisation_module import categorize_transaction
from modules.keywords_module import add_tegenrekening_keywords, add_omschrijving_keywords
from modules.classes import Transaction, Category, DatetimeRange

# Required for relative imports to also work when called
# from project root directory.
sys.path.append(os.path.dirname(__file__))

def get_dates():
    requested_dates = []

    print('Enter desired dates in dd-mm-yyyy format.\nWhen finished, type "done".\n')
    while True:
        try:
            requested_date = input()
            if requested_date == 'done':
                break
            requested_date = datetime.strptime(requested_date, '%d-%m-%Y')
            requested_date = (requested_date, requested_date)
            requested_dates.append(requested_date)
        except:
            print('That\'s not the right format, please try again.')
    return requested_dates

def get_intervals():
    requested_intervals = []
    requested_intervals_fixed = []
    current_start = datetime(1, 1, 1, 0, 0)
    current_end = datetime(1, 1, 1, 0, 0)

    # Get user input of intervals
    print('Enter desired intervals in dd-mm-yyyy/dd-mm-yyyy format.\nWhen finished, type "done".')
    while True:
        try:
            requested_interval = input()
            if requested_interval == 'done':
                break
            (start_date, end_date) = (requested_interval[:10], requested_interval[-9:])
            start_date = datetime.strptime(start_date, '%d-%m-%Y')
            end_date = datetime.strptime(end_date, '%d-%m-%Y')
            requested_interval = DatetimeRange(start_date, end_date)
            requested_intervals.append(requested_interval)
        except:
            print('That\'s not the right format, please try again.')

    # Remove overlap to remove double counting inspired by https://codereview.stackexchange.com/a/21309
    for interval in requested_intervals:
        start = interval.start_date
        end = interval.end_date
        if start > current_end:
            # this segment starts after the last segment stops
            # just add a new segment
            requested_intervals_fixed.append(interval)
            current_start, current_end = start, end
        else:
            # segments overlap, replace
            if end > current_end:
                requested_intervals_fixed[-1] = DatetimeRange(current_start, end)
            # current_start already guaranteed to be lower
            current_end = max(current_end, end)

    return requested_intervals_fixed

def get_timespan():
    requested_dates = [DatetimeRange(datetime(1,1,1), datetime(9999,1,1))]

    if '--dates' in sys.argv:
        requested_dates = get_dates()

    if '--intervals' in sys.argv:
        requested_dates = get_intervals()

    return requested_dates
