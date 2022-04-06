---
layout: post
title:  " [Introduction] Does consistency matter in Goaltending?"
date:   2022-03-28 11:52:05 -0400
---
<h1> Does consistency matter in Goaltending? </h1>
<h2> Introduction </h2>
<p>
Goaltenders make up the least predictable position in hockey. Their behavior confounds analysts and casual fans alike. It isn’t uncommon for a strong goalie to have a below replacement level year, or for an unknown goalie to come in and dominate the league. This may partly explain the relative dearth of analysis on goalies - they're voodoo, some suggest.
</p>
<p>
That's where this series of posts comes in. Ideally, they will help - even marginally - rectify this dearth. I’m going to start by exploring the idea of consistency in goalies, along with the potential attendant effects it has on standing points, current performance, and future results. This post addresses the effect of consistency on standing points.
</p>
<p>
In this series, we'll measure the effect of goalie consistency (shot-to-shot, game-to-game, and from season-to-season) on various measures, such as: current performance, future performance, and future consistency.
</p>
<p>
But before that, I'll briefly explain a few concepts that will come up across the series.
</p>
<h5>Poisson Distribution</h5>
<p>
Goals have been <a href="http://www.hockeyanalytics.com/Research_files/Poisson_Toolbox.pdf">shown</a> to follow a <a href="https://en.wikipedia.org/wiki/Poisson_distribution">Poisson process</a>. Many simulations have shown just how closely goals follow the Poisson over time.
</p>
<p>
probability mass function of the Poisson distribution.
</p>
<h5>Entropy</h5>
<p>
Entropy, a popular concept in information theory, is a measure of orderliness in a sequence. or, in our case, the inter-shot consistency of a goalie. It was first introduced <a href="https://repository.upenn.edu/cgi/viewcontent.cgi?article=1081&context=statistics_papers">here</a> for various applications, and then <a href="https://github.com/namitanandakumar/Draft-Analysis/blob/master/Streakiness/VanHAC%202018.pdf">repurposed</a> for teams and shooters in hockey (we apply it to goalies in this post). The formula for entropy is below.
</p>
<p>
<div style="text-align: center"> 
<img src="https://spazznolo.github.io/figs/goalie-formula-entropy.png" width="50%" length="75"/>
</div>
</p>
<p>
This entropy formula gets us partway there, however it does not account for the length of a goalie season, nor does it take into account the percentage of shots saved - both of which have an effect on entropy. In order to compare entropy from goalie-to-goalie and season-to-season, we need to account for these differences. To address this, the xi's in the entropy formula above are divided by the number of shots in the goalie season, and then the entropy itself is divided by the number of goals scored in a season (plus one).
</p>


<p>
Here’s what a ten-shot sequence of outcomes from shots on goal looks like (1 goal, 0 save).
</p>
<p>
<div style="text-align: center">0 0 0 0 1 0 0 0 1 0</div>
</p>
<p>
When measuring goalie performance, there is an important structural difference between shots and games. Games usually include multiple goals, while shots lead to binary events (goal or not). Shots can’t be treated in the same way as games were in the previous section - a poisson distribution is no longer fitting. 
</p>



<h5>Expected Goals</h5>
<p>
Shot data for Expected Goals is provided by <a href="https://moneypuck.com/">MoneyPuck</a>. Tanner, MoneyPuck's creator, explains expected goals as "the probability of each shot being a goal", where information such as "the distance from the net, angle of the shot, type of shot, and what happened before the shot" is considered.
</p>




