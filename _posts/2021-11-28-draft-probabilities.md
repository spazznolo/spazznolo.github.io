---
layout: post
title:  "Assigning pick probabilities with user mock drafts"
date:   2021-11-28 11:52:05 -0400
---

<h5> INTRODUCTION </h5>
If you’re picking first at the next NHL draft, you want Lafreniere. If you’re picking second or third, you want Byfield or Stutzle. If you’re picking fourth, or fifth, or sixth, or seventh, you’re picking Rossi or Perffeti, or Raymond, or Drysdale… Notice how the list lengthens as you make your way through the draft? That’s because the uncertainty of a player being better than all other available players increases the deeper you get into the draft. So maybe you really like Rossi, but you’re picking sixth, and you want to know what the odds of him being available are so you can be prepared to either trade up or take someone else. Well, what are the odds Rossi is still available at six? It’s hard to say.
<p>
Let’s say we only have our own rankings to go on. Instead of only predicting each player’s draft position, we could create probabilities of each prospect being drafted at each pick. Let’s use Rossi again as an example. Here’s how we might place probabilities on Rossi’s draft result:
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/first-plot.png" width="70%" length="200"/></div>
</p>
<p>
This is a probability distribution of Rossi’s predicted draft result. Though this is a step in the right direction, these are only our predictions of where Rossi might go. What if the teams drafting ahead of us think he’s not as good as we think he is? Well, then their probability distribution for Rossi might look like this:
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/second-plot.png" width="70%" length="200"/></div>
</p>
<p>
If the teams ahead of us view Rossi closer to the plot above, then he’ll likely slide lower than we predicted he would, and our chances of drafting him are higher than we previously thought. In fact, if we knew what other teams thought of him, we could pretty accurately predict where he’ll still be available in the draft, which allows us to either a) be comfortable we have a strong chance of picking him without trading up, or b) slide down a couple spots, pick up a mid-round pick and still get him. An important thing to remember is that Rossi’s draft position is much less affected by how we think of him than it is by how everyone else thinks of him. Namita Nandakumar wrote about the value of knowing where players will likely get drafted in <a href="http://statsportsconsulting.com/main/wp-content/uploads/Nandakumar_PerfectDraft-1.pdf">this article</a>.
</p>
<p>
In practice, no team will ever know exactly how every other team has ranked each prospect. Instead, player-pick probability distributions need to be approximated by other means. Dawson Sprigings outlined one way of doing this for <a href="https://hockey-graphs.com/2016/06/08/nhl-draft-probability-tool/">Hockey-Graphs</a> which used bayesian inference and pro rankings publishers. I’m going to outline another possible way, which uses user generated data to derive probability density functions for each player. 
</p>
<p>
The goal of this paper is to assign probabilities to questions like the one in the first paragraph: what is the probability a player is still available at a certain pick?
</p>
<h1> User Mock Drafts </h1>
Over the years, as player data has become more widely available, mock drafts have increased in popularity. In a mock draft, the creator tries to predict where a player will get picked in the upcoming draft. One site in particular, <a href="https://www.draftsite.com/">Draft Site</a>, gets hundreds of user mock drafts each year. These mock drafts naturally create probability distributions for each player’s potential pick placement. For example, here was Mikko Rantanen’s in 2015.
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/third-plot.png" width="70%" length="200"/></div>
</p>
<p>
To create the plot above, equal weight was given to each user’s mock draft, regardless of its quality. In practice, some users are more knowledgable than others. A user who can more correctly predict a draft’s order is more valuable than one who cannot. Therefore, larger weights should be given to users who are likely more accurate in their mock draft. Thankfully, there are a couple quality indicators available: a user’s difference to the average user draft, and the number of days before the draft date that a user last updated their mock draft. 
</p>
<br>
<h5>Mock Draft Quality Indicators</h5>
<h5>Difference to the Average Draft</h5>
Mikko Rantanen’s median pick from the raw user data was 9. If a user selected him 25th, they would be 16 spots off. A user’s absolute error rate can be computed for each pick in their mock draft. Below is the relationship of users’ mean absolute pick difference and their mean absolute pick error to the actual draft from 2015-2019. There’s a strong relationship between the two.
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/fourth-plot.png" width="70%" length="200"/></div>
</p>
<h1>Days to the Draft</h1>
Usually, ranking publications will release a preliminary rankings list about a year before the draft. Then, as the draft approaches and player’s develop – or don’t -  the rankings are updated. The plot below demonstrates that user data becomes more accurate as the draft day approaches.
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/fifth-plot.png" width="70%" length="200"/></div>
</p>
<p>
The variables discussed above were used to (1) filter what are likely low quality drafts and (2) create weights for each user mock draft. Players’ adjusted pick probabilities were then fitted and dampened. More information on these decisions is available in the Analysis Notes section.

