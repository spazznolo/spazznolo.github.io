---
layout: post
title:  "Tennis Tracker (alpha): US Open W SF 2022"
date:   2023-07-30 12:00:00 -0400
---
<head>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-DGRHZS5DNM"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-DGRHZS5DNM');
</script>
</head>
<h2>Tennis Tracker (alpha): Data Release</h2>
<p>
The Tennis Tracker is at the stage where outside input is necessary to move forward. In this post, I'll write a technical summary of the data, then at the end I'll include how the data can be used, and how it shouldn't be used. 
</p>
<p>
<h5>Specifications</h5>

  - broadcast time: 132 minutes
  - processing time: 129 minutes
  - processing tools: Colab T4 GPU, personal Macbook Pro
</p>
<p>
<h5>Data dictionaries</h5>
adfafs
<p>
<h5>Frame-level set</h5>
tadfafs
</p>
<p>
<b>frame:</b> frame number of match.<br>
<b>front_player_x:</b> x-coordinate of the front player in a given frame.
<b>front_player_y:</b> y-coordinate of the front player in a given frame.
<b>back_player_x:</b> x-coordinate of the back player in a given frame.
<b>back_player_y:</b> y-coordinate of the back player in a given frame.
</p>
<p>
<h5>Event-level set</h5>
asdfasdf
</p>
<p>
<b>frame:</b> frame number of match.
<b>event:</b> name of event (serve, hit, bounce, net).
<b>ball_x:</b> x-coordinate of the tennis ball during an event.
<b>ball_y:</b> y-coordinate of the tennis ball during an event.
<b>actor:</b> player or location of event (front, back).
<b>state:</b> whether ball is in play (in) or not (out); only applicable for bounces.
 <b>point:</b> point number of match.
</p>
<p>
<h5>Point-level set</h5>
asdfasdf
</p>
<p>
<b>point:</b> point number of match.
<b>serve:</b> player holding the serve (home, away).
<b>serve_side:</b> side of serve for point (ad, deuce).
<b>serve_location:</b> side of serve for point (front, back).
<b>home_point_score:</b> number of points won in game by home player.
<b>away_point_score:</b> number of points won in game by away player.
<b>home_game_score:</b> number of games won in set by home player.
<b>away_game_score:</b> number of games won in set by away player.
<b>home_set_score:</b> number of sets won in match by home player.
<b>away_set_score:</b> number of sets won in match by away player.
</p>