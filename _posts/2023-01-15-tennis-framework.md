---
layout: post
title:  "Building a framework to track tennis games at scale"
date:   2023-01-15 12:00:00 -0400
---
<h2>Building a framework to track tennis games at scale</h2>
I stepped away from the first iteration of this project last year when I realized I was going to have to annotate thousands of images to create a robust player/ball detection model. In the next few months, I'll design and build such a modelling framework. This post outlines the methods and services which will be used for the framework.
<p>
<h5>Tennis TV</h5>
The ATP has a streaming service called Tennis TV which offers full games and daily highlights for most tournaments on the tour. The highlights are of particular interest given that they consist of condensed versions of various games. This offers a diversity of players, outfits, visibility, crowds, etc. which will make the model more robust.
</p>
<p>
To maximize the diversity of the labelled set, I downloaded the quarter-final highlight video of 15 tournaments. Each video contains highlights from four games and is roughly 8 minutes long, which at 25fps is 12,000 frames, or 3,000 frames per game. I clipped each minute of each video, then took every fifth frame, up to 25 frames per minute. This is roughly 200 frames per tournament (or 50 frames per game), for 3000 frames in total. A highlight video consists of roughly 65-70% of actual game-play, with the other 30-35% being replays, audience pans, etc. Therefore, the final modelling set is roughly 2000 frames. 
</p>
<p>
<h5>Roboflow</h5>
Using Roboflow, I labelled the front player, back player, and tennis ball for each frame that featured them. Roboflow is free, slick, and saved me hours of labelling work through it's label assist feature. Basically, I annotated a couple of games manually, trained a model on these games, then loaded the model into the label assist feature to automate much of the annotation process for the remaining games. 
</p>
<p>
Roboflow also has an API that plugs easily into Google Colab.
</p>
<p>
<h5>Google Colab</h5>
I'm currently using Google Colab to train the computer vision model. I've looked around, and for my current needs (research), it fits. Easy to use, compatible with Roboflow, offers a free-to-use GPU (though it disconnects with 90 minutes of inactivity). I'm currently using Google Colab to train a YOLOv5 model.
</p>
<p>
<h5>YOLOv5</h5>
The object detection model I chose to start is YOLOv5. It's incredibly fast. Inference is around 100fps, which makes it scalable when it comes time to track an entire tournament of gameplay. It works fine for players, but it doesn't leverage the spatio-temporal nature of tennis. This is particularly problematic when detecting a tennis ball, which, depending on the context, can appear as a blurred line, blend in with the court lines, be hidden behind a player, etc.
</p>
<p>
Some results:
overall: 
front-player: 
back-player:
tennis-ball:
</p>
<p>
<h5>Video Example</h5>
Here's an example of the inference: <a href = "https://www.youtube.com/watch?v=DwdfFsjQgFg">https://www.youtube.com/watch?v=DwdfFsjQgFg</a>
</p>
<p>
<h5>Game-State Classification</h5>
Because of the labelling framework, where players are only labelled when the camera is in 'gameplay' mode (long static shot of the court with a player in front of the net and another behind it), the player detection model fails to detect players in other shots like replay or time-outs or even commercials. This allows for an indirect game-state classification strategy - whenever players aren't detected, it is assumed to be non-gameplay. A post will be dedicated on refining this. 
</p>
<p>
<h5>Detecting Court Lines</h5>
Currently still using the Hough Lines method laid out in a previous post. Ideally, this could be replaced with some sort of polygon detection algorithm which detects the outer lines of the court based on the patterns inside of it, but this hasn't been explored yet.
</p>
<p>
<h5>Post-Processing of Tennis Players</h5>
to be continued
</p>
<p>
<h5>Post-Processing of Tennis Ball</h5>
to be continued
</p>

