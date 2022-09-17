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


def wordcount_file(filename):
    # Open the file for reading
    # Specify text mode so that the file object knows to make sense of line endings
    with open(filename, 'rt') as input:
        return wordcount_lines(input)


if __name__ == '__main__':
    # Import the sys module to provide access to command line arguments
    import sys

    if len(sys.argv) != 2:
        print('Usage: <filename>\n Where <filename> is the text file from which we will count the words')
        exit()

    wordcount_list_sorted = wordcount_file(sys.argv[1])

    ## Output the list:

    # Loop through each pair in the sorted list
    for word, count in wordcount_list_sorted:
        # Output each item
        print('%s: %d' % (word, count))
