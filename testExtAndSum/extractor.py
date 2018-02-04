# Tool to extract sentences & words from a file.

from sys import argv

# import parser
from parser import *

def get_sentences(file_name):
    # Extract sentences from a text file.
    reader = open(file_name)
    sentences = reader.read()
    reader.close()
    sentences = sentences.replace("\n", "")
    sentences = convert_abbreviations_(sentences)
    sentences = sentences.replace("?", ".")
    sentences = sentences.replace("!", ".")
    sentences = sentences.split(".")
    sentences = fix_broken_sentences(sentences)
    sentences = remove_whitespace_list(sentences)
    sentences = remove_blanks(sentences)
    sentences = add_periods(sentences)
    sentences = clean_up_quotes(sentences)
    sentences = group_quotes(sentences)
    sentences = comma_handler(sentences)
    return sentences


def get_words(file_name):
    # Extract words from a text file. Clean the words by removing surrounding
    # punctuation and whitespace, and convert the word to singular.
    reader = open(file_name)
    words = reader.read()
    reader.close()
    words = words.replace("\n", " ")
    words = convert_abbreviations_(words)
    words = words.split(" ")
    words = remove_blanks(words)
    for i in range(0, len(words)):
        words[i] = clean(words[i])
    return words


def get_sentences_(str_):
    # Extract sentences from a text file.
    # reader = open(file_name)
    sentences = str_
    # reader.close()
    sentences = sentences.replace("\n", "")
    sentences = convert_abbreviations_(sentences)
    sentences = sentences.replace("?", ".")
    sentences = sentences.replace("!", ".")
    sentences = sentences.split(".")
    sentences = fix_broken_sentences(sentences)
    sentences = remove_whitespace_list(sentences)
    sentences = remove_blanks(sentences)
    sentences = add_periods(sentences)
    sentences = clean_up_quotes(sentences)
    sentences = group_quotes(sentences)
    sentences = comma_handler(sentences)
    return sentences


def convert_abbreviations_(string):
    # Remove all periods in all multi period abbreviations. Example: Y.M.C.A -> YMCA
    file = open("word_lists/abbreviations_multi.txt")
    abbreviations = str(file.read()).split("\n")
    file.close()
    new_string = string
    abbreviations_in_string = []

    # Get all the abbreviations that are in the string.
    for abbreviation in abbreviations:
        if abbreviation in string:
            abbreviations_in_string.append(abbreviation)

    # Sort the abbreviations from longest to shortest.
    # Some abbreviations overlap so its important to check the longest ones first.
    # Example: "Y.M.C.A." contains "M.C." and "C.A." and "Y.M.C.A". If the "C.A."
    # is handled first then it becomes "Y.M.CA", which is incorrect.
    abbreviations_in_string.sort(key=str.__len__)
    abbreviations_in_string.reverse()

    for abbreviation in abbreviations_in_string:
        if abbreviation in new_string:
            # new_string = str(new_string.encode('utf-8')).replace(abbreviation, abbreviation.replace(".", ""))
            new_string = str(new_string).replace(abbreviation, abbreviation.replace(".", ""))
    return new_string


def get_words_(str_):
    # Extract words from a text file. Clean the words by removing surrounding
    # punctuation and whitespace, and convert the word to singular.
    # reader = open(file_name)
    words = str_
    # reader.close()
    words = words.replace("\n", " ")
    words = convert_abbreviations_(words)
    words = words.split(" ")
    words = remove_blanks(words)
    for i in range(0, len(words)):
        words[i] = clean(words[i])
    return words


def print_usage():
    # Print how to run the tool and use the parameters.
    print('''
    Usage:
        extractor.py <article.txt> [parameter]

    Parameters:
        -i --info       display basic info about <article.txt>
        -s --sentences  extract sentences from <article.txt>
        -w --words      extract words from <article.txt>
    ''')


def handle_arguments():
    # Handle the command line arguments.
    if argv[2] == "-i" or argv[2] == "--info":
        print("Sentence count: %6d" % len(get_sentences(argv[1])))
        print("Word count:     %6d" % len(get_words(argv[1])))
    elif argv[2] == "-s" or argv[2] == "--sentences":
        sentences = get_sentences(argv[1])
        for sentence in sentences:
            print(sentence)
    elif argv[2] == "-w" or argv[2] == "--words":
        words = get_words(argv[1])
        for word in words:
            print(word)
    else:
        print_usage()


if __name__ == "__main__":
    if len(argv) == 3:
        handle_arguments()
    else:
        print_usage()
