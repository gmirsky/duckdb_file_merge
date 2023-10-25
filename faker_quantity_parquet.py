import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from faker import Faker

fake = Faker()

RECORD_COUNT = 75

# Generate fake data
data = {
    'id': list(range(RECORD_COUNT)),
    'quantity': [fake.random_int(min=0, max=9999) for _ in range(RECORD_COUNT)],
}

# Convert to pandas dataframe
df = pd.DataFrame(data)

# Convert to pyarrow table
table = pa.Table.from_pandas(df)

# Write to parquet file
pq.write_table(table, 'quantity.parquet')
