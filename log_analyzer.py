import pandas as pd

data = {
    "source_ip": [
        "192.168.1.10",
        "192.168.1.15",
        "203.0.113.25",
        "203.0.113.25",
        "203.0.113.25"
    ],
    "failed_logins": [0, 1, 2, 8, 12],
    "api_requests": [10, 15, 20, 150, 250]
}

df = pd.DataFrame(data)

df["risk_score"] = (
    (df["failed_logins"] * 5)
    + (df["api_requests"] * 0.2)
)

df["risk_level"] = df["risk_score"].apply(
    lambda score: (
        "HIGH" if score >= 50
        else "MEDIUM" if score >= 20
        else "LOW"
    )
)

print("\nCLOUD SECURITY LOG ANALYSIS")
print("=" * 50)
print(df.to_string(index=False))