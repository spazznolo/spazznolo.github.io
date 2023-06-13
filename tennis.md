---
layout: page
title: / tennis
permalink: /tennis/
---
<a href="https://spazznolo.github.io/2023/01/15/tennis-framework.html">tennis tracking framework</a>
<p>
<h2>[2022-09-16] Hello, tennis: A Liveblog</h2>
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

<p>
<h2>[2022-09-17] Project Layout</h2>
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

<p>
<h2>[2022-09-18] Tracking Games 01</h2>
Quick post on how the modelling set will be built. I'm looking for diversity of game time, court, years and gender, with a testing set that features games not in the training or validation sets. I've decided on randomly sampling 10 random 60 seconds chunks from 12 matches. That's a total of 120 minutes, or, at 1,600 frames a minute, 192,000 frames. The good news is that gameplay, like off-time, is sequential, so it won't be as daunting as it might sound. After doing 10 minutes of the Williams sisters Australian Open final in 2003, it looks like I'm averaging 3 minutes of labelling per 1 minute of broadcast time. Extrapolating, it will probably take around 6 hours to get the modelling set I'd like to start with.
</p>
<h5>Games I've chosen to track.</h5>
<p>
<b>Clay</b>
2009 Madrid Open M
2012 Roland-Garros M
2019 Stuttgart Open W
2020 Stuttgart Open W
</p>
<p>
<b>Grass</b>
2015 Wimbeldon M
2018 Wimbeldon W
2019 Wimbeldon W
2019 Wimbeldon M
</p>
<p>
<b>Hard</b>
2017 Australian Open W
2019 US Open M
2020 Australian Open W
2022 US Open W
</p>

<p>
<h2>[2022-09-19] Classifying Game States 02</h2>
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

<p>
<h2>[2022-09-20] Court Detection 01</h2>
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
From drawing hough lines on a variety of gameplay frames, the thing that strikes me most are the four lines which make up the length of the court. The two on the outside are for doubles and the two on the inside are for singles. Here we have two sets of lines which have roughly the same length and slope when captured on the broadcast. Gut feel: a set of heuristics can satisfactorily detect the court well enough for my purposes.

<p>
<h2>[2022-09-21] GitHub Repository</h2>
I created a <a href="https://github.com/spazznolo/tennis-tracker">repository</a> for this project in the off-chance it snowballs into something bigger. Tracked a game today, or ten 60 second chunk of a game between Federer and Djokovic on clay. The camerawork was a little more dynamic than the first two games I tracked, but the court detection approach using a set of heuristics with hough lines did not faulter, which is encouraging. Also, downloaded all the necessary games for the initial model and started using Todoist, an app to track my project tasks.

<p>
<h2>[2022-09-22] Court Detection 02</h2>
In the last Court Detection post, I wrote vaguely about detecting the tennis court using a set of heuristics based on Hough lines. I'm going to expand on it here, introduce the first iteration of this approach, and visualize the outcome on 25 randomly selected frames featuring gameplay (this part will only be updated once I've tracked the 12 games).
</p>
<p>
<b>Jeremie's set of heuristics for court detection</b>
1. Detect Hough lines 
2. Identify the lengthwise court lines (doubles and singles borders) by filtering Hough lines having:
    a. absolute slope between 1.5 and 3.
    b. length over 200 pixels.
3. Identify widthwise court lines by filtering the Hough lines having:
    a. y-coordinates between the minimum and maximum y-coordinates lengthwise lines (+/- 10 pixels)
    b. x-coordinates equal to or between the minimum and maximum x-coordinates lengthwise lines (+/- 5 pixels)
</p>
<p>
<div style="text-align: center"> 
<img src="https://spazznolo.github.io/figs/hough-line-ex-2.jpg" width="60%" length="150"/>
</div>
</p>

<p>
<h2>[2022-09-23] Tracking Games 02</h2>
I tracked all the clay and grass games yesterday. That's 80 minutes of broadcast time. It took two hours in total. Tracking at 1.5x realtime is twice as fast as I did in my test runs with the Williams final, which is encouraging. I'll probably finish the rest today.
</p>
<p>
The set of heuristics for the court detection strategy is coming together. It's starting to look like a sophisticated model won't be necessary. I have to test it, of course, but I've been greedy and taken random game frames to see how the initial attempt holds up and it's doing well. One idea is to get all Hough lines, block filter on a few conditions, and then train a logistic regression on the length-wise lines. It would make it a little more robust. But that's only at the back of my mind, right now I'm focused on keep things deterministic.
</p>
<p>
It dawned on me today that hard court games are much easier to predict on because the synthetic court has less imperfections. It's possible the court types are different enough that they could use their own models. As the project moves on, I'm having to make concessions, which is natural, and one major concession might be to limit the project to hard courts for the first step. The US and Austalian Opens are both on hard court and both have great video quality.
</p>
<p>
A few other things. I've tracked 100 minutes of tennis broadcasts so far and all but one (!) point was shot from the same lengthwise, static setup. This isn't to say there aren't small differences each point/game, just that the basic court detection method has a decent chance of succeeding. Curious to see how fast it will be on a fps basis. Also, the sound of racquets hitting a ball, the replay analyst breaking down a play, and the crowd cheers are all easily distingushable, which makes me wonder if sound should be included. On top of this, there seems to be a general formula for a broadcast in terms of the feed changes, something like: lengthwise static gameplay shot to change of camera perspective for player reaction to replay from different perspective to lengthwise static gameplay shot for the serve routine. Oh, and it's sort of funny how some players celebrate in ways which seem not so sportmanslike lol.
</p>

