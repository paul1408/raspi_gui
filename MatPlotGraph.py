from PyQt5.QtCore import QRect, QRectF, Qt
from PyQt5.QtGui import QColor, QPainter, QPalette, QPen, QFont, QPainterPath
from PyQt5 import QtCore, QtWidgets
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.animation as animation
import datetime

matplotlib.use('QT5Agg')

class GraphWidget(FigureCanvas):
    def __init__(self, parent=None, width=8, height=3, dpi=80):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.values = [0]
        self.times = [datetime.datetime.now().strftime('%S')]
        self.bgColor = '#373435'
        self.lineColor = '#92d500'
        self.gridColor = '#575757'
        matplotlib.rc('lines', linewidth=3, color=self.lineColor)
        matplotlib.rc('axes', facecolor=self.bgColor, edgecolor=self.gridColor, grid=True)
        matplotlib.rc('figure', facecolor=self.bgColor)
        matplotlib.rc('xtick', top=False, bottom=False, color=self.gridColor)
        matplotlib.rc('xtick.major', width=25)
        matplotlib.rc('xtick.minor', width=20)
        matplotlib.rc('ytick', left=False, right=False, color=self.gridColor)       

    def update_fig(self, val):
        self.values.append(val)
        self.times.append(datetime.datetime.now().strftime('%S'))
        if len(self.values) > 10:
            self.values.remove(self.values[0])
            self.times.remove(self.times[0])       
        
        self.axes.cla()
        self.axes.plot(self.times, self.values)
        self.draw()