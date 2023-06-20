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
In the <a href="https://spazznolo.github.io/2023/05/17/goalie-performance-1.html">first post</a>, I outlined a framework for measuring goalie talent using their career Fenwick 5v5 save percentage. It concluded with the assumptions of the initial strategy, which I'll include again below.
</p>
<p>
Assumptions:
    - <b>All shots are assumed to be equal.</b>
    - The prior distribution is assumed to be beta with hyperparameters 852 and 55.6.
    - Goalies facing less than 200 shots are ignored.
    - Age is assumed to be irrelevant.
    - Scoring rates are assumed to be constant.
    - Team systems are assumed to be identical.
</p>
<p>
In this post, I'm going to address the first assumption and propose an adjustment.
</p>
<p>
<h5>Adjusted Save Percentage</h5>
All shots are not equal, in that they do not have the same probability of becoming a goal. This is established. Many Expected Goals (xG) models have been developed to account for this. Fortunately, Peter Tanner's website <a href="https://moneypuck.com/index.html">MoneyPuck</a> provides detailed data on each unblocked shot in the NHL, including the probability of the shot being a goal according to his <a href="https://moneypuck.com/about.htm">logistic regression model</a>.
</p>
<p>
To adjust a goalie's save percentage for shot quality, we can incorporate these expected goal probabilities from MoneyPuck. Usually, after accounting for shot quality, goalie performance is measured by the number of goals saved above expected (GSAx). This changes the metric from a rate (percentage of shots saved) which is bounded by 0 and 1 to one that can include any real number. Unfortunately, the beta distribution only works with rates. One approach to retain the metric as a rate, and thus the beta distribution as prior, is as follows:
</p>
<p>
Fenwick Save Percentage (FSV%) = 1 - (Goals Against / Fenwick Shots Against)<br>
Expected Fenwick Save Percentage (xFSV%) = 1 - (Expected Goals Against / Fenwick Shots Against)<br>
Median Save Percentage (MSV%) = Median of Goalie (20+ xG faced) Career Save Percentage<br>
<b>Adjusted Save Percentage (AdjSV%) = MSV% + (FSV% - xFSV%)</b>
</p>
<p>
Let's plot the distribution of career AdjSV% for goalies who have faced 200+ shots. We will also include a fitted beta distribution in white, and a weibull in red.
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-performance-2-1.png" width="60%" length="150"/></div>
</p>
<p>
At first glance, goalies' career AdjSV% seems to follow a weibull distribution! Cool, but we're going to sidestep this finding for the remainder of the post, because (hint, hint) <em>there maybe be more than one distribution here</em>. So we're fitting another beta, which means the remaining steps remain the same as the previous post.</p>
<p>
Let's revisit the Jake Oettinger and Jeremy Swayman comparison.
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-performance-2-2.png" width="60%" length="150"/></div>
</p>
<p>
The posteriors change as follows:
    - There's a 78.77% (previously 60.28%) chance that Swayman's AdjSV% better than Oettinger's.
    - There's a 88.28% (previously 94.12%) chance that Oettinger's AdjSV% is better than the MSV%.
    - There's a 97.30% (previously 93.81%) chance that Swayman's AdjSV% is better than the MSV%.
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
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-performance-2-3.png" width="100%" length="250"/></div>
</p>
<p>
Code available here: <a href="https://github.com/spazznolo/goalie-performance/blob/main/posts/post-2.R">https://github.com/spazznolo/goalie-performance/blob/main/posts/post-2.R</a>
</p>