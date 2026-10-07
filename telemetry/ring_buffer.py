from collections import deque
from typing import Dict, List, Optional
from .models import TrendValue

class RingBuffer:
    def __init__(self, size: int = 3600):
        self.size = size
        self._data: deque = deque(maxlen=size)

    def push(self, value: float) -> None:
        self._data.append(value)

    def get_all(self) -> List[float]:
        return list(self._data)

    def latest(self) -> Optional[float]:
        if not self._data:
            return None
        return self._data[-1]

    def __len__(self) -> int:
        return len(self._data)

class TrendBuffers:
    def __init__(self, size: int = 3600):
        self.size = size
        self._buffers: Dict[str, RingBuffer] = {}

    def push(self, trend: TrendValue) -> None:
        if trend.trend_name not in self._buffers:
            self._buffers[trend.trend_name] = RingBuffer(self.size)
        self._buffers[trend.trend_name].push(trend.value)

    def get(self, trend_name: str) -> List[float]:
        buf = self._buffers.get(trend_name)
        if buf is None:
            return []
        return buf.get_all()

    def latest(self, trend_name: str) -> Optional[float]:
        buf = self._buffers.get(trend_name)
        if buf is None:
            return None
        return buf.latest()

    def names(self) -> List[str]:
        return list(self._buffers.keys())