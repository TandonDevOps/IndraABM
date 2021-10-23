# Python Profiler Considerations

---

## Why would you want to use a profiler?
Let's say you have a program that's running slow.  What is the best way to speed it up?  How do you know which function to optimize first?

Profiling is a form of program analysis that measures the frequency and duration of function calls.  To speed up our models and the IndraABM system, we need to know which functions are taking the most time to execute.  With that information we can optimize our program.  We can make our slow functions faster, or we can call our slow functions less often.


## Types of Profilers
* Deterministic Profilers - Tracing
* Statistical Profilers - Sampling


## cProfile - Tracing
Build in to the standard python library.  Docs:  https://docs.python.org/3/library/profile.html

### cProfile CLI example
example of CLI execution of cProfile redirected into a file named info.log, sorted by filename and total time (tottime): `python -m cProfile -s filename -s tottime segregation.py > segregation.profile`

Command Line arguments:
-o output file
-s sort order
-m specifies a module is being profiled instead of a script

basic structure `python -m cProfile -s <sort option> program`


## pyinstrument - Statistical
Git repo can be found here:  https://github.com/joerick/pyinstrument

Documentation:  https://pyinstrument.readthedocs.io/en/latest/


---

## What if you want to profile parts (loops, assignments, imports, io, calls) of a single function?
To profile small bits of code you can use the module timeit from pythons standard library.  The docs can be found here: https://docs.python.org/3/library/timeit.html

---

## Some other python profiler projects
### Py-Spy - Statistical
Git repo: https://github.com/benfred/py-spy

### palanteer
Git repo:  https://github.com/dfeneyrou/palanteer
Docs in repo at /docs
note: a viewer


### yappi - Tracing
Git repo:  https://github.com/sumerc/yappi
note: Multithread support

