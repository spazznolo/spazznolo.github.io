---
layout: post
title:  "Post-regulation: Is the overtime random after each shot?"
date:   2022-04-30 8:52:05 -0400
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
<h2>[Post 3] Is the overtime random after each shot?</h2>
<p>
To measure this, <em>we'll regress various team and game characteristics, including who had the last shot, on the outcome of individual games which ended in overtime</em>. Specifically, the predictors will be: a team's xGF% throughout their season, game and overtime (before the winning goal was scored), and whether they had the last shot before the winning goal was scored. Think of the non-shot predictors as controls. A few examples of what an observation looks like:
</p>
<p>
<div style="text-align: center"> 
<img src="https://spazznolo.github.io/figs/post-regulation-three-one.png" width="60%" length="150"/>
</div>
</p>
<p>
Using every game that ended in overtime since its inception in 2015, the regression can be summarized like this:
</p>
<p>
<div style="text-align: center"> 
<img src="https://spazznolo.github.io/figs/post-regulation-three-two.png" width="30%" length="75"/>
</div>
</p>
<h5>
Model Translation:
</h5>
Having the last shot matters - it adds about 13.8% to a team's win probability (63.8%).
<p>
The only other relevant predictor is a team's xGF% in the overtime before the goal was scored. It's a distant second though: a 10% increase in xGF% adds about 1.9% to the team's win probability. This means that if a team dominates overtime with 75% of Expected Goals, its probability of winning only increases 4.7% (54.7%). 
</p>
<p>
A team's xGF% in the regular season and in a given game's regulation did not factor.
</p>
<h5>
Are all shots equal, though?
</h5>
<p>
In this model, all shots were considered equal. Given that the last shot before the goal is the most important factor in the outcome of an overtime, we shouldn't just treat them equally, however. Some questions: Do all shots lead to a higher chance in winning? Can we include games that did not end in the overtime to make the analysis more robust? Doesn't every shot matter, and not just the last ones?
</p>
<p>
In the next post, we'll build a win probability model based on each given shot's characteristics.
</p>



