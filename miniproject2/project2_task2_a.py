"""
Module for printing directory contents as tree
"""
import argparse
import os
import posix


def get_display_name(path: str) -> str:
    """
    Returns entry name
    >>> get_display_name("/home/")
    'home'
    """
    return os.path.basename(os.path.abspath(path))


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


def print_styled(path: str):
    """
    Prints styled entry name
    White - regular files
    Blue - directory
    Green - executable
    Symlink displayed as file1 -> file2
    """
    display_name = get_display_name(path)
    color = ''
    bold = '1'
    if os.path.isdir(path):
        color = '34'
    elif os.path.islink(path):
        display_name += " -> " + os.readlink(path)
        color = '32'
    else:
        bold = '0'
    print(f"\033[{bold};{color}m{display_name}\033[0m")


def print_tree(path: str, prefix: str = "") -> (int, int):
    """
    Prints directory contents as a tree
    """
    directories_count = 0
    files_count = 0
    print_styled(path)
    if os.path.isdir(path):
        directories_count = 1
        entries = sorted(os.listdir(path), key=lambda x: x)
        for idx, entry in enumerate(entries):
            will_be_last = idx == len(entries) - 1
            new_prefix = get_new_prefix(prefix, will_be_last)
            print(get_entry_header(prefix, will_be_last), end='')
            dirs, files = print_tree(os.path.join(path, entry), new_prefix)
            directories_count += dirs
            files_count += files
    else:
        files_count = 1
    return directories_count, files_count


def tree(path) -> list[str]:
    lst = [entryname_of(path)]
    if isdir(path):
        for entry in dir(path):
            sublist = tree(entry)
            sublist[0] = ('└── ' if is_last_entry_in_dir else '├── ') + sublist[0]
            for i in range(1, len(sublist)):
                sublist[i] = ('    ' if is_last_entry_in_dir else '|   ') + sublist[i]
            lst.extend(sublist)
    return lst

print('\n'.join(tree('some/path')))

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
            directories_count, files_count = print_tree(args.path)
            print(f"{directories_count - 1} directories, {files_count} files")
        except PermissionError:
            print("Permission denied. Please run with sudo.")
        except FileNotFoundError:
            print("\nCannot found some file, maybe lack of permissions.")
    else:
        print("Directory was not found at the specified path")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    main()
