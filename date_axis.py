import pyqtgraph as pg
from pyqtgraph.Qt import QtGui
import time
from datetime import datetime
from datetime import datetime as dt


class DateAxis(pg.AxisItem):
    def tickStrings(self, values, scale, spacing):
        strns = []
        rng = max(values)-min(values)
        if rng < 3600*24:
            string = '%H:%M:%S'
            label1 = '%b %d -'
            label2 = ' %b %d, %Y'
        elif rng >= 3600*24 and rng < 3600*24*30:
            string = '%d'
            label1 = '%b - '
            label2 = '%b, %Y'
        elif rng >= 3600*24*30 and rng < 3600*24*30*24:
            string = '%b'
            label1 = '%Y -'
            label2 = ' %Y'
        elif rng >=3600*24*30*24:
            string = '%Y'
            label1 = ''
            label2 = ''
        for x in values:
            try:
                strns.append(time.strftime(string, time.localtime(x)))
            except ValueError:  # Windows can't handle dates before 1970
                strns.append('')
        try:
            label = time.strftime(
                    label1, time.localtime(min(values))) \
                  + time.strftime(label2, time.localtime(max(values)))
        except ValueError:
            label = ''
        return strns
