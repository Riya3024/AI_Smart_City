import random

zones = ["Gate", "Library", "Cafeteria", "Hostel"]

def simulate_zones(extra_students):
    data = {}
    for zone in zones:
        base = random.randint(20, 60)
        data[zone] = base + (extra_students * random.uniform(0.05, 0.15))
    return data