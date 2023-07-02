---
layout: post
title:  "NHL Draft: Enhancing the Draft Pick Value Framework"
date:   2023-07-01 12:00:00 -0400
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
In <a href="https://spazznolo.github.io/2023/06/20/draft-probabilities-3.html">An Application of Prospect Pick Probabilities</a>, I introduced a new perspective on draft pick value using Prashanth Iyer and I's <a href="https://piyer97.shinyapps.io/NHLDraft2023/">draft probability tool</a>. Here, I extend the methodology to include prospect value uncertainty. Then I build a framework to optimize pick value.
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
<h5>Assigning Uncertainty</h5>
Next, each player is assigned a value distribution, making sure Michkov's value has higher uncertainty by increasing the standard deviation of his distribution. Then, these probability distributions are multiplied by the probability a prospect is available at each pick, as in the previous post.
</p>
<p>
Prospect values now look like this:
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/draft-probabilities-4-2.png" width="60%" length="150"/></div>
</p>
<p>
... and pick values now look like this:
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/draft-probabilities-4-3.png" width="60%" length="150"/></div>
</p>
<p>
The probability distributions offer some bonuses:
  - there is now a difference between the mean and median WAR.
  - we can now estimate the probability that a given pick will be more valuable than another.
  - higher certainty player cause pick values to shift towards them.
</p>
<p>
SHOW EXAMPLE OF NEW PICK VALUES
</p>
<p>
<h5>Optimization</h5>
The optimization of draft value in the NHL is similar to that of a fantasy draft for a sportsbook (include link to roster optimization), and has been explored specifically for the NHL <a href="http://statsportsconsulting.com/main/wp-content/uploads/Nandakumar_PerfectDraft-1.pdf">here</a>. In this section, I'll optimize draft value by combining the pick probabilities in our draft tool with the prospect value distributions assigned above.
</p>
To illustrate
<p>
</p>
<p>
</p>
<p>
</p>
<p>
</p>
<p>
</p>
<p>
</p>
<p>
</p>