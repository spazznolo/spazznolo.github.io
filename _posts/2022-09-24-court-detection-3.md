---
layout: post
title:  "LIVEBLOG 009: Court Detection [Part 3]"
date:   2022-09-24 12:00:00 -0400
---
<h2>LIVEBLOG 009: Court Detection [Part 3]</h2>
<p>
Tracked the last of the 12 games this morning. Realized I hadn't thought of a proper pipeline from tracking to training, and paid for it in time and monotony, but it's finished. Next is to take random samples of the frames labelled as gameplay and plotting the first iteration of the Hough line method which I'll outline again below.
</p>
<p>
The most challenging part of the court detection strategy so far has been data wrangling. Python isn't my first language and the OpenCV objects-to-pandas pipeline is a little... weird. Anyways, that's to say that the strategy is exceedingly simple and the first version should be finished by the end of this weekend. It'll definitely need refinement, but I have ideas on how to improve it, so it isn't a worry. 
</p>
<p>
As a reminder:
</p>
<p>
<b>Jeremie's set of heuristics for court detection</b>
1. Detect Hough lines 
2. Identify the lengthwise court lines (doubles and singles borders) by filtering Hough lines having:
    a. absolute slope between 1.5 and 3.
    b. length over 200 pixels.
3. Identify widthwise court lines by filtering the Hough lines having:
    a. y-coordinates either between the minimum or maximum y-coordinates of the lengthwise lines (+/- 10 pixels)
    b. x-coordinates between the minimum and maximum x-coordinates lengthwise lines (+/- 10 pixels)
</p>
<p>
<b>Results (Iteration 1)</b>
<p>
<div style="text-align: center"> 
<img src="https://spazznolo.github.io/figs/hough-line-ex-2.jpg" width="60%" length="150"/>
</div>
</p>