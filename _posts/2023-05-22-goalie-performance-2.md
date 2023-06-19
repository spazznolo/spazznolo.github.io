---
layout: post
title:  "Goalie Performance: Empirical Bayes Adjusted Save Percentage"
date:   2023-05-22 8:52:05 -0400
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
It is well-known that not all shots are equal. Various Expected Goals (xG) models have been developed to account for this. Fortunately, Peter Tanner's website <a href="https://moneypuck.com/about.htm">MoneyPuck</a> provides detailed data on each unblocked shot in the NHL, including the probability of the shot being a goal.
</p>
<p>
To adjust a goalie's save percentage, we can incorporate these predictions from MoneyPuck. One approach to retain the performance measure as a rate is as follows:
</p>
<p>
Fenwick Save Percentage (FSV%) = 1 - (Goals Against / Fenwick Shots Against)<br>
Expected Fenwick Save Percentage (xFSV%) = 1 - (Expected Goals Against / Fenwick Shots Against)<br>
Median Save Percentage (MSV%) = Median of Goalie (20+ xG faced) Career Save Percentage<br>
<b>Adjusted Save Percentage (AdjSV%) = MSV% + (FSV% - xFSV%)</b>
</p>
<p>
For simplicity, let's represent the adjusted save percentage as the adjusted failure rate (1 - AdjSV%) and plot the distribution of career rates for goalies who have faced more than 20 expected goals. We will also include a fitted beta distribution in white. The goodness of fit appears better compared to the previous post, but further improvement can be achieved by exploring different distributions in future posts.
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-five-one.png" width="60%" length="150"/></div>
</p>
<p>
Since we are fitting a beta distribution once again, the remaining steps remain the same as the previous post.</p>
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
These changes occur because Swayman faces more difficult shots on average, with an xFSV% of 94.07 compared to Oettinger's 94.39.
</p>
<p>
<h5>Appendix</h5>
Below is a collection of plots which compare various save percentage metrics discussed in this and the previous post.
</p>
<p>
A couple of key points:

    - Goalies who have a poor start to their career tend to play fewer games (surprise, surprise).
    - The relationship between a goalie's SV% and their AdjSV% seems to strengthen as they face more shots.
    - A goalie's AdjSV% converges with their posterior AdjSV% as they face more shots (indicated by the yellow diagonal line).
    - Due to the previous points, there is heteroskedasticity in the relationship between a goalie's SV% and their posterior AdjSV%.
    - There is likely survivorship bias present.
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-five-three.png" width="100%" length="250"/></div>
</p>
<p>
Code available here: <a href="https://github.com/spazznolo/goalie-performance/blob/main/posts/post-2.R">https://github.com/spazznolo/goalie-consistency/blob/main/posts/post-5.R</a>
</p>