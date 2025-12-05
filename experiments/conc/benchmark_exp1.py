#!/usr/bin/env python3
import subprocess
import os

# CONFIG
BASE_URL = "https://projetmassivedata.appspot.com/api/timeline"
OUT_FILE = "../../out/conc.csv"
REPEATS = 3
N_REQ = 1

# users simultanés
CONCURRENCY_LEVELS = [1, 10, 20, 50, 100, 1000]

os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)

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
            line = next(l for l in output.splitlines() if "Time per request" in l)
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


# Boucle sur tout les niveaux de conc
for USERS in CONCURRENCY_LEVELS:
    print(f"\n=== Benchmark avec {USERS} utilisateurs simultanés ===")

    for run in range(1, REPEATS + 1):
        print(f"\n  → Run {run}/{REPEATS}")

        urls = [f"{BASE_URL}?user=user{i}" for i in range(1, USERS + 1)]

        results = run_ab_parallel(urls)

        total_ms = sum(r[0] for r in results)
        total_failed = sum(r[1] for r in results)

        avg_time = total_ms / USERS

        with open(OUT_FILE, "a") as f:
            f.write(f"{USERS},{avg_time:.2f},{run},{total_failed}\n")

        print(f"     Temps moyen : {avg_time:.2f} ms | erreurs : {total_failed}")

print("\n=== Fin ===")
