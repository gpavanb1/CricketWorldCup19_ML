from collections import defaultdict
from scraper import definitions
import numpy as np
import pandas as pd


# Generate n-bit string used to encode tournament
# 0 or 1 to indicate whether first or second team
# is the winner
def gen_sample(num_digits):
    return np.random.randint(2, size=(num_digits,))


# Calculates points table given a certain
# sample of the pool stage outcome
# Then, top 4 teams are chosen for semis
# Input is provided as list of binary digits
def gen_semis_teams(pool_binary_list, match_possibility_lol):
    points_tbl = defaultdict(int)
    # Iterate over LoL of matches and add points
    for i, values in enumerate(pool_binary_list):
        points_tbl[match_possibility_lol[i][values]] += 2

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
    tournament_matches = definitions.tournament_data()

    # Get number of remaining matches
    num_matches_left = 0
    for i in tournament_matches:
        if len(i) == 2:
            num_matches_left += 1
    for i in range(num_samples):
        sample_list = gen_sample(num_matches_left)
        finished_matches = np.array([0]*(total_matches - num_matches_left))

        sample_list = np.concatenate((finished_matches, sample_list))
        semis_teams = gen_semis_teams(sample_list, tournament_matches)
        for j in semis_teams:
            prob_table[j] += 1.0/(4.0*num_samples)

    # Sort based on probabilites
    prob_table = zip(prob_table.keys(), prob_table.values())
    prob_table.sort(key=lambda t: t[1], reverse=True)

    # Convert to data frame
    team_names = [e[0] for e in prob_table]
    prob = [e[1] for e in prob_table]
    d = {'Team': team_names, 'Probability': prob}
    return pd.DataFrame(d)