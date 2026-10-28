
import numpy as np
from sklearn.metrics import log_loss
from .config import TRAIN_RATIO
from .doc_du_lieu import load_clean_data
from .tao_feature import build_features
from .mo_hinh import train_models, predict_lambda, probs_for_all, brier


def evaluate(played):
    cut = int(len(played) * TRAIN_RATIO)
    train, test = played[:cut], played[cut:]
    print("Train:", len(train), "trận | Test:", len(test), "trận")

    # mô hình Poisson Regression
    lam_h, lam_a = predict_lambda(train_models(train), test)
    probs = probs_for_all(lam_h, lam_a)

    # mô hình so sánh (baseline): mọi trận đều dùng số bàn trung bình của tập train
    n = len(test)
    probs_base = probs_for_all([train["home_Goals"].mean()] * n, [train["away_Goals"].mean()] * n)

    y = test["result"].astype(int).values
    print("\n--- Kết quả (càng nhỏ càng tốt) ---")
    print("Đoán đều 1/3      : log loss = %.3f | Brier = %.3f" % (np.log(3), 2 / 3))
    print("Baseline          : log loss = %.3f | Brier = %.3f" % (log_loss(y, probs_base, labels=[0, 1, 2]), brier(probs_base, y)))
    print("Poisson Regression: log loss = %.3f | Brier = %.3f" % (log_loss(y, probs, labels=[0, 1, 2]), brier(probs, y)))


if __name__ == "__main__":
    played, future = build_features(load_clean_data())
    evaluate(played)
