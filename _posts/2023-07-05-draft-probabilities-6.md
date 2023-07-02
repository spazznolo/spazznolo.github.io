---
layout: post
title:  "NHL Draft: Post-Draft Analysis"
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
<h2>Enhancing the Draft Pick Value Framework</h2>
<p>
In general the probabilities were pretty well calibrated. However, the model was too certain in the top 10 picks. As a result, the sportsbooks cooked us. 
</p>
<p>
<h5>Accounting for Uncertainty</h5>
One of the main considerations for a team drafting in the 2-7 spot was whether they should risk their extremely valuable lottery pick on Matvei Michkov. He signed a 3-year contract in Russia. He only met with a few teams. He might be the most talented player in the draft. He may never come to North America... etc. Essentially, the question these teams are asking is this: is it worth drafting Michkov's uncertainty when more reliable, though perhaps less skilled, players are available? Once again teams have to make a complex calculation. Once again they're left with mostly instinct.
</p>
<p>
Unless!
</p>
<p>
Unless, prospect value uncertainty is quantified and included in the decision process.
</p>
<p>
Adapting the previous post to include uncertainty is actually easy. Instead of assigning prospect values through point estimates (Bedard was at 24 WAR, Michkov at 17.5), prospects are assigned probability distributions which reflect the uncertainty of their value. 
</p>
<p>
As an example: instead of Bedard's value being 24 WAR, it will be normally distributed with mean 24 and standard deviation x. Here's what that looks like below.
</p>
image
<p>
In this illustration:
  - Bedard has a xx% chance of providing xx-xx WAR.
  - Bedard has a xx% chance of providing xx+ WAR.
  - Bedard has a xx% chance of providing -xx WAR.
</p>
<p>
Much like the point estimates in the first post, the actual distribution doesn't matter, it's just an example.
</p>
<p>
<h5>Assigning Uncertainty</h5>
We assign probability distributions to all players and make sure to assign higher uncertainty to Michkov through a higher standard deviation. Then, these probability distributions are multiplied by the probability  probability a prospect is available by their WAR point estimate, we multiply it by their <em>probability distribution</em>.
</p>
<p>
Pick values now look like this
</p>
image
<p>
An interesting result of these probability distributions is that the estimated pick value derived with the point estimate will change. In particular, highly uncertain players will cause the estimated value to shift away from them.
<p>
The probability distributions offer some bonuses:
  - the expected value (median WAR) will be more accurate.
  - can estimate the probability that a given pick will be more valuable than another.
  - 
</p>
<p>
<h5>Optimization</h5>
The optimization of draft value in the NHL is similar to that of a fantasy draft for a sportsbook (include link to roster optimization), and has been explored specifically for the NHL <a href="http://statsportsconsulting.com/main/wp-content/uploads/Nandakumar_PerfectDraft-1.pdf">here</a>. In this section, I'll expand the idea by combining the pick probabilities in our draft tool and the prospect value distributions assigned above to optimize draft value.
</p>
Red Wings
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