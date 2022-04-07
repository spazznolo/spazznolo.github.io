---
layout: post
title:  "[Part 2] The effect of inter-shot goalie consistency on expected standing points "
date:   2022-03-30 11:52:05 -0400
---
<h2> The effect of inter-shot goalie consistency on expected standing points </h2>
<p>
Remember, <a href="https://spazznolo.github.io/2022/03/28/goalie-consistency-intro.html">entropy</a> can be used to measure inter-shot goalie consistency. 
</p>
<p>
To measure the effect of inter-shot consistency on expected standing points, we simulate 10,000 goalie seasons, all with seasonal save percentages of .900. Here, all shots are considered equally likely to become goals. Then, we calculate the entropy of each simulation, along with the expected standing points earned. The results are below.
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-one-threee.png" width="60%" length="150"/></div>
</p>
<p>
<em>Inter-shot consistency does not seem have an effect on expected standing points.</em>
</p>
<p>
The <a href="https://spazznolo.github.io/2022/04/04/goalie-consistency-3.html">next post</a>  will use entropy as a measure for goalie consistency on real data. It will be a similar exploration to <a href="https://github.com/namitanandakumar/Draft-Analysis/blob/master/Streakiness/VanHAC%202018.pdf">this one</a> on shooters, except it will be expanded to include weights on shots in the form of <a href="https://moneypuck.com/">MoneyPuck</a>’s Expected Goals.
</p>