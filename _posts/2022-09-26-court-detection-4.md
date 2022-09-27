---
layout: post
title:  "LIVEBLOG 009: Court Detection 04"
date:   2022-09-26 12:00:00 -0400
---
<h2>LIVEBLOG 010: Court Detection 04</h2>
<p>
Spent today thinking up an iterative approach at finding the lines which make up the boundary of the court. Somewhat begrudgingly, I've turned to clustering the Hough lines which pass the initial block filter (absolute slope between 1 and 3). It's a univariate hierarchical clustering strategy using lines' absolute slope, followed by a filtering of all lines which are part of the two largest clusters, then taking the minimum median absolute slope from these two largest groups (usually the largest median absolute slope is the inner lengthwise lines and the smallest is the outter lines).
</p>
<p>
Also! To remind myself: the camera is mostly static. This means there should be a quick, efficient check to see if it has moved from the previous frame. Off the top of my head, I can run the Hough line algo each frame and if the lengthwise lines are nearly identical then keep the same coordinate system and move to the next frame.
</p>
