# coding=utf-8
# Tool to extract sentences & words from a file.

from sys import argv

# import parser
# from parser import *

# Tool to count and score sentences and words.
from sys import argv

# A set of tools for debugging and creating Summarizer.

from sys import argv


def create_abbreviations():
    # Create the file abbreviations.txt.
    # Each abbreviation contains one period only, example: Mr. Mrs. Dr.
    reader = open("word_lists/words.txt")
    writer = open("word_lists/abbreviations.txt", "w")
    for line in reader:
        line = line[:-1]
        if line.endswith(".") and line.count(".") == 1:
            writer.write(line)
            writer.write("\n")
    reader.close()
    writer.close()


def create_abbreviations_multi():
    # Create the file abbreviations_multi.txt.
    # Each abbreviation contains multiple periods only, example: Y.M.C.A
    reader = open("word_lists/words.txt")
    writer = open("word_lists/abbreviations_multi.txt", "w")
    for line in reader:
        line = line[:-1]
        if line.endswith(".") and line.count(".") != 1:
            writer.write(line)
            writer.write("\n")
    reader.close()
    writer.close()


def print_usage():
    # Display the parameters.
    print('''
    Usage:
        tools.py [--options]

    Options:
        --create_abbr           create abbreviations.txt from words.txt
        --create_abbr_multi     create abbreviations_multi.txt from words.txt
    ''')


def handle_arguments():
    # Handle the command line arguments.
    if argv[1] == "--create_abbr":
        create_abbreviations()
    elif argv[1] == "--create_abbr_multi":
        create_abbreviations_multi()
    else:
        print_usage()


def get_word_scores(all_words):
    # Return a dictionary where the key is the word and the value is its count.
    file = open("word_lists/words_to_ignore.txt")
    words_to_ignore = file.read().split("\n")
    file.close()
    dictionary = {}
    for word in all_words:
        if word in words_to_ignore:
            continue
        count = 1
        if word in dictionary:
            count += dictionary.get(word)
        temp = {word: count}
        dictionary.update(temp)
    return dictionary


def score(sentence, word_scores):
    # The scoring algorithm.
    denominator = 1.0
    score = 0.0
    words = sentence.split(" ")
    for word in words:
        if word not in word_scores:
            continue
        if sentence.count(word) == 1:
            denominator += 1.0
        word = clean(word)
        score += word_scores.get(word)
    return score/denominator


def get_sentence_scores_dict(all_sentences, word_scores):
    # Return a dictionary where the key is the sentence and he value is its score.
    dictionary = {}
    for sentence in all_sentences:
        temp = {sentence: score(sentence, word_scores)}
        dictionary.update(temp)
    return dictionary


def get_sentence_scores_list(all_sentences, word_scores):
    # Return a list with the scores in the same order as the sentences.
    scores = []
    for sentence in all_sentences:
        scores.append(score(sentence, word_scores))
    return scores


def sort_dictionary(dictionary):
    # Sort the words from a dictionary in ascending order.
    sorted_ascending = sorted(dictionary, key=dictionary.__getitem__)
    sorted_descending = []
    for item in sorted_ascending:
        sorted_descending.insert(0, item)
    return sorted_descending


def print_popular(dictionary, sorted_items, top=10):
    # Print the most popular content in a dictionary, based on the order of sorted_items.
    if top >= len(sorted_items):
        top = len(sorted_items) - 1

    print("%-5s %-6s %-10s" % ("Rank:", "Score:", "Content:"))
    for i in range(0, top):
        word = sorted_items[i]
        count = dictionary.get(word)
        print("%5s %-6.1f %-10s" % ("#"+str(i+1)+".", count, word))


def x_highest_score(sentence_scores, x):
    # Find the xth highest score.
    list = []
    for score in sentence_scores:
        list.append(score)
    list.sort()
    return list[-x]


def top_sentences(all_sentences, sentence_scores, threshold):
    # Return the sentences chronologically which have equal to or above a certain score.
    result = []
    for i in range(0, len(all_sentences)):
        if sentence_scores[i] >= threshold:
            result.append(all_sentences[i])
    return result


def print_usage():
    # Print how to run the tool and use the parameters.
    print('''
    Usage:
        scoring.py <article.txt> <parameter> <quantity>

    Parameters:
        -s      print the top scoring sentences
        -w      print the top scoring words
    ''')


def handle_arguments():
    # Handle the command line arguments.
    if not argv[3].isdigit():
        print("The quantity parameter must be an integer.")
        return

    file = argv[1]
    parameter = argv[2]
    quantity = int(argv[3])

    if parameter != '-s' and parameter != '-w':
        print_usage()
        return

    words = get_words(file)
    words_scores = get_word_scores(words)
    sentences = get_sentences(file)
    sentences_scores = get_sentence_scores_dict(sentences, words_scores)

    if parameter == '-s':
        if quantity > len(sentences):
            print("Quantity specified is greater than the number of sentences.")
        else:
            print_popular(sentences_scores, sort_dictionary(sentences_scores), quantity)
    else:
        if quantity > len(words):
            print("Quantity specified is greater than the number of words.")
        else:
            print_popular(words_scores, sort_dictionary(words_scores), quantity)


if __name__ == '__main__':
    if len(argv) == 4:
        handle_arguments()
    else:
        print_usage()


# coding=utf-8
# Tool to trim and manipulate words and sentences.

from sys import argv


