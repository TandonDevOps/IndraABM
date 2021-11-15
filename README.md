Indra Model Generator
=====
This is the project folder for Indra Model Generator. 

The project aims to build a python model generator for Indra. 

Team Members
---------------------------
Ruinan Zhang | rz1109@nyu.edu 

Pankhuri | pp2535@nyu.edu

Zijie Dong | zd2036@nyu.edu

Jingyi Lu | jl11525@nyu.edu

Team Meeting 1 - Week 2 - (09/17/2021)
---------------------------
Task 1:  Each group member should investigate 2-3 existing models Indra has and document in this md file.  
Collect information about: kind of surveys/number of groups/different group structures..... and more   

### Basic Model: 
This is a minimal model that inherits from model.py and just sets up a couple of agents in two groups that do nothing except move around randomly.
For Basic Model, 4 parameters used for initial settings : `GRID_HEIGHT`, `GRID_WIDTH`, `NUMBER_OF_BLUE_AGENT`, `NUMBER_OF_RED_AGENT`. 
There are two group : **red agents** and **blue agents**.
 For each period of run, each agent just move around randomly on the plot. 

### Adam Smith fashion model:  

For the Adam Smith Fashion model, 4 parameters used for initial inputs: `GRID_HEIGHT`, `GRID_WIDTH`, `NUMBER_OF_FASHION_FOLLOWERS`, `NUMBER_OF_FASHION_TRENDSETTERS`.
The model starts with all trendsetters are red and all followers are blue. 

In this model, the dynamic between trendsetters and followers can be described as following : as the trendsetters (the elite group) want to be unique, when they see followers (the normal people) start to follow their trend and wear the same thing, they will switch to a new trend. And as followers see trendsetters change preference, they will start to follow the new trend.

For both trendsetters and followers, after each period of time move, a small value will be added to the “Neutral” preference value each of them holds. And if the value is big enough, it will change their preference and switch to new "trend". Thus after some rounds, the color of agents within followers and trendsetters started to change color based on a formula continuously. 

### Forest Fire:
There are four inputs: the grid height, the grid width, the probability a tree will catch fire on its own, the dense of the tree. Each tree has five state: `HEALTHY`, `NEW_FIRE`, `ON_FIRE`, `BURNED_OUT`, `NEW_GROWTH`.

At the very beginning, each `HEALTHY` tree has probability to catch fire on its own (from outside the model), then it will turn to `NEW_FIRE` state, then it will turn to `ON_FIRE` state.  After that, it will turn to `BURNED_OUT` state, and all its neighbors will catch fire and become `NEW_FIRE”`state. 
The more dense of the tress, the easier and faster the fire spread.  
 Finally, the `BURNED_OUT` tree will become `NEW_GROWTH”`and return to `HEALTHY”`state. 

 There are also factors that effect a forest fire. Some of which include: 
    * Wind Speed
    * Wind Direction

### Schelling's Segregation Model:
It has 7 inputs:  `GRID_HEIGHT`, `GRID_WIDTH`, `THE_DENSITY_OF_BLUE_AGENT`, `THE_DENSITY_OF_RED_AGENT`,`THE_TOLERANCE_OF_AGENTS` , `THE_STANDARS_DEVIDATION_OF_AGENTS`,`THE_SIZE_OF_AGENT_NEIGHBORHOOD`

The model illustrates how individual tendencies regarding neighbors can lead to segregation. 

The model is especially useful for the study of residential segregation of ethnic groups where agents represent householders who relocate in the city. In the model, each agent belongs to one of two groups and aims to reside within a neighborhood where the fraction of 'friends' is sufficiently high: above a predefined tolerance threshold value **F**. It is known that depending on **F**, for groups of equal size, Schelling's residential pattern converges to either complete integration (a random-like pattern) or segregation.

In this specific code piece, each time, we will calculate the `hood_ratio` of each agent. The greater number of neighborhood in the same group, the higher the `hood_ratio`. 
Each agent has its own `tolerance`. The `tolerance` is calculated based on the input `tolerance` plus some random number. 
If the `hood_ratio` is higher than `tolerance”` this agent will move. 

