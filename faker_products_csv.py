import csv
from faker import Faker
from faker_food import FoodProvider

fake = Faker()
fake.add_provider(FoodProvider)

RECORD_COUNT = 75

# Create a CSV file and write the header row
with open('products.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['id', 'product', 'price'])

    # Generate fake data and write to the CSV file
    for i in range(RECORD_COUNT):
        writer.writerow([i+1, fake.ingredient(), abs(round(fake.pydecimal(left_digits=1, right_digits=2), 2))])
