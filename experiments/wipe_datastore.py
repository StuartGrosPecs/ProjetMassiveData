from google.cloud import datastore
import time

client = datastore.Client()

BATCH_SIZE = 300     # Taille sûre pour éviter contention
MAX_RETRY = 5

def delete_kind(kind):
    print(f"Deleting all entities of kind: {kind}")

    query = client.query(kind=kind)
    entities = list(query.fetch())
    total = len(entities)
    print(f"Found {total} entities.")

    i = 0
    while i < total:
        batch = entities[i:i+BATCH_SIZE]
        keys = [e.key for e in batch]

        # tentative de suppression
        for retry in range(MAX_RETRY):
            try:
                client.delete_multi(keys)
                break
            except Exception as e:
                print(f"⚠ Contention on batch {i}-{i+len(batch)} (retry {retry+1}/{MAX_RETRY})")
                time.sleep(1)

        i += BATCH_SIZE

    print(f"Kind {kind} fully deleted.\n")


if __name__ == "__main__":
    delete_kind("Post")
    delete_kind("User")
    print("Datastore wipe completed!")
