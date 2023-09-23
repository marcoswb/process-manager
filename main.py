from os import system, listdir
from os.path import isdir

from models.Process import Process
from utils.functions import *


class ProcessManager:

    def __init__(self):
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

    def load_columns(self):
        """
        Carrega os tamanhos dos textos do cabeçalho
        """
        for column in self.__columns_header:
            self.save_length_column(column, column)

    def load_data_process(self):
        """
        Carrega os dados dos processos em memória
        """
        for directory in listdir('/proc'):
            if not isdir(f'/proc/{directory}') or not format_int(directory):
                continue

            proc = Process(directory)
            self.__data_process.append(proc)

            self.save_length_column(proc.pid, 'PID')
            self.save_length_column(proc.user, 'USER')
            self.save_length_column(proc.name, 'NAME')
            self.save_length_column(proc.priority, 'PRIORITY')
            self.save_length_column(proc.cpu_usage, 'TOTAL CPU USAGE')
            self.save_length_column(proc.memory_usage, 'MEMORY USAGE')
            self.save_length_column(proc.disk_read, 'DISK READ')
            self.save_length_column(proc.disk_write, 'DISK WRITE')

            self.__total_memory_usage += float(proc.memory_usage)
            if not self.__status_process.get(proc.status):
                self.__status_process[proc.status] = 0

            self.__status_process[proc.status] += 1

    def save_length_column(self, value, column):
        """
        Salva o tamanho máximo que cada coluna tem que ter
        """
        if self.__length_columns.get(column):
            if self.__length_columns.get(column) < len(str(value)):
                self.__length_columns[column] = len(str(value))
        else:
            self.__length_columns[column] = len(str(value))

    def get_number_free_spaces(self, column, value):
        """
        Retorna o numero de espaços em branco que precisa ser deixado
        """
        length = self.__length_columns.get(column)
        return length - len(str(value)) + 5

    def show(self):
        """
        Mostra os dados em tela
        """
        self.load_columns()
        self.load_data_process()

        self.show_infos_process()
        self.show_header()
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

    def show_header(self):
        """
        Grava em tela o cabeçalho do gerenciador
        """
        for column in self.__columns_header:
            print(column, ' '*self.get_number_free_spaces(column, column), end='')

        print('')

    def show_data(self):
        """
        Grava em tela os dados dos processos
        """
        for proc in self.__data_process:
            print(proc.pid, ' ' * self.get_number_free_spaces('PID', proc.pid), end='')
            print(proc.user, ' ' * self.get_number_free_spaces('USER', proc.user), end='')
            print(proc.name, ' ' * self.get_number_free_spaces('NAME', proc.name), end='')
            print(proc.priority, ' ' * self.get_number_free_spaces('PRIORITY', proc.priority), end='')
            print(f'{proc.memory_usage} KB', ' ' * self.get_number_free_spaces('MEMORY USAGE', f'{proc.memory_usage} KB'), end='')
            print(f'{proc.disk_read} KB', ' ' * self.get_number_free_spaces('DISK READ', f'{proc.disk_read} KB'), end='')
            print(f'{proc.disk_write} KB', ' ' * self.get_number_free_spaces('DISK WRITE', f'{proc.disk_write} KB'), end='')
            print('')


if __name__ == '__main__':
    system('clear')
    app = ProcessManager()
    app.show()
