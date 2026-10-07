from telemetry.collector import Collector

def main():
    collector = Collector(db_path="demo.db", wal_path="demo_wal.log")
    collector.start(max_ticks=5)

if __name__ == "__main__":
    main()