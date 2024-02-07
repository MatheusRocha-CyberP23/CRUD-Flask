import sqlite3, random
from models import User

Users = [
    {
        'full_name': "Arlindo Cruz",
        'cpf': '12345678999',
        'email': 'teste@gmail.com',
        'balance': 100
    },
]  

def get_new_id():
    return random.getrandbits(28)

def connect():
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, full_name TEXT NOT NULL, cpf TEXT UNIQUE NOT NULL, email TEXT UNIQUE NOT NULL, balance REAL NOT NULL)")
    conn.commit()
    conn.close()
    for i in Users:
        user = User(get_new_id(), i['full_name'], i['cpf'], i['email'], i['balance'])
        insert(user)

def insert(user):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO users VALUES (?,?,?,?,?)", (
        user.id,
        user.full_name,
        user.cpf,
        user.email,
        user.balance
    ))
    conn.commit()
    conn.close()

def get_user_by_id(user_id):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id=?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return User(row[0], row[1], row[2], row[3], row[4]).serialize() if row else None

def get_user_by_email(email):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email=?", (email,))
    row = cur.fetchone()
    conn.close()
    return User(row[0], row[1], row[2], row[3], row[4]).serialize() if row else None

def get_user_by_cpf(cpf):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE cpf=?", (cpf,))
    row = cur.fetchone()
    conn.close()
    return User(row[0], row[1], row[2], row[3], row[4]).serialize() if row else None

def update_balance(user_id, balance):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("UPDATE users SET balance=? WHERE id=?", (balance, user_id))
    conn.commit()
    conn.close()

def view():
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    users = []
    for i in rows:
        user = User(i[0], i[1], i[2], i[3], i[4])
        users.append(user)
    conn.close()
    return users

def update(user):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("UPDATE users SET full_name=?, cpf=?, email=?, balance=? WHERE id=?", (user.full_name, user.cpf, user.email, user.balance, user.id,))
    conn.commit()
    conn.close()

def delete(user_id):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    conn.close()