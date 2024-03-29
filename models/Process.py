import pwd
import os
from utils.functions import *


class Process:

    def __init__(self, pid):
        self.pid = pid
        self.name = ''
        self.status = ''
        self.user = ''
        self.user_id = ''
        self.cpu_usage = 0
        self.memory_usage = 0
        self.disk_read = 0
        self.disk_write = 0
        self.priority = ''

        self.load_information_process()

    def load_information_process(self):
        """
        Carregar informações do processo
        """
        self.name, self.status = self.get_name_status_process()
        self.user, self.user_id = self.get_user_process()
        self.cpu_usage = self.get_process_cpu_usage()
        self.memory_usage = self.get_memory_process()
        self.disk_read, self.disk_write = self.get_disk_use()
        self.priority = self.get_process_priority()

    def get_user_process(self):
        """
        Retorna o nome do usuário vinculado ao processo
        """
        target_uid = ''
        with open(f'/proc/{self.pid}/status') as status_file:
            for line in status_file.readlines():
                if line.startswith('Uid:'):
                    target_uid = line.split('\t')[3]

        username = pwd.getpwuid(format_int(target_uid)).pw_name
        return username, target_uid

    def get_name_status_process(self):
        """
        Retorna o nome e status do processo
        """
        name = ''
        status = ''
        with open(f'/proc/{self.pid}/status') as status_file:
            for line in status_file.readlines():
                if line.startswith('Name:'):
                    name = line.split(':')[1].replace('\n', '').strip()
                if line.startswith('State:'):
                    status = line.split(':')[1].replace('\n', '').strip()

        return name, status

    def get_process_cpu_usage(self):
        """
        Retorna a porcentagem de uso de CPU de um processo
        """
        with open(f'/proc/{self.pid}/stat', 'r') as stat_file:
            stat_info = stat_file.read().split()

        with open('/proc/uptime', 'r') as read_file:
            uptime_seconds = float(read_file.readline().split()[0])

        utime = float(stat_info[13])
        stime = float(stat_info[14])
        start_time = float(stat_info[21])
        number_of_clock_ticks_per_second = os.sysconf(os.sysconf_names['SC_CLK_TCK'])

        utime_seconds = utime / number_of_clock_ticks_per_second
        stime_seconds = stime / number_of_clock_ticks_per_second
        start_time_seconds = start_time / number_of_clock_ticks_per_second

        process_elapsed_time = uptime_seconds - start_time_seconds
        process_usage_seconds = utime_seconds - stime_seconds
        process_usage = process_usage_seconds * 100 / process_elapsed_time
        return process_usage

    def get_memory_process(self):
        """
        Retorna a memória que o processo está usando(em KB)
        """
        use_memory = 0
        with open(f"/proc/{self.pid}/status", 'r') as status_file:
            for line in status_file.readlines():
                if line.startswith("VmRSS"):
                    use_memory = line.split()[1]

        return use_memory

    def get_disk_use(self):
        """
        Retorna quantos KB o processo está usando para escrita e leitura em disco
        """
        with open(f'/proc/{self.pid}/io', 'r') as io_file:
            io_data = io_file.readlines()

        bytes_read = ''
        bytes_written = ''
        for line in io_data:
            if line.startswith('read_bytes'):
                bytes_read = int(line.split(':')[1])

            if line.startswith('write_bytes'):
                bytes_written = int(line.split(':')[1])

        kilobytes_read = 0
        kilobytes_written = 0
        if bytes_read > 0:
            kilobytes_read = bytes_read / 1024

        if bytes_written > 0:
            kilobytes_written = bytes_written / 1024

        return kilobytes_read, kilobytes_written

    def get_process_priority(self):
        """
        Retorna a prioridade um processo
        """
        with open(f'/proc/{self.pid}/stat', 'r') as stat_file:
            stat_data = stat_file.read()

        # A prioridade (nice value) está na posição 18
        stat_parts = stat_data.split()
        priority_level = int(stat_parts[18])

        # concatena ao nível de prioridade o seu status(baixa, padrão ou alta)
        if priority_level < -1:
            priority = f'{priority_level} (low)'
        elif priority_level == 0:
            priority = f'{priority_level} (default)'
        else:
            priority = f'{priority_level} (high)'

        return priority
