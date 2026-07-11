# mlb-stat-predictor
A Python sports analytics project using MLB hitter statistics to analyze player performance, identify offensive trends, and build machine learning models for player stat prediction.

## Progress
- Loaded and cleaned MLB batting data.
- Filtered out non-qualified hitters based on plate appearances.
- Selected features and target values for an OPS prediction model.
- Built an initial linear regression model.
- Evaluated the model using MAE, MSE, and R².
- Found that some features caused data leakage because they were too directly related to OPS.
- Removed direct OPS-related features to make the model more realistic.
- Exported cleaned/model data to CSV files for debugging.

## What I've Learned
- How to split data into features (`X`) and a target (`y`).
- How to train a basic machine learning model.
- How to evaluate predictions against actual values.
- Why data leakage can make a model look more accurate than it really is.
- Why future prediction should use past-season stats to predict next-season performance.

## Next Steps
- Combine multiple seasons of batting data.
- Create a `next_season_ops` target column.
- Train on earlier seasons and test on later seasons.
- Compare different models and feature sets.
