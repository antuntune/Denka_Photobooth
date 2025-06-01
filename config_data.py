import sqlite3
import os
from PIL import Image
import io

DB_PATH = 'event_data.db'

def create_db():
    """Kreiraj SQLite bazu i tablice za evente i trenutni event_id."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Kreiraj tablicu za evente sa svim potrebnim kolonama
    c.execute('''
        CREATE TABLE IF NOT EXISTS events (
            event_id TEXT PRIMARY KEY,
            template_image BLOB,
            print_seq_image BLOB,
            album_location TEXT,
            max_print_per_seq INTEGER,
            seq_images BLOB,
            test_album BOOLEAN,
            brightness INTEGER,
            mouse_visibility BOOLEAN,
            photo_cnt INTEGER,
            print_cnt INTEGER,
            other_settings TEXT
        )
    ''')

    # Kreiraj tablicu za trenutni event_id
    c.execute('''
        CREATE TABLE IF NOT EXISTS current_event (
            event_id TEXT
        )
    ''')

    # Kreiraj tablicu za globalne postavke
    c.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')

    conn.commit()
    conn.close()

# Pozivamo ovu funkciju kako bi inicijalizirali bazu kada pokrenemo aplikaciju
create_db()



# Pohranjujemo postavke za event_id u tablicu events
def set_setting(key, value):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Ako je value boolean, pretvori u integer (True = 1, False = 0)
    if isinstance(value, bool):
        value = 1 if value else 0

    # Dohvati trenutni event_id iz current_event
    current_event_id = get_current_event_id()

    if current_event_id:
        # Ako imamo current_event_id, pohranjujemo podatak specifičan za event_id u tablicu events
        #print(f"Ažuriram postavku {key} za event_id: {current_event_id}")
        c.execute(f'''
            UPDATE events
            SET {key} = ?
            WHERE event_id = ?
        ''', (value, current_event_id))
    else:
        # Ako nema trenutnog event_id, pohranjujemo globalnu postavku u settings tablicu
        #print(f"Ažuriram globalnu postavku {key} u tablicu settings")
        c.execute('''
            INSERT OR REPLACE INTO settings (key, value)
            VALUES (?, ?)
        ''', (key, value))

    conn.commit()
    conn.close()

# Funkcija za dohvat postavki
def get_setting(key, default=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Dohvati trenutni event_id iz current_event
    current_event_id = get_current_event_id()

    if current_event_id:
        # Ako imamo trenutni event_id, dohvatimo postavku specifičnu za taj event_id iz tablice events
        #print(f"Dohvaćam {key} za event_id: {current_event_id}")  # Logiranje za provjeru
        c.execute(f'SELECT {key} FROM events WHERE event_id = ?', (current_event_id,))
        result = c.fetchone()
        
        if result is not None:
            #print(f"Podatak za {key} za event_id {current_event_id}: {result[0]}")  # Logiranje za provjeru
            return result[0]
        else:
            print(f"{key} nije pronađen za event_id {current_event_id}")
            
    else:
        #print(f"Nema trenutnog event_id, dohvaćam globalnu postavku {key} iz tablice settings")  # Logiranje
        c.execute('SELECT value FROM settings WHERE key = ?', (key,))
        result = c.fetchone()
    
    conn.close()

    if result:
        # Ako je rezultat 1, vraćamo True, ako je 0, vraćamo False
        return bool(result[0]) if isinstance(result[0], int) else result[0]  # Ovdje vraćamo True/False ako je 1/0, ili vraćamo originalnu vrijednost
    print(f"{key} nije pronađen ni u tablici events ni u settings.")
    return default




def get_event_ids():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT event_id FROM events')
    ids = [row[0] for row in c.fetchall()]
    conn.close()
    return ids


def add_event(event_id, print_seq_image=None, album_location=None, template_image=None, max_print_per_seq=2, seq_images=None, test_album=False, brightness=100, mouse_visibility=False, photo_cnt=0, print_cnt=0, other_settings=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Provjeravamo da li event_id već postoji u bazi
    c.execute('SELECT * FROM events WHERE event_id = ?', (event_id,))
    if c.fetchone():
        conn.close()
        return False  # Ako već postoji, ne dodajemo ga ponovo
    # Ako event_id ne postoji, dodajemo ga u tablicu
    c.execute('''
        INSERT INTO events (event_id, print_seq_image, album_location, template_image, max_print_per_seq, seq_images, test_album, brightness, mouse_visibility,photo_cnt, print_cnt, other_settings) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (event_id, print_seq_image,album_location, template_image, max_print_per_seq, seq_images, test_album, brightness, mouse_visibility,photo_cnt, print_cnt, other_settings))
    conn.commit()
    conn.close()
    return True  # Ako je uspješno dodano, vraćamo True




def delete_event(event_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM events WHERE event_id = ?', (event_id,))
    conn.commit()
    conn.close()

def get_event_data():
    event_id = get_current_event_id()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM events WHERE event_id = ?', (event_id,))
    event_data = c.fetchone()
    conn.close()
    if event_data:
        return {
            'event_id': event_data[0],  # event_id je prvi stupac (index 0)
            'template_image': event_data[1],  # template_image je drugi stupac (index 1)
            'print_seq_image': event_data[2],  # print_seq_image je treći stupac (index 2)
            'album_location': event_data[3],  # album_location je četvrti stupac (index 3)
            'max_print_per_seq': event_data[4],  # max_print_per_seq je peti stupac (index 4)
            'seq_images': event_data[5],  # seq_images je šesti stupac (index 5)
            'test_album': event_data[6],  # test_album je sedmi stupac (index 6)
            'brightness': event_data[7],  # brightness je osmi stupac (index 7)
            'mouse_visibility': event_data[8],  # mouse_visibility je deveti stupac (index 8)
            'photo_cnt': event_data[9],  # photo_cnt je deseti stupac (index 9)
            'print_cnt': event_data[10],  # print_cnt je jedanaesti stupac (index 10)
            'other_settings': event_data[11]  # other_settings je dvanaesti stupac (index 11)
        }
    return None

def save_image_to_db(image_path, image_type='template_image'):
    event_id = get_current_event_id()
    if not os.path.exists(image_path):
        return False

    with open(image_path, "rb") as f:
        image_data = f.read()

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    if image_type == 'template_image':
        c.execute('''
            UPDATE events SET template_image = ? WHERE event_id = ?
        ''', (image_data, event_id))
    else:
        c.execute('''
            UPDATE events SET session = ? WHERE event_id = ?
        ''', (image_data, event_id))

    conn.commit()
    conn.close()
    return True

def set_current_event_id(event_id):
    """Spremi trenutni event ID u tablicu current_event."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Provjeri postoji li već zapis u tablici current_event
    c.execute('SELECT * FROM current_event')
    if c.fetchone():
        # Ako zapis postoji, ažuriraj ga
        c.execute('''
            UPDATE current_event
            SET event_id = ?
            WHERE rowid = 1  -- Osiguraj da je to prvi zapis
        ''', (event_id,))
    else:
        # Ako zapis ne postoji, dodaj novi
        c.execute('''
            INSERT INTO current_event (event_id)
            VALUES (?)
        ''', (event_id,))

    conn.commit()
    conn.close()
    print(f"Trenutni event ID postavljen na {event_id}.")

def get_current_event_id():
    """Vrati trenutni event ID iz baze podataka."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT event_id FROM current_event LIMIT 1')  # Dohvati samo prvi zapis
    event_id = c.fetchone()
    conn.close()

    if event_id:
        return event_id[0]
    return None