### El Farol Bar:
The problem says that on Thursday night, 100 people decide to go to the bar in El Farol, Santa Fe. And only a certain number of people will be present inside the bar that day. So, there are two cases : 
1) If more than 60 per cent of people will go to the bar on a particular day. They will have less fun in comparison to those at home.
2) If less than 60 per cent of people will go to the bar on a particular day. They will have more fun in comparison to that at home.

For this model, two parameters are used: `POPULATION_OF_THE_TWON` and `MEMORY_CAPACITY_OF_DRINKERS`.

So, through the python code of this model, we aim to find if the agent will go to the bar. To reach the solution, first, we will take an array. The integers in the array represent the agent's memory of earlier days in the bar. The more recent the memory is, the more weight it has. The sum of the array is calculated.

The function `memory_check` will check the capacity of the bar. 
The decision is based on the agent’s memory of previous nights of how crowded the bar was. If the conclusion of the agent is that bar is a crowded place, then he will not go there, and vide-versa. Once, the agent goes to the bar, the array gets appended with a new integer (i.e. new memory of the bar).

### Menger's Origin of Money:

A group of agents are placed in the environment, which randomly move and do a trade with each other. 
The key of this model is each agent just tries to find the commodities that can be traded easily, in this process, it emerges out one product that is most easily traded and it would become money.
The parameters used by the model are `Grid height`, `Grid width`, `Number of traders`, `Divisibility consideration`, `Durability consideration` and `Transportability consideration`. The commodities contain certain characteristics. These characteristics have been assigned some initial values. The outcomes for two types of commodities are calculated. If the outcome is accepted, then there will be a trade between trade 1 and trade 2.  Also, the variable, `eq_counts`, which is a counter for counting the number of continuous periods with no trade, is computed. The conclusion if the trade can take place in between two traders can be calculated through the variable `EQUILIBRIUM_DECLARED.`. If `EQUILIBRIUM_DECLARED` is greater than  `eq_counts`, then there will be no trade between two traders, and vide-versa.

### Big-box
Parameters for this model: `grid height`; `grid width`; `density of consumers`; `density of mom and pop`; `customers’ willingness to choose mom and pop`; `the farthest distance to shops that is acceptable for customers`; `the ratio of the fundings of big box vs. mom and pop`; `the period of appearance of big box store`

The model illustrates how the rise of **big-box retailers** (national chains that are often located in large-scale buildings and offer a wide range of goods, such as clothing, groceries, and hardware, to their customers at a discount price) could displace smaller, often family owned (a.k.a. **Mom-and-Pop**) retail establishments. 
Traditional mom-and-pop stores are often put in a financially challenging position when competing with large chain stores, especially when big-box retailers have much greater capital to sustain their business.
The model is to simulate different retail environments by experimenting with different values of key behavioral characteristics of consumers, big-box retailers, and mom-and-pop stores.


### Firefiles

Model parameters: `grid height`; `grid width`; `density of the fireflies`

This model illustrates the spontaneous synchronization of large crowds without a central central clock or synchronization tool. 
As in isolation, single agent ("firefly") look similar to conventional LED cycling safety lights, but in groups exhibit an immediately noticeable and striking phenomenon of unified flashing. 

In this model, the agents (fireflies) start changing color (blinking) at random frequencies. However, at each simulation run, the agents increase or decrease the frequencies based on the average of neighbor agents' blinking frequencies. After a certain number of simulation runs, we see that all of the agents are blinking at the pretty much same frequency.

This behavior is shown by calculating the standard deviation in the blinking frequencies with the environment action.

Team Meeting 2 - Week 3&4 - (09/28/2021)
---------------------------
Meeting Summary: Went through each model summary and talked about preparation tasks for initial design
Task1 : Modify the model descriptions based on prof’s comments. (Ruinan)
Task2 : Summarize the different capability needed in the models’ actions (All members. Zijie model 1-4, Pankhuri model 5&6, Ruinan model 7, Jingyi model 8)
Task 3: Select useful information from improved model descriptions and add them to the python file docstrings. (Pankhuri)
Task 4: Initial design (API) for model generator. (All members, Jingyi research on current APIs)