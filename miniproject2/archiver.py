"""
Module for printing directory contents as tree
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
    with ZipFile(dst, 'w') as zipfile:
        for file in all_files(src):
            zipfile.write(file)


def main():
    """
    Main function
    """
    parser = argparse.ArgumentParser(description='Archiver')
    parser.add_argument('src', type=str, help='path to source')
    parser.add_argument('dst', type=str, help='path to destination')
    args = parser.parse_args()

    try:
        archive(args.src, args.dst)
    except PermissionError:
        print("Permission denied. Please run with sudo.")
    except IsADirectoryError:
        print("Specified destination is not a valid path")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    main()
