---
layout: post
title:  "Empirical Bayes Save Percentage"
date:   2023-05-17 8:52:05 -0400
---
<h2>[Post 4] Empirical Bayes Save Percentage</h2>
<p>
Recall from from the introductory paragraph of this series:
"Goaltenders make up the least predictable position in hockey. Their behavior confounds analysts and casual fans alike. It isn’t uncommon for a good goalie to have a below replacement level year, or for an unknown goalie to come in and dominate the league for a stretch of time. This may partly explain the relative dearth of analysis on goalies - they're voodoo, it's often said."
</p>
<p>
Let's again look at uncertainty, but this time, instead of the uncertainty in goalie performance we'll look at the uncertainty in goalie skill. There's a difference. In the previous three posts I looked at the variance in game-to-game outcomes, but this time I want to look at the variance in a goalie's actual expected save percentage. To do this, we'll use empirical Bayes. This has been explored in <a href="https://hockey-graphs.com/2018/06/21/comparing-scoring-talent-with-empirical-bayes/">previous</a> <a href="http://varianceexplained.org/r/empirical_bayes_baseball/">papers</a>. This post is a launchpad for more detailed, rigorous research.
</p>
<p>
<h5>Step One</h5>
The first step of empirircal Bayes is to use the observed data to fit a prior distribution. Think of it like this - a new goalie you've never heard of appears. What probability would you give that they have a career .930 Fenwick save percentage*? .940? .950?
</p>
<p>
*Fenwick save percentage is the total percentage of unblocked shots saved. This means that shots which miss the net are still counted. It has been proven that goalie skill is correlated with making players miss the net.
<p>
Here's a histogram of career 5v5 Fenwick save percentages for goalies having faced 750+ shots.
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-four-one.png" width="60%" length="150"/></div>
</p>
<p>
Given a new goalie we know nothing about, it is reasonable to represent their possible career Fenwick save percentage as the plot above. Now, the histogram above is a rough distribution - there are bumps throughout which seem random. In order to smooth this, we fit a distribution to it. 
</p>
<p>
The beta distribution is a common prior when the variable of interest is a percentage (as is ours with the save percentage). Here's what fitting a beta distribution to the career Fenwick save percentage distribution looks like.
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-four-two.png" width="60%" length="150"/></div>
</p>
<p>
The fit isn't perfect (we'll explore alternatives in a future post), but it isn't terrible. The beta distribution has two hyper parameters (alpha and beta), which you can interpret as successes (saves) and failures (goals). The fitted beta distribution has as hyperparameters 1770 and 126, which means we attribute 1770 saves and 126 goals to a goalie prior to knowing anything about them. This represents a .934 Fenwick save percentage, which is the same as the median career save percentage for goalies having faces 750+ shots.
</p>
<p>
<h5>Step Two</h5>
The second step is to update the prior with each goalie's career results. Here, if a goalie has only faced a few shots, their expected save percentage will shrink towards the mean of the prior distribution and the uncertainty (represented by variance in their distribution) will remain high. Essentially the distribution will still resemble the prior's. As a goalie faces more and more shots, the uncertainty of their expected save percentage decreases.
</p>
<p>
It is quite easy to update the prior with observed goalie results. All you need to do is add the observed success and failures to the beta's hyperparameters.
</p>
<p>
As an example, let's plot the posterior distributions for two 24 year old goalies - Jake Oettinger and Jeremy Swayman.
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-four-three.png" width="60%" length="150"/></div>
</p>
<p>
These posterior distributions allow for some interesting insights, like: 
    - There's a 53.21% chance that Oettinger is better than Swayman
    - There's a 79.77% chance that Oettinger is better than average
    - There's a 73.79% chance that Swayman is better than average
    - Oettinger's distribution is tighter than Swayman's because he's faced more shots.
</p>
<p>
Here are all the assumptions with this method, though:
    - The prior distribution is assumed to be beta with hyperparameters 1770 and 126.
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