# pip install scikit-learn pandas numpy matplotlib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV, TimeSeriesSplit
from sklearn.tree import DecisionTreeClassifier, plot_tree, export_text
from sklearn.metrics import classification_report, confusion_matrix, balanced_accuracy_score
import matplotlib.pyplot as plt

def make_decision_tree_model(df: pd.DataFrame):
    # Ensure deterministic order by time if you have a date or year/week columns.
    # If you have 'year' and 'week_number', sort by them:
    sort_cols = [c for c in ["year", "week_number"] if c in df.columns]
    if sort_cols:
        df = df.sort_values(sort_cols).reset_index(drop=True)

    week = df["week_number"]
    X = pd.DataFrame({
        "week_sin": np.sin(2 * np.pi * week / 52),
        "week_cos": np.cos(2 * np.pi * week / 52),
    })
    y = df["OBSERVATION_PRESENT"].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    # --- Strong regularization & pruning ------------------------------------
    base_tree = DecisionTreeClassifier(
        random_state=42,
        class_weight="balanced"
    )

    # Keep trees small; prefer leaves with enough cases; allow cost-complexity pruning.
    param_grid = {
        "criterion": ["gini", "entropy"],
        "max_depth": [2, 3, 4, 5],          # remove None
        "min_samples_leaf": [10, 20, 30, 50],
        "min_samples_split": [10, 20, 50],
        "max_leaf_nodes": [3, 4, 6, 8],     # caps size directly
        "ccp_alpha": [0.0, 1e-4, 5e-4, 1e-3, 2e-3]  # post-pruning
    }

    # Prefer a time-aware split if your rows are in chronological order.
    # If you sorted above, this will respect temporal structure:
    cv = TimeSeriesSplit(n_splits=5) if sort_cols else 5

    search = GridSearchCV(
        base_tree,
        param_grid,
        scoring="balanced_accuracy",   # better than raw accuracy on imbalance
        cv=cv,
        n_jobs=-1
    )
    search.fit(X_train, y_train)

    best_tree = search.best_estimator_
    print("Best params:", search.best_params_)

    y_pred = best_tree.predict(X_test)
    print("\nConfusion matrix:\n", confusion_matrix(y_test, y_pred))
    print("\nClassification report:\n", classification_report(y_test, y_pred, labels=best_tree.classes_, digits=3))
    print("Balanced accuracy:", balanced_accuracy_score(y_test, y_pred))

    print("\nFeature importances:\n",
          pd.Series(best_tree.feature_importances_, index=X.columns).sort_values(ascending=False))

    plt.figure(figsize=(10, 6))
    plot_tree(best_tree, feature_names=X.columns.tolist(),
              class_names=[str(c) for c in best_tree.classes_],
              filled=True, rounded=True, fontsize=9)
    plt.tight_layout()
    plt.show()

    print(export_text(best_tree, feature_names=list(X.columns)))

if __name__ == '__main__':
    df = pd.read_csv("../data_preprocessing/environmental_data_joined/atlantic_puffin_ma_coastal_weekly_weather_observation_data.csv")
    make_decision_tree_model(df)
