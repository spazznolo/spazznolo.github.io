---
layout: post
title:  "The effect of regulation performance on overtime"
date:   2022-04-15 8:52:05 -0400
---
<h2>[Post 1] The effect of regulation performance on overtime</h2>
<p>
By most accounts, the outcome of the NHL's 5 minute 3-on-3 overtime is random. MoneyPuck, a popular website which predicts game outcomes in real time, doesn't even bother deviating from a coin flip probability for any team to win in overtime, regardless of their opponent. This is in line with betting odds, which, in a given overtime, usually offer -115 on either team (even odds before the <a href="https://en.wikipedia.org/wiki/Vigorish">vig</a>). 
</p>
<p>
This year, the Panthers, who've by far scored the most goals of any team this season, went 13-2 in overtime. The Avalanche, Hurricanes, and Leafs, the league's next best teams, went about .500.
</p>
<p>
Just how random is overtime?
</p>
<p>
Let's explore with a basic descriptive model. We'll regress various team and game characteristics on the outcome of <em>individual games which ended in overtime</em>. Specifically, the predictors will be: a team's xGF% throughout their season, game and overtime, whether they're playing at home, and whether they had the last shot before the winning goal was scored. A few examples:
</p>
<p>
<div style="text-align: center"> 
<img src="https://spazznolo.github.io/figs/post-regulation-one-one.png" width="60%" length="150"/>
</div>
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




