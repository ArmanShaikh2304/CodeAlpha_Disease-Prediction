import joblib
import pandas as pd
from pathlib import Path
from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model.pkl"


def train_and_save_model():
    """Train a Logistic Regression model and save it as model.pkl."""

    # Load the Breast Cancer Wisconsin dataset included with scikit-learn.
    dataset = load_breast_cancer()

    # Store the feature data in a DataFrame to keep clear column names.
    feature_names = [str(name) for name in dataset.feature_names]
    X = pd.DataFrame(dataset.data, columns=feature_names)
    y = dataset.target

    # Split the data so the model is tested on examples it did not train on.
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    # StandardScaler improves Logistic Regression performance on this dataset.
    model = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("classifier", LogisticRegression(max_iter=10000)),
        ]
    )

    # Train the model.
    model.fit(X_train, y_train)

    # Check accuracy on the test set.
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    # Save everything the Flask app needs in one file.
    model_package = {
        "model": model,
        "feature_names": feature_names,
        "feature_means": X.mean().to_dict(),
        "accuracy": round(float(accuracy) * 100, 2),
        "target_names": list(dataset.target_names),
    }

    joblib.dump(model_package, MODEL_PATH)

    print("Model trained successfully.")
    print(f"Model accuracy: {accuracy * 100:.2f}%")
    print(f"Saved trained model as {MODEL_PATH.name}")


if __name__ == "__main__":
    train_and_save_model()
