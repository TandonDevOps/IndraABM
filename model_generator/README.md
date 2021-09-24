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

Forest Fire:
There are four inputs: the grid height, the grid width, the probability a tree will catch fire on its own, the dense of the tree. Each tree has five state: HEALTHY, NEW_FIRE, ON_FIRE, BURNED_OUT, NEW_GROWTH.
Each HEALTHY tree has probability to catch fire on its own, then it will turn to “NEW_FIRE” state, then it will turn to “ON_FIRE” state. After that, it will turn to “BURNED_OUT” state and turn all neighbor tree into “NEW_FIRE” state. Finally, the “BURNED_OUT” tree will become “NEW_GROWTH” and return to “HEALTHY” state. 

Schelling's Segregation Model:
It has 7 inputs: the grid height, the grid width, the density of blue agent, the density of red agent, the tolerance of agents, the standard deviation of the tolerance of agents, the size of agent neighborhood. 
Agents want to live with neighborhood in the same group. Each time, we will calculate the “hood_ratio” of each agent. The greater number of neighborhood in the same group, the higher the “hood_ratio”. 
Each agent has its own “tolerance”. The “tolerance” is calculated based on the input “tolerance” plus some random number. 
If the “hood_ratio” is higher than “tolerance”, this agent will move. 

