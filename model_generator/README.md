Indra Model Generator
=====
This is the project folder for Indra Model Generator. 

The project aims to build a python model generator for Indra. 

Team Members
---------------------------
Ruinan Zhang | rz1109@nyu.edu 

Pankhuri | pp2535@nyu.edu

Zijie Dong | zd2036@nyu.edu

Team Meeting 1 - Week 2 - (09/17/2021)
---------------------------
Task 1:  Each group member should investigate 2-3 existing models Indra has and document in this md file.  
Collect information about: kind of surveys/number of groups/different group structures..... and more   

### Basci Model: 
This is a minimal model that inherits from model.py and just sets up a couple of agents in two groups that do nothing except move around randomly.
For Basic Model, 4 parameters  used for initial settings are grid heigh, grid width, number of blue agent, number of re agent. 
There are two group : red agents and blue agents. For each period of run, each agent just move around randomly on the plot. 

### Adam Smith fashion model:  

For this model, 4 parameters used for initial settings are grid heigh, grid width, number of fashion trendsetters and number of fashion followers. 
There are 4 groups : blue trendsetters, red trendsetters, blue followers and red followers. The model starts with all trendsetters are red and all followers are blue. For both trendsetters and followers, after each period of time / move, a small value will be added to the “Neutral” preference value each holds, which means if the small value is big enough, it will change their preference and they will become “don’t like sth anymore”. Thus after some rounds, the color of agents within followers and trendsetters started to change color based on a formula continuously. 

### Forest Fire:
There are four inputs: the grid height, the grid width, the probability a tree will catch fire on its own, the dense of the tree. Each tree has five state: HEALTHY, NEW_FIRE, ON_FIRE, BURNED_OUT, NEW_GROWTH.
Each HEALTHY tree has probability to catch fire on its own, then it will turn to “NEW_FIRE” state, then it will turn to “ON_FIRE” state. After that, it will turn to “BURNED_OUT” state and turn all neighbor tree into “NEW_FIRE” state. Finally, the “BURNED_OUT” tree will become “NEW_GROWTH” and return to “HEALTHY” state. 

### Schelling's Segregation Model:
It has 7 inputs: the grid height, the grid width, the density of blue agent, the density of red agent, the tolerance of agents, the standard deviation of the tolerance of agents, the size of agent neighborhood. 
Agents want to live with neighborhood in the same group. Each time, we will calculate the “hood_ratio” of each agent. The greater number of neighborhood in the same group, the higher the “hood_ratio”. 
Each agent has its own “tolerance”. The “tolerance” is calculated based on the input “tolerance” plus some random number. 
If the “hood_ratio” is higher than “tolerance”, this agent will move. 

### El Farol Bar:
The problem says that on Thursday night, 100 people decide to go to the bar in El Farol, Santa Fe. And only a certain number of people will be present inside the bar that day. So, there are two cases -
1) If more than 60 per cent of people will go to the bar on a particular day. They will have less fun in comparison to those at home.
2) If less than 60 per cent of people will go to the bar on a particular day. They will have more fun in comparison to that at home.

For this model, two parameters are used: population of the town and memory capacity of drinkers.
So, through the python code of this model, we aim to find if the agent will go to the bar. To reach the solution, first, we will take an array. The integers in the array represent the agent`s memory of earlier days in the bar. The more recent the memory is, the more weight it has. The sum of the array is calculated.
 The function 'memory_check' will check the capacity of the bar. 
The decision is based on the agent’s memory of previous nights of how crowded the bar was. If the conclusion of the agent is that bar is a crowded place, then he will not go there, and vide-versa. Once, the agent goes to the bar, the array gets appended with a new integer (i.e. new memory of the bar).

### Menger's Origin of Money:
A group of agents are placed in the environment, which randomly move and do a trade with each other. The parameters used by the model are Grid height, Grid width, Number of traders, Divisibility consideration, Durability consideration and Transportability consideration. The products considered in the code are a cow, gold, cheese, banana, diamond, avocado, stone, and milk. The commodities contain certain characteristics. These characteristics have been assigned some initial values. The outcomes for two types of commodities are calculated. If the outcome is accepted, then there will be a trade between trade 1 and trade 2.  Also, the variable, " eq_counts", which is a counter for counting the number of continuous periods with no trade, is computed. The conclusion if the trade can take place in between two traders can be calculated through the variable "EQUILIBRIUM_DECLARED. ". If EQUILIBRIUM_DECLARED is greater than  eq_counts, then there will be no trade between two traders, and vide-versa.
