import requests
import time
import csv
import concurrent.futures
import statistics
from typing import List, Tuple

class TinyInstaBenchmark:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
    
    def make_timeline_request(self, user_id: int) -> Tuple[float, bool]:
        """Faire une requête timeline et retourner le temps de réponse et le statut"""
        start_time = time.time()
        try:
            response = requests.get(
                f"{self.base_url}/api/timeline",
                params={"user": f"bench{user_id}"},  # Note: format du seed.py
                timeout=60
            )
            success = response.status_code == 200
            if not success:
                print(f"Erreur: Status code {response.status_code} pour user bench{user_id}")
            return (time.time() - start_time) * 1000, success
        except Exception as e:
            print(f"Exception pour user bench{user_id}: {e}")
            return (time.time() - start_time) * 1000, False
    
    def run_concurrent_benchmark(self, num_users: int, num_concurrent: int) -> Tuple[float, int]:
        """Exécuter le benchmark avec un nombre d'utilisateurs simultanés"""
        print(f"Lancement du benchmark avec {num_concurrent} utilisateurs simultanés...")
        
        # Les utilisateurs générés par seed.py sont bench1, bench2, ..., bench1000
        user_ids = list(range(1, min(num_users, 1000) + 1))
        
        times = []
        failed_requests = 0
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_concurrent) as executor:
            # Soumettre les tâches
            future_to_user = {
                executor.submit(self.make_timeline_request, user_id): user_id 
                for user_id in user_ids[:num_concurrent]
            }
            
            # Collecter les résultats
            for future in concurrent.futures.as_completed(future_to_user):
                response_time, success = future.result()
                times.append(response_time)
                if not success:
                    failed_requests += 1
        
        avg_time = statistics.mean(times) if times else 0
        return avg_time, failed_requests
    
    def run_benchmark_suite(self, num_users: int, concurrent_configs: List[int], num_runs: int = 3):
        """Exécuter la suite de tests de concurrence"""
        print("=== DÉBUT DU BENCHMARK DE CONCURRENCE ===")
        
        with open('out/conc.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['PARAM', 'AVG_TIME', 'RUN', 'FAILED'])
            
            for concurrent_users in concurrent_configs:
                print(f"\n--- Configuration: {concurrent_users} utilisateurs simultanés ---")
                
                for run in range(1, num_runs + 1):
                    print(f"Run {run}/{num_runs}...")
                    
                    avg_time, failed = self.run_concurrent_benchmark(num_users, concurrent_users)
                    
                    writer.writerow([concurrent_users, f"{avg_time:.2f}ms", run, failed])
                    csvfile.flush()
                    
                    print(f"Résultat: {avg_time:.2f}ms, Échecs: {failed}")
                    
                    # Pause entre les runs
                    time.sleep(2)
        
        print("=== BENCHMARK DE CONCURRENCE TERMINÉ ===")

if __name__ == "__main__":
    BASE_URL = "https://projetmassivedata.ey.r.appspot.com"
    
    benchmark = TinyInstaBenchmark(BASE_URL)
    
    CONCURRENT_CONFIGS = [1, 10, 20, 50, 100, 1000]
    
    benchmark.run_benchmark_suite(
        num_users=1000,
        concurrent_configs=CONCURRENT_CONFIGS,
        num_runs=3
    )