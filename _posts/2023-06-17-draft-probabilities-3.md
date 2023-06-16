---
layout: post
title:  "An Application of Prospect Pick Probabilities"
date:   2023-06-17 12:00:00 -0400
---
<h2>An Application of Prospect Pick Probabilities</h2>
<p>
The prospect pick probabilities available on the "Draft Pick Probabilities" tab of the <a href = "https://piyer97.shinyapps.io/NHLDraft2023/">2023 Draft Tool</a> are of obvious use for entertainment purposes, but I wanted to outline a potential way they can be used by NHL organizations as an input in their decision making process. I'll use the Montreal Canadiens as an example because I personally find them to be in an interesting position.
</p>
<p>
The Canadiens pick fifth, which, depending on who you ask, is just outside the top tiers of prospects consisting of Connor Bedard, Adam Fantilli, Matvei Mitchkov, and Leo Carlsson. The next "tier" contains a handful of players who ranking publications seem to all diagree on. The question is then, if you're the Canadiens, do you trade up to guarantee the drafting of a potential superstar, or do you risk it and hope one of them slides in the draft? Regardless of which way you're leaning, the more interesting question is "How are you making this decision?"
</p>
<p>
The truth is, either way you're leaning, you are making a complex calculation with instinct. You're considering the probability that one of the four players falls, the strength of the next best prospect, and the potential cost in assets to move up in the draft. This is an exceedingly difficult calculation to make in the moment, especially in the heat of the draft. 
</p>
<p>
Thankfully, the probabilities in this tool can help.
</p>
<p>
What every team has going into the draft is their internal prospect ranking. This ranking is derived from prospect values. For the purposes of this example, we're going to create the Canadiens prospect values by assigning quasi-random values to prospects. If you have your own, just plug them into the framework.
</p>
<p>
There is a variety of value frameworks available, but here we're going to use WAR over the entry-level contact. Below are the Canadiens' WAR projections over their entry-level contract for each of their top 5 ranked prospects.
<p>
Connor Bedard: 10
Adam Fantilli: 8
Matvei Mitchkov: 7.5
Leo Carlsson: 6.5
Zach Benson: 5.5
</p>
<p>
Value by pick:
1: 1.00*10 = 10
2: 0.99*8 = 
3: 0.87*7.5 = 
4:
5: 
</p>


<p>
<h5>Next Step: Adding Uncertainty</h5>
Certain prospects are riskier than others. They're often described as having high ceilings and low floors, etc.
We can include uncertainty in this framework by using probability distributions for prospect values instead of point estimates. 
</p>