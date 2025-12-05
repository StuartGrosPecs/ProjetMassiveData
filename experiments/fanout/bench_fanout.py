#!/usr/bin/env python3
import subprocess
import argparse
import os

# Le fanout passé en argument (10, 50 ou 100)
parser = argparse.ArgumentParser(description="Benchmark Fanout TinyInsta")
parser.add_argument("--param", type=int, required=True,
                    help="Fanout (nombre de followees : 10, 50, 100)")
args = parser.parse_args()
PARAM = args.param

# CONFIG
BASE_URL = "https://projetmassivedata.appspot.com/api/timeline"

OUT_FILE = "../../out/fanout.csv"

REPEATS = 3
N_REQ = 1
CONCURRENCY = 50 

os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)

# init CSV
if not os.path.exists(OUT_FILE) or os.path.getsize(OUT_FILE) == 0:
    with open(OUT_FILE, "w") as f:
        f.write("PARAM,AVG_TIME,RUN,FAILED\n")


# Lance ab en parallèle
def run_ab_parallel(urls):
    procs = []
    results = []

    for url in urls:
        p = subprocess.Popen(
            ["ab", "-l", "-s", "500000", "-n", str(N_REQ), "-c", "1", url],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        procs.append(p)

    for p in procs:
        output = p.communicate()[0]

        try:
            line = next(l for l in output.splitlines()
                        if "Time per request" in l and "across all" not in l)
            avg_ms = float(line.split()[3])
        except Exception:
            avg_ms = 9999.0

        try:
            line = next(l for l in output.splitlines() if "Failed requests" in l)
            failed = int(line.split()[2])
        except Exception:
            failed = 1

        results.append((avg_ms, failed))

    return results


# BENCHMARK POUR UN SEUL PARAM
print(f"\n=== Benchmark FANOUT={PARAM} (50 utilisateurs simultanés) ===")

# COLD START
print("[INFO] Cold start : envoi d'une requête de 'réveil' (non comptabilisée)...")
try:
    subprocess.run(
        [
            "ab",
            "-l",
            "-s", "500000",
            "-n", "1",
            "-c", "1",
            f"{BASE_URL}?user=user1"
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        text=True,
        check=False,
    )
except Exception as e:
    print(f"[WARN] Cold start a échoué : {e}")


for run in range(1, REPEATS + 1):
    print(f"\n  → Run {run}/{REPEATS}")

    # 50 utilisateurs simultanés
    urls = [f"{BASE_URL}?user=user{i}" for i in range(1, CONCURRENCY + 1)]

    results = run_ab_parallel(urls)

    total_ms = sum(r[0] for r in results)
    total_failed = sum(r[1] for r in results)

    avg_time = total_ms / CONCURRENCY

    with open(OUT_FILE, "a") as f:
        f.write(f"{PARAM},{avg_time:.2f},{run},{total_failed}\n")

    print(f"     Temps moyen : {avg_time:.2f} ms | erreurs : {total_failed}")

print("\n=== Fin ===")
