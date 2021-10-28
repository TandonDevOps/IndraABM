Indra Model Generator -- Actions Summary
---------------------------
### Basic Model:   
	basic_action:
		`get_pos()`: Get the current position. 
		
		`get_neighbors(agent)`: Get the neighbors of the agent. 

### Adam Smith's Fashion Model:   
	common_action:  
		`ratio_to_sin()`: calculate a value which identify how many people wear the same color in the environment. 
		
		`new_color_pref(agent[COLOR_PREF], env_color)`: get the new preference of this agent.   
		
		`dont_like_things(agent[DISPLAY_COLOR], agent[COLOR_PREF], op1, op2)`: check if the agent like the current color or not. 
		
		`change_color(agent, opp_group)`: Change the color of agent to the opp_group. 
		
### Forest Fire model:   
	tree_action:  
		`exists_neighbor(agent, lambda agent: agent.group_name() == ON_FIRE)`: Check if it exists at least one neighbor tree on fire.  
		
		`prob_state_trans(int(curr_state), state_trans))`: Calculate the probability which it catches on fire spontaneously.  
		
		`add_switch(agent, old_group, new_group)`: Switch the state. 
		
### Schelling's Segregation Model:  
	agent_action:   
		`get_prop(agent.exec_key, "hood_size", default=4)`: Find out the neighborhood size.
		
		`neighbor_ratio()`: Calculate the percentage of neighbor which this agent like.   
		
		`get_tolerance()`: It will calculate the tolerance of this agent.   
		
		`env_favorable(ratio_num, tolerance)`: See if it will move out or not. It will move if the tolerance > ratio_num.   



### Big box:

In this model, main customized actions for agents could be divided into two groups: 
- Actions for **Consumers** 

		- **Main function:** **`consumer_action(consumer, **kwargs)`** : check shops near consumer and consumer decide which shop consumer will go to buy the needed good. This function takes a `consumer` object;  
		
		- `create_consumer(name, i, action=None, **kwargs)` : create a consumer with attributes name, spending power, previous utility, and good to purchase. This is used in the consumer_action to create consumer object;  
		
		- `choose_store(consumer, sellers)` :  given a list of sellers within consumer's maximum commuting distance, choose the store with the highest utility. This function is used in the `consumer_action` function above as the store selection part of it;  
		
		- `get_rand_good()` : randomly select an item as consumer's needed good after each run;  
		
		- `utils_from_good(store, good)` : utils_from_good(store, good): calculate the utility if good is purchased at a specific store. This is used in `choose_store` function; 
		 
- Actions for **Retailers**

		- **Main Function: `retailer_action(store)`** : common action for both mom_and_pop and big-box stores to deduct expenses and check whether the store goes out of business. It calculate retailer's capital after every period;   
		
		-  `sells_good(store)` : Return True if store sells the good the consumer needs. For Big-box store, as it always sells item needed, thus return True. For consumers always return False and for Mom-and-pop store it checks if it sells the needed item; 
		 
		- `create_mp(store_grp, i, action=None, **kwargs)` :  create a mom-and-pop store with attributes name, expense, initial capital, available goods, and utility adjustment;  
		
		- `create_bb(name, mbr_id, bb_capital, action=None, **kwargs):` create a big-box retailer with attributes name, expense, and initial capital;  
		
		-  `transaction(store, consumer)` : add money to the store's capital from consumer;  
  
- User Input for this model:   
1. Group of agents: consumer, retailers(big-box and mom-and pop). 
2. Properties and attributes for each agent. For example, consumer agent : name, spending power, previous utility, and good to purchase;  
3. Customized actions for each agent.   

### El Farol Bar:
`get_decison(agent)`:Random decison taken by the agent<br/>

`weighted_sum(arr)`:Returns a weighted sum of the array, which contains agent's memory of population of the bar in the past, considering the fact that recent memories weigh more.<br/>

`memory_check(agent)`: The percentage of people present in the bar, when the agent last visited the bar. <br/>

`drinker_action(agen, kwargs)`: The final decison taken by the agent, to go or not to go. The decision will be based on agent`s recent memory of population of people present in the bar.<br/>

`create_drinker(name, i, exec_key = None, action=drinker_action)`: Creates an agent and assigns a random value of motivation.<br/>

### Menger`s Origin of Money:
- `create_trader(name,  action, kwargs)`: To create the agent, trader.<br/>

- `trader_action(agent, kwargs)`: To add the commodity to the trader`s list.<br/>

- amt_adjust(nature): Function to change the amount of commodity considering the divisibility parameter.<br/>

- nature_to_trader(traders, nature): Function to provide the trader with initial income.<br/>

- incr_ages(traders): To increment the duration of the good, owned by the trader, by 1.<br/>

- check_props(is_div, is_dura, is_trans): Deletes goods from the list, considering parameters like divisibility, durability and transportability.


### Fireflies

- Main Action: `firefly_action`

A firefly decides whether to blink or not.

In this action, the firefly would first invoke `adjust_blink_freq` to adjust its blinking frequency based on the current state. 

Then it invokes `to_blink_or_not` which returns the updated state of the agent

Finally, if the state is to be changed, then invoke `switch_state` to update the state.

- Others:

`create_firefly` create agent(s)

`calc_blink_dev` environemnt action which calculates the std deviation. (for system output)

- Model Parameters: 

`grid_height`

`grid_width`

`density`