<h5>Comparing Probability Distributions</h5>
<h1>The Effect of Treatments on Player-Pick Probability Distributions</h1>
Here’s a visualization of the effects various treatments have on the user rankings.
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/sixth-plot.png" width="70%" length="300"/></div>
</p>
<p>
The downside to user mock drafts is that prospect ranking is likely a hobby for most users. They may mostly rely on second hand information provided by hockey sites, experts, and prospect ranking models. Before going further, it’s important to measure its capacity for prediction. One way of doing this is to build a draft ranking from the data, and then measure its accuracy against professional ranking publishers.
</p>
<h1>Derived User Rankings vs the Pros</h1>
Draft rankings are derived from player-pick probability distributions by iterating through each pick of each draft, and drafting the player with the highest probability of being taken. After each pick, the player distributions are re-approximated (more information is available in the Analysis Notes section).
<p>
Here is the mean absolute error of derived user draft rankings from 2015-2019 compared to various pro projections. All experts but Bobby Mackenzie, the gold standard of draft projections, have been greyed out. It's worth noting that the goal of some professional draft analysts is to predict which players will have the best careers, and not necessarily the order they might be picked. Purple is the group average.
</p>
<p>
user_raw: raw user mock drafts
user_internal_weights: filtered, weighted, fitted and dampened user mock drafts
user_external_weights: filters, weighted (to pro consensus), fitted and dampened user mock drafts
group_average: the average error of pro rankings publishers
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/seventh-plot.png" width="70%" length="200"/></div>
</p>
<p>
Rankings derived from raw user data are below average and tend to be the worst compared to pro rankings. 
Rankings derived from adjusted user data, weighted to the average user draft, hover around the group average.
Rankings derived from adjusted user data, weighted to a pro consensus, tend to be above average.
</p>
<p>
User data, when properly treated, is competitive with pro ranking publications at predicting draft order. The advantage is that user data has built-in player-pick distributions which can be used to answer important questions about the draft.

<h5>Another Perspective on Probability Distributions</h5>
Here’s the probability Mikko Rantanen had of being selected at specific picks: 1, 0.1%; 2, 1.0%; 3, 2.6%; 4, 4.6%; 5, 7.9%. Another way to look at this is to say the probability Mikko Rantanen would be selected in the first five picks was 16.3% (the addition of each pick probability for picks 1-5). These cumulative probabilities can be calculated for each pick. Here’s what this looks like on a plot.
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/eigth-plot.png" width="70%" length="200"/></div>
</p>
<p>
This is called a cumulative distribution (each pick takes the cumulative sum of all previous pick-probabilities). A pick-probability curve like the one visualized above can be derived for each player. Given that these cumulative pick-probabilities are the cornerstone of the analysis, it’s important to measure their accuracy. The fit of these curves can be evaluated by going through each pick and asking the questions: what was the probability of this player being drafted by this pick and was he drafted by this pick?
</p>
<h5>Evaluating the Fit</h5>
Either a player was drafted by a certain pick, or they weren’t. This is called a binary event, with values 0 (he wasn’t) and 1 (he was). Mikko Rantanen had a 55.5% probability of being drafted by the eighth pick, and the result was that he wasn’t yet picked (0). The error for the probability attributed to this event can be seen as 0.555-0 = 0.555. Rantanen also had an 86.4% probability of being drafted by the twelfth pick, and the result was that he was picked (1). The error for the probability attributed to this event can be seen as 0.864-1 = -0.136.
<p>
Each player has probabilities attached for the first thirty picks of the draft. This is roughly 7,000 events. Errors can be attributed for these events the same way as they were outlined in the previous paragraph. Glenn Brier suggested a way of evaluating the goodness-of-fit of events like these by summing the squared error of all events. Brier scores for each method are posted in the plot on the next page. 
</p>
<p>
The fit can also be assessed by grouping the predicted probabilities into bins and then visualizing them against the observed percentage of time the positive outcomes occur. Here’s an example:
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/ninth-plot.png" width="70%" length="600"/></div>
</p>
<p>
The table below has 10 events which have probability between 30% and 40%. Ideally, the percent of time a player is picked by this event is also between 30-40%. In this example, the average probability is in the mid 30%s, and 30% of events had positive outcomes (player was picked). 
</p>
<p>
Grouping the data into many bins, calculating the predicted vs observed occurrences (like above) and then visualizing the predicted vs observed probabilities is called a calibration plot. It answers the question: when we give events a given probability of occurring, what percentage of the time do they actually occur? The calibration plot is plotted below along with Brier scores.
</p>
<p>
<div style="text-align: center"> <img src="https://spazznolo.github.io/figs/tenth-plot.png" width="70%" length="200"/></div>
</p>
<p>
The perfect fit is the grey line, where outcomes occur the predicted percentage of time. Whenever a curve slides away underneath the line of perfect fit, like it does with the raw user data (and to a lesser extent the adjusted user data), it means the method tends to be overconfident in its assignment of probabilities. The plot above, along with the Brier scores, suggest the adjusted user data (score ~ 0.0604) is a better fit than raw user data (score ~ 0.1981).
</p>
<p>
Cumulative player-pick probabilities for the 2020 draft are available <a href="https://drive.google.com/file/d/150JF4tPGQ0fRmMsXonIa5CJ_wVVCXBa9/view?usp=drivesdk">here</a>. 
</p>
<h5>Notes</h5>
<h5>Filtering Users</h5>
Adjusted to User Average:
1. RMSE to user average < 15
2. Days to draft < 150
<p>
Adjusted to Pro Consensus: 
1. RMSE to pro consensus < 10
2. Days to draft < 150
</p>
<h5>Attributing Weights to Users</h5>
<p>
A linear regression is fit using: RMSE to user average, days to draft, (and RMSE to pro consensus for data weighted to pro consensus) as predictors and the RMSE to actual draft order as target. User weights are the inverse of the linear model predicted RMSE of user ranking to the actual draft order.
</p>
<h5>Fitting Player Distributions</h5>
A gamma distribution is fit to adjusted data.
<h5>Dampening Player Distributions</h5>
Player distributions are dampened by the variance observed in prior years. This is superior to the variance in the raw data because, in this case, it is caused by actual deviations as opposed to what are likely bad user predicitons.
<p>
I wrote a similar article for Nylon Calculus which can be found <a href="https://fansided.com/2020/09/17/nba-draft-class-controversial-obi-toppin/">here</a>.
</p>


