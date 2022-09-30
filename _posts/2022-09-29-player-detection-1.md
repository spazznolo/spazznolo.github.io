---
layout: post
title:  "LIVEBLOG 013: Player Detection 01"
date:   2022-09-29 12:00:00 -0400
---
<h2>LIVEBLOG 013: Player Detection 01</h2>
<p>
Literature review today. Read a <i>fantastic</i> paper on table tennis tracking <a href="Player Detection 01">here</a>. Not only is the methodology explained clearly, the author provides details on the modules and parameters used in their research. Much appreciated. I'll try their method for ball detection. I can say some of their ideas will definitely make an impact on the court detection algorithm I've been writing.
</p>
<p>
Made a bit of headway on the player detection and as soon as I hit a wall I jumped over to the court perspective change, which I knew would be easy. Basically, if you know the dimensions of a regulation court and you locate the four court corners of an image, you can transform the whole thing, getting the located player's actual court location almost for free (I think).
</p>

