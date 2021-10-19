# Segregation Model Considerations

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

