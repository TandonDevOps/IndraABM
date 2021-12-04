# Python Profiler Considerations

---
# General Info
## Why profile software?

Profiling is a form of program analysis that measures the frequency and duration of function calls.  We profile software to figure out how much time is spent in each function as the program executes.  It allows us to identify which functions take the most time to run.  With that data we can optimize our program.

We can answer the following questions about a program using profiling:
* How many times is each function called?
* Which function / module is called the most?
* Which function takes the longest to run?
* What is the total time a function takes to run - counting subcalls?
* What is the total time a function takes to run - not counting subcalls?
* What is the per-call time a function takes?
* Is it faster to use a for loop, while loop, enumerate, or some other iterator?
* How often are we making recursive calls?

There are three major ways we can speed up our programs once we have the profiler data.  First, we can try to call our slowest functions less often.  Second, we can refactor our functions to execute faster, but leave the general functionality the same.  And lastly, we can change the programs architecture.  The third option is the least appealing since it will be nescesitate the most change.

---

## Types of Profilers
### Deterministic Profilers - Tracing

A deterministic profiler places hooks in the code and traps every function call.  This traces the program as it runs and gives a detailed running time for each function call.  There is some CPU overhead as the CPU will have to run both the python code and the profiler code.  Therefore the python program being profiled will run slightly slower while profiling than it would otherwise.  When using the python profiler cProfile, which comes packaged as part of python's standard library, any c code from libraries will run at full speed but the python code will run around 30% slower because of the profiler overhead. That can cause a skew in the statistics that we need to be aware of.

### Statistical Profilers - Sampling

Statistical profilers work by sampling the program's call stack at set intervals to keep track of how long different functions run.  Because the statistical profiler runs in a separate process, it does not slow down the code being profiled.  Also, because it is a seperate process it can be used in production settings to test running systems.  Note, the profiler gives run time statistics, which will not be as accurate as deterministic profilers.

---

## cProfile - Tracing - Part of pythons standard library
cProfile is build in to the python's standard library.

An example of CLI execution of cProfile redirected into a file named segregation.profile, sorted by filename and total time (tottime): `python -m cProfile -s filename -s tottime segregation.py > segregation.profile`

Command Line arguments:
-o output file
-s sort order
-m specifies a module is being profiled instead of a script

basic structure `python -m cProfile -s <sort option> <program name>`




---

## What to do once you have some info about your program / model?

You can see a link to a sample analysis of the *[segregation model](segregation.md)*

---

## What if you want to profile parts (loops, assignments, imports, io, calls) of a single function?
To profile small bits of code you can use the module timeit from pythons standard library.  The docs can be found here: https://docs.python.org/3/library/timeit.html.  This is useful for figuring out which method is fastest for your code.  For example should you use a *for loop* or a *while loop*, enumeration, list comprehension, etc.

---



## More Info
[Wikipedia - Profiling](https://en.wikipedia.org/wiki/Profiling_(computer_programming))

[cProfile : Official Docs](https://docs.python.org/3/library/profile.html)

### Some other python profiler projects
#### pyinstrument - Statistical
Git repo can be found here:  https://github.com/joerick/pyinstrument

Documentation:  https://pyinstrument.readthedocs.io/en/latest/


#### Py-Spy - Statistical
Git repo: https://github.com/benfred/py-spy

#### palanteer
Git repo:  https://github.com/dfeneyrou/palanteer
Docs in repo at /docs
note: a viewer


#### yappi - Tracing
Git repo:  https://github.com/sumerc/yappi
note: Multithread support
