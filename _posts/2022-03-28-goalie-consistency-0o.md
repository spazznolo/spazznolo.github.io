---
layout: post
title:  " [Introduction] Does consistency matter in Goaltending?"
date:   2022-03-28 11:52:05 -0400
---
<h1> Does consistency matter in Goaltending? </h1>
<h2> Introduction </h2>
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
<p>
Goals have been <a href="http://www.hockeyanalytics.com/Research_files/Poisson_Toolbox.pdf">shown</a> to follow a <a href="https://en.wikipedia.org/wiki/Poisson_distribution">Poisson process</a>. Many simulations have shown just how closely goals follow the Poisson over time. Fortunately, the Poisson is easy to simulate. Here's what 100,000 simulations of goals allowed in a game look like when a goalie is expected to allow 3 goals.
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-zero-one.png" width="60%" length="150"/></div>
</p>
<h5>Entropy</h5>
<p>
<a href="https://en.wikipedia.org/wiki/Entropy_(information_theory)">Entropy</a> is a popular concept in information theory. It measures the orderliness in a sequence, usually of binary events. Good news - shots can be expressed as a sequence of binary events. Here’s what a sequence of outcomes from shots on goal looks like (1 goal, 0 save).
</p>
<p>
<div style="text-align: center">0 0 0 0 1 0 0 0 1 0</div>
</p>
<p>
Consequently, entropy can be used to measure the inter-shot consistency of goalies. 
</p>
<p>
The application of entropy as a measure of consistency in sport was first (I think!) introduced <a href="https://repository.upenn.edu/cgi/viewcontent.cgi?article=1081&context=statistics_papers">here</a>, and then <a href="https://github.com/namitanandakumar/Draft-Analysis/blob/master/Streakiness/VanHAC%202018.pdf">repurposed</a> for teams and shooters in hockey. Here, we adapt previous work to obtain the starting formula for goalie entropy (below).
</p>
<p>
<div style="text-align: center"> 
<img src="https://spazznolo.github.io/figs/goalie-formula-entropy.png" width="50%" length="75"/>
</div>
</p>
<p>
This starting formula doesn't account for the length of a goalie season, nor does it account for the percentage of shots saved - both of which have an effect on entropy. It needs to be adjusted in order to compare entropy between goalies and between seasons. 
</p>
<h5>Normalized Entropy</h5>
<p>
To address this, the xi's in the entropy formula above are divided by the number of shots a goalie faces in a season, and then the entropy itself is divided by the number of goals a goalie allows in a season (plus one). After this, the entropy for each goalie is compared to that of 10,000 randomly generated seasons having the same performance - the entropy measure then becomes a percentile. This is exactly what was done previously for shooters. 
</p>
<p>
There is still a problem, though. All shots are currently considered equal. But it has been proven many times that <em>we should expect different goal rates for different shots</em>. One person in particular, Peter Tanner, has not only contributed to the idea of expected goals, but has generously made their work available for public consumption. Expected goals are summarized below, but the expansion of normalized entropy to include them is outlined in the <a href="https://spazznolo.github.io/2022/04/04/goalie-consistency-3.html">third post</a> of this series.
</p>
<h5>Expected Goals</h5>
<p>
Shot-level data for Expected Goals is provided by <a href="https://moneypuck.com/about.htm">MoneyPuck</a>. Tanner, MoneyPuck's creator, explains expected goals as "the probability of each shot being a goal", where information such as "the distance from the net, angle of the shot, type of shot, and what happened before the shot" is considered.
</p>




