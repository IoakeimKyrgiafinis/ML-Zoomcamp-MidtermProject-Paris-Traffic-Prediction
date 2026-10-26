import pickle
import geopandas as gpd
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

print("1. Downloading and loading Paris traffic dataset...")
url = "https://raw.githubusercontent.com/XavB64/traffic-volume-data-EU-cities/main/France/Paris/treated/Paris_AADT_AAWT_2023.geojson"
gdf = gpd.read_file(url)

print("2. Preprocessing features and target...")
target_col = 'AADT'
drop_cols = [target_col, 'AAWT', 'raw_name', 'raw_direction', 'osm_name', 'osmid', 'geometry']

X = gdf.drop(columns=drop_cols).copy()
y = gdf[target_col]

# Handle missing values
X['osm_lanes'] = X['osm_lanes'].fillna(X['osm_lanes'].median())
X['osm_maxspeed'] = X['osm_maxspeed'].fillna(X['osm_maxspeed'].median())
X['osm_type'] = X['osm_type'].fillna('unknown')
X['osm_oneway'] = X['osm_oneway'].fillna(False)

# Convert boolean columns to int
bool_cols = X.select_dtypes(include=['bool']).columns
X[bool_cols] = X[bool_cols].astype(int)

# One-hot encode categorical features
X = pd.get_dummies(X, columns=['osm_type'], drop_first=True)

# Train/Test Split
df_full_train, df_test = train_test_split(pd.concat([X, y], axis=1), test_size=0.2, random_state=42)
df_train, df_val = train_test_split(df_full_train, test_size=0.25, random_state=42)

X_train = df_train.drop(columns=[target_col])
y_train = df_train[target_col]
X_val = df_val.drop(columns=[target_col])
y_val = df_val[target_col]

# Force clean any remaining bool/string columns to int
for col in X_train.columns:
    if X_train[col].dtype == 'object' or X_train[col].dtype == bool:
        mapping = {True: 1, 'True': 1, 'true': 1, False: 0, 'False': 0, 'false': 0}
        X_train[col] = X_train[col].map(mapping).fillna(0).astype(int)
        X_val[col] = X_val[col].map(mapping).fillna(0).astype(int)

# Combine full train data
X_full_train = pd.concat([X_train, X_val])
y_full_train = pd.concat([y_train, y_val])

print("3. Training Final Random Forest Model (max_depth=10, min_samples_leaf=10)...")
final_model = RandomForestRegressor(
    n_estimators=100,
    max_depth=10,
    min_samples_leaf=10,
    random_state=42,
    n_jobs=-1
)
final_model.fit(X_full_train, y_full_train)

print("4. Saving model to model_paris_traffic.bin...")
output_file = 'model_paris_traffic.bin'
with open(output_file, 'wb') as f_out:
    pickle.dump(final_model, f_out)

print(f"Success! Model successfully saved to {output_file}.")