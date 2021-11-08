# Tutorial video Script

> This file is served as a script of tutorial video

> Presentation of forest fire model and Step 1 are mainly conducted by Yuefei, whereas Step 2 and Step 3 are mainly conducted by Licheng.
>  
> Feel free to message us if any of the script part is causing confusion.

## Intro

`screen on an intro page or the Indra GitHub page?`  
Hi everyone. This is a tutorial video for the Indra system which is an agent-based modeling system written in python.  
In this video, we will show you how to create a simple agent-based model from scratch.

## Presentation of forest fire model 

Before we get into creating a new model, let's see some runnable example models first, like the forest fire model.  
Forest fire model is an agent-based model that describes wildfire spreading and extinguishing through progress.

`cd IndraABM/models; ../run.sh forest_fire.py`  
Firstly, the terminal is asking us for some parameters, like grid height, width, the probability that a tree will catch fire, tree density, etc.   
Let's keep the default values for now, and start running the simulation to see the effects. 

`keep pressing enter until reach menu`  
We can see from the menu that there are a number of actions that we can take, such as run for N periods. Let's try this. 

`type 1 to choose run for N periods`  
It's asking us how many periods we want to run. Let's give 5 a try.

`type 5 to run 5 periods, and screen flashing with outputs`  
Wow, we are getting a lot of outputs here. Let's scroll back to the top to see what is happening here. 

`scroll back till the input 5 we give, then a little down to show the census for period 0`  
Okay, we can see it here, that we start with 704 healthy trees and none of the others. Let's see what happens next.

`scroll a bit down more to show the census for period 1, see the result, healthy trees may decrease to stay the same, describe the situation and change script as needed`  
Oh, now the healthy trees decreased to 698, and we can see the rest of them have new fires starting on them.   
Those fires will spread with speed, and soon we will see the changes on the trees surrounding them as well.

`scroll down to show the census for period 2`  
Now, not only is the new fire number increasing, the number of on fire trees is also increasing, as trees can easily catch fire if fire is already present nearby, and it keeps on self-replicating.

`scroll down to show the census for period 3, if burned out `  
Oops, some trees are already burned out by this time.   
We will see this number keep on increasing as the forest fire is spreading.   
When a tree is burned out, it reaches its final state.   
Oh, it may not, since there is still a possibility for a burned out tree to have new growth later, right? 

`scroll down more to show the number of new growth increases. Or quit by type 0 and start a new round with a larger period number until finish showing all states of a tree`

So basically, you should now have a brief overview or at least an idea how an agent-based model works.   
Wanna build a customized model on your own?   
Let's go through the code together on transforming a basic model template that we provide, to another working model called segregation now!

## Transformation from basic to segregation

`type [cp models/basic.py tutorial/basic.py] in terminal to create basic.py`  
`screen switch to IDE/Vim`  
We will modify a prototype model(basic model in basic.py)
into a real segregation model step by step to show that new developers don't have to start from scratch.

But before we get started, let me have a brief introduction of segregation model.   
The goal is to show that people with mild in-group preference towards their own group, could still lead to a highly segregated society.

Next let's get into changing the code. I will explain more during the process.

### Step1

Firstly, let's manage our agent settings like agent names and agent numbers. 

`screen on create_model function in basic.py, mouse highlight "return Basic(MODEL_NAME,grp_struct=basic_grps..."`

Each model will have a parameter called `grp_struct` which is a dictionary that contains group agent info either as a default constant or as a variable mapping to a specified value in `[MODEL_NAME].props.json`

`screen on basic_grps variable in basic.py`

For example, let's look at the `basic_grps` we have in `basic.py`:

`mouse point to blue_grp`

Inside `basic_grps`, we can see two keys: `blue_grp` and `red_grp`.   
Those are the group names that you can customize.   
Let's see inside what we have in `blue_grp`.   
We have three attributes here. 

`mouse point to mdl.MBR_ACTION: basic_action`

The first attribute defines what the agent will do at each turn when the model is running.   
Here, we can see, what the agent will do is specified in a function called `basic_action`.   
We will dig into this function later and change the function to make it do segregation model's job instead of basic. 

`mouse point to mdl.NUM_MBRS: DEF_BLUE_MBRS and mdl.NUM_MBRS_PROP: "num_blue"`

The second and third attributes together define the number of agents that we want to have.   
`mdl.NUM_MBRS_PROP` specifies that we are going to read the number of blue agents from the variable `num_blue`, which is defined in the `[MODEL_NAME].props.json`.  
If we fail to get the property value, the fallback method would be to get the value from `DEF_BLUE_MBRS` constant which we specified in the second attribute.   
Let's play around a bit to see how the changes in this setting affect the model. 

`screen to props.json, and scroll to find num_blue variable, and change its val, compile and run the model again to show changes`

`screen back to props.json, and rename num_blue to num_green, so that the fallback value will show its effect. compile and run the model again to show changes`


### Step2

Next, we will focus on the action of agents.   
`screen on IDE/Vim to edit code`  
Basically there are mainly two parts of action you need to define in your new model. 
The agent first surveys the environment. The second is to respond to the result of that survey. 
So we need to define a function (we call agent_action in ABM system)
to show how the agent surveys the environment and its response to the result.  
`start changing codes (changes are the difference between basic_step_one.py and basic_step_two.py)`  
`screen on the code of basic_action, ready to change it to agent_action in the segregation model`  
In segregation model, the agent first surveys the environment and find the ratio of agents in the same group.
We could call a predefined function called neighbor_ratio() to easily get the ratio.  
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
tolerance which means the agent is happy about where it is, it will stay put. If the ratio is less than its tolerance, 
it will move.
We define two helper functions and some default values to make the structure clearer.

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
```

One thing to mention here is that we don't assign a uniform tolerance rate for all agents. Instead, we have a default
tolerance rate and assign values in the manner of gauss distribution around it to the agents.

```
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
`screen on IDE/Vim to edit code`  
Lastly, we will look into handling props. It is basically setting properties while advanced skills are needed to 
fully understand its detailed techniques. 
Since it is only necessary in some complicated models, we will set constant properties instead.  
`start changing codes (changes are the difference between basic_step_two.py and basic_step_three.py)`

`add props as constants`
```
DEF_WIDTH = 10
DEF_HEIGHT = 10
DEF_DENSITY_RED = 0.33
DEF_DENSITY_BLUE = 0.33
```

```
class Segregation(mdl.Model):
    """
    Thomas Schelling's famous model of neighborhood segregation.
    """

    def handle_props(self, props):
        super().handle_props(props)
        # get area
        area = DEF_WIDTH * DEF_HEIGHT
        # get percentage of red and blue
        dens_red = DEF_DENSITY_RED
        dens_blue = DEF_DENSITY_BLUE
        # set group members
        segregation_grps["red_group"][mdl.NUM_MBRS] = int(dens_red * area)
        segregation_grps["blue_group"][mdl.NUM_MBRS] = int(dens_blue * area)
```


## Ending
This concludes our last step on building a segregation model based on the template. The detailed steps
in this tutorial are mostly general steps that can apply to any other easily customizable ABM models!
Thanks for watching, and please feel free to contact us if you have any questions.
 
