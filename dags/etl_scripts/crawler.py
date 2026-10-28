import requests
import pandas as pd
from pathlib import Path
from soccerdata import Understat

class PLdataUpdate():
    def __init__(self): 
        self.BASE = Path(__file__).resolve().parent.parent.parent
        self.FPL_url = "https://fantasy.premierleague.com/api/bootstrap-static/"
        self.understat = Understat(leagues="ENG-Premier League", seasons="2026/2027",no_cache = True)

        self.response = requests.get(self.FPL_url)
        self.data = self.response.json()
        self.FIX_CODE = {"BRI": "BHA", "FLH": "FUL", "LED": "LEE"}
        with open('/run/secrets/api_key','r',encoding = 'utf-8') as f:
            self.API_KEY = f.readline()

    def update_standings(self):
        url = "https://api.football-data.org/v4/competitions/PL/standings"
        headers = {"X-Auth-Token": self.API_KEY}
        local_response = requests.get(url, headers=headers)

        if local_response.status_code == 200:
            file_csv = self.BASE/'data/standings.csv'
            df_cur = pd.read_csv(file_csv)
            df_cur.iloc[0:0].to_csv(file_csv,index = False,encoding = 'utf-8')
            data = local_response.json()
            teams = data["standings"][0]["table"]
            team_names = sorted(t["team"]["tla"] for t in teams)
            team_ids = {name: team_id for team_id, name in enumerate(team_names, start=1)}
            df = pd.DataFrame([{
                "Team_id" : team_ids[t["team"]["tla"]],
                "Position": t["position"],
                "Team": t["team"]["name"],
                "Short Name": t["team"]["tla"],
                "Played": t["playedGames"],
                "Won": t["won"],
                "Draw": t["draw"],
                "Lost": t["lost"],
                "Goals For": t["goalsFor"],
                "Goals Against": t["goalsAgainst"],
                "Points": t["points"],
            } for t in teams])
            df.to_csv(file_csv, index=False, encoding="utf-8")
            print('standings updated')
        else:
            print(f'error {local_response.status_code}')
    def update_players_stat(self):
        file_csv = self.BASE/'data/players_stat.csv'
        players = self.data['elements']
        stat_cols = ['id']
        pos_df = ['NONE','GK','DF','MF','FW']
        df_stat = pd.DataFrame([{
            'player_id': p['id'],'player': p['web_name'],'pos' : pos_df[p['element_type']],
            'starts': p['starts'],
            'minutes' :p['minutes'],
            'yellow_cards':p['yellow_cards'],
            'red_cards':p['red_cards'],
            'og' : p['own_goals'],

            'pen_missed' : p['penalties_missed'],
            'goals' : p['goals_scored'],'xG' : p['expected_goals'],
            'assists' : p['assists'],'xA' : p['expected_assists'],
            'xGI' : p['expected_goal_involvements'],

            'clean_sheets' : p['clean_sheets'],
            'goals_conceded' : p['goals_conceded'],'xGC':p['expected_goals_conceded_per_90'],
            'CBI' : p['clearances_blocks_interceptions'],
            'recoveries' : p['recoveries'],
            'tackles' : p['tackles'],
            'defensive_contribution' : p['defensive_contribution'],

            'influence_rank' : p['influence_rank'],
            'creativity' : p['creativity'],'creativity_rank' : p['creativity_rank_type'],
            'threat' : p['threat'],'threat_rank' : p['threat_rank_type'],
            'ict_index_rank' : p['ict_index_rank_type']

        }for p in players])
        
        df_stat.to_csv(file_csv,index=False,encoding='utf-8-sig')
        print('players_stat updated')
    def update_players_profile(self):
        file_csv = self.BASE/'data/players_profile.csv'
        players = self.data['elements']
        teams_map = {t['id']: t['short_name'] for t in self.data['teams']}
        pos_df = ['None','GK','DF','MF','FW']
        df_profile = pd.DataFrame([{
            'player_id':p['id'],
            'player' : f'{p['first_name']} {p['second_name']}',
            'team' : teams_map[p['team']],
            'pos': pos_df[int(p['element_type'])],
            'photo_url'  : f"https://resources.premierleague.com/premierleague/photos/players/110x140/p{p['photo'].replace('.jpg', '.png')}"
        }for p in players])
        df_cur = pd.read_csv(file_csv)
        df_cur.iloc[0:0].to_csv(file_csv,index = False,encoding = 'utf-8-sig')
        df_profile.to_csv(file_csv,index=False,encoding='utf-8-sig')
        print('players_profile updated')
    def update_schedule(self):
        file_csv = self.BASE/'data/schedule.csv'
        df = self.understat.read_schedule()
        if not df.empty:
            df_cur = pd.read_csv(file_csv)
            df_cur.iloc[0:0].to_csv(file_csv,index = False,encoding='utf-8-sig')
            cols = ['date','game_id','home_team_code','home_goals','away_goals','away_team_code','is_result']
            df = df[cols]
            df['home_team_code'] = df['home_team_code'].replace(self.FIX_CODE)
            df['away_team_code'] = df['away_team_code'].replace(self.FIX_CODE)
            df.to_csv(file_csv,index = False,encoding='utf-8-sig')
            print('schedule updated')
        else:
            return print('schedule update failed')
    def update_match_stat(self):
        file_csv = self.BASE/'data/match_stat.csv'
        df = self.understat.read_team_match_stats()
        if not df.empty:
            df_cur = pd.read_csv(file_csv)
            df_cur.iloc[0:0].to_csv(file_csv,index = False,encoding='utf-8-sig')
            cols = ['game_id','home_team_code','away_team_code','home_points',
                        'home_expected_points','home_goals','home_xg','home_ppda',
                        'home_deep_completions','away_points','away_expected_points',
                        'away_goals','away_xg','away_ppda','away_deep_completions']
            df = df[cols]
            df['home_team_code'] = df['home_team_code'].replace(self.FIX_CODE)
            df['away_team_code'] = df['away_team_code'].replace(self.FIX_CODE)
            df.to_csv(file_csv,index=False,encoding='utf-8-sig')
            print('match_stat updated')
        else:
            return print('match_stat update failed')
    def update_teams(self):
        url = "https://api.football-data.org/v4/competitions/PL/teams"
        headers = {"X-Auth-Token": self.API_KEY}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            file_csv = self.BASE/'data/teams.csv'
            data = response.json()
            teams = data["teams"]
            team_names = sorted(t["tla"] for t in teams)
            team_ids = {name: team_id for team_id, name in enumerate(team_names, start=1)}
            df = pd.DataFrame([{
                'Team_id' : team_ids[t['tla']],
                'Team' : t['name'],
                'Short_name' : t['tla'],
                'Founded' : t['founded'],
                'Home_stadium' : t['venue'],
                'Logo_url' : t['crest']
            }for t in teams])
            df_cur = pd.read_csv(file_csv)
            df_cur.iloc[0:0].to_csv(file_csv,index=False,encoding='utf-8-sig')
            df.to_csv(file_csv,index=False,encoding='utf-8-sig')
            print('teams updated')
        else:
            print('teams update failed')
    def update_ALL(self):
        self.update_teams()
        self.update_standings()
        self.update_players_profile()
        self.update_players_stat()
        self.update_schedule()
        self.update_match_stat()