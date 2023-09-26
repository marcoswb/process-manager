from PySide6.QtCore import QThread, Signal
from time import sleep
from os import listdir
from os.path import isdir

from models.Process import Process
from utils.functions import *


class UpdateDataProcess(QThread):
    data_changed = Signal(list, str, str)

    def run(self):
        while True:
            sleep(5)

            data_process = []
            total_memory_usage = 0
            status_process = {}
            for directory in listdir('/proc'):
                if not isdir(f'/proc/{directory}') or not format_int(directory):
                    continue

                proc = Process(directory)
                data_process.append(proc)

                total_memory_usage += float(proc.memory_usage)
                if not status_process.get(proc.status):
                    status_process[proc.status] = 0

                status_process[proc.status] += 1

            percent_memory_usage = format((total_memory_usage * 100) / total_memory_machine(), '.2f')

            text_info_process = f'<b>Total number of processes:</b> {len(data_process)};     '
            total_status = len(status_process) - 1
            for index, status in enumerate(status_process):
                if index == total_status:
                    text_info_process += f'{status_process.get(status)} are {status}'
                else:
                    text_info_process += f'{status_process.get(status)} are {status},   '

            self.data_changed.emit(data_process, percent_memory_usage, text_info_process)


class UpdateGeneralInfos(QThread):
    data_changed = Signal(str, str, str)

    def run(self):
        while True:
            sleep(1)
            self.data_changed.emit(get_current_time(), get_uptime_machine(), format(get_cpu_percent(), ".2f"))
