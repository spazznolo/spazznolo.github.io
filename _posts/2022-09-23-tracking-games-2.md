---
layout: post
title:  "LIVEBLOG 008: Tracking Games [Part 2]"
date:   2022-09-23 12:52:05 -0400
---
<h2>LIVEBLOG 008: Tracking Games [Part 2]</h2>
<p>
I tracked all the clay and grass games yesterday. That's 80 minutes of broadcast time. It took two hours in total. Tracking at 1.5x realtime is twice as fast as I did in my test runs with the Williams final, which is encouraging. 
</p>
<p>
The set of heuristics for the court detection strategy is coming together. It's starting to look like a sophisticated model won't be necessary. I have to test it, of course, but I've been greedy and taken random frames from games to see how the initial attempt holds up and it's doing well. One idea is to get all Hough lines, block filter on a few conditions, and then train a logistic regression on the length-wise lines. 
</p>