# Username Mutator

A Python utility that generates various username mutations from a list of names.

## Usage

Basic usage:
```bash
python username_mutator.py input_file.txt
```

Available options:
```bash
python username_mutator.py [-p] [-d N] [-a domain] input_file.txt

-p, --periods     Add versions with periods between name segments
-d N, --digits N  Add numeric suffixes from 1 to N to each username
-a, --add-domain  Add @domain to all usernames
```

Examples:
```bash
# Generate usernames with periods
python username_mutator.py -p input_file.txt

# Generate usernames with numeric suffixes 1-3
python username_mutator.py -d 3 input_file.txt

# Generate usernames with domain suffix
python username_mutator.py -a example.com input_file.txt

# Combine multiple options
python username_mutator.py -p -d 3 -a example.com input_file.txt
```

The input file should contain names, with one to four names per line. For example:
```
John Smith
Mary Jane Watson
James Paul McCartney
```

The utility will output various username mutations to stdout, including:
- Initials (e.g., "js" or with -p: "j.s")
- First initial + lastname (e.g., "jsmith" or with -p: "j.smith")
- Full name concatenated (e.g., "johnsmith" or with -p: "john.smith")
- All permutations of initials and full names
- All possible combinations using subsets of the names
- With -d N: numeric suffixes from 1 to N (e.g., "johnsmith1", "johnsmith2", etc.)
- With -a domain: domain suffix (e.g., "johnsmith@example.com")

## Example Output

For input line "John Smith":
Basic output:
```
js
jsmith
johnsmith
sjohn
sj
```

With all options (-p -d 2 -a example.com):
```
j.s@example.com
j.s1@example.com
j.s2@example.com
j.smith@example.com
j.smith1@example.com
j.smith2@example.com
john.smith@example.com
john.smith1@example.com
john.smith2@example.com
// ... etc
```

## Requirements
- Python 3.6+
