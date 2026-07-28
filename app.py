from flask import Flask, render_template, request
import joblib
import numpy as np
import pandas as pd
from pathlib import Path


app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent

# Load the saved model package once when the Flask app starts.
# The package contains the trained model, feature names, accuracy, and sample values.
model_package = joblib.load(BASE_DIR / "model.pkl")
model = model_package["model"]
feature_names = model_package["feature_names"]
feature_means = model_package["feature_means"]
model_accuracy = model_package["accuracy"]


def make_feature_list(values=None):
    """Build feature data used by the HTML form."""
    values = values or {}
    features = []

    for feature_name in feature_names:
        feature_id = feature_name.replace(" ", "_").replace("-", "_")
        features.append(
            {
                "name": feature_name,
                "id": feature_id,
                "label": feature_name.title(),
                "placeholder": round(float(feature_means[feature_name]), 4),
                "value": values.get(feature_name, ""),
            }
        )

    return features


@app.route("/")
def home():
    """Show the home page with the prediction form."""
    return render_template(
        "index.html",
        features=make_feature_list(),
        accuracy=model_accuracy,
        result=None,
        error=None,
    )


@app.route("/predict", methods=["POST"])
def predict():
    """Validate form values, run the model, and show the result."""
    form_values = {}
    input_values = []

    for feature_name in feature_names:
        raw_value = request.form.get(feature_name, "").strip()
        form_values[feature_name] = raw_value

        # Every model input must be present and numeric.
        if not raw_value:
            return render_template(
                "index.html",
                features=make_feature_list(form_values),
                accuracy=model_accuracy,
                result=None,
                error=f"Please enter a value for {feature_name}.",
            )

        try:
            value = float(raw_value)
        except ValueError:
            return render_template(
                "index.html",
                features=make_feature_list(form_values),
                accuracy=model_accuracy,
                result=None,
                error=f"{feature_name} must be a valid number.",
            )

        if value < 0:
            return render_template(
                "index.html",
                features=make_feature_list(form_values),
                accuracy=model_accuracy,
                result=None,
                error=f"{feature_name} must be 0 or greater.",
            )

        input_values.append(value)

    # Use a DataFrame so the model receives the same feature names used in training.
    input_array = np.array([input_values])
    input_data = pd.DataFrame(input_array, columns=[str(name) for name in feature_names])

    prediction = model.predict(input_data)[0]
    probabilities = model.predict_proba(input_data)[0]

    # In this dataset: 0 = malignant, 1 = benign.
    if prediction == 0:
        label = "Disease Detected"
        detail = "The model predicts that this case may be malignant."
        status = "danger"
        confidence = probabilities[0] * 100
    else:
        label = "No Disease Detected"
        detail = "The model predicts that this case is likely benign."
        status = "safe"
        confidence = probabilities[1] * 100

    result = {
        "label": label,
        "detail": detail,
        "status": status,
        "confidence": round(float(confidence), 2),
    }

    return render_template(
        "index.html",
        features=make_feature_list(form_values),
        accuracy=model_accuracy,
        result=result,
        error=None,
    )


if __name__ == "__main__":
    app.run(debug=True)
