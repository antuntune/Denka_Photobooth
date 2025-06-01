import os

db_file = "event_data.db"

if os.path.exists(db_file):
    os.remove(db_file)
    print("🧹 event_data.db obrisan.")
else:
    print("✅ Nema baze za brisanje.")
