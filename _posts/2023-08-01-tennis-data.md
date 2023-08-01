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
The Tennis Tracker is at the stage where feedback is necessary to move forward. In this post, I'll write a technical summary of the data, then at the end I'll describe a few ways in which you can use the data. The output contains three datasets. The point-level set provides descriptive statistics for a given point. Most of this set is taken from tennis24. The event-level set provides each (predicted) event in the tennis match, along with descriptive information like the time of the event, the type of event, the location of the ball, etc. The frame-level set provides the location of each player throughout the match at each frame.
</p>
<p>
I chose the US Open Womens' semi-final in 2022 between Iga Swiatek and Aryna Sabalenka as the first release for no particular reason, other than it was available and that this year's US Open is soon. I suppose you can consider this post a form of "marketing", because if it's successful and people (that's you!) pull interesting information from the data, I plan to scale the program to map out entire tournaments.
</p>
<p>
<h5>Data dictionaries</h5>
<b>Frame-level set</b>
<b>frame:</b> frame number of match.
<b>front_player_x:</b> x-coordinate of the front player in a given frame.
<b>front_player_y:</b> y-coordinate of the front player in a given frame.
<b>back_player_x:</b> x-coordinate of the back player in a given frame.
<b>back_player_y:</b> y-coordinate of the back player in a given frame.
</p>
<p>
<b>Event-level set</b>
<b>frame:</b> frame number of match.
<b>event:</b> name of event (serve, hit, bounce, net).
<b>ball_x:</b> x-coordinate of the tennis ball during an event.
<b>ball_y:</b> y-coordinate of the tennis ball during an event.
<b>actor:</b> player or location of event (front, back).
<b>state:</b> whether ball is in play (in) or not (out); only applicable for bounces.
<b>point:</b> point number of match.
</p>
<p>
<b>Point-level set</b>
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
<p>
<b>Runtime Specifications</b>
<b>broadcast time:</b> 132 minutes
<b>processing time:</b> 129 minutes
<b>processing tools:</b> Colab T4 GPU, personal Macbook Pro
</p>
<p>
<h5>About the data</h5>
The Tennis Tracker relies on a single broadcast feed at 720p and 30fps. This is decidedly <em>not</em> Hawkeye. Here's the thing: it doesn't have to <em>be</em> Hawkeye for it to be valuable. My goal in building this program was to contribute to tennis analytics by supplying data which is more detailed than what's currently on offer. I believe I am close to succeeding. That being said, there are still some measures which I wouldn't recommend you use without analyzing if it is stable enough for your needs. These include: ball speed (not stable enough yet), ace counts/locations, among others (I'll add to this as I work through them).
</p>
<p>
One measure I am very interested in seeing / potentially deriving, is "return probability". As more games are tracked, the output from the Tennis Tracker could provide the foundation for a general probability of return statistic, where each shot has a probability of return attributed to it. From this, we can observe which players tend to return difficult balls, which make the most mistakes (beyond "unforced errors"), and a plethora of other metrics.
</p>