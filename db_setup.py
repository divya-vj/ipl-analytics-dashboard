import pandas as pd
import sqlite3


matches = pd.read_csv("data/matches.csv")
deliveries = pd.read_csv("data/deliveries.csv")

print("=== MATCHES TABLE ===")
print(f"Shape: {matches.shape}") # (rows, columns)
print(f"Columns: {list(matches.columns)}")
print(matches.dtypes) # data type of each column
print(matches.head(3)) # first 3 rows
print(matches.isnull().sum()) 

print("\n=== DELIVERIES TABLE ===")
print(f"Shape: {deliveries.shape}")
print(f"Columns: {list(deliveries.columns)}")
print(deliveries.dtypes)
print(deliveries.head(3))

conn = sqlite3.connect("database/ipl.db")

matches.to_sql("matches", conn, if_exists="replace", index=False)
deliveries.to_sql("deliveries", conn, if_exists="replace", index=False)

cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM matches")
print(f"Matches loaded: {cursor.fetchone()[0]}") 
cursor.execute("SELECT COUNT(*) FROM deliveries")
print(f"Deliveries loaded: {cursor.fetchone()[0]}") 

cursor.execute("PRAGMA table_info(matches)")
print("\nMatches table columns:")
for row in cursor.fetchall():

    print(f" {row[1]} ({row[2]})") # column name and type

conn.close()
print("\nDatabase built successfully!")