#!/bin/bash

echo "Expérience 1: Reset du Datastore…"

# Reset via script Python
python3 ../wipe_datastore.py

echo "Expérience 1: Seeding (1000 users, 50 posts/user, 20 followees)…"

python3 ../../massive-gcp-master/seed.py \
    --users 1000 \
    --posts 50000 \
    --follows-min 20 \
    --follows-max 20 \
    --prefix user

echo "Expérience 1: Dataset prêt"
