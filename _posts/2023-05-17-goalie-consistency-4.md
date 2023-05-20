---
layout: post
title:  "Bayesian Save Percentage"
date:   2023-05-17 8:52:05 -0400
---
<h2>[Post 4] Bayesian Save Percentage</h2>
<p>
Recall from from the introductory paragraph of this series:
"Goaltenders make up the least predictable position in hockey. Their behavior confounds analysts and casual fans alike. It isn’t uncommon for a good goalie to have a below replacement level year, or for an unknown goalie to come in and dominate the league for a stretch of time. This may partly explain the relative dearth of analysis on goalies - they're voodoo, it's often said."
</p>
<p>
Let's again look at uncertainty, but this time, instead of the uncertainty in goalie performance we'll look at the uncertainty in goalie skill. There's a difference. In the previous three posts I looked at the variance in game-to-game outcomes, but this time I want to look at the variance in a goalie's actual expected save percentage. To do this, we'll use empirical Bayes. This has been explored in previous papers [link]. This will be a launchpad for more detailed, rigorous research.
</p>
<p>
Let's start with an example. Using only Fenwick Save Percentage, who's the better goalie, Andrei Vasilevski or Jeremy Swayman? Well, looking at their career Fenwick Save Percentage, Swayman is ahead - he's at .942 while Vasilevski's at .941. However, Swayman has faced only 2,159 shots, while Vasilevsky faced 19,155. How can we take into account the fact that Vasilevsky has been elite with a greater body of work?
</p>
<p>
To start simply, here's a histogram of career goalie save percentages, unadjusted.
</p>
<p>
</p>
<h5>Distribution of Career Save Percentage for Goalies Facing 750+ shots</h5>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-four-one.png" width="60%" length="150"/></div>
</p>
<p>
Given a new goalie we know nothing about, it is reasonable to represent their possible career save percentage as the plot above. Now, the histogram above is a rough distribution - there are bumps throughout which seem random. In order to smooth this, we need to fit a distribution on it. 
</p>
<p>
The beta distribution is a common prior when the variable of interest is a percentage (as is ours with the save percentage). Here's what fitting a beta distribution to the career save percentage distribution looks like. This will be our <em>prior</em>.
</p>
<h5>Beta Distribution Fitted to Career Save Percentage Distribution</h5>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-four-two.png" width="60%" length="150"/></div>
</p>
<p>
The beta distribution has some interesting, clean properties. First of all, it 