---
layout: post
title:  "Empirical Bayes Adjusted Save Percentage"
date:   2023-05-22 8:52:05 -0400
---
<h2>[Post 5] Empirical Bayes Adjusted Save Percentage</h2>
<p>
In post 4, I outlined a framework for measuring goalie talent using their career Fenwick 5v5 save percentage. It concluded with the assumptions of the initial strategy, which I'll include below.
</p>
<p>
Assumptions:
    - The prior distribution is assumed to be from the beta family.
    - Age is assumed to be irrelevant. 
    - Scoring rates are assumed to be constant.
    - All shots are assumed to be equal. 
    - Team systems are assumed to be identical.
</p>
<p>
I'm going to address the fourth point in this post.
</p>
<p>
<h5>Adjusted Save Percentage</h5>
We already know that not all shots are equal. Countless Exepected Goals models have been produced to address this. Thankfully, Peter Tanner, through his website <a href="https://moneypuck.com/about.htm">MoneyPuck</a>, provides detailed data for each unblocked shot that occurs in the NHL (whether it hit the net or not) along with a prediction - the probability of the shot being a goal.
</p>
<p>
We can adjust a goalie's save percentage by taking into account these predictions from MoneyPuck. There are many ways to do this, but I've decided to derive one which would retain the measure as a rate. Here's what I came up with:
</p>
<p>
<br>Fenwick Save Percentage (FSV) = 1 - (Goals Against / Fenwick Shots Against)
<br>Expected Fenwick Save Percentage (xFSV%) = 1 - (Expected Goals Against / Fenwick Shots Against)
<br>Mean Save Percentage (MSV) = 1 - (Total Goals Scored / Total Shots Faced)
<br><b>Adjusted Save Percentage (AdjSP) = MSV + (FSV% - xFSV%)</b>
</p>
<p>
For the sake of simplicity, let's flip the adjusted save percentage to the adjusted failure rate (1 - AdjSP) and plot the distribution of career rates for goalies having faced more than 10 expected goals. We'll include a fitted beta distribution in white. The goodness of fit, which frankly was questionable in the last post, looks better this time. It'll improve as we try different distributions in future posts.
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-five-one.png" width="60%" length="150"/></div>
</p>
<p>
Given that we are once again fitting a beta distribution, the rest of the work is the same as the previous post.
</p>
<p>
Let's revisit the Jake Oettinger and Jeremy Swayman comparison.
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-five-two.png" width="60%" length="150"/></div>
</p>
<p>
The posteriors change as follows:
    - There's a 77.03% (previously 57.18%) chance that Swayman is better than Oettinger.
    - There's a 86.88% (previously 92.57%) chance that Oettinger is better than average.
    - There's a 96.50% (previously 91.81%) chance that Swayman is better than average.
    - Oettinger's distribution is tighter than Swayman's because he's faced more shots.
</p>
<p>
These changes are due to the fact that Swayman faces more difficult shots on a whole - his expected Fenwick save percentage is 94.07 while Oettinger's is 94.39.
<p>
Code available here: <a href="https://github.com/spazznolo/goalie-consistency/blob/main/post_5.R">https://github.com/spazznolo/goalie-consistency/blob/main/post_5.R</a>
</p>