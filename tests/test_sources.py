from telemetry.sources import (
    create_all_sources,
    TemperatureSensor,
    CpuLoadSensor,
    DoorSensor,
    ErrorCounter,)

def test_create_all_sources_returns_four():
    sources = create_all_sources()
    assert len(sources) == 4

def test_all_sources_have_unique_names():
    sources = create_all_sources()
    names = [s.name for s in sources]
    assert len(set(names)) == 4

def test_temperature_source_count_range():
    src = TemperatureSensor()
    for _ in range(20):
        result = src.generate(0.0)
        assert 100 <= len(result) <= 600

def test_cpu_source_count_range():
    src = CpuLoadSensor()
    for _ in range(20):
        result = src.generate(0.0)
        assert 100 <= len(result) <= 600

def test_door_source_count_range():
    src = DoorSensor()
    for _ in range(20):
        result = src.generate(0.0)
        assert 100 <= len(result) <= 600

def test_error_source_count_range():
    src = ErrorCounter()
    for _ in range(20):
        result = src.generate(0.0)
        assert 100 <= len(result) <= 600

def test_temperature_object_names():
    src = TemperatureSensor()
    result = src.generate(0.0)
    assert all(v.object_name.startswith("temp_") for v in result)

def test_cpu_object_names():
    src = CpuLoadSensor()
    result = src.generate(0.0)
    assert all(v.object_name.startswith("cpu_") for v in result)

def test_door_object_names():
    src = DoorSensor()
    result = src.generate(0.0)
    assert all(v.object_name.startswith("door_") for v in result)

def test_error_object_names():
    src = ErrorCounter()
    result = src.generate(0.0)
    assert all(v.object_name.startswith("err_") for v in result)

def test_source_returns_correct_source_name():
    src = TemperatureSensor()
    result = src.generate(0.0)
    assert all(v.source == "temperature" for v in result)

def test_timestamp_is_set():
    src = CpuLoadSensor()
    result = src.generate(123.45)
    assert all(v.timestamp == 123.45 for v in result)