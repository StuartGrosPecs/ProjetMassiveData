import requests
import time
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed

URL = "https://projetmassivedata.appspot.com/api/timeline?user=user1&limit=20"
NREQUESTS = 200        # nombre total de requêtes par run
CSV_PATH = "../../out/conc.csv"


def do_request():
    start = time.time()
    try:
        r = requests.get(URL, timeout=10)
        end = time.time()
        return (end - start) * 1000, (r.status_code != 200)
    except:
        end = time.time()
        return (end - start) * 1000, True


def run_benchmark(concurrency):
    """Lance NREQUESTS requêtes avec <concurrency> threads simultanés."""
    latencies = []
    failures = 0

    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = [executor.submit(do_request) for _ in range(NREQUESTS)]

        for f in as_completed(futures):
            latency, failed = f.result()
            latencies.append(latency)
            if failed:
                failures += 1

    avg = sum(latencies) / len(latencies)
    return avg, failures


def main():
    conc_levels = [1, 10, 20, 50, 100, 1000]

    with open(CSV_PATH, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["PARAM", "AVG_TIME", "RUN", "FAILED"])

        for c in conc_levels:
            for run in range(1, 4):
                avg, failed = run_benchmark(c)
                print(f"C={c} RUN={run} → {avg:.2f} ms, failed={failed}")
                writer.writerow([c, f"{avg:.3f}", run, failed])


if __name__ == "__main__":
    main()
