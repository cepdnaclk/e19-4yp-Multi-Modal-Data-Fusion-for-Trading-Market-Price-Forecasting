import sqlite3

# Connect to the database
conn = sqlite3.connect('financial_data.db')
cursor = conn.cursor()

# View table structure
cursor.execute("PRAGMA table_info(financial_data)")
print("Table Structure:")
print(cursor.fetchall())

# View sample data
cursor.execute("SELECT time, price, RSI, Macro_factor FROM financial_data LIMIT 10")
print("\nSample Data:")
for row in cursor.fetchall():
    print(row)

# Close connection
conn.close()