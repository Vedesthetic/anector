import numpy as np

# ----------------------------
# Baseline configuration
# ----------------------------
np.random.seed(42)
n_samples = 2000   # large enough for stability

# Feature order:
# [
#   keyIntervalMean (ms),
#   keyIntervalStd (ms),
#   mouseRate (events/sec),
#   clickRate (clicks/sec),
#   scrollRate (scrolls/sec),
#   tabSwitches (count),
#   answerChanges (count),
#   timeSpent (seconds)
# ]

baseline_data = np.column_stack([
    np.random.normal(110, 30, n_samples),   # keyIntervalMean
    np.random.normal(25, 10, n_samples),    # keyIntervalStd
    np.random.normal(0.8, 0.4, n_samples),  # mouseRate
    np.random.normal(0.08, 0.04, n_samples),# clickRate
    np.random.normal(0.02, 0.02, n_samples),# scrollRate
    np.random.poisson(0.2, n_samples),      # tabSwitches
    np.random.normal(3, 2, n_samples),      # answerChanges
    np.random.normal(120, 40, n_samples)    # timeSpent
])

# Remove impossible values (very important)
baseline_data = np.clip(baseline_data, a_min=0, a_max=None)
