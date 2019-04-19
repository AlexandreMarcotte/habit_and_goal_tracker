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
        self.sleepines_scale = sleep_data[:, 4]

        # Moving averages
        DAYS_OF_MV_AVG = 7
        self.sleepines_scale_mv_avg = self.moving_average(
            abs(11 - self.sleepines_scale), DAYS_OF_MV_AVG)
        self.time_sleep_mv_avg = self.moving_average(
                self.time_sleep, DAYS_OF_MV_AVG)
        self.gym_or_not = sleep_data[:, 5]
        # Time go to bed
        self.time_go_to_bed = self.time_wake_up - self.time_sleep + 24

    """
    def moving_average_conv(self, data, avg_len):
        # TODO: ALEXM improve by padding both side with same before starting
        # Calculating the moving average
        avg_data = np.convolve(data, np.ones(avg_len), 'valid') / avg_len
        # Pad the moving average
        avg_data = list(avg_data)
        for _ in range(avg_len-1):
            # avg_data.append(0)
            avg_data.insert(0, 0)
        return avg_data
    """
    def moving_average(self, data, avg_len):
        # So that data is a copy and not a pointer to data
        data = np.array(data)
        # Last point wrong in the case of sleepiness scale (therefore remove it)
        data[-1] = data[-2]
        mv_avg = []
        # correct the padding when odd number of moving average
        pad = 0
        if avg_len % 2 == 1:  # odd
            pad = 1
        pad_data = np.pad(data, (avg_len//2, avg_len//2 + pad), 'edge')
        for i in range(len(data)):
            mv_avg.append(np.mean(pad_data[i:i+avg_len]))
        mv_avg = np.array(mv_avg)
        return mv_avg

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
