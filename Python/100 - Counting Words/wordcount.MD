# Critique of wordcount_a.py
The solution addresses the objectives set out for it, but would almost certainly would have triggered a number of responses from a seasoned python developer at code review, however let's not forget that in this example we're trying to introduce someone new to python, and possibly programming, and so a number of obvious simplifications were avoided. Let's start by going through the most obvious simplification.

## X = X + Y
In cases where we are simply adding to an existing variable, whether that be incrementing a numeric value or adding a character to a string, we can use a shorthand syntax:  
'word = word + character'  
Can instead be expressed using a simpler notation:
'word += character'  
This is true for many operations across python.

## It's just a sequence of commands - there is no structure!
Indeed, in many ways it is very similar to what one might see in a simple dos batchfile or Unix shell script: a sequence of commands to be executed in order. Is that so bad? Well, not always. In fact python works very well as a cross platform replacement for scripts of commands, but in this particular case, as I think is somewhat evidenced by the section comments, the lack of structure means that someone looking at the code needs to read the entire thing to deduce what the code is doing and so that takes time and effort that could otherwise be avoided. They also need to consider every variable is at global scope which makes it hard to reason what happened to it beforehand that might by impacting later code.

The other problem with the lack of structure is that another author might want to solve a similar problem and be able to leverage much of the functionality here but to do so they would need to copy and paste that shared code into their own script. This is usually what is known as a bad thing. Why? Bug's fixed in one may not be propogated into the other. The fact that most of the code is identical should be an aid as someone who has looked at the source of one should have a head start on the other, but because it has been copy pasted this is not possible to do with any confidence as many subtle changes may have been made.

The most obvious solution to all of this is to add some structure in the form of functions and, to allow other scripts to use functions from our script, to follow a convention of only executing the full functionality of the script if it is the main script. This is accomplished in python like so:  
'''
if __name__ == '__main__':
  <your code follows>
'''
If this script is imported by any other, it will not execute the code inside the if statement.  

The script wordcount_b.py contains for the changes described above.
