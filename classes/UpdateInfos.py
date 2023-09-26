from PySide6.QtCore import QThread, Signal
from time import sleep

from utils.functions import *

class UpdateDataProcess(QThread):
    data_changed = Signal(list, float, dict)

    def run(self):
        data_process = []
        total_memory_usage = 0
        status_process = {}
        while True:
            sleep(5)

            self.data_changed.emit(data_process, total_memory_usage, status_process)


class UpdateGeneralInfos(QThread):
    data_changed = Signal(str, str, str)

    def run(self):
        while True:
            sleep(1)
            self.data_changed.emit(get_current_time(), get_uptime_machine(), format(get_cpu_percent(), ".2f"))
