# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 17:13:39 2026

@author: daram
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import os

os.makedirs("results", exist_ok=True)

# Scale benchmark data
scales = [10_000, 100_000, 1_000_000]
pg_times    = [10.909,  91.447,  991.822]
mongo_times = [0.141,   1.068,   17.288]
redis_times = [0.439,   4.394,   48.516]

COLORS = {
    "PostgreSQL": "#336791",
    "MongoDB":    "#4DB33D",
    "Redis":      "#DC382D"
}

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Left chart — linear scale (shows the dramatic PostgreSQL gap)
ax1.plot(scales, pg_times,    marker="o", linewidth=2.5,
         color=COLORS["PostgreSQL"], label="PostgreSQL")
ax1.plot(scales, mongo_times, marker="s", linewidth=2.5,
         color=COLORS["MongoDB"],    label="MongoDB")
ax1.plot(scales, redis_times, marker="^", linewidth=2.5,
         color=COLORS["Redis"],      label="Redis")

for x, y in zip(scales, pg_times):
    ax1.annotate(f"{y}s", (x, y), textcoords="offset points",
                xytext=(0, 10), ha="center", fontsize=9, color=COLORS["PostgreSQL"])
for x, y in zip(scales, mongo_times):
    ax1.annotate(f"{y}s", (x, y), textcoords="offset points",
                xytext=(0, 10), ha="center", fontsize=9, color=COLORS["MongoDB"])
for x, y in zip(scales, redis_times):
    ax1.annotate(f"{y}s", (x, y), textcoords="offset points",
                xytext=(0, -15), ha="center", fontsize=9, color=COLORS["Redis"])

ax1.set_title("Insert Time vs Scale (Linear)", fontsize=13, fontweight="bold")
ax1.set_xlabel("Number of Records", fontsize=11)
ax1.set_ylabel("Insert Time (seconds)", fontsize=11)
ax1.set_xscale("linear")
ax1.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
ax1.legend(fontsize=10)
ax1.spines[["top", "right"]].set_visible(False)
ax1.grid(alpha=0.3)

# Right chart — log scale (shows scaling behavior more clearly)
ax2.plot(scales, pg_times,    marker="o", linewidth=2.5,
         color=COLORS["PostgreSQL"], label="PostgreSQL")
ax2.plot(scales, mongo_times, marker="s", linewidth=2.5,
         color=COLORS["MongoDB"],    label="MongoDB")
ax2.plot(scales, redis_times, marker="^", linewidth=2.5,
         color=COLORS["Redis"],      label="Redis")

ax2.set_title("Insert Time vs Scale (Log Scale)", fontsize=13, fontweight="bold")
ax2.set_xlabel("Number of Records", fontsize=11)
ax2.set_ylabel("Insert Time (seconds, log scale)", fontsize=11)
ax2.set_xscale("log")
ax2.set_yscale("log")
ax2.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
ax2.legend(fontsize=10)
ax2.spines[["top", "right"]].set_visible(False)
ax2.grid(alpha=0.3, which="both")

fig.suptitle("PostgreSQL vs MongoDB vs Redis — Insert Performance at Scale",
             fontsize=14, fontweight="bold", y=1.02)

plt.tight_layout()
plt.savefig("results/chart6_scale.png", dpi=150, bbox_inches="tight")
plt.show()
print("Chart 6 saved to results/chart6_scale.png")