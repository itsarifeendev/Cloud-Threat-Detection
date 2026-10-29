# Explainable AI-Based Cloud Security Threat Detection and Risk Prioritization

> A Python command-line prototype that classifies sample security events, explains individual predictions with SHAP, analyzes CSV log batches, and prioritizes events into risk levels.

## 1. Project Overview

Cloud environments generate security-related events continuously. Reviewing each event manually can be time-consuming, and a raw prediction is difficult to trust when an analyst cannot understand why a model flagged an event.

This project demonstrates a small, explainable AI workflow for sample cloud-security event data. A Random Forest classifier predicts whether an event is **Suspicious** or **Normal** using two input features:

- `failed_logins` — number of failed login attempts represented by the event.
- `api_requests` — number of API requests represented by the event.

For a single event, the program displays a prediction and uses **SHAP (SHapley Additive exPlanations)** to help explain the model's output. For batch analysis, it reads a CSV file, predicts outcomes for each row, assigns a demo risk level, and writes analysis results and a text summary report.

**Project status:** Academic / demonstration prototype. It uses a synthetic or sample dataset and is not a production cloud security monitoring service.

## 2. Problem Statement

Security teams need ways to review potentially suspicious activity efficiently. A machine-learning prediction by itself may be difficult to interpret, while large log files can be tedious to review row by row. This project demonstrates a workflow that combines event classification, explainability, batch analysis, and risk prioritization in one command-line tool.

## 3. Objectives

1. Build a machine-learning model that classifies sample security events.
2. Explain individual model predictions using SHAP.
3. Analyze multiple events from a CSV file.
4. Prioritize events using configurable demonstration risk thresholds.
5. Generate machine-readable results and a human-readable summary report.
6. Validate expected behavior for valid input and common input errors.

## 4. Main Features

- **Single-event analysis:** Enter failed-login and API-request values to receive a prediction.
- **Explainable prediction:** Display SHAP-based feature contributions for an individual prediction.
- **CSV batch analysis:** Process multiple events from a CSV file.
- **Risk prioritization:** Assign `HIGH`, `MEDIUM`, or `LOW` based on the demo score.
- **Generated outputs:** Save batch results to `analysis_results.csv` and a summary to `security_report.txt`.
- **Input validation:** Handle missing files, missing required columns, and negative feature values.
- **Menu-based CLI:** Choose single-event analysis, CSV analysis, report summary, or exit.

## 5. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| pandas | CSV loading and tabular data processing |
| NumPy | Numerical operations where used |
| scikit-learn | Random Forest machine-learning model |
| SHAP | Explaining model predictions |
| joblib | Saving/loading the trained model |
| Command Prompt / Terminal | Running the command-line application |

Confirm exact dependencies against the repository's `requirements.txt` or Python imports before publishing.

## 6. System Architecture

```text
User
 |
 v
Command-line menu (main.py)
 |
 +--> Single event input
 |       |
 |       v
 |   Trained Random Forest model
 |       |
 |       +--> Prediction: Suspicious / Normal
 |       |
 |       +--> SHAP explanation
 |
 +--> CSV log file
         |
         v
     Validate required columns and values
         |
         v
     Model predictions and risk scoring
         |
         +--> analysis_results.csv
         |
         +--> security_report.txt
```

### Main components

- `main.py` — command-line entry point and menu.
- `train_model.py` — training workflow for the demonstration model.
- `threat_model.pkl` — serialized trained model, if included.
- `explain_model.py` — SHAP explanation functionality.
- `csv_analyzer.py` — CSV batch analysis and risk prioritization.
- `test_logs.csv` — small sample input dataset.

Check the repository if your local filenames differ.

## 7. How It Works

### A. Model training
The training script prepares demonstration data and trains a Random Forest classifier using `failed_logins` and `api_requests`. The trained model is saved as `threat_model.pkl` for reuse. Since the data is synthetic/sample data, predictions demonstrate the workflow rather than validated real-world threat detection.

### B. Single-event prediction
1. Select **Analyse a single event**.
2. Enter the two feature values.
3. The model predicts **Suspicious** or **Normal**.
4. The explanation module displays SHAP-based feature contributions, according to the implementation.

### C. CSV batch analysis
1. Select **Analyse a CSV log file**.
2. Supply a CSV file.
3. The program checks for `failed_logins` and `api_requests`.
4. Negative feature values are rejected.
5. The model predicts each row and assigns a demonstration risk level.
6. The program writes `analysis_results.csv` and `security_report.txt`.

### D. Risk prioritization
The prototype uses these demonstration thresholds:

| Risk level | Demo score |
|---|---|
| HIGH | 0.80 or higher |
| MEDIUM | 0.50 or higher, but below 0.80 |
| LOW | Below 0.50 |

