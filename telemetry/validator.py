from typing import List, Tuple
from .models import RawValue, ValidValue, InvalidValue

def is_valid_value(value) -> bool:
    if isinstance(value, bool):
        return True
    if isinstance(value, (int, float)):
        return True
    return False

def validate_batch(raw_values: List[RawValue]) -> Tuple[List[ValidValue], List[InvalidValue]]:
    valid: List[ValidValue] = []
    invalid: List[InvalidValue] = []

    for raw in raw_values:
        if is_valid_value(raw.value):
            valid.append(ValidValue(
                object_name=raw.object_name,
                value=raw.value,
                timestamp=raw.timestamp,
            ))
        else:
            invalid.append(InvalidValue(
                object_name=raw.object_name,
                value=raw.value,
                reason=f"недопустимый тип: {type(raw.value).__name__}",
                timestamp=raw.timestamp,
            ))
    return valid, invalid