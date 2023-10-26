import csv
from faker import Faker

fake = Faker()

RECORD_COUNT = 75


def generate_quantity():
    return fake.random_int(min=1)


def generate_data(num_rows):
    data = []
    for i in range(num_rows):
        row = {"id": i + 1, "quantity": generate_quantity()}
        data.append(row)
    return data


def write_to_csv(filename, data):
    with open(filename, "w", newline="") as csvfile:
        fieldnames = ["id", "quantity"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


if __name__ == "__main__":
    filename = "quantity.csv"
    data = generate_data(RECORD_COUNT)
    write_to_csv(filename, data)
