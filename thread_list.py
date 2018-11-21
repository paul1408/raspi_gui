import time, datetime
import serial
import csv
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot


class BgThread(QThread):
    signal_data = pyqtSignal(list)

    def __init__(self):
        QThread.__init__(self)
        self.is_running = True
        self.fan_power = True
        self.fan_switch = True
        self.recording = False
        self.rand_list = [0] * 8
        self.serial_port = serial.Serial(port='/dev/ttyUSB0', baudrate=19200, timeout=1)
        print(self.serial_port)

    def run(self):
        buffer = [b'0'] * 12
        b_int = [0] * 12
        b = ''
        cmd = ''

        while not self.serial_port.isOpen():
            time.sleep(0.1)

        while self.is_running:
            self.serial_port.write('@'.encode('ascii'))
            # print('Sent @ to port')
            for k in range(12):
                buffer[k] = self.serial_port.read()
                b_int[k] = int.from_bytes(buffer[k], byteorder='big')
            for i in range(8):
                self.rand_list[i] = int.from_bytes(buffer[i+1], byteorder='big')
            self.signal_data.emit(self.rand_list)         # TELEMETRY SIGNAL

            if self.recording:
                t_secs = round(time.time() - self.start_t, 2)
                self.writer.writerow([t_secs] + self.rand_list)

            if self.fan_switch is True:
                print('Fan cmd')
                if self.fan_power:
                    cmd = '$'
                else:
                    cmd = '%'
                self.serial_port.write(cmd.encode('ascii'))
                print('Sent {} to port'.format(cmd))
                b = self.serial_port.read_until()
                print(b)
                #if buffer[0] is '0':
                #    self.fan_switch = False
                self.fan_switch = False

            time.sleep(0.1)

    @pyqtSlot()
    def endJob(self):
        self.serial_port.close()
        self.is_running = False

    @pyqtSlot()
    def fanCmd(self):
        self.fan_switch = True
        self.fan_power = not self.fan_power

    @pyqtSlot()
    def recCmd(self):
        if not self.recording:
            # start record
            self.name = datetime.datetime.now().strftime('records/%Y_%m_%d_%H_%M_gas_sensors.csv') # make DIR "records"
            self.file = open('%s' % self.name, 'w', newline='')
            self.writer = csv.writer(self.file)
            self.start_t = time.time()
            print('Start REC')
        else:
            # stop record
            self.file.close()
            print('STOP REC')
        self.recording = not self.recording


class ClockThread(QThread):
    signal_time = pyqtSignal(str)

    def __init__(self):
        QThread.__init__(self)
        self.is_running = True
        self.t = '00:00:00'

    def run(self):
        while self.is_running:
            self.t = datetime.datetime.now().strftime('%H:%M:%S')
            self.signal_time.emit(self.t)
            # print('ClkThrd: {}'.format(self.t))
            time.sleep(1)

    @pyqtSlot()
    def endJob(self):
        self.is_running = False
