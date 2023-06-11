---
layout: page
title: / tennis
permalink: /tennis/
---
<h2>[2022-09-16] LIVEBLOG 001: Hello, tennis</h2>
<p>
The other day I was at a bar and the US Open was on. I don't particularly watch much pro tennis, so I was surprised by the clean camerawork. It's very elegant. During gameplay, the camera is static on a lengthwise shot which captures the entire court. It only moves slightly when the ball is hit wide and then goes right back to that symmetric static shot. I figured tennis analytics must be booming ahead of other sports because of this, so I searched for what people have come up with and found... <a href="https://hdsr.mitpress.mit.edu/pub/uy0zl4i1/release/4">this</a>, where the author, a <a href="http://on-the-t.com/">tennis researcher</a>, lists all the reasons why tennis is decidedly NOT booming, and actually lagging all other major sports. 
</p>
<p>
<div style="text-align: center"> 
<img src="https://spazznolo.github.io/figs/frame_1173.jpg" width="60%" length="150"/>
</div>
</p>
<p>
I've made a career out of statistical analysis and the implementation of traditional machine learning alogrithms, but recently I've been thinking of messing around with computer vision. I tend to learn best by trying (and failing and failing) to apply a new subject to a real-world problem I'm interested in.
</p>
<p>
Hello, tennis.
</p>
<p>
I'm going to use this blog as a place to sporadically dump my thoughts and progress on the project. The goal, by the way, is to build a program which takes in the full video broadcast of a tennis match and pushes out an account of the game in tabular format. Each row of the output would be a unique frame of the video, with the court location of both players and the ball and categorical variables for: ball bounce (yes or no), swing type (serve, backhand, forehand, overhead).
</p>
<p>
Also, there's a community of tennis fans and analysts who are manually tracking games, based on a methodology <a href="https://www.tennisabstract.com/blog/2015/09/23/the-match-charting-project-quick-start-guide/">introduced by Jeff Sackman</a>. If the computer vision project is successful, it can hopefully help scale the tracking and we can get a more comprehensive account of tennis.
</p>


<h2>[2022-09-17] LIVEBLOG 002: Project Layout</h2>
<p>
Because this project is a holistic approach at obtaining tennis data, I've decided to break it into parts. As it stands, this is how I'm thinking of approaching it.
</p>
<h5>1. <a href="https://spazznolo.github.io/2022/09/18/classifying-game-state.html">Classify game states.</a></h5>
A tennis broadcast has commercials, replays, timeouts, etc. A surprisingly small sliver of the broadcast consists of actual gameplay. Building a binary classification model which differentiates gameplay from the rest of the broadcast is an important first step. Thankfully, the long, static, symmetric shots should make this relatively easy.
<h5>2. Identify and map the court.</h5>
The ultimate goal is to locate the players and ball using a <i>common coordinate system</i>. The good news is professional tennis matches are played on regulation courts. If a few key aspects of the court are identified, then we can leverage the known court dimensions to create a common coordinate system.
<h5>3. Identify the players.</h5>
The big question here is whether we can use a pre-trained model for this task or if transfer learning is necessary. The player on the front court is basically protruding from the frame, but given the camera angle, the back court player tends to be mixed in with the ball people. I'll try a pre-trained model first and use transfer learning on the likely outcome that it isn't enough.
<h5>4. Identify the ball.</h5>
There's already a few ball tracking alorgithms available. Some are out-of-the-box and likely to fail when trying to detect a small tennis ball which travels hundreds of kilometres per hour, but at least one - TrackNet - is designed specifically for tennis matches. The ball detection seems to be the most complex of these problems, so I'm going to do a sort of literature review on the available solutions and go from there.
<h5>5. Map the players and ball to the court.</h5>
The initial location of the players and ball will be in pixels. The final step is to map these pixel coordinates into standardized coordinates via the court in step 2.
<h5>Challenges.</h5>
My instinct: the true challenges will be 1) to sufficiently diversify the model so that it doesn't get confused by the different surfaces/lighting/stadium designs that games are played on and 2) to streamline the model in terms of memory and computation time so that the whole process isn't too slow moving.