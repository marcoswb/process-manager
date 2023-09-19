import pwd
import os
import time
from utils.functions import *


class Process:

    def __init__(self, pid):
        self.pid = pid
        self.user = None
        self.user_id = None
        self.cpu_usage = None
        self.memory_usage = None
        self.disk_read = None
        self.disk_write = None
        self.priority = None

        self.load_information_process()

    def load_information_process(self):
        """
        Carregar informações do processo
        """
        self.user, self.user_id = self.get_user_process()
        self.cpu_usage = self.get_process_cpu_usage()
        self.memory_usage = self.get_memory_process()
        self.disk_read, self.disk_write = self.get_disk_use()
        self.priority = self.get_process_priority()

    def get_user_process(self):
        """
        Retorna o nome do usuário vinculado ao processo
        """
        target_uid = None
        with open(f'/proc/{self.pid}/status') as status_file:
            for line in status_file.readlines():
                if line.startswith('Uid:'):
                    target_uid = line.split('\t')[3]

        username = pwd.getpwuid(format_int(target_uid)).pw_name
        return username, target_uid

    def get_process_cpu_usage(self):
        """
        Retorna a porcentagem de uso de CPU de um processo
        """
        with open(f'/proc/{self.pid}/stat', 'r') as stat_file:
            stat_info = stat_file.read().split()

        utime = float(stat_info[13])
        stime = float(stat_info[14])
        cutime = float(stat_info[15])
        cstime = float(stat_info[16])

        total_jiffies = utime + stime + cutime + cstime
        number_of_clock_ticks_per_second = os.sysconf(os.sysconf_names['SC_CLK_TCK'])

        uptime = time.time() - (float(stat_info[21]) / number_of_clock_ticks_per_second)
        cpu_percent = ((total_jiffies / number_of_clock_ticks_per_second) / uptime) * 100.0

        before_point = str(cpu_percent).split('.')[0]
        after_point = str(cpu_percent).split('.')[1]
        return f'{before_point}.{after_point[:4]}'

    def get_memory_process(self):
        """
        Retorna a memória que o processo está usando(em KB)
        """
        use_memory = None
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
