import pandas as pd

df = pd.read_csv("data/web_traffic.csv")

print("🔍 Checking data quality...")

print("Missing values:\n", df.isnull().sum())

print("\nUnique sources:", df["source"].unique())

# Check invalid timestamps
df["timestamp"] = pd.to_datetime(df["timestamp"], errors='coerce')

invalid = df[df["timestamp"].isnull()]

print(f"\nInvalid timestamps: {len(invalid)}")

print("\n✅ Validation Complete")