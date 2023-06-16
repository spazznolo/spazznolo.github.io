---
layout: post
title:  "Deriving pick probabilities from NHL draft rankings"
date:   2023-06-16 12:00:00 -0400
---
<h2>Deriving pick probabilities from NHL draft rankings</h2>
<p>
The prospect pick probabilities in the "Draft Pick Probabilities" tab are generated through a process which primarily involves the application of a rank-ordered logit model to draft rankings released throughout the year. The methodology is a simplified version of <a href="https://ecp.ep.liu.se/index.php/linhac/article/view/480">Predicting the NHL Draft with Rank-Ordered Logit Models</a>, which itself was an extension of xxx. and so on...
</p>
<p>
There are three main components - first, partial draft rankings are made complete, then a rank-ordered logit model is fit, finally 100,000 drafts are simulated from model outputs. I will describe each component in this thread. Links are provided at the end.
</p>
<p>
<h5>Imputation of partial rankings</h5>
Technically, there are thousands of draft prospects. Consequently, draft rankings cannot include every prospect, and so, by definition, they are partial rankings. They need to be made complete to fit into our framework. We do this by first, restricting the population to prospects ranked in the top 100 by at least one publication. Then, through the <a href = "https://cran.r-project.org/web/packages/PLMIX/PLMIX.pdf">PLMIX</a> package in R, rankings are made complete using the frequency of their appearance in rankings as weights.
</p>
<p>
<h5>Fitting of Plackett-Luce models</h5>
As for the rank-ordered logit models, we're currently operating two. The first, a time-weighted frequentist method from the <a href = "https://cran.r-project.org/web/packages/PlackettLuce/PlackettLuce.pdf">PlackettLuce</a> package in R; the other, a Bayesian, <a href = "https://github.com/tyrelstokes/Monaco_ranking/blob/main/plackett_luce_opt.stan">tier-weighted implementation written in Stan</a> by <a href = "https://twitter.com/TyrelStokes">Tyrel Stokes</a>.
</p>
<p>
The time-weighted frequentist implementation is a standard application of the Plackett-Luce, except that ranking lists are weighed based on their distance to the draft in days. The ranking weights were determined using my previous work on user mock drafts. The weights are available <a href = "https://github.com/spazznolo/draft-rankings/blob/main/data/weights_for_pl.csv">here</a> for those interested. Using the draft day as the index, rankings published a month out are weighted at roughly 90%, two months at 77%, four months at 50%, and a year at 17%. 
</p>
<p>
The tier-weighted Bayesian implementation is taken wholesale from Tyrel Stokes' work on <a href = "https://github.com/tyrelstokes/Monaco_ranking">track racing</a>. His implementation contains weights, however they are determined by the Bayesian framework, which was not written with time, but tier importance + noise in mind.
</p>
<p>
<h5>Simulation of drafts</h5>
These rank-ordered logit models attribute a "strength" score to each player. Drafts are simulated (100k times) by randomly drawing (without replacement) players using their strength score as weights.
</p>
<p>
<h5>Assumptions</h5>
There are three main assumptions which don't quite fit in this methodology. The first is that the rankings are truly full rankings (they are not). The second is that draft rankings aren't related over time (they are). The third is that the population ranking publications is representative of NHL organizations (could be verified with historical data). We explain each below.
</p>
<p>
<h6>On "Full" Rankings</h6>
Theoretically, if draft rankings were actually full rankings, every single eligible prospect would be included in each ranking. Though this would be interesting in a vacuum, it's totally infeasible in practice. The question is then "how do we fit partial rankings into full rankings?". One idea is to create a cut-off for the number of players included in the population. To my mind, the best way to create this cut-off is to first clip rankings at 100 prospects (if a publication ranked 150 or 250, we ignore prospects ranked 101+; there isn't very much information loss, only a few publications rank past 100). Then, we <em>only</em> consider players appearing in this new set. We're left with roughly 200+ prospects (and counting) this way. The problem here is the PL model doesn't understand that other prospects exist - it considers the rankings to be full. Therefore, the probability that, say the 250th ranked prospect is drafted in the top 100 is forced to 0%. Consequently, we are <em>overestimating</em> the probability that our 200+ prospects are drafted during each pick. This isn't really a problem for the first round or two, but as the draft progresses it becomes increasingly problematic (I wouldn't expect much signal outside the first two rounds with this method). By the way, this could partly be addressed by adjusting for historical undercoverage, but we don't have that data.
</p>
<p>
On Time
To simplify the model, time was included through weights. Essentially, we are flattening time by saying "a ranking published right before the draft is worth about twice as much as a ranking published four months ago". Even though this works for prediction, it is not actually how the dynamic works. The reason rankings change is <em>not</em> because of time, but because of <em>what prospects/scouts do during this time</em>. This assumption is addressed in <em>Predicting the NHL Draft with Rank-Ordered Logit Models</em>, linked above.
</p>
On Selection Bias
The method necessarily assumes that prospect ranking publications are representative of NHL organizations. By "representative", we mean they value players similarly and experience similar variance in their evaluations. As an example - and this is only an example - let's imagine that ranking publications do not have the same resources as a professional hockey team, causing them to rely mostly on data instead of in-game observation, therefore placing a higher value on prospects who perform in ways which are currently being measured through game logs. The "bias" in these publication rankings would be reflected in the pick probabilities published here.
<p>
<h5>Links</h5>
The code used to generate these probabilities is available on GitHub <a href = "https://github.com/spazznolo/draft-rankings">here</a>.
</p>