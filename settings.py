"""Project-wide constants. Values that may be changed later are collected here."""

# ---- data (week 3) ----
SAMPLE_PER_CLASS = 20000   # URLs taken from each class (phishing / legitimate) to keep training fast
RANDOM_STATE = 42          # fixed so that sampling and splitting are repeatable
MAX_URL_LENGTH = 2000      # longer addresses are rejected by the website

# ---- model training (week 5) ----
TEST_SIZE = 0.2            # 20% of the URLs are kept aside for testing
DEPLOYED_SET = "all"       # the feature set (see feature_sets.py) used by the website

# ---- verdict levels shown to the user (probability that the URL is phishing, 0 to 1) ----
SAFE_BELOW = 0.35          # below this: looks safe
PHISHING_FROM = 0.65       # from this up: likely phishing; in between: suspicious


def verdict_of(probability):
    if probability < SAFE_BELOW:
        return "safe"
    if probability >= PHISHING_FROM:
        return "phishing"
    return "suspicious"
