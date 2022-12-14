# Critique of wordcount_a.py
The solution addresses the objectives set out for it, but would almost certainly would have triggered a number of responses from a seasoned python developer at code review, however let's not forget that in this example we're trying to introduce someone new to python, and possibly programming, and so a number of obvious simplifications were avoided. Let's start by going through the most obvious simplification.

## X = X + Y
In cases where we are simply adding to an existing variable, whether that be incrementing a numeric value or adding a character to a string, we can use a shorthand syntax:  
`word = word + character`  
Can instead be expressed using a simpler notation:  
`word += character`  
This is true for many operations across python.

## It's just a sequence of commands - there is no structure!
Indeed, in many ways it is very similar to what one might see in a simple dos batchfile or Unix shell script: a sequence of commands to be executed in order. Is that so bad? Well, not always. In fact python works very well as a cross platform replacement for scripts of commands, but in this particular case, as I think is somewhat evidenced by the section comments, the lack of structure means that someone looking at the code needs to read the entire thing to deduce what the code is doing and so that takes time and effort that could otherwise be avoided. They also need to consider every variable is at global scope which makes it hard to reason what happened to it beforehand that might by impacting later code.

The other problem with the lack of structure is that another author might want to solve a similar problem and be able to leverage much of the functionality here but to do so they would need to copy and paste that shared code into their own script. This is usually what is known as a bad thing. Why? Bug's fixed in one may not be propogated into the other. The fact that most of the code is identical should be an aid as someone who has looked at the source of one should have a head start on the other, but because it has been copy pasted this is not possible to do with any confidence as many subtle changes may have been made.

The final problem is that in this form have to test the functionality it in its entirety. Whilst we can test that the script does what we think it does by comparing against prior output for a given input is correct (although this might throw some suprises when using different versions of python) what we cannot do is test individual parts of the script.

The most obvious solution to all of this is to add some structure in the form of functions and, to allow other scripts to use functions from our script, to follow a convention of only executing the full functionality of the script if it is the launched script (the one passed to python). This is accomplished in like so:  
```
if __name__ == '__main__':
  <your code follows>
```
If this script is imported by any other, it will not execute the code inside the if statement.  

The script wordcount_b.py contains the changes described above.

# Critique of wordcount_b.py
The second incarnation of the script is already looking much better and specifically looking at the chief function of the script `wordcount_lines` we can hope that some person new to that code might have some vague idea of what we're trying to do:
1. Tokenize words.
2. Count words.
3. Sort in descending order of counts.

Also another developer may be able to leverage some or all of the functionality contained in this script by importing it and using the functionality it needs, or even just choose to display the information in a different format.  
However there is still much which could be improved here.

## The file object is not explicitly closed
In the original solution this *probably* wouldn't have mattered but now that we are offering this functionality to others we have to be a little more considerate of releasing resources, and our issue here is that we open a file but we do not close it. As python is a language which is able to automatically release resources for us we might consider that we don't need to worry about this. The risk is that  holding a resource open longer than we need it risks the possibility that some other code may not be able to access that same resource.

A great example is when writing to a file which will subsequently be read elsewhere in your program. By not closing the file it may prevent the attempt to open and read that file.

One way to solve this is to explicitly call the `close` method of the file object, but fortunately in our case there is a simpler and cleaner solution to the problem: context managers. Resources that support this mechanism allow precise control over when a resource is released. Files support this mechanism, so instead of:  
```
input = open(filename, 'rt')
lines = input.readlines()
```
We can write:
```
with open(filename, 'rt') as input:
    lines = input.readlines()
```
As soon as we drop out of the indented area after the with statement the file resource is released.

## The whole file is loaded into memory
This may sometimes be a good choice where enough memory is available but what if the input file becomes massive? The amount of memory needed might firstly impact other processes on the same system and second may simply fail because enough memory cannot be allocated.

In our case there is simply no reason to load the entire file contents into memory and it will only require a simple change to make this happen and we'll also need to specify less lines of code to do so! This part of 
```
def wordcount_file(filename):
    with open(filename, 'rt') as input:
        # Read all lines of the file into a list
        lines = input.readlines()

wordcount_list_sorted = wordcount_lines(lines)

return wordcount_list_sorted
```

