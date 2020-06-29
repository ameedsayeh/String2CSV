import sys
import os
import datetime
import re
import argparse

usage_instructions = \
    """
    String2CSV Usage:

    [python3] String2CSV.py (String File Path) [Output CSV Path] [CSV Delimiter] [Sort Alphabetically]
    or
    [python3] String2CSV.py (String File Path) --output [Output CSV Path] --del [CSV Delimiter] --sort [Sort Mode Alphabetically]
    """
help_instructions = \
    """
    {}

    Mandatory fields:
    =   String File Path: eg. /Users/ameedsayeh/Desktop/Localizable.string

    Optional fields:
    =   Output CSV File Path: Path to save the output csv file.
        Can be specified using --output
        Default Value: <Current Path>/output_csv_<timestamp>.csv

    =   Delimiter: Generated CSV file delimiter.
        Can be specified using --del
        Default Value: Semi-Colon ";".

    =   Sort Mode: Sort Generated file alphabitacally with these modes:
        - 0: (Default) No sort.
        - 1: Sort Keys alphabitacally in ascending order.
        - 2: Sort Keys alphabitacally in descending order.
        - 3: Sort Values alphabitacally in ascending order.
        - 4: Sort Values alphabitacally in descending order.

    Salam.
    """.format(usage_instructions)

if __name__ == "__main__":

    string_file_path = sys.argv[1] if len(sys.argv) >= 2 else None
    output_file_path = sys.argv[2] if len(sys.argv) >= 3 else None
    csv_file_delimiter = sys.argv[3] if len(sys.argv) >= 4 else None

    if string_file_path == None:
        print(usage_instructions)
        exit(-1)

    if string_file_path in ["help", "HELP", "-help", "--help"]:
        print(help_instructions)
        exit(0)

    if not os.path.exists(string_file_path) or not os.path.isfile(string_file_path):
        print("Cannot find file at path: {}".format(string_file_path))
        exit(-1)

    if output_file_path == None:
        generated_output_file_name = "output_csv_{}.csv".format(datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S"))
        output_file_path = "{}/{}".format(os.getcwd(), generated_output_file_name)
    
    if csv_file_delimiter == None:
        csv_file_delimiter = ";"
    
    input_file = open(string_file_path, "r")
    input_data = input_file.read()

    results = re.findall(r'"(.*)"\s=\s"(.*)";\n', input_data)

    if results != None and len(results) > 0:
        output_file = open(output_file_path, "w")
        for res in results:
            if len(res) == 2:
                output_file.write("{}{}{}\n".format(res[0], csv_file_delimiter, res[1]))
        output_file.close()

    print("Done!")
    input_file.close()