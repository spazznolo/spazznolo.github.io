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
Is overtime <em>completely</em> random, though?
</p>
<p>
Let's explore this thought with a set of basic descriptive models. First, we'll regress a team's regulation point percentage on their overtime point percentage, then we'll regress two characteristics (one team and one game) on the outcome of individual games which ended in overtime. Specifically, the predictors will be: a team's xGF% throughout their season and game.
</p>
<p>
Comparing regulation points percentage to overtime points percentage:
</p>
<p>
<div style="text-align: center"> 
<img src="https://spazznolo.github.io/figs/post-regulation-two-one.png" width="60%" length="150"/>
</div>
</p>
<p>
There's nothing there. I added the regression results, but you don't need a regression to see that.
</p>
<p>
Another way to look at this is to regress regulation point percentage and regulation time xGF% on the outcome of individual games. But it's the same result - there's nothing there.
</p>
<p>
<div style="text-align: center"> 
<img src="https://spazznolo.github.io/figs/post-regulation-two-two.png" width="55%" length="125"/>
</div>
</p>
