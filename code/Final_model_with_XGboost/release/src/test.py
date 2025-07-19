import sqlite3
conn = sqlite3.connect('financial_data.db')
cursor = conn.cursor()
cursor.execute("SELECT time, price FROM financial_data LIMIT 5")
print(cursor.fetchall())
conn.close()