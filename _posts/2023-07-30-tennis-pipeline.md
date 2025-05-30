---
layout: post
title:  "Tennis: Tracking Pipeline"
date:   2024-07-30 12:00:00 -0400
---
<head>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-DGRHZS5DNM"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-DGRHZS5DNM');
</script>
</head>
<h2>Tracking Pipeline</h2>
<p>
broadcast video of tennis game ->
object detection (YOLOv5) ->
instance segmentation (YOLOv5 instance-seg) ->
perspective transform 

object detection (YOLOv5) ->
post-processing of objects ->
event prediction (bounces, hits) ->

instance segmentation (YOLOv5 instance-seg) ->
simplify polygon ->
detect corners

scrape scores from tennis24 ->
get point-by-point results + player info ->
join point-by-point results + player info

outstanding questions
how to ensure events are coherent?
how to ensure points correspond?


<p>
I stepped away from the first iteration of this project last year when I realized I was going to have to annotate thousands of images to create a robust player/ball detection model. In the next few months, I'll design and build such a modelling framework. This post outlines the methods and services which will be used for the framework.
</p>
<p>
<h5>Tennis TV</h5>
The ATP has a streaming service called <a href="https://www.tennistv.com/?gclid=CjwKCAjwyqWkBhBMEiwAp2yUFkALa-AHHRpKvKlqI7MypdHnL6eRs95eB9c-PsMZ3Oo81Niyo5yRRhoC1QIQAvD_BwE">Tennis TV</a> which offers full games and daily highlights for most tournaments on the tour. The highlights are of particular interest given that they consist of condensed versions of various games. This offers a diversity of players, outfits, visibility, crowds, etc. which will make the model more robust.
</p>
<p>
To maximize the diversity of the labelled set, I downloaded the quarter-final highlight video of 15 tournaments. Each video contains highlights from four games and is roughly 8 minutes long, which at 25fps is 12,000 frames, or 3,000 frames per game. I clipped each minute of each video, then took every fifth frame, up to 25 frames per minute. This is roughly 200 frames per tournament (or 50 frames per game), for 3000 frames in total. A highlight video consists of roughly 65-70% of actual game-play, with the other 30-35% being replays, audience pans, etc. Therefore, the final modelling set is roughly 2000 frames. 
</p>
<p>
<h5>Roboflow</h5>
Using <a href="https://app.roboflow.com/tennistracker-dogbm">Roboflow</a>, I labelled the front player, back player, and tennis ball for each frame that featured them. Roboflow is free, slick, and saved me hours of labelling work through it's label assist feature. Basically, I annotated a couple of games manually, trained a model on these games, then loaded the model into the label assist feature to automate much of the annotation process for the remaining games.  The dataset is <a href="https://universe.roboflow.com/tennistracker-dogbm/tennis-tracker-duufq">publicly available</a>.
</p>
<p>
Roboflow also has an API that plugs easily into Google Colab.
</p>
<p>
<h5>Google Colab</h5>
I'm currently using <a href="https://colab.research.google.com/drive/1tM9Jbu3XwlDK8s8EVLB_lBQwNOr23u-3#scrollTo=G4fjA5X74FpF">Google Colab</a> to train the computer vision model. I've looked around, and for my current needs (research), it fits. Easy to use, compatible with Roboflow, offers a free-to-use GPU (though it disconnects with 90 minutes of inactivity). I'm using it to train a high-speed, "You Only Look Once" objection detection model.
</p>
<p>
<h5>YOLOv5</h5>
The object detection model I chose to start is <a href="https://pytorch.org/hub/ultralytics_yolov5/">YOLOv5</a>. It's incredibly fast. Inference is around 100fps, which makes it scalable when it comes time to track an entire tournament of gameplay. It works fine for players, but it doesn't leverage the spatio-temporal nature of tennis. This is particularly problematic when detecting a tennis ball, which, depending on the context, can appear as a blurred line, blend in with the court lines, be hidden behind a player, etc.
</p>
<p>
Some results from the <a href="https://app.roboflow.com/tennistracker-dogbm/tennis-tracker-duufq/deploy/15">latest</a> model iteration.
overall:      91.0% P, 85.5% R, 85.8 mAP50
front-player: 99.5% P, 99.6% R, 99.5 mAP50
back-player:  99.5% P, 99.4% R, 99.3 mAP50
tennis-ball:  74.1% P, 57.0% R, 58.7 mAP50
</p>
<p>
<h5>Video Example</h5>
For a short example of the inference, click <a href = "https://www.youtube.com/watch?v=DwdfFsjQgFg">here.</a>
</p>
<p>
<h5>Game-State Classification</h5>
Because of the labelling framework, where players are only labelled when the camera is in 'gameplay' mode (long static shot of the court with a player in front of the net and another behind it), the player detection model fails to detect players in other shots like commercials or time-outs or even replays. This allows for an indirect game-state classification strategy - whenever players aren't detected, it is assumed to be non-gameplay. A post will be dedicated on refining this. 
</p>
<p>
<h5>Detecting Court Lines</h5>
Currently still using the Hough Lines method laid out in a previous post. Ths might be replaced with YOLOv5's instance segmentation model, where the court is identified with a bounding box but the polygon is saved.
</p>
<p>
<h5>Post-Processing of Tennis Players</h5>
The model performs strongly, so a simple imputation strategy using interpolation has worked so far. I'll dedicate a post to this.
</p>
<p>
<h5>Post-Processing of Tennis Ball</h5>
to be continued
</p>

