import os
from telemetry.wal import WAL
from telemetry.models import TrendValue
from telemetry.database import Database

def test_wal_append_creates_file(tmp_path):
    path = str(tmp_path / "test.log")
    w = WAL(path)
    w.append(TrendValue("avg_temp", 25.5, 1.0))
    assert os.path.exists(path)

def test_wal_no_pending_after_clean_append(tmp_path):
    path = str(tmp_path / "test.log")
    w = WAL(path)
    w.append(TrendValue("avg_temp", 25.5, 1.0))
    w.append(TrendValue("max_cpu", 90.0, 1.0))
    assert w.read_pending() == []

def test_wal_read_pending_on_crash(tmp_path):
    path = str(tmp_path / "crash.log")
    with open(path, "w", encoding="utf-8") as f:
        f.write("1.0|avg_temp|25.5|PENDING\n")
    w = WAL(path)
    pending = w.read_pending()
    assert len(pending) == 1
    assert "avg_temp" in pending[0]

def test_wal_truncate_empties_file(tmp_path):
    path = str(tmp_path / "test.log")
    w = WAL(path)
    w.append(TrendValue("avg_temp", 25.5, 1.0))
    w.truncate()
    assert os.path.getsize(path) == 0

def test_wal_recover_into_db(tmp_path):
    path = str(tmp_path / "recover.log")
    with open(path, "w", encoding="utf-8") as f:
        f.write("1.0|avg_temp|25.5|PENDING\n")
        f.write("2.0|max_cpu|90.0|PENDING\n")

    db = Database(":memory:")
    db.connect()
    w = WAL(path)
    recovered = w.recover_into(db)
    assert recovered == 2
    assert db.count_trends() == 2
    assert w.read_pending() == []
    db.close()

def test_wal_recover_empty_file(tmp_path):
    path = str(tmp_path / "empty.log")
    open(path, "w").close()
    db = Database(":memory:")
    db.connect()
    w = WAL(path)
    recovered = w.recover_into(db)
    assert recovered == 0
    assert db.count_trends() == 0
    db.close()

def test_wal_read_pending_missing_file(tmp_path):
    path = str(tmp_path / "does_not_exist.log")
    w = WAL(path)
    assert w.read_pending() == []