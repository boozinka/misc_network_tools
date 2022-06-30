## misc_network_tools

#### ipv4_dns_resolver.py

Gives user the option to perform either a forward or reverse DNS lookup, reads in the relative files of IP addresses or hostnames depending on the chosen option and prints the FQDN to the screen with the option to save them to a .csv file.

#### ipv4_ipv6_dns_resolver.py

Works the same as "ipv4_dns_resolver.py" but works for both IPv4 and IPv6 IP addresses.

#### remove_duplicates.py

Reads in a file (.txt or .csv) containing a list treating the entries as strings. It then removes any duplicate entries and prints the output to a new .csv file. 

#### as_num_parse.py

Reads in the ouput from "show ip bgp", parses all the BGP AS numbers from the output and writes them to a file in ranges.

#### cidr_creator.py

Reads in a list of IPv4 addresses as strings, calculates the available CIDR subnets and outputs them
