import os
from typing import List, Optional
from .models import TrendValue

class WAL:
    def __init__(self, path: str = "wal.log"):
        self.path = path

    def append(self, trend: TrendValue) -> None:
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(f"{trend.timestamp}|{trend.trend_name}|{trend.value}|PENDING\n")
            f.flush()
            os.fsync(f.fileno())
            f.write(f"{trend.timestamp}|{trend.trend_name}|{trend.value}|COMMIT\n")
            f.flush()
            os.fsync(f.fileno())

    def read_pending(self) -> List[str]:
        if not os.path.exists(self.path):
            return []
        entries = {}
        with open(self.path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split("|")
                if len(parts) != 4:
                    continue
                ts, name, value, status = parts
                key = (ts, name, value)
                entries[key] = status

        pending = [k for k, v in entries.items() if v == "PENDING"]
        return ["|".join(k) for k in pending]

    def truncate(self) -> None:
        if os.path.exists(self.path):
            open(self.path, "w", encoding="utf-8").close()

    def recover_into(self, db) -> int:
        pending = self.read_pending()
        if not pending:
            self.truncate()
            return 0

        from .models import TrendValue
        recovered = 0
        for line in pending:
            ts, name, value = line.split("|")
            db.save_trend(TrendValue(
                trend_name=name,
                value=float(value),
                timestamp=float(ts),
            ))
            recovered += 1
        self.truncate()
        return recovered