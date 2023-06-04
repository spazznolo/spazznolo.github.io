---
layout: post
title:  "Goalie Performance: The Problem with Time"
date:   2023-05-24 8:52:05 -0400
---
<h2>[Post 3] Goalie Performance: The Problem with Time</h2>
<p>
In the first post, I outlined a framework for measuring goalie talent using their career Fenwick 5v5 save percentage. It concluded with the assumptions of the initial strategy, which I'll include again below.
</p>
<p>
Assumptions:
    - The prior distribution is assumed to be from the beta family.
    - Age is assumed to be irrelevant. 
    - The number of shots faced is assumed to be independent from performance.
    - Scoring rates are assumed to be constant.
    - All shots are assumed to be equal. 
    - Team systems are assumed to be identical.
</p>
<p>
I'm going to address the second and third points in this post, but in a sidewinding sort of way. 
</p>
<p>
Terms established in previous posts:
    - AdjSV%: A goalie's save percentage, adjusted for shot quality.
    - pAdjSV%: A goalie's posterior adjusted save percentage.
</p>
<p>
<h5>Exploring Experience</h5>
Let's start by defining our population. There aren't many NHL goalies, so we need to be greedy and take as many as we can for the analysis at hand. We don't know how much experience a goalie had before the 2007-2008 season, so any goalie playing that season has to be removed. The same is true for the goalies playing the 2022-2023 season. As an example, we don't know how Jeremy Sayman's career will turn out - we only know what he's done in his first few seasons, so we can't properly categorize his career yet.
</p>
<p>
Here's a short summary of the experience dataset:
    - Goalie population drops from 315 to 140.
    - Harmonic mean of shots against rises from 12,690 to 14,568 (mean drops, 4,198 to 3,225).
    - Harmonic mean of AdjSV% stays at .939 (mean drops, .932 to .927).
    - Mean of career shots faced drops from 4,198 to 3,225.
    - Mean of AdjSV% drops from .932 to .927.
</p>
<p>
To get a better sense of the longevity of a goalie career, we plot the percentage of goalies having faced at least a certain number of shots throughout their careers. This is also known as the cumulative distribution function (cdf) of career shots faced for goalies. 
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
It is difficult to understands a goalie's path by looking at their save percentage or shots faced in isolation. What's nice about the empirical Bayesian method introduced in the previous posts is that it considers these measures at the same time. Moreover, we can repeatedly re-evaluate a goalie's pAdjSV% after each shot they face. We can then plot this posterior over each shot of a goalie's career to get a sense of their path. In order to extract more insight from this, let's section goalies by their career shots faced, like this:
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
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-six-three.png" width="65%" length="165"/></div>
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
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-six-four.png" width="65%" length="165"/></div>
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
It's time to explore age.
</p>
<p>
<h5>Exploring Age</h5>
I scraped hockey-reference for each goalie's date of birth (code available <a href="https://github.com/spazznolo/goalie-consistency/blob/main/import/scrape_goalie_data.R">here</a>) in order to see how their performance changes as they age. By combining the goalies' dates of birth with the dates of their games, we can determine the exact age of a goaltender for each game they played. Unfortunately, a few goalies were not linked. 
</p>
<p>
The analysis population changes as follows:
    - Goalie population drops from 315 to 308.
    - Harmonic mean of shots against rises from 12,690 to 12,721 (mean rises, 4,198 to 4,286).
    - Harmonic mean of AdjSV% stays at .939 (mean rises, .932 to .933).
</p>
<p>
Let's start by simply grouping shots into bins by goalie age, rounded to the first decimal (ex: 26.0, 26.1, etc.), and then calculating the group-wide save percentage. Points belonging to groups with fewer shots pale in comparison to groups with many shots. Here's what that looks like:
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-six-five.png" width="60%" length="150"/></div>
</p>
<p>
Some thoughts:
    - Most shots are taken on goalies aged 23-35.
    - If you squint, you can see a little bit of an age curve here.
    - This plot is riddled with bias (particularly for goalies with short or long careers).
</p>
<p>
Let's fix some of the bias above with a few changes. Instead of simply grouping shots by age, we'll follow a well-worn strategy <a href = "https://hockey-graphs.com/2017/03/23/a-new-look-at-aging-curves-for-nhl-skaters-part-1">seemingly</a> developed by Tango Tiger <a href = "http://www.tangotiger.net/aging.html">here</a> called the delta method. Here are the steps:
    - Take change in save percentage (dSV%) from each goalie's age to the next. 
    - Take the harmonic mean of dSV% for each age as the the observed change in SV%.
    - Clip off underrepresented ages (-21, 39+).
    - Take the cumulative sum of dSV% throughout the retained age range.
</p>
<p>
Altogether, this gives us the curve below:
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-six-three.png" width="60%" length="150"/></div>
</p>
<p>
Some thoughts:
    - With this method, goalies peak around the age of 27.
    - This agrees with <a href="https://hockeyviz.com/txt/age22">some</a> past research.
    - This disagrees with <a href="https://hockey-graphs.com/2014/03/21/how-well-do-goalies-age-a-look-at-a-goalie-aging-curve/">other</a> past research.
    - There is well documented survivorship bias with this method.
</p>
<p>
INCLUDE PHANTOM YEARS HERE
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
<h5>Adjusting for Age</h5>
What do we mean by "adjusting" for age? Well, as a goalie progresses through his life, our expectations of him change. We do not expect a 15 year old goalie to play well in the NHL; we do not expect a 45 year old play well either. In between this, our expectations of the goalie increases up to a certain point (shown above to potentially be around age 27), and then decreases again for, well, forever. It follows that if a goalie starts his NHL career at 18 and faces 1000 shots, we have a different expectation of how many saves he should make than if he faced those shots starting his career at age 25. This is a definite shortcoming of the empirical Bayes strategy outlined in the 4th post.
</p>
<p>
The cleanest way to adjust for age would be to bake it into the already created adjustment for the probability of a shot being a goal. Taking the smoothed age curve presented above, we set the peak (age 27) as the standard and adjust for all other ages, so that, for example, an xFSV% of 0.940 at age 27 is 0.94000 - 0.00118 = 0.93882 at age 23 and 0.94000 - 0.00513 = 0.93487 at age 38.
</p>
<p>
Fenwick Save Percentage (FSV%) = 1 - (GA/FSA)<br>
<b>Age-Adjusted</b> Expected Fenwick Save Percentage (AdjxFSV%) = 1 - (xG/FSA) - Age Adjustment<br>
Median Save Percentage (MSV%) = Median of Goalie (20+ xG faced) Career Save Percentage<br>
<b>Adjusted (Age + xG) Save Percentage (AdjSV%) = MSV% + (FSV% - AdjxFSV%)</b>
</p>
<p>
Code available here: <a href="https://github.com/spazznolo/goalie-consistency/blob/main/posts/post-6.R">https://github.com/spazznolo/goalie-consistency/blob/main/posts/post-6.R</a>
</p>