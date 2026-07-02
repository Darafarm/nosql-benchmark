# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 00:02:44 2026

@author: daram
"""

import psycopg2
import json
import time

#  Load the generated orders 
with open("orders.json", "r") as f:
    orders = json.load(f)

#  Connect to PostgreSQL 
conn = psycopg2.connect(
    host="127.0.0.1",
    port=5433,
    dbname="benchmark",
    user="admin",
    password="password"
)
cursor = conn.cursor()

#  Create the orders table 
cursor.execute("""
    DROP TABLE IF EXISTS orders;
    CREATE TABLE orders (
        order_id      INTEGER PRIMARY KEY,
        customer_name VARCHAR(100),
        customer_email VARCHAR(100),
        product       VARCHAR(50),
        quantity      INTEGER,
        price         NUMERIC(10, 2),
        city          VARCHAR(100),
        country       VARCHAR(100),
        order_date    DATE
    );
""")
conn.commit()
print("Table created.")

# Insert all 10,000 orders and measure time 
start = time.time()

for order in orders:
    cursor.execute("""
        INSERT INTO orders (
            order_id, customer_name, customer_email,
            product, quantity, price,
            city, country, order_date
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        order["order_id"],
        order["customer_name"],
        order["customer_email"],
        order["product"],
        order["quantity"],
        order["price"],
        order["city"],
        order["country"],
        order["order_date"]
    ))

conn.commit()
end = time.time()

# Report results 
duration = round(end - start, 3)
print(f"Inserted 10,000 orders into PostgreSQL in {duration} seconds.")

# Quick verification 
cursor.execute("SELECT COUNT(*) FROM orders;")
count = cursor.fetchone()[0]
print(f"Verified: {count} records in PostgreSQL.")

cursor.close()
conn.close()