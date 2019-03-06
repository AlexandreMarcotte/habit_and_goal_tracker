# --General Packages--
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget
# --My Packages--
from tabs.gym_tab import GymTab
from tabs.sleep_and_work_tab import SleepAndWorkTab


class TabWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.tabs_list = {
            SleepAndWorkTab(): 'Sleep & work',
            GymTab(): 'Gym',
        }

        self.layout = QVBoxLayout(self)
        # Initialize tab screen
        self.tabs = QTabWidget()
        # Add tabs
        for tab, name in self.tabs_list.items():
            self.tabs.addTab(tab, name)
        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
