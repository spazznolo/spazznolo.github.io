---
layout: post
title:  "The effect of regulation performance on overtime"
date:   2022-04-15 8:52:05 -0400
---
<h2>[Post 1] The effect of regulation performance on overtime</h2>
<p>
By most accounts, the outcome of the NHL's 5 minute 3-on-3 overtime is random. MoneyPuck, a popular website which predicts game outcomes in real time, doesn't even bother deviating from a coin flip probability for any team to win in overtime, regardless of their opponent. This is in line with sports betting sites, which, in a given overtime, usually offer -115 odds for both teams (even odds before the <a href="https://en.wikipedia.org/wiki/Vigorish">vig</a>). 
</p>
<p>
This year, the Panthers, who've by far scored the most goals of any team this season, went 13-2 in overtime. The Avalanche, Hurricanes, and Leafs, the league's next best teams, went about .500.
</p>
<p>
Just how random is overtime?
</p>
<p>
Let's explore with a basic descriptive model. We'll regress various team and game characteristics on the outcome of <em>individual games which ended in overtime</em>. Specifically, the predictors will be: a team's xGF% throughout their season, game and overtime (before the winning goal was scored), whether they're playing at home, and whether they had the last shot before the winning goal was scored. A few examples:
</p>
<p>
<div style="text-align: center"> 
<img src="https://spazznolo.github.io/figs/post-regulation-one-oneee.png" width="60%" length="150"/>
</div>
</p>
<p>
Using every game that ended in overtime since its inception in 2015, the regression looks like this:
</p>
<p>
<div style="text-align: center"> 
<img src="https://spazznolo.github.io/figs/post-regulation-one-two.png" width="60%" length="150"/>
</div>
</p>
<p>
<b>Translation: </b>Whether a team had the last shot before the winning goal was scored is the strongest predictor of a win out of the five predictors. It adds about 15% to a team's win probability. A 10% increase in xGF% of a given overtime adds about 3.8% to the team's win probability. This might seem like alot, but 75% of Expected Goals is total domination, which translates to 75-50=25*0.0038... Neither a team's regular season xGF% or their regulation xGF% have an effect on the outcome of the game. 
</p>




