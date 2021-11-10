# Sandpile Model

last-updated: Nov 9, 2021

Nov 1, 2021
1602151 function calls (1567174 primitive calls) in 9.492 seconds

Oct 24, 2021
1628518 function calls (1593264 primitive calls) in 6.714 seconds


## Ten Slowest Functions in CProfiler

|ncalls | tottime | file | function |
| --- | --- | --- | --- |
| 373 | 0.063 | doccer.py | docformat(line:10) |
|3113 | 0.046 | sre_parse.py | _parse (line:493) |
| 2750 | 0.040 | inspect.py | cleandoc(626) |
| 168 | 0.039 | __init__.py |  \<module> (line:1) |
| 627 | 0.033 | sre_compile.py | _optimize_charset(line:276) |
| 1356 | 0.027 | inspect.py | _signature_from_function(line:2150) |
| 4076 | 0.025 | sre_compile.py | _compile(line:71) |
| 248 | 0.020 | traitlets.py | getmember(line:219) |
| 27880 | 0.019 | sre_parse.py | __next(line:233) |
| 42988 | 0.019 | sre_parse.py | __getitem__(line:164) |


## Thoughts
Most if not all the totime comes from built-in functions 
After taking a closer look, none of the methods that aren't built in come close to 0.01 seconds

This was done using a deterministic profiler (CProfile) so I tried using a Statistical Profiler (pyinstrument) using the command:
`python -m pyinstrument -r html  sandpile.py > sandpile.profile`

to get the time by time leading to the 9+ seconds of time used to run the code and here are the things I found:

Recorded: 22:37:16  Samples:  3268

Duration: 8.448     CPU time: 8.51

Program: sandpile.py

lib, seaborn, ipywidgets instantiates (pandas,matplotlib,numpy) - 0 -> 8.419 = 8.419 seconds
sandpile.py:1 - 8.419 -> 8.438 = 0.019 seconds
runpy.py - 8.438 -> 8.440 = 0.002 seconds
<string> - 8.440 -> end = 8.448 = 0.008 seconds

## Thoughts
Using pyinstrument will display time by time frames of what is being ran to give a different perspective of using a deterministic profiler. 
  
This is more useful than CProfile in this specific case since CProfile profiles too many details which makes it hard to organize and figure out lower-end times because it gets mixed with a lot of useless information.

CProfile however, is better to pick up outliers in terms of what takes the most time.
  
Next Step:
  Determine if any of these modules are unusued or unrequired since that is taking most of the time
