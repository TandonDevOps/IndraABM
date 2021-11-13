# Segregation Model Considerations
last-updated: Nov 7, 2021

## Ten Slowest Functions Before Refactoring
|ncalls | tottime | file | function |
| --- | --- | --- | --- |
|748323| 2.320 | space.py |  get_agent_at |
|759052|1.191 | space.py | is_empty |
|10560 | 0.878 | space.py | _load_agents |
|1049532 | 0.607 | registry.py | \_getitem_ |
|524235|0.589|registry.py | get_agent|
|1049532|0.488|registry.py| \_contains_ |
|500077|0.313|segregation.py | lambda: line 71 |
|1000154|0.151|agent.py | group_name|
|10560|0.132|space.py | \<listcomp\>: line 980
|10560|0.036|space.py | neighbor_ratio

Initial Total Run Time:  11.418 seconds

<br>
## Initial observations
Speeding up space.py will have the most effect on speeding up the segregation model.

## comments on functions
### Space.py - get_agent_at

```python
def get_agent_at(self, x, y):
        """
        Return agent at cell x,y
        If cell is empty return None.
        Always make location a str for serialization.
        """
        from registry.registry import get_agent
        if self.is_empty(x, y):
            return None
        agent_nm = self.locations[str((x, y))]
        return get_agent(agent_nm, self.exec_key)

```

The function *get_agent_at* in space.py is the most expensive time wise.
It is called almost 750,000 times and it takes more than 2.32 seconds to run, almost twice as long as the next slowest function.



``` python
def get_agent(name, exec_key=None, **kwargs):
    """
    Fetch an agent from the registry.
    Return: The agent object, or None if not found.
    """
    try:
        if exec_key is None:
            exec_key = get_exec_key(**kwargs)
        if len(name) == 0:
            raise ValueError("Cannot fetch agent with empty name")
        if name in registry[exec_key]:
            return registry[exec_key][name]
        else:
            registry.load_reg(exec_key)
            if name not in registry[exec_key]:
                print(f'ERROR: Did not find {name} in registry for {exec_key}')
                return None
            return registry[exec_key][name]
    except (FileNotFoundError, IOError):
        print(f'ERROR: Exec key {exec_key} does not exist.')
        return None

```

<br>

## Changes to Speed up the Model

### First Change: Move location of Imports
By moving the *get_agent* import from the function *get_agent_at* to the module cuts a second off of the *get_agent_at* runtime, a speed up of ~ 50%.  Overall, with that one change, the model runs in 10.034 seconds, a speed up of ~14%

The function *get_agent_at* is now the second slowest function overall.


## Ten Slowest Functions After First Change
|ncalls | tottime | file | function |
| --- | --- | --- | --- |
|761572| 1.181 | space.py | is_empty |
|752282| 1.154 | space.py |  get_agent_at |
|10560 | 0.877 | space.py | _load_agents |
|1059380 | 0.626 | registry.py | \_getitem_ |
|529159|0.573|registry.py | get_agent|
|1059380|0.499|registry.py| \_contains_ |
|505417|0.314|segregation.py | lambda: line 71 |
|1010834|0.152|agent.py | group_name|
|10560|0.135|space.py | \<listcomp\>: line 978
|10560|0.036|space.py | neighbor_ratio

After first Change Run Time:  10.046 seconds

<br>

### Change number two: Taking a look at *is_empty*
After the first change *is_empty* is now the slowest function.  It takes a total of 1.18 seconds


``` python
def is_empty(self, x, y):
        """
        See if cell x,y is empty.
        Always make location a str for serialization.
        """
        return str((x, y)) not in self.locations
```

Upon examining the code, any refactoring of the code in *get_agent_at* to remove calls to *is_empty* would result in less readable code and a hacky work around to prevent trying to access an invalid entry in the locations dictionary.

If we want to speed up our code we will have to find a way to call is_empty less, which will require calling *get_agent_at* less often.  The function *get_agent_at* is responsible for (752282 / 761572) ~ 99% of the calls to *is_empty*.

### Change number three: Taking a look at *_load_agents*

``` python
def _load_agents(self, exclude_self=True):
        """
        This fills self.my_agents with all neighbors, and maybe the center
        agents, depending upon `exclude_self`.
        """
        if DEBUG.debug2_lib:
            print("calling _load_agents in space.py")
        for y in range(self.height):
            y_coord = self.SW[Y] + y + 1
            for x in range(self.width):
                x_coord = self.SW[X] + x
                if (x_coord, y_coord) == self.center and exclude_self is True:
                    continue
                potential_neighbor = self.space.get_agent_at(x_coord,
                                                             y_coord)
                if potential_neighbor is not None:
                    self.my_agents.append(potential_neighbor)
        self._load_sub_reg_agents(exclude_self=exclude_self)
```
