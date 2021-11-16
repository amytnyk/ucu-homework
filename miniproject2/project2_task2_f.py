"""
Module like grep
"""
import argparse
import os
import re
from typing import Dict


def get_matched_files(file_pattern: str):
    """
    Yields all files under current directory that match the pattern
    """
    for subdir, dirs, files in os.walk('./'):  # search in current directory
        for file in files:
            file_path = os.path.join(subdir, file)
            if re.match(file_pattern, file_path) is not None:
                yield file_path


def search_lines(path: str, match_pattern: str) -> Dict[int, str]:
    """
    (str, str) -> Dict[line_number, line]
    Returns all lines in file, located at path, that match the pattern
    """
    try:
        matched_lines = dict()
        with open(path, 'r') as file:
            lines = file.readlines()
            for idx, line in enumerate(lines):
                if re.search(match_pattern, line) is not None:
                    matched_lines[idx + 1] = line.strip()
        return matched_lines
    except (PermissionError, UnicodeDecodeError, Exception):
        return dict()  # Maybe access to file is restricted or it's binary


def match(file_pattern: str, match_pattern: str) -> Dict[str, Dict[int, str]]:
    """
    (str, str) -> Dict[filename, Dict[line_number, line]]
    Returns all files that have matched lines
    """
    matches = dict()
    for file in get_matched_files(file_pattern):
        lines = search_lines(file, match_pattern)
        if len(lines) > 0:
            matches[file] = lines
    return matches


def make_colored(text: str, colorcode: int, bold: bool) -> str:
    return f"\033[{int(bold)};{colorcode}m{text}\033[0m"


def print_matches(file_pattern: str, match_pattern: str, count_only: bool,
                  show_lines: bool):
    matches = match(file_pattern, match_pattern)
    if count_only:
        print(sum(map(lambda _, lines: len(lines), matches.items())))
    else:
        for filename, matched_lines in matches.items():
            print(make_colored(filename, 34, True))
            for line_number, line in matched_lines.items():
                if show_lines:
                    print(make_colored(str(line_number), 32, False), end=': ')
                print(re.sub(match_pattern,
                             lambda x: make_colored(x.group(), 31, True), line))


def main():
    """
    Main function for text finder aka grep
    """
    parser = argparse.ArgumentParser(description='grep')
    parser.add_argument('str_pattern', type=str, help='string pattern')
    parser.add_argument('file_pattern', type=str, help='file pattern')
    parser.add_argument('--show_lines', action='store_true',
                        help='Show lines')
    parser.add_argument('--only_show_counts', action='store_true',
                        help='Only show counts')
    args = parser.parse_args()

    try:
        print_matches(args.file_pattern, args.str_pattern,
                      args.only_show_counts, args.show_lines)
    except PermissionError:
        print("Permission denied. Please run with sudo.")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    main()
