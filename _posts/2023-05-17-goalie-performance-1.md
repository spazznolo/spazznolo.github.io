---
layout: post
title:  "Goalie Performance: Empirical Bayes Save Percentage"
date:   2023-05-17 8:52:05 -0400
---
<h2>[Post 1] Goalie Performance: Empirical Bayes Save Percentage</h2>
<p>
Recall from the <a href="https://spazznolo.github.io/2022/03/28/goalie-consistency-1.html">introductory paragraph</a> of the series on goalie consistency: "Goaltenders make up the least predictable position in hockey. Their behavior confounds analysts and casual fans alike. It isn’t uncommon for a good goalie to have a below replacement level year, or for an unknown goalie to come in and dominate the league for a stretch of time. This may partly explain the relative dearth of analysis on goalies - they're voodoo, it's often said."
</p>
<p>
This new series is about goalie performance. In particular, I'm going to try to enhance the estimation of goalie performance using an empirical Bayes framework. Similar applications were outlined in <a href="https://hockey-graphs.com/2018/06/21/comparing-scoring-talent-with-empirical-bayes/">previous</a> <a href="http://varianceexplained.org/r/empirical_bayes_baseball/">papers</a>. There are a few advantages to this strategy, one is that we get a measure of <em>uncertainty</em>, which is vital in describing goalie performance. In this post I'm going to sketch the idea using raw save percentage, then I'll refine the methodology as I go on. 
</p>
<p>
There are essentially two steps; the first is to use the observed data to fit a prior distribution, the second is to update this prior using observed data.
</p>
<p>
<h5>Step One</h5>
The first step of empirical Bayes is to use the observed data to fit a prior distribution. Think of it like this - a new and unknown goalie emerges. What probability can we assign to their career Fenwick* save percentage being .930, .940, or .950?
</p>
<p>
*Fenwick save percentage is the total percentage of unblocked shots saved. This means that shots which miss the net are still counted. It has been proven that goalie skill is correlated with making players miss the net.
<p>
Here's a histogram of career 5v5 Fenwick save percentages for goalies having faced 200+ shots.
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-four-one.png" width="60%" length="150"/></div>
</p>
<p>
Given a new goalie we know nothing about, it is reasonable to represent their possible career Fenwick save percentage using the histogram provided above. Now, the histogram is a rough distribution - there are bumps throughout which seem random. In order to obtain a more structured representation, we fit a distribution to it. 
</p>
<p>
The beta distribution is a common prior when the variable of interest is a percentage (as is ours with the save percentage). Here's what fitting a beta distribution to the career Fenwick save percentage distribution looks like.
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-four-two.png" width="60%" length="150"/></div>
</p>
<p>
The fit isn't perfect (we'll explore alternatives (gamma, weibull, etc.) in a future post to find the best possible fit), but it isn't terrible. The beta distribution has two hyper parameters (alpha and beta), which you can interpret as successes (saves) and failures (goals). The fitted beta distribution has as hyperparameters 1770 and 126, which means we attribute 1770 saves and 126 goals to a goalie prior to knowing anything about them. This represents a .934 Fenwick save percentage, which is the same as the median career save percentage for goalies having faces 750+ shots.
</p>
<p>
<h5>Step Two</h5>
The second step is to update the prior with each goalie's career results. Here, if a goalie has only faced a few shots, their expected save percentage will shrink towards the mean of the prior distribution and the uncertainty (represented by variance in their distribution) will remain high. Essentially the distribution will still resemble the prior. As a goalie faces more shots, the uncertainty of their expected save percentage decreases.
</p>
<p>
It is quite easy to update the prior with observed goalie results. All you need to do is add the observed success and failures (again, these are just saves and shots) to the beta's hyperparameters.
</p>
<p>
As an example, let's plot the posterior distributions for two 24 year old goalies - Jake Oettinger and Jeremy Swayman.
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-four-three.png" width="60%" length="150"/></div>
</p>
<p>
These posterior distributions allow for some interesting insights, like: 
    - There's a 57.18% chance that Swayman's save percentage is higher than Oettinger's.
    - There's a 92.57% chance that Oettinger's save percentage is higher than average.
    - There's a 91.81% chance that Swayman's save percentage is higher than average.
    - Oettinger's distribution is tighter than Swayman's because he's faced more shots.
</p>
<p>
Here are all the assumptions with this method, though:
    - The prior distribution is assumed to be beta with hyperparameters 1770 and 126.
    - Goalies facing less than 200 shots are assumed to be irrelevant.
    - Age is assumed to be irrelevant.
    - Scoring rates are assumed to be constant.
    - All shots are assumed to be equal.
    - Team systems are assumed to be identical.
</p>
<p>
These will be challenged and addressed in the following posts.
</p>
<p>
Code available here: <a href="https://github.com/spazznolo/goalie-consistency/blob/main/post_4.R">https://github.com/spazznolo/goalie-consistency/blob/main/post_4.R</a>
</p>
