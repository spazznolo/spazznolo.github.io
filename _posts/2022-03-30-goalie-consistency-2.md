---
layout: post
title:  "[Part 2] The effect of inter-shot goalie consistency on expected standing points "
date:   2022-03-30 11:52:05 -0400
---
<h2> The effect of inter-shot goalie consistency on expected standing points </h2>
<p>
Here’s what a ten-shot sequence of outcomes from shots on goal looks like (1 goal, 0 save).
</p>
<p>
<div style="text-align: center">0 0 0 0 1 0 0 0 1 0</div>
</p>
<p>
When measuring goalie performance, there is an important structural difference between shots and games. Games usually include multiple goals, while shots lead to binary events (goal or not). Shots can’t be treated in the same way as games were in the previous section - a poisson distribution is no longer fitting. 
</p>
<p>
Thankfully, given that shots are a sequence of binary events, we can borrow a concept from information theory for a more robust and generalized measure of consistency. It’s called <a href="https://spazznolo.github.io/2022/03/28/goalie-consistency-intro.html">entropy</a>.
<p>
A perfectly ordered sequence has no entropy, and as it loses its orderliness (or consistency), the entropy increase. 
</p>
<p>
But how does inter-shot consistency effect the expected standing points? 
</p>
<p>
This time, we create simulate 10,000 goalie seasons, all with seasonal save percentages of .900. Then, we calculate the entropy of each simulation, along with the expected standing points earned. The results are below.
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-one-threee.png" width="60%" length="150"/></div>
</p>
<p>
<em>Inter-shot consistency does not seem have an effect on expected standing points.</em>
</p>
<p>
The next post will use entropy as a measure for consistency (or the lack thereof) on real data. Given that entropy has been measured for shooters before, it will be a very similar exploration, except it will be applied to goalies. In the post after that, I’ll attempt to improve this by exploring goalie entropy using MoneyPuck’s Expected Goals.
</p>