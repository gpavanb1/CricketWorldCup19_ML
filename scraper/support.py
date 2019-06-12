from definitions import scrap_tournament_data, scrap_tournament_odds
from os import path
import json


# Return tournament data from file if available
# Else scrap online
def tournament_data():
    if path.exists('tournament_data.txt'):
        dat = read_from_file('tournament_data.txt')
    else:
        print "Scrapping tournament data..."
        dat =  scrap_tournament_data()
        write_to_file(dat, 'tournament_data.txt')
    return dat


# Return tournament data from file if available
# Else scrap online
def tournament_odds():
    if path.exists('tournament_odds.txt'):
        dat = read_from_file('tournament_odds.txt')
    else:
        print "Scrapping tournament odds..."
        dat = scrap_tournament_odds()
        write_to_file(dat, 'tournament_odds.txt')
    return dat


# Read list-of-list from file
def read_from_file(filename):
    with open(filename) as f:
        lst = json.load(f)
    return lst


# Write list-of-list from file
def write_to_file(var, filename):
    with open(filename, "w") as f:
        json.dump(var, f)