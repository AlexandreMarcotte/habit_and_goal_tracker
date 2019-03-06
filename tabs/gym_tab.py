import pyqtgraph as pg
from PyQt5.QtWidgets import *


class GymTab(QWidget):
    def __init__(self):
        super().__init__()
        self.pg_layout = self.create_tab()

    def create_tab(self):
        layout = QHBoxLayout(self)
        pg_layout = pg.LayoutWidget()
        layout.addWidget(pg_layout)
        self.setLayout(layout)
        return pg_layout
