#!/usr/bin/env python

""" Reads a list of IPv4 addresses, removes duplicates, sorts the list
    canonically and merges them into groups of summary addresses.
"""

# Author: Wayne Bellward
# Date: 30/06/2022


import os
import sys
import pathlib
import netaddr
from ipaddress import IPv4Network
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
            os.system('cls')
    return working_dir


def get_filename(file_path, message):
    """ Welcome screen and setup for initial parameters including
        the working directory and input file """

    my_file = None
    file_input = False

    while not file_input:
        os.system('cls')
        print("\nThe specified file must be comma separated")
        file_name = input(message)
        my_file = file_path / file_name
        file_input = pathlib.Path.exists(my_file)
        if not file_input or file_name == '':
            file_input = False
            input("Invalid file name or file does not exist,"
                  " press enter to try again. ")
    return my_file


def remove_duplicates(my_list):
    """ Removes duplicate entries from a list """

    # Strip newline character from each line
    strip_list = []
    for line in my_list:
        strip_list.append(line.rstrip())

    # Convert to dictionary and returns a list to remove duplicates
    return list(dict.fromkeys(strip_list))


def get_ipv4_list(file_name):
    """ Open and read the file of IP addresses, converting each IP address
        to a list element,
    """

    # Initialise varibles
    ipv4_list = []

    # Open file and read each line as a list element
    with open(file_name) as duplicated_list:
        my_list = duplicated_list.readlines()

    # Remove duplicates from the list
    ipv4_list = remove_duplicates(my_list)
        
    return sorted(ipv4_list)


def summarise_ipaddress(ipv4_list):
    """ Performs a 'cidr_merge' on a list of string addresses and returns
        a list of summary addresses as type IPv4.
    """

    summary_net_list = netaddr.cidr_merge(ipv4_list)

    return summary_net_list


def print_subnets(cidr_list):
    """ Outputs the CIDR subnets to the screen """

    print()
    print(f'{"CIDR Prefix":>20}')
    print('-'*20)
    print()
    for cidr in cidr_list:
        print(f'{str(cidr):>20}')
    print('\n\n')


def write_cidr(cidr_list):
    """ Write CIDR summary prefixes to a .csv file """

    now = datetime.now()
    dt_str = now.strftime('%d-%m-%y_%H%M%S')

    suffix = '_' + dt_str

    filename = input("\n\nPlease enter the name of the file you wish to save without the file extension: ")
    filename = filename + suffix +'.csv'

    header = ['CIDR Prefix', ',', 'Subnet Mask', '\n']
             
    with open(filename, 'w') as file:
        file.writelines(header)
        for cidr in cidr_list:
            ipv4_cidr = IPv4Network(cidr)
            cidr_line = [str(ipv4_cidr.network_address), ',',
                         str(ipv4_cidr.netmask), '\n']
            file.writelines(cidr_line)
                
    print('\nThe file has been written to timestamped "', filename,
          '" in the local directory', sep = '')
    print()


def main():
    """ Main Program, used when the module is run directly as a script """
    
    # Read and process the firewall config file into a list
    file_path = set_working_dir()
    message = ("\nEnter the full filename containing the list of "
               "IP addresses you want to merge into CIDR subnets: ")
    
    file_name = get_filename(file_path, message)
    ipv4_list = get_ipv4_list(file_name)
    cidr_list = summarise_ipaddress(ipv4_list)
    print_subnets(cidr_list)

    answer = input('Do you want to write the results to a file (y/n): ')
    if answer.lower() == 'y':
        write_cidr(cidr_list)

    input('\nPress enter to exit the program')

    
main()
