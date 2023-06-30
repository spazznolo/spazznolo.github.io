---
layout: post
title:  "Goalie Performance: Adjusting for Age"
date:   2023-07-05 12:00:00 -0400
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
<h2>[Post 3] Goalie Performance: Adjusting for Age</h2>
<p>
In the <a href="https://spazznolo.github.io/2023/05/17/goalie-performance-1.html">first post</a>, I outlined a framework to measure goalie performance using their career Fenwick 5v5 save percentage. In the <a href="https://spazznolo.github.io/2023/05/22/goalie-performance-2.html">second post</a>, I refined the methodology to consider shot quality. The outstanding assumptions are included below.
</p>
<p>
Assumptions:
    - <b>Age is assumed to be irrelevant.</b>
    - The prior distribution is assumed to be beta with hyperparameters 852 and 55.6.
    - Goalies facing less than 200 shots are ignored.
    - Goalie careers are equal.
    - Scoring rates are assumed to be constant.
    - Team systems are assumed to be identical.
</p>
<p>
In this post, I'm going to address the effect of age on goalie performance.
</p>
<p>
<h5>Outline</h5>
Like shot quality, the effect of age on performance is a well-researched concept. It has been shown that goalies tend to improve as they age, peak, and then recede for, well, forever. This concept is typically called an <em>age curve</em>. Though goalie age curves are already available elsewhere, they differ slightly, so I'm going to define a custom age curve based on the Moneypuck dataset. Here are the steps:
    - Obtain goalie birth dates.
    - Derive goalie age for each game.
    - Define new analysis population (we won't find every goalie's date of birth).
    - Explore age.
    - Adjust for age.
</p>
<h5>Obtain goalie birth dates</h5>
I scraped hockey-reference for each goalie's date of birth (code available <a href="https://github.com/spazznolo/goalie-consistency/blob/main/import/scrape_goalie_data.R">here</a>). By combining the goalies' birth dates with the dates of each of their games, I determined their exact age for every game played.
</p>
<p>
<h5>Define new analysis population</h5>
The analysis population changes as follows (due to incomplete linkage):
    - Goalie population drops from 315 to 308.
    - Harmonic mean of shots against rises from 12,690 to 12,721 (mean rises, 4,198 to 4,286).
    - Harmonic mean of AdjSV% stays at .939 (mean rises, .932 to .933).
</p>
<p>
They barely differ.
</p>
<p>
<h5>Explore age</h5>
Let's start by simply grouping shots into bins by goalie age (rounded to the first decimal, ex: 26.0, 26.1, etc.), and then calculating the group-wide save percentage. Here's what that looks like, with points becoming paler as the group size decreases:
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
Let's fix some of the bias above with a few changes. We'll follow a well-worn strategy <a href = "https://hockey-graphs.com/2017/03/23/a-new-look-at-aging-curves-for-nhl-skaters-part-1">seemingly</a> developed by Tango Tiger <a href = "http://www.tangotiger.net/aging.html">here</a> called the delta method. Here are the steps:
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
    - There is well documented survivorship bias.
</p>
<p>
INCLUDE PHANTOM YEARS HERE
</p>
<p>
<h5>Adjusting for Age</h5>
The cleanest way that I can think of adjusting for age is to bake it into the current framework which already adjusts shots by their probability of becoming a goal. This can easily by done by first setting the peak (age 27) as the standard and then adjusting for all other ages, so that, for example, an xFSV% of 0.940 at age 27 is equivalent to an xFSV% of 0.93882 at age 23 (0.94000 - 0.00118) and an xFSV% of 0.93487 at age 38 (0.94000 - 0.00513).
</p>
<p>
    - Adjusted (xG) Save Percentage (AdjSV%) = MSV% + (FSV% - xFSV%)
    - Age Curve Adjustement (acAdj) = f(age), where f is the smoothed curve in the plot above.
    - <b>Adjusted (Age + xG) Save Percentage (AdjSV%) = MSV% + (FSV% - xFSV% + acAdj)</b>
</p>
<p>
COMPARE TWO GOALIES WITH DIFFERING AGES
</p>
<p>
Code available here: <a href="https://github.com/spazznolo/goalie-performance/blob/main/posts/post-3.R">https://github.com/spazznolo/goalie-performance/blob/main/posts/post-3.R</a>
</p>