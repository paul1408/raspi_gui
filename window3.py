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
        self.dark_gray_color= '#1b1a1a'
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
        self.layout0 = QVBoxLayout()
        self.layout0.setContentsMargins(5, 5, 5, 5)

        label1 = QLabel()
        label1.setText('Main menu')
        self.layout0.addWidget(label1)
        self.pages[0].setLayout(self.layout0)
        # #################### END PAGE 0

        # ######### PAGE 1 METER
        self.layout1 = QVBoxLayout()
        self.layout1.setContentsMargins(0, 0, 0, 0)

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
        self.fan_label_pix_1.setPixmap(QPixmap('res/pack/gas_icon_fan_off.png'))
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
        self.layout1.addLayout(self.title_box1_1)
        self.layout1.addLayout(self.title_box2_1)
        self.layout1.addLayout(self.sensorsGrid)
        self.pages[1].setLayout(self.layout1)
        # ################### END PAGE 1

        # ######### PAGE 2 DATA
        self.layout2 = QVBoxLayout()
        self.layout2.setContentsMargins(5, 5, 5, 5)

        label1 = QLabel()
        label1.setText('Data fusion')
        self.layout2.addWidget(label1)
        self.pages[2].setLayout(self.layout2)
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
        self.uart_label_txt_3.setText('UART')
        self.uart_label_txt_3.setStyleSheet('font-size: 18px;padding: 0px 35px 0px 35px; color: %s;' % self.font_gray_color)
        self.menu_grid_txt_3.addWidget(self.uart_label_txt_3, 0, 1)

        self.data_label_txt_3 = QLabel()
        self.data_label_txt_3.setText('METER')
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
        self.uart_label_pix_3.setPixmap(QPixmap('res/pack/gas_icon_UART.png'))
        self.uart_label_pix_3.setStyleSheet('padding: 5px 30px 0px 30px;')
        self.uart_label_pix_3.mousePressEvent = self.select_menu_config
        self.menu_grid_pix_3.addWidget(self.uart_label_pix_3, 0, 1)

        self.data_label_pix_3 = QLabel()
        self.data_label_pix_3.setPixmap(QPixmap('res/pack/gas_icon_data.png'))
        self.data_label_pix_3.setStyleSheet('padding: 5px 30px 0px 30px;')
        self.data_label_pix_3.mousePressEvent = self.select_menu_meter
        self.menu_grid_pix_3.addWidget(self.data_label_pix_3, 0, 2)

        self.fan_label_pix_3 = QLabel()
        self.fan_label_pix_3.setPixmap(QPixmap('res/pack/gas_icon_fan_off.png'))
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

        self.label4 = QLabel()
        self.label4.setText('CONNECT SERIAL')
        self.label4.setStyleSheet(
            'font-size: 40px; padding:50px 10px 0px 5px; color: %s;height:20px' % self.green_color)
        self.label4.mousePressEvent = self.toggle_serial

        self.label3 = QLabel()
        self.label3.setText('START REC')
        self.label3.setStyleSheet('font-size: 40px; padding:50px 10px 0px 5px; color: %s;height:20px' % self.green_color)
        self.label3.mousePressEvent = self.toggle_recording

        self.layout3.addLayout(self.title_box1_3)
        self.layout3.addLayout(self.title_box2_3)
        self.layout3.addWidget(self.label4)
        self.layout3.addWidget(self.label3)
        self.layout3.addStretch()
        self.pages[3].setLayout(self.layout3)
        # ################### END PAGE 3

        # ######### PAGE 4 MQ HELP
        self.layout4 = QVBoxLayout()
        self.layout4.setContentsMargins(5, 5, 5, 5)

        label1 = QLabel()
        label1.setText('MQ HELP')
        self.layout4.addWidget(label1)
        self.pages[4].setLayout(self.layout4)
        # ################### END PAGE 4

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
        #self.stack.setCurrentIndex(4)
        #self.current_page = 4
        print(sensor_nr)

    def toggle_fan(self, ev):
        self.fan_powered = not self.fan_powered
        if self.fan_powered:
            self.fan_label_pix_1.setMovie(self.fan_anim)
            self.fan_anim.start()
        else:
            self.fan_anim.stop()
            self.fan_label_pix_1.setPixmap(QPixmap('res/pack/gas_icon_fan_off.png'))
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

            self.label4.setText('DISCONNECT SERIAL')
            self.label4.setStyleSheet(
                'font-size: 40px; padding: 50px 0px 0px 5px; color: %s;height:20px' % self.red_color)
        else:
            self.bg_stop_signal.emit()

            self.label4.setText('CONNECT SERIAL')
            self.label4.setStyleSheet(
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
        self.time_label_txt_1.setText(t)