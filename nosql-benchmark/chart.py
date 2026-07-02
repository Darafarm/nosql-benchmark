import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import os

#Create results folder 
os.makedirs("results", exist_ok=True)

# Color scheme 
COLORS = {
    "PostgreSQL": "#336791",   # PostgreSQL blue
    "MongoDB":    "#4DB33D",   # MongoDB green
    "Redis":      "#DC382D"    # Redis red
}

#  Chart 1: Insert Speed 
fig, ax = plt.subplots(figsize=(9, 5))

databases = ["PostgreSQL", "MongoDB", "Redis"]
insert_times = [8.086, 0.189, 0.384]
bars = ax.bar(databases, insert_times,
              color=[COLORS[db] for db in databases],
              width=0.5, edgecolor="white", linewidth=1.2)

for bar, val in zip(bars, insert_times):
    ax.text(bar.get_x() + bar.get_width()/2,
            bar.get_height() + 0.1,
            f"{val}s", ha="center", va="bottom",
            fontweight="bold", fontsize=11)

ax.set_title("Insert Performance — 10,000 Records", fontsize=14, fontweight="bold", pad=15)
ax.set_ylabel("Time (seconds)", fontsize=12)
ax.set_ylim(0, max(insert_times) * 1.2)
ax.spines[["top", "right"]].set_visible(False)
ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig("results/chart1_insert_speed.png", dpi=150, bbox_inches="tight")
plt.show()
print("Chart 1 saved.")

#  Chart 2: Single Lookup Speed 
fig, ax = plt.subplots(figsize=(9, 5))

lookup_times = [1.088, 0.969, 0.501]
bars = ax.bar(databases, lookup_times,
              color=[COLORS[db] for db in databases],
              width=0.5, edgecolor="white", linewidth=1.2)

for bar, val in zip(bars, lookup_times):
    ax.text(bar.get_x() + bar.get_width()/2,
            bar.get_height() + 0.01,
            f"{val}ms", ha="center", va="bottom",
            fontweight="bold", fontsize=11)

ax.set_title("Single Record Lookup — 1,000 Queries by ID", fontsize=14, fontweight="bold", pad=15)
ax.set_ylabel("Avg Time per Query (ms)", fontsize=12)
ax.set_ylim(0, max(lookup_times) * 1.3)
ax.spines[["top", "right"]].set_visible(False)
ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig("results/chart2_lookup_speed.png", dpi=150, bbox_inches="tight")
plt.show()
print("Chart 2 saved.")

#  Chart 3: Filter Query Speed 
fig, ax = plt.subplots(figsize=(9, 5))

filter_times = [4.8, 8.48, 271.67]
bars = ax.bar(databases, filter_times,
              color=[COLORS[db] for db in databases],
              width=0.5, edgecolor="white", linewidth=1.2)

for bar, val in zip(bars, filter_times):
    label = f"{val}ms" if val < 100 else f"{val}ms\n(sampled)"
    ax.text(bar.get_x() + bar.get_width()/2,
            bar.get_height() + 2,
            label, ha="center", va="bottom",
            fontweight="bold", fontsize=11)

ax.set_title("Filter Query Performance — 100 Queries by Product", fontsize=14, fontweight="bold", pad=15)
ax.set_ylabel("Avg Time per Query (ms)", fontsize=12)
ax.set_ylim(0, max(filter_times) * 1.15)
ax.spines[["top", "right"]].set_visible(False)
ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig("results/chart3_filter_speed.png", dpi=150, bbox_inches="tight")
plt.show()
print("Chart 3 saved.")

#  Chart 4: Aggregation Speed 
fig, ax = plt.subplots(figsize=(9, 5))

agg_databases = ["PostgreSQL", "MongoDB"]
agg_times = [11.6, 32.0]
bars = ax.bar(agg_databases, agg_times,
              color=[COLORS[db] for db in agg_databases],
              width=0.4, edgecolor="white", linewidth=1.2)

for bar, val in zip(bars, agg_times):
    ax.text(bar.get_x() + bar.get_width()/2,
            bar.get_height() + 0.3,
            f"{val}ms", ha="center", va="bottom",
            fontweight="bold", fontsize=11)

ax.set_title("Aggregation Query Performance — GROUP BY Product (10 Runs)", fontsize=14, fontweight="bold", pad=15)
ax.set_ylabel("Avg Time per Query (ms)", fontsize=12)
ax.set_ylim(0, max(agg_times) * 1.3)
ax.text(0.98, 0.95, "Redis excluded — no native aggregation",
        transform=ax.transAxes, ha="right", va="top",
        fontsize=9, color="gray", style="italic")
ax.spines[["top", "right"]].set_visible(False)
ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig("results/chart4_aggregation_speed.png", dpi=150, bbox_inches="tight")
plt.show()
print("Chart 4 saved.")

# Chart 5: Summary Heatmap 
fig, ax = plt.subplots(figsize=(10, 4))

categories = ["Insert\n(10K records)", "Lookup\n(per query ms)", "Filter\n(per query ms)", "Aggregation\n(per query ms)"]
pg_scores =    [8.086,  1.088,   4.8,   11.6]
mongo_scores = [0.189,  0.969,   8.48,  32.0]
redis_scores = [0.384,  0.501,   271.67, None]

x = np.arange(len(categories))
width = 0.25

bars_pg    = ax.bar(x - width, pg_scores,    width, label="PostgreSQL", color=COLORS["PostgreSQL"], edgecolor="white")
bars_mongo = ax.bar(x,         mongo_scores, width, label="MongoDB",    color=COLORS["MongoDB"],    edgecolor="white")

redis_display = [r if r is not None else 0 for r in redis_scores]
bars_redis = ax.bar(x + width, redis_display, width, label="Redis", color=COLORS["Redis"], edgecolor="white")

ax.text(3 + width, 0.5, "N/A", ha="center", va="bottom", fontsize=9, color="gray")

ax.set_title("Complete Benchmark Summary — PostgreSQL vs MongoDB vs Redis", fontsize=13, fontweight="bold", pad=15)
ax.set_ylabel("Time (seconds or ms — see axis)", fontsize=10)
ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=10)
ax.legend(fontsize=10)
ax.spines[["top", "right"]].set_visible(False)
ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig("results/chart5_summary.png", dpi=150, bbox_inches="tight")
plt.show()
print("Chart 5 saved.")

print("\nAll 5 charts saved to results/ folder.")