---
layout: post
title:  "LIVEBLOG [Post 5] Court Detection"
date:   2022-09-19 12:52:05 -0400
---
<h2>LIVEBLOG [Post 5] Court Detection</h2>
<p>
Though I intended to develop a few simple models to compete with the VGG16 on the game-state predictions, the initial results were satisfactory and I started getting caught up with Hough lines and corner detection algos anyways so I figured I'd start a post on court detection. Each step is so new and different, I'm basically doing a literature review every time. I found a few existing court detection algorithms, which I'll summarize below. The end of the story is that none of them are fit for this exact problem and I'd prefer try my hand at a method which doesn't require much memory or runtime (familiar, I know).
</p>
<h5>Existing Court Detection Methods</h5>
<p>
<b>Tennis Court Detection</b>
Grzegorz Chlebus created a <a href="https://github.com/gchlebus/tennis-court-detection">repository</a> on GitHub for his tennis court detector. The method was adapted from Farin D. et al. "Robust Camera Calibration for Sports Videos using Court Models". It was created 4 years ago and apparently requires a bit of <a href="https://github.com/gchlebus/tennis-court-detection/issues/8">updating</a> in order to run, but unfortunately even with these updates I <a href="https://github.com/gchlebus/tennis-court-detection/issues/5">couldn't get it to work</a>. I can't confirm this, but apparently it can take up to 30 seconds to process one frame. This is hard to believe, but maybe the grid search just takes that long. I'm going to need something faster than this.
</p>
<p>
<b>Robust Camera Calibration for Sports Videos using Court Models</b>
This is the paper that Chlebus adapted in the first method on the list. The paper is available in full <a href="https://www.researchgate.net/publication/220979520_Robust_camera_calibration_for_sport_videos_using_court_models">here</a>. Notice the first word in the title is "robust", meaning the method was developed for various sports, some of which having dynamic camerawork where field vision is complex. This is a departure from the tennis broadcasts where camera perspectives barely change at all during gameplay. In the paper, they mention how a fitted model is necessary in their method because the court lines are not always obvious (model flow chart below). From tracking a few games, this just doesn't ring true for tennis so far. I'm going to be a little greedy here and try to get away with a set of heuristics based on the output from the hough line algo on openCV (memory, speed). 
</p>
<p>
<div style="text-align: center"> 
<img src="https://spazznolo.github.io/figs/robust-camera-model-flow.png" width="60%" length="150"/>
</div>
</p>
<p>
<b>Ben's Iterative Approach using RANSAC</b>
Ben, a user on Stack Overflow, suggested a possible solution for a <a href="https://stackoverflow.com/questions/24135289/python-opencv-detect-lines-in-a-tennis-court-using-two-differents-methods-of-h">similar problem</a>. This solution actually seems pretty close to the previous robust approach, except it's more lightweight. I'm probably going to try to implement Ben's suggestion simply because I want to try my hand at the RANSAC, which I've never used before. However, I <i>still</i> feel like the remarkable simplicity of the camerawork in tennis is not being fully leveraged here.
</p>
<p>
<b>Jeremie's Ricketty Approach</b>
From drawing hough lines on a variety of gameplay frames, the thing that strikes me most are the four lines which make up the length of the court. The two on the outside are for doubles and the two on the inside are for singles. Here we have two sets of lines which have roughly the same length and slope when captured on the broadcast. I'm going to randomly select 20 frames which feature gameplay and plot all the discovered hough lines in red except for those with absolute slope between 1.5 and 3 which I'll plot in green.
</p>
<p>
<div style="text-align: center"> 
<img src="https://spazznolo.github.io/figs/hough-line-ex.png" width="60%" length="150"/>
</div>
</p>
<p>
<div style="text-align: center"> 
<img src="https://spazznolo.github.io/figs/hough-line-ex-2.jpg" width="60%" length="150"/>
</div>
</p>