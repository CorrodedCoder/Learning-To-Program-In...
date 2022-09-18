# Objective: count the number of unique words in a file, and the number of occurances of each of those words
# This version leverages python library functionality to replace hand written code
# See wordcount.MD for a critique of the solution.

import collections

## Return a list of all words found in the lines of text provided
def tokenize_words(lines):
    for line in lines:
        # split the input line according to the regular expression criteria we specify:
        #   \W is a metacharacter which means: match any one non-word character
        #   + following the \W changes the meaning to match one or more non-word characters
        # The `r` preceeding the string tells python this is a raw string and so not to interpret characters
        # (such as the backslash) specially.
        for word in re.split(r'\W+', line):
            # The split will return empty strings where the start or end of the line has non word characters
            # so we check we have a word with characters in it before yielding it
            if word:
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
