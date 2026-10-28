
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent      # thư mục gốc dự án (cha của src)
DB_PATH = ROOT / "database" / "EPL.db"
OUTPUT_DIR = ROOT / "data" 
OUTPUT_DIR.mkdir(exist_ok=True)

# Mã đội trong Schedule bị lệch so với bảng Teams -> sửa lại
FIX_CODE = {"BRI": "BHA", "FLH": "FUL", "LED": "LEE"}

FEATURES = ["xG_home", "xGA_home", "xG_away", "xGA_away", "Elo_diff"]

WINDOW = 5          # lấy trung bình 5 trận gần nhất
ELO_K = 30          # hệ số cập nhật Elo
ALPHA = 1.0         # mức "phạt" hệ số của Poisson Regression (tránh học quá khớp)
TRAIN_RATIO = 0.7   # 70% trận đầu để học, 30% trận sau để kiểm tra
MAX_GOALS = 10      # tối đa 10 bàn mỗi đội khi tính xác suất tỷ số
print(ROOT)