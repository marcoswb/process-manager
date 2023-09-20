from os import system, listdir
from os.path import isdir
from models.Process import Process
from utils.functions import *

all_processes = ['1983']

system('clear')
print('NAME   |', end='')
print('PID   |', end='')
print('STATUS   |', end='')
print('USER   |', end='')
print('USER ID   |', end='')
print('CPU USE   |', end='')
print('MEMORY USE   |', end='')
print('READ DISK   |', end='')
print('WRITE DISK   |', end='')
print('PRIORITY   |', end='')
print('')
for directory in listdir('/proc'):
    if not isdir(f'/proc/{directory}') or not format_int(directory):
        continue

    proc = Process(directory)
    print(f'{proc.name}   |', end='')
    print(f'{proc.pid}   |', end='')
    print(f'{proc.status}   |', end='')
    print(f'{proc.user}   |', end='')
    print(f'{proc.user_id}   |', end='')
    print(f'{proc.cpu_usage}%   |', end='')
    print(f'{proc.memory_usage} KB   |', end='')
    print(f'{proc.disk_read} KB   |', end='')
    print(f'{proc.disk_write} KB   |', end='')
    print(f'{proc.priority}   |', end='')
    print('')
