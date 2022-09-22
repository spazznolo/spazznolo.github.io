---
layout: post
title:  "LIVEBLOG 004: Classifying Game States [Part 1]"
date:   2022-09-19 12:52:05 -0400
---
<h2>LIVEBLOG 004: Classifying Game States [Part 1]</h2>
<p>
There are a few strategies to consider when classifying game states. The strategies are going to be evaluated on accuracy, memory requirements, and runtime. This is the most simple step of the project, so we can't dedicate much of our precious memory and runtime here. 
</p>
<p>
The act of classification necissitates a model. This doesn't need to be a complex neural network, though. In fact, a set of heuristics maybe be roughly as good while significantly reducing runtime. As it happens, it's incredibly easy to differentiate gameplay from commercials, time-outs, replays, etc (call it off-time). Here's a set of hand-labeled frames exhibiting gameplay and off-time.
</p>
<p>
It takes no time to see a pattern here. Really, the only false positives that should occur are pre-serve routines (which often seem to last longer than the corresponding gameplay itself). It shouldn't be a problem including these pre-serve routines, so long as the actual serve can be identified. I guess it'll just increase the number of frames in the following steps, which could be burdensome for the memory/runtime. We'll come back to this if necessary.
</p>
<h5>Classification Options</h5>
<p>
<b>Option 1: VGG16 (transfer learning)</b>
I'm going to start with the more complex option here because it's my first computer vision project and I'm interested to install the programs and packages to get this thing off the ground. As a way to ease into transfer learning, I'm going to label a chunk of frames from the 2004 US Open final between the Williams sisters, and predict another chunk of frames from the same final. The lack of diversity in court color and texture and stadium setup and lighting etc. should make this trivial.
</p>
<p>
<b>Option 2: Set of Heuristics</b>
A frame is a numeric matrix. We can reduce the complexity of the frame by averaging out chunks of the matrix, which decreases memory usage and runtime while allowing for easier detection of patterns. To go further, my instinct is that a statistical summary of the numeric matrix could be enough to properly differentiate game states. Also, if the summary itself isn't enough, it could be fed into a simple, traditional learning algorithm (like a logistic regression), which <i>should</i> still be much faster than the first option, and definitely would require less memory, so if the results are similar, this is the obvious choice. I'm sure there are already standards for this type of easy classification, so I'll round up the current methods for simple image classification.
</p>
<p>
These strategies will be implemented and evaluated in a future post.
</p>
