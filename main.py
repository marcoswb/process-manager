from models.Process import Process

all_processes = ['1084']

for pid in all_processes:
    proc = Process(pid)
    print(f'PID: {proc.pid}')
    print(f'USER: {proc.user}')
    print(f'USER ID: {proc.user_id}')
    print(f'CPU USE: {proc.cpu_usage}%')
    print(f'MEMORY USE: {proc.memory_usage} KB')
    print(f'READ DISK: {proc.disk_read}%')
    print(f'WRITE DISK: {proc.disk_write}%')
    print(f'PRIORITY: {proc.priority}')
