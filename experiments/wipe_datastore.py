from google.cloud import datastore

client = datastore.Client()

def delete_kind(kind):
    print(f"Deleting all entities of kind: {kind}")
    query = client.query(kind=kind)
    keys = [e.key for e in query.fetch()]
    if keys:
        print(f"Deleting {len(keys)} entities...")
        client.delete_multi(keys)
    else:
        print("No entities found.")

delete_kind("User")
delete_kind("Post")

print("DONE.")
