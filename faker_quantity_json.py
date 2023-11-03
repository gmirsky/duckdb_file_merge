"""
Creates a JSON file with a list of dictionaries containing a random number of
items for each dictionary. The number of dictionaries is determined by the
NUMBER_RECORDS variable. The number of items is determined by the quantity
variable.
"""
import json
from faker import Faker

fake = Faker()

NUMBER_RECORDS = 75  # Change this to the desired number of records

records = []

for i in range(NUMBER_RECORDS):
    record = {"id": i + 1, "quantity": fake.random_int(min=0, max=9999)}
    records.append(record)

with open("quantity.json", "w", encoding="utf-8") as f:
    json.dump(records, f)
