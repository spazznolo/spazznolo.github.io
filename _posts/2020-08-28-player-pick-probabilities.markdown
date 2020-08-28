---
layout: post
title:  "Assigning Player-Pick Probabilities with User Generated Data"
date:   2020-08-28 11:52:05 -0400
---


<h5>INTRODUCTION</h5>
<br>
If you’re picking first at the next NHL draft, you want Lafreniere. If you’re picking second or third, you want Byfield or Stutzle. If you’re picking fourth, or fifth, or sixth, or seventh, you’re picking Rossi or Perffeti, or Raymond, or Drysdale… Notice how the list lengthens as you make your way through the draft? That’s because the uncertainty of a player being better than all other available players increases the deeper you get into the draft. So maybe you really like Rossi, but you’re picking sixth, and you want to know what the odds of him being available are so you can be prepared to either trade up or take someone else. Well, what are the odds Rossi is still available at six? It’s hard to say.
<br>
Let’s say we only have our own rankings to go on. Instead of only predicting each player’s draft position, we could create probabilities of each prospect being drafted at each pick. Let’s use Rossi again as an example. Here’s how we might place probabilities on Rossi’s draft result:
<br>
<img src="https://spazznolo.github.io/figs/first-plot.png"  alt="centered image" style="width: 500px; length: 500px;"/>
<br>
This is a probability distribution of Rossi’s predicted draft result. Though this is a step in the right direction, these are only our predictions of where Rossi might go. What if the teams drafting ahead of us think he’s not as good as we think he is? Well, then their probability distribution for Rossi might look like this:
<br>
<img src="https://spazznolo.github.io/figs/second-plot.png"  alt="centered image" style="width: 500px; length: 500px;"/>
<br>
If the teams ahead of us view Rossi closer to the plot above, then he’ll likely slide lower than we predicted he would, and our chances of drafting him are higher than we previously thought. In fact, if we knew what other teams thought of him, we could pretty accurately predict where he’ll still be available in the draft, which allows us to either a) be comfortable we have a strong chance of picking him without trading up, or b) slide down a couple spots, pick up a mid-round pick and still get him. An important thing to remember is that Rossi’s draft position is much less affected by how we think of him than it is by how everyone else thinks of him. Namita Nandakumar wrote about the value of knowing where players will likely get drafted in this article.
<br>
In practice, no team will ever know exactly how every other team has ranked each prospect. Instead, player-pick probability distributions need to be approximated by other means. DTM About Heart outlined one way of doing this for Hockey-Graphs which used bayesian inference and pro rankings publishers. I’m going to outline another possible way, which uses user generated data to derive probability density functions for each player. 
<br>
The goal of this paper is to assign probabilities to questions like the one in the first paragraph: what is the probability a player is still available at a certain pick?
<br>
## THE DATA
<br>
# User Mock Drafts
<br>
Over the years, as player data has become more widely available, mock drafts have increased in popularity. In a mock draft, the creator tries to predict where a player will get picked in the upcoming draft. One site in particular, Draft Site, gets hundreds of user mock drafts each year. These mock drafts naturally create probability distributions for each player’s potential pick placement. For example, here was Mikko Rantanen’s in 2015.
<br>
<img src="https://spazznolo.github.io/figs/third-plot.png"  alt="centered image" style="width: 500px; length: 500px;"/>
<br>
To create the plot above, equal weight was given to each user’s mock draft, regardless of its quality. In practice, some users are more knowledgable than others. A user who can more correctly predict a draft’s order is more valuable than one who cannot. Therefore, larger weights should be given to users who are likely more accurate in their mock draft. Thankfully, there are a couple quality indicators available: a user’s difference to the average user draft, and the number of days before the draft date that a user last updated their mock draft. 
<br>
# Quality Indicators
<br>
# 1. Difference to the Average Draft
<br>
Mikko Rantanen’s median pick from the raw user data was 9. If a user selected him 25th, they would be 16 spots off. A user’s absolute error rate can be computed for each pick in their mock draft. Below is the relationship of users’ mean absolute pick difference and their mean absolute pick error to the actual draft from 2015-2019. There’s a strong relationship between the two.
<br>
<img src="https://spazznolo.github.io/figs/fourth-plot.png"  alt="centered image" style="width: 500px; length: 500px;"/>
<br>
# 2. Days to the Draft
<br>
Usually, ranking publications will release a preliminary rankings list about a year before the draft. Then, as the draft approaches and player’s develop – or don’t -  the rankings are updated. The plot below demonstrates that user data becomes more accurate as the draft day approaches.
<br>
<img src="https://spazznolo.github.io/figs/fifth-plot.png"  alt="centered image" style="width: 500px; length: 500px;"/>
<br>
The variables discussed above were used to (1) filter what are likely low quality drafts and (2) create weights for each user mock draft. Players’ adjusted pick probabilities were then fitted and dampened. More information on these decisions is available in the Analysis Notes section.

            ​ Comparing Probability Distributions

                ​ The Effect of Treatments on Player-Pick Probability Distributions

