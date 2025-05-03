import pandas as pd
import matplotlib.pyplot as plt

# Load structured data
df = pd.read_csv("C:/Waseem/gym-log-parser/data/structured_gym_log.csv")

# Step 1: Calculate Volume
df["Volume"] = df["Weight (kg)"] * df["Reps"] * df["Sets"]

# Step 2: Group by Date and Exercise
exercise_volume = df.groupby(["Date", "Exercise"])["Volume"].sum().reset_index()

# Step 3: Full list of all dates
all_dates = pd.date_range(start=df["Date"].min(), end=df["Date"].max())

# Step 4: List of exercises you want
target_exercises = ["Bench Press", "Squats", "Deadlifts"]

# Step 5: Plot
plt.figure(figsize=(14, 8))

for exercise in target_exercises:
    exercise_df = exercise_volume[exercise_volume["Exercise"].str.lower() == exercise.lower()]
    
    exercise_df["Date"] = pd.to_datetime(exercise_df["Date"])
    exercise_df = exercise_df.set_index("Date")
    exercise_df = exercise_df.reindex(all_dates)  # Reindex to full dates
    exercise_df = exercise_df.dropna(subset=["Volume"])  # Drop missing days for clean line

    plt.plot(
        exercise_df.index, 
        exercise_df["Volume"], 
        marker='o', 
        linestyle='-', 
        linewidth=2, 
        label=exercise
    )

plt.title("Training Volume Over Time by Exercise")
plt.xlabel("Date")
plt.ylabel("Volume (kg × reps × sets)")
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()


