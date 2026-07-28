from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score

def build_model(df):

    features = [
        "hits_last_7",
        "pa_last_7",
        "strikeouts_last_7",
        "total_bases_last_7",
        "hit_rate_last_7",
        "strikeout_rate_last_7",
        "total_bases_per_game_last_7"
    ]

    target = "target_hit"

    X = df[features].copy()
    y = df[target].copy()

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    model = LogisticRegression(max_iter=1000)

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    print("Logistic Regression Results")
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Precision:", precision_score(y_test, y_pred))
    print("Recall:", recall_score(y_test, y_pred))
    print("ROC-AUC:", roc_auc_score(y_test, y_prob))

    results_df = X_test.copy()
    results_df["actual_hit"] = y_test
    results_df["predicted_hit"] = y_pred
    results_df["predicted_probability"] = y_prob

    return model, results_df