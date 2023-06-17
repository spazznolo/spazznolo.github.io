---
layout: post
title:  "Deriving pick probabilities from NHL draft rankings"
date:   2023-06-16 12:00:00 -0400
---
<h2>Deriving pick probabilities from NHL draft rankings</h2>
<p>
The prospect pick probabilities in the "Draft Pick Probabilities" tab of the <a href="https://piyer97.shinyapps.io/NHLDraft2023/">2023 Draft Stock tool</a> are generated through a process which primarily involves the application of a rank-ordered logit model to draft rankings released throughout the year. The methodology is a simplified version of <a href="https://ecp.ep.liu.se/index.php/linhac/article/view/480">Predicting the NHL Draft with Rank-Ordered Logit Models</a>.
</p>
<p>
There are three main components - first, partial draft rankings are made complete, then a rank-ordered logit model is fit, finally 100,000 drafts are simulated from model outputs. I will describe each component in this thread. Links are provided at the end.
</p>
<p>
<h4>Imputation of partial rankings</h4>
Technically, there are thousands of draft prospects. Consequently, draft rankings cannot include every prospect, and so, by definition, they are partial rankings. They need to be made complete to fit into our framework. We do this by first, restricting the population to prospects ranked in the top 100 by at least one publication. Then, through the <a href="https://cran.r-project.org/web/packages/PLMIX/PLMIX.pdf">PLMIX</a> package in R, rankings are made complete using the frequency of their appearance in rankings as weights.
</p>
<p>
```
## Create full rankings

# Get skater appearance counts
top_skater_freq <- 
  rank_summaries(
    data=ranking_matrix, 
    format_input="ordering", 
    mean_rank=TRUE,
    pc=FALSE) %>%
  .$marginals %>%
  colSums()

# Impute partial rankings to create full ranking matrix
full_ranking_matrix <- 
  make_complete(
    data=ranking_matrix, 
    format_input="ordering", 
    probitems=top_skater_freq) %>%
  .$completedata
```
</p>
<p>
<h4>Fitting of Plackett-Luce models</h4>
As for the rank-ordered logit models, we're currently operating two. The first, a time-weighted frequentist method from the <a href="https://cran.r-project.org/web/packages/PlackettLuce/PlackettLuce.pdf">PlackettLuce</a> package in R; the other, a Bayesian, <a href="https://github.com/tyrelstokes/Monaco_ranking/blob/main/plackett_luce_opt.stan">tier-weighted implementation written in Stan</a> by <a href="https://twitter.com/TyrelStokes">Tyrel Stokes</a>.
</p>
<p>
The time-weighted frequentist implementation is a standard application of the Plackett-Luce, except that ranking lists are weighed based on their distance to the draft in days. The ranking weights were determined using my previous work on user mock drafts. The weights are available <a href="https://github.com/spazznolo/draft-rankings/blob/main/data/weights_for_pl.csv">here</a> for those interested. Using the draft day as the index, rankings published a month out are weighted at roughly 90%, two months at 77%, four months at 50%, and a year at 17%. 
</p>
<p>
```
## Build Plackett-Luce model

# Fit the Plackett-Luce model
pl_model <- PlackettLuce(full_ranking_matrix, weights = weights, npseudo = 0.1, maxit = c(5000, 100))

# Obtain maximum likelihood estimates from the Plackett-Luce model
mle_estimates <- coef(pl_model, log = FALSE)
```
</p>
<p>
The tier-weighted Bayesian implementation is taken wholesale from Tyrel Stokes' work on <a href="https://github.com/tyrelstokes/Monaco_ranking">track racing</a>. His implementation contains weights, however they are determined by the Bayesian framework, which was not written with time, but tier importance + noise in mind.
</p>
<p>
<h4>Simulation of drafts</h4>
These rank-ordered logit models attribute a "strength" score to each player. Drafts are simulated (100k times) by randomly drawing (without replacement) players using their strength score as weights.
</p>
<p>
```
# Simulate draft rankings
draft_simulations <- replicate(100000, sample(1:skaters, skaters, replace = FALSE, prob = mle_estimates)
```
</p>
<p>
<h4>Assumptions</h4>
There are three main assumptions which don't quite fit in this methodology. The first is that the rankings are truly full rankings (they are not). The second is that draft rankings aren't related over time (they are). The third is that ranking publications are representative of NHL organizations (unsure, could be verified with historical data). We explain each below.
</p>
<p>
<h5>On "Full" Rankings</h5>
In an ideal scenario, full rankings would encompass every eligible prospect in each ranking, providing a comprehensive view. However, this is impractical in reality. The challenge lies in incorporating partial rankings into a complete ranking system. One approach is to establish a cut-off point for the number of players included in the rankings. In my opinion, a suitable cut-off would be to limit the rankings to the top 100 prospects. If a publication ranks more than 100 prospects (e.g., 150 or 250), we disregard prospects ranked 101 and beyond. This approach minimizes information loss since only a few publications extend their rankings beyond 100. By focusing on the players within this new set, we are left with approximately 200+ prospects and growing. However, it's important to note that the current model does not acknowledge the existence of other prospects outside this set. Consequently, the model assigns a 0% probability to a prospect ranked 250 being drafted within the top 100. As a result, the estimated probability of the 200+ prospects being drafted becomes overestimated. This issue becomes increasingly problematic as the draft progresses, and the model's effectiveness is limited after the first two rounds. One potential way to address this is by adjusting for historical undercoverage, but unfortunately, we lack the necessary data for such adjustments.
</p>
<p>
<h5>On Time</h5>
To simplify the model, time was included through weights. Essentially, we are flattening time by saying "a ranking published right before the draft is worth about twice as much as a ranking published four months ago". Even though this works for prediction, it is not actually how the dynamic works. The reason rankings change is <em>not</em> because of time, but because of <em>what prospects/scouts do during this time</em>. This assumption is addressed in <em>Predicting the NHL Draft with Rank-Ordered Logit Models</em>, linked above.
</p>
<p>
<h5>On Selection Bias</h5>
The method employed in this model assumes that prospect ranking publications represent the perspectives of NHL organizations. By "representative," we mean that these publications assign similar value to players and exhibit comparable variance in their evaluations. For instance, it is plausible that ranking publications lack the same level of resources as professional hockey teams, leading them to rely predominantly on data rather than in-game observations. Consequently, they may place greater emphasis on prospects who excel in ways which are represented in game logs. Any inherent "bias" present in these publication rankings would consequently influence the published pick probabilities in this model.
</p>
<p>
<h5>Links</h5>
The code used to generate these probabilities is available on GitHub <a href="https://github.com/spazznolo/draft-rankings">here</a>.
</p>