from PyQt5.QtCore import QRect, QRectF, Qt
from PyQt5.QtGui import QColor, QPainter, QPalette, QPen, QFont, QPainterPath
from PyQt5.QtWidgets import QWidget, QSizePolicy


class GraphWidget(QWidget):
    def __init__(self, parent=None):
        super(GraphWidget, self).__init__(parent)
        self.val = 0
        self.setBackgroundRole(QPalette.Base)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.greenColor = '#92d500'
        self.redColor = '#cd3301'
        self.bgColor = '#373435'
        self.lineColor = '#4a4a4a'
        self.padTop = 10
        self.padRight = 15
        self.padLeft = 30
        self.padDown = 20

        self.reset = True

        self.minY = 0
        self.maxY = 255
        self.deltaY = 50
        self.deltaT = 0.1
        self.updateT = 1
        self.maxT = 180
        self.counter = 0
        self.values = [0]

    def next_value(self, val):
        self.counter += self.deltaT
        if self.counter is self.updateT:
            self.counter = 0
            if len(self.values) is int(self.maxT/self.updateT):
                self.values.clear()
            self.values.append(val)

            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        if self.reset is True:
            self.reset = False
            self.draw_bg(painter)
            self.draw_axis_text(painter)
        self.draw_next_line(painter)

    def draw_bg(self, p):
        w = self.width()
        h = self.height()
        col = (w - self.padLeft - self.padRight)/3
        row = (h - self.padDown - self.padTop)/5
        p.setPen(QPen(QColor(self.bgColor), 10, Qt.SolidLine, Qt.FlatCap,
                    Qt.RoundJoin))
        p.fillRect(0, 0, self.width(), self.height(), QColor(self.bgColor))

        p.setPen(QPen(QColor(self.lineColor), 2, Qt.SolidLine, Qt.FlatCap,
                    Qt.RoundJoin))
        path = QPainterPath()
        path.moveTo(self.padLeft, self.padTop)
        path.lineTo(w - self.padRight, self.padTop)
        path.lineTo(w - self.padRight, h - self.padDown)
        path.lineTo(self.padLeft, h - self.padDown)
        path.lineTo(self.padLeft, self.padTop)
        path.moveTo(self.padLeft + col, self.padTop)
        path.lineTo(self.padLeft + col, h - self.padDown)
        path.moveTo(self.padLeft + col*2, self.padTop)
        path.lineTo(self.padLeft + col*2, h - self.padDown)
        path.moveTo(self.padLeft, self.padTop + row)
        path.lineTo(w - self.padRight, self.padTop + row)
        path.moveTo(self.padLeft, self.padTop + row*2)
        path.lineTo(w - self.padRight, self.padTop + row*2)
        path.moveTo(self.padLeft, self.padTop + row*3)
        path.lineTo(w - self.padRight, self.padTop + row*3)
        path.moveTo(self.padLeft, self.padTop + row*4)
        path.lineTo(w - self.padRight, self.padTop + row*4)
        p.drawPath(path)

    def draw_axis_text(self, p):
        w = self.width()
        h = self.height()
        col = (w - self.padLeft - self.padRight)/3
        row = (h - self.padDown - self.padTop)/5
        font = QFont()            
        font.setPixelSize(10)
        p.setFont(font)
        p.setPen(QPen(QColor(Qt.white), 2, Qt.SolidLine, Qt.FlatCap,
                 Qt.RoundJoin))
        p.drawText(QRect(5, self.padTop - 10, 20, 20), Qt.AlignHCenter, 'max')
        p.drawText(QRect(5, self.padTop + row - 10, 20, 20), Qt.AlignHCenter, '200')
        p.drawText(QRect(5, self.padTop + row*2 -10, 20, 20), Qt.AlignHCenter, '150')
        p.drawText(QRect(5, self.padTop + row*3 - 10, 20, 20), Qt.AlignHCenter, '100')
        p.drawText(QRect(5, self.padTop + row*4 - 10, 20, 20), Qt.AlignHCenter, '50')
        p.drawText(QRect(5, self.padTop + row*5 - 10, 20, 20), Qt.AlignHCenter, '0')
        p.drawText(QRect(self.padLeft - 30, h - self.padDown + 5, 50, 20), Qt.AlignHCenter, '00:00:00')
        p.drawText(QRect(self.padLeft - 30 + col, h - self.padDown + 5, 50, 20), Qt.AlignHCenter, '00:01:00')
        p.drawText(QRect(self.padLeft - 30 + col*2, h - self.padDown + 5, 50, 20), Qt.AlignHCenter, '00:02:00')
        p.drawText(QRect(self.padLeft - 30 + col*3, h - self.padDown + 5, 50, 20), Qt.AlignHCenter, '00:03:00')

    def draw_next_line(self, p):
        pass
