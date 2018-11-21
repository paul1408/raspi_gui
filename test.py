self.title_box1_2 = QHBoxLayout()
        self.title_box1_2.setContentsMargins(0, 0, 0, 0)

        self.defend_txt_2 = QLabel()
        self.defend_txt_2.setText('DEFEND Gas Sensor Data Fusion')
        self.defend_txt_2.setStyleSheet('font-size: 18px; padding:0px 0px 0px 0px; color: %s;height:20px' % self.font_gray_color)
        self.title_box1_2.addWidget(self.defend_txt_2)

        self.title_box1_2.addSpacing(15)

        self.menu_grid_txt_2 = QGridLayout()
        self.menu_grid_txt_2.setContentsMargins(0, 0, 0, 0)
        self.menu_grid_txt_2.setSpacing(0)

        self.menu_label_txt_2 = QLabel()
        self.menu_label_txt_2.setText('MENU')
        self.menu_label_txt_2.setStyleSheet('font-size: 18px;padding: 0px 35px 0px 30px; color: %s;' % self.font_gray_color)
        self.menu_grid_txt_2.addWidget(self.menu_label_txt_2, 0, 0)

        self.uart_label_txt_2 = QLabel()
        self.uart_label_txt_2.setText('UART')
        self.uart_label_txt_2.setStyleSheet('font-size: 18px;padding: 0px 35px 0px 35px; color: %s;' % self.font_gray_color)
        self.menu_grid_txt_2.addWidget(self.uart_label_txt_2, 0, 1)

        self.data_label_txt_2 = QLabel()
        self.data_label_txt_2.setText('DATA')
        self.data_label_txt_2.setStyleSheet('font-size: 18px;padding: 0px 40px 0px 40px; color: %s;' % self.font_gray_color)
        self.menu_grid_txt_2.addWidget(self.data_label_txt_2, 0, 2)

        self.fan_label_txt_2 = QLabel()
        self.fan_label_txt_2.setText('FAN')
        self.fan_label_txt_2.setStyleSheet('font-size: 18px;padding: 0px 45px 0px 40px; color: %s;' % self.font_gray_color)
        self.menu_grid_txt_2.addWidget(self.fan_label_txt_2, 0, 3)

        self.title_box1_2.addLayout(self.menu_grid_txt_2)

        self.title_box1_2.addSpacing(15)

        self.gmt_label_2 = QLabel()
        self.gmt_label_2.setText('GMT +2')
        self.gmt_label_2.setStyleSheet('font-size: 18px;padding: 0px 0px 0px 90px; color: %s;' % self.font_gray_color)

        self.title_box1_2.addWidget(self.gmt_label_2)

        self.layout_2.addLayout(self.title_box1_2)

        self.title_box2_2 = QHBoxLayout()   # second title box with pixmaps
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
        self.data_label_pix_2.setPixmap(QPixmap('res/pack/gas_icon_data.png'))
        self.data_label_pix_2.setStyleSheet('padding: 5px 30px 0px 30px;')
        self.data_label_pix_2.mousePressEvent = self.select_menu_data
        self.menu_grid_pix_2.addWidget(self.data_label_pix_2, 0, 2)

        self.fan_label_pix_2 = QLabel()
        self.fan_label_pix_2.setPixmap(QPixmap('res/pack/gas_icon_fan_off.png'))
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