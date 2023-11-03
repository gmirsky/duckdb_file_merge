"""
Create a CSV file with a column of quantity values.
"""
import csv
from faker import Faker

fake = Faker()

RECORD_COUNT = 75


def generate_quantity():
    """
    Generate a random integer between 1 and 100.
    """
    return fake.random_int(min=1)


def generate_data(num_rows):
    """
    Generate a list of dictionaries with fake data.
    """
    fake_data = []
    for i in range(num_rows):
        row = {"id": i + 1, "quantity": generate_quantity()}
        fake_data.append(row)
    return fake_data


def write_to_csv(filename, data):
    """
    Write the data to a CSV file.
    """
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["id", "quantity"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


if __name__ == "__main__":
    FILE_NAME = "quantity.csv"
    generated_data = generate_data(RECORD_COUNT)
    write_to_csv(FILE_NAME, generated_data)
