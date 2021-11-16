"""
Module for substring replacing
"""
import argparse


def get_text_from_file(path: str) -> str:
    """
    Get text from file
    """
    with open(path, 'r', encoding='utf-8') as file:
        return file.read()


def write_text_to_file(path: str, text: str):
    """
    Write text from file
    """
    with open(path, 'w', encoding='utf-8') as file:
        return file.write(text)


def replace_substring(old: str, new: str, text: str):
    """
    Replace old substrings with new
    >>> replace_substring('ab', '!', 'bbabbbaaab')
    'bb!bbaa!'
    """
    return text.replace(old, new)


def main():
    """
    Main function for substring replacing
    Usage: python project2_task1_b.py old_string new_string path [--inplace]
    """
    parser = argparse.ArgumentParser(description='Substring replacing')
    parser.add_argument('old', type=str, help='substring to be replaced')
    parser.add_argument('new', type=str, help='substring to be replaced with')
    parser.add_argument('path', type=str, help='path to file')
    parser.add_argument('--inplace', action='store_true',
                        help='Replace in place')

    args = parser.parse_args()

    try:
        text = get_text_from_file(args.path)
        text = replace_substring(args.old, args.new, text)

        if args.inplace:
            write_text_to_file(args.path, text)
        else:
            print(text)
    except FileNotFoundError:
        print("File at the specified path was not found")
    except IsADirectoryError:
        print("Please specify path to the file, not a directory")
    except PermissionError:
        print("Insufficient permissions to access file")
    except UnicodeDecodeError:
        print("Decoding error, maybe specified file is binary")


if __name__ == "__main__":
    main()
