---
layout: post
title:  "Does consistency matter in Goaltending? [Part 1]"
date:   2021-11-28 11:52:05 -0400
---

<h5> Part 1 - The effect of consistency on expected standing points </h5>
<p>
Goaltenders make up the least predictable position in hockey. Their behaviour confounds analysts and casual fans alike. It isn’t uncommon for a great goalie to have a below replacement level year, or for an unknown goalie to come in and route the league. This may partly explain the relative dearth of analysis on goalies. Which is where this series of posts comes in. Ideally, they will help - even marginally - rectify this dearth.
</p>
<p>
I’m going to start by exploring the idea of consistency in goalies, along with the potential attendant effects it has on standing points, goals saved, and future results. 
</p>
<p>
Consistency can be measured through various perspectives. For example, it can be measured from shot-to-shot, from game-to-game or from season-to-season. The first two perspectives are addressed in this post. The third will be addressed in another post.
</p>
<p>

<h3> The effect of inter-game consistency on expected standing points </h3>
</p>
<p>
Here’s an illustration: Imagine you’re the General Manager of a hockey team in a league where every single player and goalie is equally skilled. Since all players are equal, all teams are equal too. Now, a special opportunity comes up where you get to decide between four equally skilled goalies who have different levels of consistency.
</p>
<p>
Goalie A always plays average, no matter what.
Goalie B plays half his games slightly above average, and the other half slightly below average.
Goalie C plays half his games a little better than B’s good games, and the other half a little worse than B’s bad games.
</p>
<p>
Which do you want to play for you?
</p>
<p>
In order to decide, it helps to understand the underlying structure of goals in hockey. Goals have been <a href="http://www.hockeyanalytics.com/Research_files/Poisson_Toolbox.pdf">shown</a> to follow a Poisson process. 
</p>
<p>
They can also be easily simulated.
</p>
<p>
In this simulation, the number of goals a goalie allows will be represented by a set of poisson distributions, and the expected quality of play will be represented by the poisson’s expected rate of occurrences, such that in an average game, a goalie is expected to allow around 3 goals; in a slightly below average game around 3.25 goals; below average around 3.50, and so on… 
</p>
<p>
Running 10,000 simulations of 82 game seasons yields the following distributions of expected standings points.
</p>
<p>
plot things
</p>
<p>
It turns out that the average expected standing points increases as a goalie’s inter-game consistency decreases. If that’s surprising to you, you’re not alone - it is a little paradoxical. 
</p>
<p>
However, if you accept that goals follow a poisson distribution (which <a href="https://www.lakeheadu.ca/sites/default/files/uploads/77/docs/DejardineFinal.pdf">you</a> <a href="https://verbumdata.netlify.app/2019/09/15/picking-nhl-poisson/">should</a>!), the fact that a goalie who expects to save 1 and 5 goals a game gets more standing points than one who is always expected to save 3 is self-evident. It can even be eye-balled using the probability mass function of the Poisson distribution.
</p>
<p>
Still not convinced? Take the scores from past NHL seasons and look at the actual standing points % won when teams allow 0-6 goals. A team can expect higher standing points % allowing 2 and 4 goals (or 1 and 5, or 0 and 6) than it can allowing 3 goals twice.
</p>
<p>
Some other takeaways:
</p>
<p>
- The variance in expected standing points increases as a goalie’s consistency increases. This might seem paradoxical, but actually it’s pretty simple if you think about it - a goalie who we expect to allow 70% of goals some games and 30% of goals the other leads to relatively pretty certain in-game results.
</p>
<p>
- The difference in expected standing points might seem small, but it could be the difference between making and missing the playoffs. more examples (show standing points earned by player and salary $ per standing point).
</p>
<p>
This may all be interesting, but is it helpful? By itself, not really. A goalie can’t and will never be inconsistent from game to game on purpose. It does lead to other questions though, like: are some goalies inconsistent by nature?; are they inconsistent from season-to-season as well? how about from shot-to-shot? and what is the effect of inter-shot consistency on expected standing points?
</p>
<p>
<h3> The effect of inter-shot consistency on expected standing points </h3>
</p>
<p>
Here’s what a sequence of outcomes from shots on goal looks like (1 goal, 0 save).
</p>
<p>
Notice, there is an important structural difference in the consistency between shots and games. Shots lead to binary events (goal or not). Shots can’t be treated in the same way as games were in the previous section - a poisson distribution is no longer fitting. 
</p>
<p>
Thankfully, we can borrow from information theory for a more robust and generalized measure of consistency in a sequence of binary events. It’s called entropy. Entropy is a way to measure the orderliness of a sequence, or, in our case, the inter-shot consistency of a goalie. First introduced… blah blah.
</p>
<p>

plot stuff

</p>
<p>
Inter-shot consistency does not seem have an effect on expected standing points.
</p>
<p>
The next post will use the normalized entropy measure for consistency (or the lack thereof) on real data. Given that entropy has been measured for shooters before here, it will be a very similar exploration, except it will be applied to goalies. In the post after that, I’ll attempt to improve this by exploring goalie entropy using MoneyPuck’s Goals Saved Above Average.
</p>
<p>
Note: For clarity’s sake, I introduced game-to-game consistency without randomness (a goalie was expected to be above average and below average in half of his games), but this also works with randomized expectations. The plot below compares the expected standing points when the expected rate of occurrence is randomly sampled from the uniform distribution to those when the expected rate of occurrence is the average expected goals against.
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-plot-one" width="70%" length="200"/></div>



