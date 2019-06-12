from collections import defaultdict
from scraper import support
import numpy as np
import pandas as pd


# Generate list of uniform percentages
# Depending on whether it is greater than
# or equal to one team's percentage, the winner
# is decided for the instance
def gen_sample(num_matches):
    return np.random.randint(100, size=(num_matches,))


# Calculates points table given a certain
# sample of the pool stage outcome
# Then, top 4 teams are chosen for semis
# Input is provided as list of numbers, each
# between 0 and 100 representing the random number
def gen_semis_teams(pool_prob_list, tournament_odds, tournament_data):
    points_tbl = defaultdict(int)
    # Iterate over LoL of matches and add points
    for idx, uniform_number in enumerate(pool_prob_list):
        winner = 0  # Either 0 or 1
        # Decide winner based on match odds
        # Compare with odds of first team
        # to mimic odds probability when using
        # a uniform random number generator
        if uniform_number > tournament_odds[idx][0]:
            winner = 1
        points_tbl[tournament_data[idx][winner]] += 2

    team_names = points_tbl.keys()
    team_points = points_tbl.values()
    top_teams = [team_names for _, team_names in sorted(zip(team_points, team_names), reverse=True)]
    return top_teams[0:4]


# Monte Carlo estimate of the pool stage
# Returns semis qualification probability
# as teams and probabilities dataframe
def gen_pool_stage_prob(num_samples):
    prob_table = defaultdict(float)
    total_matches = 45
    tournament_matches = support.tournament_data()
    tournament_odds = support.tournament_odds()

    # Get number of remaining matches
    num_matches_left = 0
    for i in tournament_matches:
        if len(i) == 2:
            num_matches_left += 1
    for i in range(num_samples):
        sample_list = gen_sample(num_matches_left)
        finished_matches = np.array([0]*(total_matches - num_matches_left))

        sample_list = np.concatenate((finished_matches, sample_list))
        semis_teams = gen_semis_teams(sample_list, tournament_odds, tournament_matches)
        for j in semis_teams:
            prob_table[j] += 1.0/num_samples

    # Sort based on probabilities
    prob_table = zip(prob_table.keys(), prob_table.values())
    prob_table.sort(key=lambda t: t[1], reverse=True)

    # Convert to data frame
    team_names = [e[0] for e in prob_table]
    prob = [e[1] for e in prob_table]
    d = {'Team': team_names, 'Probability': prob}
    return pd.DataFrame(d, columns=['Team', 'Probability'])