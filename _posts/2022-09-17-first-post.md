---
layout: post
title:  "LIVEBLOG [Post 1] Hello, tennis"
date:   2022-09-17 10:52:05 -0400
---
<h2>LIVEBLOG [Post 1] Hello, tennis</h2>
<p>
The other day I was at a bar and the US Open was on. I don't particularly watch much pro tennis, so I was surprised by the clean camerawork. It's very elegant. During gameplay, the camera is static on a lengthwise shot which captures the entire court, it only moves slightly when the ball is hit wide and then goes right back to that symmetric static shot. I figured tennis analytics must be booming ahead of other sports because of this, so I searched for what people have come up with and found... <a href="https://hdsr.mitpress.mit.edu/pub/uy0zl4i1/release/4">this</a>. Basically, the author, a <a href="http://on-the-t.com/">tennis researcher</a>, lists all the reasons why tennis is decidedly NOT booming, and actually lagging all other major sports. 
</p>
<p>
I've made a career out of statistical analysis and the implementation of traditional machine learning alogrithms, but recently I've been thinking of messing around with computer vision. I tend to learn best by trying (and failing, and failing) to apply a new subject to a real-world problem I'm interested in.
</p>
<p>
Hello, tennis.
</p>
<p>
I'm going to use this blog as a place to sporadically dump my thoughts and progress, starting with my ultimate goal for the project. The goal, by the way, is to build a program which takes in the full video broadcast of a tennis match and pushes out an account of the game in tabular format. Each row of the output would be a unique frame of the video, with the location of both players and the ball during the frame, along with categorical variables for: ball bounce (yes or no), swing type (serve, backhand, forehand, overhead).
</p>

