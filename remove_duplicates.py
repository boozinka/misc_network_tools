#!/usr/bin/env python

import os
import socket
import re
import pathlib
from pprint import pprint


def remove_duplicates(my_list):
    # removes duplicate entries from a list

    # Strip newline character from each line
    strip_list = []
    for line in my_list:
        strip_list.append(line.rstrip())

    # Convert to dictionary and returns a list to remove duplicates
    return list(dict.fromkeys(strip_list))


# Welcome screen and setup for initial parameters including the working directory and input file
#os.system('cls')
print("\nThe specified file must be comma separated")
my_file = input("\nPlease enter the output file name: ") 

# Open file and read each line as a list element)
with open(my_file) as duplicated_list:
    my_list = duplicated_list.readlines()

new_list = remove_duplicates(my_list)

pprint(new_list)

# Save output to file
filename = input("\n\nPlease enter the name of the file you wish to save without the file extension: ")
filename = filename+'.csv'
with open(filename, 'w') as file:
    for item in new_list:
        line = [item, "\n"]
        file.writelines(line)
