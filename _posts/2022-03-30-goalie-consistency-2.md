---
layout: post
title:  "Goalie Consistency: The inter-game effect on expected standing points"
date:   2022-03-29 11:52:05 -0400
---
<head>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-DGRHZS5DNM"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-DGRHZS5DNM');
</script>
</head>
<h2>[Post 2] Goalie Consistency: The inter-game effect on expected standing points</h2>
<p>
Here’s an illustration: Imagine you’re the General Manager of a hockey team in a league where every single skater and goalie is equally skilled. Since all players are equal, all teams are equal too. Now, a special opportunity comes up where you get to decide between five equally skilled goalies who have different levels of consistency.
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
To help in this decision, let's run simulations. A set of random Poisson are generated, where the expected quality of play is represented by the Poisson’s expected rate of occurrences, such that in an average game, a goalie is expected to allow around 3 goals; in a slightly below average game around 3.25 goals; below average around 3.50, and so on… 
</p>
<p>
Running 10,000 simulations of 82 game seasons yields the following expected standings point distributions.
</p>
<p>
<table style="margin-left:auto;margin-right:auto;"><tr>
<td> <img src="https://spazznolo.github.io/figs/goalie-one-one.png" style="margin: 0px 15% 0px 20%" width="100%" length="300"/> </td>
<td> <img src="https://spazznolo.github.io/figs/goalie-one-two.png" style="margin: 0px 20% 0px 15%" width="75%" length="250"/> </td>
</tr></table>
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
- The variance in expected standing points increases as a goalie’s consistency increases. This too might seem paradoxical, but actually it’s pretty simple if you think about it - a goalie who we expect to allow 1 goal some games and 5 goals the other leads to relatively certain in-game results.
</p>
<p>
- The difference in expected standing points might seem small (about 5, or 2.4 wins, over a standard 82 game season), but it could be the difference between making and missing the playoffs.
</p>
<p>
But is any of this helpful? Taken alone, not really. <em>A goalie can’t and will never be inconsistent from game to game on purpose.</em> It does lead to other questions though, like: are some goalies inconsistent by nature?; are they inconsistent from season-to-season as well? how about from shot-to-shot? <em>and what is the effect of inter-shot consistency on expected standing points?</em> This last question is addressed in the <a href="https://spazznolo.github.io/2022/04/02/goalie-consistency-3.html">next post</a>.
</p>
<p>
</p>
<p>
<em>Note: For clarity’s sake, I introduced game-to-game consistency without randomness (a goalie was expected to be above average and below average in half of his games), but this also works with randomized expectations. The plot below compares the distribution of standing points when the expected rate of occurrence is randomly sampled from the uniform distribution to those when the expected rate of occurrence is the average expected goals against. The expected difference between a perfectly steady goalie and a perfectly random goalie is about 7 standing points!</em>
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-one-three.png" width="60%" length="150"/></div>
</p>

