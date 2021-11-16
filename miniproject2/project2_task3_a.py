"""
Module for archiving files that match the pattern
"""
import argparse
import os
import re
from zipfile import ZipFile


def match(data: bytes, pattern: str) -> bool:
    """
    Check if data contain text that matches the pattern
    If bytes can't be decoded returns false
    """
    try:
        return re.search(pattern, data.decode(encoding='utf-8')) is not None
    except UnicodeDecodeError:
        return False


def all_files(path: str, pattern: str):
    """
    Yields all files at archived file that match the pattern
    """
    with ZipFile(path, 'r') as zipfile:
        for file in zipfile.infolist():
            file_bytes = zipfile.read(file.filename)
            if match(file_bytes, pattern):
                yield file.filename, file_bytes


def archive(src: str, dst: str, pattern: str):
    """
    Archive all files that match the pattern
    """
    dirname = os.path.dirname(dst)
    if len(dirname) > 0:
        os.makedirs(dirname, exist_ok=True)
    with ZipFile(dst, 'w') as zipfile:
        for filename, file_bytes in all_files(src, pattern):
            zipfile.writestr(filename, file_bytes)


def main():
    """
    Main function for archiving
    """
    parser = argparse.ArgumentParser(description='Archiver')
    parser.add_argument('src', type=str, help='path to source')
    parser.add_argument('dst', type=str, help='path to destination')
    parser.add_argument('pattern', type=str, help='pattern')
    args = parser.parse_args()

    try:
        if os.path.exists(args.src):
            archive(args.src, args.dst, args.pattern)
        else:
            print("Cannot find any file or directory in specified source path")
    except PermissionError:
        print("Permission denied. Please run with sudo.")
    except IsADirectoryError:
        print("Specified destination is not a valid path")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    main()