def comma_handler(sentences):
    # If a sentence starts with a comma it is probably part of the sentence before it.
    new_list = []
    skip = False
    for i in range(0, len(sentences)):
        if skip:
            skip = False
            continue
        if i+1 < len(sentences) and sentences[i+1][0] == ",":
            new_list.append(sentences[i] + sentences[i+1])
            skip = True
        else:
            new_list.append(sentences[i])
    return new_list


def group_quotes(sentences):
    # Quotes should be in a single sentence, even if there are periods in the quote.
    new_list = []
    skip = 0
    for i in range(0, len(sentences)):
        if skip > 0:
            skip -= 1
            continue
        sentence = sentences[i]
        while sentence.count("\"") % 2 == 1:
            skip += 1
            if i+skip >= len(sentences):
                break
            if sentences[i+skip][0].isalnum():
                sentence += " " + sentences[i+skip]
            else:
                sentence += sentences[i+skip]
        new_list.append(sentence)
    return new_list


def clean_up_quotes(sentences):
    # print sentences
    # If a quotation follows a period, make sure it is in the same sentence.
    generified = []
    for sentence in sentences:  # Convert fancy quotes to generic quotes.
        sentence = sentence.replace('“', '\"')
        sentence = sentence.replace('”', '\"')
        generified.append(sentence)

    new_list = [generified[0]]
    for i in range(1, len(generified)):
        sentence = generified[i]
        isolated_quotation = generified[i][0] == "\"" and generified[i][1] == " "
        quotation_with_period = generified[i][0] == "\"" and generified[i][1] == "."
        if isolated_quotation and quotation_with_period:
            sentence = sentence[2:]
            new_list[-1] += "\""
        new_list.append(sentence)
    return new_list


def add_periods(sentences):
    # Add a period to each element in the list.
    new_list = []
    for sentence in sentences:
        new_list.append(sentence + ".")
    return new_list


def remove_blanks(sentences):
    # Remove all empty elements.
    new_list = []
    for sentence in sentences:
        if sentence != "":
            new_list.append(sentence)
    return new_list


def fix_broken_sentences(sentences):
    # Combine sentences in a list where periods from abbreviations where
    # mistaken for the end of a sentence.
    file = open("word_lists/abbreviations.txt")
    abbreviations = str(file.read()).split("\n")
    file.close()

    new_list = []
    flag = False
    for i in range(0, len(sentences)):
        if flag:
            flag = False
            continue

        last_word = sentences[i].split(" ")[-1]
        last_word = remove_punctuation(last_word)
        last_word = to_singular(last_word)
        last_word = remove_punctuation(last_word)
        last_word += "."

        new_list.append(sentences[i])
        for abbreviation in abbreviations:
            if abbreviation == last_word:
                new_list[-1] += "." + sentences[i+1]
                flag = True
                break
    return new_list


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


def clean(word):
    # Remove punctuation from a word and convert it to lowercase singular.
    new_word = remove_punctuation(word)
    new_word = to_singular(new_word)
    new_word = remove_punctuation(new_word)
    new_word = str(new_word).lower()
    return new_word


def to_singular(word):
    # Convert a plural word to singular, otherwise return the original word.
    new_word = word
    if word.endswith("'s") or word.endswith("s'"):
        new_word = word[:-2]
    elif word.endswith("ies"):
        new_word = word[:-3] + "y"
    return new_word


def remove_punctuation(word):
    # Remove non alphabetic & non numeric letters on either side of a word.
    new_word = word
    while new_word is not "" and not str(new_word)[0].isalnum():
        new_word = new_word[1:]
    while new_word is not "" and not str(new_word)[-1].isalnum():
        new_word = new_word[:-1]
    return new_word


def remove_whitespace_list(sentences):
    # Remove whitespace on either side of each sentence in a list.
    new_list = []
    for sentence in sentences:
        new_list.append(remove_whitespace(sentence))
    return new_list


def remove_whitespace(word):
    # Remove whitespace on either side of the a word.
    new_word = word
    while new_word is not "" and str(new_word).startswith(" "):
        new_word = new_word[1:]
    while new_word is not "" and str(new_word).endswith(" "):
        new_word = new_word[:-1]
    return new_word


def print_usage():
    # Display the parameters.
    print('''
    Usage:
        parser.py <word> [--parameter]
        parser.py <sentence> [--parameter]

    Parameters for <word>:
        -a --abbreviation   remove all periods from an abbreviation
        -s --singular       convert most words to singular and remove ownership
        -p --punctuation    remove the surrounding punctuation
        -w --whitespace     remove the surrounding whitespace

    Parameters for <sentence>:
        -a --abbreviation   remove all periods from an abbreviation
    ''')


def word_parameter():
    # Handles the logic for when the user inputs two parameters where the first is a word.
    if argv[2] == "-a" or argv[2] == "--abbreviation":
        print(str(argv[1]).replace(".", ""))
    elif argv[2] == "-s" or argv[2] == "--singular":
        print(to_singular(argv[1]))
    elif argv[2] == "-p" or argv[2] == "--punctuation":
        print(remove_punctuation(argv[1]))
    elif argv[2] == "-w" or argv[2] == "--whitespace":
        print(remove_whitespace(argv[1]))
    else:
        print_usage()


def sentence_parameter():
    # Handles the logic for when a user inputs two parameters where the first is a sentence.
    if argv[2] == "-a" or argv[2] == "--abbreviation":
        print(convert_abbreviations_(argv[1]))
    else:
        print_usage()


def handle_two_parameters():
    if str(remove_whitespace(argv[1])).count(" ") == 0:
        word_parameter()
    else:
        sentence_parameter()


if __name__ == "__main__":
    if len(argv) == 3:
        handle_two_parameters()
    else:
        print_usage()


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
