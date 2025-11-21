import requests
import time
import csv
import concurrent.futures
import statistics
import os
import sys
from typing import Tuple

class TimelineFanoutBenchmark:
    def __init__(self, root_url: str):
        self.root_url = root_url.rstrip('/')

    def query(self, uid: int) -> Tuple[float, bool]:
        start = time.time()
        try:
            r = requests.get(
                f"{self.root_url}/api/timeline",
                params={"user": f"bench{uid}"},
                timeout=60
            )
            return (time.time() - start) * 1000, r.status_code == 200
        except Exception:
            return (time.time() - start) * 1000, False

    def run_parallel(self, nb_threads: int) -> Tuple[float, int]:
        users = list(range(1, nb_threads + 1))
        times = []
        failed = 0

        with concurrent.futures.ThreadPoolExecutor(max_workers=nb_threads) as exe:
            tasks = {exe.submit(self.query, u): u for u in users}
            for future in concurrent.futures.as_completed(tasks):
                t, ok = future.result()
                times.append(t)
                if not ok:
                    failed += 1

        return statistics.mean(times), failed

    def run_suite(self, fanout_value: int, repeats: int = 3):
        print(f"=== Exp 2B : fanout={fanout_value} ===")

        # Trouver ProjetMassiveData/
        ROOT = os.path.dirname(
            os.path.dirname(
                os.path.dirname(
                    os.path.dirname(os.path.abspath(__file__))
                )
            )
        )

        OUT_DIR = os.path.join(ROOT, "out")
        os.makedirs(OUT_DIR, exist_ok=True)

        csv_path = os.path.join(OUT_DIR, "fanout.csv")

        # Append + header si nécessaire, pour ne pas écraser le fichier
        write_header = (not os.path.exists(csv_path)) or (os.path.getsize(csv_path) == 0)

        with open(csv_path, "a", newline="") as f:
            writer = csv.writer(f)

            if write_header:
                writer.writerow(["PARAM", "AVG_TIME", "RUN", "FAILED"])

            for run in range(1, repeats + 1):
                avg, failed = self.run_parallel(50)
                writer.writerow([fanout_value, f"{avg:.2f}", run, failed])
                f.flush()
                print(f"  Run {run}: {avg:.2f} ms  | fails={failed}")
                time.sleep(2)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 benchmark_exp2_fanout.py <fanout>")
        exit(1)

    fanout = int(sys.argv[1])

    bench = TimelineFanoutBenchmark("https://projetmassivedata.ey.r.appspot.com")
    bench.run_suite(fanout)