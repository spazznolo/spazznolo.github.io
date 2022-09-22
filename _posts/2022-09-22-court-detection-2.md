---
layout: post
title:  "LIVEBLOG 007: Court Detection [Part 2]"
date:   2022-09-22 12:52:05 -0400
---
<h2>LIVEBLOG 007: Court Detection [Part 2]</h2>
<p>
In the last Court Detection post, I wrote vaguely about detecting the tennis court using a set of heuristics based on Hough lines. I'm going to expand on it here, introduce the first iteration of this approach, and visualize the outcome on 25 randomly selected frames featuring gameplay (this part will only be updated once I've tracked the 12 games).
</p>
<p>
<b>Jeremie's set of heuristics for court detection</b>
1. Find the Hough lines 
2. Identify the lengthwise court lines (doubles and singles borders) by filtering Hough lines having:
    a. absolute slope between 1.5 and 3.
    b. length over 200 pixels.
3. Identify widthwise court lines by filtering the Hough lines having:
    a. y-coordinates between the minimum and maximum y-coordinates lengthwise lines (+/- 10 pixels)
    b. x-coordinates equal to or between the minimum and maximum x-coordinates lengthwise lines (+/- 5 pixels)
</p>
<p>
<div style="text-align: center"> 
<img src="https://spazznolo.github.io/figs/hough-line-ex-2.jpg" width="60%" length="150"/>
</div>
</p>