import pandas as pd
import random
from datetime import datetime, timedelta

traffic = []

pages = ["Home", "Product", "Cart", "Checkout", "Search", "Profile"]
actions = ["view", "click", "login", "logout"]
sources = ["Google", "Direct", "Instagram", "Facebook", "Ads"]

# 🔥 MAKE DATA HUGE
for _ in range(5000):   # increase this number for more data
    user = random.randint(1, 200)
    session = random.randint(1000, 5000)

    for step in pages:
        traffic.append([
            user,
            session,
            step,
            random.choice(actions),
            datetime.now() - timedelta(days=random.randint(0, 30)),
            random.choice(sources)
        ])

traffic_df = pd.DataFrame(traffic, columns=[
    "user_id", "session_id", "page", "action", "timestamp", "source"
])

traffic_df.to_csv("data/web_traffic.csv", index=False)

print("✅ Data Generated Successfully!")