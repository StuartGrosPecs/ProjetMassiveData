#!/usr/bin/env bash

set -euo pipefail

# CONFIG

USERS=1000
POSTS=$((100 * USERS)) 
CONCURRENCY=50 
PREFIX="user"

# PATHS DES SCRIPTS
SEED_SCRIPT="../../massive-gcp-master/seed.py"
WIPE_SCRIPT="../wipe_datastore.py"
INCREASE_SCRIPT="./increase_fanout.py"
BENCH_SCRIPT="./bench_fanout.py"

echo "==========================="
echo "  EXPÉRIENCE FANOUT"
echo "==========================="

# 1) FANOUT = 10

echo
echo ">>> RESET DATASTORE"
python3 "$WIPE_SCRIPT"

echo
echo ">>> SEED initial : 1000 users, 100 posts/user, 10 followees"
python3 "$SEED_SCRIPT" \
    --users "$USERS" \
    --posts "$POSTS" \
    --follows-min 10 \
    --follows-max 10 \
    --prefix "$PREFIX"

echo
echo ">>> BENCHMARK FANOUT = 10"
python3 "$BENCH_SCRIPT" --param 10

# 2) FANOUT = 50

echo
echo ">>> AUGMENTATION FANOUT -> 50"
python3 "$INCREASE_SCRIPT" --target-fanout 50 --prefix "$PREFIX"

echo
echo ">>> BENCHMARK FANOUT = 50"
python3 "$BENCH_SCRIPT" --param 50

# 3) FANOUT = 100

echo
echo ">>> AUGMENTATION FANOUT -> 100"
python3 "$INCREASE_SCRIPT" --target-fanout 100 --prefix "$PREFIX"

echo
echo ">>> BENCHMARK FANOUT = 100"
python3 "$BENCH_SCRIPT" --param 100

echo
echo "======================================"
echo " EXPÉRIENCE FANOUT TERMINÉE ✔"
echo " Résultats dans out/fanout.csv"
echo "======================================"
