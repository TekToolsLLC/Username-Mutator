#!/usr/bin/env python3

import sys
import itertools
import argparse
from typing import List, Set

def get_initials(names: List[str]) -> str:
    """Get initials from a list of names."""
    return ''.join(name[0].lower() for name in names)

def get_first_initial_lastname(names: List[str]) -> str:
    """Get first initial + last name."""
    if len(names) < 2:
        return names[0].lower()
    return f"{names[0][0]}{names[-1]}".lower()

def get_fullname(names: List[str]) -> str:
    """Get concatenated full name."""
    return ''.join(names).lower()

def join_names(names: List[str], use_periods: bool = False) -> str:
    """Join names together, optionally with periods between them."""
    names = [name.lower() for name in names]
    return '.'.join(names) if use_periods else ''.join(names)

def join_initials(names: List[str], use_periods: bool = False) -> str:
    """Join initials together, optionally with periods between them."""
    initials = [name[0].lower() for name in names]
    return '.'.join(initials) if use_periods else ''.join(initials)

def add_numeric_suffixes(username: str, suffix_limit: int, domain: str = "") -> Set[str]:
    """Add numeric suffixes to a username up to the given limit, optionally with domain."""
    if suffix_limit <= 0:
        return {f"{username}{domain}" if domain else username}
    return {f"{username}{i}{domain}" if domain else f"{username}{i}" 
            for i in range(1, suffix_limit + 1)} | {f"{username}{domain}" if domain else username}

def generate_name_mutations(names: List[str], use_periods: bool = False, 
                          suffix_limit: int = 0, domain: str = "") -> Set[str]:
    """Generate all possible username mutations from a list of names."""
    mutations = set()
    base_mutations = set()  # Store mutations before adding suffixes
    
    # Add basic mutations
    base_mutations.add(get_initials(names))
    base_mutations.add(get_first_initial_lastname(names))
    base_mutations.add(get_fullname(names))
    
    if use_periods:
        base_mutations.add(join_initials(names, True))
        base_mutations.add(f"{names[0][0]}.{names[-1]}".lower() if len(names) > 1 else names[0].lower())
        base_mutations.add(join_names(names, True))
    
    # Generate all possible subsets of names (excluding empty set)
    for r in range(1, len(names) + 1):
        for name_subset in itertools.combinations(names, r):
            # For each subset, generate all possible orderings
            for perm_names in itertools.permutations(name_subset):
                # Add full name version
                base_mutations.add(join_names(perm_names))
                base_mutations.add(join_initials(perm_names))
                if use_periods:
                    base_mutations.add(join_names(perm_names, True))
                    base_mutations.add(join_initials(perm_names, True))
    
    # Generate permutations with initials and full names
    name_elements = []
    for name in names:
        name_elements.append([name.lower(), name[0].lower()])
    
    # Generate all possible combinations
    for combination in itertools.product(*name_elements):
        base_mutations.add(''.join(combination))
        if use_periods:
            base_mutations.add('.'.join(combination))
    
    # Add numeric suffixes (and domain if specified) to all base mutations
    domain_suffix = f"@{domain}" if domain else ""
    for mutation in base_mutations:
        mutations.update(add_numeric_suffixes(mutation, suffix_limit, domain_suffix))
    
    return mutations

def process_file(filename: str, use_periods: bool = False, 
                suffix_limit: int = 0, domain: str = "") -> None:
    """Process input file and print username mutations."""
    try:
        with open(filename, 'r') as file:
            for line in file:
                # Split line into names and remove empty strings
                names = [name.strip() for name in line.strip().split()]
                if not names:
                    continue
                
                # Generate and print mutations
                mutations = generate_name_mutations(names, use_periods, suffix_limit, domain)
                for mutation in sorted(mutations):
                    print(mutation)
                
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Generate username mutations from a file')
    parser.add_argument('filename', help='Input file containing names')
    parser.add_argument('-p', '--periods', action='store_true', 
                      help='Add versions with periods between name segments')
    parser.add_argument('-d', '--digits', type=int, metavar='suffix_limit',
                      help='Add numeric suffixes from 1 to suffix_limit')
    parser.add_argument('-a', '--add-domain', type=str, metavar='domain',
                      help='Add @domain to all usernames')
    
    args = parser.parse_args()
    process_file(args.filename, args.periods, args.digits or 0, args.add_domain or "")

if __name__ == "__main__":
    main()
