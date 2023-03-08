---
layout: post
title:  "Object Detection Framework"
date:   2023-03-08 12:00:00 -0400
---
<h2>Object Detection Framework</h2>
<p>
I stepped away from the project when I realized I was going to have to anotate thousands of images to create a robust player/ball detection model. In the past few months, I decided to build a framework for such a model to be scalable. This post outlines the methods and services used for the framework.

1. VIDEO OF GAMEPLAY
The ATP has a streaming service called Tennis TV which offers full games and daily highlights for most tournaments on the tour. The highlights are of particular interest given that they consist of condensed versions of various games. This offers a diversity of: players, outfits, visibility, crowds, etc. 

To maximize the diversity of the labelled set, I downloaded the quarter-final highlight video of 15 tournaments. Each video is roughly 8 minutes long, which at 25fps is 12,000 frames. Unnecessary. I clipped each minute of each video, then took every fifth frame, up to 25 frames per minute. This is roughly 200 frames per tournament, and so 3000 frames in total.

I labelled the front player, back player, and tennis ball for each frame that featured them.

2. 
</p>
