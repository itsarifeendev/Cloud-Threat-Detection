
import joblib
import pandas as pd
import shap
import numpy as np

# Load the saved model
model = joblib.load("threat_model.pkl")

# Example event to explain
event = pd.DataFrame({
    "failed_logins": [10],
    "api_requests": [200]
})

# Predict the threat
prediction = model.predict(event)[0]
probabilities = model.predict_proba(event)[0]

print("\nEXPLAINABLE AI - THREAT ANALYSIS")
print("=" * 40)
print("Prediction:", "SUSPICIOUS" if prediction == 1 else "NORMAL")
print(f"Normal probability: {probabilities[0]:.2%}")
print(f"Suspicious probability: {probabilities[1]:.2%}")

print("\nInput features:")
print(event.to_string(index=False))

# Explain this individual prediction with SHAP
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(event)

# Support different SHAP output formats
if isinstance(shap_values, list):
    individual_values = shap_values[1][0]
else:
    values = np.asarray(shap_values)
    if values.ndim == 3:
        individual_values = values[0, :, 1]
    else:
        individual_values = values[0]

print("\nINDIVIDUAL FEATURE EXPLANATION")
print("=" * 40)

for name, value in zip(event.columns, individual_values):
    direction = (
        "towards SUSPICIOUS"
        if value > 0
        else "away from SUSPICIOUS"
        if value < 0
        else "no contribution"
    )
    print(f"{name}: {value:.4f} ({direction})")

print("\nGlobal model feature importance:")
for name, importance in zip(
    event.columns, model.feature_importances_
):
    print(f"{name}: {importance:.4f}")

print("\nNote: SHAP explains the model output.")
print("It does not prove that a real attack occurred.")
