import sqlite3
#to work with SQLAlchemy, we need to run this file in the separate 'code' folder.

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

# MUST BE INTEGER
# This is the only place where int vs INTEGER matters—in auto-incrementing columns
create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS equities (id INTEGER PRIMARY KEY, name text, price real)"
cursor.execute(create_table)

connection.commit()

connection.close()

#when we run this, we will create the data.db file.