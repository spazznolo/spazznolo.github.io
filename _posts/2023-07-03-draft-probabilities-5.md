---
layout: post
title:  "NHL Draft: Introducing a new drafting strategy"
date:   2023-07-15 12:00:00 -0400
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
In <a href="https://spazznolo.github.io/2023/06/20/draft-probabilities-3.html">An Application of Prospect Pick Probabilities</a>, I used Prashanth Iyer and myself's <a href="https://piyer97.shinyapps.io/NHLDraft2023/">draft probability tool</a> to create a new pick value framework which captured the unique dynamics of a given draft. Then, I <a href="https://spazznolo.github.io/2023/06/25/draft-probabilities-4.html">extended the methodology</a> to include prospect value uncertainty. Here, I'll introduce a brand new drafting strategy for the NHL by optimizing the pick value framework. But first, some background.
<p>
<h5>Background on Optimization</h5>
The optimization of draft value has been explored specifically for the NHL by now Kraken analyst <a href="https://twitter.com/nnstats">@nnstats</a> in this 2017 <a href="https://www.statsportsconsulting.com/wp-content/uploads/Nandakumar_PerfectDraft-1.pdf">paper</a>. It was a counter to the prevalent discourse at the time, which assumed the optimal draft was achieved by simply picking the best players as they were available. Instead, she argued that a team should only draft the best player available (BPA) if he won't be available for their next pick. For instance, Jamie Benn, a sixth round pick, should have been drafted in the fifth round to maximize total draft value.
</p>
<p>
The key outstanding question from this work was: "How can we determine if a prospect will still be available for a team's next pick?" In this post, I'll show that the prospect pick probabilities from our draft tool, when combined with prospect values, allow for a probablistic framework to make such a decision.
</p>
<p>
<h5>Introducing a new NHL drafting strategy</h5>
The strategy aims to determine a team's maximum conditional draft value at each pick. The maximum

The total expected draft value is calculated for each prospect available for selection. Therefore there are as many draft values as prospects available for a pick. The optimal draft value is the maximum of this list. Using a team's first to picks as an example, the strategy can be written in mathematical notation like this:

For each prospect, the draft value is calculated like this:
    v_i = v(p_i) + pr(p2)*v(p2) + pr(p3)*v(p3) + ... + (1 - sum(p_1:p_(x-1))*v(p_x)
  where, 
  and, pr(p_i) = probability p_i is available and the BPA

This yields a list of draft values the length being the number of available prospects.

The maximum from this list is taken as the optimal draft value:
max_draft_value = max(v1, v2, ..., vn)

</p>
<p>
To illustrate, let's consider the first round of this year's draft up to pick 17.
</p>
<p>
<h5>An example using the Red Wings' first round picks</h5>
The Red Wings held the 9th and 17th picks in this year's draft. I'm going to calculate the optimal drafting strategy for the Red Wings using a set of well-performing prospect rankings: Bob McKenzie, Cam Robinson, and Chris Peters. 
</p>
<p>
At pick 9 of the draft, these analysts had the remaining players ranked as such:
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/draft-probabilities-5-4.png" width="80%" length="200"/></div>
</p>
<p>
The question: "who should each of these analysts draft at 9 in order to maximize their expected draft value for picks 9 and 17?" We require: 1) the value of the prospect taken at 9, 2) the conditional probabilities of the remaining prospects being available at 17, and 3) the values of these remaining prospects. 
</p>