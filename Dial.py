from PyQt5.QtCore import QRect, QRectF, QSize, Qt, QTimer
from PyQt5.QtGui import QColor, QPainter, QPalette, QPen, QFont
from PyQt5.QtWidgets import QWidget, QSizePolicy


class DialWidget(QWidget):
    def __init__(self, max, parent=None):
        super(DialWidget, self).__init__(parent)
        self.value = 0
        self.max = max
        self.setBackgroundRole(QPalette.Base)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.arcColor = '#92d500'
        self.greenColor = '#92d500'
        self.redColor = '#cd3301'
        self.grayColor = '#575757'
        self.dark_gray_color = '#1b1a1a'
        self.lineSize = 30
        self.size = 120

    def update_fig(self, val):
        if val > self.max:
            self.value = self.max
        else:
            self.value = val

        if self.value > self.max*0.5:
            self.arcColor = self.redColor
        else:
            self.arcColor = self.greenColor
        self.update()

    def paintEvent(self, event):
        x = self.width()/2 - self.size/2
        y = self.lineSize/2 + self.height()/2 - self.size/2
        # x -> [a,b] to y->[c,d]  :>   y=(x-a)(d-c)/(b-a)+c
        unghi = -220 * self.value / 255 + 200   # max = 255
        painter = QPainter(self)
        font = QFont("Roboto Condensed")
        font.setPixelSize(15)
        painter.setRenderHint(QPainter.Antialiasing, True)
        # painter.translate(self.width()/2, self.height()/2)
        painter.setPen(QPen(QColor(self.grayColor), self.lineSize, Qt.SolidLine, Qt.FlatCap,
                        Qt.RoundJoin))
        painter.drawArc(QRect(x, self.lineSize/2, self.size, self.size), -20 * 16, 220 * 16)
        painter.setPen(QPen(QColor(self.arcColor), self.lineSize, Qt.SolidLine, Qt.FlatCap,
                        Qt.RoundJoin))
        painter.drawArc(QRect(x, self.lineSize/2, self.size, self.size), unghi * 16, (200 - unghi) *16)
        painter.setPen(QPen(QColor(Qt.white), 10, Qt.SolidLine, Qt.FlatCap,
                        Qt.RoundJoin))
        font.setPixelSize(18)
        painter.setFont(font)
        # painter.drawText(QRect(x-10, self.height()-20, 20, 20), Qt.AlignHCenter, '0')
        #painter.drawText(QRect(x + self.size - 20, self.height()-20, 40, 40), Qt.AlignHCenter, '{}'.format(self.max))
        font.setPixelSize(20)
        painter.setFont(font)
        painter.drawText(QRect(self.width()/2-30, self.height()*2/3, 60, 30), Qt.AlignCenter, '{}'.format(self.value))
        painter.setPen(QPen(QColor(self.dark_gray_color), 2, Qt.SolidLine, Qt.FlatCap,
                            Qt.RoundJoin))
        painter.drawRoundedRect(QRect(self.width()/2-30, self.height()*2/3, 60, 30), 5.0, 5.0)
