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
The set of heuristics for the court detection strategy is coming together. It's starting to look like a sophisticated model won't be necessary. I have to test it, of course, but I've been greedy and taken random game frames to see how the initial attempt holds up and it's doing well. One idea is to get all Hough lines, block filter on a few conditions, and then train a logistic regression on the length-wise lines. 
</p>
<p>
It dawned on me today that hard court games are much easier to predict on because the synthetic court has less imperfections. It's possible the courts are different enough that they could use their own models. As the project moves on, I'm having to make concessions, which is natural, and one major concession might be to limit the project to hard courts as a first step. The US and Austalian Opens are both on hard court and both have great video quality.
</p>