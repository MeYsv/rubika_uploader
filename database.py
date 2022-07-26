import sqlite3

def load_db():
    connect = sqlite3.connect("database.db")
    cursor = connect.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS data(size INTEGER)")
    connect.commit()
    connect.close()

def select_data():
    connect = sqlite3.connect("database.db")
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM data")
    result = cursor.fetchone()
    connect.close()
    return result

def add_data(size):
    connect = sqlite3.connect("database.db")
    cursor = connect.cursor()
    cursor.execute("INSERT OR IGNORE INTO data VALUES(:size)", {"size":size})
    connect.commit()
    connect.close()

def update_data(size):
    connect = sqlite3.connect("database.db")
    cursor = connect.cursor()
    cursor.execute("UPDATE data SET size=?", (size,))
    connect.commit()
    connect.close()