import sqlite3
import os
from PIL import Image
import io

DB_PATH = 'event_data.db'

def create_db():
    """Kreiraj SQLite bazu i tablice za evente i trenutni event_id."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Kreiraj tablicu za evente
    c.execute('''
        CREATE TABLE IF NOT EXISTS events (
            event_id TEXT PRIMARY KEY,
            print_image BLOB,
            session BLOB
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

# Funkcija za spremanje postavki
def set_setting(key, value):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
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
    c.execute('SELECT value FROM settings WHERE key = ?', (key,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else default

def get_event_ids():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT event_id FROM events')  # Provjeri tablicu 'events', a ne pozivaj samu funkciju
    ids = [row[0] for row in c.fetchall()]
    conn.close()
    return ids


def add_event(event_id, print_image=None, session=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM events WHERE event_id = ?', (event_id,))
    if c.fetchone():
        conn.close()
        return False

    c.execute('''
        INSERT INTO events (event_id, print_image, session) 
        VALUES (?, ?, ?)
    ''', (event_id, print_image, session))
    conn.commit()
    conn.close()
    return True

def delete_event(event_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM events WHERE event_id = ?', (event_id,))
    conn.commit()
    conn.close()

def get_event_data(event_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM events WHERE event_id = ?', (event_id,))
    event_data = c.fetchone()
    conn.close()
    if event_data:
        return {
            'event_id': event_data[0],
            'print_image': event_data[1],
            'session': event_data[2]
        }
    return None

def save_image_to_db(event_id, image_path, image_type='print_image'):
    if not os.path.exists(image_path):
        return False

    with open(image_path, "rb") as f:
        image_data = f.read()

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    if image_type == 'print_image':
        c.execute('''
            UPDATE events SET print_image = ? WHERE event_id = ?
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
