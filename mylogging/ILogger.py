from abc import ABC, abstractmethod

class ILogger(ABC):
    @abstractmethod
    def write(self, *values):
        pass

    @abstractmethod
    def close(self):
        pass
