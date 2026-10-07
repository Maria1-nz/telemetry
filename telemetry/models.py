from dataclasses import dataclass
from typing import Any, Union
Scalar = Union[int, float, bool]

@dataclass
class RawValue:
    source: str
    object_name: str
    value: Any
    timestamp: float

@dataclass
class ValidValue:
    object_name: str
    value: Scalar
    timestamp: float

@dataclass
class InvalidValue:
    object_name: str
    value: Any
    reason: str
    timestamp: float

@dataclass
class TrendValue:
    trend_name: str
    value: float
    timestamp: float