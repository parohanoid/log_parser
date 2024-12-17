# Log Parser

#### Description:


The **Log Parser** is a flexible and efficient command-line utility for processing and filtering log files. Whether you're working with logs containing timestamps, IP addresses, or just large volumes of data, this tool provides features to extract relevant information quickly and effectively. 

## Overview

This project provides a robust solution for log file analysis. It was designed to handle common log processing tasks, such as extracting specific data, working with timestamps or IP addresses, and processing multiple files simultaneously. Each file in the project contributes to the functionality of this tool, as detailed below:

### Project Files

1. **util.py**:
   - This is the core script that implements all the tool's functionality.
   - Contains functions for filtering logs by line numbers, timestamps, and IP addresses.
   - Supports multi-file processing, custom output files, and combining multiple filters.

2. **tests/**:
   - A directory containing unit tests for the utility.
   - Tests are written using the **pytest** framework to ensure reliability and correctness of all features.
   - Includes edge case handling and validation for key functionalities such as timestamp parsing and IP address detection.

3. **requirements.txt**:
   - Lists all the Python dependencies required to run the tool and tests.
   - Ensures a smooth setup process for users and contributors.

4. **README.md**:
   - This file serves as the primary documentation for the project.
   - Provides an overview, detailed feature descriptions, usage instructions, testing guidelines, and contribution details.

## Features

This utility comes with several key features designed to make log processing more streamlined:

1. **Filter First or Last N Lines**:
   - Allows you to extract the first or last `N` lines from the log files.
   - Handles multiple log files by considering the total line count across all files.

2. **Timestamp Filtering**:
   - Filters log lines containing timestamps.
   - By default, the utility detects timestamps in the format `HH:MM:SS`.
   - Custom timestamp formats can be provided using regular expressions.

3. **IPv4 and IPv6 Address Filtering**:
   - Filters lines containing valid IPv4 or IPv6 addresses.
   - Optionally, highlight matching IP addresses.
   - Specific IP addresses can be passed to filter and highlight only matching addresses.

4. **Multi-file Support**:
   - Accepts multiple log files as input and processes them as a single unified file.

5. **Filtered Output to a New Log File**:
   - Saves filtered lines to a new log file.
   - You can specify a custom name for the output file.

6. **Intersection of Filters**:
   - Multiple filters can be applied simultaneously.
   - Only log lines satisfying all specified filters will be included in the output.

## Usage

### Prerequisites

Ensure you have Python 3 installed on your system. To check, run:
```bash
python3 --version
```


### Command-line Arguments

Run the tool with the following syntax:
```bash
python3 util.py [options] [files]
```

To see a full list of options and their descriptions, run:
```bash
python3 util.py -h
```

### Example Commands

1. **Extract the first 100 lines from a log file:**
   ```bash
   python3 util.py example.log -f 100
   ```

2. **Filter lines containing timestamps in `HH:MM:SS` format:**
   ```bash
   python3 util.py example.log -t
   ```

3. **Filter lines with IPv4 addresses and save to a new file:**
   ```bash
   python3 util.py example.log -i -n "filtered_ipv4.log"
   ```

4. **Apply multiple filters simultaneously:**
   ```bash
   python3 util.py example1.log example2.log -f 50 -t -I -n "filtered_output.log"
   ```
   This will filter the first 50 lines containing timestamps and IPv6 addresses from `example1.log` and `example2.log`, and save the output to `filtered_output.log`.



## Running Tests

The utility includes comprehensive test coverage using **pytest**. Follow these steps to run the tests:

### Install Dependencies

Install required packages:
```bash
pip install -r requirements.txt
```

### Run Tests

Run all tests and generate an HTML report:
```bash
pytest tests/ --html=report.html --self-contained-html
```

This command generates a `report.html` file that you can open in any web browser for a detailed view of the test results.

### Test Suite Details

The tests cover the following:

1. **Line Filtering Logic:**
   - Tests for filtering the first or last `N` lines.

2. **Timestamp Detection:**
   - Validation of timestamp formats and their filtering.

3. **IP Address Matching and Highlighting:**
   - Includes IPv4 and IPv6 tests for specific and generic matching.

4. **Edge Cases:**
   - Handling of invalid data, empty inputs, and other edge cases.

## Sample Log Files

You can use publicly available sample log files to test the tool. For example:

- [Linux Loghub](https://github.com/logpai/loghub/tree/master/Linux)

Download sample file from this repository to try out the utility's features.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests if you find bugs, have feature requests, or want to improve the code or documentation.


## Acknowledgements

- Test log files were sourced from the [Loghub Linux dataset](https://github.com/logpai/loghub/tree/master/Linux).

---

**Happy Logging!**
