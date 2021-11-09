"""
Module for printing directory contents as tree
"""
import argparse
import os


def get_display_name(path: str) -> str:
    """
    Returns entry name
    >>> get_display_name("/home/")
    'home/'
    """
    entry_name = os.path.basename(os.path.abspath(path))
    if os.path.isdir(path):
        entry_name += "/"
    return entry_name


def get_new_prefix(prefix: str, is_last_entry: bool) -> str:
    """
    Returns new prefix
    >>> get_new_prefix("", True)
    '    '
    >>> get_new_prefix("│   ", False)
    '│   │   '
    """
    separator = '│'
    if is_last_entry:
        separator = ' '
    return f"{prefix}{separator}   "


def get_entry_header(prefix: str, will_be_last: bool):
    """
    Return entry header
    >>> get_entry_header('│   │   ', True)
    '│   │   └── '
    """
    ending = '├── '
    if will_be_last:
        ending = '└── '
    return prefix + ending


def print_tree(path: str, prefix: str = ""):
    """
    Prints directory contents as a tree
    """
    print(get_display_name(path))

    if os.path.isdir(path):
        entries = os.listdir(path)
        for idx, entry in enumerate(entries):
            will_be_last = idx == len(entries) - 1
            new_prefix = get_new_prefix(prefix, will_be_last)
            print(get_entry_header(prefix, will_be_last), end='')
            print_tree(os.path.join(path, entry), new_prefix)


def main():
    """
    Main function
    """
    parser = argparse.ArgumentParser(
        description='Prints directory contents as a tree')
    parser.add_argument('path', type=str, help='path to directory')
    args = parser.parse_args()

    if os.path.isdir(args.path):
        try:
            print_tree(args.path)
        except PermissionError:
            print("Permission denied. Please run with sudo.")
    else:
        print("Directory was not found at the specified path")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    main()
