import numpy as np


def read_from_file(file_name):
    sleep_data = np.loadtxt(file_name, delimiter=',')
    return sleep_data