These are **prototype thresholds**, not industry-standard cut-offs. Interpret the score according to the actual code; do not assume it is a calibrated probability unless validated.

## 8. Requirements

- Python installed on the computer.
- Project files downloaded or cloned locally.
- Required Python packages installed.
- A CSV file with the required columns for batch analysis.

Recommended packages include `pandas`, `numpy`, `scikit-learn`, `shap`, and `joblib`; install `matplotlib` if the code imports it. Confirm exact dependencies and versions from the repository.

## 9. Installation and Setup

### Clone the repository
Replace `YOUR-USERNAME` with your GitHub username after publishing:

```bash
git clone https://github.com/YOUR-USERNAME/Cloud-Threat-Detection.git
cd Cloud-Threat-Detection
```

### Create and activate a virtual environment

**Windows PowerShell:**
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**
```bat
py -m venv .venv
.venv\Scripts\activate.bat
```

### Install dependencies
If `requirements.txt` exists:

```bash
python -m pip install -r requirements.txt
```

### Run the application
```bash
python main.py
```

The menu offers:
1. Analyse a single event
2. Analyse a CSV log file
3. View latest report summary
4. Exit

If the model file is absent, run `python train_model.py` if that matches the implementation and training workflow.

## 10. Sample CSV Input

Save as `test_logs.csv`:

```csv
failed_logins,api_requests
10,200
1,20
5,100
```

In the current demonstration run, this three-row sample produced:

- Total records: **3**
- Suspicious predictions: **2**
- Normal predictions: **1**
- Risk levels: **1 HIGH, 1 MEDIUM, 1 LOW**

These figures describe this specific synthetic sample and current model run. They are not a real-world performance benchmark. Results may change if data, training, preprocessing, or code changes.

## 11. Output Files

| File | Purpose |
|---|---|
| `analysis_results.csv` | Row-level batch predictions and risk information |
| `security_report.txt` | Human-readable summary of the latest analysis |
| `test_logs.csv` | Sample input dataset |
| `test_results.csv` | Test output, if generated locally |
| `invalid_logs.csv` | Invalid-input test file, if used locally |

Generated outputs can be recreated. Consider excluding temporary output files from Git. Never publish real security logs or sensitive data.

## 12. Testing and Validation

| Test | Scenario | Expected / observed behavior |
|---|---|---|
| TC01 | Single event: 10 failed logins, 200 API requests | Prediction displayed with SHAP explanation |
| TC02 | Valid three-row CSV | Batch analysis completed |
| TC03 | Risk prioritization | HIGH / MEDIUM / LOW assigned using demo thresholds |
| TC04 | View report summary | Latest report summary displayed |
| TC05 | Missing CSV path | File-not-found error displayed |
| TC06 | Required columns missing | Message indicates `failed_logins` and `api_requests` are required |
| TC07 | Negative feature value | `Feature values cannot be negative.` |

These are functional checks, not a formal security evaluation. They do not establish precision, recall, false-positive rate, or production readiness.

## 13. Limitations

- The project is a prototype and uses synthetic/sample data.
- The described model uses only two input features.
- Real-world predictive accuracy has not been established.
- Live AWS CloudTrail, GuardDuty, or VPC Flow Logs integration is not established by this CLI workflow.
- Risk thresholds are demonstration settings and may require calibration.
- SHAP explains model behavior; it does not prove that an event is malicious or establish causation.
- The tool does not replace a security analyst, incident response process, or production monitoring platform.

## 14. Future Enhancements

- Evaluate with a representative, authorized security dataset.
- Report precision, recall, F1-score, confusion matrix, and false-positive/false-negative rates.
- Add validated features and document data provenance.
- Calibrate model scores and risk thresholds with domain experts.
- Add unit tests, structured logging, and reproducible dependency versions.
- Explore secure AWS integration with least-privilege permissions and safe log handling.
- Add alerting and analyst feedback workflows.

## 15. Security and Privacy

- Never commit AWS access keys, passwords, API tokens, `.env` files, or credentials.
- Do not upload confidential, personal, or real customer security logs.
- Use least-privilege access if cloud integrations are added later.
- Treat predictions as decision-support output, not automatic incident-response authority.

## 16. Conclusion

This project demonstrates a local, explainable machine-learning workflow for sample security event analysis. It combines Random Forest classification, SHAP explanations, CSV batch processing, demonstration risk prioritization, and report generation. Its current value is educational and prototypical; realistic evaluation and secure integration would be required before operational use.

## 17. Repository Maintenance

Before publishing, verify filenames, dependencies, and run commands against the actual repository. Add screenshots only if they contain no sensitive information. Choose a license only if you intend to grant reuse rights and can legally redistribute all included material.
