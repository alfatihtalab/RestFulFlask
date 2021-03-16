import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

table_user = "CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username text, password text)"

table_items = "CREATE TABLE IF NOT EXISTS items(name text, price real)"

cursor.execute(table_items)
cursor.execute(table_user)

cursor.execute("INSERT INTO items VALUES('test', 22.6)")

connection.commit()
connection.close()