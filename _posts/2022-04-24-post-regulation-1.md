---
layout: post
title:  "Measuring the uncertainty caused by the current overtime format"
date:   2022-04-24 8:52:05 -0400
---
<h2>[Post 1] Measuring the uncertainty caused by the current overtime format</h2>
<p>
By most accounts, the outcome of the NHL's 5 minute 3-on-3 overtime is random. <a href="https://moneypuck.com/">MoneyPuck</a>, a popular website which predicts game outcomes in real time, assigns a coin flip probability for any team to win in overtime, regardless of their opponent. This is in line with sports betting sites, which, in a given overtime, usually offer -115 odds for both teams (even odds before the <a href="https://en.wikipedia.org/wiki/Vigorish">vig</a>). 
</p>
<p>
For now, let's take this at face value (we'll save the skepticism for another post). The consequence is that, after regulation time, the team's essentially flip a coin to determine the winner. If a given team happens to get lucky and land a bunch of heads, it gets more points than another team who happened to land a bunch of tails.  This added randomness is a problem - it causes uncertainty in the final standing points, which could have an effect on the final rankings and, importantly, if a team makes the playoffs or not - or a team's chance at winning the draft lottery.
</p>
<p>
But how much uncertainty does the current playoff format add?
</p>
<p>
To measure this, we'll create a synthetic conference of teams. Each synthetic team is assigned a regulation points total based on the average regulation standing points of their rank (the average regulation standing points of the first ranked teams in the conference from 2015-2019 [0.637, 0.67, xx] is the first ranked synthetic team. And so on... It looks something like this:
</p>
<p>
<div style="text-align: center"> 
<img src="https://spazznolo.github.io/figs/post-regulation-one-onee.png" width="60%" length="150"/>
</div>
</p>
<p>
Now we assign the average number of overtime games (23%, or about 19, regardless of team ranking) to each team, and flip coins by way of the binomial to determine the number of overtime points won for each team. 
</p>
<p>
A team can expect to stray from their expected standing points by about 1.76 points. On average, the largest swings (both positive and negative) are about 4.4 standing points. For context, we can simulate seasons with: 1) the synthetic conference of teams with regulation point totals and 2) coin flips to determine overtime winners. With this, we can see in what percentage of seasons a team who would have made the playoffs with their regulation points misses with the extra overtime point (about 44%), as well as the average number of ranking changes which occur in a given year due to the overtime point (about 5.5).
</p>







