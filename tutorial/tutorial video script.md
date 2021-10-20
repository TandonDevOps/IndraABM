# Tutorial video Script

> This file is served as a script of tutorial video

## Intro

`screen on an intro page or the Indra GitHub page?`  
Hi everyone. This is a tutorial video for the Indra system which is an agent-based modeling system written in python. In
this video, we will show you how to create an ABM model.

## Presentation of forest fire model

First, we will represent the forest fire model to show how a runnable model work.  
`screen switch to forest_fire.py file and run the model`

## Transformation from basic to segregation

`type [cp models/basic.py tutorial/basic.py] in terminal to create basic.py`  
`screen switch to IDE/Vim`
We will modify a prototype model(basic model in basic.py)
into a real segregation model step by step to show that new developers don't have to start from scratch.

Before we get started, let me have a brief introduction of segregation model. The goal is to show that people with mild
in-group preference towards their own group, could still lead to a highly segregated society. Each round consists of
agents checking their neighborhood to see what the ratio of members in the same group is and get their own tolerance
rate. Move if ratio < tolerance, stay put otherwise.

Next let's get into changing the code.

### Step1

Firstly, let's manage our agent settings like agent names and agent numbers. 

`screen on create_model function in basic.py, mouse highlight "return Basic(MODEL_NAME,grp_struct=basic_grps..."`

Each model will have a parameter called grp_struct in which we passed a dictionary that contains group agent info either as a default constant or as a variable mapping to the value which specified in props.json

`screen on basic_grps variable in basic.py`

For example, let's look at the basic_grps we have in basic.py:

`mouse point to blue_grp`

Inside basic_grps, we can see two keys: blue_grp and red_grp. Those are the group names that you can customized. Let's see inside what we have in blue_grp. We have three attributes here. 

`mouse point to mdl.MBR_ACTION: basic_action`

The first attribute defines what the agent will do at each turn when the model is running. Here, we can see, what the agent will do is specified in a function called basic_action. We will dig into this function later and change the function to make it do segregation model's job instead of basic. 

`mouse point to mdl.NUM_MBRS: DEF_BLUE_MBRS and mdl.NUM_MBRS_PROP: "num_blue"`

The second and third attributes together defines the number of agents that we want to have. mdl.NUM_MBRS_PROP specifies that we are going to read the number of blue agents from the variable num_blue, which is defined in the props.json. If we fail to get the property value, the fallback method would be to get the value from DEF_BLUE_MBRS constant which we specified in the second attribute. Let's play around a bit to see how the changes in this setting affect the model. 

`screen to props.json, and scroll to find num_blue variable, and change its val, compile and run the model again to show changes`

`screen back to props.json, and rename num_blue to num_green, so that the fallback value will show its effect. compile and run the model again to show changes`


### Step2

`screen on IDE/Vim to edit code`  
Basically there are mainly two things you need to define in your new model. The agent first surveys the environment. The
second is to respond to the result of that survey. So we need to define a function (we call agent_action in ABM system)
to show how the agent surveys the environment and the response to the result.  
`start changing codes (changes are the difference between basic_step_one.py and basic_step_two.py)`  
`screen on the code of basic_action, ready to change it to agent_action in segregation model`  
In segregation model, the agent first surveys the environment and find the ratio of agents in its group.

`write the first part of agent_action`

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
```

Then, we need to define its response to the result of the survey. It is rather simple. If the ratio is no less than its
tolerance which means it is happy about where it is, it will stay put. If the ratio is less than its tolerance, it will
move.

`write the second part of the agent_action and two helper functions and four default values`

```
    # if we like our neighborhood, stay put:
    if env_favorable(ratio_num, get_tolerance(DEF_TOLERANCE, DEF_SIGMA)):
        return acts.DONT_MOVE
    else:
        # if we don't like our neighborhood, move!
        return acts.MOVE
    
DEF_TOLERANCE = .5
DEF_SIGMA = .2

MIN_TOL = 0.1
MAX_TOL = 0.9    
    
def get_tolerance(default_tolerance, sigma):
    """
    `tolerance` measures how *little* of one's own group one will
    tolerate being among.
    """
    tol = random.gauss(default_tolerance, sigma)
    # a low tolerance number here means high tolerance!
    tol = min(tol, MAX_TOL)
    tol = max(tol, MIN_TOL)
    return tol


def env_favorable(hood_ratio, my_tolerance):
    """
    Is the environment to our agent's liking or not??
    """
    return hood_ratio >= my_tolerance
```

### Step3

## Ending
