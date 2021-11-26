# The Origin of Money: An Agent-Based Model of Carl Menger's Theory

Eugene Callahan and Peiwen Tang

## Introduction

Carl Menger famously, in his 1892 paper, "On the Origin of Money,"
offered an *emergent phenomenon*
theory of how humans came to employ a *medium of exchange* (money) for most
transactions: it is unlikely, he held, that people with no experience with some
good gradually *emerging* as a medium of exchange could simply invent money *ab
nihilo*. Instead, one good would, over time, come to be understood as widely
exchangeable: and that recognition, in itself, would make the good a more
attractive acquisition in future possible exchanges.

But Menger went further, and analyzed *why* certain goods were particularly
suited to take on the role of medium of exchange. Such properties as
*divisibility*, *durability*, and *ease of transport* would all increase the
likelihood that a good would emerge as a medium of exchange.

It is not easy to test a theory like Menger's: it is unlikely that society will
allow the interested scientist to wipe clean all members' knowledge of money
and wait to see if a medium of exchange spontaneously emerges. (Examples like
the WWII POWs who used cigarettes as money are somewhat tarnished by the fact
that such prisoners already had experience with using money.) However,
*agent-based models* (ABMs), while certainly not real societies, can be
programmed so that the *agents* they contain "act like" real economic agents in
some important respects. And, as a leading tool in exploring emergent
phenomena, it seems appropriate to use an ABM as a way to explore the
plausibility of Menger's theory.

## The World in the Model

An initial question that may strike the reader is, "Of what relevance 
could a simple computer model have for examining a historical hypothesis
about what occurred in the real world?" We point such a reader to Mary 
Morgan's work *The World in the Model*.

According to Morgan:

"Writing down a model and manipulating it allows economists to think through in
a consistent and logical way how a number of variables might interrelate, and
to find solutions to questions about such systems. This habit of making and
using models extends the powers of the mind to ask questions and explore the
answers in complicated cases." (p. 258)

Morgan discusses how models aid in classification: “Such model experimental
work allows the economist to test out intuitions and ideas and so come to
understand what the laws of demand and supply mean in different
circumstances” (p. 272) [RELEVANT??]

In short, setting up a model in which we can watch money emerge (or not) allows
us to explore the relations between the different factors Menger held to be
important in its emergence. At the very least, if varying these factors can
cause a good in the model to emerge or fail to emerge as money, we show that
Menger's model is logically coherent.

**Agent-Based Modeling**

We want to reproduce an environment so that trades can happen based on the key factors
concluded by Menger, and based on the trading results, we could thus discuss whether
Menger's theory is valid or not. Agent-based modeling is the one we select to recreate
the trading market. As defined by Epstein and Axtell in their book *Growing Artificial Societies*,
agent-based model is an interpretation of an "artificial society", and within it, "fundamental
social structure and group behaviors emerge from the interaction of individuals operating in
artificial environments under rules that place only bounded demands on each agent's information
and computational capacity." (p. 4)  Epstein and Axtell also mentioned the three major components
of agent-based models: agents, environment, and rules. In our case, agents are served as the rational
humans in the society; rules are the "Menger factors",
the characteristics that draw people's attention
to trade-in or trade-out certain goods; environment is a platform we want to provide to the people in
this artificial environment such that people can select the ones to trade with, and like what happened
in the real-world, people need to walk around in order to interact with each other. Fulfilling the
needed conditions makes agent-based modeling an optimal choice to implement Menger's theorem.


## Menger's Theory

Starting from the basic idea that a commodity should be traded by its
owner in exchange for another more useful to him,
Menger looks back to an
"uncoined state.“ Menger seeks to discover 
the causes behind the emergence of a good as money.
 
A naive view of barter is that an agent will only seek
to exchange in order to acquire what he/she directly wants.
However, that would result in a very limited number of trades,
because of the difficulty in finding "mutual coincidence of wants":
trades would only occur when you have "extra" of what I want, while I have
extra of what you want. Thus, it may make sense to trade my surplus goods for
some other goods I don't need myself, *if* the goods I acquire are easier to
trade than those I surrendered.

Menger realized that this ease of trading was an emergent social phenomenon:
the more economic agents realize that good A is relatively easy to trade, the
greater the ease of trading becomes. Thus we have a network effect, similar
to that we see with a social media platform: the more people on a platform, the
mode people want to get on the platform, since there are more people there with
whom to interact.

