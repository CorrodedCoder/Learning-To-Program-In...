# Objective: count the number of unique words in a file, and the number of occurances of each of those words
# This version aims to show the simplest to understand implementation of this and pays no attention to doing
# things in the most efficient (or even the most sensible) way.
# See wordcount.MD for a critique of the solution.

# Import the sys module to provide access to command line arguments
import sys

if len(sys.argv) != 2:
    print('Usage: <filename>\n Where <filename> is the text file from which we will count the words')
    exit()

filename = sys.argv[1]

## Read the contents of the file into a list of lines

# Open the file for reading
# Specify text mode so that the file object knows to make sense of line endings
input = open(filename, 'rt')

# Read all lines of the file into a list
lines = input.readlines()

## All words found in the file contents will be added to a list

# Create an empty list to record each word found
words = []

# Loop through each line
for line in lines:
    # This string will keep track of characters found
    word = ''
    # Loop through each character in the line
    for character in line:
        # If the character is in the alphabet then add it to the word
        if character.isalpha():
            word = word + character
        else:
            # If the current character is not in the alphabet then
            # add any preceding alphabetic characters as a word
            if len(word) != 0:
                words.append(word)
                # Prepare for the next word by resetting this to an empty string
                word = ''
    # If the final characters in the text were not followed by whitespace
    # then we need to be sure to include this final word.
    if len(word) != 0:
        words.append(word)

## We now have a list of all the words in the file so let's count them

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
        wordcounts[word] = wordcounts[word] + 1

## Sort the words in decreasing order of frequency

# Create a list of pairs of word and count based on the dictionary items
wordcount_list = wordcounts.items()

# Use the "sorted" algorithm to produce a new list of pairs sorted in reverse order
# using the count element of each pair as a key.
# (ignore the lambda syntax at this point, we are just telling the "sorted"
# algorithm to sort the items based on the second element of each item,
# which is the count)
wordcount_list_sorted = sorted(wordcount_list, reverse=True, key=lambda pair: pair[1])

## Output the list:

# Loop through each pair in the sorted list
for word, count in wordcount_list_sorted:
    # Output each item
    print('%s: %d' % (word, count))
