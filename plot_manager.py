import pyqtgraph as pg
from general_function.create_cmap import create_cmap
from data import Data
from COLOR import *
from datetime import datetime as dt
from date_axis import DateAxis


class PlotManager:
    def __init__(self):
        date_axis = DateAxis(orientation='bottom')
        # vb = pg.ViewBox()
        # p = pg.PlotWidget(
        #         viewBox=vb, axisItems={'bottom': date_axis},
        #         enableMenu=False, title='Plot')
        # Create the data object by reading the data from file
        self.data = Data()
        self.data.print_data()
        self.pw = pg.PlotWidget()
        self.pw.showGrid(x=True, y=True, alpha=0.5)
        self.pw.setYRange(4, 14)

        self.add_sliding_region()

    def add_sliding_region(self):
        sliding_region = pg.LinearRegionItem([120, 130])
        sliding_region.setBrush((0, 255, 0, 5))
        self.pw.addItem(sliding_region)

    def plot_n_sleep_hours(self):
        # Plot
        self.plot_info(self.data.time_wake_up, pen_color='b')
        self.plot_info(self.data.time_sleep, pen_color=(255, 165, 0))
        self.plot_w_or_wo_alarm()

    def plot_n_working_h(self):
        self.pw.plot(
            x=self.data.t, y=self.data.working_hours, label='Working hours',
            pen='g')
        # dates = [dt(2018, 1, 5), dt(2018, 3, 6)]  # Date is given by the number of second after 1970
        # y = [1, 6]
        # self.pw.plot(x=dates, y=y)

    def plot_gym_sessions(self):
        self.pw.plot(
            self.data.t, self.data.gym_or_not*4, symbol='o', symbolSize=8,
            label='Gym or not', pen='k')

    def plot_info(self, info_to_plot, pen_color):
        cmap = create_cmap(self.data.sleepines_scale)
        sleepiness_color = [pg.mkBrush(color) for color in cmap]
        self.pw.plot(
            self.data.t, info_to_plot, symbol='o', symbolSize=8,
            symbolBrush=sleepiness_color, label='Time wake up',
            pen=pen_color)

    def plot_w_or_wo_alarm(self):
        color = [g, y, r, k]
        self.data.w_or_wo_alarm[self.data.w_or_wo_alarm == -1] = 3
        for i, val in enumerate(self.data.w_or_wo_alarm):
            pen = pg.mkPen(color[int(val)], width=6)
            v_line = pg.InfiniteLine(i, pen=pen)
            self.pw.addItem(v_line)
