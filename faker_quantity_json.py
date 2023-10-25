import json
from faker import Faker

fake = Faker()

num_records = 75  # Change this to the desired number of records

records = []

for i in range(num_records):
    record = {
        'id': i + 1,
        'quantity': fake.random_int(min=0, max=9999)
    }
    records.append(record)

with open('quantity.json', 'w') as f:
    json.dump(records, f)
