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
allow the interested scientist to wipe clean all members knowledge of money
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
circumstances” (p. 272) 

In short, setting up a model in which we can watch money emerge (or not) allows
us to explore the relations between the different factors Menger held to be
important in its emergence. At the very least, if varying these factors can
cause a good in the model to emerge or fail to emerge as money, we show that
Menger's model is logically coherent.

**Why Agent-Based Model**
(Growing Artificial Societies by J. Epstein and Robert Axtell)


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
price in reality, that in the barter system, we are not likely to have a fixed ratio of how many unit of good A can be traded into a certain unit of good B during every round of trade, that is, there's no so-called "price" while exchanging goods.
 
Menger listed three categories of factors that influence the degree of 
salebleness of goods, and they cover buyers’ own
interest (which we model as the utility the agent assigns to the next unit of the
good), the goods’ own characteristics
(what we will to focus on), and external factors (which we will ignore). 

The circumstantial influencer includes the number of people involved in the trading with their 
characteristics, including their degree of willingness and their purchasing power, the divisibility of the good itself and the environmental factors like the market and regulation maturity; the spatial limits comprises the geographical distribution of the good, the cost and easiness of transportation, availability of the corresponding means of transportation towards different goods, and the development of the trading market; the time limits incorporate factors like for how long does one need the good, the durability of the good, the preservation cost, the rate of interest of the good, and market periodicity.

Under the above listed circumstances and limits, goods are divided into two
categories: those one directly wants, or, those that can be exchanged. When
anyone has brought goods not highly saleable to market, the idea uppermost in
his mind is to exchange them. One reason is that the goods cannot be directly
used by him/her. But another intriguing reason why one chose to purchase the
item is that someone else may want it. As saleableness of goods encounter both
objective (i.e. goods’ characteristics) and subjective (i.e. personal interest)
factors, it can be greatly different for each one, and thus different people
can have different levels of willingness to purchase/sell a goods.

*These wares would be qualified by their costliness, easy transportability, and
fitness for preservation (in connection with the circumstance of their
corresponding to a steady and widely distributed demand), to ensure to the
possessor a power, not only “here” and “now” but as nearly as possible
unlimited in space and time generally, over all other market-goods at economic
prices.* (pg. 35)
 
Menger then looks at the "saleability" of different goods 
TODO!
[HERE WE SHOULD HAVE A BRIEF DISCUSSION OF CATTLE, SALT, GEMS, ETC.
SEE MY DISCUSSION IN ECONOMICS FOR REAL PEOPLE. WE CAN QUOTE ME!]
 
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


**With the proposed problems by Hodgson on Menger's theory, Why it is still worthwhile to discuss Menger's theory and do modeling on it**:

Hodgson's doubt:
*"The main problem with Menger's theory is that, given potential quality
variation, the spontaneous process of evolution of the monetary unit may break
down, possibly requiring the intervention of the state or central bank to
maintain the currency unit." -> "potential adulteration and debasement of
commodities"* 
 
Hodgson insisted the importance of *state*, which can control the variation of money caused by adulteration.
**My thinking:**

1. Adulteration happened because of the emerging money; the process of emerging
money can hardly cause faking a good because people are not sure which good
would eventually become money and whether it is worthwhile to fake it (will
fake a cow to a sheep make it more saleable?)
2. Why does adulteration matter during the process of the emergence of money?
It does not necessarily change the div/dura/trans
 
