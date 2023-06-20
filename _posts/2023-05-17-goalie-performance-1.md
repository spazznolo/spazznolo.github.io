---
layout: post
title:  "Goalie Performance: Empirical Bayes Save Percentage"
date:   2023-05-17 8:52:05 -0400
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
<h2>[Post 1] Goalie Performance: Empirical Bayes Save Percentage</h2>
<p>
Recall from the <a href="https://spazznolo.github.io/2022/03/28/goalie-consistency-1.html">introductory paragraph</a> of the series on goalie consistency: "Goaltenders make up the least predictable position in hockey. Their behavior confounds analysts and casual fans alike. It isn’t uncommon for a good goalie to have a below replacement level year, or for an unknown goalie to come in and dominate the league for a stretch of time. This may partly explain the relative dearth of analysis on goalies - they're voodoo, it's often said."
</p>
<p>
This new series focuses on goalie performance. It aims to enhance the estimation of goalie performance using an empirical Bayes framework. Similar applications were outlined in <a href="https://hockey-graphs.com/2018/06/21/comparing-scoring-talent-with-empirical-bayes/">previous</a> <a href="http://varianceexplained.org/r/empirical_bayes_baseball/">papers</a>. The strategy has several advantages over frequentist methods, chiefly the ability to measure uncertainty, which is crucial in describing goalie performance. In this post, the idea is sketched using raw save percentage as the performance metric, with further refinement of the methodology in subsequent posts.
</p>
<p>
The empirical Bayes approach involves two steps. The first step is to use observed data to fit a prior distribution, and the second step is to update this prior using observed data.
</p>
<p>
<h5>Step One</h5>
Imagine a scenario where a new and unknown goalie emerges. What probability can we assign to their career Fenwick* save percentage being .930, .940, or .950?
</p>
<p>
*Fenwick save percentage refers to the total percentage of unblocked shots saved, including shots that miss the net. It has been established that goalie skill correlates with the ability to make players miss the net.
<p>
To represent the possible career Fenwick save percentage for a new goalie, we can utilize the provided histogram of career 5v5 Fenwick save percentages for goalies who have faced 200+ shots (including those facing less adds noise - don't worry, it'll be addressed in a future post).
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-performance-1-1.png" width="60%" length="150"/></div>
</p>
<p>
While the histogram provides a rough distribution, it contains random bumps throughout. To obtain a more structured representation, we fit a distribution to it.
</p>
<p>
The beta distribution is a commonly used prior when the variable of interest is a percentage, as in the case of the raw save percentage. Fitting a beta distribution to the career Fenwick save percentage distribution yields the following result.
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-performance-1-2.png" width="60%" length="150"/></div>
</p>
<p>
The fit is... not really good, and alternative distributions such as gamma or Weibull will be explored in future posts to find the best fit, but it serves its purpose as an introduction to the framework. The beta distribution has two hyperparameters, alpha and beta, which can be interpreted as successes (saves) and failures (goals). The fitted beta distribution in this case has hyperparameters 852 and 55.6, indicating that we attribute 852 saves and 55.6 goals to a goalie before knowing anything about them. This corresponds to a .9388 Fenwick save percentage, or, a little below the median save percentage for goalies facing 200+ shots (.9406).
</p>
<p>
<h5>Step Two</h5>
The second step involves updating the prior distribution with each goalie's career results. When a goalie has faced only a few shots, their estimated save percentage shrinks towards the mean of the prior distribution, while the uncertainty (represented by variance in the distribution) remains high. As a goalie faces more shots, the uncertainty of their estimated save percentage decreases.
</p>
<p>
Updating the prior with observed goalie results is relatively straightforward. It requires adding the observed successes and failures (saves and shots) to the hyperparameters of the beta distribution.
</p>
<p>
As an example, let's plot the posterior distributions for two 24-year-old goalies: Jake Oettinger and Jeremy Swayman.</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-four-three.png" width="60%" length="150"/></div>
</p>
<p>
These posterior distributions offer interesting insights, like: 
    - There's a 60.28% chance that Swayman's save percentage is higher than Oettinger's.
    - There's a 94.12% chance that Oettinger's save percentage is higher than average.
    - There's a 93.81% chance that Swayman's save percentage is higher than average.
    - Oettinger's distribution is tighter than Swayman's because he's faced more shots.
</p>
<p>
It's important to list all the assumptions with this method:
    - All shots are assumed to be equal.
    - The prior distribution is assumed to be beta with hyperparameters 852 and 55.6.
    - Goalies facing less than 200 shots are ignored.
    - Age is assumed to be irrelevant.
    - Scoring rates are assumed to be constant.
    - Team systems are assumed to be identical.
</p>
<p>
These will be challenged and addressed in the following posts.
</p>
<p>
Code available here: <a href="https://github.com/spazznolo/goalie-performance/blob/main/post_1.R">https://github.com/spazznolo/goalie-consistency/blob/main/post_4.R</a>
</p>
