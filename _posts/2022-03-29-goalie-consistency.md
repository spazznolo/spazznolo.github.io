---
layout: post
title:  "Does consistency matter in Goaltending? [Part 1]"
date:   2022-03-29 11:52:05 -0400
---
<h5> Does consistency matter in Goaltending? </h5>
<p>
</p>
<h5> Part 1 - The effect of goalie consistency on expected standing points </h5>
<p>
Goaltenders make up the least predictable position in hockey. Their behaviour confounds analysts and casual fans alike. It isn’t uncommon for a strong goalie to have a below replacement level year, or for an unknown goalie to come in and dominate the league. This may partly explain the relative dearth of analysis on goalies - they're voodoo, some suggest.
</p>
<p>
That's where this series of posts comes in. Ideally, they will help - even marginally - rectify this dearth. I’m going to start by exploring the idea of consistency in goalies, along with the potential attendant effects it has on standing points, current performance, and future results. 
</p>
<p>
Consistency can be measured through various perspectives. For example, it can be measured from shot-to-shot, from game-to-game or from season-to-season. The first two perspectives are addressed in this post. The third will be addressed in another post.
</p>
<p>
<h5> The effect of inter-game consistency on expected standing points </h5>
</p>
<p>
Here’s an illustration: Imagine you’re the General Manager of a hockey team in a league where every single player and goalie is equally skilled. Since all players are equal, all teams are equal too. Now, a special opportunity comes up where you get to decide between eight equally skilled goalies who have different levels of consistency.
</p>
<p>
Goalie A always plays average, no matter what.
Goalie B plays half his games slightly above average, and the other half slightly below average.
Goalie C plays half his games a little better than B’s good games, and the other half a little worse than B’s bad games.
And so on...
</p>
<p>
Which do you want to play for you?
</p>
<p>
In order to decide, it helps to understand the underlying structure of goals in hockey. Goals have been <a href="http://www.hockeyanalytics.com/Research_files/Poisson_Toolbox.pdf">shown</a> to follow a <a href="https://en.wikipedia.org/wiki/Poisson_distribution">Poisson process</a>. Many simulations have shown just how closely goals follow the Poisson over time. Not only is this a clean approximation, it can also easily be simulated.
</p>
<p>
In this simulation, the number of goals a goalie allows will be represented by a set of poisson distributions, and the expected quality of play will be represented by the poisson’s expected rate of occurrences, such that in an average game, a goalie is expected to allow around 3 goals; in a slightly below average game around 3.25 goals; below average around 3.50, and so on… 
</p>
<p>
Running 10,000 simulations of 82 game seasons yields the following distributions of expected standings points.
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-plot-two.png" width="70%" length="200"/></div>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-plot-three.png" width="30%" length="50"/></div>
</p>
<p>
It turns out <em>the average expected standing points increases as a goalie’s inter-game consistency decreases</em>. If that’s surprising to you, you’re not alone - it is a little paradoxical. 
</p>
<p>
However, if you accept that goals follow a poisson distribution (which <a href="https://www.lakeheadu.ca/sites/default/files/uploads/77/docs/DejardineFinal.pdf">you</a> <a href="https://verbumdata.netlify.app/2019/09/15/picking-nhl-poisson/">should</a>!), the fact that a goalie who expects to allow 1 and 5 goals a game gets more standing points than one who is always expected to allow 3 is self-evident. It can even be eye-balled using the probability mass function of the Poisson distribution.
</p>
<p>
Still not convinced? Take the scores from past NHL seasons and look at the actual standing points % won when teams allow 0-6 goals. A team can expect higher standing points % allowing 2 and 4 goals (or 1 and 5, or 0 and 6) than it can allowing 3 goals twice.
</p>
<p>
Some other takeaways:
</p>
<p>
- The variance in expected standing points increases as a goalie’s consistency increases. This too might seem paradoxical, but actually it’s pretty simple if you think about it - a goalie who we expect to allow 70% of goals some games and 30% of goals the other leads to relatively certain in-game results.
</p>
<p>
- The difference in expected standing points might seem small (about 5, or 2.4 wins, over a standard 82 game season), but it could be the difference between making and missing the playoffs.
</p>
<p>
This may all be interesting, but is it helpful? By itself, <b>not really</b>. <em>A goalie can’t and will never be inconsistent from game to game on purpose.</em> It does lead to other questions though, like: are some goalies inconsistent by nature?; are they inconsistent from season-to-season as well? how about from shot-to-shot? and what is the effect of inter-shot consistency on expected standing points?
</p>
<p>
<h5> The effect of inter-shot consistency on expected standing points </h5>
</p>
<p>
Here’s what a ten-shot sequence of outcomes from shots on goal looks like (1 goal, 0 save).
</p>
<p>
0 0 0 0 1 0 0 0 1 0
</p>
<p>
Notice, there is an important structural difference in the consistency between shots and games. Shots lead to binary events (goal or not). Shots can’t be treated in the same way as games were in the previous section - a poisson distribution is no longer fitting. 
</p>
<p>
Thankfully, given that this is a sequence of binary events, we can borrow from information theory for a more robust and generalized measure of consistency. It’s called <a href="https://en.wikipedia.org/wiki/Entropy_(information_theory)">entropy</a>. Entropy is a way to measure the orderliness of a sequence, or, in our case, the inter-shot consistency of a goalie. It was first introduced <a href="https://repository.upenn.edu/cgi/viewcontent.cgi?article=1081&context=statistics_papers">here</a> for various applications, and then <a href="https://repository.upenn.edu/cgi/viewcontent.cgi?article=1081&context=statistics_papers">repurposed</a> for teams and shooters in hockey (we apply it to goalies in this post).
</p>
<p>
A perfectly ordered sequence has no entropy, and as it loses its orderliness (or consistency), the entropy rises. But how does this decrease in inter-shot consistency effect the expected standing points? 
</p>
<p>
This time, 10,000 random sequences of goalie seasons are created all with the same seasonal save percentage of .900. Then, the entropy of each random sequence is calculated along with the expected standing points earned. The results are below.
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-plot-four.png" width="70%" length="200"/></div>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-plot-six.png" width="70%" length="200"/></div>
</p>
<p>
<em>Inter-shot consistency does not seem have an effect on expected standing points.</em>
</p>
<p>
The next post will use the normalized entropy measure for consistency (or the lack thereof) on real data. Given that entropy has been measured for shooters before, it will be a very similar exploration, except it will be applied to goalies. In the post after that, I’ll attempt to improve this by exploring goalie entropy using MoneyPuck’s Goals Saved Above Average.
</p>
<p>
<em>Note: For clarity’s sake, I introduced game-to-game consistency without randomness (a goalie was expected to be above average and below average in half of his games), but this also works with randomized expectations. The plot below compares the distribution of standing points when the expected rate of occurrence is randomly sampled from the uniform distribution to those when the expected rate of occurrence is the average expected goals against. The expected difference between a perfectly steady goalie and a perfectly random goalie is about 7 standing points!</em>
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-plot-one.png" width="70%" length="200"/></div>
</p>