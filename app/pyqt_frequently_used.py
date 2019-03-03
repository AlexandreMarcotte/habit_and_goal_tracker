from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from app.colors import *


def create_new_data_txt_box(layout, name, pos):
    if name is not None:
        l = create_txt_label(name)
        layout.addWidget(l, *pos)
    le = QLineEdit('')
    layout.addWidget(le, pos[0]+1, 0, 1, 1)


def create_txt_label(name):
    l = QLabel(name)
    l.setFrameShape(QFrame.Panel)
    l.setFrameShadow(QFrame.Sunken)
    l.setLineWidth(1)
    l.setAlignment(Qt.AlignCenter)
    l.setStyleSheet(f"""font-weight: 420; 
                        background-color: {label_grey}; 
                        font-size: 10pt;""")
    l.setMaximumHeight(26)
    return l

