# Got Database? Nope!

This repository features a sample python script using an in-memory DuckDB database and SQL to read in two files, merge, sort and filter the data using one SQL statement. 

The demonstration walks through the various parts of the final SQL statement to show how each file is read and then the final SQL statement incorporates all of the statements into one master statement to perform the desired functionality.

## Run the demonstration

### Generate the data to use in the demonstration.

Create the data files using the bash or z-shell script or by executing python on each script that begins with "faker_"

Run the demonstration for the CSV files

```bash
python3 merge_files.py --main-input products.csv --secondary-input quantity.csv --output merged_data.csv
```

Run the demonstration for JSON

```bash
python3 merge_files.py --main-input products.json --secondary-input quantity.json --output merged_data.json
```

Run the demonstration for the parquet files.

```bash
python3 merge_files.py --main-input products.parquet --secondary-input quantity.parquet --output merged-data.parquet
```

