import matplotlib.pyplot as plt
import numpy as np
# GUI
from PyQt5.QtWidgets import *
import pyqtgraph as pg
# import sys
from datetime import datetime as dt
# -- My Packages --
from general_function.inner_dock import InnerDock
from pyqtgraph.dockarea import DockArea
from general_function.create_cmap import create_cmap
from app.pyqt_frequently_used import create_new_data_txt_box
from data import Data
from date_axis import DateAxis


class SleepAndWorkTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = self.create_tab()

        self.tracked_categories = [
            'Time wake up', 'Nb h sleep', 'Wake up w alarm',
            'n h working', 'Sleepiness', 'Gym',]

        self.set_pg_configuration()
        self.dock_area = self.create_dock_area()
        self.pw = self.init_plot()

        self.add_info_to_layout()
        # self.init_data_from_file()
        self.data = Data()
        self.data.print_data()
        self.plot_n_sleep_hours()
        self.plot_n_working_h()

    def create_tab(self):
        layout = QHBoxLayout(self)
        pg_layout = pg.LayoutWidget()
        layout.addWidget(pg_layout)
        self.setLayout(layout)
        return pg_layout

    def set_pg_configuration(self):
        pg.setConfigOption('background', 'w')
        pg.setConfigOptions(antialias=True)

    def create_dock_area(self):
        dock_area = DockArea()
        self.layout.addWidget(dock_area, 1, 0, 1, 6)
        return dock_area

    def init_plot(self):
        # date_axis = DateAxis(orientation='bottom')
        # vb = pg.ViewBox()
        # p = pg.PlotWidget(
        #         viewBox=vb, axisItems={'bottom': date_axis},
        #         enableMenu=False, title='Plot')
        p = pg.PlotWidget()
        p.showGrid(x=True, y=True, alpha=0.5)
        p.setYRange(4, 14)
        plot_dock = InnerDock(
                self.layout, 'show plot', b_pos=(0, 1), toggle_button=True)
        plot_dock.layout.addWidget(p)
        self.dock_area.addDock(plot_dock.dock)
        return p

    def add_info_to_layout(self):
        # create a Inner dock for the adding of new information for the day
        settings_d = InnerDock(
                self.layout, 'add info', b_pos=(0, 0), toggle_button=True,
                size=(1, 1))

        for i, category in enumerate(self.tracked_categories):
            create_new_data_txt_box(settings_d.layout, category, pos=(i*2, 0))  # TODO: ALEXM Mettre le survey a la place de le faire moi meme?

        add_info_b = QPushButton('add info to csv')
        settings_d.layout.addWidget(add_info_b, 12, 0)

        self.dock_area.addDock(settings_d.dock, position='left')

    def plot_n_sleep_hours(self):
        # Plot
        self.plot_info(self.data.time_wake_up, pen_color='b')
        self.plot_info(self.data.time_sleep, pen_color=(255, 165, 0))
        self.plot_w_or_wo_alarm()

    def plot_n_working_h(self):
        self.pw.plot(
                x=self.data.t, y=self.data.working_hours, label='Working hours', pen='g')
        # dates = [dt(2018, 1, 5), dt(2018, 3, 6)]  # Date is given by the number of second after 1970
        # y = [1, 6]
        # self.pw.plot(x=dates, y=y)

    def plot_info(self, info_to_plot, pen_color):
        cmap = create_cmap(self.data.sleepines_scale)
        sleepiness_color = [pg.mkBrush(color) for color in cmap]
        self.pw.plot(
                self.data.t, info_to_plot, symbol='o', symbolSize=8,
                symbolBrush=sleepiness_color, label='Time wake up',
                pen=pen_color)

    def plot_w_or_wo_alarm(self):
        r = (255, 0, 0, 20)  # Put these color in a COLOR file (And,, create namedtuple instead ?)
        g = (0, 255, 0, 20)
        y = (229, 223, 0, 50)
        k = (0, 0, 0, 10)
        color = [g, y, r, k]
        self.data.w_or_wo_alarm[self.data.w_or_wo_alarm == -1] = 3
        for i, val in enumerate(self.data.w_or_wo_alarm):
            pen = pg.mkPen(color[int(val)], width=6)
            v_line = pg.InfiniteLine(i, pen=pen)
            self.pw.addItem(v_line)

