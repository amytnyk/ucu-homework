"""
Target game implementation
"""
from typing import List
import random
import sys


def get_random_char():
    """
    Generate random char
    """
    return chr(random.randint(ord('A'), ord('Z')))


def generate_grid() -> List[List[str]]:
    """
    Generates list of lists of letters - i.e. grid for the game.
    e.g. [['I', 'G', 'E'], ['P', 'I', 'S'], ['W', 'M', 'G']]
    """
    return [[get_random_char() for j in range(3)] for i in range(3)]


def get_words(filename: str, letters: List[str]) -> List[str]:
    """
    Reads the file f. Checks the words with rules and returns a list of words.
    """
    words = []
    with open(filename, 'r') as file:
        for word in file.read().split('\n'):
            word = word.lower()
            if is_eligible(word, letters):
                words.append(word)
    return list(set(words))


def get_user_words() -> List[str]:
    """
    Gets words from user input and returns a list with these words.
    Usage: enter a word or press ctrl+d to finish.
    """
    return [line for line in sys.stdin]


def is_eligible(word: str, letters: List[str]) -> bool:
    """
    Check if word can be created from letters
    """
    for char in word:
        if word.count(char) > letters.count(char):
            return False
    return len(word) >= 4 and letters[4] in word


def get_pure_user_words(user_words: List[str], letters: List[str],
                        words_from_dict: List[str]) -> List[str]:
    """
    (list, list, list) -> list

    Checks user words with the rules and returns list of those words
    that are not in dictionary.
    """
    return list(
        filter(lambda x: is_eligible(x, letters) and x not in words_from_dict,
               user_words))


def results():
    """
    print game results
    """
