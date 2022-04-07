---
layout: post
title:  "[Part 3] The effects of inter-shot goalie consistency (using NHL data)"
date:   2022-04-04 8:52:05 -0400
---
<h2> The effects of inter-shot goalie consistency (using real data) </h2>
<p>
In the <a href="https://spazznolo.github.io/2022/03/28/goalie-consistency-0.html">Introduction</a>, we defined normalized entropy as a measure for inter-shot goalie consistency using the following equation:
</p>
<p> 
<div style="text-align: center"> 
<img src="https://spazznolo.github.io/figs/goalie-formula-entropy.png" width="50%" length="75"/>
</div>
</p>
<p> 
Here, we advance this idea to include Expected Goals. To do so, we need to modify two parts: the simulation of seasons - we can no longer randomize seasons through sampling without replacement; and the entropy equation listed above - which needs to include the probability of shots beoming goals.
</p>
<h5>Season Simulations</h5>
<p> 
Shots are now represented by the likelihood that they become a goal. To create a sequence of outcomes (goal or save), we flip a weighted coin by way of a binomial simulation, with the weight being the probability that the shot becomes a goal <em>minus the goalie's goals saved above expected per expected goal</em>. This way, the simulations will mirror a goalie's deviance from the average performance (if a goalie leaves more goals in than he should have, so will the simulations).
</p>
<p> 
For example, xx in 2020 saved x more goals than expected per expected goal. The simulation of a shot with a probability of 14% of beoming a goal then can be represented by:
</p>
<h5>Entropy Equation</h5>
<p> 
<div style="text-align: center"> 
<img src="https://spazznolo.github.io/figs/goalie-formula-entropy-two.png" width="50%" length="75"/>
</div>
</p>
<p> 
With this, we can easily measure various outcomes goalie consistency might have an effect on. And it turns out - as the plots below show - that there isn't much there. A goalie's inter-shot consistency in a given season doesn't say much their inter-shot consistency in the next season, better goalie careers don't appear to have more or less consistency than a worse career, etc. 
</p>
<p>
Note: A goalie season must include at least 800 shots (roughly 20 games) to be included in the season comparisons, and goalie-career must include at least 5 seasons, facing at least 800 shots in each, to be included in the career comparisons.
</p>
<h5>Inter-shot goalie consistency does not have an effect on overall performance.</h5>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-three-one.png" width="60%" length="150"/></div>
</p>
<h5>The 10 streakiest goalie careers.</h5>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-three-twoo.png" width="60%" length="150"/></div>
</p>
<h5>The 10 least streaky goalie careers.</h5>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-three-threee.png" width="60%" length="150"/></div>
</p>
<h5>Goalie inter-shot consistency does not have an effect on career season-over-season consistency.</h5>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-three-four.png" width="60%" length="150"/></div>
</p>