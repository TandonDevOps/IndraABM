# Python Profiler Considerations

## Types
* Deterministic Profilers - Tracing
* Statistical Profilers - Sampling


### cProfile - Tracing
Build in to the standard python library.  Docs:  https://docs.python.org/3/library/profile.html

#### cProfile CLI example
example of CLI execution of cProfile redirected into a file named info.log, sorted by filename and total time (tottime): `python -m cProfile -s filename -s tottime segregation.py > info.log`

Command Line arguments:
-o output file
-s sort order
-m specifies a module is being profiled instead of a script

basic structure `python -m cProfile -s <sort option> program`


### pyinstrument - Statistical
Git repo can be found here:  https://github.com/joerick/pyinstrument

Documentation:  https://pyinstrument.readthedocs.io/en/latest/


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

