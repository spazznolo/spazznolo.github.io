---
layout: post
title:  "Object Detection Framework"
date:   2023-03-08 12:00:00 -0400
---
<h2>Object Detection Framework</h2>
<p>
I stepped away from the project last year when I realized I was going to have to annotate thousands of images to create a robust player/ball detection model. In the past few months, I decided to map and build such a modelling framework. This post outlines the methods and services used for the framework.
</p>
<p>
TENNIS TV
The ATP has a streaming service called Tennis TV which offers full games and daily highlights for most tournaments on the tour. The highlights are of particular interest given that they consist of condensed versions of various games. This offers a diversity of players, outfits, visibility, crowds, etc. which will make the model more robust.
</p>
<p>
To maximize the diversity of the labelled set, I downloaded the quarter-final highlight video of 15 tournaments. Each video contains highlights from four games and is roughly 8 minutes long, which at 25fps is 12,000 frames, or 3,000 frames per game. I clipped each minute of each video, then took every fifth frame, up to 25 frames per minute. This is roughly 200 frames per tournament (or 50 frames per game), for 3000 frames in total. A highlight video consists of roughly 65-70% of actual game-play, with the other 30-35% being replays, audience pans, etc. Therefore, the final modelling set is roughly 2000 frames. 
</p>
<p>
ROBOFLOW
Using Roboflow, I labelled the front player, back player, and tennis ball for each frame that featured them. Roboflow is free, slick, and saved me hours of labelling work through it's label assist feature. Basically, I annotated a couple of games manually, trained a model on these games, then loaded the model into the label assist feature to automate much of the annotation process for the remaining games. 
</p>
<p>
Roboflow also has an API that plugs easily into Google Colab.
</p>
<p>
GOOGLE COLAB
I'm currently using Google Colab to train the computer vision model. I've looked around, and for my current needs (research), it fits. Easy to use, compatible with Roboflow, offers a free-to-use GPU (though it disconnects with 90 minutes of inactivity). I'm currently using Google Colab to train a YOLOv5 model.
</p>
<p>
YOLOv5
The object detection model I chose to start is YOLOv5. It's incredibly fast. Inference is around 100fps, which makes it scalable when it comes time to track an entire tournament of gameplay. It works fine for players, but it doesn't leverage the spatio-temporal nature of tennis. This is particularly problematic when detecting a tennis ball, which, depending on the context, can appear as a blurred line, blend in with the court lines, be hidden behind a player, etc.

Some results:
overall: 91.0% mAP; 95.9% precision; 90.6% recall
front-player: 99.2% mAP; 99.6% precision; 99.1% recall
back-player:
tennis-ball:
</p>
<p>
VIDEO EXAMPLE
Here's an example of the inference: https://www.youtube.com/watch?v=DwdfFsjQgFg
</p>
<p>
GAME-STATE CLASSIFICATION
Because of the labelling framework, where players are only labelled when the camera is in 'gameplay' mode (long static shot of the court with a player in front of the net and another behind it), the player detection model fails to detect players in other shots like replay or time-outs or even commercials. This allows for an indirect game-state classification strategy - whenever players aren't detected, it is assumed to be non-gameplay. A post will be dedicated on refining this. 
</p>
<p>
DETECTING COURT LINES
Currently still using the Hough Lines method laid out in a previous post. Ideally, this could be replaced with some sort of polygon detection algorithm which detects the outer lines of the court based on the patterns inside of it, but this hasn't been explored yet.
</p>
<p>
POST-PROCESSING OF TENNIS PLAYERS
adf
</p>
<p>
POST-PROCESSING OF TENNIS BALL
adf
</p>

