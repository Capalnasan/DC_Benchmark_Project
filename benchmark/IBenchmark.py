from abc import ABC, abstractmethod

class IBenchmark(ABC):
    """Interface for benchmark classes."""

    @abstractmethod
    def initialize(self, *params):
        pass

    @abstractmethod
    def run(self, *params):
        pass

    @abstractmethod
    def clean(self):
        pass

    @abstractmethod
    def cancel(self):
        pass