```
def wordcount_file(filename):
  with open(filename, 'rt') as input:
      return wordcount_lines(input)
```
This might come as a surprise as we were calling `wordcount_lines` with a list of lines whereas now we're calling it with a file object. Fortunately the approach to iterating across a text file object is identical to the approach to iterating through a list (one of python's dynamically typed strengths) and so it just works.

## The list of words is also loaded into memory
This is a very similar problem to the previous one as we are going to maintain a list of every single word read from the file, but it is a flaw with the approach used rather than the python code itself, so to fix this we need to stop maintaining a list of every single word read but instead move to counting as we go.

This requires a bit more of a structural change where instead of:
```
def wordcount_lines(lines):
    words = tokenize_words(lines)
    wordcounts = count_words(words)
```
These need to be combined together somehow. A simple approach of combining the code of both functions together would be messy as it would break our separation of concerns: should a word counting algorithm need to know how to tokenize the input, and wouldn't that mean we couldn't use it in concert with a different tokenizer?

Another alternative might be to have `tokenize_words` instead yield a set of words one line at a time and pass them one line at a time to `count_words` but that would mean a rather simple function would need to have previous state passed to it each time which would then be updated.

Fortunately python again comes to the rescue with a feature that really can change how your code is written in a substantial way: generators. A generator is a function that instead of being called in the usual way returns an object that can be iterated over. Instead of the function returning a value using the `return` keyword, a generator when iterated over provides a value using the `yield` keyword, until it's finished (or the caller stops iterating.

Let's rewrite tokenize_words as an iterator. The before looked like this:
```
def tokenize_words(lines):
    words = []
    for line in lines:
        word = ''
        for character in line:
            if character.isalpha():
                word += character
            else:
                if len(word) != 0:
                    words.append(word)
                    word = ''
        if len(word) != 0:
            words.append(word)
    return words
```
The generator function looks like this:
```
def tokenize_words(lines):
    for line in lines:
        word = ''
        for character in line:
            if character.isalpha():
                word += character
            else:
                if len(word) != 0:
                    yield word
                    word = ''
        if len(word) != 0:
            yield word
```
Less code, fewer state variables, and again this works without any change to the rest of the code, but it makes sense to rewrite this part of `wordcount_lines` to stop pretending we have a list of words as instead we have a generator object which behaves quite differently and shouldn't be kept around after iteration has completed:
```
words = tokenize_words(lines)
wordcounts = count_words(words)
```
Becomes:
```
wordcounts = count_words(tokenize_words(lines))
```

The script wordcount_c.py contains the changes described above.

# Critique of wordcount_c.py
## The word count list is kept in memory
There remains a theoretical risk of memory overuse with a large enough set of input data with enough words in it to cause us problems, but to solve this would require an entirely different approach involving persisting this information outside of memory, so we'll leave that problem as out of scope.

## There are two copies of the word count list: the unsorted and the sorted
This is true and could have been solved at the beginning by using the list `sort` method rather than the `sorted` function which returns a new list. So something like from this:
```
wordcount_list_sorted = sorted(wordcount_list, reverse=True, key=lambda pair: pair[1])
```
To:
```
wordcount_list.sort(reverse=True, key=lambda pair: pair[1])
```
Except... I haven't been entirely honest with you :( but honestly I was doing it for your benefit! Python has had two major release versions: 2 and 3. Python 2 is out of support so most of this is moot, but the code above works fine with python 2, but not with python 3 which would complain with the error `AttributeError: 'dict_items' object has no attribute 'sort'`. This is because although I've been telling you that wordcount_list was a list, it is actually only a list when running under python 2 and under python 3 it's a dict_items object which... well... it's complicated... it's a type of view but the thing to note is that it will iterate as needed and so there actually weren't two copies of the word count list under python 3 anyway.

The better news is that we're actually going to change our solution in the next step in such a way that this is no longer going to be of concern.

## We should be leveraging the python library modules instead of reinventing the wheel
As always with modern languages with large frameworks of libraries included the challenge is as much what you aren't aware of as how you're writing your code. Best way to avoid bugs: don't write the code in the first place (Karate Kid reference).

