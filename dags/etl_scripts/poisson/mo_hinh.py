
import numpy as np
from scipy.stats import poisson
from sklearn.linear_model import PoissonRegressor
from .config import FEATURES, ALPHA, MAX_GOALS


def train_models(train):
    """Huấn luyện 2 mô hình: một cho bàn thắng đội nhà, một cho đội khách."""
    model_home = PoissonRegressor(alpha=ALPHA).fit(train[FEATURES], train["home_Goals"])
    model_away = PoissonRegressor(alpha=ALPHA).fit(train[FEATURES], train["away_Goals"])
    return model_home, model_away


def predict_lambda(models, data):
    """Dự đoán số bàn thắng kỳ vọng (lambda) của đội nhà và đội khách."""
    model_home, model_away = models
    return model_home.predict(data[FEATURES]), model_away.predict(data[FEATURES])


def win_draw_lose(lam_home, lam_away):
    """Từ lambda của 2 đội -> (xác suất [nhà thắng, hòa, khách thắng], bảng xác suất tỷ số)."""
    goals = np.arange(MAX_GOALS + 1)
    # bảng xác suất tỷ số: hàng = số bàn đội nhà, cột = số bàn đội khách
    table = np.outer(poisson.pmf(goals, lam_home), poisson.pmf(goals, lam_away))
    table = table / table.sum()
    home_win = np.tril(table, -1).sum()    # nửa dưới: đội nhà ghi nhiều hơn
    draw = np.trace(table)                 # đường chéo: bằng nhau
    away_win = np.triu(table, 1).sum()     # nửa trên: đội khách ghi nhiều hơn
    return [home_win, draw, away_win], table


def probs_for_all(lam_home, lam_away):
    """Tính xác suất thắng/hòa/thua cho nhiều trận."""
    return np.array([win_draw_lose(h, a)[0] for h, a in zip(lam_home, lam_away)])


def brier(probs, y):
    """Brier score: càng nhỏ càng tốt."""
    return np.mean(np.sum((probs - np.eye(3)[y]) ** 2, axis=1))


if __name__ == "__main__":
    # ví dụ kiểm tra: đội nhà kỳ vọng 1.7 bàn, đội khách 1.2 bàn
    probs, table = win_draw_lose(1.7, 1.2)
    print("Xác suất [nhà thắng, hòa, khách thắng]:", np.round(probs, 3), "| tổng =", round(sum(probs), 3))
    print("Tỷ số có khả năng cao nhất:", np.unravel_index(table.argmax(), table.shape))
