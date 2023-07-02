---
layout: post
title:  "NHL Draft: An Application of Prospect Pick Probabilities [Part 2]"
date:   2023-07-02 1:00:00 -0400
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
<h2>An Application of Prospect Pick Probabilities [Part 2]</h2>
<p>
In <a href="https://spazznolo.github.io/2023/06/20/draft-probabilities-3.html">An Application of Prospect Pick Probabilities</a>, I introduced a new perspective on draft pick value using Prashanth Iyer and I's <a href="https://piyer97.shinyapps.io/NHLDraft2023/">draft probability tool</a>. Here, I extend the methodology to include prospect value uncertainty.
</p>
<p>
<h5>Accounting for Uncertainty</h5>
One of the main considerations for teams drafting in the 2-7 spot this year was whether they should risk their extremely valuable lottery pick on Matvei Michkov. He signed a 3-year contract in Russia. He only met with a few teams. He might be the most talented player in the draft. He may never come to North America... etc. Essentially, the question these teams were asking is this: is it worth drafting Michkov's uncertainty when more reliable, though perhaps less skilled, players are available? Once again, teams have to make a complex calculation. Once again, they're left with mostly instinct.
</p>
<p>
Unless!
</p>
<p>
Unless, prospect value uncertainty is quantified and included in the decision process.
</p>
<p>
<h5>Assigning Uncertainty</h5>
Adapting the previous post to include uncertainty is actually easy. Instead of assigning prospect values through point estimates (Bedard was at 24 WAR, Michkov at 17.5), prospects are assigned <a href="https://www.scribbr.com/statistics/probability-distributions/#:~:text=A%20probability%20distribution%20is%20a,using%20graphs%20or%20probability%20tables.">probability distributions</a> which reflect the uncertainty of their value. 
</p>
<p>
As an example: instead of Bedard's value being 24 WAR, it will be normally distributed with mean 24 and standard deviation 3. Here's what that looks like:
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/draft-probabilities-4-1.png" width="60%" length="150"/></div>
</p>
<p>
In this example:
  - Bedard has a 50% chance of providing 22-26 WAR.
  - Bedard has a 25% chance of providing 26+ WAR.
  - Bedard has a 25% chance of providing -22 WAR.
</p>
<p>
Like the point estimates in the first post, the actual distribution doesn't matter, it's just an example to illustrate the framework I'm introducing.
</p>
<p>
Let's assign these value distributions to each player, making sure Michkov's value has higher uncertainty by increasing the standard deviation of his distribution. Prospect values now look like this:
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/draft-probabilities-4-2.png" width="60%" length="150"/></div>
</p>
<p>
Then, these probability distributions are multiplied by the probability a prospect is available at each pick, as in the previous post. Pick values now look like this:
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/draft-probabilities-4-3.png" width="60%" length="150"/></div>
</p>
<p>
With these pick value distributions you get the same comparisons as you did in the previous post, plus:
  - the probability that a given pick will be more valuable than another.
  - WAR for whichever "outcome" you're interested in (like top 10% scenario, bottom 10%, etc.)
</p>
<p>
Let's re-visit the Montreal example where I suggested they should only trade up if the value of the fourth pick (15.87) exceeded that of their package (fifth pick (13.15) plus a piece). After including uncertainty, these point estimates become probability distributions and the difference between the two picks looks like this:
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/draft-probabilities-4-4.png" width="60%" length="150"/></div>
</p>
