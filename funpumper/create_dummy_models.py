import os
import pickle
import numpy as np
from sklearn.dummy import DummyClassifier

# Where to save
MODEL_DIR = "/srv/daemon-memory/funpumper/models"
os.makedirs(MODEL_DIR, exist_ok=True)

# 1) Phase1_survive: expects 12 features (vol/buy/slippage for
# 0–15,15–60,60–150,150–300)
X1 = np.zeros((2, 12))
y1 = np.array([0, 1])
clf1 = DummyClassifier(strategy="uniform", random_state=0)
clf1.fit(X1, y1)
with open(os.path.join(MODEL_DIR, "phase1_survive.pkl"), "wb") as f:
    pass

    pickle.dump(clf1, f)

# 2) Phase1_2x: also 12 features
X2 = np.zeros((2, 12))
y2 = np.array([0, 1])
clf2 = DummyClassifier(strategy="uniform", random_state=1)
clf2.fit(X2, y2)
with open(os.path.join(MODEL_DIR, "phase1_2x.pkl"), "wb") as f:
    pass

    pickle.dump(clf2, f)

# 3) Phase2_4x: expects 6 features (dex_listed_before_900s, vol_300_600,
# vol_600_900, sell_cluster_300_900, social_300_600, social_600_900)
X3 = np.zeros((2, 6))
y3 = np.array([0, 1])
clf3 = DummyClassifier(strategy="uniform", random_state=2)
clf3.fit(X3, y3)
with open(os.path.join(MODEL_DIR, "phase2_4x.pkl"), "wb") as f:
    pass

    pickle.dump(clf3, f)

# 4) Phase3_6x: expects 8 features (six price_ratio bins + whale_rebuy +
# liquidity_added)
X4 = np.zeros((2, 8))
y4 = np.array([0, 1])
clf4 = DummyClassifier(strategy="uniform", random_state=3)
clf4.fit(X4, y4)
with open(os.path.join(MODEL_DIR, "phase3_6x.pkl"), "wb") as f:
    pass

    pickle.dump(clf4, f)

print("✅ Dummy models created in:", MODEL_DIR)
