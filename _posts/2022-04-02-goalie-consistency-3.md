---
layout: post
title:  "[Part 3] The effects of inter-shot goalie consistency (using NHL data)"
date:   2022-04-04 8:52:05 -0400
---
<h2> The effects of inter-shot goalie consistency (using real data) </h2>
<p>
In the second post, we used raw entropy as a measure of goalie consistency because the simulated goalie seasons all had the same save percentage (.900). However in the real world, some goalies play more games than others, and they stop pucks at different rates too. To address this, entropy is normalized as described in the <a href="https://repository.upenn.edu/cgi/viewcontent.cgi?article=1081&context=statistics_papers">Introduction</a>.
</p>
<p>
This isn't it though, because not all shots have the same probability of going in. Many factors influence the probability of a shot turning into a goal. Some of these are captured in the public expected goals model created by Peter Tanner at <a href="https://moneypuck.com/about.htm">MoneyPuck</a>.
</p>
<p>
ONE PARAGRAPH ABOUT XG APPLICATION
</p>
<p> 
It turns out - as the plots below will show - that there isn't much there. Consistency in a given season doesn't say much about consistency in another season, better goalie careers don't appear to be more or less consistent than a worse career, etc. 
</p>
<p>
Note: A goalie season must include at least 800 shots (roughly 20 games) to be included in the season comparisons, and goalie-career must include at least 5 seasons, facing at least 800 shots in each, to be included in the career comparisons.
</p>
<h5>Inter-shot goalie consistency does not have an effect on overall performance.</h5>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-three-one.png" width="60%" length="150"/></div>
</p>
<h5>The 10 streakiest goalie careers.</h5>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-three-twoo.png" width="60%" length="150"/></div>
</p>
<h5>The 10 least streaky goalie careers.</h5>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-three-threee.png" width="60%" length="150"/></div>
</p>
<h5>Goalie inter-shot consistency does not have an effect on career season-over-season consistency.</h5>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-three-four.png" width="60%" length="150"/></div>
</p>