He also pointed out 
that it is incorrect to assume that *all commodities, at a
definite point of time and in given market, may be mutually exchanged in
definite quantities at will.* (pg. 23)
[IS THAT A QUOTE??? AND IS IT RELEVANT?]

Menger sees that trading can hardly just follow
our willingness, and there exists a gap between wholesale price and retail
price in reality, that in the barter system, we
are not likely to have a fixed ratio of how many unit of 
good A can be traded into a certain unit of good B
during every round of trade, that is, there's no so-called 
"price" while exchanging goods.
 
Menger listed three categories of factors that influence the degree of 
salebleness of goods, and they cover buyers’ own
interest (which we model as the utility the agent assigns to the next unit of the
good), the goods’ own characteristics
(what we will to focus on), and external factors (which we will ignore). 

The circumstantial influencer includes the number of people involved in the trading with their 
characteristics, including their degree of willingness and their purchasing power, the divisibility 
of the good itself and the environmental factors like the market and regulation maturity; the spatial 
limits comprises the geographical distribution of the good, the cost and easiness of transportation, 
availability of the corresponding means of transportation towards different goods, and the development 
of the trading market; the time limits incorporate factors like for how long does one need the good, the 
durability of the good, the preservation cost, the rate of interest of the good, and market periodicity.

Under the above listed circumstances and limits, goods are divided into two
categories: those one directly wants, or, those that can be exchanged. When
anyone has brought goods not highly saleable to market, the idea uppermost in
his mind is to exchange them. One reason is that the goods cannot be directly
used by him/her. But another intriguing reason why one chose to purchase the
item is that someone else may want it. As saleableness of goods encounter both
objective (i.e. goods’ characteristics) and subjective (i.e. personal interest)
factors, it can be greatly different for each one, and thus different people
can have different levels of willingness to purchase/sell a goods.

As Callahan (2004) discusses listed, "historically, a great variety of goods has been used as a 
medium of exchange: cows, salt, cowry shells, large stones, exotic feathers, cocoa beans, 
tobacco, iron, copper, silver, gold, and more. " (p.83) Every possible item owned by people 
could possibly become a medium of exchange. Menger then looks at the "saleability" of different 
by examining the following criteria:

*These wares would be qualified by their costliness, easy transportability, and
fitness for preservation (in connection with the circumstance of their
corresponding to a steady and widely distributed demand), to ensure to the
possessor a power, not only “here” and “now” but as nearly as possible
unlimited in space and time generally, over all other market-goods at economic
prices.* (Menger, 1892, p. 35)
 
He concludes that the precious metals, especially silver and gold, often best
fulfill all the criteria for serving as money:

- Divisibility: The homogeneity of precious metal easily allows people to
control the quality and weight when dividing them, without having unequal 
value for different portions.
- Durability: Precious metal have almost unlimited durability
and cost little to preserve.
- Transportability: The demand for the precious metals 
is well distributed geographically, and their high value to
weight ratio makes them easy to move.

## Critiques of Menger

David Graeber (2011) makes the case that Menger's theory is just historically wrong:
that, in fact, the precious metals became money by government fiat.
Whether he is correct or not is a question for detailed historical research,
not for an agent-based model. Here we are only interested in the *plausibility*
and *implicaitons* of Menger's theory, not whether he describes an actual
historical process.

Hodgson (1992) doubts that "the main problem with Menger's theory is that, given
potential quality variation, the spontaneous process of evolution of the monetary unit may break
down, possibly requiring the intervention of the state or central bank to
maintain the currency unit." He points out the issue of 
"potential adulteration and debasement of commodities".
Moreover, Hodgson insists the importance of the *state*,
which can control the variation of money caused
by adulteration. He makes the point that government intervention shall be a crucial part of gold 
emegring of money.
 
The adulteration concern introduced by Hodgson is not of concern for our project
for the following reason: Money adulteration is a phenomena that occurs to a good that
*has* emerged as money. Therefore, this problem occurs *after* the Mengerian process
of money's emergence.
 
