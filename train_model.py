
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Sample training dataset for learning
data = {
    "failed_logins": [
        0, 1, 0, 2, 1, 3, 0, 2,
        8, 10, 12, 7, 15, 9, 11, 8,
        1, 0, 3, 2, 9, 14, 1, 10
    ],
    "api_requests": [
        10, 15, 12, 20, 18, 25, 8, 22,
        150, 200, 250, 130, 300, 180, 220, 160,
        14, 9, 30, 16, 170, 280, 12, 210
    ],
    "label": [
        0, 0, 0, 0, 0, 0, 0, 0,
        1, 1, 1, 1, 1, 1, 1, 1,
        0, 0, 0, 0, 1, 1, 0, 1
    ]
}

df = pd.DataFrame(data)

X = df[["failed_logins", "api_requests"]]
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

print("\nAI THREAT DETECTION MODEL")
print("=" * 40)
print(classification_report(
    y_test,
    predictions,
    target_names=["Normal", "Suspicious"],
    zero_division=0
))

# Test a new example
new_event = pd.DataFrame({
    "failed_logins": [10],
    "api_requests": [200]
})

prediction = model.predict(new_event)[0]
probability = model.predict_proba(new_event)[0][1]

print("New event prediction:",
      "SUSPICIOUS" if prediction == 1 else "NORMAL")
print(f"Model-estimated suspicious probability: {probability:.2%}")
joblib.dump(model, "threat_model.pkl")
print("Model saved successfully!")
