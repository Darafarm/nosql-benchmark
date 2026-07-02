# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 17:19:16 2026

@author: daram
"""

# NoSQL Benchmark: PostgreSQL vs MongoDB vs Redis

A rigorous, reproducible performance benchmark comparing three major database systems on identical workloads at scale. Built as part of an ongoing research project investigating distributed database systems, query optimization, and data engineering infrastructure.

## What This Project Measures

This benchmark answers one engineering question: for the same data and the same workload, how do PostgreSQL, MongoDB, and Redis compare in terms of speed and why?

Four workload types are measured across three database systems:

Insert performance at 10K, 100K, and 1M records.
Single record lookup by ID across 1,000 queries.
Filter queries by field value across 100 queries.
Aggregation queries with GROUP BY across 10 queries.

## Tech Stack

Databases: PostgreSQL 15, MongoDB 6, Redis 7.
Infrastructure: Docker and Docker Compose.
Language: Python 3.13.
Libraries: psycopg2, pymongo, redis-py, faker, matplotlib.
Data: 10,000 to 1,000,000 synthetic e-commerce orders.

## Project Structure

```
nosql-benchmark/
├── docker-compose.yml
├── generate_data.py
├── insert_postgres.py
├── insert_mongo.py
├── insert_redis.py
├── benchmark_read.py
├── benchmark_filter.py
├── benchmark_aggregate.py
├── benchmark_scale.py
├── charts.py
├── chart6_scale.py
└── results/
    ├── results.csv
    ├── chart1_insert_speed.png
    ├── chart2_lookup_speed.png
    ├── chart3_filter_speed.png
    ├── chart4_aggregation_speed.png
    ├── chart5_summary.png
    └── chart6_scale.png
```

## How to Reproduce

Prerequisites: Docker Desktop, Python 3.x, pip.

Clone the repository.
```bash
git clone https://github.com/YOUR_USERNAME/nosql-benchmark.git
cd nosql-benchmark
```

Start all three databases.
```bash
docker-compose up -d
```

Install Python dependencies.
```bash
pip install pymongo psycopg2-binary redis faker matplotlib
```

Generate the data.
```bash
python generate_data.py
```

Run all benchmarks.
```bash
python insert_postgres.py
python insert_mongo.py
python insert_redis.py
python benchmark_read.py
python benchmark_filter.py
python benchmark_aggregate.py
python benchmark_scale.py
```

Generate charts.
```bash
python charts.py
python chart6_scale.py
```

## Benchmark Results

### Insert Performance

| Scale | PostgreSQL | MongoDB | Redis |
|---|---|---|---|
| 10,000 rows | 10.909s | 0.141s | 0.439s |
| 100,000 rows | 91.447s | 1.068s | 4.394s |
| 1,000,000 rows | 991.822s | 17.288s | 48.516s |

### Single Record Lookup (1,000 queries)

| Database | Total Time | Avg Per Query |
|---|---|---|
| PostgreSQL | 1.088s | 1.088ms |
| MongoDB | 0.969s | 0.969ms |
| Redis | 0.501s | 0.501ms |

### Filter Query (100 queries by product)

| Database | Total Time | Avg Per Query |
|---|---|---|
| PostgreSQL | 0.48s | 4.8ms |
| MongoDB | 0.848s | 8.48ms |
| Redis | not suitable | not suitable |

### Aggregation Query (10 GROUP BY queries)

| Database | Total Time | Avg Per Query |
|---|---|---|
| PostgreSQL | 0.116s | 11.6ms |
| MongoDB | 0.32s | 32.0ms |
| Redis | not applicable | not applicable |

## Key Findings

MongoDB dominates insert performance. At 1 million records, MongoDB inserted data in 17 seconds compared to PostgreSQL's 991 seconds. This is because MongoDB uses batch inserts with no schema validation, no write-ahead log overhead, and no constraint checking. PostgreSQL enforces ACID guarantees on every single row, which costs time but buys reliability and data integrity.

Redis wins single record lookups. At 0.501ms per query, Redis is the fastest for key-based retrieval because it stores everything in memory with no disk access required. PostgreSQL and MongoDB are competitive at roughly 1ms per query because both use B-tree indexes that efficiently locate records without scanning the entire dataset.

PostgreSQL wins filter and aggregation queries. With proper indexing, PostgreSQL retrieves filtered results in 4.8ms compared to MongoDB's 8.48ms. For aggregation, PostgreSQL completes GROUP BY queries in 11.6ms compared to MongoDB's 32ms. PostgreSQL's mature query optimizer and decades of refinement for analytical workloads give it a decisive advantage for complex query types.

Redis is unsuitable for filter and aggregation workloads. Redis has no native filter or aggregation mechanism. Simulating a filter query requires scanning every key individually, which produced times exceeding 7,000ms per query at 10,000 records. This is not a limitation of Redis's speed but of its fundamental architecture. Redis was designed exclusively for key-based access, not field-based filtering or grouping.

## When to Use Each Database

Use PostgreSQL when your application needs complex queries involving joins, aggregations, and strict data integrity. PostgreSQL is the right choice when correctness matters more than raw speed and when your data has well-defined relationships and structure.

Use MongoDB when your data is flexible or document-shaped, when you need to insert large volumes of data quickly, and when your queries are primarily document retrievals rather than complex analytical joins. MongoDB is the right choice when schema flexibility and write speed are the primary priorities.

Use Redis when your application needs sub-millisecond retrieval of individual records by a known key. Redis is the right choice for caching, session storage, leaderboards, and any workload where you always know the key and need the value returned instantly.

## What This Benchmark Proves

The results confirm that no single database is universally best. Each database wins decisively in exactly the domain it was designed for. The most important engineering insight is not knowing which database is fastest in absolute terms but knowing which database is right for a specific access pattern. Choosing the wrong database does not make you slightly slower. As the Redis filter result demonstrates, it can make you more than 1,500 times slower.

## Author

Daramola James Oluseyi
PhD Student, Electrical and Computer Engineering
Marquette University, Milwaukee, WI