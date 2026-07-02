# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 13:18:11 2026

@author: daram
"""

import psycopg2
import pymongo
import redis
import json
import time

# Connection setup 
pg_conn = psycopg2.connect(
    host="127.0.0.1",
    port=5434,
    dbname="benchmark",
    user="admin",
    password="password"
)
pg_cursor = pg_conn.cursor()

mongo_client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
mongo_collection = mongo_client["benchmark"]["orders"]

redis_client = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)

# Test parameters 
PRODUCTS = [
    "Laptop", "Phone", "Tablet", "Monitor", "Keyboard",
    "Mouse", "Headphones", "Webcam", "SSD", "USB Hub"
]
NUM_RUNS = 10

print(f"Running filter queries ({NUM_RUNS} runs each product)...\n")

# PostgreSQL filter 
start = time.time()
for _ in range(NUM_RUNS):
    for product in PRODUCTS:
        pg_cursor.execute(
            "SELECT * FROM orders WHERE product = %s",
            (product,)
        )
        pg_cursor.fetchall()
end = time.time()
pg_time = round(end - start, 3)
total_queries = NUM_RUNS * len(PRODUCTS)
print(f"PostgreSQL : {pg_time}s for {total_queries} filter queries")
print(f"            avg per query: {round(pg_time/total_queries*1000, 3)}ms")

# MongoDB filter 
start = time.time()
for _ in range(NUM_RUNS):
    for product in PRODUCTS:
        list(mongo_collection.find({"product": product}))
end = time.time()
mongo_time = round(end - start, 3)
print(f"\nMongoDB    : {mongo_time}s for {total_queries} filter queries")
print(f"            avg per query: {round(mongo_time/total_queries*1000, 3)}ms")

# Redis filter 
# Redis has no native filter; simulate by scanning all keys
#  Redis filter 
REDIS_SAMPLE = 500
keys_sample = redis_client.keys("order:*")[:REDIS_SAMPLE]

start = time.time()
for _ in range(NUM_RUNS):
    for product in PRODUCTS:
        matched = []
        for key in keys_sample:
            order_product = redis_client.hget(key, "product")
            if order_product == product:
                matched.append(redis_client.hgetall(key))
end = time.time()
redis_time = round(end - start, 3)
print(f"\nRedis      : {redis_time}s for {total_queries} filter queries (sampled {REDIS_SAMPLE} keys)")
print(f"            avg per query: {round(redis_time/total_queries*1000, 3)}ms")

# Summary 
print("\n" + "="*50)
print("FILTER QUERY SUMMARY")
print("="*50)
print(f"PostgreSQL : {pg_time}s total | {round(pg_time/total_queries*1000, 3)}ms per query")
print(f"MongoDB    : {mongo_time}s total | {round(mongo_time/total_queries*1000, 3)}ms per query")
print(f"Redis      : {redis_time}s total | {round(redis_time/total_queries*1000, 3)}ms per query")

# Cleanup 
pg_cursor.close()
pg_conn.close()
mongo_client.close()
redis_client.close()