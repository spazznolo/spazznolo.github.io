---
layout: post
title:  "[Part 3] The effects of inter-shot goalie consistency (using NHL data)"
date:   2022-04-07 8:52:05 -0400
---
<h2> The effects of inter-shot goalie consistency (using real data) </h2>
<p>
In the <a href="https://spazznolo.github.io/2022/03/28/goalie-consistency-0.html">Introduction</a>, we defined normalized entropy as a measure for inter-shot goalie consistency using the following equation:
</p>
<p> 
<div style="text-align: center"> 
<img src="https://spazznolo.github.io/figs/goalie-formula-entropy.png" width="40%" length="60"/>
</div>
</p>
<p>
In order to advance this idea to include Expected Goals,we need to modify two parts: the simulation of seasons - we can no longer randomize seasons through sampling shot outcomes without replacement; and the entropy equation listed above - which needs to include the probability of shots becoming goals.
</p>
<h5>Modifying Season Simulations</h5>
To convert a sequence of Expected Goals into a sequence of outcomes (goal or save), we flip a weighted coin by way of a <a href="https://en.wikipedia.org/wiki/Binomial_distribution">binomial</a> simulation, with the weight being the probability that the shot becomes a goal <em>minus the goalie's goals saved above expected per expected goal multiplied by the original shot probability</em>. This way, the simulations will mirror a goalie's deviance from the expected performance (if a goalie allows more goals than expected, so will the simulations).
<p> 
For example, in 2020 Thatcher Demko was scored on 99 times, but was expected to be scored on 105.7 times. He saved 6.7 goals above what he was expected to, and 6.7/105.7 = 0.0631 goals per expected goal. The simulation of a shot with a 14% chance of becoming a goal can then be represented by a weighted coin flip with probabilities of (0.14-(0.14*0.0631)) = 13.1% for a goal and (1-P(goal)) = 86.9% for a save/miss.
</p>
<h5>Modifying the Entropy Equation</h5>
The entropy equation is modified in the following way: instead of the number of shots saved in a row (or, the save streak) between goals, we sum the number of Expected Goals saved in between goals (the Expected Goals saved streak).
<div style="text-align: center"> 
<img src="https://spazznolo.github.io/figs/goalie-formula-entropy-two.png" width="80%" length="125"/>
</div>
<h5>The Results</h5>
With this, we can  measure the effect of inter-shot goalie consistency on various things. And it turns out - as the plots below show - that there isn't much there. A goalie's inter-shot consistency in a given season doesn't say much about their inter-shot consistency in the next season, better goalie careers don't appear to have more or less consistency than a worse career, etc. 
<p>
</p>
<p>
<em>Note: A goalie season must include at least 800 shots (roughly 20 games) to be included in the season comparisons, and a goalie career must include at least 5 seasons, facing at least 800 shots in each, to be included in the career comparisons.</em>
</p>
<p>
</p>
<h5>Inter-shot goalie consistency does not have an effect on overall performance.</h5>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-three-one.png" width="60%" length="150"/></div>
</p>
<h5>The 10 streakiest goalie careers.</h5>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-three-two.png" width="60%" length="150"/></div>
</p>
<h5>The 10 least streaky goalie careers.</h5>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-three-three.png" width="60%" length="150"/></div>
</p>
<h5>Goalie inter-shot consistency does not have an effect on career season-over-season consistency.</h5>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-three-four.png" width="60%" length="150"/></div>
</p>