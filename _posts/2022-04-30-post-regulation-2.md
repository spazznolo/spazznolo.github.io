---
layout: post
title:  "Is the overtime completely random?"
date:   2022-04-30 8:52:05 -0400
---
<h2>[Post 2] Is the overtime completely random?</h2>
<p>
By most accounts, the outcome of the NHL's 5 minute 3-on-3 overtime is random. <a href="https://moneypuck.com/">MoneyPuck</a>, a popular website which predicts game outcomes in real time, assigns a coin flip probability for any team to win in overtime, regardless of their opponent. This is in line with sports betting sites, which, in a given overtime, usually offer -115 odds for both teams (even odds before the <a href="https://en.wikipedia.org/wiki/Vigorish">vig</a>). 
</p>
<p>
This year, the Panthers, who've by far scored the most goals of any team this season, went 13-2 in overtime. The Avalanche, Hurricanes, and Leafs, the league's next best teams, went about .500.
</p>
<p>
Is overtime <em>completely</em> random, though?
</p>
<p>
Let's explore this thought with a basic descriptive model. <em>We'll regress various team and game characteristics on the outcome of individual games which ended in overtime</em>. Specifically, the predictors will be: a team's xGF% throughout their season and game. A few examples:
</p>
<p>
<div style="text-align: center"> 
<img src="https://spazznolo.github.io/figs/post-regulation-one-one.png" width="60%" length="150"/>
</div>
</p>
<p>
Using every game that ended in overtime since its inception in 2015, the regression can be summarized like this:
</p>
<p>
<div style="text-align: center"> 
<img src="https://spazznolo.github.io/figs/post-regulation-one-two.png" width="30%" length="75"/>
</div>
</p>
<h5>
Model Translation:
</h5>
By far, the strongest predictor of outcome for games ending in overtime is whether or not a team had the last shot before the winning goal was scored - it adds about 13.8% to a team's win probability (63.8%).
<p>
The only other relevant predictor is a team's xGF% in the overtime before the goal was scored. It's a distant second though: a 10% increase in xGF% adds about 1.9% to the team's win probability. This means that if a team dominates overtime with 75% of Expected Goals, its probability of winning only increases 4.7% (54.7%). 
</p>
<p>
A team's xGF% in the regular season and in a given game's regulation did not factor.
</p>
<h5>
Are all shots equal, though?
</h5>
In this model, all shots were considered equal. Given that the last shot before the goal is the most important factor in the outcome of an overtime, we shouldn't just treat them equally, however. Some questions: Do all shots lead to a higher chance in winning? Can we include games that did not end in the overtime to make the analysis more robust? Doesn't every shot matter, and not just the last ones?
<p>
In the next post, we'll build a win probability model based on each given shot's characteristics.
</p>



