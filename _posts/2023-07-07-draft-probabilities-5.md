---
layout: post
title:  "NHL Draft: Introducing a new NHL drafting strategy"
date:   2023-07-07 12:00:00 -0400
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
<h2>Introducing a new NHL drafting strategy</h2>
<p>
In <a href="https://spazznolo.github.io/2023/06/20/draft-probabilities-3.html">An Application of Prospect Pick Probabilities</a>, I used Prashanth Iyer and myself's <a href="https://piyer97.shinyapps.io/NHLDraft2023/">draft probability tool</a> to create a new pick value framework which captured the unique dynamics of a given draft. Then, I <a href="https://spazznolo.github.io/2023/06/25/draft-probabilities-4.html">extended the methodology</a> to include the uncertainty of prospect values. Here, I'll introduce a brand new drafting strategy for the NHL which aims to maximize draft value. But first, some background.
<p>
<h5>Background on Optimization</h5>
The optimization of draft value has been explored specifically for the NHL by now Kraken analyst <a href="https://twitter.com/nnstats">@nnstats</a> in this 2017 <a href="https://www.statsportsconsulting.com/wp-content/uploads/Nandakumar_PerfectDraft-1.pdf">paper</a>. It was a counter to the prevalent discourse at the time, which assumed the optimal draft was achieved by simply picking the best players as they were available. Instead, she argued that a team should only draft the best player available (BPA) if he won't be available for their next pick. For instance, Jamie Benn, a sixth round pick, should have been drafted in the fifth round to maximize total draft value.
</p>
<p>
The key outstanding question from this work was: "How do we determine if the risk of deferring on the BPA and losing him is worth the reward of drafting another good prospect before landing the BPA later?" In this post, I'll show that the prospect pick probabilities from our draft tool, when combined with prospect values, allow for a probablistic framework to make such a decision.
</p>
<p>
<h5>Introducing a new NHL drafting strategy</h5>
The strategy aims to determine a team's maximum conditional draft value at each pick. The maximum value is selected from a list of conditional draft values associated with each available prospect. Using a team's first two picks as an example, the strategy can be written (somewhat) formally like this:
</p>
<br>
for n remaining prospects, ranked 1 to n<br>
max draft value = max(v1, v2, ..., vn)<br>
where,<br>
vi = estimated draft value when choosing prospect i with the next pick, specifically for i != 1<br>
vi = v(pi) + (Pj(p1) x v(p1)) + ... + ((1 - Pj(p1) - ... - Pj(p(x-1))) x v(px))<br>
where,<br>
v(pi) = value of prospect i,<br>
Pj(pi) = probability that propsect i is available at pick j, and<br>
Pj(p1) + ... + Pj(p(x-1)) < 1 and Pj(p1) + ... + Pj(p(x-1)) + Pj(p(x))) >= 1<br>
<p>
To further illustrate, let's consider the first round of this year's draft up to pick 17.
</p>
<p>
<h5>An example using the Red Wings' first round picks</h5>
The Red Wings held the 9th and 17th picks in this year's draft. I'm going to calculate the optimal drafting strategy for the Red Wings using a set of <a href="https://twitter.com/spazznolo/status/1674392375018307585">well-performing</a> prospect rankings from Bob McKenzie, Cam Robinson, and Chris Peters. Prospect values are assigned using their respective ranking in the historical pick value chart.
</p>
<p>
At pick 9 of the draft, these analysts had the remaining players ranked as such:
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/draft-probabilities-5-4.png" width="80%" length="200"/></div>
</p>
<p>
Let's determine who each analyst should draft at 9 in order to maximize their expected draft value for picks 9 and 17. To answer, we use the equation shown above, which requires: 1) the value of the prospect taken at 9, 2) the conditional probabilities of the remaining prospects being available at 17, and 3) the values of these remaining prospects. 
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/draft-probabilities-5-5.png" width="80%" length="200"/></div>
</p>
<p>
Here, McKenzie and Robinson should take the BPA to maximize conditional draft value, but Peters should defer and take his second BPA, Zach Benson.
</p>