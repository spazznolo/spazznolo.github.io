---
layout: post
title:  "NHL Draft: Introducing a new drafting strategy"
date:   2023-07-05 12:00:00 -0400
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
In <a href="https://spazznolo.github.io/2023/06/20/draft-probabilities-3.html">An Application of Prospect Pick Probabilities</a>, I used Prashanth Iyer and I's <a href="https://piyer97.shinyapps.io/NHLDraft2023/">draft probability tool</a> to create a new pick value framework which captured the unique dynamics of a given draft. Then, I <a href="https://spazznolo.github.io/2023/06/25/draft-probabilities-4.html">extended the methodology</a> to include prospect value uncertainty. Here, I introduce a new drafting strategy for NHL teams by optimizing the pick value framework.
</p>
<p>
But first, a visual recap for those who don't want to read the <a href="https://spazznolo.github.io/2023/06/16/draft-probabilities-2.html">previous</a> <a href="https://spazznolo.github.io/2023/06/20/draft-probabilities-3.html">three</a> <a href="https://spazznolo.github.io/2023/07/02/draft-probabilities-4.html">posts</a> (I get it).
</p>
<p>
<h5>Visual Recap</h5>
1. A rank-ordered logit model was built using numerous publication rankings throughout the draft year to derive prospect pick probabilities, like this:
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/draft-probabilities-4-4.png" width="60%" length="150"/></div>
</p>
<p>
2. Prospect values were derived using a historical draft pick value chart (values are placeholders for teams' actual internal projections), along with uncertainty estimates, like this:
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/draft-probabilities-4-4.png" width="60%" length="150"/></div>
</p>
<p>
3. The previous two points were combined to create new pick value charts, like this:
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/draft-probabilities-4-4.png" width="60%" length="150"/></div>
</p>
<p>
As an example, the value of the third pick for a team who ranked the top 3 players in the draft as Bedard-Fantilli-Carlsson would be calculated as follows:
  - There's a 0% chance Bedard is available, so his value is multiplied by 0.
  - There's a 21.0% chance Fantilli is available, so his value is multiplied by 0.210.
  - There's a 79% that neither Bedard nor Fantilli is available, so Carlsson's value is multiplied by 0.790.
  - These three values are summed to get the third pick's value.
</p>
<p>
<h5>Background on Optimization</h5>
The optimization of draft value has been explored specifically for the NHL by now Kraken analyst <a href="https://twitter.com/nnstats">@nnstats</a> in this 2017 <a href="https://www.statsportsconsulting.com/wp-content/uploads/Nandakumar_PerfectDraft-1.pdf">paper</a>. It was a counter to the prevalent discourse at the time, which assumed the optimal draft was simply picking the best players as they were available. She argued that a team should only draft the best player available (BPA) if he won't be available for their next pick. For instance, Jamie Benn, a sixth round pick, should have been drafted in the fifth round to maximize total draft value.
</p>
<p>
The key outstanding question from this work was: "How can we determine if a prospect will still be available for a team's next pick?" In this post, I'll show that the prospect pick probabilities from our draft tool can provide the answer.
</p>
<p>
<h5>Introducing a new NHL drafting strategy</h5>
A team's draft value is optimized when they, in aggregate, maximize the possible value from their draft picks. This cannot be done in retrospect - it can only be done looking ahead, which means the framework must be probablistic.
</p>
<p>
A team's draft value is not taken at the pick level, but at the draft level. These may often converge, but when they don't, a team must forego drafting the best player available in order to maximize draft value.
</p>
<p>
As picks are made, a team's estimated optimal draft value will change, until it is their turn to pick.
</p>
<p>
To illustrate, let's consider the first round of this year's draft up to pick 17.
</p>
<p>
<h5>An example using the Red Wings' first round picks</h5>
The Red Wings held the 9th and 17th picks in this year's draft. They ended up taking Nate Danielson and Axel Sandin Pelikka, presumably their BPAs. To illustrate the new drafting strategy, I'll share a situation where draft value was not maximized.
</p>
<p>
On June 1st, 2023, Chris Peters, an NHL draft analyst at FloHockey, released his ranking of the top 32 propsects. This ranking ended up becoming the 3rd closest to the actual draft order among 90+ rankings. We're going to pretend his rankings are the Red Wings' for this example. At pick 9 of the draft, Peters had the remaining players ranked as such:
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/draft-probabilities-5-4.png" width="60%" length="150"/></div>
</p>
<p>
The question: "who should the Wings draft at 9 in order to maximize their expected draft value for picks 9 and 17?"
</p>
<p>
To determine this, they need: 1) the value of the prospect taken at 9, 2) the conditional probabilities of the remaining prospects being available at 17, and 3) the values of these remainig prospects. 
</p>
<p>
<em>Note:</em> Another way to frame this is to find the maximum of the conditional values for F().
</p>