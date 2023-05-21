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
The first step of empirircal Bayes is to estimate a prior distribution. Think of it like this - a new goalie you've never heard of appears. What probability would you give that they have a career .910 save percentage? .920? .930? 
</p>
<p>
The second step is to update the fit prior with each goalie's career results. Here, if a goalie has only faced a few shots, there will be higher uncertainty (represented by variance in their distribution) of their save percentage. As a goalie saves more shots, the uncertainty will decrease.
</p>
<p>
Let's start with an example. Using only Fenwick Save Percentage, who's the better goalie, Andrei Vasilevski or Jeremy Swayman? Well, looking at their career Fenwick Save Percentage, Swayman is ahead - he's at .942 while Vasilevski's at .941. However, Swayman has faced only 2,159 shots, while Vasilevsky faced 19,155. How can we take into account the fact that Vasilevsky has been elite with a greater body of work?
</p>
<p>
To start simply, here's a histogram of career Fenwick save percentages for goalies having faced 750+ shots.
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
This fit isn't perfect, and we'll explore alternatives in a future post, but it isn't terrible. The beta distribution has two hyper parameters (alpha and beta), which you can interpret as the successes (saves) and failures (goals) we attribute to a goalie before we know anything about them.  The fitted beta distribution has as hyperparameters 1770 and 126, which represents 1770 saves and 126 goals, or a save percentage of .9335 to begin.
</p>
<p>
From this, it is quite easy to update the prior with observed goalie results. All you need to do is add the observed success and failures to the beta's hyperparameters. Here are Vasilevsky and Swayman's distributions.
</p>
<h5>Posterior Distributions of Vasilevsky and Swayman</h5>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-four-three.png" width="60%" length="150"/></div>
</p>
<p>
Some takeaways from this plot: 
    - There's a 79.49% chance that Vasilevsky is better than Swayman
    - There's a 99.99% chance that Vasilevsky is better than average
    - There's a 86.73% chance that Swayman is better than average
</p>
<p>
Here are all the assumptions with this method, though:
    - The prior distribution is assumed to be beta with hyperparameters 1770 and 126.
    - Age is assumed to be irrelevant. 
    - Scoring rates are assumed to be constant.
    - All shots are assumed to be equal. 
    - Team systems are the same.
</p>
<p>
These will be challenged and addressed in the following posts.
</p>
<highlight>
goalie_prior = fitdist(career_save_pcts$mean_sv_pct, "beta", method = 'mle')
prior_points = dbeta(sv_pct_fits, shape1 = goalie_prior$estimate[1], shape2 = goalie_prior$estimate[2])
prior_points = prior_points/sum(prior_points)
</highlight>
