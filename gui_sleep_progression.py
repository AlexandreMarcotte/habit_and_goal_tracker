


"""
class Tabs(QWidget):
    def __init__(self):
        super(Tabs, self).__init__()
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.gym_tab = QWidget()
        self.sleep_and_work_tab = QWidget()

        # Add tabs
        self.tabs.addTab(self.gym_tab, 'Sleep & work')
        self.tabs.addTab(self.sleep_and_work_tab, 'Gym')

        # Compose tabs
        self.create_gym_tab()
        self.create_sleep_and_work_tab()

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def create_gym_tab(self):
        self.tab1.layout = QGridLayout(self)
        self.tab1.setLayout(self.tab1.layout)

    def create_sleep_and_work_tab(self):
        # self.layout = QVBoxLayout(self)                                         # This line allowed me to set this object as the central widget (adding the word self to the function made it work)
        self.tab2.layout = QGridLayout(self)
        sleep_plotter_widget = SleepPlotterWidget(self.tabs.layout)
        # self.tab2.layout.addWidget(self.plot, 0, 0, 3, 2)
        # self.my_plot = ScrollingPlot(self.plot)
        # self.timer.timeout.connect(self.my_plot.update)
        self.tab2.setLayout(self.tab2.layout)


"""
