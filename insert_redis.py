# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 00:51:51 2026

@author: daram
"""
import redis
import json
import time

# 1. Load orders
with open("orders.json", "r") as f:
    orders = json.load(f)

# 2. Connect to Redis
client = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)

# 3. Clear existing data
client.flushdb()
print("Redis cleared.")

# 4. Insert and measure
start = time.time()

pipe = client.pipeline()
for order in orders:
    key = f"order:{order['order_id']}"
    pipe.hset(key, mapping={
        "order_id":       order["order_id"],
        "customer_name":  order["customer_name"],
        "customer_email": order["customer_email"],
        "product":        order["product"],
        "quantity":       order["quantity"],
        "price":          order["price"],
        "city":           order["city"],
        "country":        order["country"],
        "order_date":     order["order_date"]
    })
pipe.execute()

end = time.time()

# 5. Report
duration = round(end - start, 3)
print(f"Inserted 10,000 orders into Redis in {duration} seconds.")

# 6. Verify
count = client.dbsize()
print(f"Verified: {count} records in Redis.")

client.close()