import sys
import os
import re
import argparse
from datetime import datetime
from collections import OrderedDict

def generate_output_file_name():
    return os.path.join(os.getcwd(), "output_{}.string".format(datetime.now().strftime("%Y%m%d%H%M%S")))

def get_regex(csv_delimiter):
    return r'(.*){}(.*)\n'.format(csv_delimiter)

def find_all_matching(input_file_path, input_file_encoding, regex):
    input_file = open(input_file_path, "r", encoding=input_file_encoding)
    input_data = input_file.read()
    input_file.close()

    return list(re.findall(regex, input_data))

def remove_duplicate_keys(data):
    filtered_data = list(OrderedDict.fromkeys(data))

    return filtered_data

def sort_data(data, sort_mode = 0):

    if sort_mode not in range(1,5):
        return data

    if sort_mode == 1:
        key_index = 0
        reverse = False
    elif sort_mode == 2:
        key_index = 0
        reverse = True
    elif sort_mode == 3:
        key_index = 1
        reverse = False
    elif sort_mode == 4:
        key_index = 1
        reverse = True
        
    return sorted(data, key=lambda group: group[key_index],reverse=reverse)

def convert_to_string_format(data):
    buffer = ""
    for group in data:
        buffer += "\"{}\" = \"{}\";\n".format(group[0], group[1])

    return buffer

def write_data_on_file(output_data, output_file_path, output_file_encoding):
    output_file = open(output_file_path, "w", encoding=output_file_encoding)
    output_file.write(output_data)
    output_file.close()

def print_end_message(output_file_path, num_keys, duplicates):
    print("Done!\nGenerated {} key(s) in file {}.\n{} Duplicate(s) was/were removed".format(num_keys, output_file_path, duplicates))


def main():

    ### Start - Parsing Args ###
    parsed_args = parser.parse_args()

    input_file_path = parsed_args.input
    csv_delimiter = parsed_args.delimiter
    sort_mode = parsed_args.sort
    input_file_encoding = parsed_args.input_encoding
    output_file_encoding = parsed_args.output_encoding
    remove_duplicates = parsed_args.remove_duplicates
    silent = parsed_args.silent

    if parsed_args.output is None:
        output_file_path = generate_output_file_name()
    else:
        output_file_path = parsed_args.output
    ### End - Parsing Args ###
    
    results = find_all_matching(input_file_path, input_file_encoding, get_regex(csv_delimiter))

    starting_length = len(results)

    if remove_duplicates:
        results = remove_duplicate_keys(results)
    
    sorted_data = sort_data(results, sort_mode)
    output_data = convert_to_string_format(sorted_data)
    write_data_on_file(output_data, output_file_path, output_file_encoding)

    if not silent:
        ending_length = len(results)
        print_end_message(output_file_path, ending_length, starting_length - ending_length)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="CSV2String Convertor")

    parser.add_argument("--input", type=str, required=True, action="store", help="Source .csv file path")
    parser.add_argument("--delimiter", type=str, required=True, action="store", help="csv delimiter", default=";")
    parser.add_argument("--output", type=str, required=False, action="store", help="Output .string file path")
    parser.add_argument("--sort", type=int, required=False, action="store", help="Sort Mode", default=0)
    parser.add_argument("--input-encoding", type=str, required=False, action="store", help="Source .csv file encoding", default="utf-8")
    parser.add_argument("--output-encoding", type=str, required=False, action="store", help="Output .string file encoding", default="utf-8")
    parser.add_argument("--remove-duplicates", required=False, action="store_true", help="Remove Duplicate Keys")
    parser.add_argument("--silent", required=False, action="store_true", help="No printing")

    main()
