import sqlite3
import pandas as pd
from .config import DB_PATH, FIX_CODE


def load_clean_data():
    """Đọc Schedule + Match_stat, làm sạch, ghép lại. Trả về DataFrame sắp xếp theo ngày."""
    if not DB_PATH.exists():
        raise FileNotFoundError("Không tìm thấy database: %s" % DB_PATH)

    # --- đọc ---
    conn = sqlite3.connect(DB_PATH)
    schedule = pd.read_sql("SELECT * FROM Schedule", conn)
    stat = pd.read_sql("SELECT game_Id, home_Xg, away_Xg FROM Match_stat", conn)
    conn.close()

    # --- làm sạch ---
    schedule["home_Team"] = schedule["home_Team"].replace(FIX_CODE)   # sửa mã đội
    schedule["away_Team"] = schedule["away_Team"].replace(FIX_CODE)
    schedule["date"] = pd.to_datetime(schedule["date"])               # chuỗi -> ngày giờ
    schedule["is_result"] = schedule["is_result"].astype(int)         # '1'/'0' -> 1/0

    # --- ghép với bảng có xG rồi sắp xếp theo thời gian ---
    df = schedule.merge(stat, on="game_Id", how="left")
    return df.sort_values("date").reset_index(drop=True)


if __name__ == "__main__":
    df = load_clean_data()
    print("Tổng số trận:", len(df), "| đã đá:", (df["is_result"] == 1).sum())
    print(df.dtypes)
    print(df.head())
