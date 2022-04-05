---
layout: post
title:  "Does consistency matter in Goaltending? [Introduction]"
date:   2022-03-28 11:52:05 -0400
---
<h2> Does consistency matter in Goaltending? </h2>
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
Entropy is a way to measure the orderliness of a sequence, or, in our case, the inter-shot consistency of a goalie. It was first introduced <a href="https://repository.upenn.edu/cgi/viewcontent.cgi?article=1081&context=statistics_papers">here</a> for various applications, and then <a href="https://github.com/namitanandakumar/Draft-Analysis/blob/master/Streakiness/VanHAC%202018.pdf">repurposed</a> for teams and shooters in hockey (we apply it to goalies in this post).
</p>
<h5>Expected Goals</h5>
<p>
</p>




