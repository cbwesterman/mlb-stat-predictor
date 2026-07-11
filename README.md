# mlb-stat-predictor
A Python sports analytics project using MLB hitter statistics to analyze player performance, identify offensive trends, and build machine learning models for player stat prediction.

# Current Model Progress
-Loaded in current 2026 MLB statistics up-to-date
-Removed non-qualified hitters (Current Games Played * 3.1 Plate Appearances)
-Removed non-useful stat columns, and renamed remaining columns
-Created features list for model, target is OPS
-For first model used LinearRegression
-Discovered what data leakage is and removed some features to improve model
