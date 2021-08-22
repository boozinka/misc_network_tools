#!/usr/bin/env python

# DNS Resolver
# Reads a file and does a forward or reverse DNS lookup
# Writes output to a new file

import os
import socket
import pathlib
from pprint import pprint

def set_working_dir():
    # Welcome screen and setup for initial parameters including the working directory and input file

    working_dir = ""

    directory_input = False
    while not directory_input:
        working_dir = pathlib.Path(input("Please enter the directory path where all files"
                                         " will be read from and written to: "))
        directory_input = pathlib.Path.exists(working_dir)
        if not directory_input:
            input("Invalid path or directory, press enter to try again. ")
            os.system('cls')
    return working_dir


def get_file(working_dir):
    # Welcome screen and setup for initial parameters including the working directory and input file

    my_file = None
    file_input = False

    while not file_input:
        os.system('cls')
        print("\nThe specified file must be comma separated")
        file_name = input("\nPlease enter the input file name: ")
        my_file = working_dir / file_name
        file_input = pathlib.Path.exists(my_file)
        if not file_input:
            input("Invalid file name or file does not exist, press enter to try again. ")
    return my_file


def read_file(my_file):
    # Open file and read it as a string)

    with open(my_file) as analyser_log:
        analyser_log = analyser_log.read()
    return analyser_log


def write_dict(fqdn_dict):
    # write the hostnames and IP addresses to a .csv file

    filename = input("\n\nPlease enter the name of the file you wish to save without the file extension: ")
    filename = filename+'.csv'
    with open(filename, 'w') as file:
        for keys,values in fqdn_dict.items():
            fqdn_pair = [keys, ",", values, "\n"]
            file.writelines(fqdn_pair)


def remove_duplicates(my_list):
    # removes duplicate entries from a list

    my_set = set(my_list)  # Convert list to a set
    my_set |= my_set  # Remove Duplicate entries
    my_list = list(my_set)  # Convert back to a list
    return my_list


def print_dict(fqdn_dict):
    # Print the FQDN Dictionary formatted on the screen

    print(f'{"HOSTNAME":<50} {" "*5:5} {"IP ADDRESS":>20}')
    print(f'{"-"*50:50} {" "*5:5} {"-"*20:20}')
    for keys,values in fqdn_dict.items():
        # Print table of FQDN Hostnames and their IP addresses.
        print(f'{keys:<50} {" "*5:5} {values:>20}')
    print()


def forward_dns(host_str):
    # Forward DNS Lookup - Resolves FQDN's to IP addresses

    print("\n\n")
    print(" ### WARNING - Resolving large lists can take considerable time ###")
    print("The specified file must be a .txt or .csv file in the format of one IP address per line")
    choice = input("\nPress any key to continue or '0' to return to the Main Menu ")
    
    ip_list = []
    fqdn_pairs = {}
    resolved_host_dict = {}
    unresolved_host_dict = {}
    host_list = host_str.splitlines()  # remove '/n' and convert to a list
    if choice == "0":
        return choice
    else:
        for hostname in host_list:
            try:
                # returns IP address for a given hostname
                ip_data = socket.getaddrinfo(hostname, None)
                ip_addr = [x[4][0] for x in ip_data]
                ip_addr = ip_addr[0]
                ip_list.append(ip_addr)  # creates list of ip's based on resolvable hosts only
            except socket.gaierror:
                # handles resolution errors, by creating a dictionary of unresolved hostnames
                ip_addr = "Unresolved"
                unresolved_host_dict[hostname] = ip_addr

        for ip_addr in ip_list:
            try:
                # returns FQDN's from the IP list resolved from hostnames
                my_socket = (ip_addr, 0)
                host_data = socket.getnameinfo(my_socket, 0)
                fqdn_hostname = host_data[0]
            except socket.gaierror:
                # handles IP's with no FQDN
                fqdn_hostname = "Unresolved"
            resolved_host_dict[fqdn_hostname] = ip_addr
        # concatanations both resolved and unresolved dictionaries
        fqdn_pairs = dict(resolved_host_dict)
        fqdn_pairs.update(unresolved_host_dict)
        return fqdn_pairs


def reverse_dns(ip_str):
    # Reverse DNS Lookup - Resolves IP addresses to FQDN's

    print("\n\n")
    print(" ### WARNING - Resolving large lists can take considerable time ###")
    print("The specified file must be a .txt or .csv file in the format of one IP address per line")
    choice = input("\nPress any key to continue or '0' to return to the Main Menu ")

    fqdn_pairs = {}
    ip_list = ip_str.splitlines()  # remove '/n' and convert to a list
    if choice == "0":
        return choice
    else:
        for ip_addr in ip_list:
            try:
                my_socket = (ip_addr, 0)
                host_data = socket.getnameinfo(my_socket, 0)
                hostname = host_data[0]
            except socket.gaierror:
                # handles IP's with no FQDN
                hostname = "Unresolved"
            fqdn_pairs[hostname] = ip_addr
    return fqdn_pairs


def main_menu():
    # Setup Main Menu Loop

    os.system('cls')
    mm_choice = None
    while mm_choice != "0":
        print(
            """
            Main Menu

            0 - Quit
            1 - Forward DNS Lookups - Resolve FQDN's to IP addresses
            2 - Reverse DNS Lookups - Resolve IP addresses to FQDN's
            """
        )

        mm_choice = input("Choice: ")
        print()
        return mm_choice


# Main Program Function
def main():
    """Main Program"""

    datafolder = set_working_dir()

    mm_val = None
    while mm_val != "0":
        mm_val = main_menu()
        if mm_val == "1":
            print("\nForward DNS Lookup Routine...")
            file_name = get_file(datafolder)
            host_str = read_file(file_name)  # read IP's in from file as a string
            fqdn_pairs = remove_duplicates(host_str)
            fqdn_pairs = forward_dns(host_str)
            if fqdn_pairs != '0':  # print the dictionary of IP's and FQDN's if not cancelled
                os.system('cls')
                print_dict(fqdn_pairs)
                save_file = input("\n\nPress 's' to save as a .csv or enter to return to the main menu. ").lower()
                if save_file == "s":
                    write_dict(fqdn_pairs)
        elif mm_val == "2":
            print("\nReverse DNS Lookup Routine...")
            file_name = get_file(datafolder)
            ip_str = read_file(file_name)  # read IP's in from file as a string
            fqdn_pairs = remove_duplicates(ip_str)
            fqdn_pairs = reverse_dns(ip_str)
            if fqdn_pairs != '0':  # print the dictionary of IP's and FQDN's if not cancelled
                os.system('cls')
                print_dict(fqdn_pairs)
                save_file = input("\n\nPress 's' to save as a .csv or enter to return to the main menu. ").lower()
                if save_file == "s":
                    write_dict(fqdn_pairs)


main()
input("\n\nPress the enter key to exit.")
