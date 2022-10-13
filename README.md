# Learning-To-Program-In...
Simple lessons in programming across multiple programming languages.

# The approach
The idea of these lessons comes from my experience both being mentored and mentoring others which happens somewhat organically at code review time. A good code review feeds back on effective use of the programming language and helpful libraries provided, points out idiomatic ways of solving problems, encourages clear maintainable code, and provides focus on how the code could and should be tested.

The approach for these lessons is to start by providing a very simple, hopefully understandable, implementation of a solution and then review the solution and refactor into something better. This then continues until we end up with a final version which hopefully demonstrates at least some of the criteria above. Although the initial implementations are intended to be correct (aside from any accidental bugs!), if the choice is between easy to understand and correct then we will start with the former and end with the latter so far as it is practical to do so.

It should be noted that the final version does not imply perfection as there are many ways to solve most problems and different requirements might mean different decisions are correct. A particular example is error handling where the right solution might be simply to fail and stop or where possible attempt to retry a failed operation. Functionality intended for an end user would likely have a stronger focus on providing meaningful error messages, whereas functionality intended for a fellow developer might be content to display the location in the code where the error occurred.

These are probably not suitable for complete beginners to programming and possibly also not for those new to a given language or who haven't yet reached a point of being able to write their own code, but anyone who has written a program or two in the language of choice will hopefully get something out of the observations and the ensuant refactoring.
