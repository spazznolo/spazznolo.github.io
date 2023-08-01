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
<h2>Tennis Tracker (alpha): Initial Data Release</h2>
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
<h5>Data dictionary</h5>
Frame-level set
  - frame: frame number of match.
  - front_player_x: x-coordinate of the front player in a given frame.
  - front_player_y: y-coordinate of the front player in a given frame.
  - back_player_x: x-coordinate of the back player in a given frame.
  - back_player_y: y-coordinate of the back player in a given frame.

Event-level set
  - frame: frame number of match.
  - event: name of event (serve, hit, bounce, net).
  - ball_x: x-coordinate of the tennis ball during an event.
  - ball_y: y-coordinate of the tennis ball during an event.
  - actor: player or location of event (front, back).
  - state: whether ball is in play (in) or not (out); only applicable for bounces.
  - point: point number of match.

  Point-level set
  - point: point number of match.
  - serve: player holding the serve (home, away).
  - serve_side: side of serve for point (ad, deuce).
  - serve_location: side of serve for point (front, back).
  - home_point_score: number of points won in game by home player.
  - away_point_score: number of points won in game by away player.
  - home_game_score: number of games won in set by home player.
  - away_game_score: number of games won in set by away player.
  - home_set_score: number of sets won in match by home player.
  - away_set_score: number of sets won in match by away player.
</p>