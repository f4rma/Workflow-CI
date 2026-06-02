# Melatih model RandomForestClassifier dengan MLflow autolog, tracking disimpan secara lokal di (mlruns/).

import os
import sys

# Opt-in agar tracking lokal ./mlruns tetap bisa dipakai + dibuka via `mlflow ui`.
os.environ["MLFLOW_ALLOW_FILE_STORE"] = "true"

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import mlflow
import mlflow.sklearn

# Parse command line arguments
data_path = sys.argv[1] if len(sys.argv) > 1 else "heart-disease_preprocessing.csv"
n_estimators = int(sys.argv[2]) if len(sys.argv) > 2 else 100
random_state = int(sys.argv[3]) if len(sys.argv) > 3 else 42
test_size = float(sys.argv[4]) if len(sys.argv) > 4 else 0.2

print(f"Parameters: data_path={data_path}, n_estimators={n_estimators}, random_state={random_state}, test_size={test_size}")

# Load dataset 
df = pd.read_csv(data_path)

X = df.drop(columns=["target"])
y = df["target"]

# Split data 
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=test_size, random_state=random_state, stratify=y
)

print(f"Train size : {X_train.shape[0]} | Test size : {X_test.shape[0]}")

# MLflow setup
mlflow.set_tracking_uri("file:./mlruns")
mlflow.set_experiment("heart-disease-basic")

# Autolog 
mlflow.sklearn.autolog()

# Training
with mlflow.start_run(run_name=f"RandomForest_n{n_estimators}"):
    model = RandomForestClassifier(n_estimators=n_estimators, random_state=random_state)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    # Log additional parameters
    mlflow.log_param("data_path", data_path)
    mlflow.log_param("test_size", test_size)
    
    print(f"\nAccuracy : {acc:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    print("\nMLflow run selesai. Jalankan 'mlflow ui' untuk melihat dashboard.")
    
    # Get run info untuk Docker build
    run_id = mlflow.active_run().info.run_id
    print(f"\nRun ID: {run_id}")
