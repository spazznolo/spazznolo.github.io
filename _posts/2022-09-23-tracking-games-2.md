---
layout: post
title:  "LIVEBLOG 008: Tracking Games [Part 2]"
date:   2022-09-23 12:00:00 -0400
---
<h2>LIVEBLOG 008: Tracking Games [Part 2]</h2>
<p>
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