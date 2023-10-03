from sys import exit
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QHeaderView
from PySide6.QtCore import QFile, Slot
from os import listdir
from os.path import isdir
from time import sleep

from models.Process import Process
from classes.UpdateInfos import UpdateDataProcess, UpdateGeneralInfos
from utils.functions import *


class ProcessManager(QMainWindow):

    def __init__(self):
        super().__init__()

        self.__data_process = []
        self.__total_memory_usage = 0
        self.__status_process = {}
        self.__columns_header = [
            'PID',
            'USER',
            'NAME',
            'PRIORITY',
            'MEMORY USAGE',
            'DISK READ',
            'DISK WRITE'
        ]

        self.__window = self.setup_ui('./screen_ui/screen.ui')
        self.link_components()

        # atualizar informações gerais
        self.update_data_thread = UpdateGeneralInfos(self)
        self.update_data_thread.data_changed.connect(self.update_infos_process)
        self.update_data_thread.start()

        # atualizar informações dos processos
        self.update_data_thread = UpdateDataProcess(self)
        self.update_data_thread.data_changed.connect(self.update_data_process)
        self.update_data_thread.start()

    @staticmethod
    def setup_ui(ui_file_name):
        """
        Inicializar interface
        """
        ui_file = QFile(ui_file_name)
        loader = QUiLoader()
        return loader.load(ui_file)

    def link_components(self):
        """
        Vincular componentes da interface
        """
        self.__table_list_process = self.__window.table__list_process

        # redimensionar tamanho do cabeçalho conforme tamanho da tela
        header = self.__table_list_process.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        self.__label_time = self.__window.label__time
        self.__label_uptime = self.__window.label__uptime
        self.__label_cpu_usage = self.__window.label__cpu_usage
        self.__label_memory_usage = self.__window.label__memory_usage
        self.__label_infos_process = self.__window.label__infos_process

        self.__button_stop = self.__window.button__stop
        self.__button_resume = self.__window.button__resume
        self.__button_restart = self.__window.button__restart
        self.__button_kill = self.__window.button__kill
        #
        self.__button_stop.clicked.connect(self.stop_process)
        self.__button_resume.clicked.connect(self.resume_process)
        self.__button_restart.clicked.connect(self.restart_process)
        self.__button_kill.clicked.connect(self.kill_process)

    def init(self):
        """
        Renderizar janela
        """
        self.load_data_process()
        self.fill_data()
        self.show_infos_process()

        self.__window.showMaximized()

    def load_data_process(self):
        """
        Carrega os dados dos processos em memória
        """
        self.__data_process.clear()
        self.__status_process = {}
        self.__total_memory_usage = 0
        for directory in listdir('/proc'):
            if not isdir(f'/proc/{directory}') or not format_int(directory):
                continue

            proc = Process(directory)
            self.__data_process.append(proc)

            self.__total_memory_usage += float(proc.memory_usage)
            if not self.__status_process.get(proc.status):
                self.__status_process[proc.status] = 0

            self.__status_process[proc.status] += 1

    def fill_data(self):
        """
        Preenche os dados em memória em tela
        """
        while self.__table_list_process.rowCount() > 0:
            self.__table_list_process.removeRow(0)

        for index, proc in enumerate(self.__data_process):
            self.__table_list_process.insertRow(index)

            self.__table_list_process.setItem(index, 0, QTableWidgetItem(str(proc.pid)))
            self.__table_list_process.setItem(index, 1, QTableWidgetItem(str(proc.user)))
            self.__table_list_process.setItem(index, 2, QTableWidgetItem(str(proc.name)))
            self.__table_list_process.setItem(index, 3, QTableWidgetItem(str(proc.priority)))
            self.__table_list_process.setItem(index, 4, QTableWidgetItem(str(proc.memory_usage)))
            self.__table_list_process.setItem(index, 5, QTableWidgetItem(str(proc.disk_read)))
            self.__table_list_process.setItem(index, 6, QTableWidgetItem(str(proc.disk_write)))
            self.__table_list_process.setItem(index, 7, QTableWidgetItem(str(proc.status)))

    def show_infos_process(self):
        """
        Mostra em tela alguns dados gerais dos processos
        """
        percent_memory_usage = (self.__total_memory_usage * 100) / total_memory_machine()

        self.__label_time.setText(f'<b>Current time:</b> {get_current_time()}')
        self.__label_uptime.setText(f'<b>Uptime machine:</b> {get_uptime_machine()}h')
        self.__label_cpu_usage.setText(f'<b>Total CPU used:</b> {format(get_cpu_percent(), ".2f")}%')
        self.__label_memory_usage.setText(f'<b>Total memory used:</b> {format(percent_memory_usage, ".2f")}%')

        text_info_process = f'<b>Total number of processes:</b> {len(self.__data_process)};     '
        total_status = len(self.__status_process) - 1
        for index, status in enumerate(self.__status_process):
            if index == total_status:
                text_info_process += f'{self.__status_process.get(status)} are {status}'
            else:
                text_info_process += f'{self.__status_process.get(status)} are {status},   '

        self.__label_infos_process.setText(text_info_process)

    @Slot(dict, str, str)
    def update_data_process(self, data_process, percent_memory_usage, text_info_process):
        """
        Atualiza os dados dos processos na lista
        """
        location_processes_in_the_list = {}
        for row in range(self.__table_list_process.rowCount()):
            item = self.__table_list_process.item(row, 0)
            if item is not None:
                location_processes_in_the_list[item.text()] = row

        active_process = []
        for pid in data_process:
            row = location_processes_in_the_list.get(str(pid))
            if row is not None:
                for column, value in enumerate(data_process.get(pid)):
                    item = self.__table_list_process.item(row, column)
                    item.setText(value)
                    active_process.append(str(pid))
            else:
                # inserir item que ainda não existe na lista
                new_index = self.__table_list_process.rowCount()
                self.__table_list_process.insertRow(new_index)

                self.__table_list_process.setItem(new_index, 0, QTableWidgetItem(str(data_process.get(pid)[0])))
                self.__table_list_process.setItem(new_index, 1, QTableWidgetItem(str(data_process.get(pid)[1])))
                self.__table_list_process.setItem(new_index, 2, QTableWidgetItem(str(data_process.get(pid)[2])))
                self.__table_list_process.setItem(new_index, 3, QTableWidgetItem(str(data_process.get(pid)[3])))
                self.__table_list_process.setItem(new_index, 4, QTableWidgetItem(str(data_process.get(pid)[4])))
                self.__table_list_process.setItem(new_index, 5, QTableWidgetItem(str(data_process.get(pid)[5])))
                self.__table_list_process.setItem(new_index, 6, QTableWidgetItem(str(data_process.get(pid)[6])))
                self.__table_list_process.setItem(new_index, 7, QTableWidgetItem(str(data_process.get(pid)[7])))

                active_process.append(str(pid))

        for pid, row in location_processes_in_the_list.items():
            if pid not in active_process:
                self.__table_list_process.removeRow(row)

        self.__label_memory_usage.setText(f'<b>Total memory used:</b> {percent_memory_usage}%')
        self.__label_infos_process.setText(text_info_process)

    @Slot(str, str, str)
    def update_infos_process(self, current_time, uptime_machine, cpu_percent):
        self.__label_time.setText(f'<b>Current time:</b> {current_time}')
        self.__label_uptime.setText(f'<b>Uptime machine:</b> {uptime_machine}h')
        self.__label_cpu_usage.setText(f'<b>Total CPU used:</b> {cpu_percent}%')

    def stop_process(self):
        """
        Parar execução de um processo
        """
        pass

    def resume_process(self):
        """
        Resumir execução de um processo
        """
        pass

    def restart_process(self):
        """
        Reiniciar um processo
        """
        pass

    def kill_process(self):
        """
        Finalizar execução de um processo
        """
        row, pid = self.get_selected_process()
        send_signal_process(pid, '15')
        self.__table_list_process.removeRow(row)
        self.__table_list_process.clearSelection()

    def get_selected_process(self):
        """
        Retorna o PID da linha selecionada
        """
        items = self.__table_list_process.selectedItems()
        if items:
            return items[0].row(), items[0].text()

        return None, None


if __name__ == '__main__':
    app = QApplication([])

    window = ProcessManager()
    window.init()

    exit(app.exec())
