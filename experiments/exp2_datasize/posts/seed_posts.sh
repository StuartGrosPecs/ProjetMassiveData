#!/bin/bash

# Vérifier qu'un paramètre est fourni
if [ -z "$1" ]; then
    echo "Erreur : il faut fournir le nombre de posts par utilisateur."
    echo "Usage : ./seed_posts.sh <posts_per_user>"
    exit 1
fi

POSTS_PER_USER=$1

# 21 users au minimum car "Fixer le nombre de followers à 20"
USERS=30
TOTAL_POSTS=$((POSTS_PER_USER * USERS))

echo "Reset Datastore..."
python3 ../../wipe_datastore.py

echo "Seed (Exp 2A - $POSTS_PER_USER posts/user → $TOTAL_POSTS posts totaux)"

python3 ../../../massive-gcp-master/seed.py \
    --users $USERS \
    --posts $TOTAL_POSTS \
    --follows-min 20 \
    --follows-max 20 \
    --prefix bench

echo "Dataset généré."
