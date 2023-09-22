import time


def format_int(value):
    try:
        return int(value)
    except:
        return 0


def get_current_time():
    return time.strftime('%H:%M:%S', time.localtime())


def get_uptime_machine():
    with open('/proc/uptime', 'r') as read_file:
        uptime_seconds = float(read_file.readline().split()[0])

    minutes, seconds = divmod(uptime_seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return '%d:%02d:%02d' % (hours, minutes, seconds)


def total_memory_machine():
    with open('/proc/meminfo', 'r') as read_file:
        for line in read_file.readlines():
            if line.startswith('MemTotal'):
                return float(line.split(':')[1].replace('kB', '').strip())
