import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV, TimeSeriesSplit
from sklearn.tree import DecisionTreeClassifier, plot_tree, export_text
from sklearn.metrics import classification_report, confusion_matrix, balanced_accuracy_score
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestClassifier

def make_random_forest_model(df, plot_title_text):
    week = df["week_number"].astype(float)
    df["week_sin"] = np.sin(2 * np.pi * week / 52)
    df["week_cos"] = np.cos(2 * np.pi * week / 52)

    #df.groupby(['week_number']).agg({'OBSERVATION_COUNT': 'sum'})

    X = df[["week_sin", "week_cos", "year", "tavg", "tmin", "tmax", "prcp", "snow", "wspd", "pres"]]
    y = df["OBSERVATION_PRESENT"].astype(bool)

    # Split data for training and testing
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    # Random Forest creation
    rf = RandomForestClassifier(
        n_estimators=200,  # Number of decision trees
        max_depth=4,
        min_samples_leaf=5,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    )

    param_grid = {
        "n_estimators": [100, 200, 400],
        "max_depth": [3, 4, 5, 6, None],
        "min_samples_leaf": [1, 3, 5, 10],
        "max_features": ["sqrt", "log2"]
    }

    grid = GridSearchCV(
        rf,
        param_grid,
        scoring="balanced_accuracy",
        cv=5,
        n_jobs=-1,
        verbose=1
    )
    grid.fit(X_train, y_train)

    best_rf = grid.best_estimator_
    print("Best parameters:", grid.best_params_)

    # Evaluate model
    y_pred = best_rf.predict(X_test)
    print("\nConfusion matrix:\n", confusion_matrix(y_test, y_pred))
    print("\nClassification report:\n", classification_report(y_test, y_pred, digits=3))
    print("Balanced accuracy:", balanced_accuracy_score(y_test, y_pred))

    # Feature importance
    importances = pd.Series(best_rf.feature_importances_, index=X.columns).sort_values(ascending=False)
    print("\nFeature importances:\n", importances)

    plt.figure(figsize=(6, 4))
    importances.plot(kind="barh")
    plt.title(plot_title_text, fontsize=16)

    importances_bar_chart, dec_tree_diagram = plt.subplots(figsize=(14, 8))

    plot_tree(best_rf.estimators_[0],
              feature_names=X.columns,
              filled=True,
              rounded=True,
              proportion=True,
              precision=2,
              label='all',
              fontsize=16,
              ax=dec_tree_diagram)
    dec_tree_diagram.set_title(plot_title_text, fontsize=22)
    plt.tight_layout()

    plt.show()

    print(export_text(best_rf.estimators_[0], feature_names=list(X.columns)))

if __name__ == '__main__':
    alt_puffin_env_df = pd.read_csv("../data_preprocessing/environmental_data_joined/atlantic_puffin_ma_coastal_weekly_weather_observation_data.csv")
    osprey_env_df = pd.read_csv(
        "../data_preprocessing/environmental_data_joined/osprey_glacier_bay_weekly_weather_observation_data.csv")
    ca_condor_env_df = pd.read_csv("../data_preprocessing/environmental_data_joined/ca_condor_grand_canyon_weekly_weather_observation_data.csv")
    make_random_forest_model(alt_puffin_env_df, "Atlantic Puffin - Massachusetts Coastal Area")
    make_random_forest_model(osprey_env_df, "Osprey - Glacier Bay, Alaska")
    make_random_forest_model(ca_condor_env_df, "California Condor - Grand Canyon")
