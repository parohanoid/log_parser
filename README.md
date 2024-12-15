# Features

This is a CLI log utility filtering log lines as required.

Run ```source/util.py -h``` to know the usages of features.


1. Filter first or last N lines (Considers total line count of all the files if multiple files are given)
2. Filter only the lines containing timestamps in the format - HH:MM:SS. (Custom format can be passed as a regex value)
3. Filter only the lines with a valid IPv4 or IPv6 addresses (A specific IP address can be passed to match only that IP address; IP addresses in the file need to be separated by space). Also highlights the matched addresses.
4. Supports passing multiple files
5. You may create a new log file of the filtered lines using -n. (a custom name for the new file can be given by passing the argument value: --new-log="new_file_name.log")
6. More the filters, smaller the output (Filter is the intersection of all options)


# Usage:
1. Download source/util.py
2. Run util.py with command line arguments as desired.

### Example:

The below arguments would create a new file called ```first100_ipv6.log``` with IPv6 addresses and with timestamps:
```
python3 source/util.py Linux_2k.log Linux_2.log -f 100 -t -I -n "first100_ipv6.log"
```


# Run Tests:
1. Clone Repo
2. Install pytest and pytest-html with ```pip install -r requirements.txt```
3. Run all tests and generate a shareable report with:
```
pytest tests/ --html=report.html --self-contained.html
```



Test log files were sourced from https://github.com/logpai/loghub/tree/master/Linux