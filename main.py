import sqlite3

from init import statments

conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

for statement in statments:
    cursor.execute(statement)


