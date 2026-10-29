# Explainable AI-Based Cloud Security Threat Detection and Risk Prioritization

## 1. Project Overview
This project is a Python command-line prototype that demonstrates machine-learning-based cloud security event analysis, explainable AI, CSV log processing, and risk prioritization.

It uses a Random Forest classifier to classify sample security events as Suspicious or Normal based on failed login attempts and API request counts. SHAP is used to explain individual model predictions. The application can analyze CSV files, assign demonstration risk levels, and generate analysis reports.

## 2. Problem Statement
Security logs can contain many events that require review. Manual analysis may be time-consuming, and machine-learning predictions can be difficult to interpret without explanations. This project demonstrates a simple approach to classifying sample events, explaining predictions, and prioritizing results for further review.

## 3. Objectives
- Classify sample security events as Suspicious or Normal.
- Explain individual predictions using SHAP.
- Analyze multiple events from CSV files.
- Assign High, Medium, and Low demonstration risk levels.
- Generate CSV analysis results and a text summary report.
- Validate common input errors.

## 4. Technologies Used
- Python
- scikit-learn — Random Forest classifier
- SHAP — Explainable AI
- pandas — CSV data processing
- NumPy — numerical operations where used
- joblib — model saving and loading

## 5. Main Features
- Single-event threat prediction.
- SHAP-based explanation of individual predictions.
- CSV batch analysis.
- Risk prioritization.
- Automated generation of analysis_results.csv and security_report.txt.
- Input validation for missing files, missing columns, and negative values.
- Menu-based command-line interface.

## 6. System Architecture
User Input → Input Validation → Random Forest Model → Prediction → SHAP Explanation for individual events.

For CSV analysis: CSV Input → Validation → Model Prediction → Risk Prioritization → analysis_results.csv and security_report.txt.

## 7. Project Files
- main.py — main command-line application.
- train_model.py — model training workflow.
- explain_model.py — prediction explanation functionality.
- csv_analyzer.py — CSV analysis and risk prioritization.
- threat_model.pkl — saved model, if included.
- test_logs.csv — sample input data.

## 8. How the Project Works
1. Run the application from a terminal.
2. Select single-event analysis or CSV batch analysis.
3. Provide the required input data.
4. The model predicts whether an event is Suspicious or Normal.
5. SHAP provides feature-contribution explanations for individual predictions.
6. CSV analysis assigns demonstration risk levels and generates report files.

## 9. Risk Prioritization
The current prototype uses these demonstration thresholds:
- HIGH: score >= 0.80
- MEDIUM: score >= 0.50 and < 0.80
- LOW: score < 0.50

These are demonstration thresholds, not industry standards. Interpret the score according to the actual implementation.

## 10. Sample Input
```csv
failed_logins,api_requests
10,200
1,20
5,100
```

In the current demonstration run, this three-row sample produced two Suspicious predictions and one Normal prediction, with one event each categorized HIGH, MEDIUM, and LOW. Results may change if the model or data changes.

## 11. Installation and Execution
1. Install Python.
2. Open a terminal in the project directory.
3. Activate the virtual environment if one is used.
4. Install dependencies if a requirements.txt file is provided:
   ```bash
   python -m pip install -r requirements.txt
   ```
5. Run the application:
   ```bash
   python main.py
   ```

If the model file is missing, run python train_model.py if that matches the project's training workflow.

## 12. Testing
The prototype was checked for:
- Single-event prediction with SHAP explanation.
- Valid CSV batch analysis.
- Risk categorization.
- Viewing the latest report summary.
- Missing-file handling.
- Missing required CSV columns.
- Negative-value validation.

## 13. Limitations
- This is an academic prototype using synthetic/sample data.
- The described model uses two features: failed login attempts and API request counts.
- Real-world model accuracy has not been established.
- Live AWS CloudTrail, GuardDuty, or VPC Flow Logs integration is not established in the current workflow.
- Risk thresholds are demonstration settings.
- SHAP explains model behavior but does not prove malicious intent.
- This project is not a production security monitoring system.

## 14. Future Enhancements
- Evaluate the model using an authorized, representative security dataset.
- Measure precision, recall, F1-score, and false-positive rates.
- Improve feature engineering and validate risk thresholds.
- Add automated tests and reproducible dependency versions.
- Explore secure AWS integration with least-privilege permissions.
- Add alerting and analyst feedback workflows.

## 15. Security and Privacy
Never upload passwords, AWS credentials, API keys, personal information, or confidential security logs to this repository.

## 16. Conclusion
This project demonstrates the use of machine learning and explainable AI for sample security event classification, CSV log analysis, risk prioritization, and report generation. It is intended for academic learning and demonstration. Further evaluation and secure integration would be required before operational use.
