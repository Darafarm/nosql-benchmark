# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 14:24:12 2026

@author: daram
"""

import json
import random
from faker import Faker

fake = Faker()

PRODUCTS = [
    "Laptop", "Phone", "Tablet", "Monitor", "Keyboard",
    "Mouse", "Headphones", "Webcam", "SSD", "USB Hub"
]

def generate_orders(n, seed=42):
    random.seed(seed)
    Faker.seed(seed)
    orders = []
    for i in range(1, n + 1):
        order = {
            "order_id": i,
            "customer_name": fake.name(),
            "customer_email": fake.email(),
            "product": random.choice(PRODUCTS),
            "quantity": random.randint(1, 10),
            "price": round(random.uniform(10.0, 1500.0), 2),
            "city": fake.city(),
            "country": fake.country(),
            "order_date": fake.date_between(
                start_date="-2y", end_date="today"
            ).strftime("%Y-%m-%d")
        }
        orders.append(order)
    return orders

if __name__ == "__main__":
    for n in [10000, 100000, 1000000]:
        print(f"Generating {n:,} orders...")
        orders = generate_orders(n)
        filename = f"orders_{n}.json"
        with open(filename, "w") as f:
            json.dump(orders, f)
        print(f"Saved to {filename}")
    print("Done.")