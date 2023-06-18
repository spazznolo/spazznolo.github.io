---
layout: post
title:  "Goalie Performance: Empirical Bayes Adjusted Save Percentage"
date:   2023-05-22 8:52:05 -0400
---
<h2>[Post 2] Goalie Performance: Empirical Bayes Adjusted Save Percentage</h2>
<p>
In the first post, I outlined a framework for measuring goalie talent using their career Fenwick 5v5 save percentage. It concluded with the assumptions of the initial strategy, which I'll include again below.
</p>
<p>
Assumptions:
    - The prior distribution is assumed to be from the beta family.
    - Age is assumed to be irrelevant. 
    - Scoring rates are assumed to be constant.
    - <b>All shots are assumed to be equal.</b>
    - Team systems are assumed to be identical.
</p>
<p>
I'm going to address the fourth assumption, that all shots are equal, in this post.
</p>
<p>
<h5>Adjusted Save Percentage</h5>
We already know that not all shots are equal. Countless Exepected Goals models have been produced to address this. Thankfully, Peter Tanner, through his website <a href="https://moneypuck.com/about.htm">MoneyPuck</a>, provides detailed data for each unblocked shot that occurs in the NHL (whether it hit the net or not) along with a prediction - the probability of the shot being a goal.
</p>
<p>
We can adjust a goalie's save percentage by taking into account these predictions from MoneyPuck. There are many ways to do this, but I've decided to derive one which would retain the performance measure as a rate. Here's what I came up with:
</p>
<p>
Fenwick Save Percentage (FSV%) = 1 - (Goals Against / Fenwick Shots Against)<br>
Expected Fenwick Save Percentage (xFSV%) = 1 - (Expected Goals Against / Fenwick Shots Against)<br>
Median Save Percentage (MSV%) = Median of Goalie (20+ xG faced) Career Save Percentage<br>
<b>Adjusted Save Percentage (AdjSV%) = MSV% + (FSV% - xFSV%)</b>
</p>
<p>
For the sake of simplicity, let's flip the adjusted save percentage to the adjusted failure rate (1 - AdjSV%) and plot the distribution of career rates for goalies having faced more than 20 expected goals. We'll include a fitted beta distribution in white. The goodness of fit, which frankly was questionable in the last post, looks better this time. It'll improve as we try different distributions in future posts.
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
    - There's a 77.03% (previously 57.18%) chance that Swayman's AdjSV% better than Oettinger's.
    - There's a 86.88% (previously 92.57%) chance that Oettinger's AdjSV% is better than the MSV%.
    - There's a 96.50% (previously 91.81%) chance that Swayman's AdjSV% is better than the MSV%.
</p>
<p>
These changes are due to the fact that Swayman faces more difficult shots than Oettinger on a whole - his xFSV% is 94.07 while Oettinger's is 94.39.
</p>
<p>
<h5>Appendix</h5>
Below is a collection of plots which compare various save percentage metrics discussed in this + the last post.
</p>
<p>
Couple of points:
    - Goalies who have a bad start to their career tend to not play many games (surprise, surprise).
    - The relationship between a goalie's SV% and his AdjSV% seems to strengthen as he faces more shots.
    - A goalie's AdjSV% converges with his posterior AdjSV% as he faces more shots (that's the yellow diagonal line).
    - The consequence of the previous three points - there is heteroskedasticity in the relationship between a goalie's SV% and his posterior AdjSV%.
    - There is almost certainly survivorship bias. 
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-five-three.png" width="100%" length="250"/></div>
</p>
<p>
Code available here: <a href="https://github.com/spazznolo/goalie-performance/blob/main/posts/post-2.R">https://github.com/spazznolo/goalie-consistency/blob/main/posts/post-5.R</a>
</p>