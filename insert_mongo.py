# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 00:50:21 2026

@author: daram
"""

import pymongo
import json
import time

# 1. Load orders
with open("orders.json", "r") as f:
    orders = json.load(f)

# 2. Connect to MongoDB
client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
db = client["benchmark"]
collection = db["orders"]

# 3. Clear any existing data
collection.drop()
print("Collection cleared.")

# 4. Insert and measure
start = time.time()
collection.insert_many(orders)
end = time.time()

# 5. Report
duration = round(end - start, 3)
print(f"Inserted 10,000 orders into MongoDB in {duration} seconds.")

# 6. Verify
count = collection.count_documents({})
print(f"Verified: {count} records in MongoDB.")

client.close()