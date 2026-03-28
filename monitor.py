import pandas as pd

df = pd.read_csv("data/web_traffic.csv")

if len(df) < 1000:
    print("⚠️ WARNING: Low data volume!")
else:
    print("✅ Data volume is healthy")