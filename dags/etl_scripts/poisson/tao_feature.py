
import numpy as np
import pandas as pd
from .config import FEATURES, WINDOW, ELO_K
from .doc_du_lieu import load_clean_data


def avg_last_n(values):
    
    if len(values) == 0:
        return np.nan
    return np.mean(values[-WINDOW:])


def update_elo(elo, home, away, home_goals, away_goals):
   
    expected = 1 / (1 + 10 ** ((elo[away] - elo[home]) / 400))    # xác suất nhà thắng theo Elo
    if home_goals > away_goals:
        actual = 1
    elif home_goals == away_goals:
        actual = 0.5
    else:
        actual = 0
    elo[home] += ELO_K * (actual - expected)
    elo[away] -= ELO_K * (actual - expected)


def build_features(df):
    
    teams = set(df["home_Team"]) | set(df["away_Team"])
    elo = {t: 1500 for t in teams}              # mọi đội bắt đầu 1500 điểm
    xg_for = {t: [] for t in teams}             # lịch sử xG tạo ra
    xg_against = {t: [] for t in teams}         # lịch sử xG phải chịu

    rows = []
    for _, m in df.iterrows():
        h, a = m["home_Team"], m["away_Team"]

        # 1) feature của trận này, tính từ các trận ĐÃ xảy ra trước đó
        row = {"game_Id": m["game_Id"], "date": m["date"], "home_Team": h, "away_Team": a,
               "is_result": m["is_result"],
               "xG_home": avg_last_n(xg_for[h]), "xGA_home": avg_last_n(xg_against[h]),
               "xG_away": avg_last_n(xg_for[a]), "xGA_away": avg_last_n(xg_against[a]),
               "Elo_diff": (elo[h] - elo[a]) / 100}

        # 2) nếu trận đã đá: lưu kết quả, rồi MỚI cập nhật Elo và lịch sử
        if m["is_result"] == 1:
            hg, ag = int(m["home_Goals"]), int(m["away_Goals"])
            row["home_Goals"], row["away_Goals"] = hg, ag
            row["result"] = 0 if hg > ag else (1 if hg == ag else 2)    # 0 nhà thắng, 1 hòa, 2 khách thắng
            update_elo(elo, h, a, hg, ag)
            xg_for[h].append(m["home_Xg"]);  xg_against[h].append(m["away_Xg"])
            xg_for[a].append(m["away_Xg"]);  xg_against[a].append(m["home_Xg"])
        rows.append(row)

    data = pd.DataFrame(rows)
    played = data[data["is_result"] == 1].dropna(subset=FEATURES).reset_index(drop=True)  # trận để học
    future = data[data["is_result"] == 0].reset_index(drop=True)                          # trận cần dự đoán
    return played, future


if __name__ == "__main__":
    played, future = build_features(load_clean_data())
    print("Trận để học:", len(played), "| trận cần dự đoán:", len(future))
    print(played[["home_Team", "away_Team"] + FEATURES].head())
    print(future[["home_Team", "away_Team"] + FEATURES].head())
