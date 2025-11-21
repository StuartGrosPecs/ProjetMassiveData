import requests
import time
import csv
import concurrent.futures
import statistics
from typing import List, Tuple

class TimelineLoadTester:
    def __init__(self, root_url: str):
        # On retire un éventuel / à la fin de l'URL pour éviter les doublons
        self.root_url = root_url.rstrip('/')

    def query_timeline(self, uid: int) -> Tuple[float, bool]:
        """
        Envoie une requête timeline pour un utilisateur "benchX".
        Renvoie le temps en millisecondes + si ça a marché ou pas.
        """
        start = time.time()
        try:
            r = requests.get(
                f"{self.root_url}/api/timeline",
                params={"user": f"bench{uid}"},
                timeout=60
            )
            return (time.time() - start) * 1000, (r.status_code == 200)
        except Exception as err:
            print(f"[Erreur] bench{uid} → {err}")
            return (time.time() - start) * 1000, False

    def run_parallel_requests(self, total_users: int, nb_threads: int) -> Tuple[float, int]:
        """
        Lance plusieurs requêtes en même temps pour voir si ça tient la route.
        """
        print(f"→ Test avec {nb_threads} requêtes en parallèle")

        user_list = list(range(1, min(total_users, 1000) + 1))
        times = []
        failed = 0

        # Pool de requêtes parallèles
        with concurrent.futures.ThreadPoolExecutor(max_workers=nb_threads) as pool:
            tasks = {
                pool.submit(self.query_timeline, u): u
                for u in user_list[:nb_threads]
            }

            # On récupère les résultats au fur et à mesure
            for future in concurrent.futures.as_completed(tasks):
                duration, ok = future.result()
                times.append(duration)
                if not ok:
                    failed += 1

        average = statistics.mean(times) if times else 0.0
        return average, failed

    def execute_suite(self, total_users: int, configs: List[int], repeats: int = 3):
        """
        Lance tous les tests pour différents niveaux de parallélisme
        et enregistre le tout dans conc.csv.
        """
        print("=== Début des tests ===")

        with open("out/conc.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["PARAM", "AVG_TIME", "RUN", "FAILED"])

            for cfg in configs:
                print(f"\nTest avec {cfg} utilisateurs simultanés")
                for run_idx in range(1, repeats + 1):
                    print(f"  - Essai {run_idx}/{repeats}")

                    avg_ms, nb_failed = self.run_parallel_requests(total_users, cfg)

                    writer.writerow([cfg, f"{avg_ms:.2f}", run_idx, nb_failed])
                    f.flush()

                    print(f"    Temps moyen : {avg_ms:.2f} ms | Erreurs : {nb_failed}")
                    time.sleep(2)

        print("=== Fin des tests ===")

if __name__ == "__main__":
    BASE_URL = "https://projetmassivedata.ey.r.appspot.com"

    tester = TimelineLoadTester(BASE_URL)

    SCENARIOS = [1, 10, 20, 50, 100, 1000]

    tester.execute_suite(
        total_users=1000,
        configs=SCENARIOS,
        repeats=3
    )
