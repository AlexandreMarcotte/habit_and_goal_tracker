# GUI
from PyQt5.QtWidgets import *
import pyqtgraph as pg
# -- My Packages --
from general_function.inner_dock import InnerDock
from pyqtgraph.dockarea import DockArea
from app.pyqt_frequently_used import create_new_data_txt_box
from plot_manager import PlotManager


class SleepAndWorkTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = self.create_tab()

        self.tracked_categories = [
            'Time wake up', 'Nb h sleep', 'Wake up w alarm',
            'n h working', 'Sleepiness', 'Gym',]

        self.set_pg_configuration()
        self.dock_area = self.create_dock_area()
        # Plot
        self.plot_manager = PlotManager()
        self.plot_manager.plot_n_sleep_hours()
        self.plot_manager.plot_n_working_h()

        plot_dock = InnerDock(
            self.layout, 'show plot', b_pos=(0, 1), toggle_button=True)
        plot_dock.layout.addWidget(self.plot_manager.pw)
        self.dock_area.addDock(plot_dock.dock)

        self.add_txt_box_to_layout()

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

    def add_txt_box_to_layout(self):
        self.all_line_edit : [QLineEdit] = []
        # create a Inner dock for the adding of new information for the day
        settings_d = InnerDock(
                self.layout, 'add info', b_pos=(0, 0), toggle_button=True,
                size=(1, 1))

        for i, category in enumerate(self.tracked_categories):
            self.all_line_edit.append(
                    create_new_data_txt_box(
                            settings_d.layout, category, pos=(i*2, 0)))  # TODO: ALEXM Mettre le survey a la place de le faire moi meme?

        add_info_b = QPushButton('add info to csv')
        add_info_b.clicked.connect(self.save_new_info_to_file)
        settings_d.layout.addWidget(add_info_b, 12, 0)

        self.dock_area.addDock(settings_d.dock, position='left')

    def save_new_info_to_file(self):
        new_info = []
        for le in self.all_line_edit:
            new_info.append(le)
            print(le)



