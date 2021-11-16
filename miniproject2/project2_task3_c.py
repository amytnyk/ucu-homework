"""
Module for archiving
"""
import argparse
import os
from zipfile import ZipFile


def all_files(path: str):
    """
    Yields all files at specified path
    """
    if os.path.isfile(path):
        yield path
    else:
        for subdir, dirs, files in os.walk(path):
            for file in files:
                yield os.path.join(subdir, file)


def archive(src: str, dst: str):
    """
    Zip src and save to dst
    """
    src_dir = os.path.dirname(src) if os.path.isfile(src) else src
    with ZipFile(dst, 'w') as zipfile:
        for file in all_files(src):
            if os.path.abspath(file) != os.path.abspath(dst):
                zipfile.write(file, os.path.relpath(file, src_dir))


def main():
    """
    Main function for archiving
    usage: python project2_task3_c.py src dst
    """
    parser = argparse.ArgumentParser(description='Archiver')
    parser.add_argument('src', type=str, help='path to source')
    parser.add_argument('dst', type=str, help='path to destination')
    args = parser.parse_args()

    try:
        if os.path.exists(args.src):
            archive(args.src, args.dst)
        else:
            print("Cannot find any file or directory in specified source path")
    except PermissionError:
        print("Permission denied. Please run with sudo.")
    except IsADirectoryError:
        print("Specified destination is not a valid path")


if __name__ == "__main__":
    main()
