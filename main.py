import sys
from PyQt5.QtWidgets import QApplication
from thread_list import ClockThread
from window3 import Window


if __name__ == '__main__':
    #init
    App = QApplication(sys.argv)
    win = Window()
    clkWork = ClockThread()

    # events
    clkWork.signal_time.connect(win.clock_slot)
    win.clk_stop_signal.connect(clkWork.endJob)

    # start
    clkWork.start()
    sys.exit(App.exec_())
