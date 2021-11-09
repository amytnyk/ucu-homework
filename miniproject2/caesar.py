"""
Module for caesar encryption/decryption
"""
import argparse


def shift_char(char: str, starting_char: str, offset: int) -> str:
    """
    Shift char by offset
    >>> shift_char('y', 'a', 3)
    'b'
    >>> shift_char('C', 'A', -4)
    'Y'
    """
    char_idx = ord(char) + offset - ord(starting_char)
    if char_idx < 0:
        char_idx = 26 + char_idx % 26
    return chr(char_idx % 26 + ord(starting_char))


def transform_char(char: str, offset: int) -> str:
    """
    Transform char by offset
    >>> transform_char('Y', 3)
    'B'
    >>> transform_char('a', -3)
    'x'
    >>> transform_char('&', 16)
    '&'
    """
    if 'a' <= char <= 'z':
        return shift_char(char, 'a', offset)
    elif 'A' <= char <= 'Z':
        return shift_char(char, 'A', offset)
    return char


def shift_data(text: str, offset: int) -> str:
    """
    Shift data with offset
    >>> shift_data('abcdefz', 1)
    'bcdefga'
    >>> shift_data('bcdefgA', -1)
    'abcdefZ'
    >>> shift_data(shift_data('@#$%^&*(llhji', 17), -17)
    '@#$%^&*(llhji'
    """
    return ''.join([transform_char(char, offset) for char in text])


def encrypt(text: str, offset: int) -> str:
    """
    Encrypt data with offset
    >>> encrypt('abcdefz', 1)
    'bcdefga'
    """
    return shift_data(text, offset)


def decrypt(text: str, offset: int) -> str:
    """
    Decrypt data with offset
    >>> decrypt('bcdefga', 1)
    'abcdefz'
    """
    return shift_data(text, -offset)


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


def non_negative_int(arg):
    """
    Type function for argparse - a non-negative integer
    """
    try:
        val = int(arg)
    except ValueError:
        raise argparse.ArgumentTypeError("Must be an integer value")
    if val < 0:
        raise argparse.ArgumentTypeError("Argument must be non-negative")
    return val


def main():
    """
    Main function
    """
    parser = argparse.ArgumentParser(description='Caesar encryption/decryption')
    parser.add_argument('path', type=str, help='path to file')
    parser.add_argument('--offset', type=non_negative_int,
                        default=13, help='Offset')
    parser.add_argument('--decrypt', action='store_true',
                        help='Decrypt instead of encrypt')
    parser.add_argument('--inplace', action='store_true',
                        help='Encrypt/Decrypt in place')

    args = parser.parse_args()

    try:
        text = get_text_from_file(args.path)
        if args.decrypt:
            text = decrypt(text, args.offset)
        else:
            text = encrypt(text, args.offset)
        if args.inplace:
            write_text_to_file(args.path, text)
        else:
            print(text)
    except FileNotFoundError:
        print("File at the specified path was not found")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    main()
