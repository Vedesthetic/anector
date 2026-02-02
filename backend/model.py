import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

np.random.seed(42)
n = 3000

# Baseline tuned from YOUR real behavior
baseline = np.column_stack([
    np.random.normal(300, 200, n),   # keyIntervalMean
    np.random.normal(150, 120, n),   # keyIntervalStd
    np.random.normal(0.8, 0.6, n),   # mouseRate
    np.random.normal(0.08, 0.06, n), # clickRate
    np.random.normal(0.01, 0.01, n), # scrollRate
    np.random.poisson(0.6, n),       # tabSwitches
    np.random.normal(20, 20, n),     # answerChanges
    np.random.normal(40, 30, n)      # timeSpent
])

baseline = np.clip(baseline, 0, None)

scaler = StandardScaler()
X = scaler.fit_transform(baseline)

model = IsolationForest(
    n_estimators=400,
    contamination=0.02,
    random_state=42
)
model.fit(X)

scores = -model.score_samples(X)
mean, std = scores.mean(), scores.std()
low, high = mean - 3*std, mean + 3*std

def get_anomaly_score(features):
    f = np.array(features, dtype=float).reshape(1, -1)
    f = np.clip(f, 0, None)

    time_spent = f[0, 7]
    edits = f[0, 6]
    tabs = f[0, 5]

    # 1️⃣ Safe normal case
    if time_spent < 60 and edits <= 5 and tabs == 0:
        return 0.25

    # 2️⃣ ML-based score
    f_scaled = scaler.transform(f)
    raw = -model.score_samples(f_scaled)[0]

    # Guard against divide-by-zero
    if high - low <= 1e-6:
        score = 0.3
    else:
        score = (raw - low) / (high - low)
        score = float(np.clip(score, 0, 1))

    # 3️⃣ Review bias for spammy fast typing
    if edits > 30 and time_spent < 60:
        score = max(score, 0.5)

    # ✅ FINAL GUARANTEED RETURN
    return round(float(score), 2)

