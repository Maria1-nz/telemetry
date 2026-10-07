from telemetry.validator import is_valid_value, validate_batch
from telemetry.models import RawValue

def test_int_is_valid():
    assert is_valid_value(42) is True

def test_float_is_valid():
    assert is_valid_value(3.14) is True

def test_bool_is_valid():
    assert is_valid_value(True) is True
    assert is_valid_value(False) is True

def test_string_is_invalid():
    assert is_valid_value("abc") is False

def test_none_is_invalid():
    assert is_valid_value(None) is False

def test_list_is_invalid():
    assert is_valid_value([1, 2, 3]) is False

def test_validate_batch_splits_correctly():
    raws = [
        RawValue("s", "o1", 42, 0.0),
        RawValue("s", "o2", "bad", 0.0),
        RawValue("s", "o3", True, 0.0),
        RawValue("s", "o4", None, 0.0),
        RawValue("s", "o5", 3.14, 0.0),]

    valid, invalid = validate_batch(raws)
    assert len(valid) == 3
    assert len(invalid) == 2
    assert valid[0].object_name == "o1"
    assert valid[1].object_name == "o3"
    assert valid[2].object_name == "o5"
    assert invalid[0].object_name == "o2"
    assert invalid[1].object_name == "o4"

def test_validate_empty_batch():
    valid, invalid = validate_batch([])
    assert valid == []
    assert invalid == []

def test_invalid_has_reason():
    raws = [RawValue("s", "o1", "bad", 0.0)]
    _, invalid = validate_batch(raws)
    assert len(invalid) == 1
    assert "str" in invalid[0].reason