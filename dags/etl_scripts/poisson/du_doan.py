
import numpy as np
import pandas as pd
from .config import OUTPUT_DIR
from .doc_du_lieu import load_clean_data
from .tao_feature import build_features
from .mo_hinh import train_models, predict_lambda, win_draw_lose


def predict_future(played, future):
    lam_h, lam_a = predict_lambda(train_models(played), future)
    rows = []
    for i in range(len(future)):
        (p_home, p_draw, p_away), table = win_draw_lose(lam_h[i], lam_a[i])
        best = np.unravel_index(table.argmax(), table.shape)      # ô có xác suất lớn nhất
        rows.append({"match_id": future["game_Id"][i], "home_team": future["home_Team"][i],
                     "away_team": future["away_Team"][i], "prob_home_win": round(p_home, 4),
                     "prob_draw": round(p_draw, 4), "prob_away_win": round(p_away, 4),
                     "most_likely_score": "%d-%d" % best})
    return pd.DataFrame(rows)


if __name__ == "__main__":
    played, future = build_features(load_clean_data())
    result = predict_future(played, future)
    result.to_csv(OUTPUT_DIR / "predictions.csv", index=False)
    print("Đã lưu outputs/predictions.csv (%d trận)" % len(result))
    print(result.head())