Furthermore, government control of money issuance may not be as innocent
Hodgson thinks. Ford (2014), discusses the earliest money 
adulteration, which is dominated by the government itself, "The Roman government even
created their own fake gold coins.
This was done primarily through debasement, using less and less gold over time. Of course,
they demanded that they value of exchange be kept the same, even implementing
draconian laws to enforce their wishes."

 
**Why can we don't include state/regulation in our modeling:**
 
Background: One of the circumstances that affects the degrees of salebleness (quoted above) is the impact of 
regulation. Hodgson also mentions for several times on the importance of government intervention.
 
Ikeda states that "according to Menger, a sound monetary system does not
require legal sanctions, and is not predicated upon the explicit agreement of
market participants.
On the other hand, Menger argues that the state may have played a role in
overcoming the difficulties of using metal as an exchange commodity"
 
Having Hodgson insisting on the importance of state regulation in the emergence
of money, here we can see the chronological order described by Ikeda,
emphasizing that we can first have the money emerge spontaneously, then we need
to have the government intervention to do things like quality control.
 
**In the early stage of trading in our model, why random goods other than gold can emerge?**

"Menger pointed out that although it is possible for government to compel
market participants to accept certain kinds of money, this does not mean that
market participants will be pleased to accept them"
 
Ikeda concludes that "the merits of indirect exchange were not discovered by
everyone simultaneously", so we can see unordered trading behavior during the
early stage of trading - hard to tell which good emerges, but after a period
of time and enough rounds of trading between agents, the suitable media of
exchange will emerge.



## Translating Menger into an Agent-Based Model

- Isolate the factors that can make a good become money.
- Each "Menger factor" can be turned on or off.
- To measure how much a good is approaching the status of money, we track how many times each good trades.
- A good "becomes money" as it comes close to being 
  one side of every trade.


## The Design of Our Model

- Elements and Functionalities
    
    Our model is primarily in `money.py` with supporting generic economic
    functions in `trade_utils.py`.
    In our model, we apply three main
    factors mentioned in Carl Menger's essay, *On the Origins of Money*. Each
    attribute for each good is represented in a decimal number greater than
    zero and less and equal to one. 

    - **Divisibility** identifies how separable a good is. A cow is less
    divisible than a chunk of gold because if a cow is cut into a half, it's
    not tradeable anymore as a livestock. Smaller the number, more divisible
    the good. 
    - **Durability** determines how long an item can be stored. Foods are
    generally less durable than metals, and the decayed food would be less
    valuable than the fresh ones. Goods like livestock have their own
    lifespans, and if a cow is dead, it is unlikely to be traded in the market.
    Having a durability close to 1 meaning that the good is very durable, not
    easily corrupted (like diamond). 
    - **Transportability** shows whether an item is easy to be carried. It's
    easy for us to carry some avocados but not milk because milk could be split
    out while avocados can be put in anywhere. 

    These three key attributes will determine which good is likely to emergence into money in the process of trading. 

    In our model, the nature holds a certain number of 
    different goods, each having an arbitrary number units (we set all goods having
    the same number of units). The user can choose at most the maximum number 
    agents we set, and at least two agents to trade with each other. Each "Menger
    factor" can be turned on or off so that the user can view the effect of
    each attribute on the number of trades. We track the numbers of how many times each good trades, 
    and the most traded good becomes money. In our model, *utility*, how eager a trader
    wants to own the good, is a representation of the *value* of a good. For
    each agent, when trading, only when gaining the offered good can provide a
    larger utility than losing the good he/she holds can continue the trade.
    Otherwise, this offer will be rejected by the agent or the agent may ask
    for more units. We have line graph representing the trend of number of
    trades for each good and once the trade is idle for a certain number of periods, 
    there will be an alert that the equilibrium in our
    environment may be reached, meaning that maybe there will be no trade
    happened during the following periods, reminding the user that the current
    result is likely to be the final result. 

    Of note is the fact that our model only a single rule for trading: agents
    must discover trades that are mutually beneficial. [QUOTE MENGER
    FROM PRINCIPLES ON TRADE AT UNEQUAL EVALUATIONS.] Our model captures this
    notion by having agents begin with a minimal bid for some good they desire.
    The agents then "haggle" until they possibly arrive at an exchange ratio for
    their two goods at which each of them gains utility from trading.
    As Kirzner (1992) [PRICE DISCOVERY].

    Divisibility, durability and transportability, while characteristics of 
    individual goods, are not specifically sought out by our agents.
    Instead, these factors add to the likelihood that a mutually beneficial
    trade can take place at all. For instance, in our model, higher
    transportability for some good allows trades to take place with more distant 
    agents.
        
     
    In running our model, we see that eventually, the good with
    the best combination of divisibility, durability, and transportability
    always emerges as the medium of exchange, but if middle
    stage of the trading iteration (like the result got at the 250th
    trade while the equilibrium is reached at the 600th trade), the most
    traded goods may not necessary be the same for each time - agents
    are still learning from their "mistakes". 
    "In regard to discovery,
    market prices (especially disequilibrium prices) should be seen not
    so much as known signals to be deliberately consulted in order to find
    out the right thing to do, but rather as spontaneously generated flashing
    red lights alerting hitherto unwitting market  participants to the
    possibility of pure entrepreneurial profit or the danger of loss." (Kirzner, 1992, p. 150)
    That's the reason why we are tracking the number of trades during the
    whole process instead of just recording the final result.
    We are seeing the evolution of agents' trading decisions, and
    how those decisions accumulate  to our final emerged money.


