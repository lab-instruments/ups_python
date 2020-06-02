from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QThread, pyqtSignal
from DiscoveryClient import DiscoveryClient
import sys
from UpsApi import UpsApi


class DiscoThread(QThread):

    # Signal for Response
    disc_sig = pyqtSignal(list)

    def __init__(self):
        QThread.__init__(self)
        self.dc = DiscoveryClient(5)

    def run(self):
        while True:
            ipList = self.dc.run()
            self.disc_sig.emit(ipList)


class UpsGui(QtWidgets.QMainWindow):
    def __init__(self):

        # Load GUI
        super(UpsGui, self).__init__()
        uic.loadUi('/local/git/ups_python/python/gui.ui', self)
        self.show()

        # Setup UpsApi
        self.api = UpsApi()

        # Setup UI
        self.setup_ui()

        # Start Discovery Thread
        self.dt = DiscoThread()
        self.dt.disc_sig.connect(self.update_ups_list)
        self.dt.start()

    def setup_ui(self):

        # Populate Mode List
        self.modeSel.addItem('Idle')
        self.modeSel.addItem('Loopback')
        self.modeSel.addItem('Debug')
        self.modeSel.addItem('Run')
        self.modeSel.setCurrentIndex(0)

        # Setup UPS Connect Button
        self.upsConnect.clicked.connect(self.ups_connect)

        # Setup Debug Set Buttons and Boxes
        self.ledDebugSet.clicked.connect(self.debug_led_set)
        self.dac0DebugSet.clicked.connect(self.debug_dac0_set)
        self.dac1DebugSet.clicked.connect(self.debug_dac1_set)
        self.modeSel.currentIndexChanged.connect(self.mode_set)
        self.pinchValve.stateChanged.connect(self.pv_set)

        # Setup Run Buttons and Boxes
        self.runStart.clicked.connect(self.start_run)
        self.runStop.clicked.connect(self.stop_run)

        # Set Tabs Enable
        self.tabs.setTabEnabled(0, False)
        self.tabs.setTabEnabled(1, False)

    def stop_run(self):
        # Issue Command
        self.api.set_stop()

        # Enable/Disable Buttons
        self.runStart.setEnabled(True)
        self.runStop.setEnabled(False)

    def start_run(self):

        # Get Values from GUI
        run_pre_time = int(self.runPreTrigTimerValue.text())
        run_post_time = int(self.runLoopTimerValue.text())
        run_time = int(self.runTimerValue.text())
        num_loops = int(self.runNumLoopsValue.text())

        # Issue Command
        self.api.set_run(num_loops, run_pre_time, run_post_time, run_time)

        # Enable/Disable Buttons
        self.runStart.setEnabled(False)
        self.runStop.setEnabled(True)

    def pv_set(self):
        if self.pinchValve.isChecked():
            self.api.set_valve(1)
        else:
            self.api.set_valve(0)

    def mode_set(self):

        # Requested Mode
        mode = int(self.modeSel.currentIndex())

        # Switch Based on Mode Set
        if mode == 0:  # Idle Mode
            self._set_mode_idle()

        elif mode == 1:  # Loopback Mode
            self._set_mode_loopback()

        elif mode == 2:  # Debug Mode
            self._set_mode_debug()

        elif mode == 3:  # Run Mode
            self._set_mode_run()

    def _set_mode_idle(self):

        # Disable Tabs
        self.tabs.setTabEnabled(0, False)
        self.tabs.setTabEnabled(1, False)
        self.tabs.setCurrentIndex(0)

        # Reset GUI Fields
        self.dac0DebugValue.setText('0')
        self.dac1DebugValue.setText('0')
        self.ledDebugValue.setText('0')
        self.pinchValve.setCheckState(False)

        # Reset Box
        self.api.set_dac0(0)
        self.api.set_dac1(0)
        self.api.set_led(0)
        self.api.set_valve(0)
        self.api.set_mode(0)

    def _set_mode_loopback(self):

        # Enable Debug Tab
        self.tabs.setTabEnabled(0, True)
        self.tabs.setTabEnabled(1, False)
        self.tabs.setCurrentIndex(0)

        # Reset GUI Fields
        self.dac0DebugValue.setText('0')
        self.dac1DebugValue.setText('0')
        self.ledDebugValue.setText('0')
        self.pinchValve.setCheckState(False)

        # Reset Box
        self.api.set_dac0(0)
        self.api.set_dac1(0)
        self.api.set_led(0)
        self.api.set_valve(0)
        self.api.set_mode(1)

    def _set_mode_debug(self):

        # Enable Debug Tab
        self.tabs.setTabEnabled(0, True)
        self.tabs.setTabEnabled(1, False)
        self.tabs.setCurrentIndex(0)

        # Reset GUI Fields
        self.dac0DebugValue.setText('0')
        self.dac1DebugValue.setText('0')
        self.ledDebugValue.setText('0')
        self.pinchValve.setCheckState(False)

        # Reset Box
        self.api.set_dac0(0)
        self.api.set_dac1(0)
        self.api.set_led(0)
        self.api.set_valve(0)
        self.api.set_mode(2)

    def _set_mode_run(self):

        # Enable Debug Tab
        self.tabs.setTabEnabled(0, False)
        self.tabs.setTabEnabled(1, True)
        self.tabs.setCurrentIndex(1)

        # Reset GUI Fields
        self.dac0DebugValue.setText('0')
        self.dac1DebugValue.setText('0')
        self.ledDebugValue.setText('0')
        self.pinchValve.setCheckState(False)

        # Reset GUI Fields
        self.runPreTrigTimerValue.setText('20')
        self.runTimerValue.setText('20')
        self.runLoopTimerValue.setText('60')
        self.runNumLoopsValue.setText('1')

        # Reset Box
        self.api.set_dac0(0)
        self.api.set_dac1(0)
        self.api.set_led(0)
        self.api.set_valve(0)
        self.api.set_mode(3)

    def debug_led_set(self):
        self.api.set_led(int(self.ledDebugValue.text()))

    def debug_dac0_set(self):
        self.api.set_dac0(int(self.dac0DebugValue.text()))

    def debug_dac1_set(self):
        self.api.set_dac1(int(self.dac1DebugValue.text()))

    def ups_connect(self):

        # Get Select Items from Box
        selected_ip = self.upsIpList.selectedItems()

        # Check if Anything is Selected
        if selected_ip:

            # Setup UpsApi with Selected IP Address
            self.api.connect(selected_ip[0].text())

            # Disable Connect Button
            self.upsConnect.setEnabled(False)

            # Enable Debug Tab and Model Select Box
            self.modeGroupBox.setEnabled(True)
            self.tabs.setTabEnabled(0, True)

            # Reset Box
            self.modeSel.setCurrentIndex(2)
            self.api.set_dac0(0)
            self.api.set_dac1(0)
            self.api.set_led(0)
            self.api.set_valve(0)

    def update_ups_list(self, ipList):

        # ----------------------------------------------------------------------
        #  Get items currently in the list box and compare them to the input
        #  IP address list.  If they exist, remove them from the input IP list.
        #  If they don't exist, remove them from the listbox.
        # ----------------------------------------------------------------------
        for idx in range(self.upsIpList.count()):
            if self.upsIpList.item(idx).text() in ipList:
                ipList.remove(self.upsIpList.item(idx).text())
            else:
                self.upsIpList.takeItem(idx)

        # Add to Box
        self.upsIpList.addItems(ipList)

    # def init_ui(self):
    #     self.


app = QtWidgets.QApplication(sys.argv)
window = UpsGui()
app.exec_()