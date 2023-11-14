"""
Merge two files using DuckDB.
"""
import argparse
from argparse import ArgumentParser
from dataclasses import dataclass
import os

import duckdb

ACCEPTABLE_TYPES = [
    "csv",
    "parquet",  # not supported yet in this script
    "json",  # not supported yet in this script
]


@dataclass
class File:
    """
    File class.
    """

    name: str
    type: str
    encoding: str
    seperator: str


def parse_args():
    """
    Parse command line arguments.

    :return: args: command line arguments
    """
    parser = ArgumentParser(
        description="Merge two files into one",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog="Example: python merge_files.py -i input.txt -o output.txt",
    )
    # this will be the primary file that will be merged with the secondary file
    parser.add_argument(
        "-m",
        "--main-input",
        dest="input1",
        type=extant_file,
        help="Main input file",
        metavar="extant_file",
        required=True,
    )
    # this will be the secondary file that will be merged with the primary file
    parser.add_argument(
        "-s",
        "--secondary-input",
        dest="input2",
        type=extant_file,
        help="Secondary input file",
        metavar="extant_file",
        required=True,
    )
    # this will be the output file that will be created
    parser.add_argument(
        "-o",
        "--output",
        dest="output",
        type=str,
        help="Output file",
        metavar="FILE",
        required=True,
    )
    # this will be the version of the script
    parser.add_argument("-V", "--version", action="version", version="%(prog)s 1.0")
    return parser.parse_args()


def extant_file(x):
    """
    'Type' for argparse - checks that file exists but does not open.

    :param x: file name
    :return: file name if exists

    """
    if not os.path.exists(x):
        # Argparse uses the ArgumentTypeError to give a rejection message like:
        # error: argument input: x does not exist
        raise argparse.ArgumentTypeError(f"{x} does not exist")  # pylint: disable=C0209, W1310
    return x


def merge_files(file1: File, file2: File, output):
    """
    Merge two files into one using DuckDB and then write to the result to a CSV file.
    """
    # create a DuckDB database in memory
    conn = duckdb.connect(":memory:") # pylint: disable=I1101

    print()
    if file1.type == "csv":
        # select file1 from CSV
        sql1 = (
            f"SELECT * FROM read_csv('{file1.name}', delim='{file1.seperator}',"
            " header=true, columns={'id':'INTEGER', 'product':'VARCHAR', 'price':'DECIMAL(9,2)'} )"
        )
        execute_and_print_output_of_the_duckdb_command(
            conn, sql1, "Selecting file 1 from csv"
        )
    elif file1.type == "json":
        # select file1 from JSON
        sql1 = f"SELECT * FROM '{file1.name}' "
        execute_and_print_output_of_the_duckdb_command(
            conn, sql1, "Selecting file 1 from JSON"
        )
    elif file1.type == "parquet":
        # select file1 from Parquet
        sql1 = f"SELECT * FROM '{file1.name}' "
        execute_and_print_output_of_the_duckdb_command(
            conn, sql1, "Selecting file 1 from parquet"
        )
    else:
        raise ValueError(
            f"File type {file1.type} not supported. Must be one of {ACCEPTABLE_TYPES}"
        )

    if file2.type == "csv":
        # select file2 from CSV
        sql2 = (
            f"SELECT * FROM read_csv('{file2.name}', delim='{file1.seperator}',"
            " header=true, columns={'id':'INTEGER', 'quantity':'INTEGER'} )"
        )
        execute_and_print_output_of_the_duckdb_command(
            conn, sql2, "Selecting file 2 from csv"
        )
    elif file2.type == "json":
        # select file2 from JSON
        sql2 = f"SELECT * FROM '{file2.name}' "
        execute_and_print_output_of_the_duckdb_command(
            conn, sql2, "Selecting file 2 from JSON"
        )
    elif file2.type == "parquet":
        # select file2 from Parquet
        sql2 = f"SELECT * FROM '{file2.name}' "
        execute_and_print_output_of_the_duckdb_command(
            conn, sql2, "Selecting file 2 from parquet"
        )
    else:
        raise ValueError(
            f"File type {file2.type} not supported. Must be one of {ACCEPTABLE_TYPES}"
        )

    # join the two CSV files from CSV and calculate total price
    sql3 = (
        "SELECT table1.product, table1.id, table1.price, table2.quantity, "
        " (table1.price * table2.quantity) as 'total_price' "
        f" FROM ({sql1}) table1 join ({sql2}) table2 on (table1.id = table2.id) "
        "WHERE table1.product not like 'J%' "
        "ORDER BY table1.product"
    )
    execute_and_print_output_of_the_duckdb_command(
        conn,
        sql3,
        (
            "Joining the two files, filtering out anything"
            " that starts with 'J' and calculating total price"
        ),
    )
    # export the result of the query to a CSV file
    if file1.type == "csv":
        # export the result of the query to a CSV file
        sql4 = f"COPY ({sql3}) to '{output}' WITH (HEADER 1, DELIMITER '{file1.seperator}')"
    elif file1.type == "json":
        sql4 = f"COPY ({sql3}) to '{output}' (FORMAT JSON, ARRAY true)"
    elif file1.type == "parquet":
        sql4 = f"COPY ({sql3}) to '{output}' (FORMAT PARQUET, COMPRESSION ZSTD)"
    else:
        raise ValueError(
            f"File type {file1.type} not supported. Must be one of {ACCEPTABLE_TYPES}"
        )

    execute_and_print_output_of_the_duckdb_command(
        conn,
        sql4,
        (
            f"Writing the result of the query to a {file1.type} file"
            f" named {output} and providing a count of the rows"
            " after filtering out anything that started with 'J'"
        ),
    )
    # close the connection to duckdb
    conn.close()


def execute_and_print_output_of_the_duckdb_command(conn, arg1, arg2):
    """
    Execute and print the output of the DuckDB command.
    """
    
    print()
    print(arg2)
    print()
    print(conn.execute(f"{arg1};").fetchdf())
    print()


def main():
    """
    Main function for script.
    """

    ENCODING = "utf-8"

    args = parse_args()
    print("args")
    print(args)

    # extract the file types from the file names
    file1_type = args.input1.split(".")[-1]
    file2_type = args.input2.split(".")[-1]

    # check if the file types are supported
    if file1_type not in ACCEPTABLE_TYPES:
        raise ValueError(
            f"Main file type {file1_type} not supported. Must be one of {ACCEPTABLE_TYPES}"
        )
    if file2_type not in ACCEPTABLE_TYPES:
        raise ValueError(
            f"Secondary file type {file2_type} not supported. Must be one of {ACCEPTABLE_TYPES}"
        )
    if file1_type != file2_type:
        raise ValueError(f"File types {file1_type} and {file2_type} must be the same.")

    # create the file objects to pass to the the function
    file1 = File(
        name=args.input1,
        type=file1_type,
        encoding=ENCODING,
        seperator=",",  # this can be changed to a different seperator
    )

    file2 = File(
        name=args.input2,
        type=file2_type,
        encoding=ENCODING,
        seperator=",",  # this can be changed to a different seperator
    )

    # merge the two files
    merge_files(file1=file1, file2=file2, output=args.output)

    print("Done")


if __name__ == "__main__":
    main()
