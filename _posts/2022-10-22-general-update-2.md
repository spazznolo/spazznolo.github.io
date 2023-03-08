---
layout: post
title:  "Object Detection Framework"
date:   2023-03-08 12:00:00 -0400
---
<h2>Object Detection Framework</h2>
<p>
I stepped away from the project when I realized I was going to have to anotate thousands of images to create a robust player/ball detection model. In the past few months, I decided to build a framework for such a model to be scalable. This post outlines the methods and services used for the framework.
</p>
<p>
TENNIS TV
The ATP has a streaming service called Tennis TV which offers full games and daily highlights for most tournaments on the tour. The highlights are of particular interest given that they consist of condensed versions of various games. This offers a diversity of: players, outfits, visibility, crowds, etc. 
</p>
<p>
To maximize the diversity of the labelled set, I downloaded the quarter-final highlight video of 15 tournaments. Each video is roughly 8 minutes long, which at 25fps is 12,000 frames. Unnecessary. I clipped each minute of each video, then took every fifth frame, up to 25 frames per minute. This is roughly 200 frames per tournament, 3000 frames in total.
</p>
<p>
ROBOFLOW
Using Roboflow, I labelled the front player, back player, and tennis ball for each frame that featured them. Roboflow is free, slick, and saved me hours of labelling work through it's label assist feature. Roboflow also has an API that plugs easily into Google Colab.
</p>
<p>
GOOGLE COLAB
I'm currently using Google Colab to train the computer vision model. I've looked around, and for my current needs (research), it fits. Easy to use, compatible with Roboflow, offers a free-to-use GPU (though it disconnects with inactivity). 
</p>
<p>
YOLOv5
The object detection model I chose to start is YOLOv5. It's incredibly fast. Inference is around 100fps, which makes it scalable when it comes time to run inference on an entire tournament of gameplay. It works fine for players, but I it doesn't include past positions in it's inference of a current position. This is particularly problematic when detecting a tennis ball, which, depending on the context, can appear as a blurred line, blend in with the court lines, be hidden behind a player.

Some results:
front-player: 
back-player:
tennis-ball:
</p>
<p>
GAME-STATE CLASSIFICATION
adsfa
</p>
<p>
DETECTING COURT LINES
adf
</p>
<p>
POST-PROCESSING OF TENNIS PLAYERS
adf
</p>
<p>
POST-PROCESSING OF TENNIS BALL
adf
</p>

