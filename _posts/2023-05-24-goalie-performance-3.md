---
layout: post
title:  "Goalie Performance: Exploring the Distribution"
date:   2023-05-24 8:52:05 -0400
---
```ruby
require 'redcarpet'
markdown = Redcarpet.new("Hello World!")
puts markdown.to_html
```
<h2>[Post 3: Still Working on this] Goalie Performance: Exploring the Distribution</h2>
<p>
In the <a href="https://spazznolo.github.io/2023/05/17/goalie-performance-1.html">first post</a>, I outlined a framework for measuring goalie talent using their career Fenwick 5v5 save percentage. In the second post, the methodology was adapted to consider shot quality. There are two obvious problems with this methodology, though. 
</p>
<p>
    1. Goalies facing less than 10 xG had to be thrown out.
    2. Goalies' career AdjSV% were treated equally.
</p>
<p>
Even though we're only talking about a 10xG cut-off, this eliminates more goalies than I would have liked. To illustrate this, here's the cumulative distribution function. It turns out 90 of 314 goalies (28.7%) faced below 10xG in their careers!
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-six-one.png" width="60%" length="150"/></div>
</p>
<p>
One possible solution to this was proposed by <a href="http://varianceexplained.org/r/empirical_bayes_baseball/">David Robinson</a> in his Baysian series on baseball. Instead of fitting a beta distribution to batting averages, he fit a negative binomial distribution using 1) at bats and 2) hits. This can easily be applied to goalies using 1) shots faced and 2) adjusted saves. It has <em>its</em> problems too, though (which, of course, David addresses in a string of fantastic blog posts, eventually putting out a <a href = "https://drob.gumroad.com/l/empirical-bayes">book</a>). The main problem is this: goalies are weighted by the number of career shots they faced. Why was, say, Henrik Lundvist given more opportunities to play than Zachary Fucal? Was it random? No, he performed better. Intuitively, goalies who perform well likely get more chances to play than if they play poorly, in which case they'll get less chances until, finally, they are no longer given the chance to play at all. Let's see if the data matches intuition. We group goalies by career seasons played and then take the average AdjSV% for each group; seasons played on the x-axis against mean AdjSV% on the y-axis. 
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-six-two.png" width="60%" length="150"/></div>
</p>
<p>
There is definitely bias here. This potential solution has caused a compromise. Do we weigh the observations by shots faced, which is biased towards better performing goalies, or do we treat all goalie careers equally, losing nearly 30% of our population (albeit less than 1% of shots faced) at the same time? Or... is there an alternative?
</p>
<p>
David suggests using a beta-binomial regression to fit batting averages to at-bats. Essentially, each at-bat total has its own prior. Though this is a good idea for his use case, it isn't great for mine. The problem is that I am heavily biased towards building something which can help in making decisions - I want to build towards a model which is useful for goalies who are playing right now, and we don't know how many shots they will face in the future! I need something different.
</p>
<h5>Combining Priors</h5>
Fortunately, we may be able to address this by expanding our Bayesian framework to include two priors, glued together by a likelihood. Let's revisit the goalie career AdjSV% density plots, except this time split goalies into two groups - those facing over 1,500 shots, and those facing less.
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-six-three.png" width="60%" length="150"/></div>
</p>
<p>
Some thoughts:
    - From these group distributions, we can build two separate priors.
    - These can be merged by including a likelihood of a goalie belonging to each group.
    - The likelihood is the probability that a goalie belongs to each group.
    - The likelihood will sum to 1, and begins at the observed occurence (in %) for each group.
    - For example, 35% of the goalies in our population have faced over 1500 shots, so that is the initial weight.
    - This likelihood will shift depending on his performance as he faces more shots.
</p>
<p>
Here's a simple idea for a likelihood: run a logistic regression using cumulative shots faced and AdjSV% onto the outcome of whether a goalie ended up facing over 1500 shots. This model would be easy to train and interpret.
</p>
<p>
And, it turns out, such a model is not only simple but is well-calibrated:
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-six-four.png" width="60%" length="150"/></div>
</p>
<p>
The new equation to derive the posterior save percentage then becomes:
    P(1500+)*(alphaO + AdjSV)/(alphaO + betaO + S) + P(-1500)*(alphaU + AdjSV)/(alphaU + betaU + S)

    where:
    - P(1500+) = Predicted probability that goalie faces 1500+ shots in career.
    - alphaO = alpha from fitted beta distribution on goalies facing 1500+ shots.
    - betaO = beta from fitted beta distribution on goalies facing 1500+ shots.
    - P(-1500) = Predicted probability that goalie faces -1500 shots in career.
    - alphaU = alpha from fitted beta distribution on goalies facing -1500 shots.
    - betaU = beta from fitted beta distribution on goalies facing -1500 shots.
</p>
<p>
In the next post, I'll explore age as a confounder in the assessment of goalie performance.
</p>
<p>
Code available here: <a href="https://github.com/spazznolo/goalie-consistency/blob/main/posts/post-6.R">https://github.com/spazznolo/goalie-consistency/blob/main/posts/post-6.R</a>
</p>