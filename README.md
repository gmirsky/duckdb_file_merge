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

## Sample output

```bash
python3 merge_files.py --main-input products.parquet --secondary-input quantity.parquet --output merged-data.parquet

args
Namespace(input1='products.parquet', input2='quantity.parquet', output='merged-data.parquet')


Selecting file 1 from parquet

    id              product  price
0    1  Vegetable spaghetti   9.69
1    2           Wattleseed   4.66
2    3        Vanilla Beans   3.62
3    4         Sesame Seeds   7.65
4    5    Hot smoked salmon   8.67
..  ..                  ...    ...
70  71         Asian Greens   5.81
71  72            Mahi mahi   9.17
72  73         Sweet Potato   5.00
73  74   White wine vinegar   8.64
74  75          CarobCarrot   0.17

[75 rows x 3 columns]


Selecting file 2 from parquet

    id  quantity
0    0      8020
1    1      5012
2    2      8772
3    3      8011
4    4      3087
..  ..       ...
70  70      7899
71  71      5420
72  72      6450
73  73      7146
74  74      9082

[75 rows x 2 columns]


Joining the two files, filtering out anything
        that starts with 'J' and calculating total price

               product  id  price  quantity  total_price
0                 Agar  53   8.73      1567     13679.91
1             Allspice  40   6.58      2227     14653.66
2         Asian Greens  71   5.81      5420     31490.20
3            Asparagus  12   0.83      2152      1786.16
4        Baking Powder  14   5.21       932      4855.72
..                 ...  ..    ...       ...          ...
69          Wattleseed   2   4.66      8772     40877.52
70  White wine vinegar  74   8.64      9082     78468.48
71        William Pear  52   5.35      7660     40981.00
72        Yellow Papaw  18   5.96      3193     19030.28
73             Yoghurt  20   1.14      6451      7354.14

[74 rows x 5 columns]


Writing the result of the query to a parquet file named merged-data.parquet and providing a count of the rows after filtering out anything that started with 'J'

   Count
0     74

Done
```

