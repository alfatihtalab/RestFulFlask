import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

# iq = "INSERT INTO users VALUES(Null , ? , ?)"
# user1 = ("alfatih", "pass")
# cursor.execute(iq, user1)
# connection.commit()

q = "SELECT * FROM users"
users = cursor.execute(q)


for row in users:
    print(row)
