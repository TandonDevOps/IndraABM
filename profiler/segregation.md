# Segregation Model Considerations
last-updated: Oct 19, 2021

## Slowest Functions
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