- Design Process 
    - Utility Function
        
        Utility is our important determinant for a trader to accept or reject
        an offer, and it is a representation of the value of a good - only when
        the trader wants to own the good and worth losing the good being
        requested is the offered goods valuable. We initially used a linear
        utility function.

        ```python
        def gen_util_func(qty):
            return max_util - qty
        ```

        The *max_util* can be set by the model. However, the law of
        **Diminishing Marginal Utility** states that "all else equal as
        consumption increases the marginal utility derived from each additional
        unit declines" (Gossen's First Law *citation needed*). So, we updated
        our utility function.

        ```python
        def gen_util_func(qty):
            return max_util * (DIM_UTIL_BASE ** (-qty))
        ```

        The use of exponential function makes our utility function fit closer to real-life trading.

    - Offering and Responding
        During one trade, we have one an initiator offering one good (*good A*)
        at a time and a receiver being asked to trade one good (*good B*). The
        initiator starts with offering one unit of *good A*, or the smallest divisible 
        unit of the good if the "divisibility" factor is on. 

        For the receiver, he/she will evaluate the utilities of gaining *good
        A* and losing *good B*. If the gain (the utility of getting *good A*)
        is smaller than the loss (the absolute value of the utility of losing
        *good B*), the receiver will tell the initiator that the offered amount
        of *good A* is inadequate so that that the initiator can increase the
        amount offered. The receiver can re-determine the gain and loss with
        the new amount. If the initiator offers all the available amount but
        the receiver thinks that he/she still can't gain utility, the trade
        will be rejected. If the gain is larger than the loss, the receiver
        will wait for the initiator to evaluate his/her gain and loss. If both
        parties can achieve larger gain than loss, the receiver will accept the
        offer, meaning that the trade is made. Our record will increment the
        trade_count of the both goods by one. Otherwise, if the initiator can't
        gain in this trade, he/she will reject the trade because the receiver
        is always trading with one unit of good, meaning that there's no room
        to increase the amount. 

        The initiator will loop through all the available goods he/she has to seek trades.

    - Randomization in Trading
        
        During the implementation of our divisibility attribute, we found that the first good of the natures_good dictionary is always traded the most. We solved the problem by using these two lines of code:
        ```python
        goods_list = list(goods_dict.keys())
        good = random.choice(goods_list)
        ```
        so that the first good in the dictionary will not have the priority when endowed to the agents by nature.
    - Implementation of Divisibility

        We give each good a divisibility decimal value, ranging from 0 to 1, representing its degree of divisibility. The higher the value is, the less divisible the good is. If divisibility is on, wherever the goods quantity is applied during calculation, it will be multiplied by the divisibility value, representing that instead of taking the value directly from the available amount of each agent, one unit now is instead one smallest tradable unit, so basically more divisible item can have more potential opportunities to be traded with as it has more tradable units.

        The following is an example of how divisibility is applied in our model:
        ```python
        if "divisibility" in trader["goods"][item]:
            amt = trader["goods"][good]["divisibility"]
        ```
    - Implementation of Durability

        We apply durability adjustment while calculating the utility together with the age of the good. When the "durability" factor is turned on, the utility calculation will adjust the pre-calculated utility, so that a larger utility and an older good would have a stronger negative impact on the utility. The durability value is a decimal number ranging from zero to one, and higher the number is, the more durable the good is.

        ```python
        if "durability" in trader["goods"][item]:
        return val*(trader["goods"][good]["durability"] **
                    (trader["goods"][good]["age"]/5))
        ```
        
        The age of all goods starts from 0, and during each round of the trade, whether or not the good is traded, the age will be incremented by one. If the good is considered too old, its amount available will be set to zero, meaning that the good could no longer be traded.

        ```python
        if math.exp(-(1-trader["goods"][good]["durability"]) *
           (trader["goods"][good]["age"]/10)) < 0.0001:
            trader["goods"][good][AMT_AVAIL] = 0
        ```
    - Transportability and Grid

        Transportability value is an integer representing the furthest distance an agent could go. If the transportability factor is on, we would check the distance between the two agents, and compare the value of transportability with it. If distance is larger than either of the transportability value of the good the agent holds for this round of trade, it means that the agent could not carry the good to reach the other agent and the trade will be directly set as failed. Otherwise, the trade could be continued. 

