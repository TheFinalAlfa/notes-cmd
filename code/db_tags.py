import sqlite3

def exists_tag(id:int, connection:sqlite3.Connection):
    with connection:
        return connection.execute(f"SELECT count(id) FROM tags WHERE id == ?", (id,)).fetchone()[0] == 1

def new_tag(name:str, connection:sqlite3.Connection):
    with connection:
        connection.execute(f"INSERT INTO notes (name) VALUES (?)", 
                           (name,))
        return connection.execute("SELECT last_insert_rowid()")

def delete_tag(id:int, connection:sqlite3.Connection):
    with connection:
        connection.execute(f"DELETE FROM tags WHERE id == ?", (id,))

def update_tag(name:str, id:int, connection:sqlite3.Connection):
    with connection:
        connection.execute(f"UPDATE tags SET name = ? WHERE id == ?", 
                           (name, id) )

def get_tag_simple(connection:sqlite3.Connection):
    with connection:
        results = connection.execute("SELECT id, name FROM tags ORDER BY id ASC")
        return results.fetchall()

def get_tag(connection:sqlite3.Connection):
    with connection:
        pass

def add_notes_tag(connection:sqlite3.Connection):
    with connection:
        pass

def remove_notes_tag(connection:sqlite3.Connection):
    with connection:
        pass