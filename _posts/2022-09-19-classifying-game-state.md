---
layout: post
title:  "LIVEBLOG [Post 3] Classifying Game States"
date:   2022-09-18 12:52:05 -0400
---
<h2>LIVEBLOG [Post 3] Classifying Game States</h2>
<p>
There are a few strategies to consider when classifying game states. The strategies are going to be evaluated on accuracy, memory requirements, and runtime. This is the most simple step of the project, so we can't dedicate much of our precious memory and runtime here. 
</p>
<p>
The act of classification necissitates a model. This doesn't need to be a complex neural network, though. In fact, a set of heuristics maybe be roughly as good while significantly reducing runtime. As it happens, it's incredibly easy to differentiate gameplay from commercials, time-outs, replays, etc (call it off-time).
</p>
<p>
Here's a set of frames exhibiting gameplay and off-time that I hand-labeled while considering which models to try and how to rate them.
</p>


