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
<b>Tennis Court Detection</b>
Grzegorz Chlebus created a <a href="https://github.com/gchlebus/tennis-court-detection">repository</a> on GitHub for his tennis court detector. The method was adapted from Farin D. et al. "Robust Camera Calibration for Sports Videos using Court Models". It was created 4 years ago and apparently requires a bit of updating in order to run, but unfortunately even with these updates I <a href="https://github.com/gchlebus/tennis-court-detection/issues/5">couldn't get it to work</a>.