---
layout: post
title:  "LIVEBLOG [Post 3] Building the Model Set"
date:   2022-09-18 12:52:05 -0400
---
<h2>LIVEBLOG [Post 3] Building the Model Set</h2>
<p>
Quick post on how the modelling set will be built. I'm looking for diversity of game time, court, years and gender, with a testing set that features games not in the training or validation sets. I've decided on randomly sampling 10 random 60 seconds chunks from 12 matches. That's a total of 120 minutes, or, at 1,600 frames a minute, 192,000 frames. The good news is that gameplay, like off-time, is sequential. It won't be as daunting as it might sound. After doing 10 minutes of the Williams sisters Australian Open final in 2003, it looks like I'm averaging 3 minutes of labelling per 1 minute of broadcast time. Extrapolating, it will probably take around 6 hours to get the modelling set I'd like to start with.
</p>
<h5>Games I've chosen to track.</h5>
2003 Australian Open W-F (hard court)