---
layout: post
title:  "Goalie Performance: Exploring the Distribution"
date:   2023-06-24 8:52:05 -0400
---
<head>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-DGRHZS5DNM"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-DGRHZS5DNM');
</script>
</head>
<h2>[Post 4] Goalie Performance: Exploring the Distribution</h2>
<p>
In the first post, I outlined a framework for measuring goalie performance using their career Fenwick 5v5 save percentage. In the second post, the methodology was refined to consider shot quality. The outstanding assumptions of the refined strategy are included below.
</p>
<p>
Assumptions:
    - <b>The prior distribution is assumed to be beta with hyperparameters 852 and 55.6.</b>
    - <b>Goalies facing less than 200 shots are ignored.</b>
    - <b>Goalie careers are equal.</b>
    - Age is assumed to be irrelevant.
    - Scoring rates are assumed to be constant.
    - Team systems are assumed to be identical.
</p>
<p>
In this post, I'm going to address the first, second and third outstanding assumptions and then propose one sweeping adjustment to take care of them.
</p>
<p>
<h5>Goalies in the analysis</h5>
Whenever we decide on a range of years for an analysis (in this case, 2007-2022), we are cutting of goalies mid-career. Some, like Carter Hart are beginning their careers, while others, like Lundqvist, ended them during this period. Since we are not yet adjusting for age, we can't include these goalies in the analysis. Therefore, only goalies who started their careers post-2007 and ended their careers pre-2022 can be included. This is a 15 year range.
</p>
<p>
The analysis population changes as follows:
    - Goalie population drops from 315 to 140.
    - Harmonic mean of shots against rises from 12,690 to 14,568 (mean drops, 4,198 to 3,225).
    - Harmonic mean of AdjSV% stays at .939 (mean drops, .932 to .927).
    - Mean of career shots faced drops from 4,198 to 3,225.
    - Mean of AdjSV% drops from .932 to .927.
</p>
<p>
<h5>Goalie importance</h5>
The 200 shot cut-off surprisingly filters out 90 out of 314 goalies (or, 28.7%). To illustrate this, here's the cumulative distribution function of career shots faced for goalies:
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-six-one.png" width="60%" length="150"/></div>
</p>
<p>
This is a problem. One possible solution to this was proposed by <a href="http://varianceexplained.org/r/empirical_bayes_baseball/">David Robinson</a> in his Baysian series on baseball. Instead of fitting a beta distribution to batting averages, he fit a negative binomial distribution using 1) at bats and 2) hits. This can easily be applied to goalies using 1) shots faced and 2) adjusted saves. It has <em>its</em> problems, though (which, of course, David addresses in a string of fantastic blog posts, eventually putting out a <a href = "https://drob.gumroad.com/l/empirical-bayes">book</a>). The main problem is that it introduces bias - goalies who perform well are likely to get more opportunities to play compared to those who perform poorly. As proof, here's a plot showing the average AdjSV% by career seasons played:
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-six-two.png" width="60%" length="150"/></div>
</p>
<p>
There is definitely bias. We're faced with a compromise: Do we weigh the observations by shots faced, which is biased towards better performing goalies, or do we treat all goalie careers equally, losing nearly 30% of our population (albeit less than 1% of shots faced) at the same time? Or... is there an alternative?
</p>
<p>
David suggests using a beta-binomial regression to fit batting averages to at-bats. Essentially, each at-bat total has its own prior. Though this is a good idea for his use case, it isn't great for mine. The problem is that I want to build something which can help in making decisions about goalies who are still playing, and we don't know how many shots they will face in the future! I need something different.
</p>
<h5>Combining Priors</h5>
To address these issues, the Bayesian framework can be expanded to include two priors, glued together by a probability. The goalie career AdjSV% density plots are revisited, this time splitting goalies into two groups: those facing over 1,500 shots and those facing less. From these group distributions, two separate priors can be built, and they can be merged by including a probability of a goalie belonging to each group, which can change as they face more shots.
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-six-three.png" width="60%" length="150"/></div>
</p>
<p>
Here's a simple idea for the probability described above: run a logistic regression using cumulative shots faced and AdjSV% onto the outcome of whether a goalie ended up facing over 1500 shots. This model would be easy to train and interpret.
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
Code available here: <a href="https://github.com/spazznolo/goalie-performance/blob/main/posts/post-4.R">https://github.com/spazznolo/goalie-performance/blob/main/posts/post-4.R</a>
</p>