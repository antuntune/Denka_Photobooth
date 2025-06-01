import os
import shutil

# Putanja do glavnog foldera
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def remove_file(path):
    if os.path.isfile(path):
        print(f"🗑️  Brišem: {path}")
        os.remove(path)

def clean_project():
    for root, dirs, files in os.walk(BASE_DIR):
        for file in files:
            if file.endswith(".pyc") or file.endswith(".db-journal"):
                remove_file(os.path.join(root, file))
        for dir_name in dirs:
            if dir_name == "__pycache__":
                full_path = os.path.join(root, dir_name)
                print(f"🗑️  Brišem folder: {full_path}")
                shutil.rmtree(full_path, ignore_errors=True)

    # Ovdje brišemo photobooth.db ako postoji
    db_path = os.path.join(BASE_DIR, "event_data.db")
    remove_file(db_path)

    print("✅ Sustav očišćen.")

if __name__ == "__main__":
    clean_project()
