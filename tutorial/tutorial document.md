# Script

> This file is served as a detailed documentation on how to create a new model for new developers

## The main procedure of creating a new model

Main differences between different models are the properties they defined and how their agents act. The main procedure
of creating a new models is listed as follows.

1. find/create an [ABM](https://en.wikipedia.org/wiki/Agent-based_model)  
   e.g. [segregation](https://en.wikipedia.org/wiki/Schelling%27s_model_of_segregation),
   [sandpile](https://en.wikipedia.org/wiki/Abelian_sandpile_model)
2. **define props**  
   Each model possesses its own properties. Define them under models/props as a json file. The filename of props needs
   to be the same with the model name.  
   e.g. **segregation**.props.json, **sandpile**.props.json

3. **define action**  
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

# Brief introduction of  [segregation model](https://en.wikipedia.org/wiki/Schelling%27s_model_of_segregation)

Show that people with mild in-group preference towards their own group, could still lead to a highly segregated society.

Each round consists of agents checking their neighborhood to see what the ratio is (using acts.neighbor_ratio()) 
and get the tolerance.
Move if ratio < tolerance, stay put otherwise.

# Steps to transform basic.py into segregation.py
**Step 1: Manage your group agent settings like agent names, agent numbers**

Involved files: [YOUR_MODEL].props.json, [YOUR_MODEL].py

Each model will have a parameter called grp_struct in which we passed a dictionary that contains group agent info 
either as a default constant or as a variable mapping to the value which specified in props.json

For example, let's look at the basic_grps we have in basic.py:
```
basic_grps = {
    "blue_grp": { --> group name that you can customized
        mdl.MBR_ACTION: basic_action, --> basic_action will be a function that user defines 
                                        for what agents do each turn of the model.
        mdl.NUM_MBRS: DEF_BLUE_MBRS, --> DEF_BLUE_MBRS is a constant that defined in the source code 
                                        in case we don't get the property value from props.json
        mdl.NUM_MBRS_PROP: "num_blue", --> For the number of blue agents, we will get value from variable num_blue in 
                                        the props.json file first; if we fails to get the property value, the fallback 
                                        method would be to get the value from DEF_BLUE_MBRS constant which we 
                                        specified earlier
        mdl.COLOR: acts.BLUE --> By default, all models will have two agent groups, which are in blue color and red color
    },
    "red_grp": {
        mdl.MBR_ACTION: basic_action,
        mdl.NUM_MBRS: DEF_RED_MBRS,
        mdl.NUM_MBRS_PROP: "num_red",
        mdl.COLOR: acts.RED
    },
}
```
Next, let's look into the props.json file, for example, basic.props.json:
```
"num_blue": {
    "val": 2, --> Here we specify for the num of blue agent we should have
    "question": "How many blue agents do you want?", --> You can also specify user questions through here 
                                                        to get user-generated input
    "atype": "INT",
    "hival": 100,
    "lowval": 1
},
"num_red": {
    "val": 2,
    "question": "How many red agents do you want?",
    "atype": "INT",
    "hival": 100,
    "lowval": 1
},
```
So those are the group agent settings that we can customize through [YOUR_MODEL].props.json and [YOUR_MODEL].py,
let's see changes that are needed for step one from basic.py to segregation.py:  
We changed basic_grps to segregation_grps, class name Basic to Segregation, 
and specify NUM_RED and NUM_BLUE as fallback values.

Please refer to code in tutorial/basic_step_one.py and compare with models/basic.py to see detailed changes.

**Step 2: Change basic_action function to agent_action to do segregation model job**


Since basic model is only a minimal model that inherits from model.py, agents in the basic model do nothing
but moving around randomly while printing some information out.  
While normally in a real ABM model, agents in each group do a certain action under a specific rule.
So there are mainly two things you need to define in your new model. The agent first surveys the environment. The second is to respond to the result of that survey. 
This response might include things such as moving, switching groups, eating sheep 
and reproducing for the wolf in [wolfsheep](http://edutechwiki.unige.ch/en/NetLogo_Wolf_Sheep_Predation_model) model.
For example, let's look at the agent_action we have in segregation.py
```
def agent_action(agent, **kwargs):
    """
    This is what agents do each turn of the model.
    """
    # find out the neighborhood size:
    hood_size = acts.get_prop(agent.exec_key, "hood_size", default=4)
    # see what % of agents are in our group in our hood:
    ratio_num = acts.neighbor_ratio(agent,
                                    lambda a: a.group_name() ==
                                    agent.group_name(),
                                    size=hood_size)
    # if we like our neighborhood, stay put:
    if env_favorable(ratio_num, get_tolerance(DEF_TOLERANCE, DEF_SIGMA)):
        return acts.DONT_MOVE
    else:
        # if we don't like our neighborhood, move!
        return acts.MOVE
```
The action in segregation model is moving to another spot or staying put. The rule is whether the tolerance ratio is
higher than the ratio of agents in the same group in the neighborhood or not. Meanwhile, we need to define some helper
functions like `env_favorable, get_tolerance` and some default values in these function.

Please refer to code and comments in tutorial/basic_step_two.py and compare with models/basic_step_one.py 
to see detailed changes.

**Step 3: Handle the initialization of the model class(mainly dealing with initializing props)**
TODO, discussion needed.
