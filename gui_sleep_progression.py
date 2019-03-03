import matplotlib.pyplot as plt
import numpy as np
# GUI
from PyQt5.QtWidgets import *
import pyqtgraph as pg
import sys
# -- My Packages --
from read_from_file import read_from_file
from inner_dock import InnerDock
from pyqtgraph.dockarea import DockArea
from create_cmap import create_cmap
from app.pyqt_frequently_used import create_new_data_txt_box


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
        self.layout = self.init_layout()
        self.dock_area = self.create_dock_area()
        self.plot = self.init_plot()

        self.add_info_to_layout()
        # Add info
        self.init_data_from_file()
        self.plot_n_sleep_hours()

    def init_data_from_file(self):
        path = '/home/alex/Documents/improve_myself/sleeping_progression/sleep.csv'
        sleep_data = read_from_file(path)
        self.time_wake_up = sleep_data[:, 0]
        self.t = np.arange(len(self.time_wake_up))
        self.time_sleep = sleep_data[:, 1]
        self.w_or_wo_alarm = sleep_data[:, 2]
        self.working_hours = sleep_data[:, 3]
        self.sleepines_scale = sleep_data[:, 4] + 6
        self.time_go_to_bed = self.time_wake_up - self.time_sleep

    def init_layout(self):
        l = QGridLayout(self)
        pg.setConfigOption('background', 'w')
        pg.setConfigOptions(antialias=True)
        return l

    def create_dock_area(self):
        dock_area = DockArea()
        self.layout.addWidget(dock_area, 1, 0, 1, 6)
        return dock_area

    def init_plot(self):
        p = pg.PlotWidget()
        p.showGrid(x=True, y=True, alpha=0.5)
        p.setYRange(4, 14)
        plot_dock = InnerDock(
                self.layout, 'plot', b_pos=(0, 1), toggle_button=True)
        plot_dock.layout.addWidget(p)
        self.dock_area.addDock(plot_dock.dock)
        return p

    def add_info_to_layout(self):
        # create a Inner dock for the adding of new information for the day
        settings_d = InnerDock(
                self.layout, 'add info', b_pos=(0, 0), toggle_button=True,
                size=(1, 1))

        create_new_data_txt_box(settings_d.layout, 'Time wake up', pos=(0, 0))
        create_new_data_txt_box(settings_d.layout, 'Nb h sleep', pos=(2, 0))
        create_new_data_txt_box(settings_d.layout, 'Wake up w alarm', pos=(4, 0))
        create_new_data_txt_box(settings_d.layout, 'n h working', pos=(6, 0))
        create_new_data_txt_box(settings_d.layout, 'Sleepiness', pos=(8, 0))
        create_new_data_txt_box(settings_d.layout, 'Gym', pos=(10, 0))

        add_info_b = QPushButton('add info to csv')
        settings_d.layout.addWidget(add_info_b, 12, 0)

        self.dock_area.addDock(settings_d.dock, position='left')

    def plot_n_sleep_hours(self):
        # Plot
        self.plot_info(self.time_wake_up, pen_color='b')
        self.plot_info(self.time_sleep, pen_color=(255, 165, 0))
        # self.plot_time_sleep(sleepiness=True)
        self.plot_n_working_h()
        self.plot_w_or_wo_alarm()
        # Info
        self.print_sleep_info()

    def plot_n_working_h(self):
        self.plot.plot(
                self.t, self.working_hours, label='Working hours', pen='g')

    def plot_info(self, info_to_plot, pen_color):
        cmap = create_cmap(self.sleepines_scale)
        sleepiness_color = [pg.mkBrush(color) for color in cmap]
        self.plot.plot(
                self.t, info_to_plot, symbol='o', symbolSize=8,
                symbolBrush=sleepiness_color, label='Time wake up',
                pen=pen_color)

    def plot_w_or_wo_alarm(self):
        r = (255, 0, 0, 20)
        g = (0, 255, 0, 20)
        y = (229, 223, 0, 50)
        k = (0, 0, 0, 10)
        color = [g, y, r, k]
        self.w_or_wo_alarm[self.w_or_wo_alarm == -1] = 3
        for i, val in enumerate(self.w_or_wo_alarm):
            pen = pg.mkPen(color[int(val)], width=6)
            v_line = pg.InfiniteLine(i, pen=pen)
            self.plot.addItem(v_line)

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


def main():
    app = QApplication(sys.argv)
    m = MainWin()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()