import pandas as pd
import matplotlib.pyplot as plt

# Load structured data
df = pd.read_csv("C:/Waseem/gym-log-parser/data/structured_gym_log.csv")

# Step 1: Filter for specific exercise
exercise_name = "Squats"
exercise_df = df[df["Exercise"].str.lower() == exercise_name.lower()]

# Step 2: Get top set (max weight) per day
top_sets = exercise_df.groupby("Date")["Weight (kg)"].max().reset_index()

# Step 3: Plot
plt.figure(figsize=(10,6))
plt.plot(top_sets["Date"], top_sets["Weight (kg)"], marker='o', linestyle='-')
plt.title(f"{exercise_name} Top Set Over Time")
plt.xlabel("Date")
plt.ylabel("Top Set Weight (kg)")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()



