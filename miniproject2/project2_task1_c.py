"""
Module for caesar encryption/decryption
>>> a = "LoReM IpSum Та ШоСЬ таМ!!!!"
>>> offset = 777 # can be any integer
>>> decrypt(encrypt(a, offset), offset) == a
True
"""
import argparse

alphabets = [
    'абвгґдеєжзиіїйклмнопрстуфхцчшщьюя',
    'abcdefghijklmnopqrstuvwxyz'
]


def normalize_idx(idx: int, alphabet_len: int):
    """
    Normalizes char index, so that idx will be in [0;alphabet_len)
    >>> normalize_idx(28, 26)
    2
    >>> normalize_idx(-2, 26)
    24
    """
    if idx < 0:
        idx = alphabet_len + idx % alphabet_len
    return idx % alphabet_len


def shift_char(char: str, offset: int) -> str:
    """
    Shift char by offset
    >>> shift_char('y', 3)
    'b'
    >>> shift_char('C', -4)
    'Y'
    >>> shift_char('ш', -4)
    'ф'
    """
    for alphabet in alphabets:
        if char.lower() in alphabet:
            is_upper = char.isupper()
            new_char_idx = alphabet.index(char.lower()) + offset
            shifted_char = alphabet[normalize_idx(new_char_idx, len(alphabet))]
            if is_upper:
                shifted_char = shifted_char.upper()
            return shifted_char
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
    return ''.join([shift_char(char, offset) for char in text])


def encrypt(text: str, offset: int) -> str:
    """
    Encrypt data with offset
    >>> encrypt('abcdefz', 1)
    'bcdefga'
    >>> encrypt('УКУ', 1)
    'ФЛФ'
    """
    return shift_data(text, offset)


def decrypt(text: str, offset: int) -> str:
    """
    Decrypt data with offset
    >>> decrypt('bcdefga', 1)
    'abcdefz'
    >>> decrypt('ЛО', 1)
    'КН'
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
    >>> non_negative_int("56")
    56
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
    Main function for caesar encryption/decryption
    Usage: python project2_task1_c.py path [--offset] [--decrypt] [--inplace]
    """
    parser = argparse.ArgumentParser(
        description='Caesar encryption/decryption')
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
    except IsADirectoryError:
        print("Please specify path to file, not a directory")
    except PermissionError:
        print("Insufficient permissions to access file")
    except UnicodeDecodeError:
        print("Decoding error, maybe specified file is binary")


if __name__ == "__main__":
    main()
