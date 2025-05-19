# Dropout Prediction App

This application predicts students dropout status using a pre-trained XGBoost model. The app is built with Streamlit and allows users to upload a CSV file containing student data, process it, and download the prediction results.

## Features
- Upload a CSV file with student data.
- Validate the uploaded file for required columns.
- Perform preprocessing, including encoding and scaling.
- Predict student dropout status using the XGBoost model.
- Display the predicted dropout rate and provide a downloadable CSV file with predictions.

## Prerequisites
Before running the app, ensure you have the following installed:
- Python 3.8 or higher
- Required Python libraries:
  - `streamlit`
  - `pandas`
  - `joblib`
  - `scikit-learn`
  - `xgboost`

You can install the required libraries using the following command:

```bash
pip install -r requirements.txt
```

## Required Files

Make sure the following files are in the same directory as `app.py`:

1. `xgb_model.pkl` - The pre-trained XGBoost model.
2. `scaler.pkl` - The scaler used for preprocessing the data.

## How to Use

1. Run the Application
  - Go to this [link](https://deploy-app-jaya-jaya-institute-nairkivm.streamlit.app/) or
  - Open a terminal, navigate to the directory containing `app.py`, and run the following command: 

```bash
streamlit run app.py
```

1. Upload a CSV File
   - Prepare a CSV file containing student data. 
   - Use the "Upload CSV file" button in the app to upload your file.
2. View Predictions
   - The app will process the data, perform predictions, and display:
      - The predicted dropout rate.
      - A preview of the data with a new column PredictedDropout indicating the prediction results.
3. Download Results
   - Use the "Download Prediction Result" button to download the processed CSV file with predictions.
