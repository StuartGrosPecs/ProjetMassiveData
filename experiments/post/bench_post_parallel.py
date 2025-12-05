#!/usr/bin/env python3
import subprocess
import concurrent.futures
import os
import re
import sys
import math

# CONFIG GLOBALE
APP_HOST = "https://projetmassivedata.appspot.com"

USERS = 50               
N_REQ_TOTAL = 100         # nombre total de requêtes globales
N_REQ_PER_USER = N_REQ_TOTAL // USERS
CONCURRENCY_PER_USER = 1  # 1 client par ab donc 50 ab en parallèle
RUNS = 3                 

OUT_DIR = os.path.expanduser("~/ProjetMassiveData/out")
OUT_CSV = os.path.join(OUT_DIR, "post.csv")

os.makedirs(OUT_DIR, exist_ok=True)


# Lance un ab pour un user
def run_ab_for_user(uid, param, run_id):
    url = f"{APP_HOST}/api/timeline?user=user{uid}"

    cmd = [
        "ab",
        "-k",
        "-n", str(N_REQ_PER_USER),
        "-c", str(CONCURRENCY_PER_USER),
        url,
    ]

    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    output = result.stdout

    # Analyse
    avg_time = math.nan
    failed = 1

    # Time per request
    m = re.search(r"Time per request:\s+([\d\.]+)\s+\[ms\]", output)
    if m:
        try:
            avg_time = float(m.group(1))
        except ValueError:
            avg_time = math.nan

    # Failed requests
    m2 = re.search(r"Failed requests:\s+(\d+)", output)
    if m2:
        failed = 0 if int(m2.group(1)) == 0 else 1

    print(f"user{uid} → AVG={avg_time} ms | FAILED={failed}")
    return uid, avg_time, failed


def main():
    if len(sys.argv) != 2:
        print("Usage: bench_post_parallel.py <posts_per_user>")
        print("Exemple: bench_post_parallel.py 100")
        sys.exit(1)

    param = sys.argv[1]  # 10, 100, 1000

    print(f"Benchmark POST parallèle pour PARAM={param}")
    print(f"   50 timelines distinctes")
    print(f"   {RUNS} RUNS automatiques\n")

    # Init CSV
    if not os.path.exists(OUT_CSV) or os.path.getsize(OUT_CSV) == 0:
        with open(OUT_CSV, "w") as f:
            f.write("PARAM,AVG_TIME,RUN,FAILED\n")

    # COLD START
    warmup_url = f"{APP_HOST}/api/timeline?user=user1"
    print("[INFO] Cold start : envoi d'une requête de réveil (non comptabilisée)...")
    try:
        subprocess.run(
            ["ab", "-k", "-n", "1", "-c", "1", warmup_url],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            text=True,
            check=False,
        )
    except Exception as e:
        print(f"[WARN] Cold start échoué : {e}")

    for run_id in range(1, RUNS + 1):
        print(f"\n========================================")
        print(f"RUN {run_id}/{RUNS} pour PARAM={param}")
        print("========================================\n")

        results = []

        # Lances 50 AB en parallèle
        with concurrent.futures.ThreadPoolExecutor(max_workers=USERS) as executor:
            futures = [
                executor.submit(run_ab_for_user, uid, param, run_id)
                for uid in range(1, USERS + 1)
            ]
            for future in concurrent.futures.as_completed(futures):
                results.append(future.result())

        # Temps moyen global
        valid_times = [avg for (_, avg, failed) in results if not math.isnan(avg)]
        if valid_times:
            avg_global = sum(valid_times) / len(valid_times)
            avg_global_str = f"{avg_global:.3f}"
        else:
            avg_global_str = "NaN"

        # FAILED
        failed_global = 1 if any(failed == 1 for (_, _, failed) in results) else 0

        print(f"Résultats RUN {run_id}")
        print(f"   AVG_TIME global = {avg_global_str} ms")
        print(f"   FAILED global   = {failed_global}\n")

        # Ajout au CSV
        with open(OUT_CSV, "a") as f:
            f.write(f"{param},{avg_global_str},{run_id},{failed_global}\n")

    print("\nBenchmark POST terminé.")
    print(f"Résultats cumulés dans : {OUT_CSV}")


if __name__ == "__main__":
    main()
