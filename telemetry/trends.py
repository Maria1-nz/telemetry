from typing import List, Dict
from .models import ValidValue, TrendValue

TREND_NAMES = [
    "total_objects",
    "valid_count",
    "invalid_count",
    "valid_ratio",
    "avg_value",
    "max_value",
    "min_value",
    "sum_value",
    "unique_objects",
    "sources_count",
    "temperature_avg",
    "temperature_max",
    "cpu_avg",
    "cpu_max",
    "door_true_ratio",
    "error_avg",
    "error_max",
    "range_value",
    "median_value",
    "std_value",]

def _to_number(v) -> float:
    if isinstance(v, bool):
        return 1.0 if v else 0.0
    return float(v)

def compute_trends(
    valid: List[ValidValue],
    invalid_count: int,
    total_objects: int,
    sources_count: int,
    timestamp: float,
) -> List[TrendValue]:

    result: List[TrendValue] = []
    numbers = [_to_number(v.value) for v in valid]

    result.append(TrendValue("total_objects", float(total_objects), timestamp))
    result.append(TrendValue("valid_count", float(len(valid)), timestamp))
    result.append(TrendValue("invalid_count", float(invalid_count), timestamp))

    if total_objects > 0:
        result.append(TrendValue("valid_ratio", len(valid) / total_objects, timestamp))
    else:
        result.append(TrendValue("valid_ratio", 0.0, timestamp))

    if numbers:
        result.append(TrendValue("avg_value", sum(numbers) / len(numbers), timestamp))
        result.append(TrendValue("max_value", max(numbers), timestamp))
        result.append(TrendValue("min_value", min(numbers), timestamp))
        result.append(TrendValue("sum_value", sum(numbers), timestamp))
        sorted_nums = sorted(numbers)
        n = len(sorted_nums)
        median = sorted_nums[n // 2] if n % 2 == 1 else (sorted_nums[n // 2 - 1] + sorted_nums[n // 2]) / 2
        result.append(TrendValue("median_value", median, timestamp))
        mean = sum(numbers) / len(numbers)
        variance = sum((x - mean) ** 2 for x in numbers) / len(numbers)
        result.append(TrendValue("std_value", variance ** 0.5, timestamp))
        result.append(TrendValue("range_value", max(numbers) - min(numbers), timestamp))
    else:
        for name in ["avg_value", "max_value", "min_value", "sum_value",
                     "median_value", "std_value", "range_value"]:
            result.append(TrendValue(name, 0.0, timestamp))

    result.append(TrendValue("unique_objects", float(len({v.object_name for v in valid})), timestamp))
    result.append(TrendValue("sources_count", float(sources_count), timestamp))

    temps = [n for v, n in zip(valid, numbers) if v.object_name.startswith("temp_")]
    cpus = [n for v, n in zip(valid, numbers) if v.object_name.startswith("cpu_")]
    doors = [n for v, n in zip(valid, numbers) if v.object_name.startswith("door_")]
    errors = [n for v, n in zip(valid, numbers) if v.object_name.startswith("err_")]

    result.append(TrendValue("temperature_avg", sum(temps) / len(temps) if temps else 0.0, timestamp))
    result.append(TrendValue("temperature_max", max(temps) if temps else 0.0, timestamp))
    result.append(TrendValue("cpu_avg", sum(cpus) / len(cpus) if cpus else 0.0, timestamp))
    result.append(TrendValue("cpu_max", max(cpus) if cpus else 0.0, timestamp))
    result.append(TrendValue("door_true_ratio", sum(doors) / len(doors) if doors else 0.0, timestamp))
    result.append(TrendValue("error_avg", sum(errors) / len(errors) if errors else 0.0, timestamp))
    result.append(TrendValue("error_max", max(errors) if errors else 0.0, timestamp))
    return result