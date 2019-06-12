import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import settings
import calendar
from datetime import datetime
import support

team_dtls = []

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


# Invert the abbreviation of a team
def full_name(abbrv):
    return team_abbr.keys()[team_abbr.values().index(abbrv)]


# Replace team name with abbreviation
def sanitize_team(_str):
    for i in team_abbr.keys():
        _str = _str.replace(i, team_abbr[i])
    return _str


# Returns a list-of-list containing
# the two teams
def scrap_tournament_data():
    # Scraping URLs
    base_url = settings.base_url
    page = requests.get(base_url)
    soup = BeautifulSoup(page.text, 'lxml')

    # Get row in table
    match_details_teams = soup.find_all('div', {'class': 'cb-col-100'})
    match_result = {}

    for i in match_details_teams:
        # Team names in match
        match_details_team = i.find('a', {'class': 'text-hvr-underline'})
        if match_details_team:
            if match_details_team.find('span'):
                if i.find('a', {'class': 'cb-text-complete'}):
                    # Winner team is taken from elapsed matches
                    status = [str(sanitize_team(str(i.find('a', {'class': 'cb-text-complete'}).
                              text.split(' won by')[0])))]
                else:
                    # Both teams are part of upcoming matches
                    status = [i_val for i_val in str(sanitize_team(str(match_details_team.find('span')
                              .text.split(',')[0]))).split(' vs ')]

                match_result[str(match_details_team.find('span').text.split(',')[0])] = status

    # Get list of tournament matches
    tournament_matches = []

    for key, value in match_result.items():
        tournament_matches.append(value)

    # Elapsed matches are placed first
    tournament_matches.sort(key=len)
    return tournament_matches


def scrap_tournament_odds():
    match_list = support.tournament_data()
    odds = []
    for match in match_list:
        if len(match) == 2:
            teama = full_name(match[0])
            teamb = full_name(match[1])
            odds.append(func_lst_ten_mtchs(teama, teamb))
        else:
            odds.append([100])
        print "Found odds for: ", match
    return odds


def func_lst_ten_mtchs(teama, teamb):
    last_10_macthes = []

    team_id= team_index(teama)
    for i_yr in range(0,10):
        last_10_macthes_val = 0
        yr = 2019 - i_yr
        main_base_url = 'http://stats.espncricinfo.com/ci/engine/records/team/match_results.html?class=2;id='+str(yr)+';team='+team_id+';type=year'

        page = requests.get(main_base_url)
        soup = BeautifulSoup(page.text,'lxml')
        mtch_dtls_full = soup.find_all('tr',{'class':'data1'})
        mtch_dtls_full_desc = []
        main_lst = []

        for lp in mtch_dtls_full:
            mtch_dtls_full_desc.append(lp.find_all('td',{'nowrap':'nowrap'}))
        for mtch_date_lp in mtch_dtls_full_desc:
            lst=[]
            for mtch_date_lp_2 in mtch_date_lp:
                if ('Jan') in str(mtch_date_lp_2.text) or ('Feb') in str(mtch_date_lp_2.text) or ('Mar') in str(mtch_date_lp_2.text) or ('Apr') in str(mtch_date_lp_2.text) or ('May') in str(mtch_date_lp_2.text) or ('Jun') in str(mtch_date_lp_2.text) or ('Jul') in str(mtch_date_lp_2.text) or ('Aug') in str(mtch_date_lp_2.text) or ('Sep') in str(mtch_date_lp_2.text) or ('Oct') in str(mtch_date_lp_2.text) or ('Nov') in str(mtch_date_lp_2.text) or ('Dec') in str(mtch_date_lp_2.text):
                    lst.append(str(mtch_date_lp_2.text))
                    if len(str(mtch_date_lp_2.text).split(',')[0]) == 5:
                        dt_value = str(mtch_date_lp_2.text).split(',')[0]+','+str(mtch_date_lp_2.text).split(',')[1]
                    else:
                        dt_value = str(mtch_date_lp_2.text).split(',')[0][0:6].replace('-','') +','+ str(mtch_date_lp_2.text).split(',')[1]
                    lst.append(int(calendar.timegm(datetime.strptime(dt_value, '%b %d, %Y').utctimetuple())))
                else:
                    lst.append(str(mtch_date_lp_2.text))
            main_lst.append(lst)

        for k in range(0,len(main_lst)):
            if (((main_lst[k][0] == teama and  main_lst[k][1] == teamb) or (main_lst[k][1] == teama and  main_lst[k][0] == teamb)) and str(main_lst[k][2])!='tied'):
                if len(last_10_macthes)<25:
                    last_10_macthes.append(main_lst[k])
                else:
                    last_10_macthes_val = 1
                    break

        if last_10_macthes_val == 1:
            break

    teama_val = 0
    teamb_val = 0

    # print("last_10_macthes",last_10_macthes)

    def sortMatchdate(val):
        return val[5]

    last_10_macthes.sort(key=sortMatchdate, reverse = True)

    # print("last_10_macthes after sorted", last_10_macthes)

    del last_10_macthes[10:]

    # print("last_10_macthes after sorted and deleted", last_10_macthes)

    for i in range(0,len(last_10_macthes)):
        if last_10_macthes[i][2] == teama:
            teama_val += 1
        elif last_10_macthes[i][2] == teamb:
            teamb_val += 1

    if len(last_10_macthes) != 0:
        return [(float(teama_val)/float(len(last_10_macthes)))*100,(float(teamb_val)/float(len(last_10_macthes)))*100]
    else:
        return [50, 50]

def team_index(team):
    team_lst = 'http://www.espncricinfo.com/story/_/id/18791072/all-cricket-teams-index'
    team_ind = requests.get(team_lst)
    soup_team = BeautifulSoup(team_ind.text,'lxml')

    tm_dtls = soup_team.find_all('div',{'class':'article-body'})
    for i in tm_dtls:
        tm_dtls_desc = i.find_all('p')

    for j in tm_dtls_desc:
        if j.find('a'):
            team_dtls.append([str(j.find('a').attrs['href'].split('/')[4]),str(j.text)])

    for val in team_dtls:
        if val[1] == team:
            return(val[0])
