import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np

def train_and_predict(train_file='C:\\Users\\visha\\OneDrive\\Desktop\\summer-analytics-mid-hackathon\\hacktrain.csv', test_file='C:\\Users\\visha\\OneDrive\\Desktop\\summer-analytics-mid-hackathon\\hacktest.csv', submission_file='C:\\Users\\visha\\OneDrive\\Desktop\\summer-analytics-mid-hackathon\\submission.csv'):
    # Load data
    try:
        train_df = pd.read_csv(train_file)
        test_df = pd.read_csv(test_file)
    except FileNotFoundError:
        print(f"Error: Make sure the paths to your dataset files are correct.")
        return

    # Identify NDVI columns
    ndvi_cols = [col for col in train_df.columns if '_N' in col]

    # --- Preprocessing ---

    # Impute missing values with the mean of each NDVI column
    for col in ndvi_cols:
        train_df[col].fillna(train_df[col].mean(), inplace=True)
        test_df[col].fillna(test_df[col].mean(), inplace=True)

    # Simple Denoising: Apply a rolling mean (moving average)
    # This is a basic approach and can be improved
    for col in ndvi_cols:
        train_df[col] = train_df[col].rolling(window=3, min_periods=1, center=True).mean()
        test_df[col] = test_df[col].rolling(window=3, min_periods=1, center=True).mean()

    # --- Feature Engineering ---
    # Extract statistical features from NDVI time series
    train_df['ndvi_mean'] = train_df[ndvi_cols].mean(axis=1)
    train_df['ndvi_std'] = train_df[ndvi_cols].std(axis=1)
    train_df['ndvi_min'] = train_df[ndvi_cols].min(axis=1)
    train_df['ndvi_max'] = train_df[ndvi_cols].max(axis=1)
    train_df['ndvi_median'] = train_df[ndvi_cols].median(axis=1)

    test_df['ndvi_mean'] = test_df[ndvi_cols].mean(axis=1)
    test_df['ndvi_std'] = test_df[ndvi_cols].std(axis=1)
    test_df['ndvi_min'] = test_df[ndvi_cols].min(axis=1)
    test_df['ndvi_max'] = test_df[ndvi_cols].max(axis=1)
    test_df['ndvi_median'] = test_df[ndvi_cols].median(axis=1)

    # Features to use for training
    features = ['ndvi_mean', 'ndvi_std', 'ndvi_min', 'ndvi_max', 'ndvi_median']

    # Add back the original NDVI columns for now, you can refine this later
    features.extend(ndvi_cols)

    X_train = train_df[features]
    y_train = train_df['class']
    X_test = test_df[features]

    # --- Model Training ---
    # Initialize and train Logistic Regression model
    # Using 'multinomial' solver for multiclass classification and 'lbfgs' for efficiency
    model = LogisticRegression(max_iter=1000, solver='lbfgs', multi_class='multinomial')
    model.fit(X_train, y_train)

    # --- Prediction ---
    predictions = model.predict(X_test)

    # --- Create Submission File ---
    submission_df = pd.DataFrame({'ID': test_df['ID'], 'class': predictions})
    submission_df.to_csv(submission_file, index=False)

    print(f"Submission file '{submission_file}' created successfully.")
    print("Model training and prediction complete.")

if __name__ == "__main__":
    train_and_predict() 