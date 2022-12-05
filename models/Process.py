class Process:

    def __init__(self, pid):
        self.pid = pid
        self.user = ''
        self.cpu_usage = ''
        self.memory_usage = ''
        self.disk_read = ''
        self.disk_write = ''
        self.priority = ''
    

    def load_infos(self):
        pass

    