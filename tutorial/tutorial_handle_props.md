# Tutorial of handling props

> Since handling props in Indra system requires advanced skills to fully understand, 
> we make another video delving into it.
>
> This file is served as a script and a document of tutorial video for handling props.

## Main structure
1. introduce the structure of the `[MODEL_NAME].props.json`
2. analyse and explain handling props
3. change code and show how handling props works(setting parameters in the terminal lines)
4. mention handling props on the web

## Introduction of `[MODEL_NAME].props.json`
Handling props is basically setting values of the parameters in the model. In Indra system, you are asked several
questions to set parameters when you run the model in the terminal mode. The parameters and the questions are 
defined in the `[MODEL_NAME].props.json` file.  

Next I will show you one example to help you understand the general structure/format of the file.  
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
