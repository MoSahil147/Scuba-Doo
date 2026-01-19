## as the name suggets, we are here training our model here

## we are using the RandomForestClassifier

## We chose Random Forest Classifier because the dive safety prediction depends on Complex and Non-Linear relationships between variables like wave height, ocean current, temperature, and UV index. Models like Linear Regression are only suited for predicting continuous values, while Logistic Regression assumes a linear decision boundary and performs poorly with overlapping or complex features. Decision Trees tend to overfit easily, especially with noisy or synthetic data. SVM is difficult to scale and tune with many features, KNN is slow and sensitive to irrelevant features, and Naive Bayes relies on independence assumptions that don’t apply here. Though Gradient Boosting (like XGBoost) can outperform Random Forest in some cases, it’s slower to train and requires more tuning. Neural Networks demand larger datasets and more compute, which wasn’t necessary for our structured tabular data. Random Forest offered the best balance of speed, accuracy, and robustness, especially when dealing with synthetic but realistic data and mixed feature scales, making it the most practical and effective choice.

##Random Forest is an ensemble machine learning algorithm that builds many decision trees and combines their outputs to improve accuracy and reduce overfitting. It works well with structured data and supports both classification (predicting categories like safe/unsafe) and regression (predicting continuous values like temperature or price).
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

## Step 1: Loading the dataset from CSV
print("Loading dataset!!!")
df = pd.read_csv("Data/final_synthetic_dive_dataset.csv")
print("Initial rows:", len(df))

## Step 2: Normalize 'verdict' values and create a binary column
    # Convert all entries in the 'verdict' column to lowercase and strip spaces
    ## For context Verdict refers to the dive safety outcome, indicating wether the scuba dive is consider SAFE or NOT SAFE
df["verdict"] = df["verdict"].astype(str).str.strip().str.lower()

    # Map 'safe' to 1, 'unsafe' to 0 for binary classification
df["verdict_binary"] = df["verdict"].map({
    "safe": 1,
    "unsafe": 0
})

    # Drop rows where verdict could not be mapped (for example:- empty or invalid strings)
df = df.dropna(subset=["verdict_binary"])

print("Rows after verdict cleanup:", len(df))
print("Verdict distribution:")
print(df["verdict"].value_counts())

## Step 3: Defining the core numeric features to be used for training
CORE_NUMERIC_COLS = [
    "latitude",
    "longitude",
    "month",
    "hour_of_day",
    "wave_height",
    "sea_surface_temperature",
    "ocean_current_velocity",
    "uv_index_max",
    "pressure_msl",
    "typical_depth"
]

## Step 4: Convert columns to numeric and handle format inconsistencies
    # Some values might be stored with commas instead of decimal points
for col in CORE_NUMERIC_COLS:
    df[col] = df[col].astype(str).str.replace(",", ".", regex=False).str.strip()
    df[col] = pd.to_numeric(df[col], errors="coerce")  # Coerce errors set to NaN

## Step 5: Fill missing numeric values with column median (safe imputation)
    ## Loop through each important numeric feature
for col in CORE_NUMERIC_COLS:

    ## Calculating the median value of the column
    ## Median is the middle value and is not affected much by outliers, Outliers are data points that differ significantly from other observations in a dataset.
    median_value = df[col].median()

    ## Replace missing values (NaN) in that column with the median
    ## This keeps all rows instead of deleting data
    df[col] = df[col].fillna(median_value)

print("Rows after numeric cleanup:", len(df))

## Step 6: Separate features (X) and target (y)
X = df[CORE_NUMERIC_COLS]
y = df["verdict_binary"]

print("Final dataset size:", len(df))
print("Target distribution:")
print(y.value_counts())

## Step 7: Split the dataset into training and testing sets (80/20 split)
X_train, X_test, y_train, y_test = train_test_split(
    X,                  # feature columns (input values)
    y,                  # target column ('verdict_binary')
    test_size=0.2,      # 20% of the data goes to testing set, 80% to training
    random_state=42,    # ensures consistent results every time you run The random_state is a fixed number that ensures the same result every time you run the code. It controls the randomness used in splitting the dataset. For example, if random_state=42, we will always get the same training and test sets when re-running the code. This is important for reproducibility.
    stratify=y          # keeps the class distribution balanced in both sets
)

print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))

## Step 8: Train a Random Forest Classifier
model = RandomForestClassifier(
    n_estimators=150,      # Number of trees in the forest
    max_depth=10,          # Max depth of each tree
    random_state=42,       # For reproducibility
    n_jobs=-1              # Use all CPU cores
)

model.fit(X_train, y_train)

## Step 9: Evaluate model accuracy on both training and testing sets
train_acc = model.score(X_train, y_train)
test_acc = model.score(X_test, y_test)

print("Training accuracy:", round(train_acc * 100, 2))
print("Testing accuracy:", round(test_acc * 100, 2))

## Step 10: Save the trained model to a file
joblib.dump(model, "Data/scuba_dive_model.pkl")
print("Model saved successfully, Check the Data folder")