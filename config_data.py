import shelve
import os
from PIL import Image
import io


DB_PATH = 'event_data_db'  # shelve dodaje ekstenzije automatski

# --- Funkcije za rad s event ID-evima ---
def get_event_ids():
    with shelve.open(DB_PATH) as db:
        return db.get("event_ids", [])

def set_event_ids(ids):
    with shelve.open(DB_PATH) as db:
        db["event_ids"] = ids

def add_event_id(event_id):
    ids = get_event_ids()
    if event_id not in ids:
        ids.append(event_id)
        set_event_ids(ids)
        return True
    return False

def remove_event_id(event_id):
    ids = get_event_ids()
    if event_id in ids:
        ids.remove(event_id)
        set_event_ids(ids)
        return True
    return False

def move_event_id_to_top(event_id):
    ids = get_event_ids()
    if event_id in ids:
        ids.remove(event_id)
        ids.insert(0, event_id)
        set_event_ids(ids)
        return True
    return False

def get_first_event_id():
    ids = get_event_ids()
    return ids[0] if ids else None

def clear_event_ids():
    with shelve.open(DB_PATH) as db:
        if "event_ids" in db:
            del db["event_ids"]

def clear_all():
    for suffix in ['', '.db', '.dat', '.bak', '.dir']:
        try:
            os.remove(DB_PATH + suffix)
        except FileNotFoundError:
            pass

def print_event_ids():
    print("📋 Event ID-evi:", get_event_ids() or "(prazno)")

def print_entire_database():
    with shelve.open(DB_PATH) as db:
        if not db:
            print("📂 Baza je prazna.")
            return
        print("📦 Sadržaj baze:")
        for key, value in db.items():
            print(f"🔑 {key} → {value}")

def get_first_event_id():
    ids = get_event_ids()
    return ids[0]

def set_value(key, value):
    with shelve.open(DB_PATH) as db:
        db[key] = value

def get_value(key, default=None):
    with shelve.open(DB_PATH) as db:
        return db.get(key, default)


def save_image_to_db(key, image_path):
    """Spremi sliku u shelve kao bajtove pod zadanim ključem."""
    if not os.path.exists(image_path):
        print(f"❌ Ne postoji slika: {image_path}")
        return False

    with open(image_path, "rb") as f:
        image_bytes = f.read()

    with shelve.open(DB_PATH) as db:
        db[key] = image_bytes
        print(f"🖼️ Slika '{image_path}' spremljena pod ključem '{key}'.")
        return True

def load_image_from_db(key):
    """Učitaj sliku iz shelve baze kao PIL.Image objekt."""
    with shelve.open(DB_PATH) as db:
        image_bytes = db.get(key, None)
        if image_bytes is None:
            print(f"⚠️ Nema slike pod ključem '{key}'.")
            return None

    return Image.open(io.BytesIO(image_bytes))

# Spremanje slike
#save_image_to_db("template_image", "/home/denka/template.jpg")

# Učitavanje slike i prikaz
#img = load_image_from_db("template_image")
#if img:
#    img.show()



#set_value("templatePath", "/home/denka/template.jpg")
#print(get_value("templatePath"))
#print(get_value("nonexistent", "nije postavljeno"))



#import event_storage

# Brisanje svih ID-eva
#event_storage.clear_event_ids()

# Dodavanje
#event_storage.add_event_id("test_1")
#event_storage.add_event_id("test_2")
#event_storage.add_event_id("doro")

# Ispis
#event_storage.print_event_ids()

# Pomicanje na vrh
#event_storage.move_event_id_to_top("doro")
#event_storage.print_event_ids()

# Brisanje jednog ID-a
#event_storage.remove_event_id("test_1")
#event_storage.print_event_ids()
