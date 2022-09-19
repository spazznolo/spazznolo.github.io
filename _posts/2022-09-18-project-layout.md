---
layout: post
title:  "LIVEBLOG [Post 2] Project Layout"
date:   2022-09-18 10:52:05 -0400
---
<h2>LIVEBLOG [Post 2] Project Layout</h2>
<p>
Because this project is a holistic approach at obtaining tennis data, I've decided to break it into parts. As it stands, this is how I'm thinking of approaching it.
</p>
<p>
<h5>1. Classify game states.</h5>
A tennis broadcast has commercials, replays, timeouts, etc. A surprisingly small sliver of the broadcast consists of actual gameplay. Building a binary classification model which differentiates gameplay from the rest of the broadcast is an important first step. Thankfully, the long static, symmetric shots should make this relatively easy.
</p>
<p>
<h5>2. Identify the court.</h5>
Professional tennis matches are played on regulation courts. This is important - by locating the court, we have a standardized system by which to measure distances. 
</p>
<p>
<h5>3. Map the court.</h5>
After the court's been detected in step 2, pretty easily, the ball and players can be projected onto this system. This step should be the easiest, where the outputs from step 2, are projected onto a regulation court.
</p>
<p>
<h5>4. Identify the players.</h5>
The big question here is whether we can use a pre-trained model for this task or if transfer learning is necessary. The player on the front court is basically protruding from the frame, but given the camera angle, the back court player tends to be mixed in with the ball people. I'll try a pre-trained model first and use transfer learning on the likely outcome that it isn't enough.
</p>
<p>
<h5>4. Identify the ball.</h5>
There's already a few ball tracking alorgithms available. Some are out-of-the-box and likely to fail when trying to detect a small tennis ball which travels hundreds of kilometres per hour, but at least one - TrackNet - is designed specifically for tennis matches. The ball detection seems to be the most complex of these problems, so I'm going to dedicate a post to a sort of literature review on the available solutions and go from there.
</p>
<p>
<h5>5. Challenges.</h5>
My instinct: the true challenges will be 1) to sufficiently diversify the model so that it doesn't get confused by the different surfaces/lighting/stadium designs that games are played on and 2) to streamline the model in terms of memory and computation time so that the whole process isn't too slow moving.
</p>