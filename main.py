from models.Process import Process

all_processes = ['1311']

for pid in all_processes:
    proc = Process(pid)
    print(proc.pid)
    print(proc.user)
    print(proc.user_id)
    print(proc.cpu_usage)
    print(proc.memory_usage)
    print(proc.disk_read)
    print(proc.disk_write)
    print(proc.priority)
