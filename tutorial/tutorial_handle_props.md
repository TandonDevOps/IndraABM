# Tutorial of handling props

> Since handling props in Indra system requires advanced skills to fully understand, 
> we make another video delving into it.
>
> This file is served as a script and a document of tutorial video for handling props.

## Content
1. Intro
2. Introduction of `[MODEL_NAME].props.json`
3. Analyze and explain handling props
4. Play around with handle props
5. Handle props from the web
6. End


## Intro
This is a short but more advanced tutorial for Indra system that focus mainly on dealing with user defined props, 
as we will dig deep into the code on all the places that you can customize for parameters.  
We will also introduce the frontend interface for our Indra System.  
If you want a general walk through on how to create an ABM from Indra, please watch our general tutorial video, which will also cover the basics of handling props. 

If you simply want to have a basic use of handling props, it is rather simple.
Write all the parameters you need in the `[MODEL_NAME].props.json` file, call `super().handle_props(props)` and retrieve
the value of the parameter by `self.get_prop(prop_nm)` with the name of the parameter as input. Then you could set attributes
in your struct of group if further processing on the user entered parameters is needed. E.g. `segregation_grps["red_group"][NUM_MBRS] = int(dens_red * area)`
In this video, we will present further details of handling props. 

## Introduction of `[MODEL_NAME].props.json`
Handling props is basically setting values of the parameters in the model. In Indra system, you are asked several
questions to set parameters when you run the model in the terminal mode. The parameters and the questions are 
defined in the `[MODEL_NAME].props.json` file.  

Before we get into the code, I will show you one example to help you understand the general structure/format of the file.  
`screen on segregation.props.json`  
Let's have a look at the props file of segregation model.
It is actually a two-layer dictionary. The key of outer dictionary is the parameter, and the value is an inner
dictionary with attribute as key and value of the attribute as value.
For the keys of outer dictionary, there is not much to talk about. They are the parameters you are going to set in your
model.  
`highlight the line`  
For inner dictionary. First you set a default value of the parameter or in other words, the fallback value of the
parameter when you press enter. The attribute name is "val", and we set a default value 40 for grid_height.  
`highlight the line`  
The second attribute is "question" which is the question you design to ask in the terminal. 
It is better to compose a clear question since the parameter name itself might be confusing.  
`highlight the line`  
The third one is "atype" which defines the data type of the parameter. There are several options: "INT" which represents
integer, "DBL" which represents double, "BOOL" which represents boolean, "STR" which represents string.  
`highlight two lines`  
And the last two attributes "hival" and "lowval" which defines the 
highest and lowest value of the parameter are for numeric types "INT" and "DBL".
You can set these two attributes based on the specific restrictions in your model.
```
"grid_height": {
    "val": 40,
    "question": "What is the grid height?",
    "atype": "INT",
    "hival": 100,
    "lowval": 2
},
```

Now we have a basic understanding of the props file, let's begin exploring the code to figure out how exactly handling
props deals with props file and if there is another way to set parameters. I will explain while going through the code step by step. 

## Analyze and explain handling props
`screen on segregation.py`  
In some complicated ABM models, users need to set multiple parameters like I just mentioned in the example. 
So a function that helps handle props (called handle_props() in Indra) is needed to set values of these parameters.
On the whole, handling props tries to initialize `self.props` in the model so that we could set parameters with `self.props.get(prop_nm)`  
To achieve this goal, we will make use of the function `PropArgs.create_props()` in the site-package called PropArgs.

There are actually lots of details along the way, so I will talk more about the key points and briefly mention some other details.
Let's get started!

`highlight super().handle_props(props)`  
Since all our model classes inherit from the base class Model, we first call `super().handle_props(props)` 
defined in the base model, props is a dictionary of parameter name to value mapping. We will leave it for now and talk about it later.
  
`cursor on handle_props() and step into it`  
Let's step into it to see what's going on.
First, we retrieve the user type from env variable. If the function is called from API, we will skip setting the questions.
Otherwise, we will have questions set on the terminal.
Next, we will call init_props() to set `self.props` which is what we will mainly talk about.
After that, we will get height and width here since almost all models use them.

`screen on lib.utils.py init_props()`  
In `init_props()`, we will call the function `PropArgs.create_props()`. 
There are some parameters, `model_dir` is the directory path of the model and `model_nm` is the name of the model,
they are used to generate the path of the `[MODEL_NAME].props.json`(say `props` in the video) file.
`props` is the dictionary of the parameters I just mentioned. 
`skip_user_questions` is to set whether we need to generate questions in the terminal.
Okay, let's move on.

`screen on propargs.proargs.py`  
In `create_props()`, we will initialize an instance of class PropArgs and return.

