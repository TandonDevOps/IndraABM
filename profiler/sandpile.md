# Sandpile Model
last-updated: Oct 24, 2021
1628518 function calls (1593264 primitive calls) in 6.714 seconds

## Ten Slowest Functions

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
A lot of print statements (Creating agent, I am not toppling, etc)
Most of the totime comes from built-in functions 

After taking a closer look, none of the methods that aren't built in come close to 0.01 seconds, here is a quick list of built in functions that take the longest
  |ncalls | tottime | function |
  | --- | --- | --- |
  |1830  |  6.288 | {built-in method builtins.compile} |
  |10514  |  0.224 | {built-in method posix.stat} |
  |188/187  |  0.176 | {built-in method _imp.create_dynamic} |
  |1382  |  0.108 | {built-in method marshal.dumps} |
  |2773  |  0.098 | {built-in method io.open_code} |
