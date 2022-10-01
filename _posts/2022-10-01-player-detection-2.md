---
layout: post
title:  "LIVEBLOG 014: Player Detection 02"
date:   2022-10-01 12:00:00 -0400
---
<h2>LIVEBLOG 014: Player Detection 02</h2>
<p>
More literature review. This <a href="https://www.researchgate.net/publication/285203332_An_Efficient_Ball_and_Player_Detection_in_Broadcast_Tennis_Video">paper</a> breaks down a similar methodology as the previous research I posted on Table Tennis. Actually, they are nearly identical in their processing - they combine a background filter with frame differencing using something called a logical AND operation. It sounds formal so I looked into it but it seems they're just combining the images. Maybe something was lost in the translation. Anyways, they follow this with thresholding and dilation.
</p>


