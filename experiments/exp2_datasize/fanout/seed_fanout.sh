#!/bin/bash

# Vérifier qu'un paramètre est fourni (nombre de followees)
if [ -z "$1" ]; then
    echo "Erreur : vous devez fournir le nombre de followees par utilisateur."
    echo "Usage : ./seed_fanout.sh <followees_per_user>"
    exit 1
fi

FANOUT=$1

USERS=101

POSTS_PER_USER=100
TOTAL_POSTS=$((POSTS_PER_USER * USERS))

echo "Reset Datastore..."
python3 ../../wipe_datastore.py

echo "Seed Exp 2B :"
echo "  - $USERS utilisateurs"
echo "  - $POSTS_PER_USER posts/user → $TOTAL_POSTS posts totaux"
echo "  - $FANOUT followees/user"

python3 ../../../massive-gcp-master/seed.py \
    --users $USERS \
    --posts $TOTAL_POSTS \
    --follows-min $FANOUT \
    --follows-max $FANOUT \
    --prefix bench

echo "Dataset Exp 2B généré."
