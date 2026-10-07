import random
from abc import ABC, abstractmethod
from typing import List
from .models import RawValue

class BaseSource(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def generate(self, timestamp: float) -> List[RawValue]:
        pass

    def _random_count(self) -> int:
        return random.randint(100, 600)

    def _maybe_garbage(self):
        if random.random() < 0.02:
            return random.choice(["garbage", None, [], {}])
        return None

class TemperatureSensor(BaseSource):
    def __init__(self):
        super().__init__("temperature")

    def generate(self, timestamp: float) -> List[RawValue]:
        count = self._random_count()
        result = []
        for i in range(count):
            garbage = self._maybe_garbage()
            if garbage is not None:
                value = garbage
            else:
                value = round(random.uniform(15.0, 95.0), 2)
            result.append(RawValue(
                source=self.name,
                object_name=f"temp_{i}",
                value=value,
                timestamp=timestamp,
            ))
        return result

class CpuLoadSensor(BaseSource):
    def __init__(self):
        super().__init__("cpu_load")

    def generate(self, timestamp: float) -> List[RawValue]:
        count = self._random_count()
        result = []
        for i in range(count):
            garbage = self._maybe_garbage()
            if garbage is not None:
                value = garbage
            else:
                value = random.randint(0, 100)
            result.append(RawValue(
                source=self.name,
                object_name=f"cpu_{i}",
                value=value,
                timestamp=timestamp,
            ))
        return result

class DoorSensor(BaseSource):
    def __init__(self):
        super().__init__("door")

    def generate(self, timestamp: float) -> List[RawValue]:
        count = self._random_count()
        result = []
        for i in range(count):
            garbage = self._maybe_garbage()
            if garbage is not None:
                value = garbage
            else:
                value = random.choice([True, False])
            result.append(RawValue(
                source=self.name,
                object_name=f"door_{i}",
                value=value,
                timestamp=timestamp,
            ))
        return result

class ErrorCounter(BaseSource):
    def __init__(self):
        super().__init__("error_counter")

    def generate(self, timestamp: float) -> List[RawValue]:
        count = self._random_count()
        result = []
        for i in range(count):
            garbage = self._maybe_garbage()
            if garbage is not None:
                value = garbage
            else:
                value = random.randint(0, 255)
            result.append(RawValue(
                source=self.name,
                object_name=f"err_{i}",
                value=value,
                timestamp=timestamp,
            ))
        return result

def create_all_sources() -> List[BaseSource]:
    return [
        TemperatureSensor(),
        CpuLoadSensor(),
        DoorSensor(),
        ErrorCounter(),
    ]