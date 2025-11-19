#!/bin/bash

# ==========================================
#  Benchmark Concurrency – Apache Bench (ab)
#  Génère : out/conc.csv
#  Usage : ./bench_concurrency.sh
# ==========================================

URL="https://projetmassivedata.appspot.com/api/timeline?user=user1&limit=20"
OUT_DIR="out"
OUT_FILE="$OUT_DIR/conc.csv"

# Concurrence à tester
CONC_LIST=(1 10 20 50 100 1000)

# Nombre total de requêtes à envoyer pour chaque test
N=200   # ab exige N >= C

mkdir -p "$OUT_DIR"

echo "PARAM,AVG_TIME,RUN,FAILED" > "$OUT_FILE"

echo "Début du benchmark de concurrence..."
echo "URL testée: $URL"
echo

for C in "${CONC_LIST[@]}"; do
    echo "=== Concurrency $C ==="
    for RUN in 1 2 3; do
        echo "Run $RUN..."

        # Lancement du benchmark
        RESULT=$(ab -n $N -c $C "$URL" 2>&1)

        # Extraction du temps moyen (Time per request)
        AVG_TIME=$(echo "$RESULT" | grep "Time per request:" | head -n1 | awk '{print $4}')

        # Extraction errors
        FAILED=$(echo "$RESULT" | grep "Failed requests" | awk '{print $3}')

        # Ajout ligne CSV
        echo "$C,$AVG_TIME,$RUN,$FAILED" >> "$OUT_FILE"

        echo "  -> Avg: $AVG_TIME ms | Failed: $FAILED"
    done
done

echo
echo "Benchmark terminé !"
echo "Résultat disponible dans : $OUT_FILE"
