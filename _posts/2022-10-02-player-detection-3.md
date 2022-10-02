---
layout: post
title:  "LIVEBLOG 015: Player Detection 03"
date:   2022-10-02 12:00:00 -0400
---
<h2>LIVEBLOG 015: Player Detection 03</h2>
<p>
I'm going to call today a soft implementation of the strategies used in the papers I read yesterday. Many of these concepts are covered in opencv, so the implementation is pretty easy. I'm calibrating the thresholds and blurs and running random chunks of gameplay through it. Mostly I do this to capture patterns, but I'm realizing the more I use these clips to calibrate, the more I'm biasing my methods on the collection of games I've tracked. Probably, I should download a bunch of different game highlights to better diversify the chunks I'm "training" on.
</p>
<p>
As for the actual detection, the player closest to the camera is easy to locate in full, but the player on the other side of the court is more difficult. While running through these random game chunks, I'm thinking that I could implement for the player detection what the Table Tennis paper did for the ball - use the previous known location of the player, and then search only in the neighborhood of that location. There's still the problem that sometimes the feet disappear from the contour due to lower differencing from the court.
</p>
