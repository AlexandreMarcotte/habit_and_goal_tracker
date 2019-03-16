import numpy as np
from datetime import timedelta, datetime, date
import csv


def create_date_object(line):
    line = line[0].split('-')
    line = [int(v) for v in line]
    one_date = datetime(*line)
    return one_date


def read_from_file(file_name):
    sleep_data = []
    dates = []
    # sleep_data = np.loadtxt(file_name, delimiter=',')
    with open(file_name, 'r') as f:
        for line in f:
            line = line.strip().split(',')                   # TODO: ALEXM read the file as a csv instead

            dates.append(create_date_object(line))
            line = line[1:]  # Remove date data which is a string
            sleep_data.append(np.array([float(v) for v in line]))
        sleep_data = np.array(sleep_data)
    return dates, sleep_data


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