`screen on propargs.proargs.py __init__()`  
There are two ways to initialize `self.props`: from file or directly from a dictionary.  
If we pass a props file, we will call `json.load()` first to convert the content of the json file into a props dictionary.
Then we call `set_props_from_dict()` to retrieve the values in the props dictionary and put them into `self.props`.  
If we pass a props dictionary, we directly call `set_props_from_dict()` to put values into `self.props`.
Remind that if we pass both props file and props dict, values set by the props file will be overwritten by the values in
the props dict since values in the props dict is set after the props file.

Let's jump into set_props_from_dict() to see what's going on there.   
`screen on proargs.property_dict.py def set_props_from_dict(prop_args, prop_dict)`  
For each parameter.
We ensure the attribute `val` to be the same type as the input `atype` (do type casting if necessary). 
We simply retrieve the value of all other attributes and initialize an instance of class `Prop`.

After this, we finally dit it! We now have `self.props` with all the values we set either directly by passing the dictionary or from the configuration file.  
`screen go back to segregation.py.handle_props()`  
Let's go all the way back. Now, we can get values of the parameters.   
`screen on lib/model.py.get_prop()`  
We actually do not retrieve value directly from `self.props` but call a method in the class called `self.get_prop()` to
hide the `self.props` because we want it to be read-only to cause less trouble.
Passing the name of the parameter into `self.get_prop(prop_nm)` and get the value.
In segregation model, we need to get the density of each group and calculate the area by the width and height.
Then we can set the number of members of each group.

Up to now, I believe you have got the spirit of how `handle_props()` works. Let's move on and see its effect.

## Play around with handle props
`hover over def handle_props`  
Last time in the general tutorial, we present how we can specify parameters with user questions in the presentation of forest_fire model.  
But we simply set constant values for the parameters in the transformation from 
basic model to segregation model since it is more straightforward way to set parameters. 
After all the explanations above, it is a good time to put it into practice and see how it goes. 
If we don't want to assign a constant value to a parameter but rather from a configurable file and maybe even compute the values by other properties, 
this would be the perfect approach that you are looking for.  

```
"""
Thomas Schelling's famous model of neighborhood segregation.
"""
def handle_props(self, props):
    super().handle_props(props)
    # get area
    area = self.width * self.height
    # get percentage of red and blue
    dens_red = self.get_prop("dens_red")
    dens_blue = self.get_prop("dens_blue")
    # set group members
    segregation_grps["red_group"][mdl.NUM_MBRS] = int(dens_red * area)
    segregation_grps["blue_group"][mdl.NUM_MBRS] = int(dens_blue * area)
```

`copy and paste the above code to replace the previous handle_props function which just did constant assignments`  
Here, for the blue group members and red group members, we don't want a constant like 200 that is fixed, but a formula to calculate it based on the blue density and red density parameters we specified.   

If we choose run for N periods in the menu, and run for 1 period. We can see the blue and red members are no longer the 250 which we specified as the default value. 
`run the model again to see effect`

We get the value from the density value times the area, which is 0.33, the default density value, times by area, which is 40*40.   
This computation will get the blue or red member that we got now, that is 528.   
`hover over the terminal result: group census blue_group: 528, red_group: 528`

We can also get rid of handle_props function if you don't think this kind of computation is needed for your parameters. 

`scroll up and highlight to show line 11 and 12 NUM_RED and NUM_BLUE parameter`
In that way, the blue members and red members will use the default value that we specified earlier in this file, which is 250. 

`delete handle_props function and run the model again to show that the program is now using the default value 250`

## Handling props from the web
`open browser and copy and paste in url https://tandondevops.github.io/IndraFrontend/#/`  
Besides running your models through terminal, we also have a web-based frontend interface to show our ABMs. You can see it directly from here, that we have a drop-down menu for the user to select a model. 
Those models can be prepopulated from the configuration, which means you can have your own customized model to be shown here if you want!

`select forest fire from drop-down menu`  
If we proceed with selecting the forest fire model here, our page will show us four questions that are the same as the questions that we will get from terminal.  
These questions are read from the same configuration file which is the `[MODEL_NAME].props.json` file. 

`mouse point to one of the input box's gray default value`  
We can see in the input box, we have the default value in gray, like grid height & width should be 40.   
If we do want to specify a value, we can type in the input box, just like we will type in a customized value in terminal before we hit enter.

`click on submit and click on run with the default 10 periods`  
Here we can see a more visual-friendly graph than on the terminal.   
We have the output from the terminal in the section of model status shown on the right, as well as the scatter plot at the bottom. 

Basically, we keep the workflow consistent throughout both terminal and web. This should just be a brief overview to get you know we have the web option to get to show your models!

## End
This concludes our condensed video tutorial that focuses mainly on handling parameters.  
Please feel free to contact us if you have any questions.  
Also, feel free to comment or start an issue track on the specific topics that you want to dive into.  
We may consider producing more of those short video tutorials if those help!
