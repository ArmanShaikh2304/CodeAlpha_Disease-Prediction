# Disease Prediction Web Application

A beginner-friendly Flask and Machine Learning project that predicts whether breast cancer is detected using the Breast Cancer Wisconsin dataset from scikit-learn.

The app trains a Logistic Regression model, saves it with Joblib, and loads it in Flask to make predictions from a clean web form.

## Features

- Flask web application
- Logistic Regression model
- Breast Cancer Wisconsin dataset from scikit-learn
- Saved model using Joblib
- Input validation
- Prediction result on the same page
- Confidence percentage
- Model accuracy shown on the homepage
- Reset button
- Responsive HTML, CSS, and JavaScript frontend






## How It Works

1. `train_model.py` loads the Breast Cancer Wisconsin dataset.
2. The dataset is split into training and testing data.
3. A Logistic Regression model is trained inside a simple preprocessing pipeline.
4. The model accuracy is printed in the terminal.
5. The trained model and helpful metadata are saved as `model.pkl`.
6. `app.py` loads `model.pkl` and uses it to predict form inputs.

## Prediction Output

The app displays one of these results:

- Disease Detected
- No Disease Detected

It also displays the model confidence as a percentage.


