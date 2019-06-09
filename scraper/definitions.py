import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import settings

# Team abbreviations
team_abbr = defaultdict(str)
team_abbr['New Zealand'] = 'NZ'
team_abbr['Sri Lanka'] = 'SL'
team_abbr['West Indies'] = 'WI'
team_abbr['Bangladesh'] = 'BAN'
team_abbr['England'] = 'ENG'
team_abbr['Afghanistan'] = 'AFG'
team_abbr['Pakistan'] = 'PAK'
team_abbr['Australia'] = 'AUS'
team_abbr['South Africa'] = 'RSA'
team_abbr['India'] = 'IND'


# Replace team name with abbreviation
def sanitize_team(str):
    for i in team_abbr.keys():
        str = str.replace(i, team_abbr[i])
    return str


def tournament_data():
    # Scraping URLs
    base_url = settings.base_url
    page = requests.get(base_url)
    soup = BeautifulSoup(page.text, 'lxml')

    # Get row in table
    match_details_teams = soup.find_all('div',{'class':'cb-col-100'})
    match_result = {}

    for i in match_details_teams:
        # Team names in match
        mtch_dtls_team = i.find('a',{'class':'text-hvr-underline'})
        if mtch_dtls_team:
            if mtch_dtls_team.find('span'):
                if i.find('a',{'class':'cb-text-complete'}):
                    # Winner team is taken from elapsed matches
                    status = [str(sanitize_team(str(i.find('a',{'class':'cb-text-complete'}).\
                             text.split(' won by')[0])))]
                else:
                    # Both teams are part of upcoming matches
                    status = [i_val for i_val in str(sanitize_team(str(mtch_dtls_team.find('span')
                             .text.split(',')[0]))).split(' vs ')]

                match_result[str(mtch_dtls_team.find('span').text.split(',')[0])] = status

    # Get list of tournament matches
    tournament_matches = []

    for key,value in match_result.items():
        tournament_matches.append(value)

    # Elapsed matches are placed first
    tournament_matches.sort(key=len)
    return tournament_matches