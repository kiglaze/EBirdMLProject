import numpy as np
import pandas as pd
from pandas import DataFrame
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
import os

def main():
    osprey_glacier_bay_df = pd.read_csv("../data_preprocessing/restricted_geo_loc_sighting_weekly/osprey_glacier_bay_weekly.csv")
    generate_cyclical_log_reg_plots(osprey_glacier_bay_df, "Osprey", "Glacier Bay, Alaska")

    ca_condor_gc_df = pd.read_csv("../data_preprocessing/restricted_geo_loc_sighting_weekly/ca_condor_grand_canyon_weekly.csv")
    generate_cyclical_log_reg_plots(ca_condor_gc_df, "California Condor", "Grand Canyon")

    alt_puffin_ma_coast_df = pd.read_csv("../data_preprocessing/restricted_geo_loc_sighting_weekly/atlantic_puffin_ma_coastal_weekly.csv")
    generate_cyclical_log_reg_plots(alt_puffin_ma_coast_df, "Atlantic Puffin", "Massachusetts Coastal Area")

def generate_cyclical_log_reg_plots(df: DataFrame, species_name, location_name):
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
    plt.xlabel('Week In Year', fontsize=20)
    plt.ylabel(f"Probability of Sighting", fontsize=20)
    plt.title(f"{location_name} (2015-2025): {species_name} \nPresence vs. Week of Year (Cyclic Logistic Regression)", fontsize=22)
    plt.legend()
    plt.tight_layout()

    output_directory = "logistic_regression_plots"
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    output_filename = f"{output_directory}/log_reg_{species_name.replace(' ', '_').lower()}_{location_name.replace(' ', '_').lower()}.png"
    plt.savefig(output_filename)
    plt.show()
    plt.close()

if __name__ == "__main__":
    main()
