# A Big-box vs. Mom-and-pop's Dilemma

Eugene Callahan, Nhi Pham, Kangqing He, Nathan Conroy

## Abstract
Conventional wisdom from "free market" economists would have it that moves to ban "big box" retailers such as Walmart from certain localities are rebellions against consumer sovereignty and must hurt consumer welfare. After all, if consumers did not want to shop at the big box retailer, they would simply not do so, correct? The fact that they switch their shopping to the big box and away from "mom-and-pop" stores show they prefer the big box.
This paper attempts to show that such analysis is simplistic. We present a model in which all consumers have the following preference ordering in some retail sector:
1. Have both local shops and the big box store.
2. Have only local shops.
3. Have only the big box store.

We then show that, under not outrageous assumptions, it is easy for consumers, in trying to achieve their first preference, to instead wind up with their third. This is due to consumers facing a prisoner's dilemma, as well as knowledge problems: Consumers might, if they had perfect knowledge of the exit points of the local shops and the ability to finely coordinate their own shopping, be able to achieve their first preference (a mix of big box and mom-and-pop shopping available). But, in general consumers have little knowledge of how much sales must be reduced before a small shop will exit the industry, nor do they have very much ability to coordinate their shopping with other consumers. Therefore, since they cannot fine tune their shopping to achieve 1), they shop at the big box store whenever it suits them for a particular purchase, without regards to the "macro" effects of their choices. The end result is that all of the mom-and-pops are driven out of business, despite no consumer wanting that result. Thus, it may make sense, faced with such knowledge and game theoretic difficulties, for consumers to bind themselves in advance to 2), by banning a, or some, or all, big box stores.

## Introduction & Literature Review
In economics, mom-and-pop stores often refer to small local businesses, some of which include local restaurants, bookshops, and grocery stores. Big-box retailers are stores that are often located in large-scale buildings and offer a wide range of goods, such as clothing, groceries, and hardware, to its customers at a discount price. It is inevitable that traditional mom-and-pop stores are often put in a financially challenging position when competing with large chain stores, especially when big-box retailers have much greater capital to sustain their business. Although being placed at a disadvantage in the business world, some local stores can still coexist with giant retailers, or even thrive and dominate the market. A possible step towards understanding this phenomenon is agent-based modeling (ABM) where we aim to simulate different retail environments by experimenting with different values of key behavioral characteristics of consumers, big-box retailers, and mom-and-pop stores. We investigate several key attributes that influence the consumer's choice to shop at big-box retailers or at mom-and-pop stores such as the density of local stores and consumer preferences. Using ABM with adjustable attributes, our model provides a set of simulations under different conditions and offers insights of big-box vs. mom-and-pop survivals in the market. By assigning different values for such attributes and letting these individual agents interact with each other in the simulated environment, the emergent outcome of the micro behaviors can resemble real-world scenarios and allow us to gain a better understanding of the retail market. Implications from our agent-based method also provide a better explanation for the growth or decay of big-box retailers and mom-and-pop stores' populations in comparison to top-down approaches that try to capture the complexity of the phenomenon through differential equations.

In addition, there has been work on constructing theoretical models of big-box retailers and mom-and-pop stores. 

## Theory & Methodology
### Theoretical Approach
### Our Model Design
The design of our model includes 2 main files: 
1. [IndraABM/capital/bigbox.py](https://github.com/TandonDevOps/IndraABM/blob/staging/capital/bigbox.py): contains the code for the main functions of the model, including:
- **Consumer-related functions**:
    - *get_rand_good*: randomly assign each consumer's needed item after each run. 
    - *create_consumer*: create a consumer with attributes name, spending power, previous utility, and good to purchase.
    - *consumer_action*: determine the best seller to purchase the needed item.
    - *utils_from_good*: calculate the utility if good is purchased at a specific store. If store is a big-box, there is no preference and function returns value -1.0; else if store is a mom-and-pop, utility is calculated as (a random double between 0.0 and 1.0 + store's adjusted utility) * consumer's preference.
    - *choose_store*: given a list of sellers within consumer's maximum commuting distance, choose the store with the highest utility.
- **Retailer-related functions**:
    - *sells_good*: return if store sells needed good. If store is a big-box, function always returns true.
    - *create_mp*: create a mom-and-pop store with attributes name, expense, initial capital, available goods, and utility adjustment.
    - *create_bb*: create a big-box retailer with attributes name, expense, and initial capital.
    - *retailer_action*: calculate retailer's capital after every period and determine if a retailer goes out of business.
    - *transaction*: when a transaction is made, money from consumer is added to store's capital. 
- **Environment functions**:
    - *town_action*: determine when a big-box retailer is created in town.
    - *handle_props*: adjust values for key attributes based on user inputs; otherwise use default values.
2. [IndraABM/capital/props/bigbox.props.json](https://github.com/TandonDevOps/IndraABM/blob/staging/capital/props/bigbox.props.json): contains questions for all customized attributes. For each question, user can choose to input in a value (e.g. integer/double) between a lower bound and an upper bound, or choose to use the default value assigned by the system. Key attributes include:
    - *Density of consumers*: double value with default value 0.05, within range [0.01, 0.7].
    - *Density of local stores*: double value with default value 0.3, within range [0.1, 0.3].
    - *Consumer preference for local stores*: double value with default value 0.1, within range [0.0, 0.4].
    - *The maximum commuting distance to the store*: integer value with default value 2, within range [1, 5]
    - *Big-box vs. mom-and-pop's capital multiplier*: determine how much more funding a big-box retailer would have than mom-and-pop stores do; default value 10, within range [10, 100]
    - *Period when a big-box retailer appears in town*: integer value with default value 7, within range [1, 15]

In our design, there are 5 available types of goods: books, coffee, groceries, hardware, and meals. Each mom-and-pop store is randomly assigned with expense, initial capital, and utility adjustment. User can assign the number of consumers and mom-and-pop stores in the environment, but at most 1 big-box retailer exists in town for all periods. After a number of periods, the equilibrium in the simulated environment may be reached. This implies that there will be likely no future transaction happening between consumers and retailers, and thus the current outcome can be considered as the final result.

## Empirical Evidence
## Conclusion
## Bibliography
## Acknowledgement
Authors are listed in order of contribution.

