import pandas as pd
import sqlite3
from pathlib import Path


class update_data():
    def __init__(self):
        self.BASE = Path(__file__).resolve().parent.parent.parent
        self.connection = sqlite3.connect(self.BASE/'database/EPL.db')
        self.cursor = self.connection.cursor()
    def close(self):
        self.connection.close()
    def upsert_teams_table(self):
        df = pd.read_csv(self.BASE/'data/teams.csv')
        rows = df[['Team_id','Team','Short_name','Founded','Home_stadium','Logo_url']].values.tolist()
        self.cursor.executemany("""
        INSERT INTO Teams(team_Id,team,short_Name,founded,home_Stadium,logo_Url)
        VALUES ( ?, ?, ?, ?, ?, ?)
        ON CONFLICT(short_Name) DO UPDATE SET
            team = excluded.team,
            short_Name = excluded.short_Name,
            founded = excluded.founded,
            home_Stadium = excluded.home_Stadium,
            logo_Url = excluded.logo_Url
        """,rows)
        self.connection.commit()
        print("upsert teams finised")
    def upsert_Standings_table(self):   
        df = pd.read_csv(self.BASE/'data/standings.csv')
        rows = df[['Team_id','Position','Team','Short Name','Played'
                   ,'Won','Draw','Lost','Goals For','Goals Against','Points']].values.tolist()
        self.cursor.executemany("""
        INSERT INTO Standings(team_Id,pos,team,short_Name,played,won,draw,lost,
        goals_For,goals_Against,points)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(short_Name) DO UPDATE SET
            pos = excluded.pos,
            team = excluded.team,
            short_Name = excluded.short_Name,
            played = excluded.played,
            won = excluded.won,
            draw = excluded.draw,
            lost = excluded.lost,
            goals_For = excluded.goals_For,
            goals_Against = excluded.goals_Against,
            points = excluded.points
        """,rows)
        self.connection.commit()
        print('upsert standings finished')
    def upsert_Schedule_table(self):
        df = pd.read_csv(self.BASE/'data/schedule.csv')
        rows = df[['date','game_id','home_team_code','home_goals',
                   'away_goals','away_team_code','is_result']].values.tolist()
        self.cursor.executemany("""
        INSERT INTO Schedule(date,game_Id,home_Team,home_Goals,away_Goals,away_Team,is_result)
        VALUES(?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(game_Id) DO UPDATE SET
            date = excluded.date,
            home_Team = excluded.home_Team,
            home_Goals = excluded.home_Goals,
            away_Goals = excluded.away_Goals,
            away_Team = excluded.away_Team,
            is_result = excluded.is_result
        """,rows)
        self.connection.commit()
        print('upsert Schedule finished')      
    def upsert_Match_stat_table(self):
        df = pd.read_csv(self.BASE/'data/match_stat.csv')
        rows = df[['game_id','home_team_code','away_team_code','home_points',
                   'home_expected_points','home_goals','home_xg','home_ppda',
                   'home_deep_completions','away_points','away_expected_points',
                   'away_goals','away_xg','away_ppda','away_expected_points']].values.tolist()
        self.cursor.executemany("""
        INSERT INTO Match_stat(game_Id,home_Team,away_Team,home_points,home_Xp,home_Goals,
        home_Xg,home_Ppda,home_Deep_completions,away_Points,away_xP,away_Goals,away_Xg,away_Ppda,away_deep_completions)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(game_Id) DO UPDATE SET
            home_Team = excluded.home_Team,
            away_Team = excluded.away_Team,
            home_points = excluded.home_points,
            home_Xp = excluded.home_Xp,
            home_Goals = excluded.home_Goals,
            home_Xg = excluded.home_Xg,
            home_Ppda = excluded.home_Ppda,
            home_Deep_completions = excluded.home_Deep_completions,
            away_Points = excluded.away_Points,
            away_xP = excluded.away_xP,
            away_Goals = excluded.away_Goals,
            away_Xg = excluded.away_Xg,
            away_Ppda = excluded.away_Ppda,
            away_deep_completions = excluded.away_deep_completions
        """,rows)
        self.connection.commit()
        print('upsert Match_stat finished')
    def upsert_Player_profile_table(self):
        df = pd.read_csv(self.BASE/'data/players_profile.csv')
        rows = df[['player_id','player','team','pos','photo_url']].values.tolist()
        self.cursor.executemany("""
        INSERT INTO Player_profile(player_Id,player,team,pos,photo_url)
        VALUES ( ?, ?, ?, ?, ?)
        ON CONFLICT(player_Id) DO UPDATE SET
            player = excluded.player,
            team = excluded.team,
            pos = excluded.pos,
            photo_url = excluded.photo_url
        """,rows)
        self.connection.commit()
        print("upsert player_profile finised")
    def upsert_Player_stat_table(self):
        df = pd.read_csv(self.BASE/'data/players_stat.csv')
        rows = df[['player_id','player','pos','starts','minutes','yellow_cards','red_cards',
                   'og','pen_missed','goals','xG','assists','xA','xGI','clean_sheets','goals_conceded',
                   'xGC','CBI','recoveries','tackles','defensive_contribution','influence_rank','creativity','creativity_rank',
                   'threat','threat_rank','ict_index_rank']].values.tolist()
        self.cursor.executemany("""
        INSERT INTO Player_stat(player_Id,player,pos,starts,minutes,yellow_Cards ,red_Cards ,og ,pen_Missed ,
        goals ,xG ,assists ,xA ,xGI ,clean_Sheets ,goals_Conceded ,xGC ,cbi ,recoveries ,tackles ,
        defensive_Contribution ,influence_Rank ,creativity ,creativity_Rank ,threat ,threat_Rank ,ict_index_rank)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        ON CONFLICT(player_Id) DO UPDATE SET
            player_Id = excluded.player_Id,
            player = excluded.player,
            pos = excluded.pos,
            starts = excluded.starts,
            minutes = excluded.minutes,
            yellow_Cards = excluded.yellow_Cards,
            red_Cards = excluded.red_Cards,
            og = excluded.og,
            pen_Missed = excluded.pen_Missed,
            goals = excluded.goals,
            xG = excluded.xG,
            assists = excluded.assists,
            xA = excluded.xA,
            xGI = excluded.xGI,
            clean_Sheets = excluded.clean_Sheets,
            goals_Conceded = excluded.goals_Conceded,
            xGC = excluded.xGC,
            cbi = excluded.cbi,
            recoveries = excluded.recoveries,
            tackles = excluded.tackles,
            defensive_Contribution = excluded.defensive_Contribution,
            influence_Rank = excluded.influence_Rank,
            creativity = excluded.creativity,
            creativity_Rank = excluded.creativity_Rank,
            threat = excluded.threat,
            threat_Rank = excluded.threat_Rank,
            ict_index_rank = excluded.ict_index_rank
        """,rows)
        self.connection.commit()
        print('upsert player_stat finished')
    def upsert_predictions_table(self):
        df = pd.read_csv(self.BASE/'data/predictions.csv')
        rows = df[['match_id','home_team','away_team','prob_home_win',
                   'prob_draw','prob_away_win']].values.tolist()
        self.cursor.executemany("""
        INSERT INTO Predictions(game_Id,home_Team,away_Team,prob_Home_win,
        prob_Draw,prob_Away_win) VALUES(?,?,?,?,?,?)
        ON CONFLICT(game_Id) DO UPDATE SET
            home_Team = excluded.home_Team,
            away_Team = excluded.away_Team,
            prob_Home_win = excluded.prob_Home_win,
            prob_Draw = excluded.prob_Draw,
            prob_Away_win = excluded.prob_Away_win
        """,rows)
        print('upsert predictions finished')
        self.connection.commit()
    def upsert_all(self):
        self.upsert_teams_table()
        self.upsert_Standings_table()
        self.upsert_Schedule_table()
        self.upsert_Match_stat_table()
        self.upsert_Player_profile_table()
        self.upsert_Player_stat_table()
        print("done")
        self.connection.close()
    def close_connection(self):
        self.connection.close()