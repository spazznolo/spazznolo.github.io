---
layout: post
title:  "Deriving pick probabilities from NHL draft rankings"
date:   2023-06-16 8:52:05 -0400
---
<p>
<h2>Deriving pick probabilities from NHL draft rankings</h2>
The probabilities are generated through a process which primarily involves the application of a rank-ordered logit model to draft rankings released throughout the year. The methodology is a simplified version of "Predicting the NHL Draft with Rank-Ordered Logit Models".
</p>
<p>
There are three main components - first, partial draft rankings are made complete, then a rank-ordered logit model is fit, finally 100,000 drafts are simulated from model outputs. I will describe each component in this thread. Links are provided at the end.
</p>
<p>
<h5>Imputation of partial rankings</h5>
Technically, there are thousands of draft prospects. Consequently, draft rankings cannot include every prospect, and so, by definition, they are partial rankings. They need to be made complete to fit into our framework. Here's how we do it...
</p>
<p>
First, we restrict the population to prospects ranked in the top 100 by at least one publication. Then, through the PLMIX package in R, rankings are made complete using the frequency of their appearance in rankings as weights.
</p>
<p>
<h5>Fitting of Plackett-Luce models</h5>
As for the rank-ordered logit models, we're currently operating two. The first, a time-weighted frequentist method from the PlackettLuce package in R; the other, a Bayesian, tier-weighted implementation written in Stan by @TyrelStokes...
</p>
<p>
The time-weighted frequentist implementation is a standard application of the Plackett-Luce, except that ranking lists are weighed based on their distance to the draft in days. The ranking weights were determined using my previous work on user mock drafts, and are linked at the end.
</p>
<p>
Here's a plot of user mock draft error against the distance to the draft in days. For example, using the draft day as the index, rankings published a month out are weighted at roughly 90%, two months at 77%, four months at 50%, and a year at 17%.
</p>
<p>
The tier-weighted Bayesian implementation is taken wholesale from @TyrelStokes' work on track racing. His implementation contains weights, however they are determined by the Bayesian framework, which was not written with time, but tier importance + noise in mind.
</p>
<p>
<h5>Simulation of drafts</h5>
These rank-ordered logit models attribute a "strength" score to each player. Drafts are simulated (100k times) by randomly drawing (without replacement) players using their strength score as weights.
</p>
Assumptions

Links
draft tool: https://piyer97.shinyapps.io/NHLDraft2023/
article: https://ecp.ep.liu.se/index.php/linhac/article/view/480
weights: https://github.com/spazznolo/draft-rankings/blob/main/data/weights_for_pl.csv
Stokes stan script: https://github.com/tyrelstokes/Monaco_ranking/blob/main/plackett_luce_opt.stan
project repo: https://github.com/spazznolo/draft-rankings