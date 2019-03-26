import numpy as np
# --My Packages--
from general_function.read_from_file import read_from_file


class Data:
    def __init__(self):
        self.read_data()

    def read_data(self):
        path = '/home/alex/Documents/improve_myself/sleeping_progression/sleep.csv'
        self.dates, sleep_data = read_from_file(path)
        self.time_wake_up = sleep_data[:, 0]
        self.t = np.arange(len(self.time_wake_up))
        self.time_sleep = sleep_data[:, 1]
        self.w_or_wo_alarm = sleep_data[:, 2]
        self.working_hours = sleep_data[:, 3]
        self.sleepines_scale = sleep_data[:, 4] + 6
        self.gym_or_not = sleep_data[:, 5]
        self.time_go_to_bed = self.time_wake_up - self.time_sleep

    def print_data(self):
        # print('last 7 days work', self.working_hours[-8:-1])
        print('last week: ', np.sum(self.working_hours[-8:-1]))
        # Average time wake up
        median_time_wake_up = np.median(self.time_wake_up)
        print('Median time wake up: ', median_time_wake_up)
        # plt.axhline(median_time_wake_up, c='blue')
        # Average time spent sleeping
        non_zero_time_sleep = self.time_sleep[np.nonzero(self.time_sleep)]
        avg_time_sleep = np.average(non_zero_time_sleep[-7:])
        print('sleep last 40 days', non_zero_time_sleep[-7:])
        print('Average sleeping time (over the last two week): ', avg_time_sleep)
        print('n days', len(non_zero_time_sleep))
        # plt.axhline(avg_time_sleep, c='orange')
