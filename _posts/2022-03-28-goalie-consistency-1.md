---
layout: post
title:  "Goalie Consistency: Does it matter?"
date:   2022-03-28 11:52:05 -0400
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
<h2>[Post 1] Goalie Consistency: Does it matter?</h2>
<p>
Goaltenders make up the least predictable position in hockey. Their behavior confounds analysts and casual fans alike. It isn’t uncommon for a strong goalie to have a below replacement level year, or for an unknown goalie to come in and dominate the league. This may partly explain the relative dearth of analysis on goalies - they're voodoo, it's often said.
</p>
<p>
That's where this series of posts comes in. Ideally, it will help - even marginally - rectify this dearth. I’m going to explore the idea of consistency in goalies, along with its potential attendant effects on standing points, current performance, and future performance.
</p>
<p>
But before that, in this post, I'll briefly explain a few concepts that will come up across the series.
</p>
<h5>Poisson Distribution</h5>
Goals have been <a href="http://www.hockeyanalytics.com/Research_files/Poisson_Toolbox.pdf">shown</a> to follow a <a href="https://en.wikipedia.org/wiki/Poisson_distribution">Poisson process</a>. Fortunately, the Poisson is easy to simulate. Here's what 100,000 simulations of goals allowed in a game look like when a goalie is expected to allow 3 goals.
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-zero-one.png" width="60%" length="150"/></div>
</p>
<p>
<em>The simulation of the Poisson to obtain outcomes for an exploration on inter-game goalie consistency occurs in the <a href="https://spazznolo.github.io/2022/04/04/goalie-consistency-1.html">second post</a> of this series.</em>
</p>
<h5>Entropy</h5>
<a href="https://en.wikipedia.org/wiki/Entropy_(information_theory)">Entropy</a> is a popular concept in information theory. It measures the orderliness in a sequence, usually of binary events. Good news - shots can be expressed as a sequence of binary events. Here’s what a sequence of outcomes from shots on goal can look like (1 goal, 0 save).
<p>
<div style="text-align: center">0 0 0 0 1 0 0 0 1 0</div>
</p>
<p>
Because of this, entropy can be used to measure the inter-shot consistency of goalies. 
</p>
<p>
The application of entropy as a measure of consistency in sport was first (I think!) introduced <a href="https://repository.upenn.edu/cgi/viewcontent.cgi?article=1081&context=statistics_papers">here</a>, and then <a href="https://github.com/namitanandakumar/Draft-Analysis/blob/master/Streakiness/VanHAC%202018.pdf">repurposed</a> for teams and shooters in hockey. We adapt this previous work to obtain the starting formula for goalie entropy (below).
</p>
<p>
<div style="text-align: center"> 
<img src="https://spazznolo.github.io/figs/goalie-formula-entropy.png" width="50%" length="75"/>
</div>
</p>
<p>
Since entropy sums streaks of saves, it follows that higher entropy equates to a lack of consistency - or conversely that low entropy equates to consistency. 
</p>
<p>
<em>Entropy is used to explore inter-shot goalie consistency in the <a href="https://spazznolo.github.io/2022/04/04/goalie-consistency-2.html">second post</a> of this series.</em>
</p>
<p>
There's a problem though. This starting formula doesn't account for the length of a goalie season, nor does it account for the percentage of shots saved - both of which have an effect on entropy. It needs to be adjusted if we're going to compare it between goalies and between seasons. 
</p>
<h5>Normalized Entropy</h5>
To address this, the xi's in the entropy formula above are divided by the number of shots a goalie faces in a season, and then the entropy itself is divided by the number of goals a goalie allows in a season (plus one). After this, the entropy for each goalie is compared to that of 10,000 randomly generated (by sampling without replacement) seasons having the same performance - it becomes a percentile. 
<p>
Up to now, this follows exactly the <a href="https://github.com/namitanandakumar/Draft-Analysis/blob/master/Streakiness/VanHAC%202018.pdf">previous work</a> on shooters. 
</p>
<p> 
There is still a problem, though - all shots are currently considered equal. But it has been proven <a href="https://hockeyviz.com/txt/xg5">many</a> <a href="https://evolving-hockey.com/blog/a-new-expected-goals-model-for-predicting-goals-in-the-nhl/">times</a> that <em>we should expect different goal rates for different shots</em>. Thankfully, Peter Tanner makes his work on Expected Goals available for public consumption. His take on them is summarized below.
</p>
<h5>Expected Goals</h5>
Tanner, through his website <a href="https://moneypuck.com/about.htm">MoneyPuck</a>, provides detailed data for each unblocked shot that occurs in the NHL (whether it hit the net or not) along with a prediction - the probability of the shot being a goal. His model includes information such as "the distance from the net, angle of the shot, type of shot, and what happened before the shot" among other things.
<p>
<em>The expansion of normalized entropy to include expected goals is outlined in the <a href="https://spazznolo.github.io/2022/04/04/goalie-consistency-3.html">third post</a> of this series.</em>
</p>
<p>
Posts in this series:
<a href="https://spazznolo.github.io/2022/03/30/goalie-consistency-2.html">
[Post 1] The effect of inter-game goalie consistency on expected standing points
</a> <a href="https://spazznolo.github.io/2022/04/02/goalie-consistency-3.html">
[Post 2] The effect of inter-shot goalie consistency on expected standing points
</a> <a href="https://spazznolo.github.io/2022/04/07/goalie-consistency-4.html">
[Post 3] The effects of inter-shot goalie consistency (using real data)
</a>





