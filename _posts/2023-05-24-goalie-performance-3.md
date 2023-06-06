---
layout: post
title:  "Goalie Performance: Exploring the Distribution"
date:   2023-05-24 8:52:05 -0400
---
<h2>[Post 3] Goalie Performance: Exploring the Distribution</h2>
<p>
In the first post, I outlined a framework for measuring goalie talent using their career Fenwick 5v5 save percentage. A prior from the beta family was fit to the goalie career AdjSV% histogram, which yielded the hyper-parameters we built the posterior with (alpha of 56.45766, beta of 881.8847). There's a problem, though. To fit this prior, we had to throw out goalies who faced less than 10 xG. Unfortunately, 90 of the 314 goalies in our set were cut! Moreover, we treated goalies equally, meaning Zachary Fucale was considered to be as informative as Henrik Lundqvist. 
</p>
<p>
It turns out we can fix both issues outlined above with one change - instead of fitting a beta distribution with goalie AdjSV%, we can fit a negative binomial distribution with goalies' 1) shots faced and 2) adjusted saves. EXPLAIN MORE With this, we can include all goalies, as long as they have made a save and allowed a goal. These are totals, so the prior will be weighted towards experience.
</p>
<p>
Problem solved? 
</p>
<p>
Not really. Think of which kind of goalies get to gain experience - if a goalie performs well, they'll keep getting more chances to play; if they play poorly, they'll get less chances until, finally, they are no longer given the chance to play. Therefore, the extent of a goalie's experience is biased by his performance. For now, we sidestep the problem with fitting a "correct" distribution and further explore experience.
</p>
<p>
<h5>Exploring Experience</h5>
To start, we can't keep every goalie in our population for this analysis. We just don't know how much experience a goalie had before the 2007-2008 season, so any goalie playing that season has to be removed. The same is true for the goalies playing the 2022-2023 season. As an example, we don't know how Jeremy Sayman's career will turn out - we only know what he's done in his first few seasons, so we can't properly categorize his career yet.
</p>
<p>
Here's a short summary of the reduced population:
    - Goalie population drops from 315 to 140.
    - Harmonic mean of shots against rises from 12,690 to 14,568 (mean drops, 4,198 to 3,225).
    - Harmonic mean of AdjSV% stays at .939 (mean drops, .932 to .927).
    - Mean of career shots faced drops from 4,198 to 3,225.
    - Mean of AdjSV% drops from .932 to .927.
</p>
<p>
To conextualize goalie career lengths, we plot the percentage of goalies having faced at least a certain number of shots throughout their careers. This is also known as the cumulative distribution function (cdf) of career shots faced for goalies. 
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-six-one.png" width="60%" length="150"/></div>
</p>
<p>
Some thoughts:
    - 25% of goalies faced 33 shots or less (!).
    - 50% of goalies faced 202 shots or less (that's about 7 games).
    - 75% of goalies faced 2,606 shots or less.
</p>
<p>
Another perspective on goalie longevity is the number of seasons played. This measure differs from shots for goalies who play more games per season (starters). Again, we plot the cdf, but this time for goalie career seasons played.
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-six-two.png" width="60%" length="150"/></div>
</p>
<p>
Some thoughts:
    - 42% of goalies played only one season.
    - 74% of goalies played five seasons or less.
    - 90% of goalies played twelve seasons or less.
</p>
<p>
It should now be obvious that most goalies don't really have a typical NHL career as we imagine them. Let's confirm the assumption that goalies with more experience perform better than those with less. Simple plot, we group goalies by career seasons played and then take the average AdjSV% for each group; seasons played on the x-axis against mean AdjSV% on the y-axis. 
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-six-three.png" width="60%" length="150"/></div>
</p>
<p>
What does this mean for the prior distribution? Do we weigh the observations by shots faced, which is biased towards goalies with experience, or treat all goalies equally, losing nearly 30% of our population (albeit less than 1% of shots faced) at the same time?
</p>

<p>
It is difficult to understand a goalie's path by looking at their save percentage or shots faced in isolation. What's nice about the empirical Bayesian method introduced in the previous posts is that it considers these measures at the same time. Moreover, we can repeatedly re-evaluate a goalie's pAdjSV% after each shot they face. We can then plot this posterior over each shot of a goalie's career to get a sense of their path. In order to extract more insight from this, let's section goalies by their career shots faced, like this:
</p>
<p>
Goalies facing:
    - less than 300 shots -> -0300.
    - more than 300 shots, but less than 1,500 -> -1500.
    - more than 1,500 shots, but less than 6,000 -> -6000.
    - more than 6000 -> 6000+.
</p>
<p>
As an example, Braden Holtby's pAdjSV% after facing various shot totals:
    - 0 shots: 0.9417 (as is every goalie's)
    - 1,000 shots: 0.9421
    - 5,000 shots: 0.9425
    - 10,000 shots: 0.9452
    - 15,000 shots: 0.9450
    - 19,555 shots: 0.9433
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-six-three.png" width="60%" length="150"/></div>
</p>
<p>
Some thoughts:
    - Nearly every goalie (77.1%) who faces -6000 shots ends his career with a pAdjSV% below expected.
    - Goalies facing 1500+ but -6000 seem to fade as their career progresses.
    - These goalies tend to be backups, facing ~600-1000 shots a season.
    - This fade could partly be due to aging effects.
</p>
<p>
To get a clearer sense of the dynamics described above, let's take the group average pAdjSV% through each shot faced.
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-six-four.png" width="60%" length="150"/></div>
</p>
<p>
Some thoughts:
    - The effects are much clearer here.
    - There isn't much to glean from goalies facing -300 shots.
    - These short NHL careers are almost certainly due to reasons outside their play in the NHL.
    - Goalies facing -1500 shots fade quickly. They are given a decent look and fail acutely.
    - Goalies facing -6000 shots start as the best group through the first 1,000 shots, then fade.
    - This seemingly unintuitive result is likely due to randomness, and, more interestingly, age.
</p>
<p>
Let's revisit the unintuive plot comparing pAdjSV% over goalie careers, grouped by career length. This time, we'll plot the average age of goalies in each group as they face shots over their career.
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-six-six.png" width="60%" length="150"/></div>
</p>
<p>
Some thoughts:
    - Goalies facing -6000 shots are ~1.5 years older than 6000+ goalies throughout their career.
    - This difference obviously includes the span from age 23 to roughly 27.
    - This is precisely the age range in which goalies seem to be improving in AdjSV%.
    - We can adjust for this.
</p>
<p>
In the next post, we explore how age is a confounder in assessing goalie performance.
</p>
<p>
Code available here: <a href="https://github.com/spazznolo/goalie-consistency/blob/main/posts/post-6.R">https://github.com/spazznolo/goalie-consistency/blob/main/posts/post-6.R</a>
</p>