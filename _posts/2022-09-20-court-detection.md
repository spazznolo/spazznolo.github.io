---
layout: post
title:  "LIVEBLOG [Post 5] Court Detection"
date:   2022-09-19 12:52:05 -0400
---
<h2>LIVEBLOG [Post 5] Court Detection</h2>
<p>
Though I intended to develop a few simple models to compete with the VGG16, the initial results using transfer learning were satisfactory and I started getting caught up with Hough lines and corner detection algos. Each step is so new and different, I'm basically doing a literature review every time. During this search, I found a few existing court detection algorithms. I'll list them below along with a short summary. The end of the story is that none of them are fit for this exact problem and I'd prefer try my hand at a method which doesn't require much memory or runtime (familiar, I know).
</p>
<h5>Existing Court Detection Methods</h5>
<p>
<b>Tennis Court Detection</b>
Grzegorz Chlebus created a <a href="https://github.com/gchlebus/tennis-court-detection">repository</a> on GitHub for his tennis court detector. The method was adapted from Farin D. et al. "Robust Camera Calibration for Sports Videos using Court Models". It was created 4 years ago and apparently requires a bit of <a href="https://github.com/gchlebus/tennis-court-detection/issues/8">updating</a> in order to run, but unfortunately even with these updates I <a href="https://github.com/gchlebus/tennis-court-detection/issues/5">couldn't get it to work</a>. I can't confirm this, but apparently it can take up to 30 seconds to process one frame. This is hard to believe, but maybe the grid search works just takes that long. I'm going to need something fast than this.
</p>
<p>
<b>Robust Camera Calibration for Sports Videos using Court Models</b>
This is the paper, available <a href="https://www.researchgate.net/publication/220979520_Robust_camera_calibration_for_sport_videos_using_court_models">here</a>, that Chlebus adapted in the first method on the list. Notice the first word here is "robust", meaning the method was developed for various sports, some of which having dynamic camerawork where field vision is complex. This is a departure from the tennis broadcasts, who barely change camera perspectives at all during gameplay. In the paper, they mention how a fitted model is necessary in their method because the court lines are not always obvious (model flow chart below). From tracking a few games, this just doesn't ring true for tennis so far. I'm going to be a little greedy here and try to get away with a set of heuristics. 
</p>
<p>
<div style="text-align: center"> 
<img src="https://spazznolo.github.io/figs/robust-camera-model-flow.png" width="60%" length="150"/>
</div>
</p>