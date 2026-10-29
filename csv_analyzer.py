
import pandas as pd
import joblib

# Load the trained model
model = joblib.load("threat_model.pkl")

# Read the CSV file
file_name = input("Enter CSV file path: ").strip().strip('"')
data = pd.read_csv(file_name)

# Check required columns
required = ["failed_logins", "api_requests"]

if not all(col in data.columns for col in required):
    print("Error: CSV must contain these columns:")
    print(", ".join(required))

else:
    # Predict threats
    predictions = model.predict(data[required])
    probabilities = model.predict_proba(data[required])[:, 1]

    # Add prediction and probability
    data["prediction"] = [
        "SUSPICIOUS" if p == 1 else "NORMAL"
        for p in predictions
    ]

    data["suspicious_probability"] = probabilities.round(4)

    # Risk prioritization
    def risk_level(probability):
        if probability >= 0.80:
            return "HIGH"
        elif probability >= 0.50:
            return "MEDIUM"
        else:
            return "LOW"

    data["risk_level"] = [
        risk_level(p) for p in probabilities
    ]

    # Sort highest risk first
    risk_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    data["_risk_order"] = data["risk_level"].map(risk_order)

    data = data.sort_values(
        by=["_risk_order", "suspicious_probability"],
        ascending=[True, False]
    ).drop(columns=["_risk_order"])

    # Save results
    output_file = "analysis_results.csv"
    data.to_csv(output_file, index=False)

    # Display summary
    print("\nCLOUD THREAT ANALYSIS")
    print("=" * 40)

    print(data[
        ["failed_logins", "api_requests",
         "prediction", "suspicious_probability", "risk_level"]
    ].to_string(index=False))

    print("\nRisk Summary:")
    print(data["risk_level"].value_counts().to_string())

    print(f"\nResults saved to {output_file}")