<p>
<h2>[2022-09-24] Court Detection 03</h2>
Tracked the last of the 12 games this morning. Realized I hadn't thought of a proper pipeline from tracking to training, and paid for it in time and monotony, but it's finished. Next is to take random samples of the frames labelled as gameplay and plot the first iteration of the Hough line method which I'll outline again below.
</p>
<p>
The most challenging part of the court detection strategy so far has been data wrangling. Python isn't my first language and the OpenCV objects-to-pandas pipeline is a little... weird. Anyways, that's to say that the strategy is exceedingly simple and the first version should be finished by the end of this weekend. It'll definitely need refinement, but I have ideas on how to improve it, so it isn't a worry. 
</p>
<p>
As a reminder:
</p>
<p>
<b>Jeremie's set of heuristics for court detection</b>
1. Detect Hough lines 
2. Identify the lengthwise court lines (doubles and singles borders) by filtering Hough lines having:
    a. absolute slope between 1 and 3.
    b. length over 100 pixels.
3. Identify widthwise court lines by filtering the Hough lines having:
    a. y-coordinates either between the minimum or maximum y-coordinates of the lengthwise lines (+/- 10 pixels)
    b. x-coordinates between the minimum and maximum x-coordinates lengthwise lines (+/- 10 pixels)
</p>
<p>
<b>Results (Iteration 1)</b>
<p>
<div style="text-align: center"> 
<img src="https://spazznolo.github.io/figs/hough-collage-1.jpg" width="90%" length="300"/>
</div>
</p>
<p>
Obviously, there are large problems here. Mostly they stem from either the false positives or false continuations of the lengthwise lines. The widthwise lines rely on a correct y-range, and a false positive/continuation changes the range for the worse. In retrospect, it was naive to try a deterministic approach, but I'm happy to have tried, because it folds in nicely to the next step.
</p>

<p>
<h2>[2022-09-26] Court Detection 04</h2>
Spent today thinking up an iterative approach at finding the lines which make up the boundary of the court. Somewhat begrudgingly, I've turned to clustering the Hough lines which pass the initial block filter (absolute slope between 1 and 3). It's a univariate hierarchical clustering strategy using lines' absolute slope, followed by a filtering of all lines which are part of the two largest clusters, then taking the minimum median absolute slope from these two largest groups (usually the largest median absolute slope is the inner lengthwise lines and the smallest is the outter lines).
</p>
<p>
Also, to remind myself: the camera is mostly static. This means there should be a quick, efficient check to see if it has moved from the previous frame. Off the top of my head, I can run the Hough line algo each frame and if the lengthwise lines are nearly identical then keep the same coordinate system and move to the next frame.
</p>
<b>Results (Iteration 2)</b>
<p>
<div style="text-align: center"> 
<img src="https://spazznolo.github.io/figs/hough-collage-2.jpg" width="90%" length="300"/>
</div>
</p>

<p>
<h2>[2022-09-27] Court Detection 05</h2>
The clustering has made the strategy much more robust, especially in combination with taking the median slope and intercept of the lines. Next is to plot these lines through the whole image, creating a plane where the court should be. This should be ready later today.
</p>
<p>

</p>
<b>Results (Iteration 3)</b>
<p>
<div style="text-align: center"> 
<img src="https://spazznolo.github.io/figs/hough-collage-3.jpg" width="90%" length="300"/>
</div>
</p>