### Leverage the collections.Counter class
collections.Counter object is, to quote from the python docs: a dict subclass for counting hashable objects.  
Sounds like something we're already doing right? Yes, we can remove `count_words` from our solution and drop in replace it with `collections.Counter`. So from:
```
wordcounts = count_words(tokenize_words(lines))
```
To:
```
wordcounts = collections.Counter(tokenize_words(lines))
```
But it gets even better! `collections.Counter` has a method called `most_common` which, from the python docs: Return a list of the n most common elements and their counts from the most common to the least.

So that takes us from:
```
def wordcount_lines(lines):
    wordcounts = collections.Counter(tokenize_words(lines))
    wordcount_list = wordcounts.items()
    wordcount_list_sorted = sorted(wordcount_list, reverse=True, key=lambda pair: pair[1])
    return wordcount_list_sorted
```
To:
```
def wordcount_lines(lines):
    wordcounts = collections.Counter(tokenize_words(lines))
    return wordcounts.most_common()
```

### Leverage the argparse library to handle argument parsing and provide usage/help.
We are handling input arguments to our script in a primitive way and whilst it works it doesn't do much more than output a single line of warning when the solution is invoked from the command line with anything other than a single parameter. It also doesn't validate that the file exists and can be opened, so if it cannot be then the end user gets an unhelpful stacktrace:
```
python wordcount_c.py not_exist.txt
Traceback (most recent call last):
  File "wordcount_c.py", line 86, in <module>
    wordcount_list_sorted = wordcount_file(sys.argv[1])
  File "wordcount_c.py", line 74, in wordcount_file
    with open(filename, 'rt') as input:
IOError: [Errno 2] No such file or directory: 'not_exist.txt'
```
A Python library to the rescue again this time in the form of the `argparse` module. This module can do more than just parse arguments as we'll see below as we change from:
```
import sys

if len(sys.argv) != 2:
    print('Usage: <filename>\n Where <filename> is the text file from which we will count the words')
    exit()

wordcount_list_sorted = wordcount_file(sys.argv[1])
```
To:
```
import argparse

parser = argparse.ArgumentParser(description='Count occurances of each word in the input text')
parser.add_argument('input', type=argparse.FileType('rt'))

args = parser.parse_args()

wordcount_list_sorted = wordcount_lines(args.input)
```
So the argument parser will accept a single input parameter which represents our input text filename and will attempt to open the file for reading when the script command line is parsed. This happens when `parser.parse_args()` is called and returns an object with a member named after the option name, `input` in our case.

It will also generate help text for the end user when no arguments are specified or when `-h` is passed:
```
usage: wordcount_d.py [-h] input

Count occurances of each word in the input text

positional arguments:
  input

optional arguments:
  -h, --help  show this help message and exit
```

We no longer need the wordcount_file function as it was only opening the file and calling `wordcount_lines` with the file object anyway.

What happens if we pass in a filename which does not exist?
```
usage: wordcount_d.py [-h] input
wordcount_d.py: error: argument input: can't open 'not_exist.txt': [Errno 2] No such file or directory: 'not_exist.txt'
```

One final benefit of specifying the parameter type as a file is that we can actually now use standard input (stdin) instead of specifying the filename by specifying a single hypen `-` parameter. So on Unix:  
```cat sample.txt|python wordcount_d.py -```  
And on Windows:  
```type sample.txt|python wordcount_d.py -```  

### Leverage the re module to handle tokenizing
Warning: this section involves regular expressions and if you aren't used to these then you might want to go and read a little about them elsewhere first. Put simply they are ways of using a syntax to specify patterns to be matched in strings.

The `re` module will allow us to replace our `tokenize_words` function with a much shorter implementation, but it might not be very intuitive unless you are familiar with regular expression syntax. The original looked like this:
```
def tokenize_words(lines):
    for line in lines:
        word = ''
        for character in line:
            if character.isalpha():
                word += character
            else:
                if len(word) != 0:
                    yield word
                    # Prepare for the next word by resetting this to an empty string
                    word = ''
        if len(word) != 0:
            yield word
```
The replacement like this:
```
def tokenize_words(lines):
    for line in lines:
        for word in re.split(r'\W+', line):
            if word:
                yield word
```
The regular expression specifies will match one or more non word characters (i.e. anything other than alphabet characters) and use those matches to split up the line. If there are any non word characters at the start or the end of the line then we get empty strings returned so we only yield words that have characters in them.


