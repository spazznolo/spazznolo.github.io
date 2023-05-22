---
layout: post
title:  "Empirical Bayes Goals Saved Above Expected"
date:   2023-05-22 8:52:05 -0400
---
<h2>[Post 5] Empirical Bayes Goals Saved Above Expected</h2>
<p>
In post 4, I outlined a framework for measuring goalie talent using their career Fenwick 5v5 save percentage. It concluded with the assumptions of the initial strategy, which I'll include below.
</p>
<p>
Assumptions:
    - The prior distribution (for Fenwick 5v5 save percentage) is assumed to be beta with hyperparameters 1770 and 126.
    - Age is assumed to be irrelevant. 
    - Scoring rates are assumed to be constant.
    - All shots are assumed to be equal. 
    - Team systems are assumed to be identical.
</p>
<p>
I'm going to address the fourth point in this post. We already know that not all shots are equal. Countless Exepected Goals models have been produced to address this. Thankfully, Peter Tanner, through his website <a href="https://moneypuck.com/about.htm">MoneyPuck</a>, provides detailed data for each unblocked shot that occurs in the NHL (whether it hit the net or not) along with a prediction - the probability of the shot being a goal.
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-five-one.png" width="60%" length="150"/></div>
</p>
<p>
Code available here: <a href="https://github.com/spazznolo/goalie-consistency/blob/main/post_5.R">https://github.com/spazznolo/goalie-consistency/blob/main/post_5.R</a>
</p>