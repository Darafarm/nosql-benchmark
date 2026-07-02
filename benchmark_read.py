# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 12:04:29 2026

@author: daram
"""

import psycopg2
import pymongo
import redis
import json
import time
import random

random.seed(42)

#  Connection setup 
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
NUM_LOOKUPS = 1000
order_ids = random.sample(range(1, 10001), NUM_LOOKUPS)

print(f"Running {NUM_LOOKUPS} random single-record lookups on each database...\n")

#  PostgreSQL single lookup 
start = time.time()
for order_id in order_ids:
    pg_cursor.execute("SELECT * FROM orders WHERE order_id = %s", (order_id,))
    pg_cursor.fetchone()
end = time.time()
pg_time = round(end - start, 3)
print(f"PostgreSQL : {pg_time}s for {NUM_LOOKUPS} lookups")
print(f"     avg per lookup: {round(pg_time/NUM_LOOKUPS*1000, 3)}ms")

#  MongoDB single lookup 
start = time.time()
for order_id in order_ids:
    mongo_collection.find_one({"order_id": order_id})
end = time.time()
mongo_time = round(end - start, 3)
print(f"\nMongoDB    : {mongo_time}s for {NUM_LOOKUPS} lookups")
print(f"            avg per lookup: {round(mongo_time/NUM_LOOKUPS*1000, 3)}ms")

# Redis single lookup 
start = time.time()
for order_id in order_ids:
    redis_client.hgetall(f"order:{order_id}")
end = time.time()
redis_time = round(end - start, 3)
print(f"\nRedis      : {redis_time}s for {NUM_LOOKUPS} lookups")
print(f"            avg per lookup: {round(redis_time/NUM_LOOKUPS*1000, 3)}ms")

# Summary 
print("\n" + "="*50)
print("SINGLE RECORD LOOKUP SUMMARY")
print("="*50)
print(f"PostgreSQL : {pg_time}s total | {round(pg_time/NUM_LOOKUPS*1000, 3)}ms per lookup")
print(f"MongoDB    : {mongo_time}s total | {round(mongo_time/NUM_LOOKUPS*1000, 3)}ms per lookup")
print(f"Redis      : {redis_time}s total | {round(redis_time/NUM_LOOKUPS*1000, 3)}ms per lookup")

# Cleanup 
pg_cursor.close()
pg_conn.close()
mongo_client.close()
redis_client.close()