The script wordcount_d.py contains the changes described above.

# Critique of wordcount_d.py
The following criticisms are more about how I got from wordcount_a.py to wordcount_d.py than the code per se.

## How do you know your changes worked?
Well this is probably the biggest ommisions since we started: we haven't been checking that the behaviour has remained the same after we made each change. This would have been one of the most compelling reasons to move from the unstructured wordcount_a.py to the functions in wordcount_b.py as we would then have been able to start testing our functions in isolation of each other.

Side note: In fact there are a schools of thought called Test Driven Development (TDD) and Test First Development (TFD) that would strongly encourage (mandate? religious warning!) that we write the test ahead of the bit of functionality/change we're making (there's more to it than this, but there are many excellent resources that would explain it better than I). In essence the chief benefit is that we think about problem from the user (API caller in our case) perspective rather than the implementors perspective. This can have benefits both in producing a more pleasing API for the end user, a more testable set of functionality because we have to think about how we can test this up front and can even save time in coding because we don't necessarily have to write code that we later realise we need to rewrite/throw-away. The approach is not beloved by all and it may work better in some cases than others, but I do recommend giving it a serious try to see some of the benefits.

So how to test the behaviour of each function: leverage the python unittest module. In our case I'm going to write a separate script which is going to import our main script and test the functions individually:
```
import unittest
import wordcount_d

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
        self.assertSequenceEqual(wordcount_d.wordcount_lines([
            "My name is, my name is, my name is... Skinny Shadowy!",
            ]), [('name', 3), ('is', 3), ('my', 2), ('My', 1), ('Skinny', 1), ('Shadowy', 1)])

    def test_multiple_lines(self):
        self.assertSequenceEqual(wordcount_d.wordcount_lines([
            "There ", "can,", " be ", " only", "one!", ""
            ]), [('There', 1), ('can', 1), ('be', 1), ('only', 1), ('one', 1)])

if __name__ == '__main__':
    unittest.main()
```
In the case of `tokenize_words` it returns a generator so wrapping it in a `list()` causes it to populate a list from that generator which we can then use to compare with the expected outcome.

Running the above script under python 3 yields this kind of outcome:
```
.....
----------------------------------------------------------------------
Ran 5 tests in 0.001s

OK
```
Strangely running the same under python 2 doesn't end so well:
```
..F..
======================================================================
FAIL: test_multiple_lines (__main__.TestWordcountLines)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "test_wordcount.py", line 30, in test_multiple_lines
    ]), [('There', 1), ('can', 1), ('be', 1), ('only', 1), ('one', 1)])
AssertionError: Sequences differ: [('be', 1), ('only', 1), ('The... != [('There', 1), ('can', 1), ('b...

First differing element 0:
('be', 1)
('There', 1)

- [('be', 1), ('only', 1), ('There', 1), ('can', 1), ('one', 1)]
+ [('There', 1), ('can', 1), ('be', 1), ('only', 1), ('one', 1)]

----------------------------------------------------------------------
Ran 5 tests in 0.002s

FAILED (failures=1)
```
The order is different for words sharing the same count! This was not a requirement for the algorithm so it's more of a test problem, but to understand why it's different between python 2 and 3 we need to look at the documentation for `collections.Counter.most_common()' which says:
1. Python 2: Elements with equal counts are ordered arbitrarily
2. Python 3: Elements with equal counts are ordered in the order first encountered

Well, that explains it - but what do we do about it? It's actually a little complex to resolve because a lot of the preprocessing of the answer (such as sorting first by word and then by count) would hide any issues in our algorithm. Whatever we do we also only need to do it in python 2 as well. We could replace the comparison with our own helper function that compares the way we expect, but if it doesn't match then the test won't show all the helpful `unittest` output which shows you exactly what differs.

I decided to write a function which would walk through the list grouping the pairs sharing the same word count using `itertools.groupby` and then using `sorted` on each group of pairs, finally reassembling the list or word, count pairs. By passing both the output from `wordcount_lines` and the expected results through this function, we can then allow the `unittest.assertEqual` to do its work on these. This is only needed for python 2 so let's leave python 3 to work as it usually does, by detecting the python version and providing a passthrough implementation in python 3:
```
import itertools
import operator

