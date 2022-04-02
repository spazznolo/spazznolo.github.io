---
layout: post
title:  "Does consistency matter in Goaltending? [Part 2]"
date:   2022-04-01 8:52:05 -0400
---

<h2> Does consistency matter in Goaltending? </h2>
<h2> Part 2 - Exploring the effects of goalie consistency using real data </h2>
<p>
In the <a href="https://spazznolo.github.io/2022/03/29/goalie-consistency-1.html">previous post</a>, the concept of entropy as a measure of consistency was <a href="https://github.com/namitanandakumar/Draft-Analysis/blob/master/Streakiness/VanHAC%202018.pdf">repurposed</a> for hockey goalies using simulated data. Here, it's applied to actual NHL data, supplied by <a href="https://moneypuck.com/">MoneyPuck</a>. This will be a short post - mostly descriptive. It tees up the next one.
</p>
<p>
Remember: to measure entropy, an entire goalie season is first turned into a binary sequence of 0's (saves) and 1's (goals). In the first post, because each generated goalie-season had the same save percentage, entropy could be compared as is. However in the real world, goalies stop pucks at different rates. This causes a problem, because the rarer an event is, the higher entropy it will tend to have. We address this by simulating 10,000 goalie-seasons for each goalie's season save percentage, and then calculate the percent of simulations which have less entropy than the one we observed in the real world. With this, we get something called <a href="https://repository.upenn.edu/cgi/viewcontent.cgi?article=1081&context=statistics_papers">normalized entropy</a>. Now that entropy has been normalized, it can be compared from goalie-to-goalie.
</p>
<p>

</p>
<h5>The effect of goalie-season consistency on save percentage</h5>
<p>
In this comparison, a goalie-season must include at least 800 shots and every shot is considered equal.
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-two-one.png" width="70%" length="200"/></div>
</p>
<p>
</p>
<h5>The most consistent goalie careers</h5>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-two-two.png" width="70%" length="200"/></div>
</p>
<h5>The effect of goalie consistency on career save percentage</h5>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-two-three.png" width="70%" length="200"/></div>
</p>
<h5>The effect of goalie consistency on career season-over-season save percentage</h5>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-two-four.png" width="70%" length="200"/></div>
</p>
<p>
</p>
<p>
</p>
<p>
</p>
<p>
</p>
<p>
</p>