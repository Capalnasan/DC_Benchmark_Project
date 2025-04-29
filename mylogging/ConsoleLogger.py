from mylogging.ILogger import ILogger

class ConsoleLogger(ILogger):
    def write(self, *values):
        print(*values)

    def close(self):
        pass