Here’s a visualization of the effects various treatments have on the user rankings. (add third step)
<br>
The downside to user mock drafts is that prospect ranking is likely a hobby for most users. They may mostly rely on second hand information provided by hockey sites, experts, and prospect ranking models. Before going further, it’s important to measure its capacity for prediction. One way of doing this is to build a draft ranking from the data, and then measure its accuracy against professional ranking publishers.
<br>
# Derived User Rankings vs the Pros
<br>
Draft rankings are derived from player-pick probability distributions by iterating through each pick of each draft, and drafting the player with the highest probability of being taken. After each pick, the player distributions are re-approximated (more information is available in the Analysis Notes section).
<br>
Here is the mean absolute error of derived user draft rankings from 2015-2019 compared to various pro ranking publications. All experts but Bobby Mackenzie, the gold standard of draft rankings, have been greyed out. Purple is the group average.
<br>
user_raw: raw user mock drafts
user_internal_weights: filtered, weighted, fitted and dampened user mock drafts
user_external_weights: filters, weighted (to pro consensus), fitted and dampened user mock drafts
group_average: the average error of pro rankings publishers
<br>
<img src="https://spazznolo.github.io/figs/seventh-plot.png"  alt="centered image" style="width: 500px; length: 500px;"/>
<br>
Rankings derived from raw user data are below average and tend to be the worst compared to pro rankings. 
Rankings derived from adjusted user data, weighted to the average user draft, hover around the group average.
Rankings derived from adjusted user data, weighted to a pro consensus, tend to be above average.
<br>
User data, when properly treated, is competitive with pro ranking publications at predicting draft order. The advantage is that user data has built-in player-pick distributions which can be used to answer important questions about the draft.
<br>
## ANALYSIS
<br>
# Another Perspective on Probability Distributions
<br>
Here’s the probability Mikko Rantanen had of being selected at specific picks: 1, 0.1%; 2, 1.0%; 3, 2.6%; 4, 4.6%; 5, 7.9%. Another way to look at this is to say the probability Mikko Rantanen would be selected in the first five picks was 16.3% (the addition of each pick probability for picks 1-5). These cumulative probabilities can be calculated for each pick. Here’s what this looks like on a plot.
<br>
<img src="https://spazznolo.github.io/figs/eigth-plot.png"  alt="centered image" width=textWidth height="200"/>
<br>
This is called a cumulative distribution (each pick takes the cumulative sum of all previous pick-probabilities). A pick-probability curve like the one visualized above can be derived for each player. Given that these cumulative pick-probabilities are the cornerstone of the analysis, it’s important to measure their accuracy. The fit of these curves can be evaluated by going through each pick and asking the questions: what was the probability of this player being drafted by this pick and was he drafted by this pick?
<br>
# Evaluating the Fit
<br>
Either a player was drafted by a certain pick, or they weren’t. This is called a binary event, with values 0 (he wasn’t) and 1 (he was). Mikko Rantanen had a 55.5% probability of being drafted by the eighth pick, and the result was that he wasn’t yet picked (0). The error for the probability attributed to this event can be seen as 0.555-0 = 0.555. Rantanen also had an 86.4% probability of being drafted by the twelfth pick, and the result was that he was picked (1). The error for the probability attributed to this event can be seen as 0.864-1 = -0.136. 
<br>
Each player has probabilities attached for the first thirty picks of the draft. This is roughly 7,000 events. Errors can be attributed for these events the same way as they were outlined in the previous paragraph. Glenn Brier suggested a way of evaluating the goodness-of-fit of events like these by summing the squared error of all events. Brier scores for each method are posted in the plot on the next page. 
<br>
The fit can also be assessed by grouping the predicted probabilities into bins and then visualizing them against the observed percentage of time the positive outcomes occur. Here’s an example:
<br>
The table below has 10 events which have probability between 30% and 40%. Ideally, the percent of time a player is picked by this event is also between 30-40%. In this example, the average probability is in the mid 30%s, and 30% of events had positive outcomes (player was picked). 
<br>
Grouping the data into many bins, calculating the predicted vs observed occurrences (like above) and then visualizing the predicted vs observed probabilities is called a calibration plot. It answers the question: when we give events a given probability of occurring, what percentage of the time do they actually occur? The calibration plot is plotted below along with Brier scores.
<br>
The perfect fit is the grey line, where outcomes occur the predicted percentage of time. Whenever a curve slides away underneath the line of perfect fit, like it does with the raw user data (and to a lesser extent the adjusted user data), it means the method tends to be overconfident in its assignment of probabilities. The plot above, along with the Brier scores, suggest the adjusted user data (score ~ 0.081) is a better fit than raw user data (score ~ 0.196).
<br>
# NEXT STEPS
<br>
Regardless of one’s methods for developing player-pick probability distributions, on draft day low-likelihood events will nearly always occur. Some examples in recent drafts: Barrett Hayton was selected with the 5th pick in the 2018 draft. He was ranked 13th and had a 4.7% probability of being selected that early. Gabe Vilardi was selected with the 11th pick of the 2017 draft. He was ranked 3rd and had a 5.2% probability of sliding at least that late.
<br>
Question: How do the probability distributions of the remaining players change now that either (1) a player was selected earlier than we thought he would or (2) a highly ranked player is sliding past where we though he would? I’ve yet to think of a way of doing this which I’m satisfied with, but I’ll lay out my thoughts so far.
<br>
# Dynamic Player-Pick Probabilities
<br>
In the 2018 draft, two players were considered possibilities for the first overall pick: Nico Hischier (~60%) and Nolan Patrick (~40%). The probabilities for the second overall pick were: Patrick (40%), Hischier (36%), with Heiskanen and Vilardi sharing much of the rest. After Hischier is selected first overall, Patrick’s ~40% probability of getting drafted first overall needs to be distributed across other picks. One way of doing this is to distribute this probability proportionally across Patrick’s remaining probability distribution. Here’s what that would look like. 
<br>
Patrick’s pick probabilities go from 40.5%, 50.5% and 8.5% (picks 1,2 and 3 respectively) before the draft, to 0%, 82.5% and 16% after Hischier is drafted first overall. 
<br>
The problem here is that, after shifting each player’s pick probabilities from the first overall pick to other picks across their pick-probability distributions, the total probability of all players being selected second overall does not sum to 100%. To fix this, player-pick probabilities are recalibrated by dividing each player’s probability by the sum of the pick probability. These operations are repeated until calibrations are as desired. This comes at the expense of distortions to player-pick probability distributions. 
<br>
Though this method is admittedly sub-optimal, it does naturally shrink a player’s probability of getting drafted in the first 30 picks as they slide in the draft. An example of how this looks in practice is Arthur Kaliyev, who was ranked 15th in the 2019 draft, but slid into the second round. Here’s how his probability of being drafted in the first thirty picks changes as he slides down the draft.
The next step will be to look for better ways to redistribute player pick probabilities after they expire, as this has interesting use cases. For example, it can answer the question: what was the probability Mikko Rantanen had of being select 11th, given everything that happened in the draft before then? Or, more useful, what is the probability Marco Rossi is drafted by the sixth pick, given Lafreniere, Byfield and Stutzle are picked 1-3 vs if one of the three slip?
<br>
# Evaluating the Fit of Dynamic Player-Pick Distributions
<br>
# Back to the Marco Rossi Example
<br>
Question: What is the probability Marco Rossi is drafted by the sixth pick, given Lafreniere, Byfield and Stutzle are picked 1-3 vs if one of the three slip?
<br>
The current consensus ranking for the top three picks of the 2020 draft is: Lafreniere, Byfield, and Stutzle. If the Senators reach for another player on the third pick, what happens to Rossi’s probability of still being available sixth? To run this simulation, Alex Holtz was used as the reach for the third pick. Rossi’s probability of being taken by the sixth pick drops nearly 10% because of this.
<br>
# ANALYSIS NOTES
<br>
# Filtering Users
<br>
Filters for adjusted data weighted to user average: RMSE to user average < 15, days to draft < 150
Filters for adjusted data weighted to pro consensus: RMSE to pro consensus < 10, days to draft < 150
<br>
# Attributing Weights to Users
<br>
A linear regression is fit using: RMSE to user average, days to draft, (and RMSE to pro consensus for data weighted to pro consensus) as predictors and RMSE to actual draft order as target. 
User weights are the inverse of the linear model predicted RMSE of user ranking to the actual draft order.
<br>
# Fitting Player Distributions
<br>
A gamma distribution is fitted to adjusted data.
<br>
# Dampening Player Distributions
<br>
Talk about ‘makeshift prior’ and how the deviation created by it is better than that of the raw data because it is observed deviation vs likely bad user predictions. 




