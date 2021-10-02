# Script

> This file is served as a script of tutorial video and can also be organized as a documentation on how to
> create a new model for new developers

## The main procedure of creating a new model

Main differences between different models are the properties they defined and how their agents act. The main procedure
of creating a new models is listed as follows.

1. find a thesis of some [ABM](https://en.wikipedia.org/wiki/Agent-based_model)  
   e.g. [segregation](https://en.wikipedia.org/wiki/Schelling%27s_model_of_segregation),
   [sandpile](https://en.wikipedia.org/wiki/Abelian_sandpile_model)
2. define props  
   Each model possesses its own properties. Define them under models/props as a json file. The filename of props needs
   to be the same with the model name.  
   e.g. **segregation**.props.json, **sandpile**.props.json

3. define action  
   Based on the specific ABM thesis, each agent in the model has an action. The action may be shared by all agents or
   need to defined separately.  
   Define the action and some helper functions if needed. Some functions are so commonly used that they are defined in
   lib/actions.py such as neighbor_ratio()  
   e.g. In segregation model. An agent's action is **MOVE** when the number of agents in the same group in the
   neighborhood is even less than the tolerance ratio which is the least it expects or **STAY PUT** otherwise. The
   helper functions include get_tolerance, env_favorable, neighbor_ratio.

Since the basic model (in basic.py) is a runnable model, one easy way to get a new model running is maintaining the main
structure of basic model and replace the props and action with what you defined so that you don't have to build a new
model from scratch. Follow the DevOps principles by doing incremental development and tests after every few changes.

