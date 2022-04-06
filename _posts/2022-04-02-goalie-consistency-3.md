---
layout: post
title:  "[Part 3] The effects of inter-shot goalie consistency (using NHL data)"
date:   2022-04-04 8:52:05 -0400
---
<h2> The effects of inter-shot goalie consistency (using real data) </h2>
<p>
In the <a href="https://spazznolo.github.io/2022/03/29/goalie-consistency-1.html">previous post</a>, the concept of entropy as a measure of consistency was <a href="https://github.com/namitanandakumar/Draft-Analysis/blob/master/Streakiness/VanHAC%202018.pdf">repurposed</a> for hockey goalies using simulated data. Here, it's applied to actual NHL data (2007-2020), supplied by <a href="https://moneypuck.com/">MoneyPuck</a> (check it out! he does great work). This will be a short post - mostly descriptive. It tees up the next one.
</p>
<p>
Remember: to measure entropy, an entire goalie season is first turned into a binary sequence of 0's (saves) and 1's (goals). Then, xxx. 
</p>
<p>
In the first post, entropy was compared as is because each simulated goalie-season had the same save percentage (.900). However in the real world, goalies stop pucks at different rates. This causes a problem, because the rarer an event is, the higher entropy it will tend to have. We address this by simulating 10,000 seasons for each goalie season's save percentage, and then calculate the percent of simulations which have less entropy than the one we observed in the real world. This leads to <a href="https://repository.upenn.edu/cgi/viewcontent.cgi?article=1081&context=statistics_papers">normalized entropy</a>.
</p>
<p>
Now that entropy has been normalized, it can be compared from goalie-to-goalie.
</p>
<p>
Note: A goalie-season must include at least 800 shots (roughly 20 games) to be included in the season comparisons, and goalie-career must include at least 5 seasons, facing at least 800 shots in each, to be included in the career comparisons.
</p>
<h5>Goalie-season consistency does not have an effect on save percentage.</h5>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-three-one.png" width="60%" length="150"/></div>
</p>
<h5>The 10 streakiest goalie careers.</h5>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-three-twoo.png" width="60%" length="150"/></div>
</p>
<h5>The 10 least streakiest goalie careers.</h5>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-three-threee.png" width="60%" length="150"/></div>
</p>
<h5>Goalie consistency does not have an effect on career season-over-season consistency.</h5>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-three-four.png" width="60%" length="150"/></div>
</p>