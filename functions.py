import sqlite3

def check(session):
    id = session.get("user_id")

    if id:
        return True
    
    else:
        return False
    
def get_db():
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    return connection, cursor