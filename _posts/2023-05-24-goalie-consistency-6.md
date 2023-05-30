---
layout: post
title:  "Goalie Performance Assessment: The Problem with Time"
date:   2023-05-24 8:52:05 -0400
---
<h2>[Post 6] Goalie Performance Assessment: The Problem with Time</h2>
<p>
In post 4, I outlined a framework for measuring goalie talent using their career Fenwick 5v5 save percentage. It concluded with the assumptions of the initial strategy, which I'll include again below.
</p>
<p>
Assumptions:
    - The prior distribution is assumed to be from the beta family.
    - Age is assumed to be irrelevant. 
    - Scoring rates are assumed to be constant.
    - All shots are assumed to be equal. 
    - Team systems are assumed to be identical.
</p>
<p>
I'm going to address the second point in this post, but before I do, I wanted to share an interesting (though probably intuitive) finding. Below is the cumulative distribution function for seasons played during their career for goalies who haven't played the first (2007-2008) or last season (2022-2023) from the available data (this way we remove goalies who are in the middle of their careers). It shows that almost 50% of goalies who have played an NHL game ended up only playing one season.
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-six-one.png" width="60%" length="150"/></div>
</p>
<p>
Summary of findings (for careers starting after 2007-2008 and ending before 2022-2023):
    - 47% of goalies played only one season.
    - 70% of goalies played three seasons or less.
    - 91% of goalies played eight seasons or less.
</p>
<p>
<h5>Exploring Age</h5>
I scraped hockey-reference for each goalie's date of birth (code available here) in order to see how their performance changes as they age. Using goalie birthdays and dates of games, we can get the exact age of goalies for each of their games. I started the exploration grouping shots into bins by goalie age, rounded to the first decimal (ex: 26.0, 26.1, etc.), and then calculating the group-wide save percentage. I added alpha to the number of shots faced, so groups with few shots pale in comparison to groups with many shots. Here's what that looks like:
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-six-two.png" width="60%" length="150"/></div>
</p>
<p>
Some thoughts:
    - Most shots are taken on goalies aged 23-35.
    - If you squint, you can see a little bit of an age curve here.
    - This plot is riddled with bias (particularly for goalies with short or long careers).
</p>
<p>
Let's fix the bias above with a few changes. Instead of simply grouping shots by age, we'll follow a strategy <a href = "https://hockey-graphs.com/2017/03/23/a-new-look-at-aging-curves-for-nhl-skaters-part-1">seemingly</a> developed by Tango Tiger <a href = "http://www.tangotiger.net/aging.html">here</a> called the delta method. Here are the steps:
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
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-six-four.png" width="65%" length="165"/></div>
</p>
<p>
Some more thoughts:
    - Pretty well every goalie who faces less than 1500 shots ends his career with a pAdjSV% below average.
    - Goalies 
    - This disagrees with <a href="https://hockey-graphs.com/2014/03/21/how-well-do-goalies-age-a-look-at-a-goalie-aging-curve/">other</a> past research.
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-six-five.png" width="60%" length="150"/></div>
</p>
<p>
Code available here: <a href="https://github.com/spazznolo/goalie-consistency/blob/main/posts/post-6.R">https://github.com/spazznolo/goalie-consistency/blob/main/posts/post-6.R</a>
</p>