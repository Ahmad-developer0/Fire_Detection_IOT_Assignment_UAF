import sqlite3

def create_table():
    conn = sqlite3.connect("fire_data.db")
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time TEXT,
            gas INTEGER,
            temperature INTEGER,
            flame TEXT,
            status TEXT
        )
    ''')

    conn.commit()
    conn.close()

def insert_data(time, gas, temperature, flame, status):
    conn = sqlite3.connect("fire_data.db")
    c = conn.cursor()

    c.execute('''
        INSERT INTO sensor_data
        (time, gas, temperature, flame, status)
        VALUES (?, ?, ?, ?, ?)
    ''', (time, gas, temperature, flame, status))

    conn.commit()
    conn.close()