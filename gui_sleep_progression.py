import matplotlib.pyplot as plt
import numpy as np
# GUI
from PyQt5.QtWidgets import *
import pyqtgraph as pg
import sys
import draw_rectangle


class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.sleep_plot_widget = SleepPlotterWidget()
        self.setCentralWidget(self.sleep_plot_widget)
        self.show()

# CSV format to save in the same file:
# Time wake up | Nb h sleep | Wake up w alarm (1: True, 0: False) |
# n h working (-1: no data, ) | How awake I am throughout the day (see habit_test)
# | Gym (1:True; 0:False, -1:not recorded)

class SleepPlotterWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout, self.plot = self.init_layout_and_plot()
        self.init_data_from_file()
        self.plot_n_sleep_hours()

    def init_data_from_file(self):
        path = '/home/alex/Documents/improve_myself/sleeping_progression/sleep.csv'
        sleep_data = read_from_file(path)
        self.time_wake_up = sleep_data[:, 0]
        self.t = np.linspace(0, len(self.time_wake_up), len(self.time_wake_up))
        self.time_sleep = sleep_data[:, 1]
        self.w_or_wo_alarm = sleep_data[:, 2]
        self.working_hours = sleep_data[:, 3]
        self.sleepines_scale = sleep_data[:, 4] + 6
        self.time_go_to_bed = self.time_wake_up - self.time_sleep


    def init_layout_and_plot(self):
        layout = QGridLayout(self)
        pg.setConfigOption('background', 'w')
        pg.setConfigOptions(antialias=True)
        plot = pg.PlotWidget()
        plot.showGrid(x=True, y=True, alpha=0.5)
        plot.setYRange(4, 14)
        layout.addWidget(plot)
        return layout, plot

    def plot_n_sleep_hours(self):
        # Plot
        self.plot_info(self.time_wake_up, pen_color='b')
        self.plot_info(self.time_sleep, pen_color=(255, 165, 0))
        # self.plot_time_sleep(sleepiness=True)
        self.plot_n_working_h()
        self.plot_w_or_wo_alarm()
        # Info
        self.print_sleep_info()
        # Plot info
        # self.set_plot_info()
        plt.show()

    def set_plot_info(self):
        plt.title('Sleep patern over time')
        plt.minorticks_on()
        plt.xlabel('(n) days after removing internet at home')
        plt.ylabel('hours')
        plt.grid(which='both')
        plt.ylim(4, 14)
        # plt.legend()

    def create_cmap(self, z):
        cmap = plt.get_cmap('seismic')
        min_z = np.min(z)
        max_z = np.max(z)
        cmap = cmap((z - min_z)/(max_z - min_z))
        cmap[:, 3] = 0.8
        cmap *= 255
        return cmap

    def plot_n_working_h(self):
        self.plot.plot(
                self.t, self.working_hours, label='Working hours',
                pen='g')

    def plot_info(self, info_to_plot, pen_color, sleepiness=True):
        cmap = self.create_cmap(self.sleepines_scale)
        sleepiness_color = [pg.mkBrush(color) for color in cmap]
        self.plot.plot(
                self.t, info_to_plot, symbol='o', symbolSize=7,
                symbolBrush=sleepiness_color, label='Time wake up',
                pen=pen_color)

    def plot_w_or_wo_alarm(self):
        r = (255, 0, 0, 50)
        g = (0, 255, 0, 50)
        y = (249, 243, 0, 50)
        k = (0, 0, 0, 20)
        color = [r, y, g, k]
        self.w_or_wo_alarm[self.w_or_wo_alarm == -1] = 3
        colors = np.array([color[int(d)] for d in self.w_or_wo_alarm])

        n = 10
        spi = pg.ScatterPlotItem(
                size=100, pen=pg.mkPen(None), brush=pg.mkBrush(0, 255, 255, 120))
        # pos = np.random.normal(size=(2,n), scale=100)
        x = np.linspace(0, 100, n)
        y = np.zeros(n)
        pos = np.vstack((x, y))
        # pos = list(zip(x, y))

        spots = [{'pos': pos[:,i], 'data': 1, 'brush':pg.intColor(10),
                  'symbol': 1, 'size': 10.} for i in range(n)]


        # spots = [{'pos': pos[:,i], 'data': 1} for i in range(n)] + [{'pos': [0,0], 'data': 1}]
        spi.addPoints(spots)
        self.plot.addItem(spi)


        # squares = draw_rectangle.SquareItem(
        #         x=self.t.round(), y=np.zeros(len(self.t)),
        #         w=np.ones(len(self.t)), h=np.ones(len(self.t))*10)
        # self.plot.addItem(squares)
            # square = draw_rectangle.SquareItem(x=int(t), y=0, w=1, h=10, color=r)
            # self.plot.addItem(square)

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
    app = QApplication(sys.argv)
    m = MainWin()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()