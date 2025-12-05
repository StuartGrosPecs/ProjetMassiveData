#!/usr/bin/env python3
import argparse
import random
from google.cloud import datastore


def parse_args():
    p = argparse.ArgumentParser(
        description="Augmente le fanout (taille du champ 'follows') pour les users TinyInsta."
    )
    p.add_argument(
        "--target-fanout",
        type=int,
        required=True,
        help="Nombre de followees désiré par utilisateur (ex: 50 ou 100).",
    )
    p.add_argument(
        "--prefix",
        type=str,
        default="user",
        help="Préfixe des IDs utilisateur (default: 'user', donc user1, user2, ...).",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Affiche ce qui serait fait sans écrire dans Datastore.",
    )
    return p.parse_args()


def load_users(client: datastore.Client, prefix: str):
    """
    Charge tous les users dont la key.name commence par prefix.
    (ex: user1, user2, ...)
    """
    query = client.query(kind="User")
    users = []

    for entity in query.fetch():
        key_name = entity.key.name
        if key_name and key_name.startswith(prefix):
            users.append(key_name)

    users.sort()
    print(f"[INFO] {len(users)} utilisateurs chargés (prefix={prefix}).")
    return users


def load_user_entities_map(client: datastore.Client, user_ids):
    """
    Charge les entités User complètes sous forme de dict: id -> entity
    """
    entities_map = {}
    keys = [client.key("User", uid) for uid in user_ids]
    entities = client.get_multi(keys)

    for ent in entities:
        if ent is not None:
            entities_map[ent.key.name] = ent

    print(f"[INFO] {len(entities_map)} entités User chargées.")
    return entities_map


def adjust_fanout(
    client: datastore.Client,
    user_ids,
    entities_map,
    target_fanout: int,
    dry_run: bool,
):
    """
    Pour chaque user, ajoute des followees aléatoires jusqu'à atteindre target_fanout.
    """
    all_users_set = set(user_ids)
    updated_count = 0
    total_new_edges = 0

    for uid in user_ids:
        ent = entities_map.get(uid)
        if ent is None:
            continue

        existing = set(ent.get("follows", []))
        current_deg = len(existing)

        if current_deg >= target_fanout:
            # Rien à faire pour ce user
            continue

        missing = target_fanout - current_deg

        # Candidats possibles = tous les users sauf soi-même et ceux déjà suivis
        candidates = list(all_users_set - {uid} - existing)
        if not candidates:
            continue

        if len(candidates) <= missing:
            chosen = candidates
        else:
            chosen = random.sample(candidates, missing)

        new_follows = sorted(existing.union(chosen))
        ent["follows"] = new_follows

        updated_count += 1
        total_new_edges += len(chosen)

        print(
            f"[DEBUG] {uid}: {current_deg} -> {len(new_follows)} followees "
            f"(ajout de {len(chosen)})"
        )

        if not dry_run:
            client.put(ent)

    print(
        f"[INFO] Utilisateurs mis à jour: {updated_count}, "
        f"nouvelles relations de follow: {total_new_edges}"
    )


def main():
    args = parse_args()
    client = datastore.Client()

    print(
        f"[INFO] Augmentation du fanout jusqu'à {args.target_fanout} "
        f"(prefix={args.prefix}, dry_run={args.dry_run})"
    )

    user_ids = load_users(client, args.prefix)
    entities_map = load_user_entities_map(client, user_ids)

    adjust_fanout(
        client,
        user_ids,
        entities_map,
        target_fanout=args.target_fanout,
        dry_run=args.dry_run,
    )

    print("[INFO] Terminé.")


if __name__ == "__main__":
    main()
