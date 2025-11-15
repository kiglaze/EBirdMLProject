import numpy as np
from sklearn.cluster import DBSCAN

EARTH_RADIUS_KM = 6371.0088

def find_clusters_by_geo_loc_no_noise(df):
    # Compute labels without expanding df
    labels = _dbscan_labels_from_latlon_deg(
        df["LATITUDE"], df["LONGITUDE"],
        eps_km=50.0, min_samples=5  # consider raising min_samples from 2
    )

    # One filtered copy for output
    mask = labels != -1
    out = df.loc[mask].copy()
    out["CLUSTER"] = labels[mask].astype(np.int32, copy=False)

    # Optional: debug sizes without materializing huge prints
    print(f"rows_in: {len(df)}, rows_no_noise: {len(out)}")
    return out

def _dbscan_labels_from_latlon_deg(lat_deg, lon_deg, eps_km=50.0, min_samples=5):
    # Compact float32 radians matrix
    lat = lat_deg.to_numpy(dtype=np.float32, copy=False)
    lon = lon_deg.to_numpy(dtype=np.float32, copy=False)
    X = np.radians(np.column_stack((lat, lon)))   # (N,2) float32

    eps_rad = eps_km / EARTH_RADIUS_KM
    labels = DBSCAN(
        eps=eps_rad,
        min_samples=min_samples,
        metric="haversine",
        algorithm="ball_tree",
        n_jobs=1,
    ).fit_predict(X)

    # Free the large temporary asap
    del X
    return labels
