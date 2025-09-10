
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib
import warnings

warnings.filterwarnings('ignore')

# Step 1: Load the dataset
try:
    df = pd.read_csv('WA_Fn-UseC_-Telco-Customer-Churn.csv')
    print("Dataset loaded successfully!")
except FileNotFoundError:
    print("Error: 'WA_Fn-UseC_-Telco-Customer-Churn.csv' not found.")
    print("Please make sure the CSV file is in the same directory as this script.")
    exit()

# Step 2: Data Cleaning and Preprocessing
print("\n--- Starting Data Cleaning and Preprocessing ---")
df = df.drop('customerID', axis=1)
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')

median_total_charges = df['TotalCharges'].median()
df['TotalCharges'].fillna(median_total_charges, inplace=True)

X = df.drop('Churn', axis=1)
y = df['Churn'].apply(lambda x: 1 if x == 'Yes' else 0)

numerical_features = X.select_dtypes(include=np.number).columns.tolist()
categorical_features = X.select_dtypes(exclude=np.number).columns.tolist()

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_features),
       ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ])

# Step 3: Splitting the Dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
print("Dataset split into training and testing sets.")

# Step 4: Building the Model Pipeline and Hyperparameter Tuning
print("--- Training the model with Hyperparameter Tuning ---")
log_reg_pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                                      ('classifier', LogisticRegression(random_state=42, max_iter=1000))])

param_grid = {
    'classifier__C': [0.01, 0.1, 1, 10, 100],
    'classifier__solver': ['liblinear', 'saga']
}

grid_search = GridSearchCV(log_reg_pipeline, param_grid, cv=5, scoring='roc_auc', n_jobs=-1)
grid_search.fit(X_train, y_train)

best_model = grid_search.best_estimator_
print(f"Best parameters found: {grid_search.best_params_}")

# Step 5: Saving the Model
print("\n--- Saving the final model ---")
model_filename = 'churn_model.joblib'
joblib.dump(best_model, model_filename)
print(f"Model saved successfully as '{model_filename}'")
print("\n--- Script Finished ---")
   


