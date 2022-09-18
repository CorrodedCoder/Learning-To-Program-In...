# Objective: count the number of unique words in a file, and the number of occurances of each of those words
# This version leverages python library functionality to replace hand written code
# See wordcount.MD for a critique of the solution.

import collections

## Return a list of all words found in the lines of text provided
def tokenize_words(lines):
    # Loop through each line
    for line in lines:
        # This string will keep track of characters found
        word = ''
        # Loop through each character in the line
        for character in line:
            # If the character is in the alphabet then add it to the word
            if character.isalpha():
                word += character
            else:
                # If the current character is not in the alphabet then
                # add any preceding alphabetic characters as a word
                if len(word) != 0:
                    yield word
                    # Prepare for the next word by resetting this to an empty string
                    word = ''
        # If the final characters in the text were not followed by whitespace
        # then we need to be sure to include this final word.
        if len(word) != 0:
            yield word


## Sort the words in decreasing order of frequency
def wordcount_lines(lines):
    ## Tokenize the words contained in the text lines and count them
    wordcounts = collections.Counter(tokenize_words(lines))

    ## Return the words in decreasing order of frequency
    return wordcounts.most_common()


if __name__ == '__main__':
    # Import the argparse module to process command line options
    import argparse

    # Create an argument parser object
    parser = argparse.ArgumentParser(description='Count occurances of each word in the input text')

    # Add a single argument which will open the file for reading text
    parser.add_argument('input', type=argparse.FileType('rt'))

    # Parse arguments
    args = parser.parse_args()

    wordcount_list_sorted = wordcount_lines(args.input)

    ## Output the list:

    # Loop through each pair in the sorted list
    for word, count in wordcount_list_sorted:
        # Output each item
        print('%s: %d' % (word, count))
