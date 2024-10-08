import sqlite3


def new_note(caption:str, content:str, connection:sqlite3.Connection):
    with connection:
        connection.execute(f"INSERT INTO notes (caption, content) VALUES (?, ?)", 
                           (caption, content))
        return connection.execute("SELECT last_insert_rowid()")
    

def delete_note(id:int, connection:sqlite3.Connection):
    with connection:
        connection.execute(f"DELETE FROM notes WHERE id == ?", (id,))


def update_note(id:int, caption:str, content:str, connection:sqlite3.Connection):
    with connection:
        connection.execute(f"UPDATE notes SET caption = ?, content = ? WHERE id == ?", 
                           (caption, content, id) )


def get_notes_simple(connection:sqlite3.Connection):
    with connection:
        results = connection.execute("SELECT id, caption FROM notes ORDER BY id ASC")
        return results.fetchall()


def get_note_by_id(id:int, connection:sqlite3.Connection):
    with connection:
        results = connection.execute(f"SELECT id, caption, content FROM notes WHERE id == ?", (id,))
        return results.fetchone()


def exists_id(id:int, connection:sqlite3.Connection):
    with connection:
        return connection.execute(f"SELECT count(id) FROM notes WHERE id == ?", (id,)).fetchone()[0] == 1


def set_up_db(db_name = "db.db") -> sqlite3.Connection:
    connection = sqlite3.connect(db_name)
    connection.execute("PRAGMA foreign_keys = 1")
    with connection:
        cur = connection.execute("SELECT name FROM sqlite_master")
        all_tables = cur.fetchall()
        if ("notes",) not in all_tables:
            cur.execute("CREATE TABLE notes(id INTEGER PRIMARY KEY, caption, content)")
        if ("tags",) not in all_tables:
            cur.execute("CREATE TABLE tags (id INTEGER PRIMARY KEY, name)")
        if ("note_tags",) not in all_tables:
            cur.execute("""CREATE TABLE note_tags (note_id INTEGER REFERENCES notes(id), tag_id REFERENCES tags(id))""")
        return connection