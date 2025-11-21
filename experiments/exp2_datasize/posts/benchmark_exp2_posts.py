import requests
import time
import csv
import concurrent.futures
import statistics
import sys
import os

class TimelinePostsBenchmark:
    def __init__(self, root_url: str):
        self.root_url = root_url.rstrip('/')

    def query(self, uid: int):
        start = time.time()
        try:
            r = requests.get(
                f"{self.root_url}/api/timeline",
                params={"user": f"bench{uid}"},
                timeout=60
            )
            return (time.time() - start) * 1000, (r.status_code == 200)
        except Exception:
            return (time.time() - start) * 1000, False

    def run_parallel(self, threads: int):
        users = list(range(1, threads + 1))
        times = []
        fails = 0

        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as pool:
            futures = {pool.submit(self.query, u): u for u in users}
            for fut in concurrent.futures.as_completed(futures):
                t, ok = fut.result()
                times.append(t)
                if not ok:
                    fails += 1

        return statistics.mean(times), fails

    def run_suite(self, param_value: int, repeats: int = 3):
        print(f"=== Exp 2A : {param_value} posts/user ===")

        # Trouver la racine du projet (ProjetMassiveData/)
        ROOT =  os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

        # Dossier out global
        OUT_DIR = os.path.join(ROOT, "out")
        os.makedirs(OUT_DIR, exist_ok=True)

        # Fichier CSV final
        csv_path = os.path.join(OUT_DIR, "post.csv")

        # Déterminer si on doit écrire l’en-tête
        write_header = (not os.path.exists(csv_path)) or (os.path.getsize(csv_path) == 0)

        # Écriture des données (append)
        with open(csv_path, "a", newline="") as f:
            writer = csv.writer(f)

            if write_header:
                writer.writerow(["PARAM", "AVG_TIME", "RUN", "FAILED"])

            for run in range(1, repeats + 1):
                avg, failed = self.run_parallel(50)
                writer.writerow([param_value, f"{avg:.2f}", run, failed])
                f.flush()

                print(f"Run {run}: {avg:.2f} ms, fails={failed}")
                time.sleep(2)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 benchmark_posts.py <posts_per_user>")
        exit(1)

    param = int(sys.argv[1])

    bench = TimelinePostsBenchmark("https://projetmassivedata.ey.r.appspot.com")
    bench.run_suite(param)