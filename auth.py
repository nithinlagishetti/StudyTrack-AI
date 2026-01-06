import sqlite3

def register_user(username, password):
    conn = sqlite3.connect("users.db", check_same_thread=False)
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users VALUES (?,?)", (username, password))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def login_user(username, password):
    conn = sqlite3.connect("users.db", check_same_thread=False)
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )
    user = cur.fetchone()
    conn.close()
    return user
