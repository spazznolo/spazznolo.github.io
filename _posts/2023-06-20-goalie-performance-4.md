---
layout: post
title:  "Goalie Performance: Age is Confounding"
date:   2023-06-20 8:52:05 -0400
---
<h2>[Post 4: Still Working on this] Goalie Performance: Age is Confounding</h2>
<p>
In the first post, I outlined a framework for measuring goalie talent using their career Fenwick 5v5 save percentage. It concluded with the assumptions of the initial strategy, which I'll include again below.
</p>
<p>
Assumptions:
    - The prior distribution is assumed to be from the beta family.
    - <b>Age is assumed to be irrelevant.</b>
    - The number of shots faced is assumed to be independent from performance.
    - Scoring rates are assumed to be constant.
    - All shots are assumed to be equal. 
    - Team systems are assumed to be identical.
</p>
<p>
I'm going to address the second assumption, that age is assumed to be irrelevant, in this post.
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
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-seven-one.png" width="60%" length="150"/></div>
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
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-seven-two.png" width="60%" length="150"/></div>
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
<h5>Adjusting for Age</h5>
The above plot confirms the intuition that expectations for goalies depends on age. It follows that if a goalie starts his NHL career at 18 and faces 1000 shots, we have a different expectation of how many saves he should make than if he faced those same shots starting his career at age 25. This is a definite shortcoming of the empirical Bayes strategy outlined in the first post.
</p>
<p>
The cleanest way to adjust for age that I can think of is to bake it into the already created adjustment for the probability of a shot being a goal. Taking the smoothed age curve presented above, we set the peak (age 27) as the standard and adjust for all other ages, so that, for example, an xFSV% of 0.940 at age 27 is 0.94000 - 0.00118 = 0.93882 at age 23 and 0.94000 - 0.00513 = 0.93487 at age 38.
</p>
<p>
Fenwick Save Percentage (FSV%) = 1 - (GA/FSA)<br>
<b>Age-Adjusted</b> Expected Fenwick Save Percentage (AdjxFSV%) = 1 - (xG/FSA) - Age Adjustment<br>
Median Save Percentage (MSV%) = Median of Goalie (20+ xG faced) Career Save Percentage<br>
<b>Adjusted (Age + xG) Save Percentage (AdjSV%) = MSV% + (FSV% - AdjxFSV%)</b>
</p>
<p>
Code available here: <a href="https://github.com/spazznolo/goalie-performance/blob/main/posts/post-4.R">https://github.com/spazznolo/goalie-consistency/blob/main/posts/post-6.R</a>
</p>