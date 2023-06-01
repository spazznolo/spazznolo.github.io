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
    - The number of shots faced is assumed to be independent from performance.
    - Scoring rates are assumed to be constant.
    - All shots are assumed to be equal. 
    - Team systems are assumed to be identical.
</p>
<p>
I'm going to address the second and third points in this post, but in a sidewinding sort of way. 
</p>
<p>
<h5>Exploring Experience</h5>
Let's start the exploration by defining our population. There aren't many NHL goalie careers, so we need to be greedy and take as many as we can for the analysis at hand. When we talk about experience, we're referencing the number of shots faced. We don't know how many shots a goalie faced before 2007, so any goalie playing before then has to be removed. The converse is true for the 2022-2023 season. 

Here's a short summary of the experience dataset:
    - Goalie population drops from 318 to 130.
    - Average career shots faced drops from 4,198 to 3,225.
    - AdjSV% drops from .937 to .927
</p>
<p>
I wanted to start by sharing an interesting (though probably intuitive) finding. Below is the cumulative distribution function for goalie career seasons played.
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
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-six-four.png" width="65%" length="165"/></div>
</p>
<p>
Some thoughts:
    - Nearly every goalie [give %] who faces -6000 shots ends his career with a pAdjSV% below average.
    - Goalies facing 1500+ but -6000 seem to regress towards league average pAdjSV%.
    - These goalies tend to be backups, facing ~600-1000 shots a season.
    - This regression to league average could partly be due to aging effects.
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-six-five.png" width="65%" length="165"/></div>
</p>
An important dimension is missing in the above data which could partially explain the unintuitive result where goalies who face < 5000 shots take a significant early lead in pAdjSV% over goalies who face 5000+ shots - age. Let's plot the average age of goalies in each group as they face shots over their career.
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-six-six.png" width="65%" length="165"/></div>
</p>
<p>
Some thoughts:
    - Goalies who face -5000 shots are about 1.5 years older throughout their career.
    - This difference obviously includes the span from age 23 to roughly 27.
    - This is precisely the age range in which goalies seem to be improving in AdjSV%.
    - We need to adjust for this.
</p>
<p>
<h5>Exploring Age</h5>
<p>
I scraped hockey-reference for each goalie's date of birth (code available <a href="https://github.com/spazznolo/goalie-consistency/blob/main/import/scrape_goalie_data.R">here</a>) in order to see how their performance changes as they age. Using goalies' dates of birth with dates of games, we can get the exact age of a goaltender for each of their games. A few goalies were not linked. Our analysis population changes as follows:
    - Goalie population drops from 318 to 311.
    - Average career shots faced drops from 4,198 to 3,225.
    - AdjSV% drops from .937 to .927
</p>
<p>
Let's start by simply grouping shots into bins by goalie age, rounded to the first decimal (ex: 26.0, 26.1, etc.), and then calculating the group-wide save percentage. Points belonging to groups with fewer shots pale in comparison to groups with many shots. Here's what that looks like:
</p>
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
</p>
<p>
<h5>Adjusting for Age</h5>
adfadfasdf
</p>
<p>
adfadf
</p>
<p>
Code available here: <a href="https://github.com/spazznolo/goalie-consistency/blob/main/posts/post-6.R">https://github.com/spazznolo/goalie-consistency/blob/main/posts/post-6.R</a>
</p>