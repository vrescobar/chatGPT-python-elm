NOTE: EVERYTHING this repositoriy wiht the exception of this own note ahs been
generated integrally with chatGPT and asked gradually how to correct or refactor each one
of the errors that showed up on the terminal.

For that I followed as guidelines these both articles:
[Building A Virtual Machine inside ChatGPT](https://www.engraved.blog/building-a-virtual-machine-inside/)
[Building an interpreter for my own programming language in ChatGPT](https://6502.is-a.dev/posts/aoc-2022/)

It took me around two hours, where ChatGPT was the mian pilot and I became the copilot, trying to run 
the project and asking gpt gpt to refactor the parts of the code that didn't run, showing the console output mistake and how would it fix the given function etc.

I could ask to change the tests form unittest to pytest and similar tasks,... and it did so, The files I ask it to "cat" them and just copied them on my filesystem.

The language doesnÄt completely run but it was just a 2 hour experiment.

The day GPT is the Pilot and humans become the copilot in a pair programming role is almost here.


Actual generated README code begins here:

----


Elm-python
=========

Elm-python is an experimental programming language. It takes inspiration from
Clojure and Elm, and is implemented in Python. It compiles to LLVM.

Features
--------

-   Immutable data structures
-   First-class functions
-   Pattern matching
-   Algebraic data types

Usage
-----

Run the REPL:

    $ python3 -m elm_python.repl

Copy code

Compile a file:

    $ python3 -m elm_python.main my_program.elm

Copy code

Run tests:

    $ pytest

Copy code

Roadmap
-------

-   Type inference
-   Compiler optimizations
-   Standard library

License
-------

MIT



All the python code lines are:

    ls -1 *.py|cat|wc -l
