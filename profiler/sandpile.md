# Sandpile Model
last-updated: Oct 24, 2021
1628518 function calls (1593264 primitive calls) in 6.714 seconds

## Ten Slowest Functions

|ncalls | tottime | file | function |
| --- | --- | --- | --- |
|3113 | 0.057 | sre_parse.py | _parse (line:493) |
| 248 | 0.041 | traitlets.py | getmember(line:219) |
| 4076 | 0.040 | sre_compile.py | _compile(line:71) |
| 168 | 0.039 | __init__.py | <module>(line:1) |
| 373 | 0.035 | doccer.py | docformat(line:10) |
| 2750 | 0.034 | inspect.py | cleandoc(626) |
| 627 | 0.033 | sre_compile.py | _optimize_charset(line:276) |
| 27880 | 0.019 | sre_parse.py | __next(line:233) |
| 42988 | 0.019 | sre_parse.py | __getitem__(line:164) |
| 1356 | 0.018 | inspect.py | _signature_from_function(line:2150) |

## Thoughts
A lot of print statements (Creating agent, I am not toppling, etc)
Most of the totime comes from built-in functions 
  
Compared to segregation.py, there are a lot less calls which probably makes sense for the small tottime which makes sense for the minimal model