<p>
<h2>[2022-09-28] Change-up 06</h2>
The final iteration of the first version of the lengthwise court line capture is complete. Next is to get the widthwise lines. I can either rely on more clustering around the ends of the lengthwise lines or try for a new approach. Currently, the strategy runs at about 1.5x realtime, which I think is unacceptable for actual production but is fine for now. Here it is below.
</p>
<p>
<div style="text-align: center"> 
<img src="https://spazznolo.github.io/figs/hough-line-ex-4.jpg" width="90%" length="300"/>
</div>
</p>
<p>
I'm going to change things up for the next bit and temporarily abandon the court detection bit to work on player detection. This was originally supposed to train my computer vision muscle, but lately I've mostly been working with filtering Hough lines and I'm looking for a change of pace.
</p>
<p>
Update: While reading various strategies to detect players, I came across a <a href="https://www.researchgate.net/publication/221411677_Player_Detection_and_Tracking_in_Broadcast_Tennis_Video">paper</a> outlining a strategy which uses non-dominant color extraction. I found an example of this on Stack and interpreted the code to get this:
</p>
<p>
<div style="text-align: center"> 
<img src="https://spazznolo.github.io/figs/hough-line-ex-3.jpg" width="90%" length="300"/>
</div>
</p>

<p>
<h2>[2022-09-29] Player Detection 01</h2>
Literature review today. Read a <i>fantastic</i> paper on table tennis tracking <a href="Player Detection 01">here</a>. Not only is the methodology explained clearly, the author provides details on the modules and parameters used in their research. Much appreciated. I'll try their method for ball detection. I can say some of their ideas will definitely make an impact on the court detection algorithm I've been writing.
</p>
<p>
Also made a bit of headway on the player detection and as soon as I hit a wall I jumped over to the court perspective change, which I knew would be easy. Basically, if you know the dimensions of a regulation court and you locate the four court corners of an image, you can transform the whole thing, getting the located player's actual court location almost for free (I think).
</p>

<p>
<h2>[2022-10-01] Player Detection 02</h2>
More literature review. This <a href="https://www.researchgate.net/publication/285203332_An_Efficient_Ball_and_Player_Detection_in_Broadcast_Tennis_Video">paper</a> breaks down a similar methodology as the previous research I posted on Table Tennis. Actually, they are nearly identical in their processing - they combine a background filter with frame differencing using something called a logical AND operation. It sounds formal so I looked into it but it seems they're just combining the images. Maybe something was lost in the translation. Anyways, they follow this with thresholding and dilation.
</p>
<p>
In many of these papers, accuracy is measured as the percentage of time a player/ball is correctly located on the screen. This is a little more stringent than what I'm going for in this project. With tracking data, these misses (if they're known) probably can be imputed. Weird inaccuracies might be smoothed when the frames are connected into a sequence.
</p>
<p>
<div style="text-align: center"> 
<img src="https://spazznolo.github.io/figs/player-detect-1.png" width="60%" length="150"/>
</div>
</p>

<p>
<h2>[2022-10-02] Player Detection 03</h2>
I'm going to call today a soft implementation of the strategies used in the papers I read yesterday. Many of these concepts are covered in opencv, so the implementation is pretty easy. I'm calibrating the thresholds and blurs and running random chunks of gameplay through it. Mostly I do this to capture patterns, but I'm realizing the more I use these clips to calibrate, the more I'm biasing my methods on the collection of games I've tracked. Probably, I should download a bunch of different game highlights to better diversify the chunks I'm "training" on.
</p>
<p>
As for the actual detection, the player closest to the camera is easy to locate in full, but the player on the other side of the court is more difficult. While running through these random game chunks, I'm thinking that I could implement for the player detection what the Table Tennis paper did for the ball - use the previous known location of the player, and then search only in the neighborhood of that location. There's still the problem that sometimes the feet disappear from the contour due to lower differencing from the court.
</p>

<p>
<h2>[2022-10-03] Pipeline Build 01</h2>
Started thinking about tying together the modules to get the desired output for a single point. This will force me to zoom out and notice the fault lines of the project so far. One thing I'm curious to see is how robust the imputation will be. For example, if a player is misidentified (and this should be obvious), we can impute their location by taking their last known location. One frame is not enough time to really change one's court location very much. 
</p>

<p>
<h2>[2022-10-09] Player Detect Demo</h2>
It's been a while. I've been working on a court/player detection demo. I'm going to run a demo on an entire match and troubleshoot from there. So far one point has been processed and the results were encouraging. I'm trying to find a way to embed videos here, but the file size is just too big for github pages so far. Maybe I'll upload some demos to Youtube later.
</p>

<p>
<h2>[2022-10-12] General Update</h2>

- Game-state detection hasn't been touched since my first run of it using on the Williams' sisters Australian Open game. I haven't thought about it too much because it'll be easy to do and I'm in a problem solving mood lately.

- The first iteration of the court detection strategy is complete. It's not bad, but it tends to stretch out an edge of the backcourt, which is problematic not only for location data but for in/out of bound calls.

- The first iteration of the player detection strategy is complete. The post-processing here really smooths things out. This isn't a scientific paper, I don't care if I have to lean heavily on post-processing to get to the ultimate goal of tracking data, so long as I can document the accuracy of it.

- The first iteration of the coordinate projection is complete. Nothing much to say; as long as the other steps are okay, this is trivial.
</p>
