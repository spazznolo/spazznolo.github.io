---
layout: post
title:  "An Application of Prospect Pick Probabilities"
date:   2023-06-16 12:00:00 -0400
---
<h2>An Application of Prospect Pick Probabilities</h2>
<p>
The prospect pick probabilities available on the "Draft Pick Probabilities" tab of the <a href = "https://piyer97.shinyapps.io/NHLDraft2023/">2023 Draft Tool</a> made by Pranshanth Iyer and I are of obvious use for entertainment purposes, but I wanted to outline a potential way they can be used by NHL organizations as an input in their decision making process. I'll use the Montreal Canadiens as an example because I personally find them to be in an interesting position.
</p>
<p>
The Canadiens pick fifth, which, according to consensus, is just outside the top tiers of prospects consisting of Connor Bedard, Adam Fantilli, Matvei Mitchkov, and Leo Carlsson. The next "tier", contains a handful of players which ranking publications seem to all disagree on. The question is then, if you're the Canadiens, do you trade up to guarantee the drafting of a potential superstar, or do you risk it and hope one of them slides in the draft? Regardless of which way you're leaning, the more interesting question, in my opinion, is: "How are you making this decision?"
</p>
<p>
The truth is, either way you're leaning, you are making a complex calculation with instinct. You're considering the probability that one of the big four prospects falls, along with the strength of the next best prospect and the potential cost in assets to move up in the draft. This is an exceedingly difficult calculation to make in the moment, especially in the heat of the draft. 
</p>
<p>
Thankfully, the probabilities in this tool can help.
</p>
<p>
The only other piece of information we need are the values assigned by the Canadiens for each of the top five prospects.
</p>
<p>
<h5>Prospect Values</h5>
Going into the draft, every team establishes a ranking based on their internal evaluation of prospects. Although various value frameworks are available, for the purpose of this discussion, let's assume the Canadiens evaluate prospects based on their predicted Wins Above Replacement (WAR) while their rights are held by the team (7 years), and the predicted WAR of their top five ranked prospects is as follows (feel free to use the metric and values of your choosing):
</p>
<p>
  - Connor Bedard: 24.0
  - Adam Fantilli: 19.0
  - Matvei Mitchkov: 17.5
  - Leo Carlsson: 14.0
  - Zach Benson: 10.0
</p>
<p>
<h5>Prospect Pick Probabilities</h5>
Next, we can use our tool to get the probability that each player is still available at each pick. Here they are:
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/draft-probability-3-1.png" width="85%" length="125"/></div>
</p>
<p>
<h5>Pick Values</h5>
The value of each draft pick has long been established in the hockey analytics community. Here's the Athletic's:
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/draft-probability-3-2.png" width="70%" length="80"/></div>
</p>
<p>
It is important to clarify that these values are <em>averages</em>. There are weak drafts (like last year), and strong drafts (like this year). There are also heterogenous pockets, where strong players are clustered together, and there are steep drops in value. Consequently, for our purposes, it is more appropriate to derive pick values based on the prospects <em>eligible for this year's draft</em>. As the Canadiens, we derive pick values by multiplying the probability a prospect is available at a certain pick by their predicted WAR. Obviously, we're going to take the player we value highest, so the pick values are calculated like so:
</p>
<p>
1st pick - (1.000*24) = 24.000
2nd pick - (0.002*24) + (0.998*19) = 19.010
3rd pick - (0.000*24) + (0.215*19) + (0.785*17.5) = 17.823
4th pick - (0.000*24) + (0.029*19) + (0.399*17.5) + (0.572*14.0) = 15.542
5th pick - (0.000*24) + (0.002*19) + (0.105*17.5) + (0.293*14.0) + (0.599*10.0) = 11.978
</p>
<p>
Using the third pick as an example - there is a 0% chance Bedard is available, so his value is multiplied by 0, there is a 21.5% chance Fantilli is available, and since the Canadiens have him ranked as the second best player available, they would draft him if available, so his value is multiplied by 0.2150. That leaves a 78.5% chance that neither Bedard nor Fantilli are available, in which case they select their third ranked player, Mitchkov, so we multiply his value by 0.7850.
</p>
<p>
<h5>Decisions, decisions</h5>
With pick probabilities and prospect values, the Canadiens now have a quantitive framework to determine the value of a pick in the upcoming draft. It follows that they also have the <em>value difference</em> in picks. This brings us back to the initial question: should the Canadiens consider trading down? 
</p>
<p>
Let's explore this by examining a hypothetical scenario where they have the opportunity to trade down to the fourth pick. To gain organizational value, they would need to give up less than the value of the fourth pick (15.542) minus the value of their fifth pick (11.978), which equals 3.564 WAR. With this, a complex decision becomes relatively simple, at least in theory.
</p>
<p>
By combining prospect pick probabilities with internal evaluations, NHL organizations like the Canadiens can make more informed decisions about their draft strategies and potential trade scenarios.
</p>
<p>
<h5>Next Step: Adding Uncertainty</h5>
Certain prospects are riskier than others. They're often described as having high ceilings and low floors.
To account for these differences in riskiness, we can include uncertainty in this framework through the use of probability distributions for prospect values instead of point estimates. Perhaps in another post.
</p>