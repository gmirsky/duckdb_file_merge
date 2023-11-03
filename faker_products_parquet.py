"""
Create a Parquet file with fake data using the Faker library.
"""
from faker import Faker
from faker_food import FoodProvider
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

# Create a Faker instance
fake = Faker()
fake.add_provider(FoodProvider)

RECORD_COUNT = 75

# Generate fake data for the "id", "product", and "price" columns
ids = [i + 1 for i in range(RECORD_COUNT)]
products = [fake.ingredient() for _ in range(RECORD_COUNT)]
prices = [
    fake.pyfloat(left_digits=1, right_digits=2, positive=True)
    for _ in range(RECORD_COUNT)
]

# Create a pandas DataFrame with the fake data
df = pd.DataFrame({"id": ids, "product": products, "price": prices})

# Convert the pandas DataFrame to a PyArrow Tabl
table = pa.Table.from_pandas(df)

# Write the PyArrow Table to a Parquet file
pq.write_table(table, "products.parquet")
