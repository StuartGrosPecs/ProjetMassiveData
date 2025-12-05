#!/usr/bin/env bash

set -euo pipefail


# Taille des données
USERS=1000               
POSTS=$((50 * USERS)) 
FOLLOWS=20

echo "Expérience concurrence : reset du Datastore…"
python3 ../wipe_datastore.py

echo "Expérience concurrence : seeding (${USERS} users, 50 posts/user, 20 followees)…"

python3 ../../massive-gcp-master/seed.py \
    --users "$USERS" \
    --posts "$POSTS" \
    --follows-min "$FOLLOWS" \
    --follows-max "$FOLLOWS" \
    --prefix user

echo "Expérience concurrence : dataset prêt"
