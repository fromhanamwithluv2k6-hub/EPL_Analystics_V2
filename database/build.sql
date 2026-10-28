CREATE TABLE Teams(

team_Id INT,
team VARCHAR(50),
short_Name CHAR(3),
founded INT,
home_Stadium VARCHAR(50),
logo_Url VARCHAR(255),
PRIMARY KEY(short_Name)

);
CREATE TABLE Standings(

team_Id INT,
pos INT,
team VARCHAR(50),
short_Name CHAR(3),
played INT,
won INT,
draw INT,
lost INT,
goals_For INT,
goals_Against INT,
points INT,
PRIMARY KEY(short_Name),
FOREIGN KEY (short_Name) REFERENCES Teams(short_Name)

);
CREATE TABLE Schedule(
date VARCHAR(100),
game_Id INT,
home_Team CHAR(3),
home_Goals INT,
away_Goals INT,
away_Team CHAR(3),
is_result VARCHAR(5),

PRIMARY KEY(game_Id),
FOREIGN KEY(home_Team) REFERENCES Teams(short_Name),
FOREIGN KEY(away_Team) REFERENCES Teams(short_Name)
);
CREATE TABLE Match_stat(
game_Id INT,
home_Team CHAR(3),
away_Team CHAR(3),
home_points INT,
home_Xp FLOAT,
home_Goals INT,
home_Xg FLOAT,
home_Ppda FLOAT,
home_Deep_completions INT,
away_Points INT,
away_xP FLOAT,
away_Goals INT,
away_Xg FLOAT,
away_Ppda FLOAT,
away_deep_completions INT,
PRIMARY KEY(game_Id),
FOREIGN KEY(game_Id) REFERENCES Schedule(game_Id)
);
CREATE TABLE Player_profile(

player_Id INT,
player VARCHAR(50),
team CHAR(3),
pos CHAR(2),
photo_url VARCHAR(255),
PRIMARY KEY(player_Id),
FOREIGN KEY(team) REFERENCES Teams(short_Name)

);
CREATE TABLE Player_stat(
player_Id INT,
player VARCHAR(50),
pos CHAR(2),
starts INT,
minutes INT,
yellow_Cards INT,
red_Cards INT,
og INT,
pen_Missed INT,
goals INT,
xG FLOAT,
assists INT,
xA FLOAT,
xGI FLOAT,
clean_Sheets INT,
goals_Conceded INT,
xGC FLOAT,
cbi INT,
recoveries INT,
tackles INT,
defensive_Contribution INT,
influence_Rank INT,
creativity FLOAT,
creativity_Rank INT,
threat INT,
threat_Rank INT,
ict_index_rank INT,
PRIMARY KEY(player_Id),
FOREIGN KEY(player_Id) REFERENCES Player_profile(player_Id)
);