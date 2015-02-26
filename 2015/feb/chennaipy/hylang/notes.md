# A Lisp powered python

## Lisp?

Lisp is a programming language designed by John McCarthy in 1958. It stands for
"LISt Processing". Lisp is the second oldest high level programming language to
have survived till date (Who can name the other?).

Lisp uses a concept of Polish Notations or S-Expressions to represent
everything within the language.

We usually write this to add 2 numbers:

    1 + 2

This is how you'd write it in the polish notation

    + 1 1

In lisp, we would write this as a parenthesized polish notation, that is:

    (+ 1 1)

While this can look very intimidating, its very easy once you understand it.
One of the greatest advantages of something like this is that it supports
variable arity out of the box. The syntax of lisp is actually very simple - The
first symbol inside the parens is the function to run and the ones following
the first symbol are the arguments to that function. 

Lets revisit the initial example with multiple numbers. Usual we'd have to
write it this way: 

    1 + 2 + 3 + 4

But in a polish notation, it becomes:

    + 1 2 3 4

Simple, no?

## Hy

- Lisp powered python
- Transforms the lisp code into python AST

### TODO

- Watch [this](https://www.youtube.com/watch?v=AmMaN1AokTI)

### Getting and running Hy

    $ pip install hy $ hy

### Why use Hy?

- Hy is a Pythonic lisp, so it lets us cross apply our knowledge from python
  whilst writing it in a lispy way.
- For people with any experience of Lisp, this would be great since they can
  apply the powers of lisp with the great ecosystem of a language like python
- For people with no background of Lisp, it is a wonderful way to get started
  with experimenting with it right within the comfort of python
- Has great interop with python since it compiles down to the python ast. Can
  be proven via pdb

### Some Hy

Python

    def say_hello(name):
      print "Hello", name

    if __name__ == "__main__":
      say_hello("python")

Hy

    (defn say_hello [name]
      (print "Hello" name))

    (if (= __name__ "__main__")
      (say_hello "python"))

---


