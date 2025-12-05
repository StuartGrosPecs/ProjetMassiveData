#!/usr/bin/env bash
# Seed TinyInsta pour l'expérience "post" (taille des données)
# Utilisation :
#   ./seed_post_level.sh 10
#   ./seed_post_level.sh 100
#   ./seed_post_level.sh 1000

set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <posts_per_user>"
  echo "Exemple: $0 10   # ≈ 10 posts par utilisateur"
  exit 1
fi

POSTS_PER_USER="$1"


# CONFIG
APP_DIR="$HOME/ProjetMassiveData/massive-gcp-master"
SEED_SCRIPT="${APP_DIR}/seed.py"

USERS=1000          
FOLLOWS_MIN=20      
FOLLOWS_MAX=20      
PREFIX="user"

TOTAL_POSTS=$((USERS * POSTS_PER_USER))

echo "Seed expérience POST"
echo "   USERS        = ${USERS}"
echo "   FOLLOWS_MIN  = ${FOLLOWS_MIN}"
echo "   FOLLOWS_MAX  = ${FOLLOWS_MAX}"
echo "   PREFIX       = ${PREFIX}"
echo "   POSTS/USER   = ${POSTS_PER_USER}"
echo "   TOTAL_POSTS  ≈ ${TOTAL_POSTS}"
echo

cd "${APP_DIR}"

python3 "${SEED_SCRIPT}" \
  --users "${USERS}" \
  --posts "${TOTAL_POSTS}" \
  --follows-min "${FOLLOWS_MIN}" \
  --follows-max "${FOLLOWS_MAX}" \
  --prefix "${PREFIX}"

echo
echo "Seed terminé pour ~${POSTS_PER_USER} posts par utilisateur."