Example of early adulteration (I'm still trying to find academic paper. I only
found articles from websites talking about the history of fake gold:
https://certifiedgoldexchange.com/fake-gold-coins-throughout-history/):
 
*"The first known example of fake gold coins can be found in the Greek city of
Lydia, around the year 600 BC. Typically, these fakes were created by either
shaving off the edges of a real coin or mixing lesser amounts of gold with
other base metals. The Persian Daric was also a often copied gold coin, in
various denominations.

The Roman government even created their own fake gold coins. This was done
primarily through debasement, using less and less gold over time. Of course,
they demanded that they value of exchange be kept the same, even implementing
draconian laws to enforce their wishes. Many historians feel that the amount of
counterfeit gold coins in circulation combined with the government (and
military) constantly debasing the money played a major role in the downfall of
the Roman Empire"*

**My thinking:**
   - only when gold turn out to be money does it be faked (not during the emergence of money)
   - intervention of state can also cause faking gold

Conclusion: Hodgson's concern may not be a problem and does not allow us to dismiss Menger's theory.
 
**Why can we don't include state/regulation in our modeling:**
 
Background: One of the circumstances that affects the degrees of salebleness (quoted above) is the impact of regulation. Hodgson also mentions for several times on the importance of government intervention.
 
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

Why we reduced Menger's criteria to only three factors: divisibility, durability and transportability.

- Each "Menger factor" can be turned on or off.
- We track how many times each good trades.
- A good "becomes money" as it comes close to being 
  one side of every trade.

Divisibility: homogeneous
in terms of standard unit

## The Design of Our Model

- Elements and Functionalities
    
    Our model is primarily in `money.py` with supporting generic economic
    functions in `trade_utils.py`.
    In our model, we apply three main
    factors mentioned in Carl Menger's essay, *On the Origins of Money*. Each
    attribute for each good is represented in a decimal number greater than
    zero and less and equal to one. 

    - **Divisibility** identifies how seperatable a good is. A cow is less
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
    each attribute on the number of trades. We track the numbers of how many times each good trades, and the most traded good becomes money. In our model, *utility*, how eager a trader
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

- Design Process 
    - Utility Function
        
        Utility is our important determinate for a trader to accept or reject
        an offer, and it is a representation of the value of a good - only when
        the trader wants to own the good and worth losing the good being
        requested is the offered good valuable. We initially used a linear
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

        The use of exponential function makes our utility function fit closer to the real-life trading.

    - Offering and Responding
        (TODO: PRICE DISCOVERY BY KIRZNER)
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
        will wait for the initiator to evaluator his/her gain and loss. If both
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
        so that the first good in the dictionary will not have the priority when endowed to the agents by the nature.
    - Implementation of Divisibility

        We give each good a divisibility decimal value, ranged from 0 to 1, representing its degree of divisibility. The higher the value is, the less divisible the good is. If divisibility is on, wherever the goods quantity is applied during calculation, it will be multiplied by the divisibility value, representing that instead of taking the value directly from the avaliable amount of each agent, one unit now is instead one smallest tradable unit, so basically more divisible item can have more potential opportunities to be traded with as it has more tradeable units.

        The following is an example of how divisibility is applied in our model:
        ```python
        if "divisibility" in trader["goods"][item]:
            amt = trader["goods"][good]["divisibility"]
        ```
    - Implementation of Durability

        We apply durability adjustment while calculating the utility together with the age of the good. When the "durability" factor is turned on, the utility calculation will adjust the pre-calculated utility, so that a larger utility and an older good would have a stronger nagtive impact on the utility. The durability value is a decimal number ranges from zero to one, and higher the number is, more durable the good is. 
        ```python
        if "durability" in trader["goods"][item]:
        return val*(trader["goods"][good]["durability"] **
                    (trader["goods"][good]["age"]/5))
        ```
        
        The ages of all goods starts from 0, and during each round of the trade, whether or not the good is traded, the age will be incremented by one. If the good is considered too old, its amount avaliable will be set to zero, meaning that the good could no longer be traded.
        ```python
        if math.exp(-(1-trader["goods"][good]["durability"]) *
           (trader["goods"][good]["age"]/10)) < 0.0001:
            trader["goods"][good][AMT_AVAIL] = 0
        ```
    - Transportability and Grid

        Transportability value is an integer representing the furthest distance an agent could go. If the transportability factor is on, we would check the distance between the two agents, and compare the value of transportability with it. If distance is larger than either of the transportability value of the good the agent holds for this round of trade, it means that the agent could not carry the good to reach the other agent and the trade will be directly set as failed. Otherwise, the trade could be continued. 

## Findings

While isolating durability, We found that after rounds of trading when the most traded good is likely to emerge, we see goods with low durability trades actively during that stage (in our model, agents holding banana and avocado are very happy to trade with each other when both goods are rotted). The reason why it happens is that when both goods are very decayed, as their durability values are very close (and small), their utilities would be similarly small (approaching zero). Two goods with identical utilities would lead to a successful trade, but in reality, it is hardly to have someone to accept a rotten banana because what can one do with it? In reponse to the finding, we set a bar to the combination result of the age and durability of the good, and if the result is lower than the cut-off, we amount of the good to be zero, meaning that the good is not acceptable to be traded in the market.

One realization we gained from our modeling efforts is that "transportability"
is a two-way street: it only helps to have a good that can be transported a
long ways when the good you want in exchange can *also* be transported a long
ways. There is no sense sending your gold from New York to South Carolina
for paw-paws, since the paw-paws won't make it back.

Another facet of transportability that became apparent during our experiments
is that transportability only becomes important for agents engaged in
long-distance trade. When we set our agents' trading neighborhoods to a small
size, transportability disappeared as a factor.

[Here we will discuss experiments with different parameters and so on.]
- Isolation of Durability
When a good is too decayed, its `amt_avaliable` will be set to zero by using the followinng code:

```python
if math.exp(-(1-trader["goods"][good]["durability"]) *
           (trader["goods"][good]["age"]/10)) &lt; 0.0001:
            trader["goods"][good][AMT_AVAIL] = 0
```
Without this adjustment on `amt_avaliable`, when only applying the
functionality of durability, we see that gold is traded very often (which is
not surprising), but banana and milk are also extensively traded. The reason is
that when these two items are too decayed, their utility delta will be very
similar, and a lot of tradings will be exculsively between them, while gold,
having a very optimal utility delta, can be too good for the banana holders to
trade for.

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

