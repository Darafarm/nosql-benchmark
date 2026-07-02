# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 21:56:08 2026

@author: daram
"""

import psycopg2
import pymongo
import time

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

NUM_RUNS = 10

print(f"Running aggregation queries ({NUM_RUNS} runs)...\n")
print("Query: total revenue and order count grouped by product\n")

#  PostgreSQL aggregation 
start = time.time()
for _ in range(NUM_RUNS):
    pg_cursor.execute("""
        SELECT product,
               COUNT(*) as total_orders,
               SUM(price) as total_revenue,
               AVG(price) as avg_price
        FROM orders
        GROUP BY product
        ORDER BY total_revenue DESC
    """)
    pg_cursor.fetchall()
end = time.time()
pg_time = round(end - start, 3)
print(f"PostgreSQL : {pg_time}s for {NUM_RUNS} aggregation queries")
print(f"            avg per query: {round(pg_time/NUM_RUNS*1000, 3)}ms")

#  MongoDB aggregation 
start = time.time()
for _ in range(NUM_RUNS):
    list(mongo_collection.aggregate([
        {
            "$group": {
                "_id": "$product",
                "total_orders": {"$sum": 1},
                "total_revenue": {"$sum": "$price"},
                "avg_price": {"$avg": "$price"}
            }
        },
        {
            "$sort": {"total_revenue": -1}
        }
    ]))
end = time.time()
mongo_time = round(end - start, 3)
print(f"\nMongoDB    : {mongo_time}s for {NUM_RUNS} aggregation queries")
print(f"            avg per query: {round(mongo_time/NUM_RUNS*1000, 3)}ms")

#  Summary 
print("\n" + "="*50)
print("AGGREGATION QUERY SUMMARY")
print("="*50)
print(f"PostgreSQL : {pg_time}s | {round(pg_time/NUM_RUNS*1000, 3)}ms per query")
print(f"MongoDB    : {mongo_time}s | {round(mongo_time/NUM_RUNS*1000, 3)}ms per query")
print(f"\nNote: Redis excluded - no native aggregation/grouping capability")

#  Cleanup 
pg_cursor.close()
pg_conn.close()
mongo_client.close()