from sys import exit
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox, QHeaderView
from PySide6.QtCore import QFile
from os import system, listdir
from os.path import isdir

from models.Process import Process
from utils.functions import *


class ProcessManager(QMainWindow):

    def __init__(self):
        super().__init__()

        self.__data_process = []
        self.__length_columns = {}
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
        self.__window.showMaximized()

    def load_data_process(self):
        """
        Carrega os dados dos processos em memória
        """
        for directory in listdir('/proc'):
            if not isdir(f'/proc/{directory}') or not format_int(directory):
                continue

            proc = Process(directory)
            self.__data_process.append(proc)

            self.__total_memory_usage += float(proc.memory_usage)
            if not self.__status_process.get(proc.status):
                self.__status_process[proc.status] = 0

            self.__status_process[proc.status] += 1

    def show(self):
        """
        Mostra os dados em tela
        """
        self.load_data_process()

        self.show_infos_process()
        self.show_data()

    def show_infos_process(self):
        """
        Mostra em tela alguns dados gerais dos processos
        """
        percent_memory_usage = (self.__total_memory_usage * 100) / total_memory_machine()
        total_cpu_usage = get_cpu_percent()
        print(f'Horário atual: {get_current_time()}, máquina ativa a {get_uptime_machine()}h')
        print(f'Número total de processos: {len(self.__data_process)}, ', end='')

        total_status = len(self.__status_process) -1
        for index, status in enumerate(self.__status_process):
            if index == total_status:
                print(f'{status}: {self.__status_process.get(status)}')
            else:
                print(f'{status}: {self.__status_process.get(status)}, ', end='')

        print(f'Total de CPU utilizado: {format(total_cpu_usage, ".2f")}%')
        print(f'Total de memória utilizada: {format(percent_memory_usage, ".2f")}%')

    def show_data(self):
        """
        Grava em tela os dados dos processos
        """
        for proc in self.__data_process:
            print(proc.pid)
            print(proc.user)
            print(proc.name)
            print(proc.priority)
            print(f'{proc.memory_usage} KB')
            print(f'{proc.disk_read} KB')
            print(f'{proc.disk_write} KB')
            print('')

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
        pass


if __name__ == '__main__':
    app = QApplication([])

    window = ProcessManager()
    window.init()

    exit(app.exec())

