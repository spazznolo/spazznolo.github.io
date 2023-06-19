---
layout: post
title:  "NHL Draft: An Application of Prospect Pick Probabilities"
date:   2023-06-16 12:00:00 -0400
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
<h2>An Application of Prospect Pick Probabilities</h2>
<p>
The prospect pick probabilities available on the "Draft Pick Probabilities" tab of the <a href = "https://piyer97.shinyapps.io/NHLDraft2023/">2023 Draft Tool</a>, created by Pranshanth Iyer and myself, can be used by NHL organizations to inform their decision-making process. Let's take the Montreal Canadiens as an example.
</p>
<p>
The Canadiens pick fifth, which, according to consensus, is just outside the top tiers of prospects consisting of Connor Bedard, Adam Fantilli, Matvei Mitchkov, and Leo Carlsson. The next "tier", contains a handful of players which ranking publications seem to mostly disagree on. One common question is, if you're the Canadiens, do you trade up to guarantee the drafting of a potential superstar, or do you take the risk and hope one of them slides in the draft? However a more interesting question, in my opinion, is: "How are you making this decision?"
</p>
<p>
The truth is that either way you're leaning, you are making a complex calculation with instinct. You're considering 1) the value of each prospect, 2) the probability of each prospect being available at a given pick, and 3) the appropriate cost in assets to move up in the draft. This is an exceedingly difficult calculation to make in the moment, especially in the heat of the draft. 
</p>
<p>
Thankfully, the probabilities in this tool can help.
</p>
<p>
<h5>Prospect Values</h5>
First, we need the value of the top 5 prospects accoridng to the Canadiens. For this example, let's assume they evaluate prospects based on their predicted Wins Above Replacement (WAR) while their rights are held by the team (7 years), and the predicted WAR of their top five ranked prospects is as follows (feel free to use the metric and values of your choosing):
</p>
<p>
  - Connor Bedard: 24.0
  - Adam Fantilli: 19.0
  - Matvei Mitchkov: 17.5
  - Leo Carlsson: 14.0
  - Will Smith: 10.0
</p>
<p>
<h5>Prospect Pick Probabilities</h5>
Next, we can use our tool to get the probability that each player is still available at each pick. Here they are:
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/draft-probabilities-3-1.png" width="85%" length="125"/></div>
</p>
<p>
<h5>Pick Values</h5>
As the Canadiens, we derive our very own pick values by multiplying the probability a prospect is available at a certain pick by their predicted WAR. Obviously, we're going to take the highest-value player available, so the pick values are calculated like so:
</p>
<p>
1st pick - (1.000*24) = 24.000
2nd pick - (0.002*24) + (0.998*19) = 19.010
3rd pick - (0.000*24) + (0.210*19) + (0.790*17.5) = 17.815
4th pick - (0.000*24) + (0.028*19) + (0.420*17.5) + (0.552*14.0) = 15.610
5th pick - (0.000*24) + (0.002*19) + (0.111*17.5) + (0.269*14.0) + (0.618*10.0) = 11.927
</p>
<p>
Using the third pick as an example:

  - There is a 0% chance Bedard, the Canadiens' highest ranked prospect, is available, so his value is multiplied by 0.
  - There's a 21.0% chance Fantilli, the Canadiens' second-ranked prospect, is available, so his value is multiplied by 0.210.
  - If neither Bedard nor Fantilli is available (79.0% chance), the Canadiens would select Mitchkov, whose value is multiplied by 0.790.
  - In total, the pick is valued at 17.815 WAR.
</p>
<p>
<h5>Previous Work</h5>
Note that this is a departure from the usual draft pick value chart which has long been established in the hockey analytics community (below is an example of the Athletic's) which uses <em>average</em> pick values:</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/draft-probability-3-2.png" width="70%" length="80"/></div>
</p>
<p>
The reason for this proposed departure is that, in practice, there are weak drafts (like last year), and strong drafts (like this year). Even within a draft class, there can be pockets of heterogeneity where talented players are clustered together, as well as instances of significant drops in value. Consequently, for our purposes, it is more appropriate to derive pick values based on the prospects <em>eligible for this year's draft</em>. Moreover, since the historical value chart is well-established, the Canadiens should be trying to leverage it to find value gains.
</p>
<p>
<h5>Decisions, Decisions</h5>
With pick probabilities and prospect values, the Canadiens now have a quantitive framework to determine the value of a pick in the upcoming draft. This allows them to assess the value difference between picks and consider trade scenarios. Which brings us back to the initial question: should the Canadiens consider trading up? 
</p>
<p>
Let's explore this with a hypothetical scenario. Imagine they have the opportunity to trade up to the fourth pick. To gain organizational value, they would need to give up less than the value of the fourth pick (15.610) minus the value of their fifth pick (11.927), which equals 3.683 WAR. If they can trade their fifth plus a piece which is worth less than 3.564 WAR, they've gained value. With this, a complex decision becomes relatively simple, at least in theory.
</p>
<p>
By combining prospect pick probabilities with internal evaluations, the Canadiens can make more informed decisions about their draft strategies and potential trades.
</p>
<p>
<h5>Next Step: Adding Uncertainty</h5>
Arriving at a single point estimate for prospect values can be challenging and may not fully account for the inherent uncertainty surrounding prospects. Different scouts and analysts may have varying evaluations and opinions on a player's potential. Additionally, prospects inherently come with different levels of risk.
</p>
<p>
To address this, we can include uncertainty in this framework by assigning probability distributions to prospect values rather than relying solely on point estimates. By considering the range of potential outcomes and assigning probabilities to different scenarios, a more comprehensive assessment can be made. Perhaps in another post.
</p>
<br>
<script src="https://utteranc.es/client.js"
        repo="spazznolo/spazznolo.github.io"
        issue-term="pathname"
        label="Comment"
        theme="github-dark"
        crossorigin="anonymous"
        async>
</script>