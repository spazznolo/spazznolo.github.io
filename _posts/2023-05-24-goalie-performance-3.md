---
layout: post
title:  "Goalie Performance: Exploring the Distribution"
date:   2023-05-24 8:52:05 -0400
---
<h2>[Post 3] Goalie Performance: Exploring the Distribution</h2>
<p>
In the first post, I outlined a framework for measuring goalie talent using their career Fenwick 5v5 save percentage. In the second post, a prior from the beta family was fit to the goalie career AdjSV% histogram, which yielded the hyper-parameters we built the posterior from (alpha of 56.45766, beta of 881.8847). There are two obvious problems with this methodology, though. 
</p>
<p>
    1. Goalies facing less than 10 xG had to be thrown out.
    2. Goalies were treated equally, meaning Zachary Fucale's career SV% was considered to be as informative as Henrik Lundqvist's.
</p>
<p>
Even though we're only talking about a 10xG cut-off, this eliminates more goalies than I would have thought. To illustrate this, here's the cdf xxxx.
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-six-one.png" width="60%" length="150"/></div>
</p>
<p>
One possible solution to this was proposed by David Robinson <a href="http://varianceexplained.org/r/empirical_bayes_baseball/">here</a>. Instead of fitting a beta distribution to batting averages, he fit a negative binomial distribution using 1) at bats and 2) hits. This can easily be applied to goalies uing 1) shots faced and 2) adjusted saves. It has <em>its</em> problems too, though (which, of course, David addresses in a string of fantastic blog posts which became a <a href = "https://drob.gumroad.com/l/empirical-bayes">book</a>). Think back to Zachary Fucal and Henrik Lundqvist. Why was Lundvist given more opportunities to play? Was it random? Intuitively, my thinking is that if a goalie performs well, they'll keep getting more chances to play; if they play poorly, they'll get less chances until, finally, they are no longer given the chance to play at all. This can be confirmed with a simple plot. We group goalies by career seasons played and then take the average AdjSV% for each group; seasons played on the x-axis against mean AdjSV% on the y-axis. 
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-six-three.png" width="60%" length="150"/></div>
</p>
<p>
What does this mean for the prior distribution? We're left with a compromise. Do we weigh the observations by shots faced, which is biased towards better performing goalies, or do we treat all goalie careers equally, losing nearly 30% of our population (albeit less than 1% of shots faced) at the same time? Or... is there an alternative?
</p>
<h5>Combining Priors</h5>
Recall that nearly 50% of goalies face less than 200 shots. This is a huge spoke in our wheels, methodologically speaking. It is responsible for the tension described above. Fortunately, we may be able to address this by expanding our Bayesian framework to include two priors, glued together by a likelihood.
</p>
<p>
We revisit the goalie career AdjSV% density plots, except this time we split goalies into two equally sized groups - those facing over 200 shots, and those facing less. Here's what they look like:
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-six-four.png" width="60%" length="150"/></div>
</p>
<p>
Some thoughts:
    - From these group distributions, we can build two separate priors.
    - These can be merged by including a likelihood of a goalie belonging to each group.
    - The likelihood is the probability that a goalie belongs to each group.
    - The likelihood will sum to 1, and begins at 50% for each group.
    - This is because 50% of the goalies in our population have faced over 200 shots.
    - This likelihood will shift depending on his performance as he faces more shots.
</p>
<p>
Here's a simple idea for a likelihood: run a logistic regression using cumulative shots faced and AdjSV% onto the outcome wheter a goalie ended up facing over 200 shots. It turns out such a model is not only simple but is well-calibrated.
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-six-five.png" width="60%" length="150"/></div>
</p>
<p>
<h5>Contextualizing Experience</h5>
Let's start simple: How long is the average goalie career? How many goalies face over 30 shots? How many make it past 200?... All of these questions can be answered by plotting the cumulative distribution function (cdf) of career shots faced for goalies.
</p>
<p>
Some thoughts:
    - 25% of goalies faced 33 shots or less (!).
    - 50% of goalies faced 202 shots or less (that's about 7 games).
    - 75% of goalies faced 2,606 shots or less.
</p>
<p>
We can gain another perspective on goalie experience by repeating the plot above for goalie career seasons played.
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-six-two.png" width="60%" length="150"/></div>
</p>
<p>
Some thoughts:
    - 42% of goalies played only one season.
    - 74% of goalies played five seasons or less.
    - 90% of goalies played twelve seasons or less.
</p>
<p>
It should now be obvious that most goalies don't really have a typical NHL career as we imagine them. Let's confirm the assumption that goalies with more experience perform better than those with less.
</p>
<p>
In the next post, we explore how age is a confounder in assessing goalie performance.
</p>
<p>
Code available here: <a href="https://github.com/spazznolo/goalie-consistency/blob/main/posts/post-6.R">https://github.com/spazznolo/goalie-consistency/blob/main/posts/post-6.R</a>
</p>