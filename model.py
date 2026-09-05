import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_poisson_deviance

def build_model(df):
    model_df = df.copy()

    model_features = [
        "hits_last_7",
        "pa_last_7",
        "hit_rate_last_7",
        "opp_hit_rate_last_5",
        "opp_k_rate_last_5",
        "batter_rest_days",
        "starting_pitcher_rest_days",
        "starting_pitcher_hand_L"
    ]

    model_df = model_df.dropna(subset=model_features)
    model_df = model_df[model_df["plate_appearances"] >= 2]
    model_df = model_df.sort_values("game_date").reset_index(drop=True)

    target = "hits"

    cutoff_index = int(len(model_df) * 0.8)
    cutoff_date = model_df.iloc[cutoff_index]["game_date"]
    train_df = model_df[model_df["game_date"] < cutoff_date]
    test_df = model_df[model_df["game_date"] >= cutoff_date]

    X_train, y_train = train_df[model_features], train_df[target]
    X_test, y_test = test_df[model_features], test_df[target]

    print(f"Train: {len(X_train)} games (through {train_df['game_date'].max()})")
    print(f"Test: {len(X_test)} games ({test_df['game_date'].min()} to {test_df['game_date'].max()})")

    exposure_train = train_df["pa_last_7"] / 7
    exposure_test = test_df["pa_last_7"] / 7

    baseline_pred = test_df["hit_rate_last_7"] * exposure_test
    print("\nNaive Baseline (hit_rate_last_7 * expected PA)")
    print("MAE:", mean_absolute_error(y_test, baseline_pred))

    X_train_c = sm.add_constant(X_train)
    X_test_c = sm.add_constant(X_test, has_constant="add")

    poisson_model = sm.GLM(
        y_train, X_train_c,
        family=sm.families.Poisson(),
        offset=np.log(exposure_train)
    ).fit()

    poisson_pred = poisson_model.predict(X_test_c, offset=np.log(exposure_test))

    print("\nPoisson Regression Results")
    print("MAE:", mean_absolute_error(y_test, poisson_pred))
    print("Poisson Deviance:", mean_poisson_deviance(y_test, poisson_pred))
    print(poisson_model.summary())

    X_train_rf = X_train.copy()
    X_train_rf["exposure"] = exposure_train
    X_test_rf = X_test.copy()
    X_test_rf["exposure"] = exposure_test

    rf_model = RandomForestRegressor(
        n_estimators=300, max_depth=5, min_samples_leaf=10, random_state=42
    )
    rf_model.fit(X_train_rf, y_train)
    rf_pred = rf_model.predict(X_test_rf)

    print("\nRandom Forest Results")
    print("MAE:", mean_absolute_error(y_test, rf_pred))
    print("Poisson Deviance:", mean_poisson_deviance(y_test, np.clip(rf_pred, 1e-6, None)))

    importances = pd.Series(rf_model.feature_importances_, index=X_train_rf.columns).sort_values(ascending=False)
    print("\nFeature Importances (Random Forest)")
    print(importances)

    results_df = test_df.copy()
    results_df["predicted_hits_poisson"] = poisson_pred.values
    results_df["predicted_hits_rf"] = rf_pred

    return poisson_model, rf_model, results_df