import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt

def main():
    df = pd.read_csv("../data_preprocessing/restricted_geo_loc_sighting_weekly/osprey_glacier_bay_weekly.csv")

    # scale weeks to [0,1] for interpretability (optional)
    df['WEEK_FRACTION'] = (df['WEEK_IN_YEAR'] - 1) / 52.0

    df['WEEK_SIN'] = np.sin(2 * np.pi * df['WEEK_IN_YEAR'] / 52)
    df['WEEK_COS'] = np.cos(2 * np.pi * df['WEEK_IN_YEAR'] / 52)

    x = df[['WEEK_SIN', 'WEEK_COS']].values
    y = df['OBSERVATION_PRESENT'].astype(int).values

    # Fit a regular logistic regression (linear in week)
    model = LogisticRegression()
    model.fit(x, y)

    # Predict probabilities for plotting
    week_grid = np.linspace(1, 52, 200)
    X_grid = np.column_stack([
        np.sin(2 * np.pi * week_grid / 52),
        np.cos(2 * np.pi * week_grid / 52)
    ])
    pred_probs = model.predict_proba(X_grid)[:, 1]

    plt.figure(figsize=(10, 6))
    plt.scatter(df['WEEK_IN_YEAR'], y, alpha=0.2, label='Observations')
    plt.plot(week_grid, pred_probs, label='Cyclic Logistic Regression', color='red')
    plt.xlabel('Week In Year')
    plt.ylabel('Probability of Osprey Presence')
    plt.title('Glacier Bay, Alaska (2015-2025): Osprey Presence vs. Week of Year (Cyclic Logistic Regression)')
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
