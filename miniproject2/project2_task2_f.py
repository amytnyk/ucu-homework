"""
Module for searching plain-text data sets for lines that match a regex.
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


def search_lines(path: str, search_pattern: str) -> Dict[int, str]:
    """
    (str, str) -> Dict[line_number, line]
    Returns all lines in file, located at path, which contain pattern
    """
    try:
        matched_lines = dict()
        with open(path, 'r') as file:
            lines = file.readlines()
            for idx, line in enumerate(lines):
                if re.search(search_pattern, line) is not None:
                    matched_lines[idx + 1] = line.strip()
        return matched_lines
    except (PermissionError, UnicodeDecodeError, Exception):
        return dict()  # Maybe access to file is restricted or it's binary


def match(file_pattern: str, search_pattern: str) -> Dict[str, Dict[int, str]]:
    """
    (str, str) -> Dict[filename, Dict[line_number, line]]
    Returns all files that have matched lines
    """
    matches = dict()
    for file in get_matched_files(file_pattern):
        lines = search_lines(file, search_pattern)
        if len(lines) > 0:
            matches[file] = lines
    return matches


def get_colorcode_by_str(color: str) -> int:
    """
    Return terminal colorcode by color string name
    >>> get_colorcode_by_str('red')
    31
    """
    if color == 'green':
        return 32
    elif color == 'red':
        return 31
    elif color == 'blue':
        return 34
    return 37


def make_colored(text: str, color: str, bold: bool) -> str:
    """
    Returns colored text
    >>> make_colored('Ukrainian Catholic University', 'green', True)
    '\\x1b[1;32mUkrainian Catholic University\\x1b[0m'
    """
    return f"\033[{int(bold)};{get_colorcode_by_str(color)}m{text}\033[0m"


def highlight_match(line: str, search_pattern: str) -> str:
    """
    Highlights matched pattern in line with red color
    >>> highlight_match("Romanyuk TOP, but python sucks", 'o')
    'R\\x1b[1;31mo\\x1b[0mmanyuk TOP, but pyth\\x1b[1;31mo\\x1b[0mn sucks'
    """
    return re.sub(search_pattern,
                  lambda x: make_colored(x.group(), 'red', True), line)


def print_matches(file_pattern: str, search_pattern: str, count_only: bool,
                  show_lines: bool):
    """
    Prints all matches
    """
    matches = match(file_pattern, search_pattern)

    for filename, matched_lines in matches.items():
        print(make_colored(filename, 'blue', True), end='')
        if count_only:
            print(f': {len(matched_lines)}')
        else:
            print()  # make newline
            for line_number, line in matched_lines.items():
                if show_lines:
                    print(make_colored(str(line_number), 'green', False),
                          end=': ')
                print(highlight_match(line, search_pattern))


def main():
    """
    Main function for searching text aka grep
    usage: python project2_task2_f.py str_pattern file_pattern [show_lines]\
    [only_show_counts]
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
    main()
