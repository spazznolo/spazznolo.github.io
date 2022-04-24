---
layout: post
title:  "The effect of regulation performance on overtime"
date:   2022-04-10 8:52:05 -0400
---
<h2>[Post 1] The effect of regulation performance on overtime</h2>
<p>
By most accounts, the 5 minute 3-on-3 overtime used by the NHL is considered random. MoneyPuck doesn't even bother deviating from a 50% win probability for both teams. Just how random is overtime, though? Let's start this exploration with a basic descriptive model.
</p>
<p>
We'll regress various team and game characteristics on the outcome of individual overtimes, specifically a team's xGF% throughout their season, game and overtime, whether they're at home and whether they had the last shot before the winning goal. Here's a few examples:
</p>
<p>
</p>
<p>
A team's performance in regulation has little relation to its performance in overtime. On average, teams with a 10% increase in xGF% in regulation experience about a 1.9% increase in xGF% in overtime. This is about the same xGF% increase as a team gets in overtimes played at home (1.7%).
</p>
<p>
<div style="text-align: center"> 
<img src="https://spazznolo.github.io/figs/post-regulation-one-twoo.png" width="60%" length="150"/>
</div>
</p>
<p>
This isn't so surprising, though. Broken up into 5 minute chunks, hockey is actually pretty random! Breaking regulation time into 5 minute chunks, a 10% positive deviance in a team's xGF% in a given chunk leads to about a 0.2% increase in its xGF% performance in the next chunk. For context, the home team sits at a 1.5xGF% increase just for being at home.
</p>




