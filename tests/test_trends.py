from telemetry.trends import compute_trends, TREND_NAMES
from telemetry.models import ValidValue

def make_valid(name, value):
    return ValidValue(name, value, 0.0)

def test_trend_count_is_20():
    trends = compute_trends([], 0, 0, 4, 1.0)
    assert len(trends) == 20

def test_trend_names_match_constant():
    trends = compute_trends([], 0, 0, 4, 1.0)
    names = [t.trend_name for t in trends]
    assert sorted(names) == sorted(TREND_NAMES)

def test_counts():
    valid = [make_valid("temp_1", 10.0), make_valid("cpu_1", 20.0)]
    trends = compute_trends(valid, invalid_count=3, total_objects=5,
                            sources_count=4, timestamp=1.0)
    by_name = {t.trend_name: t.value for t in trends}
    assert by_name["total_objects"] == 5.0
    assert by_name["valid_count"] == 2.0
    assert by_name["invalid_count"] == 3.0

def test_valid_ratio():
    valid = [make_valid("temp_1", 10.0)]
    trends = compute_trends(valid, invalid_count=1, total_objects=2,
                            sources_count=4, timestamp=1.0)
    by_name = {t.trend_name: t.value for t in trends}
    assert by_name["valid_ratio"] == 0.5

def test_valid_ratio_empty():
    trends = compute_trends([], 0, 0, 4, 1.0)
    by_name = {t.trend_name: t.value for t in trends}
    assert by_name["valid_ratio"] == 0.0

def test_avg_max_min_sum():
    valid = [make_valid("temp_1", 10.0), make_valid("temp_2", 20.0), make_valid("temp_3", 30.0)]
    trends = compute_trends(valid, 0, 3, 4, 1.0)
    by_name = {t.trend_name: t.value for t in trends}
    assert by_name["avg_value"] == 20.0
    assert by_name["max_value"] == 30.0
    assert by_name["min_value"] == 10.0
    assert by_name["sum_value"] == 60.0

def test_median_odd():
    valid = [make_valid("t_1", 1.0), make_valid("t_2", 2.0), make_valid("t_3", 100.0)]
    trends = compute_trends(valid, 0, 3, 4, 1.0)
    by_name = {t.trend_name: t.value for t in trends}
    assert by_name["median_value"] == 2.0

def test_median_even():
    valid = [make_valid("t_1", 1.0), make_valid("t_2", 2.0),
             make_valid("t_3", 3.0), make_valid("t_4", 4.0)]
    trends = compute_trends(valid, 0, 4, 4, 1.0)
    by_name = {t.trend_name: t.value for t in trends}
    assert by_name["median_value"] == 2.5

def test_bool_converts_to_number():
    valid = [make_valid("door_1", True), make_valid("door_2", False)]
    trends = compute_trends(valid, 0, 2, 4, 1.0)
    by_name = {t.trend_name: t.value for t in trends}
    assert by_name["door_true_ratio"] == 0.5

def test_temperature_specific():
    valid = [make_valid("temp_1", 20.0), make_valid("temp_2", 30.0)]
    trends = compute_trends(valid, 0, 2, 4, 1.0)
    by_name = {t.trend_name: t.value for t in trends}
    assert by_name["temperature_avg"] == 25.0
    assert by_name["temperature_max"] == 30.0

def test_cpu_specific():
    valid = [make_valid("cpu_1", 40.0), make_valid("cpu_2", 80.0)]
    trends = compute_trends(valid, 0, 2, 4, 1.0)
    by_name = {t.trend_name: t.value for t in trends}
    assert by_name["cpu_avg"] == 60.0
    assert by_name["cpu_max"] == 80.0

def test_error_specific():
    valid = [make_valid("err_1", 5.0), make_valid("err_2", 15.0)]
    trends = compute_trends(valid, 0, 2, 4, 1.0)
    by_name = {t.trend_name: t.value for t in trends}
    assert by_name["error_avg"] == 10.0
    assert by_name["error_max"] == 15.0

def test_empty_valid_sets_zeros():
    trends = compute_trends([], 5, 5, 4, 1.0)
    by_name = {t.trend_name: t.value for t in trends}
    assert by_name["avg_value"] == 0.0
    assert by_name["max_value"] == 0.0
    assert by_name["min_value"] == 0.0
    assert by_name["temperature_avg"] == 0.0

def test_unique_objects():
    valid = [make_valid("obj_1", 1.0), make_valid("obj_1", 2.0),
             make_valid("obj_2", 3.0)]
    trends = compute_trends(valid, 0, 3, 4, 1.0)
    by_name = {t.trend_name: t.value for t in trends}
    assert by_name["unique_objects"] == 2.0

def test_sources_count():
    trends = compute_trends([], 0, 0, 4, 1.0)
    by_name = {t.trend_name: t.value for t in trends}
    assert by_name["sources_count"] == 4.0