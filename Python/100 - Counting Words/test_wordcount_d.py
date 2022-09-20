import unittest
import sys

import wordcount_d

if sys.version_info.major == 2:
    import itertools
    import operator

    def reorder(wordcounts):
        return list(wordcount for _, group in itertools.groupby(wordcounts, key=operator.itemgetter(1)) for wordcount in sorted(group))
else:
    def reorder(wordcounts):
        return wordcounts


class TestTokenizeWords(unittest.TestCase):
    def test_single_line(self):
        self.assertEqual(list(wordcount_d.tokenize_words(["My name is, my name is, my name is... Skinny Shadowy!"])),
            ['My', 'name', 'is', 'my', 'name', 'is', 'my', 'name', 'is', 'Skinny', 'Shadowy'])

    def test_leading_and_trailing_nonwords(self):
        self.assertEqual(list(wordcount_d.tokenize_words([".one two, three,"])),
            ['one', 'two', 'three'])


class TestWordcountLines(unittest.TestCase):
    def test_single_line(self):
        self.assertSequenceEqual(wordcount_d.wordcount_lines([
            "Mango, Mango, Banana, Mango, Banana, Apple",
            ]), [('Mango', 3), ('Banana', 2), ('Apple', 1)])

    def test_single_line2(self):
        self.assertSequenceEqual(reorder(wordcount_d.wordcount_lines([
            "My name is, my name is, my name is... Skinny Shadowy!",
            ])), reorder([('name', 3), ('is', 3), ('my', 2), ('My', 1), ('Skinny', 1), ('Shadowy', 1)]))

    def test_multiple_lines(self):
        self.assertSequenceEqual(reorder(wordcount_d.wordcount_lines([
            "There ", "can,", " be ", " only", "one!", ""
            ])), reorder([('There', 1), ('can', 1), ('be', 1), ('only', 1), ('one', 1)]))


if __name__ == '__main__':
    unittest.main()
