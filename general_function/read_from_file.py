import numpy as np
from datetime import timedelta, datetime, date
import csv


def read_from_file(file_name):
    sleep_data = np.loadtxt(file_name, delimiter=',')
    return sleep_data


def read_from_file_and_add_date_to_new_file(file_name):
    today = date(2019, 3, 11)
    data_with_date = []
    sleep_data = np.loadtxt(file_name, delimiter=',')

    for i, d in enumerate(reversed(sleep_data)):
        d = list(d)
        d = [str(today - timedelta(days=i))] + d
        data_with_date.append(d)
    # reverse the data again
    data_with_date = data_with_date[::-1]

    with open('sleep.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(data_with_date)
    return sleep_data
