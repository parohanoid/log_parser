#!/usr/bin/env python3


import fileinput
import argparse
import ipaddress
import re
import sys


def first(line_num, limit):
    if limit != None:
        if line_num < limit:
            return True
        else:
            return False
    return True


def last(line_num, limit, line_count):
    if limit != None:
        if line_num >= (line_count - limit):
            return True
        else:
            return False
    return True


def check_time(line, format):
    if format is not None:
        return bool(re.search(format, line))
    return True


def highlight_ip(text, ip_address, ip_type):
    if ip_address is not None:
        text_arr = text.split(" ")
        highlighted = False
        address_class = (
            ipaddress.IPv4Address if ip_type == "ipv4" else ipaddress.IPv6Address
        )

        for i in range(len(text_arr)):
            try:
                # Check if the current text element is a valid IP address and either matches the target or is not a match (for boolean check)
                if (
                    ip_address != True
                    and address_class(text_arr[i]) == address_class(ip_address)
                ) or (ip_address == True and address_class(text_arr[i])):
                    text_arr[i] = "\033[44m" + text_arr[i] + "\033[0m"
                    highlighted = True
            except ipaddress.AddressValueError:
                continue

        return (True, " ".join(text_arr)) if highlighted else (False, text)
    return (True, text)


def main():
    parser = argparse.ArgumentParser(description="Log File Analysis Tool")

    parser.add_argument(
        "files",
        nargs="*",
        help="Log file path or just the file name if it is in the same directory as this program. Also accepts multiple filenames/paths which will concatenate all files and process as a single log file.",
    )

    parser.add_argument(
        "-f", "--first", type=int, help="Print first NUM lines where NUM is an integer."
    )

    parser.add_argument(
        "-l", "--last", type=int, help="Print last NUM lines where NUM is an integer."
    )

    parser.add_argument(
        "-t",
        "--timestamps",
        nargs="?",
        const=r"([01][0-9]|2[0-3]):[0-5][0-9](:[0-5][0-9])",
        default=None,
        type=str,
        help="Print lines that contain a timestamp in HH:MM:SS format. (Default is HH:MM:SS format, any custom datetime format can be passed in regex expression.)",
    )

    parser.add_argument(
        "-i",
        "--ipv4",
        nargs="?",
        const=True,
        default=None,
        type=str,
        help="Print lines that contain an IPv4 address, if input is given matching IPs are highlighted else all lines with IPv4 are printed.",
    )
    # matching IPs are highlighted

    parser.add_argument(
        "-I",
        "--ipv6",
        nargs="?",
        const=True,
        default=None,
        type=str,
        help="Print lines that contain an IPv6 address in standard notation, if input is given matching IPs are highlighted else all lines with IPv6 are printed.",
    )
    # matching IPs are highlighted

    parser.add_argument(
        "-n",
        "--new-log",
        nargs="?",
        const="filtered.log",
        default=None,
        type=str,
        help="Create a new log file with the filtered log lines, value can be given as the new file name including the file extension (example/default: filtered.log).",
    )
    # matching IPs are highlighted

    args = parser.parse_args()

    # Check if we're reading from stdin
    if not args.files:  # No files provided
        lines = sys.stdin.readlines()  # Read all stdin lines into memory
    else:
        with fileinput.input(files=args.files or ("-",)) as f:
            lines = list(f)  # Store lines in memory
    
    # total line count
    line_count = len(lines)

    if args.new_log:
        output_file = open(args.new_log, "w")

    for i in range(line_count):

        ipv4_matched, h_line_ipv4 = highlight_ip(lines[i], args.ipv4, "ipv4")
        ipv6_matched, h_line_ipv6 = highlight_ip(h_line_ipv4, args.ipv6, "ipv6")

        if (
            first(i, args.first)
            and last(i, args.last, line_count)
            and check_time(lines[i], args.timestamps)
            and ipv4_matched
            and ipv6_matched
        ):
            print(h_line_ipv6, end="")
            if args.new_log is not None:
                output_file.write(lines[i])

    if args.new_log:
        output_file.close()
    
    print()


if __name__ == "__main__":
    main()






