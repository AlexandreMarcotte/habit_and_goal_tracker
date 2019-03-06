import matplotlib.pyplot as plt
import numpy as np
import os

# CSV format to save in the same file:
# Time wake up | Nb h sleep | Wake up w alarm (1: True, 0: False) |
# n h working (-1: no data, ) | How awake I am throughout the day (see habit_test)
# | Gym (1:True; 0:False, -1:not recorded)

class SleepPlotter():
    def __init__(self):
        path = '/home/alex/Documents/improve_myself/sleeping_progression/sleep.csv'
        sleep_data = read_from_file(path)
        self.time_wake_up = sleep_data[:, 0]
        self.t = np.linspace(0, len(self.time_wake_up), len(self.time_wake_up))
        self.time_sleep = sleep_data[:, 1]
        self.w_or_wo_alarm = sleep_data[:, 2]
        self.working_hours = sleep_data[:, 3]
        self.sleepines_scale = sleep_data[:, 4] + 6
        self.time_go_to_bed = self.time_wake_up - self.time_sleep

        self.plot_n_sleep_hours()

    def plot_n_sleep_hours(self):
        plt.figure(figsize=(12, 10), dpi=100, facecolor='w')
        # Plot
        self.plot_time_wake_up(sleepiness=True)
        self.plot_time_sleep(sleepiness=True)
        self.plot_n_working_h()
        self.plot_w_or_wo_alarm()
        # Info
        self.print_sleep_info()
        # Plot info
        self.set_plot_info()
        plt.show()

    def set_plot_info(self):
        plt.title('Sleep patern over time')
        plt.minorticks_on()
        plt.xlabel('(n) days after removing internet at home')
        plt.ylabel('hours')
        plt.grid(which='both')
        plt.ylim(4, 14)
        # plt.legend()

    def plot_n_working_h(self):
        plt.plot(self.t, self.working_hours, label='Working hours')

    def plot_time_wake_up(self, sleepiness=False):
        plt.plot(
            self.t, self.time_wake_up, label='Time wake up')
        if sleepiness:
            plt.scatter(
                self.t, self.time_wake_up, label='Time wake up', s=50,
                c=self.sleepines_scale, cmap='seismic')

    def plot_time_sleep(self, sleepiness=False):
        plt.plot(self.t, self.time_sleep, label='Sleep duration')
        if sleepiness:
            plt.scatter(
                self.t, self.time_sleep, label='Time wake up', s=50,
                c=self.sleepines_scale, cmap='seismic')

    def plot_w_or_wo_alarm(self):
        color = ['g', 'y', 'r']
        for t, val in zip(self.t, self.w_or_wo_alarm):
            if val == -1:
                c = 'k'
            else:
                c = color[int(val)]
            plt.axvline(t, c=c, alpha=0.15, linewidth=6)


    def print_sleep_info(self):
        # print('last 7 days work', self.working_hours[-8:-1])
        print('last week: ', np.sum(self.working_hours[-8:-1]))
        # Average time wake up
        median_time_wake_up = np.median(self.time_wake_up)
        print('Median time wake up: ', median_time_wake_up)
        # plt.axhline(median_time_wake_up, c='blue')
        # Average time spent sleeping
        non_zero_time_sleep = self.time_sleep[np.nonzero(self.time_sleep)]
        avg_time_sleep = np.average(non_zero_time_sleep[-50:])
        print('sleep last 40 days', non_zero_time_sleep[-50:])
        print('Average sleeping time (over the last 40 days): ', avg_time_sleep)
        print('n days', len(non_zero_time_sleep))
        plt.axhline(avg_time_sleep, c='orange')


def read_from_file(file_name):
    sleep_data = np.loadtxt(file_name, delimiter=',')
    return sleep_data


def main():
    sp = SleepPlotter()

if __name__ == '__main__':
    main()
