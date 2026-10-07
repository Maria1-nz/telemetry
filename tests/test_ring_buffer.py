from telemetry.ring_buffer import RingBuffer, TrendBuffers
from telemetry.models import TrendValue

def test_ring_buffer_push_and_get():
    rb = RingBuffer(size=5)
    rb.push(1.0)
    rb.push(2.0)
    rb.push(3.0)
    assert rb.get_all() == [1.0, 2.0, 3.0]

def test_ring_buffer_evicts_old():
    rb = RingBuffer(size=3)
    for i in range(5):
        rb.push(float(i))
    assert rb.get_all() == [2.0, 3.0, 4.0]
    assert len(rb) == 3

def test_ring_buffer_latest():
    rb = RingBuffer(size=3)
    assert rb.latest() is None
    rb.push(1.0)
    rb.push(2.0)
    assert rb.latest() == 2.0

def test_ring_buffer_default_size_3600():
    rb = RingBuffer()
    for i in range(4000):
        rb.push(float(i))
    assert len(rb) == 3600
    assert rb.get_all()[0] == 400.0
    assert rb.latest() == 3999.0

def test_trend_buffers_creates_on_push():
    tb = TrendBuffers(size=10)
    tb.push(TrendValue("avg_temp", 25.0, 0.0))
    assert "avg_temp" in tb.names()

def test_trend_buffers_separate_by_name():
    tb = TrendBuffers(size=10)
    tb.push(TrendValue("avg_temp", 25.0, 0.0))
    tb.push(TrendValue("max_cpu", 90.0, 0.0))
    tb.push(TrendValue("avg_temp", 26.0, 1.0))
    assert tb.get("avg_temp") == [25.0, 26.0]
    assert tb.get("max_cpu") == [90.0]

def test_trend_buffers_unknown_returns_empty():
    tb = TrendBuffers(size=10)
    assert tb.get("nonexistent") == []
    assert tb.latest("nonexistent") is None

def test_trend_buffers_latest():
    tb = TrendBuffers(size=5)
    for i in range(10):
        tb.push(TrendValue("avg_temp", float(i), 0.0))
    assert tb.latest("avg_temp") == 9.0
    assert len(tb.get("avg_temp")) == 5