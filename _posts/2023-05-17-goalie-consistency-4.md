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
Let's again look at uncertainty, but this time, instead of the uncertainty in goalie performance we'll look at the uncertainty in goalie skill. There's a difference. In the previous three posts I looked at the variance in game-to-game outcomes, but this time I want to look at the variance in a goalie's actual expected save percentage. To do this, we'll use a Bayesian framework which has already been explored in previous papers [link].
</p>
<p>
A Bayesian framework requires a prior distribution,...
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
It is reasonable to say that, given a new goalie we know nothing about, the distribution of possible outcomes for him could fit the plot above. This will be the <em>prior</em>.
</p>
<p>
Here's what fitting a beta distribution, a common prior when the variable of interest is a percentage (as is ours with the save percentage) to the career save percentage distribution looks like.
</p>
<h5>Beta Distribution Fitted to Career Save Percentage Distribution</h5>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-four-two.png" width="60%" length="150"/></div>
</p>
