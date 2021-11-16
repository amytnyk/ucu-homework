"""
Module for archiving files that contain text that matches the pattern
"""
import argparse
import os
import re
import zipfile
from zipfile import ZipFile


def match(data: bytes, pattern: str) -> bool:
    """
    Check if data contain text that matches the pattern
    If bytes can't be decoded returns false
    """
    try:
        return re.search(pattern, data.decode(encoding='utf-8')) is not None
    except UnicodeDecodeError:
        return False  # probably file is binary


def all_files(path: str, pattern: str):
    """
    Yields all files at archived file that match the pattern
    """
    with ZipFile(path, 'r') as zip_file:
        for file in zip_file.infolist():
            file_bytes = zip_file.read(file.filename)
            if match(file_bytes, pattern):
                yield file.filename, file_bytes


def archive(src: str, dst: str, pattern: str):
    """
    Archive all files that match the pattern
    """
    dirname = os.path.dirname(dst)
    if len(dirname) > 0:
        os.makedirs(dirname, exist_ok=True)
    try:
        with ZipFile(dst, 'w') as zip_file:
            for filename, file_bytes in all_files(src, pattern):
                zip_file.writestr(filename, file_bytes)
    except zipfile.BadZipfile as e:
        os.remove(dst)  # clean up
        raise e


def main():
    """
    Main function for archiving
    usage: python project2_task3_a.py pattern src dst
    """
    parser = argparse.ArgumentParser(description='Archiver')
    parser.add_argument('pattern', type=str, help='pattern')
    parser.add_argument('src', type=str, help='path to source')
    parser.add_argument('dst', type=str, help='path to destination')
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
    except zipfile.BadZipfile:
        print("Specified source file is not zip file")


if __name__ == "__main__":
    main()
