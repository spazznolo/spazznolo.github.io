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
<h5>2. Locate the court.</h5>
Professional tennis matches are played on regulation courts. This is important - by locating the court, we have a standardized system by which to measure distances. Pretty easily, the ball and players can be projected onto this system.
</p>
<p>
<h5>3. Identify the players.</h5>
The big question here is whether we can use a pre-trained model for this task or if transfer learning is necessary. The player on the front court is basically protruding from the frame, but given the camera angle, the back court player tends to be mixed in with the ball people. I'll try a pre-trained model first and use transfer learning on the likely outcome that it isn't enough.
</p>
<p>
<h5>4. Identify the ball.</h5>
Hmmmmm...
</p>
<p>
My instinct: the true challenges will be 1) to sufficiently diversify the model so that it doesn't get confused by the different surfaces games are played on and 2) to streamline the model in terms of memory and computation time so that the whole process isn't too slow moving.
</p>