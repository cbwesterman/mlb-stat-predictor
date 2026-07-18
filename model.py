import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def create_model(X, y):
    
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    lr_model = LinearRegression()

    lr_model.fit(X_train, y_train)

    y_pred = lr_model.predict(X_test)

    lr_results = pd.DataFrame({
        "Actual OPS": y_test,
        "Predicted OPS": y_pred
    })

    print(lr_results.head(10))

    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print("LR_MAE:", mae)
    print("LR_MSE:", mse)
    print("LR_R²:", r2)

    rf_model = RandomForestRegressor(
        n_estimators=200,
        random_state=42
    )

    rf_model.fit(X_train, y_train)

    y_pred = rf_model.predict(X_test)

    rf_results = pd.DataFrame({
        "Actual OPS": y_test,
        "Predicted OPS": y_pred
    })

    print(rf_results.head(10))

    print("MAE:", mean_absolute_error(y_test, y_pred))
    print("MSE:", mean_squared_error(y_test, y_pred))
    print("R²:", r2_score(y_test, y_pred))