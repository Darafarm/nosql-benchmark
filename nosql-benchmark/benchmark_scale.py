import psycopg2
import pymongo
import redis
import json
import time

# Connection functions
def get_postgres():
    return psycopg2.connect(
        host="127.0.0.1",
        port=5434,
        dbname="benchmark",
        user="admin",
        password="password"
    )

def get_mongo():
    client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
    return client, client["benchmark"]["orders_scale"]

def get_redis():
    return redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)

# Scale sizes to test
SCALES = [10000, 100000, 1000000]

# Store results for summary table
results = []

# Chunk size for Redis pipeline to avoid socket timeout
CHUNK_SIZE = 5000

print("=" * 60)
print("SCALE BENCHMARK — INSERT PERFORMANCE")
print("=" * 60)

for n in SCALES:
    # Load the pre-generated orders file for this scale
    print(f"\nLoading {n:,} orders from file...")
    with open(f"orders_{n}.json", "r") as f:
        orders = json.load(f)
    print(f"Loaded. Running inserts...\n")

    # PostgreSQL — create fresh table then insert row by row
    conn = get_postgres()
    cursor = conn.cursor()
    cursor.execute("""
        DROP TABLE IF EXISTS orders_scale;
        CREATE TABLE orders_scale (
            order_id      INTEGER PRIMARY KEY,
            customer_name VARCHAR(100),
            customer_email VARCHAR(100),
            product       VARCHAR(50),
            quantity      INTEGER,
            price         NUMERIC(10,2),
            city          VARCHAR(100),
            country       VARCHAR(100),
            order_date    DATE
        );
    """)
    conn.commit()

    start = time.time()
    for order in orders:
        cursor.execute("""
            INSERT INTO orders_scale (
                order_id, customer_name, customer_email,
                product, quantity, price,
                city, country, order_date
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            order["order_id"], order["customer_name"],
            order["customer_email"], order["product"],
            order["quantity"], order["price"],
            order["city"], order["country"], order["order_date"]
        ))
    conn.commit()
    pg_time = round(time.time() - start, 3)
    cursor.close()
    conn.close()
    print(f"PostgreSQL  {n:>9,} rows : {pg_time}s")

    # MongoDB — drop existing collection then batch insert all at once
    client, collection = get_mongo()
    collection.drop()

    start = time.time()
    collection.insert_many(orders)
    mongo_time = round(time.time() - start, 3)
    client.close()
    print(f"MongoDB     {n:>9,} rows : {mongo_time}s")

    # Redis — flush database then insert using chunked pipeline to avoid timeout
    r = get_redis()
    r.flushdb()

    start = time.time()
    for i in range(0, len(orders), CHUNK_SIZE):
        chunk = orders[i:i + CHUNK_SIZE]
        pipe = r.pipeline()
        for order in chunk:
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
    redis_time = round(time.time() - start, 3)
    r.close()
    print(f"Redis       {n:>9,} rows : {redis_time}s")

    # Store this scale's results for the summary table
    results.append({
        "scale": n,
        "postgresql": pg_time,
        "mongodb": mongo_time,
        "redis": redis_time
    })

# Print final summary table
print("\n" + "=" * 60)
print("SCALE BENCHMARK SUMMARY")
print("=" * 60)
print(f"{'Scale':<12} {'PostgreSQL':>12} {'MongoDB':>12} {'Redis':>12}")
print("-" * 50)
for r in results:
    print(f"{r['scale']:<12,} {r['postgresql']:>11}s {r['mongodb']:>11}s {r['redis']:>11}s")