def reorder(wordcounts):
    return list(wordcount for _, group in itertools.groupby(wordcounts, key=operator.itemgetter(1)) for wordcount in sorted(group))
```
Note: I haven't mentioned any of the following yet so you'll either have to take my word for it or start reading the python documentation:
1. `itertools.groupby`
2. `operator.itemgetter`
3. Using the convention of a single underscore as throwaway variable
4. A list comprehension.
5. A double for loop list comprehension

Finally, note that we only need the alternative approach for comparisons when using python 2 so let's use the python interpreter version to decide to use this implementation for python 2 and a dummy passthrough implementation for python 3:
```
if sys.version_info.major == 2:
    import itertools
    import operator

    def reorder(wordcounts):
        return list(wordcount for _, group in itertools.groupby(wordcounts, key=operator.itemgetter(1)) for wordcount in sorted(group))
else:
    def reorder(wordcounts):
        return wordcounts
```
Note: the mechanism of using some criteria to choose an alternate definition of a function demonstrates a very powerful feature of pythons dynamic nature allowing it to make powerful implementation decisions even at runtime.

## Why did you make performance/memory improvements without measuring first?
Another great question! One of the great wisdom sayings when it comes to optmisation is "measure first" and anyone who's spent a long time optimising a code only to discover that they were optimising the wrong thing will have learned this the hard way!

In my case I was trying to show the logically efficient thing to do but really more focussing on just being able to handle large bodies of text, but nevertheless it would have been a good idea to measure time and memory usage as we made changes.

Python has a number of ways to do this from full profilers through to the relatively simple `timeit` module which is really tuned for benchmarking small snippets of code and can either be used directly in a script as we have with other modules or can be invoked from the command line with a snippet of code.

I ran it as follows as it allows me to choose which version of python to use and which script to use:  
`py -3 -m timeit -s "from wordcount_d import wordcount_lines" "wordcount_lines(open('article-urls.txt', 'rt', encoding='utf-8'))"`  
The breakdown is:
1. `py`: the common launcher (well, more common on Windows than Unix in my experience)
2. `-3`: the version of python for the common launcher to pick, `-2` for python 2. If you aren't using the common launcher then skip this argument.
3. `-s "<code>"`: optional setup code to be used to prepare ahead of running the test, but not included in the measurements.
4. `"<code>"`: code to be benchmarked.

When running under python 3 on Windows we need to pass the encoding as utf-8 if we expect characters that are not in the command prompt's language codepage (which is much too complicated to go into here... possibly ever...).

I chose a corpus of text which is around 265MB long in order to give our code enough work to do to get something vaguely helpful to see the difference. The output from the above command looked like this on my system:
```
py -3 -m timeit -s "from wordcount_d import wordcount_lines" "wordcount_lines(open('article-urls.txt', 'rt', encoding='utf-8'))"
1 loop, best of 5: 37.8 sec per loop
py -2 -m timeit -s "from wordcount_d import wordcount_lines" "wordcount_lines(open('article-urls.txt', 'rt'))"
10 loops, best of 3: 49.8 sec per loop
```
| Script | Python | Result | Output |
| --- | --- | --- | --- |
| wordcount_b | 2 | 62.5s | `1 loops, best of 5: 62.5 sec per loop` |
| wordcount_b | 3 | 66.1s | `1 loop, best of 5: 66.1 sec per loop` |
| wordcount_c | 2 | 59.4s | `1 loops, best of 5: 59.4 sec per loop` |
| wordcount_c | 3 | 64.4s | `1 loop, best of 5: 64.4 sec per loop` |
| wordcount_d | 2 | 49.9s | `1 loops, best of 5: 49.9 sec per loop` |
| wordcount_d | 3 | 38.7s | `1 loop, best of 5: 38.7 sec per loop` |

(note that I also passed the options `-n 1 -r 5` to Python 2 invocations so that they didn't take so long :smiley: )
