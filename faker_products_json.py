import json
from faker import Faker
from faker_food import FoodProvider

fake = Faker()
fake.add_provider(FoodProvider)

num_products = 75  # specify the number of products to generate

products = []  # create an empty list to store the generated products

for i in range(num_products):
    product = {
        "id": i + 1,
        "product": fake.ingredient(),
        "price": fake.pyfloat(left_digits=1, right_digits=2, positive=True),
    }
    products.append(product)

with open("products.json", "w") as f:
    json.dump(products, f)
