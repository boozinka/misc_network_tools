#!/usr/bin/env python

""" This program reads an output file, and then searches and captures private
    BGP AS numbers.
"""

# Author: Wayne Bellward
# Date:   29/10/2021


import re
import pathlib
import itertools
from pprint import pprint
from datetime import datetime



def set_working_dir():
    """ Function that sets the working directory """

    working_dir = ""

    directory_input = False
    while not directory_input:
        working_dir = pathlib.Path(input("Please enter the path to your input"
                        " file, or 'enter' if it's in the same directory as"
                        " this program: "))
        directory_input = pathlib.Path.exists(working_dir)
        if not directory_input:
            input("Invalid path or directory, press enter to try again. ")
    return working_dir


def get_filename(file_path, message):
    """ Ask user for the filename of the policy id list and validates it """

    my_file = None
    file_input = False

    while not file_input:
        file_name = input(message)
        my_file = file_path / file_name
        file_input = pathlib.Path.exists(my_file)
        if not file_input or file_name == '':
            file_input = False
            print("Invalid file name or file does not exist,"
                  " please try again. ")
    return my_file


def read_file(my_file):
    # Open file and read it as a string)

    with open(my_file) as bgp_out:
        sh_ip_bgp = bgp_out.read()
    return sh_ip_bgp


def write_file(as_ranges):
    """ Writes the contents of the list to a .csv file. """

    now = datetime.now()
    dt_str = now.strftime('%d-%m-%y_%H%M%S')

    filename = 'bgp_as_ranges' + '_' + dt_str +'.csv'
    print('\nThe BGP AS number ranges have been written to "', filename,
          '" in the local directory', sep = '')
    print()

    with open(filename, 'w') as file:

        # Write header
        header = ['Start AS Number', ',', 'End AS Number', '\n']
        file.writelines(header)

        for as_tuple in as_ranges:
            if as_tuple[0] == as_tuple[1]:
                line = [str(as_tuple[0]), '\n']
                file.writelines(line)
            else:
                line = [str(as_tuple[0]), ',', str(as_tuple[1]), '\n']
                file.writelines(line)


def find_ranges(as_list):
    """ Find ranges in a list of BGP AS numbers """

    # Convert list AS numbers strings into a list of as number integers
    as_list = list(map(int, as_list))

    # Create an ascending sorted set from list
    iterable = sorted(set(as_list))

    # Create tuples of ranges in the number sequence
    for key, group in itertools.groupby(enumerate(iterable),
                                        lambda pair: pair[1] - pair[0]):
        group = list(group)
        yield group[0][1], group[-1][1]
        

def capture_pri_as (sh_ip_bgp):
    """ Capture private BGP AS numbers to a list """

    """ The following explains the patterns defined in the 'pattern_list'

        6451[2-9]	  - (matches on 64512 – 64519)
        645[2-9][0-9]	  - (matches on 64520 – 64599)
        64[6-9][0-9][0-9] - (matches on 64600 – 64999)
        65[0-4][0-9][0-9] - (matches on 65000 – 65499)
        655[0-2][0-9]	  - (matches on 65500 – 65529)
        6553[0-5]	  - (matches on 65530 – 65535)
    """

    pattern_64519 = re.compile(r'6451[2-9]')
    pattern_64599 = re.compile(r'645[2-9][0-9]')
    pattern_64999 = re.compile(r'64[6-9][0-9][0-9]')
    pattern_65499 = re.compile(r'65[0-4][0-9][0-9]')
    pattern_65529 = re.compile(r'655[0-2][0-9]')
    pattern_65535 = re.compile(r'6553[0-5]')


    pattern_list = [pattern_64519,
                    pattern_64599,
                    pattern_64999,
                    pattern_65499,
                    pattern_65529,
                    pattern_65535,
                    ]

    bgp_as_nums = []
    
    for pattern in pattern_list:
        tmp_as_nums = re.findall(pattern, sh_ip_bgp)
        # Remove duplicate AS numbers
        tmp_as_nums = list(dict.fromkeys(tmp_as_nums))
        bgp_as_nums.extend(tmp_as_nums)
    return (list(find_ranges(bgp_as_nums)))


def main():
     """ Main program """

     # Read and process the firewall config file into a list
     file_path = set_working_dir()
     input_message = ("\nEnter the full filename containing the 'show ip bgp'"
                         " output: ")
     my_file = get_filename(file_path, input_message)

     bgp_str = read_file(my_file)
     as_ranges = capture_pri_as(bgp_str)
     write_file(as_ranges)
     input('\nPress enter to close the program.')


if __name__ == "__main__":
    main()
