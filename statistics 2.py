# statistics.py

import json
import os

STATS_FILE = "statistics.json"

def read_stats():
    if not os.path.exists(STATS_FILE):
        return {"conversations": 0, "sales": 0}

    with open(STATS_FILE, "r") as file:
        return json.load(file)

def write_stats(stats):
    with open(STATS_FILE, "w") as file:
        json.dump(stats, file)

def increment_stat(stat_key):
    stats = read_stats()
    stats[stat_key] += 1
    write_stats(stats)

def increment_conversations():
    increment_stat("conversations")

def increment_sales():
    increment_stat("sales")

def get_statistics():
    return read_stats()
