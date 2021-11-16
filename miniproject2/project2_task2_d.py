"""
Module for copying files from src to dst
"""
import argparse
import os


def copy_file(src: str, dst: str):
    """
    Copy file from src to dst
    """
    with open(dst, 'wb') as file:
        with open(src, 'rb') as original_file:
            file.write(original_file.read())


def get_dest_path(src: str, dst: str, srcpath: str):
    """
    Returns dest path
    >>> get_dest_path('../srcfolder/', '../../destdir', '../srcfolder/hi.txt')
    '../../destdir/hi.txt'
    """
    return os.path.normpath(os.path.join(dst, os.path.relpath(srcpath, src)))


def copy_tree(src: str, dst: str):
    """
    Copy files from src to dst
    """
    for subdir, dirs, files in os.walk(src):
        os.makedirs(get_dest_path(src, dst, subdir), exist_ok=True)
        for file in files:
            src_path = os.path.join(subdir, file)
            dest_path = get_dest_path(src, dst, src_path)
            copy_file(src_path, dest_path)


def main():
    """
    Main function for copying files
    usage: python project2_task2_d.py src dst
    """
    parser = argparse.ArgumentParser(description='Copy files')
    parser.add_argument('src', type=str, help='path to source')
    parser.add_argument('dst', type=str, help='path to destination')
    args = parser.parse_args()

    if not os.path.isdir(args.src):
        print("Directory was not found at the specified src path")
    else:
        try:
            copy_tree(args.src, args.dst)
        except PermissionError:
            print("Permission denied. Please run with sudo.")


if __name__ == "__main__":
    main()
