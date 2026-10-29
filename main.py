
from pathlib import Path
import joblib
import pandas as pd
import shap
import numpy as np

MODEL_FILE = Path("threat_model.pkl")
FEATURES = ["failed_logins", "api_requests"]
OUTPUT_FILE = Path("analysis_results.csv")
REPORT_FILE = Path("security_report.txt")


def load_model():
    if not MODEL_FILE.exists():
        print("Model file not found:", MODEL_FILE)
        return None

    try:
        return joblib.load(MODEL_FILE)
    except Exception as exc:
        print("Could not load model:", exc)
        return None


def get_risk(probability):
    if probability >= 0.80:
        return "HIGH"
    elif probability >= 0.50:
        return "MEDIUM"
    return "LOW"


def explain_prediction(model, event):
    prediction = int(model.predict(event)[0])
    probabilities = model.predict_proba(event)[0]
    suspicious_probability = float(probabilities[1])

    print("\n--- THREAT PREDICTION ---")
    print("Prediction:", "SUSPICIOUS" if prediction == 1 else "NORMAL")
    print(f"Suspicious probability: {suspicious_probability:.2%}")
    print("Risk level:", get_risk(suspicious_probability))

    try:
        explainer = shap.TreeExplainer(model)
        values = explainer.shap_values(event)

        if isinstance(values, list):
            individual = np.asarray(values[1])[0]
        else:
            values = np.asarray(values)
            if values.ndim == 3:
                individual = values[0, :, 1]
            elif values.ndim == 2:
                individual = values[0]
            else:
                print("Unexpected SHAP output format.")
                return

        print("\n--- SHAP EXPLANATION ---")
        for name, value in zip(FEATURES, individual):
            direction = (
                "towards SUSPICIOUS" if value > 0
                else "away from SUSPICIOUS" if value < 0
                else "no directional contribution"
            )
            print(f"{name}: {value:.4f} ({direction})")

    except Exception as exc:
        print("SHAP explanation could not be generated:", exc)

    print("\nNote: Model predictions require real-data validation.")


def single_event_analysis(model):
    try:
        failed = int(input("Number of failed logins: "))
        requests = int(input("Number of API requests: "))

        if failed < 0 or requests < 0:
            print("Values cannot be negative.")
            return

        event = pd.DataFrame(
            [[failed, requests]], columns=FEATURES
        )
        explain_prediction(model, event)

    except ValueError:
        print("Please enter valid whole numbers.")


def csv_analysis(model):
    filename = input("Enter CSV path (example: test_logs.csv): ")
    filename = filename.strip().strip('"')

    try:
        data = pd.read_csv(filename)

        if not all(column in data.columns for column in FEATURES):
            print("CSV must contain:", ", ".join(FEATURES))
            return

        if data.empty:
            print("The CSV file has no records.")
            return

        for column in FEATURES:
            data[column] = pd.to_numeric(data[column], errors="raise")

        if data[FEATURES].isna().any().any():
            print("CSV contains missing feature values.")
            return

        if (data[FEATURES] < 0).any().any():
            print("Feature values cannot be negative.")
            return

        predictions = model.predict(data[FEATURES])
        probabilities = model.predict_proba(data[FEATURES])[:, 1]

        data["prediction"] = [
            "SUSPICIOUS" if int(p) == 1 else "NORMAL"
            for p in predictions
        ]
        data["suspicious_probability"] = probabilities.round(4)
        data["risk_level"] = [
            get_risk(float(p)) for p in probabilities
        ]

        order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
        data["_order"] = data["risk_level"].map(order)
        data = data.sort_values(
            ["_order", "suspicious_probability"],
            ascending=[True, False]
        ).drop(columns="_order")

        data.to_csv(OUTPUT_FILE, index=False)
        create_report(data)

        print("\n--- CSV ANALYSIS RESULTS ---")
        print(data.to_string(index=False))
        print("\nRisk summary:")
        print(data["risk_level"].value_counts().to_string())
        print("\nSaved results:", OUTPUT_FILE)
        print("Saved report:", REPORT_FILE)

    except FileNotFoundError:
        print("CSV file not found. Check its path.")
    except (ValueError, TypeError) as exc:
        print("Invalid CSV data:", exc)
    except Exception as exc:
        print("Analysis failed:", exc)


def create_report(data):
    total = len(data)
    suspicious = int((data["prediction"] == "SUSPICIOUS").sum())
    counts = data["risk_level"].value_counts()

    lines = [
        "CLOUD SECURITY THREAT ANALYSIS REPORT",
        "=" * 42,
        f"Total records analysed: {total}",
        f"Suspicious predictions: {suspicious}",
        f"Normal predictions: {total - suspicious}",
        "",
        "Risk category counts:",
        f"HIGH: {int(counts.get('HIGH', 0))}",
        f"MEDIUM: {int(counts.get('MEDIUM', 0))}",
        f"LOW: {int(counts.get('LOW', 0))}",
        "",
        f"Detailed results file: {OUTPUT_FILE}",
        "",
        "IMPORTANT LIMITATIONS",
        "This model was trained on a small synthetic dataset.",
        "Risk thresholds are demonstration settings, not validated standards.",
        "Predictions do not confirm that a real attack occurred.",
        "Validate using representative, labelled cloud-security data.",
    ]

    REPORT_FILE.write_text("\n".join(lines), encoding="utf-8")


def main():
    model = load_model()
    if model is None:
        return

    while True:
        print("\n" + "=" * 42)
        print("EXPLAINABLE AI CLOUD THREAT ANALYZER")
        print("=" * 42)
        print("1. Analyse a single event")
        print("2. Analyse a CSV log file")
        print("3. View latest report summary")
        print("4. Exit")

        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            single_event_analysis(model)
        elif choice == "2":
            csv_analysis(model)
        elif choice == "3":
            if REPORT_FILE.exists():
                print("\n" + REPORT_FILE.read_text(encoding="utf-8"))
            else:
                print("No report yet. Run CSV analysis first.")
        elif choice == "4":
            print("Thank you. Exiting analyzer.")
            break
        else:
            print("Invalid choice. Enter 1, 2, 3 or 4.")


if __name__ == "__main__":
    main()
