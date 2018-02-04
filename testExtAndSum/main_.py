# The highest level code that brings everything together.

# import filter, scoring, extractor
from filter import *
from scoring import *
from extractor import *

def print_usage():
    # Display the parameters and what they mean.
    print('''
    Usage:
        main.py <article.txt> <summary length>

    Explanation:
        Parameter 1: the location and name of the text to summarize
        Parameter 2: the number of sentences for the summary to contain
    ''')


def summarize(str_, num_of_sentences):
    # Summarize a file. The length of the summary will be the number of sentences specified.
    # file = filename

    # Extract all the words and sentences and get their respective scores.
    all_words = get_words_(str_)
    word_scores = get_word_scores(all_words)
    all_sentences = get_sentences_(str_)
    all_sentences = omit_transition_sentences(all_sentences)
    sentence_scores = get_sentence_scores_list(all_sentences, word_scores)

    if num_of_sentences > len(all_sentences):
        print("The summary cannot be longer than the text.")
        return

    # Get x sentences with the highest scores, in chronological order.
    threshold = x_highest_score(sentence_scores, num_of_sentences)
    top_sentence = top_sentences(all_sentences, sentence_scores, threshold)

    # Put the top sentences into one string.
    summary = ""
    for sentence in top_sentence:
        summary += sentence + " "
    summary = summary[:-1]
    print(summary)
    return summary


if __name__ == '__main__':
    # if len(argv) != 3:
    #     print_usage()
    # elif not str(argv[2]).isdigit():
    #     print_usage()
    # else:
    #     summarize(argv[1], int(argv[2]))
    summarize('sample_articles/test.txt', 2)
