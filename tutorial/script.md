# Script

> This file is served as a script of tutorial video and can also be organized as a documentation on how to 
> create a new model for new developers



## The main procedure of creating a new model

1. find a thesis of some [ABM](https://en.wikipedia.org/wiki/Agent-based_model)  
e.g. [segregation](https://en.wikipedia.org/wiki/Schelling%27s_model_of_segregation), 
[sandpile](https://en.wikipedia.org/wiki/Abelian_sandpile_model)
2. define props  
Each model possesses its own properties. Define them under models/props as a json file.

3. define action  
Based on the specific ABM thesis, each agent in the model has an action. The action may be shared by all agents
or need to defined separately.  
Define the action and some helper functions if needed. Some functions are so commonly used that they are defined in
lib/actions.py such as neighbor_ratio()  
e.g. In segregation model. An agent's action is **MOVE** when the number of agents in the same group in the neighborhood
is even less than the tolerance ratio which is the least it expects or **STAY PUT** otherwise. The helper functions
include get_tolerance, env_favorable, neighbor_ratio.

One easy way to get the new model running is maintaining the main structure in basic.py and replace the props and action 
with what you defined.

