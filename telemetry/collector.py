import time
import signal
import sys
from .sources import create_all_sources
from .validator import validate_batch
from .database import Database
from .wal import WAL
from .ring_buffer import TrendBuffers
from .trends import compute_trends

class Collector:
    def __init__(self, db_path: str = "telemetry.db", wal_path: str = "wal.log"):
        self.sources = create_all_sources()
        self.db = Database(db_path)
        self.wal = WAL(wal_path)
        self.buffers = TrendBuffers(size=3600)
        self.running = False
        self.tick = 0

    def start(self, max_ticks: int = None):
        self.db.connect()

        recovered = self.wal.recover_into(self.db)
        if recovered > 0:
            print(f"[WAL] восстановлено {recovered} записей трендов")

        self.running = True
        signal.signal(signal.SIGINT, self._on_stop)

        print("[Сборщик] старт")
        start_time = time.time()

        try:
            while self.running:
                tick_start = time.time()
                self.tick += 1
                self._run_tick(self.tick)

                if max_ticks is not None and self.tick >= max_ticks:
                    break

                elapsed = time.time() - tick_start
                sleep_for = 1.0 - elapsed
                if sleep_for > 0:
                    time.sleep(sleep_for)
        finally:
            self.db.close()
            print(f"[Сборщик] стоп. Всего тиков: {self.tick}")

    def _on_stop(self, signum, frame):
        self.running = False

    def _run_tick(self, tick: int):
        timestamp = time.time()

        all_raw = []
        for source in self.sources:
            all_raw.extend(source.generate(timestamp))

        valid, invalid = validate_batch(all_raw)

        self.db.save_valid(valid)
        self.db.save_invalid(invalid)

        trends = compute_trends(
            valid=valid,
            invalid_count=len(invalid),
            total_objects=len(all_raw),
            sources_count=len(self.sources),
            timestamp=timestamp,)

        for trend in trends:
            self.wal.append(trend)
            self.db.save_trend(trend)
            self.buffers.push(trend)

        print(f"[tick {tick}] собрано {len(all_raw)} | "
              f"валидных {len(valid)} | невалидных {len(invalid)} | "
              f"трендов {len(trends)}")