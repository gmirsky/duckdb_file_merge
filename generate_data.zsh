#!/bin/zsh
emulate -LR zsh # reset zsh options
export PATH=/bin/zsh:$PATH

# Generate data
python3 faker_products_csv.py
python3 faker_products_json.py
python3 faker_products_parquet.py

python3 faker_quantity_csv.py
python3 faker_quantity_json.py
python3 faker_quantity_parquet.py