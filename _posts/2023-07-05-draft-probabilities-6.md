---
layout: post
title:  "NHL Draft: Post-Draft Analysis"
date:   2023-07-20 12:00:00 -0400
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
<h2>Enhancing the Draft Pick Value Framework</h2>
<p>
In general the probabilities were pretty well calibrated. However, the model was too certain in the top 10 picks. As a result, the sportsbooks cooked us. 
</p>

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