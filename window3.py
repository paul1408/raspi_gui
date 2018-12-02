from PyQt5.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QStackedWidget
from PyQt5.QtCore import pyqtSlot, Qt, pyqtSignal
from PyQt5.QtGui import QPalette, QPixmap, QFontDatabase, QPainter, QColor, QMovie, QFont
from Dial import DialWidget
from thread_list import BgThread


# ### TO DO
# * clock label not updating on other pages except METER
# * implement rest of the pages
# ##################################################################

class Window(QWidget):
    bgWork: BgThread
    clk_stop_signal = pyqtSignal()
    bg_stop_signal = pyqtSignal()
    fan_signal = pyqtSignal()
    rec_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.val_list = [0]
        self.dial = [DialWidget(100)] * 8
        self.sensor_name_list = ['General Combustible Gas', 'Alcohol',
                                 'Natural Gas, Methane', 'LPG, Natural Gas, Coal Gas', 'LPG, Propane',\
                                 'Carbon Monoxide', 'Hydrogen', 'Air Quality Control']
        self.sensor_pixmap = ['mq2.png', 'mq3.png', 'mq4.png', 'mq5.png',
                              'mq6.png', 'mq7.png', 'mq8.png', 'mq135.png']
        self.sensor_max_list = [255, 255, 255, 255, 255, 255, 255, 255]
        self.sensor_rec_list = [0, 0, 0, 0, 0, 0, 0, 0]
        self.fan_powered = True
        self.connected = False
        self.recording = False
        self.title = 'Telemetrie'
        self.current_page = 0
        self.left = 100
        self.top = 100
        self.width = 1024
        self.height = 600
        self.black_color = '#000000'
        self.gray_color = '#373435'
        self.dark_gray_color = '#1b1a1a'
        self.green_color = '#92d500'
        self.blue_color = '#1bb2bb'
        self.dark_blue_color = '#2e679d'
        self.green_color = '#92d400'
        self.red_color = '#cd3301'
        self.white_color = '#FFFFFF'
        self.font_gray_color = '#828486'
        self.fan_anim = QMovie('res/pack/gas_icon_fan_on.gif')
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        id = QFontDatabase.addApplicationFont('res/font/BreuerText-Regular.ttf')
        # font = QFont(QFontDatabase.applicationFontFamilies(id)[0])
        self.setStyleSheet('background-color:black; font-family: BreuerText')

        # stack pages: 0 - main menu, 1 - meter, 2 - data, 3 - config, 4 - help
        self.page_nr = 5
        self.pages = list()
        for p in range(self.page_nr):
            self.pages.append(QWidget())
        # ######### PAGE 0 MAIN
        self.layout_0 = QVBoxLayout()
        self.layout_0.setContentsMargins(0, 0, 0, 0)

        self.title_box1_0 = QHBoxLayout()
        self.title_box1_0.setContentsMargins(0, 0, 0, 0)

        self.defend_txt_0 = QLabel()
        self.defend_txt_0.setText('DEFEND Gas Sensor Data Fusion')
        self.defend_txt_0.setStyleSheet(
            'font-size: 18px; padding:0px 0px 0px 0px; color: %s;height:20px' % self.font_gray_color)
        self.title_box1_0.addWidget(self.defend_txt_0)

        self.title_box1_0.addSpacing(15)

        self.menu_grid_txt_0 = QGridLayout()
        self.menu_grid_txt_0.setContentsMargins(0, 0, 0, 0)
        self.menu_grid_txt_0.setSpacing(0)

        self.menu_label_txt_0 = QLabel()
        self.menu_label_txt_0.setText('METER')
        self.menu_label_txt_0.setStyleSheet(
            'font-size: 18px;padding: 0px 33px 0px 28px; color: %s;' % self.font_gray_color)
        self.menu_grid_txt_0.addWidget(self.menu_label_txt_0, 0, 0)

        self.uart_label_txt_0 = QLabel()
        self.uart_label_txt_0.setText('DATA')
        self.uart_label_txt_0.setStyleSheet(
            'font-size: 18px;padding: 0px 35px 0px 35px; color: %s;' % self.font_gray_color)
        self.menu_grid_txt_0.addWidget(self.uart_label_txt_0, 0, 1)

        self.data_label_txt_0 = QLabel()
        self.data_label_txt_0.setText('UART')
        self.data_label_txt_0.setStyleSheet(
            'font-size: 18px;padding: 0px 40px 0px 40px; color: %s;' % self.font_gray_color)
        self.menu_grid_txt_0.addWidget(self.data_label_txt_0, 0, 2)

        self.fan_label_txt_0 = QLabel()
        self.fan_label_txt_0.setText('FAN')
        self.fan_label_txt_0.setStyleSheet(
            'font-size: 18px;padding: 0px 45px 0px 40px; color: %s;' % self.font_gray_color)
        self.menu_grid_txt_0.addWidget(self.fan_label_txt_0, 0, 3)

        self.title_box1_0.addLayout(self.menu_grid_txt_0)

        self.title_box1_0.addSpacing(15)

        self.gmt_label_0 = QLabel()
        self.gmt_label_0.setText('GMT +2')
        self.gmt_label_0.setStyleSheet('font-size: 18px;padding: 0px 0px 0px 90px; color: %s;' % self.font_gray_color)

        self.title_box1_0.addWidget(self.gmt_label_0)

        self.layout_0.addLayout(self.title_box1_0)

        self.title_box2_0 = QHBoxLayout()  # second title box with pixmaps
        self.title_box2_0.setContentsMargins(0, 0, 0, 0)
        self.title_box2_0.setSpacing(0)

        self.frame1_0 = QFrame()
        self.frame1_0.setFixedWidth(240)
        self.frame1_0.setFixedHeight(80)
        self.frame1_0.setStyleSheet('background-color:%s; border: 0px; border-radius: 10px;' % self.dark_gray_color)
        self.defend_pix_0 = QLabel(self.frame1_0)
        self.defend_pix_0.setPixmap(QPixmap('res/pack/defend.png'))
        self.defend_pix_0.setFixedWidth(240)
        self.defend_pix_0.setAlignment(Qt.AlignCenter)
        self.title_box2_0.addWidget(self.frame1_0)

        self.title_box2_0.addSpacing(15)

        self.frame2_0 = QFrame()
        self.frame2_0.setStyleSheet('background-color:%s; border: 0px; border-radius: 10px;' % self.dark_gray_color)
        self.frame2_0.setFixedWidth(495)
        self.frame2_0.setFixedHeight(80)

        self.menu_grid_pix_0 = QGridLayout(self.frame2_0)
        self.menu_grid_pix_0.setContentsMargins(0, 0, 0, 0)
        self.menu_grid_pix_0.setSpacing(0)

        self.menu_label_pix_0 = QLabel()
        self.menu_label_pix_0.setPixmap(QPixmap('res/pack/gas_icon_meter.png'))
        self.menu_label_pix_0.setStyleSheet('padding: 5px 30px 0px 30px;')
        self.menu_label_pix_0.mousePressEvent = self.select_menu_meter
        self.menu_grid_pix_0.addWidget(self.menu_label_pix_0, 0, 0)

        self.uart_label_pix_0 = QLabel()
        self.uart_label_pix_0.setPixmap(QPixmap('res/pack/gas_icon_data.png'))
        self.uart_label_pix_0.setStyleSheet('padding: 5px 30px 0px 30px;')
        self.uart_label_pix_0.mousePressEvent = self.select_menu_data
        self.menu_grid_pix_0.addWidget(self.uart_label_pix_0, 0, 1)

        self.data_label_pix_0 = QLabel()
        self.data_label_pix_0.setPixmap(QPixmap('res/pack/gas_icon_UART.png'))
        self.data_label_pix_0.setStyleSheet('padding: 5px 30px 0px 30px;')
        self.data_label_pix_0.mousePressEvent = self.select_menu_config
        self.menu_grid_pix_0.addWidget(self.data_label_pix_0, 0, 2)

        self.fan_label_pix_0 = QLabel()
        self.fan_label_pix_0.setMovie(self.fan_anim)
        self.fan_label_pix_0.setStyleSheet('padding: 5px 30px 0px 30px;')
        self.fan_label_pix_0.mousePressEvent = self.toggle_fan
        self.menu_grid_pix_0.addWidget(self.fan_label_pix_0, 0, 3)

        self.title_box2_0.addWidget(self.frame2_0)

        self.title_box2_0.addSpacing(15)

        self.frame3_0 = QFrame()
        self.frame3_0.setStyleSheet('background-color:%s; border: 0px; border-radius: 10px;' % self.dark_gray_color)
        self.frame3_0.setFixedWidth(240)
        self.frame3_0.setFixedHeight(80)

        self.clock_box_0 = QHBoxLayout(self.frame3_0)
        self.time_label_pix_0 = QLabel()
        self.time_label_pix_0.setPixmap(QPixmap('res/pack/clock.png'))
        self.time_label_txt_0 = QLabel()
        self.time_label_txt_0.setText('00:00:00')
        self.time_label_txt_0.setStyleSheet('font-size: 40px; color: %s' % self.white_color)
        self.clock_box_0.addWidget(self.time_label_pix_0)
        self.clock_box_0.addWidget(self.time_label_txt_0)
        self.title_box2_0.addWidget(self.frame3_0)

        self.layout_0.addLayout(self.title_box2_0)

        label0 = QLabel()
        label0.setText('Main menu')
        label0.setStyleSheet('font-size: 24px;padding: 0px 0px 0px 90px; color: %s;' % self.font_gray_color)
        self.layout_0.addWidget(label0)

        self.layout_0.addStretch()

        self.pages[0].setLayout(self.layout_0)
        # #################### END PAGE 0

        # ######### PAGE 1 METER
        self.layout_1 = QVBoxLayout()
        self.layout_1.setContentsMargins(0, 0, 0, 0)

        self.title_box1_1 = QHBoxLayout()
        self.title_box1_1.setContentsMargins(0, 0, 0, 0)

        self.defend_txt_1 = QLabel()
        self.defend_txt_1.setText('DEFEND Gas Sensor Data Fusion')
        self.defend_txt_1.setStyleSheet('font-size: 18px; padding:0px 0px 0px 0px; color: %s;height:20px' % self.font_gray_color)
        self.title_box1_1.addWidget(self.defend_txt_1)

        self.title_box1_1.addSpacing(15)

        self.menu_grid_txt_1 = QGridLayout()
        self.menu_grid_txt_1.setContentsMargins(0, 0, 0, 0)
        self.menu_grid_txt_1.setSpacing(0)

        self.menu_label_txt_1 = QLabel()
        self.menu_label_txt_1.setText('MENU')
        self.menu_label_txt_1.setStyleSheet('font-size: 18px;padding: 0px 35px 0px 30px; color: %s;' % self.font_gray_color)
        self.menu_grid_txt_1.addWidget(self.menu_label_txt_1, 0, 0)

        self.uart_label_txt_1 = QLabel()
        self.uart_label_txt_1.setText('UART')
        self.uart_label_txt_1.setStyleSheet('font-size: 18px;padding: 0px 35px 0px 35px; color: %s;' % self.font_gray_color)
        self.menu_grid_txt_1.addWidget(self.uart_label_txt_1, 0, 1)

        self.data_label_txt_1 = QLabel()
        self.data_label_txt_1.setText('DATA')
        self.data_label_txt_1.setStyleSheet('font-size: 18px;padding: 0px 40px 0px 40px; color: %s;' % self.font_gray_color)
        self.menu_grid_txt_1.addWidget(self.data_label_txt_1, 0, 2)

        self.fan_label_txt_1 = QLabel()
        self.fan_label_txt_1.setText('FAN')
        self.fan_label_txt_1.setStyleSheet('font-size: 18px;padding: 0px 45px 0px 40px; color: %s;' % self.font_gray_color)
        self.menu_grid_txt_1.addWidget(self.fan_label_txt_1, 0, 3)

        self.title_box1_1.addLayout(self.menu_grid_txt_1)

        self.title_box1_1.addSpacing(15)

        self.gmt_label_1 = QLabel()
        self.gmt_label_1.setText('GMT +2')
        self.gmt_label_1.setStyleSheet('font-size: 18px;padding: 0px 0px 0px 90px; color: %s;' % self.font_gray_color)

        self.title_box1_1.addWidget(self.gmt_label_1)

        self.layout_1.addLayout(self.title_box1_1)

        self.title_box2_1 = QHBoxLayout()   # second title box with pixmaps
        self.title_box2_1.setContentsMargins(0, 0, 0, 0)
        self.title_box2_1.setSpacing(0)

        self.frame1_1 = QFrame()
        self.frame1_1.setFixedWidth(240)
        self.frame1_1.setFixedHeight(80)
        self.frame1_1.setStyleSheet('background-color:%s; border: 0px; border-radius: 10px;' % self.dark_gray_color)
        self.defend_pix_1 = QLabel(self.frame1_1)
        self.defend_pix_1.setPixmap(QPixmap('res/pack/defend.png'))
        self.defend_pix_1.setFixedWidth(240)
        self.defend_pix_1.setAlignment(Qt.AlignCenter)
        self.title_box2_1.addWidget(self.frame1_1)

        self.title_box2_1.addSpacing(15)

        self.frame2_1 = QFrame()
        self.frame2_1.setStyleSheet('background-color:%s; border: 0px; border-radius: 10px;' % self.dark_gray_color)
        self.frame2_1.setFixedWidth(495)
        self.frame2_1.setFixedHeight(80)

        self.menu_grid_pix_1 = QGridLayout(self.frame2_1)
        self.menu_grid_pix_1.setContentsMargins(0, 0, 0, 0)
        self.menu_grid_pix_1.setSpacing(0)

        self.menu_label_pix_1 = QLabel()
        self.menu_label_pix_1.setPixmap(QPixmap('res/pack/gas_icon_main_menu.png'))
        self.menu_label_pix_1.setStyleSheet('padding: 5px 30px 0px 30px;')
        self.menu_label_pix_1.mousePressEvent = self.select_menu_main
        self.menu_grid_pix_1.addWidget(self.menu_label_pix_1, 0, 0)

        self.uart_label_pix_1 = QLabel()
        self.uart_label_pix_1.setPixmap(QPixmap('res/pack/gas_icon_UART.png'))
        self.uart_label_pix_1.setStyleSheet('padding: 5px 30px 0px 30px;')
        self.uart_label_pix_1.mousePressEvent = self.select_menu_config
        self.menu_grid_pix_1.addWidget(self.uart_label_pix_1, 0, 1)

        self.data_label_pix_1 = QLabel()
        self.data_label_pix_1.setPixmap(QPixmap('res/pack/gas_icon_data.png'))
        self.data_label_pix_1.setStyleSheet('padding: 5px 30px 0px 30px;')
        self.data_label_pix_1.mousePressEvent = self.select_menu_data
        self.menu_grid_pix_1.addWidget(self.data_label_pix_1, 0, 2)

        self.fan_label_pix_1 = QLabel()
        self.fan_label_pix_1.setMovie(self.fan_anim)
        self.fan_label_pix_1.setStyleSheet('padding: 5px 30px 0px 30px;')
        self.fan_label_pix_1.mousePressEvent = self.toggle_fan
        self.menu_grid_pix_1.addWidget(self.fan_label_pix_1, 0, 3)

        self.title_box2_1.addWidget(self.frame2_1)

        self.title_box2_1.addSpacing(15)

        self.frame3_1 = QFrame()
        self.frame3_1.setStyleSheet('background-color:%s; border: 0px; border-radius: 10px;' % self.dark_gray_color)
        self.frame3_1.setFixedWidth(240)
        self.frame3_1.setFixedHeight(80)

        self.clock_box_1 = QHBoxLayout(self.frame3_1)
        self.time_label_pix_1 = QLabel()
        self.time_label_pix_1.setPixmap(QPixmap('res/pack/clock.png'))
        self.time_label_txt_1 = QLabel()
        self.time_label_txt_1.setText('00:00:00')
        self.time_label_txt_1.setStyleSheet('font-size: 40px; color: %s' % self.white_color)
        self.clock_box_1.addWidget(self.time_label_pix_1)
        self.clock_box_1.addWidget(self.time_label_txt_1)
        self.title_box2_1.addWidget(self.frame3_1)

        self.layout_1.addLayout(self.title_box2_1)

        self.sensorsGrid = QGridLayout()
        self.sensorsGrid.setContentsMargins(0, 10, 0, 0)
        self.sensorsGrid.setSpacing(15)
        for j in range(0, 2):
            for k in range(0, 4):
                self.frame = QFrame(self)
                self.frame.setStyleSheet('background-color:%s;' % self.gray_color)
                self.cell = QVBoxLayout(self.frame)
                self.cell.setContentsMargins(0, 0, 0, 0)

                self.sensorLabel = QLabel()
                self.sensorLabel.setText(self.sensor_name_list[k+4*j])
                self.sensorLabel.setStyleSheet('font-size: 18px;padding: 10px 0px 0px 0px; color: %s;' % self.white_color)
                self.sensorLabel.setAlignment(Qt.AlignHCenter)

                self.dial[k+4*j] = DialWidget(self.sensor_max_list[k+4*j])
                self.dial[k+4*j].setFixedHeight(100)
                self.dial[k+4*j].setMinimumWidth(170)

                self.modelTxtLabel = QLabel()
                self.modelTxtLabel.setPixmap(QPixmap('res/pack/gas_icon_{}'.format(self.sensor_pixmap[k+4*j])))
                self.modelTxtLabel.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
                self.modelTxtLabel.mousePressEvent = lambda ev, nr = k+4*j: self.select_menu_help(nr)

                self.cell.addWidget(self.sensorLabel)
                self.cell.addWidget(self.dial[k+4*j])
                self.cell.addWidget(self.modelTxtLabel)
                self.sensorsGrid.addWidget(self.frame, j, k)

        # self.layout1.addLayout(self.titleGridtext1)

        self.layout_1.addLayout(self.sensorsGrid)

        self.pages[1].setLayout(self.layout_1)
        # ################### END PAGE 1

        # ######### PAGE 2 DATA
        self.layout_2 = QVBoxLayout()
        self.layout_2.setContentsMargins(0, 0, 0, 0)

        self.title_box1_2 = QHBoxLayout()
        self.title_box1_2.setContentsMargins(0, 0, 0, 0)

        self.defend_txt_2 = QLabel()
        self.defend_txt_2.setText('DEFEND Gas Sensor Data Fusion')
        self.defend_txt_2.setStyleSheet(
            'font-size: 18px; padding:0px 0px 0px 0px; color: %s;height:20px' % self.font_gray_color)
        self.title_box1_2.addWidget(self.defend_txt_2)

        self.title_box1_2.addSpacing(15)

        self.menu_grid_txt_2 = QGridLayout()
        self.menu_grid_txt_2.setContentsMargins(0, 0, 0, 0)
        self.menu_grid_txt_2.setSpacing(0)

        self.menu_label_txt_2 = QLabel()
        self.menu_label_txt_2.setText('MENU')
        self.menu_label_txt_2.setStyleSheet(
            'font-size: 18px;padding: 0px 35px 0px 30px; color: %s;' % self.font_gray_color)
        self.menu_grid_txt_2.addWidget(self.menu_label_txt_2, 0, 0)

        self.uart_label_txt_2 = QLabel()
        self.uart_label_txt_2.setText('UART')
        self.uart_label_txt_2.setStyleSheet(
            'font-size: 18px;padding: 0px 35px 0px 35px; color: %s;' % self.font_gray_color)
        self.menu_grid_txt_2.addWidget(self.uart_label_txt_2, 0, 1)

        self.data_label_txt_2 = QLabel()
        self.data_label_txt_2.setText('METER')
        self.data_label_txt_2.setStyleSheet(
            'font-size: 18px;padding: 0px 40px 0px 40px; color: %s;' % self.font_gray_color)
        self.menu_grid_txt_2.addWidget(self.data_label_txt_2, 0, 2)

        self.fan_label_txt_2 = QLabel()
        self.fan_label_txt_2.setText('FAN')
        self.fan_label_txt_2.setStyleSheet(
            'font-size: 18px;padding: 0px 45px 0px 40px; color: %s;' % self.font_gray_color)
        self.menu_grid_txt_2.addWidget(self.fan_label_txt_2, 0, 3)

        self.title_box1_2.addLayout(self.menu_grid_txt_2)

        self.title_box1_2.addSpacing(15)

        self.gmt_label_2 = QLabel()
        self.gmt_label_2.setText('GMT +2')
        self.gmt_label_2.setStyleSheet('font-size: 18px;padding: 0px 0px 0px 90px; color: %s;' % self.font_gray_color)

        self.title_box1_2.addWidget(self.gmt_label_2)

        self.layout_2.addLayout(self.title_box1_2)

        self.title_box2_2 = QHBoxLayout()  # second title box with pixmaps
        self.title_box2_2.setContentsMargins(0, 0, 0, 0)
        self.title_box2_2.setSpacing(0)

        self.frame1_2 = QFrame()
        self.frame1_2.setFixedWidth(240)
        self.frame1_2.setFixedHeight(80)
        self.frame1_2.setStyleSheet('background-color:%s; border: 0px; border-radius: 10px;' % self.dark_gray_color)
        self.defend_pix_2 = QLabel(self.frame1_2)
        self.defend_pix_2.setPixmap(QPixmap('res/pack/defend.png'))
        self.defend_pix_2.setFixedWidth(240)
        self.defend_pix_2.setAlignment(Qt.AlignCenter)
        self.title_box2_2.addWidget(self.frame1_2)

        self.title_box2_2.addSpacing(15)

        self.frame2_2 = QFrame()
        self.frame2_2.setStyleSheet('background-color:%s; border: 0px; border-radius: 10px;' % self.dark_gray_color)
        self.frame2_2.setFixedWidth(495)
        self.frame2_2.setFixedHeight(80)

        self.menu_grid_pix_2 = QGridLayout(self.frame2_2)
        self.menu_grid_pix_2.setContentsMargins(0, 0, 0, 0)
        self.menu_grid_pix_2.setSpacing(0)

        self.menu_label_pix_2 = QLabel()
        self.menu_label_pix_2.setPixmap(QPixmap('res/pack/gas_icon_main_menu.png'))
        self.menu_label_pix_2.setStyleSheet('padding: 5px 30px 0px 30px;')
        self.menu_label_pix_2.mousePressEvent = self.select_menu_main
        self.menu_grid_pix_2.addWidget(self.menu_label_pix_2, 0, 0)

        self.uart_label_pix_2 = QLabel()
        self.uart_label_pix_2.setPixmap(QPixmap('res/pack/gas_icon_UART.png'))
        self.uart_label_pix_2.setStyleSheet('padding: 5px 30px 0px 30px;')
        self.uart_label_pix_2.mousePressEvent = self.select_menu_config
        self.menu_grid_pix_2.addWidget(self.uart_label_pix_2, 0, 1)

        self.data_label_pix_2 = QLabel()
        self.data_label_pix_2.setPixmap(QPixmap('res/pack/gas_icon_meter.png'))
        self.data_label_pix_2.setStyleSheet('padding: 5px 30px 0px 30px;')
        self.data_label_pix_2.mousePressEvent = self.select_menu_meter
        self.menu_grid_pix_2.addWidget(self.data_label_pix_2, 0, 2)

        self.fan_label_pix_2 = QLabel()
        self.fan_label_pix_2.setMovie(self.fan_anim)
        self.fan_label_pix_2.setStyleSheet('padding: 5px 30px 0px 30px;')
        self.fan_label_pix_2.mousePressEvent = self.toggle_fan
        self.menu_grid_pix_2.addWidget(self.fan_label_pix_2, 0, 3)

        self.title_box2_2.addWidget(self.frame2_2)

        self.title_box2_2.addSpacing(15)

        self.frame3_2 = QFrame()
        self.frame3_2.setStyleSheet('background-color:%s; border: 0px; border-radius: 10px;' % self.dark_gray_color)
        self.frame3_2.setFixedWidth(240)
        self.frame3_2.setFixedHeight(80)

        self.clock_box_2 = QHBoxLayout(self.frame3_2)
        self.time_label_pix_2 = QLabel()
        self.time_label_pix_2.setPixmap(QPixmap('res/pack/clock.png'))
        self.time_label_txt_2 = QLabel()
        self.time_label_txt_2.setText('00:00:00')
        self.time_label_txt_2.setStyleSheet('font-size: 40px; color: %s' % self.white_color)
        self.clock_box_2.addWidget(self.time_label_pix_2)
        self.clock_box_2.addWidget(self.time_label_txt_2)
        self.title_box2_2.addWidget(self.frame3_2)

        self.layout_2.addLayout(self.title_box2_2)

        self.data_grid_frame = QFrame()
        self.data_grid_frame.setStyleSheet('background-color:%s;' % self.gray_color)
        self.data_grid = QGridLayout(self.data_grid_frame)

        self.data_grid.setColumnMinimumWidth(0, 60)

        self.substance_label = QLabel()
        self.substance_label.setText('Substance')
        self.substance_label.setStyleSheet('font-size: 18px;padding: 0px 0px 0px 0px; color: %s;' % self.white_color)
        self.data_grid.addWidget(self.substance_label, 0, 1, 1, 3)

        self.formula_label = QLabel()
        self.formula_label.setText('Formula')
        self.formula_label.setStyleSheet('font-size: 18px;padding: 0px 0px 0px 0px; color: %s;' % self.white_color)
        self.data_grid.addWidget(self.formula_label, 0, 4, 1, 2)

        self.data_grid.setColumnMinimumWidth(5, 60 * 5)

        self.probability_label = QLabel()
        self.probability_label.setText('Probability')
        self.probability_label.setStyleSheet('font-size: 18px;padding: 0px 0px 0px 0px; color: %s;' % self.white_color)
        self.data_grid.addWidget(self.probability_label, 0, 6, 1, 1)

        self.sensors_label = QLabel()
        self.sensors_label.setText('Sensors')
        self.sensors_label.setStyleSheet('font-size: 18px;padding: 0px 0px 0px 0px; color: %s;' % self.white_color)
        self.data_grid.addWidget(self.sensors_label, 0, 7, 1, 4)

        self.acetone_color_label = QLabel()
        self.acetone_color_label.setText('||||')
        self.acetone_color_label.setStyleSheet('font-size: 18px;padding: 0px 0px 0px 0px; color: %s;' % self.red_color)
        self.data_grid.addWidget(self.acetone_color_label, 1, 0, 1, 1)

        self.acetone_subst_label = QLabel()

        self.data_label = QLabel()
        self.data_label.setPixmap(QPixmap('res/pack/data_background.png'))

        self.layout_2.addSpacing(10)

        self.layout_2.addWidget(self.data_label)

        self.pages[2].setLayout(self.layout_2)
        # ################### END PAGE 2

        # ######### PAGE 3 CONFIG
        self.layout3 = QVBoxLayout()
        self.layout3.setContentsMargins(0, 0, 0, 0)

        self.title_box1_3 = QHBoxLayout()
        self.title_box1_3.setContentsMargins(0, 0, 0, 0)

        self.defend_txt_3 = QLabel()
        self.defend_txt_3.setText('DEFEND Gas Sensor Data Fusion')
        self.defend_txt_3.setStyleSheet(
            'font-size: 18px; padding:0px 0px 0px 0px; color: %s;height:20px' % self.font_gray_color)
        self.title_box1_3.addWidget(self.defend_txt_3)

        self.title_box1_3.addSpacing(15)

        self.menu_grid_txt_3 = QGridLayout()
        self.menu_grid_txt_3.setContentsMargins(0, 0, 0, 0)
        self.menu_grid_txt_3.setSpacing(0)

        self.menu_label_txt_3 = QLabel()
        self.menu_label_txt_3.setText('MENU')
        self.menu_label_txt_3.setStyleSheet('font-size: 18px;padding: 0px 35px 0px 30px; color: %s;' % self.font_gray_color)
        self.menu_grid_txt_3.addWidget(self.menu_label_txt_3, 0, 0)

        self.uart_label_txt_3 = QLabel()
        self.uart_label_txt_3.setText('METER')
        self.uart_label_txt_3.setStyleSheet('font-size: 18px;padding: 0px 35px 0px 35px; color: %s;' % self.font_gray_color)
        self.menu_grid_txt_3.addWidget(self.uart_label_txt_3, 0, 1)

        self.data_label_txt_3 = QLabel()
        self.data_label_txt_3.setText('DATA')
        self.data_label_txt_3.setStyleSheet('font-size: 18px;padding: 0px 38px 0px 28px; color: %s;' % self.font_gray_color)
        self.menu_grid_txt_3.addWidget(self.data_label_txt_3, 0, 2)

        self.fan_label_txt_3 = QLabel()
        self.fan_label_txt_3.setText('FAN')
        self.fan_label_txt_3.setStyleSheet('font-size: 18px;padding: 0px 45px 0px 40px; color: %s;' % self.font_gray_color)
        self.menu_grid_txt_3.addWidget(self.fan_label_txt_3, 0, 3)

        self.title_box1_3.addLayout(self.menu_grid_txt_3)

        self.title_box1_3.addSpacing(15)

        self.gmt_label_3 = QLabel()
        self.gmt_label_3.setText('GMT +2')
        self.gmt_label_3.setStyleSheet('font-size: 18px;padding: 0px 0px 0px 90px; color: %s;' % self.font_gray_color)

        self.title_box1_3.addWidget(self.gmt_label_3)

        self.title_box2_3 = QHBoxLayout()  # second title box with pixmaps
        self.title_box2_3.setContentsMargins(0, 0, 0, 0)
        self.title_box2_3.setSpacing(0)

        self.frame1_3 = QFrame()
        self.frame1_3.setFixedWidth(240)
        self.frame1_3.setFixedHeight(80)
        self.frame1_3.setStyleSheet('background-color:%s; border: 0px; border-radius: 10px;' % self.dark_gray_color)
        self.defend_pix_3 = QLabel(self.frame1_3)
        self.defend_pix_3.setPixmap(QPixmap('res/pack/defend.png'))
        self.defend_pix_3.setFixedWidth(240)
        self.defend_pix_3.setAlignment(Qt.AlignCenter)
        self.title_box2_3.addWidget(self.frame1_3)

        self.title_box2_3.addSpacing(15)

        self.frame2_3 = QFrame()
        self.frame2_3.setStyleSheet('background-color:%s; border: 0px; border-radius: 10px;' % self.dark_gray_color)
        self.frame2_3.setFixedWidth(495)
        self.frame2_3.setFixedHeight(80)

        self.menu_grid_pix_3 = QGridLayout(self.frame2_3)
        self.menu_grid_pix_3.setContentsMargins(0, 0, 0, 0)
        self.menu_grid_pix_3.setSpacing(0)

        self.menu_label_pix_3 = QLabel()
        self.menu_label_pix_3.setPixmap(QPixmap('res/pack/gas_icon_main_menu.png'))
        self.menu_label_pix_3.setStyleSheet('padding: 5px 30px 0px 30px;')
        self.menu_label_pix_3.mousePressEvent = self.select_menu_main
        self.menu_grid_pix_3.addWidget(self.menu_label_pix_3, 0, 0)

        self.uart_label_pix_3 = QLabel()
        self.uart_label_pix_3.setPixmap(QPixmap('res/pack/gas_icon_meter.png'))
        self.uart_label_pix_3.setStyleSheet('padding: 5px 30px 0px 30px;')
        self.uart_label_pix_3.mousePressEvent = self.select_menu_meter
        self.menu_grid_pix_3.addWidget(self.uart_label_pix_3, 0, 1)

        self.data_label_pix_3 = QLabel()
        self.data_label_pix_3.setPixmap(QPixmap('res/pack/gas_icon_data.png'))
        self.data_label_pix_3.setStyleSheet('padding: 5px 30px 0px 30px;')
        self.data_label_pix_3.mousePressEvent = self.select_menu_data
        self.menu_grid_pix_3.addWidget(self.data_label_pix_3, 0, 2)

        self.fan_label_pix_3 = QLabel()
        self.fan_label_pix_3.setMovie(self.fan_anim)
        self.fan_label_pix_3.setStyleSheet('padding: 5px 30px 0px 30px;')
        self.fan_label_pix_3.mousePressEvent = self.toggle_fan
        self.menu_grid_pix_3.addWidget(self.fan_label_pix_3, 0, 3)

        self.title_box2_3.addWidget(self.frame2_3)

        self.title_box2_3.addSpacing(15)

        self.frame3_3 = QFrame()
        self.frame3_3.setStyleSheet('background-color:%s; border: 0px; border-radius: 10px;' % self.dark_gray_color)
        self.frame3_3.setFixedWidth(240)
        self.frame3_3.setFixedHeight(80)

        self.clock_box_3 = QHBoxLayout(self.frame3_3)
        self.time_label_pix_3 = QLabel()
        self.time_label_pix_3.setPixmap(QPixmap('res/pack/clock.png'))
        self.time_label_txt_3 = QLabel()
        self.time_label_txt_3.setText('00:00:00')
        self.time_label_txt_3.setStyleSheet('font-size: 40px; color: %s' % self.white_color)
        self.clock_box_3.addWidget(self.time_label_pix_3)
        self.clock_box_3.addWidget(self.time_label_txt_3)
        self.title_box2_3.addWidget(self.frame3_3)

        self.label33 = QLabel()
        self.label33.setText('CONNECT SERIAL')
        self.label33.setStyleSheet(
            'font-size: 40px; padding:50px 10px 0px 5px; color: %s;height:20px' % self.green_color)
        self.label33.mousePressEvent = self.toggle_serial

        self.label3 = QLabel()
        self.label3.setText('START REC')
        self.label3.setStyleSheet('font-size: 40px; padding:50px 10px 0px 5px; color: %s;height:20px' % self.green_color)
        self.label3.mousePressEvent = self.toggle_recording

        self.layout3.addLayout(self.title_box1_3)
        self.layout3.addLayout(self.title_box2_3)
        self.layout3.addWidget(self.label33)
        self.layout3.addWidget(self.label3)
        self.layout3.addStretch()
        self.pages[3].setLayout(self.layout3)
        # ################### END PAGE 3

        # ######### PAGE 4 MQ HELP
        self.layout_4 = QVBoxLayout()
        self.layout_4.setContentsMargins(0, 0, 0, 0)

        self.title_box1_4 = QHBoxLayout()
        self.title_box1_4.setContentsMargins(0, 0, 0, 0)

        self.defend_txt_4 = QLabel()
        self.defend_txt_4.setText('DEFEND Gas Sensor Data Fusion')
        self.defend_txt_4.setStyleSheet(
            'font-size: 18px; padding:0px 0px 0px 0px; color: %s;height:20px' % self.font_gray_color)
        self.title_box1_4.addWidget(self.defend_txt_4)

        self.title_box1_4.addSpacing(15)

        self.menu_grid_txt_4 = QGridLayout()
        self.menu_grid_txt_4.setContentsMargins(0, 0, 0, 0)
        self.menu_grid_txt_4.setSpacing(0)

        self.menu_label_txt_4 = QLabel()
        self.menu_label_txt_4.setText('MENU')
        self.menu_label_txt_4.setStyleSheet(
            'font-size: 18px;padding: 0px 35px 0px 30px; color: %s;' % self.font_gray_color)
        self.menu_grid_txt_4.addWidget(self.menu_label_txt_4, 0, 0)

        self.uart_label_txt_4 = QLabel()
        self.uart_label_txt_4.setText('UART')
        self.uart_label_txt_4.setStyleSheet(
            'font-size: 18px;padding: 0px 35px 0px 35px; color: %s;' % self.font_gray_color)
        self.menu_grid_txt_4.addWidget(self.uart_label_txt_4, 0, 1)

        self.data_label_txt_4 = QLabel()
        self.data_label_txt_4.setText('METER')
        self.data_label_txt_4.setStyleSheet(
            'font-size: 18px;padding: 0px 40px 0px 40px; color: %s;' % self.font_gray_color)
        self.menu_grid_txt_4.addWidget(self.data_label_txt_4, 0, 2)

        self.fan_label_txt_4 = QLabel()
        self.fan_label_txt_4.setText('FAN')
        self.fan_label_txt_4.setStyleSheet(
            'font-size: 18px;padding: 0px 45px 0px 40px; color: %s;' % self.font_gray_color)
        self.menu_grid_txt_4.addWidget(self.fan_label_txt_4, 0, 3)

        self.title_box1_4.addLayout(self.menu_grid_txt_4)

        self.title_box1_4.addSpacing(15)

        self.gmt_label_4 = QLabel()
        self.gmt_label_4.setText('GMT +2')
        self.gmt_label_4.setStyleSheet('font-size: 18px;padding: 0px 0px 0px 90px; color: %s;' % self.font_gray_color)

        self.title_box1_4.addWidget(self.gmt_label_4)

        self.layout_4.addLayout(self.title_box1_4)

        self.title_box2_4 = QHBoxLayout()  # second title box with pixmaps
        self.title_box2_4.setContentsMargins(0, 0, 0, 0)
        self.title_box2_4.setSpacing(0)

        self.frame1_4 = QFrame()
        self.frame1_4.setFixedWidth(240)
        self.frame1_4.setFixedHeight(80)
        self.frame1_4.setStyleSheet('background-color:%s; border: 0px; border-radius: 10px;' % self.dark_gray_color)
        self.defend_pix_4 = QLabel(self.frame1_4)
        self.defend_pix_4.setPixmap(QPixmap('res/pack/defend.png'))
        self.defend_pix_4.setFixedWidth(240)
        self.defend_pix_4.setAlignment(Qt.AlignCenter)
        self.title_box2_4.addWidget(self.frame1_4)

        self.title_box2_4.addSpacing(15)

        self.frame2_4 = QFrame()
        self.frame2_4.setStyleSheet('background-color:%s; border: 0px; border-radius: 10px;' % self.dark_gray_color)
        self.frame2_4.setFixedWidth(495)
        self.frame2_4.setFixedHeight(80)

        self.menu_grid_pix_4 = QGridLayout(self.frame2_4)
        self.menu_grid_pix_4.setContentsMargins(0, 0, 0, 0)
        self.menu_grid_pix_4.setSpacing(0)

        self.menu_label_pix_4 = QLabel()
        self.menu_label_pix_4.setPixmap(QPixmap('res/pack/gas_icon_main_menu.png'))
        self.menu_label_pix_4.setStyleSheet('padding: 5px 30px 0px 30px;')
        self.menu_label_pix_4.mousePressEvent = self.select_menu_main
        self.menu_grid_pix_4.addWidget(self.menu_label_pix_4, 0, 0)

        self.uart_label_pix_4 = QLabel()
        self.uart_label_pix_4.setPixmap(QPixmap('res/pack/gas_icon_UART.png'))
        self.uart_label_pix_4.setStyleSheet('padding: 5px 30px 0px 30px;')
        self.uart_label_pix_4.mousePressEvent = self.select_menu_config
        self.menu_grid_pix_4.addWidget(self.uart_label_pix_4, 0, 1)

        self.data_label_pix_4 = QLabel()
        self.data_label_pix_4.setPixmap(QPixmap('res/pack/gas_icon_meter.png'))
        self.data_label_pix_4.setStyleSheet('padding: 5px 30px 0px 30px;')
        self.data_label_pix_4.mousePressEvent = self.select_menu_meter
        self.menu_grid_pix_4.addWidget(self.data_label_pix_4, 0, 2)

        self.fan_label_pix_4 = QLabel()
        self.fan_label_pix_4.setMovie(self.fan_anim)
        self.fan_label_pix_4.setStyleSheet('padding: 5px 30px 0px 30px;')
        self.fan_label_pix_4.mousePressEvent = self.toggle_fan
        self.menu_grid_pix_4.addWidget(self.fan_label_pix_4, 0, 3)

        self.title_box2_4.addWidget(self.frame2_4)

        self.title_box2_4.addSpacing(15)

        self.frame3_4 = QFrame()
        self.frame3_4.setStyleSheet('background-color:%s; border: 0px; border-radius: 10px;' % self.dark_gray_color)
        self.frame3_4.setFixedWidth(240)
        self.frame3_4.setFixedHeight(80)

        self.clock_box_4 = QHBoxLayout(self.frame3_4)
        self.time_label_pix_4 = QLabel()
        self.time_label_pix_4.setPixmap(QPixmap('res/pack/clock.png'))
        self.time_label_txt_4 = QLabel()
        self.time_label_txt_4.setText('00:00:00')
        self.time_label_txt_4.setStyleSheet('font-size: 40px; color: %s' % self.white_color)
        self.clock_box_4.addWidget(self.time_label_pix_4)
        self.clock_box_4.addWidget(self.time_label_txt_4)
        self.title_box2_4.addWidget(self.frame3_4)

        self.layout_4.addLayout(self.title_box2_4)

        self.label4 = QLabel()
        self.label4.setText('MQ HELP')
        self.label4.setStyleSheet('font-size: 26px; padding:50px 10px 0px 5px; color: %s;height:20px' % self.green_color)
        self.layout_4.addWidget(self.label4)
        self.layout_4.addStretch()

        self.pages[4].setLayout(self.layout_4)
        # ################### END PAGE 4

        self.fan_anim.start()

        # ######### STACK
        self.stack = QStackedWidget()
        for page in self.pages:
            self.stack.addWidget(page)
        self.stack.setCurrentIndex(1)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.stack)
        self.setLayout(self.mainLayout)
        self.show()
        # ###################

    def keyPressEvent(self, event):
        # ESC
        if event.key() == Qt.Key_Escape:
            self.clk_stop_signal.emit()
            self.close()
        elif event.key() == Qt.Key_0:
            self.stack.setCurrentIndex(0)
        elif event.key() == Qt.Key_1:
            self.stack.setCurrentIndex(1)
        elif event.key() == Qt.Key_2:
            self.stack.setCurrentIndex(2)
        elif event.key() == Qt.Key_3:
            self.stack.setCurrentIndex(3)
        elif event.key() == Qt.Key_4:
            self.stack.setCurrentIndex(4)

    def select_menu_main(self, ev):
        self.stack.setCurrentIndex(0)
        self.current_page = 0

    def select_menu_meter(self, ev):
        self.stack.setCurrentIndex(1)
        self.current_page = 1

    def select_menu_data(self, ev):
        self.stack.setCurrentIndex(2)
        self.current_page = 2

    def select_menu_config(self, ev):
        self.stack.setCurrentIndex(3)
        self.current_page = 3

    def select_menu_help(self, sensor_nr):
        self.label4.setText(self.sensor_pixmap[sensor_nr])
        self.stack.setCurrentIndex(4)
        self.current_page = 4
        print(sensor_nr)

    def toggle_fan(self, ev):
        self.fan_powered = not self.fan_powered
        if self.fan_powered:
            self.fan_anim.start()
        else:
            self.fan_anim.stop()
        self.fan_signal.emit()

    def toggle_recording(self, ev):
        self.recording = not self.recording
        if self.recording:
            self.label3.setText('STOP REC')
            self.label3.setStyleSheet('font-size: 40px; padding: 50px 0px 0px 5px; color: %s;height:20px' % self.red_color)
        else:
            self.label3.setText('START REC')
            self.label3.setStyleSheet('font-size: 40px; padding: 50px 0px 0px 5px; color: %s;height:20px' % self.green_color)
        self.rec_signal.emit()

    def toggle_serial(self, ev):
        self.connected = not self.connected

        if self.connected:
            self.bgWork = BgThread()
            self.bgWork.signal_data.connect(self.data_slot)
            self.fan_signal.connect(self.bgWork.fanCmd)
            self.bg_stop_signal.connect(self.bgWork.endJob)
            self.rec_signal.connect(self.bgWork.recCmd)
            self.bgWork.start()

            self.label33.setText('DISCONNECT SERIAL')
            self.label33.setStyleSheet(
                'font-size: 40px; padding: 50px 0px 0px 5px; color: %s;height:20px' % self.red_color)
        else:
            self.bg_stop_signal.emit()

            self.label33.setText('CONNECT SERIAL')
            self.label33.setStyleSheet(
                'font-size: 40px; padding: 50px 0px 0px 5px; color: %s;height:20px' % self.green_color)

    @pyqtSlot(list)
    def data_slot(self, vals):
        for k in range(len(vals)):
            self.dial[k].update_fig(vals[k])
            if self.sensor_rec_list[k] < vals[k]:
                self.sensor_rec_list[k] = vals[k]

    @pyqtSlot(str)
    def telemetry_select_slot(self, robo_name):
        self.robotLabel.setText(robo_name)

    @pyqtSlot(str)
    def clock_slot(self, t):
        self.time_label_txt_0.setText(t)
        self.time_label_txt_1.setText(t)
        self.time_label_txt_2.setText(t)
        self.time_label_txt_3.setText(t)
        self.time_label_txt_4.setText(t)
