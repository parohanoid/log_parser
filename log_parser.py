import datetime
import fileinput
import argparse
import ipaddress


def first(input_arg):
    if input_arg is not None:
        if fileinput.lineno() <= input_arg:
            return True
        else:
            return False
    return True


def last(input_arg, line_count):
    if input_arg is not None:
        if fileinput.lineno() >= (line_count - input_arg):
            return True
        else:
            return False
    return True


def check_time(line, format):
    if format is not None:

        text_arr = line.split(" ")
        matched = False

        for i in range(len(text_arr)):
            try:
                datetime.datetime.strptime(text_arr[i], format)
                return True
            except ValueError:
                continue

        return matched

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
        const="%H:%M:%S",
        default=None,
        type=str,
        help="Print lines that contain a timestamp in HH:MM:SS format. (Default is HH:MM:SS format (pythonic: %H:%M:%S), any custom datetime format can also be passed but must be passed in pythonic format: https://strftime.org/.)",
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

    # total line count
    line_count = 0
    with fileinput.input(files=args.files or ("-",)) as f:
        for line in f:
            line_count += 1

    print("Output:")

    if args.n is not None:
        output_file = open(args.n, "w")

    with fileinput.input(files=args.files or ("-",)) as f:
        for line in f:

            ipv4_matched, line = highlight_ip(line, args.i, "ipv4")
            ipv6_matched, line = highlight_ip(line, args.I, "ipv6")

            if (
                first(args.f)
                and last(args.l, line_count)
                and check_time(line, args.t)
                and ipv4_matched
                and ipv6_matched
            ):
                print(line)
                if args.n is not None:
                    output_file.write(line + "\n")
    
    if args.n is not None:
        output_file.close()

    # Implementation based on increasing specificity

    # for line in fileinput.input(encoding="utf-8"):
    #     if fileinput.lineno() <= 10:
    #         print(line)

    # optional features
    # 1. start and end date and time stamp
    # 2. feed data to an ML
    # 3. multiple files - done
    # 4. create a new log file after applying the filters - done
    # 5. status code

    # Bugs / Improvements:
    #     1. However, since fileinput allows for multiple files to be processed, the line numbers may reset for each new file, which can make this logic difficult to apply when working with multiple files. This could lead to bugs or unexpected behavior.

    # Suggested fix: Track the line count for the entire set of files and pass that value to first() and last().
    
    # 2. use re for time
    #     The check_time function checks for a timestamp in each line by splitting it and trying to match each word against the provided timestamp format. This logic is prone to errors, especially if the timestamp is not in the expected position.

    # It would be more robust to use regular expressions or look for specific patterns (e.g., ^\d{2}:\d{2}:\d{2}$) to identify the timestamp.

    # Suggested fix: Use a regular expression to match the timestamp more accurately:

    # python
    # Copy code
    # import re
    # def check_time(line, format):
    #     if format is not None:
    #         pattern = r'\b\d{2}:\d{2}:\d{2}\b'
    #         if re.search(pattern, line):
    #             return True
    #     return False


    # Tasks:
    # 1. multiple files lines - done
    # 2. errors
    # 3. use re for timestamp?
    # 4. test suite
    # 5. 
    


if __name__ == "__main__":
    main()
