from mylogging.ILogger import ILogger

class FileLogger(ILogger):
    def __init__(self, filename):
        self.file = open(filename, 'w')

    def write(self, *values):
        self.file.write(' '.join(map(str, values)) + '\n')

    def close(self):
        self.file.close()
