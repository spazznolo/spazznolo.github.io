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
I'm going to address the second point in this post, but before I do, I wanted to share an interesting (though probably intuitive) finding. Below is the cumulative distribution function for seasons played by goalies. It shows that less than 50% of goalies who have played an NHL game end up playing over 3 seasons.
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/goalie-six-one.png" width="60%" length="150"/></div>
</p>
<p>
Summary of findings:
    - Over 25% of goalies play only one season.
    - Over 50% of goalies play three seasons or less.
    - Over 75% of goalies play seven seasons or less.
</p>
<p>
Code available here: <a href="https://github.com/spazznolo/goalie-consistency/blob/main/post_6.R">https://github.com/spazznolo/goalie-consistency/blob/main/post_6.R</a>
</p>