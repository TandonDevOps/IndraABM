# Python Profiler Considerations

---

## Why would you want to use a profiler?
Let's say you have a program that's running slow.  What is the best way to speed it up?  How do you know which function to optimize first?

Profiling is a form of program analysis that measures the frequency and duration of function calls.  To speed up our models and the IndraABM system, we need to know which functions are taking the most time to execute.  With that information we can optimize our program.  We can make our slow functions faster, or we can call our slow functions less often.


## Types of Profilers
* Deterministic Profilers - Tracing
* Statistical Profilers - Sampling

A deterministic profiler places hooks in your code and traps every call, tracing the program as it runs, giving detailed run times for each function.  There is a bit of overhead, so the python program will run slightly slower while profiling.  One idiosyncrasy using the python profiler cProfile is that the python code will run slower than usual, around 30% so, while any c code run from libraries will run without a slowdown. That can cause a skew in statistics that one needs to be aware of.

Statistical profilers work by sampling the program's call stack at set intervals to keep track of how long different functions run.  Because the statistical profiler runs in a separate process, it does not slow down the code being profiled.  Also, because it is a seperate process it can be used in production settings to test running systems.  Note, the profiler gives run time statistics, which will not be as accurate as deterministic profilers.


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

## What to do once you have some info about your program / model?

You can see a link to a sample analysis of the *[segregation model](segregation.md)*

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

