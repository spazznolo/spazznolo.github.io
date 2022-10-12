---
layout: post
title:  "LIVEBLOG 018: General Update"
date:   2022-10-12 12:00:00 -0400
---
<h2>LIVEBLOG 018: General Update</h2>
<p>
An update of things:

- Game-state detection hasn't been touched since my first run of it using on the Williams' sisters Australian Open game. I haven't thought about it too much because it'll be easy to do and I'm in a problem solving mood lately.

- The first iteration of the court detection strategy is complete. It's not bad, but it tends to stretch out an edge of the backcourt, which is problematic not only for location data but for in/out of bound calls.

- The first iteration of the player detection strategy is complete. The post-processing here really smooths things out. This isn't a scientific paper, I don't care if I have to lean heavily on post-processing to get to the ultimate goal of tracking data, so long as I can document the accuracy of it.

- The first iteration of the coordinate projection is complete. Nothing much to say; as long as the other steps are okay, this is trivial.
</p>
