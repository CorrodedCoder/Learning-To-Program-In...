# Objective: count the number of unique words in a file, and the number of occurances of each of those words
# This version adds structure to the solution in the form of functions but
# remains relatively simplistic.
# See wordcount.MD for a critique of the solution.

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


## Given a list of words, return a count of each words in the form of a
## dictionary, where the key is the word and the value is the count
def count_words(words):
    # Create a dictionary to record each word (the key) and the number of times it appears (the value)
    wordcounts = {}

    # Loop through each word
    for word in words:
        # Has the word already been seen?
        if word not in wordcounts:
            # The word is not in the dictionary, so add it with a count of one
            wordcounts[word] = 1
        else:
            # The word is in the dictionary, so increase the count by one
            wordcounts[word] += 1

    return wordcounts


## Sort the words in decreasing order of frequency
def wordcount_lines(lines):
    ## Tokenize the words contained in the text lines and count them
    wordcounts = count_words(tokenize_words(lines))

    ## Sort the words in decreasing order of frequency

    # Create a list of pairs of word and count based on the dictionary items
    wordcount_list = wordcounts.items()

    # Use the "sorted" algorithm to produce a new list of pairs sorted in reverse order
    # using the count element of each pair as a key.
    # (ignore the lambda syntax at this point, we are just telling the "sorted"
    # algorithm to sort the items based on the second element of each item,
    # which is the count)
    wordcount_list_sorted = sorted(wordcount_list, reverse=True, key=lambda pair: pair[1])

    return wordcount_list_sorted


def wordcount_file(filename):
    ## Read the contents of the file into a list of lines

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