## Findings

While isolating durability, we found that after rounds of trading, when the
most traded good is likely to emerge, we saw goods with low durability trading
actively during that stage. (In our model, agents holding bananas and avocados
are very happy to trade with each other when both goods are rotten.)
The reason why it happens is that when both goods are very decayed, 
as their durability values are very close (and small), their utilities
would be similarly small (approaching zero).
Two goods with identical utilities would lead to a successful trade,
but in reality, it is hard to have someone accept a rotten banana
because what can one do with it? In response to the finding, we
set a bar to the combination result of the age and durability
[CHECK CODE: TRY TO STATE MORE PRECISELY] of
the good, and if the result is lower than the cut-off, we amount
the good to be zero, meaning that the good is not
acceptable to be traded in the market.

Another finding we got from our modeling efforts is that "transportability"
is a two-way street: it only helps to have a good that can be transported a
long ways when the good you want in exchange can *also* be transported a long
ways. There is no sense sending your gold from New York to South Carolina
for paw-paws, since the paw-paws won't make it back.

Another facet of transportability that became apparent during our experiments
is that transportability only becomes important for agents engaged in
long-distance trade. When we set our agents' trading neighborhoods to a small
size, transportability disappeared as a factor.


## Conclusion

Our efforts are certainly not an attempt to "prove" Menger's theory of the
origin of money is correct, if such a thing is even possible. Rather, the fact
that Menger's theory can be implemented in a formal system, such as an ABM,
instead is only put forward as increasing its plausibility: if the theory
"works" in the simplified world of our model, then the possibility it reflects
how money really emerged is made more likely.


## Bibliography

Graeber, David (2011)
*Debt: The First 5,000 Years*
New York: Melville House.

Hodgson, G. M. (1992).
"Carl Menger's Theory of the Evolution of Money: Some Problems."
*Review of Political Economy*, 4, 4, 396-412.

Ikeda, Yukihiro (2008).
"Carl Menger’s monetary theory: A revisionist view."
*European Journal History of Economic Thought*,
15:3 pp. 455-473.
https://www.researchgate.net/publication/24079934_Carl_Menger%27s_monetary_theory_A_revisionist_view#fullTextFileContent

Menger, Carl (1892).
"On the Origin of Money" (English translation by Caroline A.
Foley),
*Economic Journal*, Volume 2 (1892), pp. 239–55.  

Morgan, M. S. (2012).
*The world in the model: How economists work and think*.
Cambridge: Cambridge University Press.

Epstein, J. M., Axtell, R. (1996).
*Growing Artificial Societies*.
Washington, D.C.: Brookings Institution Press

Callahan, G. (2004).
*Economics for Real People: An Introduction to the Austrian School*.
Ludwig von Mises Institute.

Ford, B. (2014).
*Fake Gold Coins Throughout History*.
https://certifiedgoldexchange.com/fake-gold-coins-throughout-history/)

Kirzner, I. M. (1992).
*The meaning of the market process: Essays in the development of modern austrian
economics*.
Routledge.
